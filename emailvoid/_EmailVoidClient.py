#

from __future__ import absolute_import, print_function

from logging import getLogger
from requests import Session

from ._EmailVoidMessage import EmailVoidMessage
from ._EmailVoidError import EmailVoidError


class EmailVoidClient(object):
    def __init__(self, apikey=None, host="www.emailvoid.com", port=80, timeout=10):
        self.__log = getLogger('emailvoid.client')
        #
        self._host = host
        self._port = port
        #
        self._apikey = apikey
        #
        self._timeout = timeout
        #
        self._sess = Session()

    def dispose(self):
        if self._sess:
            self._sess.close()
            self._sess = None

    def _make_address(self, endpoint, secure=False):
        result = "http://{host}:{port}{path}".format(host=self._host, port=self._port, path=endpoint)
        return result

    def _make_request(self, endpoint, params, raw=False):
        headers = {
            'X-Auth': self._apikey,
        }
        url = self._make_address(endpoint=endpoint)
        res = self._sess.post(url, json=params, headers=headers, verify=False, timeout=self._timeout)
        self.__log.debug("Server response: {content!r}".format(content=res.content))
        #
        if res.status_code == 403:
            raise EmailVoidError("Authorization error")
        #
        if res.status_code != 200:
            self.__log.error("Server response: {content!r}".format(content=res.content))
            raise EmailVoidError("Internal Server Error")
        #
        if raw:
            result = res.content
        else:
            values = res.json()
            if "error" in values:
                msg = values.get('error')
                raise EmailVoidError(msg)
            result = values # TODO - receive from `records` area
        return result

    def msg_count(self, mailbox=None):
        params = {
            'local': mailbox
        }
        res = self._make_request(endpoint="/api/2.0/msg/count", params=params)
        result = res.get('count')
        return result


    def msg_search(self, mailbox):
        params = {
            'local': mailbox,
        }
        res = self._make_request(endpoint="/api/2.0/msg/search", params=params)
        records = res.get('records')
        #
        result = []
        for record in records:
            m = EmailVoidMessage(**record)
            result.append(m)
        return result


    def msg_content(self, msgid):
        endpoint = "/api/2.0/msg/{msgid}/content".format(msgid=msgid)
        params = {}
        res = self._make_request(endpoint=endpoint, params=params, raw=True)
        return res
