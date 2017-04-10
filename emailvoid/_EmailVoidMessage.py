#

from __future__ import absolute_import

from warnings import warn


class EmailVoidMessage(object):
    def __init__(self, **kwargs):
        self._domain = kwargs.get('domain')
        self._local = kwargs.get('local')
        self._id = kwargs.get('id')
        self._msgid = kwargs.get('msgid')
        self._created_at = kwargs.get('created_at')

    @property
    def created_at(self):
        return self._created_at

    @property
    def msgid(self):
        return self._msgid

    def get_msgid(self):
        warn("deprecated", DeprecationWarning)
        return self._msgid

    def __repr__(self):
        return "<EmailVoidMessage msgid={msgid!r} created_at={created_at!r}>".format(msgid=self._msgid, created_at=self._created_at)
