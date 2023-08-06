###############################################################################
#
# Crossbar.io Fabric Center
# Copyright (c) Crossbar.io Technologies GmbH. All rights reserved.
#
###############################################################################

from zlmdb import table
from zlmdb import MapOidCbor, MapOidOidSet, MapOidTimestampStringOid

from .eventhistory import ZdbEvent


@table('9cbbac57-a810-4c08-b232-339ad3e0cb10', marshal=ZdbEvent.marshal, parse=ZdbEvent.parse)
class ZdbEvents(MapOidCbor):
    """
    Persisted events archive. Map of ``publication_id`` to ``PersistedEvent``.
    """


@table('2e86bf86-25a2-4016-8d8b-49c98d0f72ac')
class ZdbEventSubscriptions(MapOidOidSet):
    """
    Persisted event subscriptions. Map of ``publication_id`` to set of ``subscription_id``s.
    """


@table('e9bebf28-f109-45ad-8c89-c93b884e3e50')
class ZdbEventHistory(MapOidTimestampStringOid):
    """
    Persisted event history. Map of ``(trace_id, timestamp, uri)`` to ``publication_id``.
    """


import txaio
txaio.use_twisted()

__all__ = ('ZdbSchema', )

log = txaio.make_logger()


class ZdbSchema(object):
    """
    CFC edge database schema for ZLMDB.
    """

    def __init__(self, db):
        self.db = db

    # event_archive: ZdbEvents
    event_archive = None
    """
    Event archive.
    """

    # event_subscriptions: ZdbEventSubscriptions
    event_subscriptions = None
    """
    Subscriptions an event was dispatched to.
    """

    # event_history: ZdbEventHistory
    event_history = None
    """
    Persisted event history.
    """

    @staticmethod
    def attach(db):
        """
        Factory to create a schema from attaching to a database. The schema tables
        will be automatically mapped as persistant maps and attached to the
        database slots.

        :param db: zlmdb.Database
        :return: object of Schema
        """
        log.info('Attaching database schema to database {db} ..', db=db)

        schema = ZdbSchema(db)

        schema.event_archive = db.attach_table(ZdbEvents)
        schema.event_subscriptions = db.attach_table(ZdbEventSubscriptions)
        schema.event_history = db.attach_table(ZdbEventHistory)

        log.info('Successfully attached schema {schema} to database {db}.', schema=schema, db=db)

        return schema
