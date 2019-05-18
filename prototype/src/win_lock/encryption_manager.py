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

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        encrypted_bytes = self.encrypt_bytes(file_bytes)
        with open(file_path+'.wl', 'wb') as f:
            f.write(encrypted_bytes)

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