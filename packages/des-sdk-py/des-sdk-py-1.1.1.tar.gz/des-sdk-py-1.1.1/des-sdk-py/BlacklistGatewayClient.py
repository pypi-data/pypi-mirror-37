import Client
import requests
import time
import Common.util as util
import json
from eth_utils import encode_hex
import logging
log = logging.getLogger(__name__)


class BlacklistGatewayClient(Client.DESClient):
    """get question token
       @param requestId
       @param redirectUrl
       @param loanInfoList
       @returns {Promise<any>}
    """

    def getQuestionToken(self, requestId, redirectUrl, loanInfoList):
        getTokenParams = { "requestId": requestId,
                           "redirectUrl": redirectUrl,
                           "loadInfos": loanInfoList}
        response = requests.post(self.baseUrl + '/token', data=getTokenParams)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            log.error(response.status_code)


    """get question report
       @param token
       @returns {Promise<any>}
    """

    def getQuestionReport(self, token):
        getQuestionReportParmas = {'token': token,
                                   'timestamp': int(time.time()) + 60
                                   }
        tempSig = util.sign(bytes(str(getQuestionReportParmas), 'utf8'), self.privateKey)
        getQuestionReportParmas['signature'] = encode_hex(tempSig)[2:]
        print(getQuestionReportParmas)
        response = requests.post(self.baseUrl + '/question/report', data=json.dumps(getQuestionReportParmas), headers={'content-type': 'application/json'})
        print(response.content, response.text)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            log.error(response.status_code)


if __name__ == "__main__":
    client = BlacklistGatewayClient('5K8iH1jMJxn8TKXXgHJHjkf8zGXsbVPvrCLvU2GekDh2nk4ZPSF', '1.2.323', 'https://survey.gxb.io/blacklist')
    print(client.getQuestionReport("GXC4ywUcU8h6zPqESvAMkGREmmg9r54etHTpEtBHp8Rg2WYAcmFnD"))
    # print(client.getQuestionToken())
