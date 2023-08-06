##############################################################################
#
#                        Crossbar.io Fabric
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from __future__ import absolute_import, division

from collections import deque

import zlmdb

from .eventhistory import ZdbEvent
from .schema import ZdbSchema

__all__ = ('ZdbRealmStore', )


class QueuedCall(object):

    __slots__ = ('session', 'call', 'registration', 'authorization')

    def __init__(self, session, call, registration, authorization):
        self.session = session
        self.call = call
        self.registration = registration
        self.authorization = authorization


class ZdbCallQueue(object):
    """
    ZLMDB-backed call queue.
    """

    GLOBAL_QUEUE_LIMIT = 1000
    """
    The global call queue limit, in case not overridden.
    """

    def __init__(self, db, schema, config):
        """

        See the example here:

        https://github.com/crossbario/crossbar-examples/tree/master/scaling-microservices/queued

        .. code-block:: json

            "store": {
                "type": "memory",
                "limit": 1000,      // global default for limit on call queues
                "call-queue": [
                    {
                        "uri": "com.example.compute",
                        "match": "exact",
                        "limit": 10000  // procedure specific call queue limit
                    }
                ]
            }
        """
        self.log = db.log

        self._db = db
        self._schema = schema

        # whole store configuration
        self._config = config

        # limit to call queue per registration
        self._limit = self._config.get('limit', self.GLOBAL_QUEUE_LIMIT)

        # map: registration.id -> deque( (session, call, registration, authorization) )
        self._queued_calls = {}

    def maybe_queue_call(self, session, call, registration, authorization):
        # FIXME: match this against the config, not just plain accept queueing!
        if registration.id not in self._queued_calls:
            self._queued_calls[registration.id] = deque()

        self._queued_calls[registration.id].append(QueuedCall(session, call, registration, authorization))

        return True

    def get_queued_call(self, registration):
        if registration.id in self._queued_calls and self._queued_calls[registration.id]:
            return self._queued_calls[registration.id][0]

    def pop_queued_call(self, registration):
        if registration.id in self._queued_calls and self._queued_calls[registration.id]:
            return self._queued_calls[registration.id].popleft()


