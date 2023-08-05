#!/usr/bin/env python3
# coding=utf-8

import Client
import json
import Common.validator as validator
import time
import Common.constants as constants
import random
import Common.util as util
from eth_utils import encode_hex
import Common.memo as AES
from Common import exceptions as exceptions
import requests
import logging
log = logging.getLogger(__name__)


import urllib
import urllib.parse
import urllib.request
import ast

class MerchantClient(Client.DESClient):
    """ fetch product info by product id
        :param productId
        :return response data which format is json
    """
    def getProduct(self, productId):
        log.debug("search product info: %s", productId)
        response = requests.get(self.baseUrl + "/api/product/%s" % productId)

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            log.error(response.status_code)

    """ create data exchange request
        :param productId
        :param params
        :returns requested data transaction id
    """
    def createDataExchangeRequest(self, productId, params):
        # research products information
        productResult = self.getProduct(productId)
        # print(productResult) #TODO for test
        result = productResult
        if not result.get("onlineDatasources"):
            raise exceptions.InvalidOnlineDatasourcesException("there is no dataSource")
        # validate whether the format of params is suitable for product params
        if not validator.validate(result.get('product').get('input'), params):
            raise exceptions.InvalidTxParamsException("input params is invalid")
        param = {"params": params,
                 "timestamp": int(time.time())
                 }
        param = str(param)
        expiration = int(time.time()) + constants.DEFAULT_TIMEOUT
        dataExchangeReqList = []

        log.debug("start to clear up the request params")
        for dataSourceAccount in result.get("onlineDatasources"):
            if self.accountId == dataSourceAccount.get("account_id"):
                continue

            #TODO format parms, maybe need to class.
            amount = {
                "amount": result.get("product").get("price").get("amount"),
                "assetId": result.get("product").get("price").get("assetId")
            }
            requestParams = {
                             "from": self.accountId,
                             "to": dataSourceAccount.get("accountId"),
                             "proxyAccount": result.get("des").get("accountId"),
                             "percent": result.get("des").get("percent"),
                             "memo": util.md5Encode(bytes(param, "utf8")),  #temporary method for the situation that param is dict.
                             "expiration": expiration,
                             "amount": amount,
                             }
            requestParams["signatures"] = [self.signature(util.serialization(requestParams), self.privateKey)]
            req = {"requestParams": requestParams,
                   "nonce": random.getrandbits(63),
                   }
            req["params"] = self.encrypt(self.privateKey,
                                         dataSourceAccount.get("publicKey"),
                                         req.get("nonce"),
                                         param)
            dataExchangeReqList.append(req)

        if not len(dataExchangeReqList):
            raise exceptions.InvalidTxParamsException("dataExchange request is empty")
        # send request of creating data exchange
        log.info("create request of data exchange.")

        # data = json.dumps(dataExchangeReqList).encode('utf-8')
        # headers = {'content-type': 'application/json'}
        # print(self.baseUrl + "/api/request/create/%s" % productId)
        # req = urllib.request.Request(self.baseUrl + "/api/request/create/%s" % productId, data=data, headers=headers)
        # res = urllib.request.urlopen(req)
        # result = res.read().decode("utf-8")
        # print("data:", result, type(result))
        # print(ast.literal_eval(result))
        # return ast.literal_eval(result).get("request_id")

        response = requests.post(self.baseUrl + "/api/request/create/%s" % productId, data=json.dumps(dataExchangeReqList), headers={'content-type': 'application/json'})
        # print("\n=====request=====\nurl:\n", self.baseUrl + "/api/request/create/%s" % productId, "\ndata:\n", json.dumps(dataExchangeReqList), "\nheaders:\n", {'content-type': 'application/json'}) #TODO for test
        # print("\n=====response=====\n", response, response.text, response.content, response.status_code, "\n") # TODO for test
        result = {}
        if response.status_code == requests.codes.ok:
            result = response.json()
        else:
            log.error(response.status_code)
        log.info("complete request of data exchange: %s." % result.get('request_id'))
        return result.get("request_id")


    """ fetch result by request id
        :param requestId
        :param timeout
        :returns ExchangeData
    """
    def getResult(self, requestId, timeout=8):
        log.debug("search the result of transaction which Id is：%s", requestId)
        start = time.time()
        log.debug("start to poll for the result")
        while True:
            response = requests.get(self.baseUrl + "/api/request/%s" % requestId)
            dataExchange = {}
            if response.status_code == requests.codes.ok:
                dataExchange = response.json()
            else:
                log.error(response.status_code)
            if len(dataExchange) and dataExchange.get("status") != "IN_PROGRESS":
                if not dataExchange.get("datasources"):
                    return dataExchange
                for dataExchangeDetail in dataExchange.get("datasources"):
                    if dataExchangeDetail.get("status") != "SUCCESS":
                        continue
                    dataExchangeDetail["data"] = self.decryptResult(self.privateKey,
                                                                    dataExchangeDetail.get("datasourcePublicKey"),
                                                                    dataExchangeDetail.get("nonce"),
                                                                    dataExchangeDetail.get("data"))
                return dataExchange
            time.sleep(0.06)
            if int(time.time()) - start > timeout:
                break
        log.debug("end polling")
        return None

    """ decrypt result before it returned
        :param privateKey, publicKey, nonce, data
        :returns original data
    """
    def decryptResult(self, privateKey, publicKey, nonce, data):
        return AES.decode_memo(privateKey, publicKey, nonce, data)

    """ encrypt result before it returned
        :param privateKey, publicKey, nonce, data
        :returns enciphered data
    """
    def encrypt(self, privateKey, publicKey, nonce, data):
        return AES.encode_memo(privateKey, publicKey, nonce, data)

    """ signature requestParms before request
        :param requestParams, privateKey
        :returns signatured data(hex string)
    """
    def signature(self, requestParams, privateKey):
        log.debug(privateKey, " to sign.")
        sign = util.sign(requestParams, privateKey)# "bankCardNo": "6236681540015259109"
        log.debug("sign done")
        return encode_hex(sign)[2:]

if __name__ == "__main__":
    client = MerchantClient('5K8iH1jMJxn8TKXXgHJHjkf8zGXsbVPvrCLvU2GekDh2nk4ZPSF', '1.2.323', 'http://192.168.1.124:6388')
    result = client.createDataExchangeRequest(9, {
        "bankCardNo": "6236681540015259109",
        # "name": "黄志勇",
        # "idcard": "420702198702167354",
        # "phone": "18867105786",
    })
    # print("\nresultid: %s" % result, "\n") #TODO for test
    response = client.getResult(result)
    if response.get("datasources") is not None:
        # print(k, "/", i)
        # k += 1
        for data in response.get("datasources"):
            print(data.get("data"))
    else:
        print("response is None, please try more")
