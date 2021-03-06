file_ = '$DATA_FILE'
log_file = '$LOG_FILE'
import sys
import os
from PyQt5.QtWidgets import (QLineEdit, QApplication, QInputDialog, QMessageBox)
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging
logger = logging.getLogger()
pwd_attempts = 0

def configure_logger():
    os.mkdir(os.path.dirname(log_file)) if not os.path.exists(os.path.dirname(log_file)) else None
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("SESSION INITIALISED FOR: {}".format(file_))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def getPassword():
    pwd, ok = QInputDialog.getText(None, "Win-Lock", "Enter your win-lock password",
                                   QLineEdit.Password)
    if not ok:
        logger.info("User Canceled password input")
        sys.exit(1)
    return pwd

def init():
    app = QApplication(sys.argv)
    config = {
        'user': 'test_user',
        'password': None,
        'log_level': 'debug',
        #'database': r'D:\cambo\Docs\Projects\win-lock\prototype\tests\test_data\test_database.db'
    }
    configure_logger()
    main(app, config)

def main(app, config):
    config['password'] = getPassword()
    try:
        manager = CryptManager(config, b'salty_boy')
        with open(resource_path(file_), 'rb') as f:
            encrypted_bytes = f.read()
        logging.info("Manager initialised")
        try:
            decrypted_data = manager.decrypt_bytes(encrypted_bytes)
        except InvalidToken as e:
            global pwd_attempts
            pwd_attempts += 1
            logger.info("User entered Incorrect Password... {} Attempts".format(pwd_attempts))
            QMessageBox.question(None,'Win-Lock',"Incorrect Password",QMessageBox.Ok)
            return main(app, config)

        logger.info("Decrypted {}".format(file_))
        out_file = file_.replace('.wl','')
        with open(os.path.join(os.getcwd(),out_file), 'wb') as f:
            f.write(decrypted_data)
        logger.info("Wrote {}".format(os.path.abspath(out_file)))
        logger.info("Done")
    except Exception as e:
        logger.exception("FAILED -- {}".format(e))


class CryptManager(object):
    def __init__(self, config, salt=b'Default Salt'):
        self.salt = salt
        self.kdf = self._get_kdf(self.salt)
        self.key = self._get_key(config.pop('password'))

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        encrypted_bytes = self.encrypt_bytes(file_bytes)
        with open(file_path + '.wl', 'wb') as f:
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
            backend=default_backend()
        )

    def _get_key(self, password):
        password = password.encode() if not isinstance(password, bytes) else password
        return base64.urlsafe_b64encode(self.kdf.derive(password))


if __name__ == '__main__':
    init()