class ZdbEventStore(object):
    """
    ZLMDB-backed event store.
    """

    GLOBAL_HISTORY_LIMIT = 100
    """
    The global history limit, in case not overridden.
    """

    STORE_TYPE = 'zlmdb'

    def __init__(self, db, schema, config):
        self.log = db.log
        self._db = db
        self._schema = schema
        self._config = config
        self._max_buffer = config.get('max-buffer', 10000)
        self._buffer_flush = config.get('buffer-flush', 200)
        self._buffer = {}
        self._log_counter = 0

    def attach_subscription_map(self, subscription_map):
        for sub in self._config.get('event-history', []):
            uri = sub['uri']
            match = sub.get('match', u'exact')
            observation, was_already_observed, was_first_observer = subscription_map.add_observer(
                self, uri=uri, match=match)
            subscription_id = observation.id

            # in-memory buffer
            self._buffer[subscription_id] = deque()

    def store_event(self, session, publication_id, publish):
        """
        Store event to event history.

        :param session: The publishing session.
        :type session: :class:`autobahn.wamp.interfaces.ISession`

        :param publication_id: The WAMP publication ID under which the publish happens
        :type publication_id: int

        :param publish: The WAMP publish message.
        :type publish: :class:`autobahn.wamp.messages.Publish`
        """
        with self._db.begin(write=True) as txn:

            evt = self._schema.event_archive[txn, publication_id]
            if evt:
                raise Exception('duplicate event for publication_id={}'.format(publication_id))

            evt = ZdbEvent()
            evt.time_ns = zlmdb.time_ns()
            evt.realm = session._realm
            evt.session_id = session._session_id
            evt.authid = session._authid
            evt.authrole = session._authrole
            evt.publication_id = publication_id
            evt.topic = publish.topic
            evt.args = publish.args
            evt.kwargs = publish.kwargs

            self._schema.event_archive[txn, publication_id] = evt

            if self._log_counter % 1000 == 0:
                current = self._schema.event_archive.count(txn)
                self.log.info(
                    "Event {publication_id} stored in {store_type}-store. Total records currently in store: {current}",
                    store_type=self.STORE_TYPE,
                    publication_id=publication_id,
                    current=current)
            self._log_counter += 1

    def store_event_history(self, publication_id, subscription_id):
        """
        Store publication history for subscription.

        :param publication_id: The ID of the event publication to be persisted.
        :type publication_id: int

        :param subscription_id: The ID of the subscription the event (identified by the publication ID),
            was published to, because the event's topic matched the subscription.
        :type subscription_id: int
        """
        assert type(publication_id) == int
        assert type(subscription_id) == int

        # ZdbEventSubscriptions(MapOidOidSet):
        with self._db.begin(write=True) as txn:

            subs = self._schema.event_subscriptions[txn, publication_id]
            if not subs:
                subs = set()
            subs.add(subscription_id)
            self._schema.event_subscriptions[txn, publication_id] = subs

            # event_history
            # map: (trace_id, timestamp, uri) -> publication_id
            # map: (uri, timestamp) -> publication_id

        self.log.debug(
            "Event {publication_id} history persisted for subscription {subscription_id}",
            publication_id=publication_id,
            subscription_id=subscription_id)

    def get_events(self, subscription_id, limit):
        """
        Retrieve given number of last events for a given subscription.

        If no history is maintained for the given subscription, None is returned.

        :param subscription_id: The ID of the subscription to retrieve events for.
        :type subscription_id: int
        :param limit: Limit number of events returned.
        :type limit: int

        :return: List of events: at most ``limit`` events in reverse chronological order.
        :rtype: list or None
        """
        assert type(subscription_id) == int
        assert type(limit) == int

        with self._db.begin() as txn:
            res = []
            i = 0
            for evt in self._schema.event_history.select(txn):
                res.append(evt.marshal())
                i += 1
                if i >= limit:
                    break

        return res

    def get_event_history(self, subscription_id, from_ts, until_ts):
        """
        Retrieve event history for time range for a given subscription.

        If no history is maintained for the given subscription, None is returned.

        :param subscription_id: The ID of the subscription to retrieve events for.
        :type subscription_id: int
        :param from_ts: Filter events from this date (string in ISO-8601 format).
        :type from_ts: unicode
        :param until_ts: Filter events until this date (string in ISO-8601 format).
        :type until_ts: unicode
        """
        raise Exception("not implemented")


class ZdbRealmStore(object):
    """
    ZLMDB backed realm store.

    See the example here:

    https://github.com/crossbario/crossbar-examples/tree/master/event-history

    "store": {
        "type": "zlmdb",
        "max-buffer": 100,
        "buffer-flush": 200,
        "path": "../mydb1",
        "event-history": [
            {
                "uri": "com.example.oncounter",
                "match": "exact"
            }
        ]
    }
    """

    event_store = None
    """
    Store for event history.
    """

    call_store = None
    """
    Store for call queueing.
    """

    def __init__(self, personality, factory, config):
        """

        :param config: Realm store configuration item.
        :type config: Mapping
        """
        dbfile = config.get('path', None)
        assert type(dbfile) == str

        maxsize = config.get('maxsize', 128 * 2**20)
        assert type(maxsize) == int
        # allow maxsize 128kiB to 128GiB
        assert maxsize >= 128 * 1024 and maxsize <= 128 * 2**30

        readonly = config.get('readonly', False)
        assert type(readonly) == bool

        sync = config.get('sync', True)
        assert type(sync) == bool

        self.log = personality.log

        self._db = zlmdb.Database(dbfile=dbfile, maxsize=maxsize, readonly=readonly, sync=sync)
        self._db.__enter__()
        self._schema = ZdbSchema.attach(self._db)

        self.event_store = ZdbEventStore(self._db, self._schema, config)
        self.call_store = ZdbCallQueue(self._db, self._schema, config)

        self.log.info('Realm store initialized (type=zlmdb, dbfile="{dbfile}", maxsize={maxsize}, readonly={readonly}, sync={sync})',
                      dbfile=dbfile, maxsize=maxsize, readonly=readonly, sync=sync)
