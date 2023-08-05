import Client
import time
from Common import util as util
import json
import requests
import logging
log = logging.getLogger(__name__)

class DatasourceClient(Client.DESClient):

    def __init__(self, privateKey, accountId, queryUrl):
        super(DatasourceClient, self).__init__(privateKey, accountId)
        self.queryUrl = queryUrl

    """heart beat to des server
       @param products
       @returns {Promise<any>}
    """
    def heartbeat(self, products):
        heartbeat = {
            "account": self.accountId,
            "products": products,
            "queryUrl": self.queryUrl,
            "timestamp": int(time.time()) + 3,
        }
        heartbeat['signature'] = util.sign(bytes(str(heartbeat), "utf8"), self.privateKey)
        response = requests.post(self.baseUrl+'/api/datasource/heartbeat', data=heartbeat)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            log.error(response.status_code)


    """encrypt data with shared secret
       @param params
       @param publicKey
       @returns {{data: string, nonce: *}}
    """
    def encrypt(self, params, publicKey):
        pass

    """decrypt message with shared secret
       :param message
       :param nonce
       :param publicKey
       :returns      
    """
    def decrypt(self, nonce, publicKey):
        pass
