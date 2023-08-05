# Install
pip install des-sdk-py
# Usage
## Merchant client
    //initializing
    client = MerchantClient('5K8iH1jMJxn8TKXXgHJHjkf8zGXsbVPvrCLvU2GekDh2nk4XXXX', accountID, url)
    //creat data exchange and return request id
    result = client.createDataExchangeRequest(9, {
        "bankCardNo": "bankID"
    })
    //get result thourgh reuqest id
    response = client.getResult(result)
    if response.get("datasources") is not None:
        for data in response.get("datasources"):
            print(data.get("data"))
    else:
        print("response is None, please try more")
## Datasource client
    //initializing
    client = BlacklistGatewayClient('5KFachrDu7yHqhDeqdshedh6cWasLDv8d8Rko2JuvKM12XXXXXX', account)
    print(client.getQuestionReport("GXC4ywUcU8h6zPqESvAMkGREmmg9r54etHTpEtBHp8Rg2WYXXXXXX"))

# Dev Documents
https://doc.gxb.io/des/
