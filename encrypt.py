import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from urllib.parse import quote

import json
import base64

public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDACwPDxYycdCiNeblZa9LjvDzb
iZU1vc9gKRcG/pGjZ/DJkI4HmoUE2r/o6SfB5az3s+H5JDzmOMVQ63hD7LZQGR4k
3iYWnCg3UpQZkZEtFtXBXsQHjKVJqCiEtK+gtxz4WnriDjf+e/CxJ7OD03e7sy5N
Y/akVmYNtghKZzz6jwIDAQAB
-----END PUBLIC KEY-----"""


def encrypt(password):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()


def getSecretParam(p):
    if p is None or p.strip() == "":
        return ""

    arr = []
    maxIndex = 0

    for i in range(len(p) + 1):
        if (i + 1) % 30 == 0:
            arr.append(encrypt(p[maxIndex:i]))
            maxIndex = i

    if maxIndex != len(p):
        arr.append(encrypt(p[maxIndex : len(p)]))

    return quote(json.dumps(arr))
