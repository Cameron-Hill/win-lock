import random
import string
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptManager(object):

    def __init__(self, config, salt = b'Default Salt'):
        self.salt = salt
        self.kdf = self._get_kdf(self.salt)
        self.key = self._get_key(config.pop('password'))

    def encrypt_and_delete_file(self, file_path, passes=3):
        out_file = self.encrypt_file(file_path)
        self.secure_delete(file_path, passes)
        return out_file

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        encrypted_bytes = self.encrypt_bytes(file_bytes)
        out_file = file_path+'.wl'
        with open(out_file, 'wb') as f:
            f.write(encrypted_bytes)
        return out_file

    def encrypt_bytes(self, data):
        return Fernet(self.key).encrypt(data)

    def decrypt_bytes(self, data):
        return Fernet(self.key).decrypt(data)

    def _get_kdf(self, salt):
        return PBKDF2HMAC(
            algorithm=hashes.SHA3_256(),
            length=32,
            salt=salt,
            iterations=1000,
            backend = default_backend()
        )

    def _get_key(self, password):
        password = password.encode() if not isinstance(password, bytes) else password
        return base64.urlsafe_b64encode(self.kdf.derive(password))

    @staticmethod
    def secure_delete(path, passes=1):
        for i in range(passes):
            with open(path, "r+b") as f:
                f.read()
                length = f.tell()
                f.seek(0)
                f.write(os.urandom(length))
        new_path = os.path.join(os.path.dirname(path),''.join(random.choices(string.ascii_letters + string.digits+'_-', k=15)))
        os.rename(path, new_path)
        os.remove(new_path)