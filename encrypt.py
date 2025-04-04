from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import urllib.parse
import json


def load_rsa_public_key(pem_key: str) -> RSA.RsaKey:
    pem_key = pem_key.strip()
    return RSA.import_key(pem_key)


def rsa_encrypt(public_key: RSA.RsaKey, data: str) -> str:
    cipher = PKCS1_v1_5.new(public_key)
    encrypted_data = cipher.encrypt(data.encode("utf-8"))
    return base64.b64encode(encrypted_data).decode("utf-8")


def get_secret_param(p: str, public_key_pem: str) -> str:
    public_key = load_rsa_public_key(public_key_pem)
    arr = []
    max_index = 0

    for i in range(len(p) + 1):
        if (i + 1) % 30 == 0:
            encrypted_part = rsa_encrypt(public_key, p[max_index:i])
            arr.append(urllib.parse.quote(encrypted_part))
            max_index = i

    if max_index != len(p):
        encrypted_part = rsa_encrypt(public_key, p[max_index:])
        arr.append(urllib.parse.quote(encrypted_part))

    return json.dumps(arr)

