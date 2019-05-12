import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_key(password, salt):
    if not isinstance(password,bytes) or not isinstance(salt,bytes):
        #todo make custom exceptin
        raise Exception('Password and salt must be of type bytes')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_256(),
        length=32,
        salt=salt,
        iterations=1000,
        backend = default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

