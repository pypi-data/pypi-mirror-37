from jsonrpcclient.clients.http_client import HTTPClient


class DESClient(object):

    def __init__(self, privateKey, accountId, baseUrl='https://des.gxchain.cn'):
        self._privateKey = privateKey
        self._accountId = accountId
        self._baseUrl = baseUrl

    @property
    def privateKey(self):
        return self._privateKey

    @privateKey.setter
    def privateKey(self, privateKey):
        self._privateKey = privateKey

    @property
    def accountId(self):
        return self._accountId

    @accountId.setter
    def accountId(self, accountId):
        self._accountId = accountId

    @property
    def baseUrl(self):
        return self._baseUrl

    @baseUrl.setter
    def baseUrl(self, baseUrl):
        self._baseUrl = baseUrl
