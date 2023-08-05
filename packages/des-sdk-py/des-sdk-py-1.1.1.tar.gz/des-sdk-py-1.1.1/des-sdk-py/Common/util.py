import hashlib
from graphenebase import ecdsa

from bitsharesbase import (
    operations
)

""" digest param before request
    :param param
    :returns MD5
"""
def md5Encode(byte):
    if type(byte) is not bytes:
        raise Exception
    m = hashlib.md5()
    m.update(byte)
    return m.hexdigest()


""" signature requestParams before request
    :param message, wifKeys
    :returns signatured data(hex string)
"""
def sign(message, wifKeys):
    signature = ecdsa.sign_message(message, wifKeys)
    return signature


""" serialize requestParms before request
    :param requestParams
    :returns serialization data(using method from BTS)
"""
def serialization(data):
    op = operations.SerialForSignature(**data)
    return op.__bytes__()

if __name__ == "__main__":
    pass