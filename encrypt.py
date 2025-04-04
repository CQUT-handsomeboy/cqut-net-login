import base64
import rsa

from urllib.parse import quote


"""
以下是由k君提供的加密算法
"""


class rsaEncrypy:
    def __init__(self):
        pubkey = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDACwPDxYycdCiNeblZa9LjvDzbiZU1vc9gKRcG/pGjZ/DJkI4HmoUE2r/o6SfB5az3s+H5JDzmOMVQ63hD7LZQGR4k3iYWnCg3UpQZkZEtFtXBXsQHjKVJqCiEtK+gtxz4WnriDjf+e/CxJ7OD03e7sy5NY/akVmYNtghKZzz6jwIDAQAB\n-----END PUBLIC KEY-----"
        self.key = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode())

    def run(self, e) -> str:
        parms = []
        for i in range(0, len(e), 60):
            result = e[i : i + 60]
            e_byte = result.encode("utf-8")
            s = rsa.encrypt(e_byte, self.key)
            t = base64.b64encode(s).decode().replace("=", "")
            parms.append(t)
        r = str(parms)
        r = r.replace(" ", "").replace("'", '"')
        encoded_str = quote(r.encode("utf-8"), safe="")
        encoded_str = encoded_str.replace("%7C", "%5Cu003d%5Cn")
        print(encoded_str)
        return encoded_str
