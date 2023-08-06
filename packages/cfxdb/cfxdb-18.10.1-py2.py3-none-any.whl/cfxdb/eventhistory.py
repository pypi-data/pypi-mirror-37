##############################################################################
#
#                        Crossbar.io Fabric
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import pprint


class ZdbEvent(object):
    def __init__(self,
                 time_ns=None,
                 realm=None,
                 session_id=None,
                 authid=None,
                 authrole=None,
                 publication_id=None,
                 topic=None,
                 args=None,
                 kwargs=None):
        self.time_ns = time_ns
        self.realm = realm
        self.session_id = session_id
        self.authid = authid
        self.authrole = authrole
        self.publication_id = publication_id
        self.topic = topic
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return '\n{}\n'.format(pprint.pformat(self.marshal()))

    def marshal(self):
        assert type(self.time_ns) == int
        assert type(self.realm) == str
        assert type(self.session_id) == int
        assert type(self.authid) == str
        assert type(self.authrole) == str
        assert type(self.publication_id) == int
        assert type(self.topic) == str
        assert self.args is None or type(self.args) == list
        assert self.kwargs is None or type(self.kwargs) == dict

        obj = {
            'time_ns': self.time_ns,
            'realm': self.realm,
            'session_id': self.session_id,
            'authid': self.authid,
            'authrole': self.authrole,
            'publication_id': self.publication_id,
            'topic': self.topic,
            'args': self.args,
            'kwargs': self.kwargs,
        }
        return obj

    @staticmethod
    def parse(data):
        assert type(data) == dict

        time_ns = data.get('time_ns', None)
        realm = data.get('realm', None)
        session_id = data.get('session_id', None)
        authid = data.get('authid', None)
        authrole = data.get('authrole', None)
        publication_id = data.get('publication_id', None)
        topic = data.get('topic', None)
        args = data.get('args', None)
        kwargs = data.get('kwargs', None)

        assert type(time_ns) == int
        assert type(realm) == str
        assert type(session_id) == int
        assert type(authid) == str
        assert type(authrole) == str
        assert type(publication_id) == int
        assert type(topic) == str
        assert args is None or type(args) == list
        assert kwargs is None or type(kwargs) == dict

        obj = ZdbEvent(
            time_ns=time_ns,
            realm=realm,
            session_id=session_id,
            authid=authid,
            authrole=authrole,
            publication_id=publication_id,
            topic=topic,
            args=args,
            kwargs=kwargs)
        return obj
