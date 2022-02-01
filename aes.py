import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import sys
import os
import json

AC_DIR  = "accounts"
POSTFIX = "aes"

class crypto_handler():
    def __init__(self, password):
        self.__gen_key(password)

    def __gen_key(self, password):
        salt = f"salty{password[int(len(password)/2)]}saltier".encode()
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=hashlib.sha3_512(salt).hexdigest().encode(),
                iterations=100000
            )
            self.__key = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))
        except Exception as ex:
            print("Keygen Error", ex)
            sys.exit(-1)

    def encrypt(self, data):
        return self.__key.encrypt(data)

    def decrypt(self, data):
        try:
            return self.__key.decrypt(data)
        except Exception as ex:
            print(ex)
            sys.exit(-1)


class file_handler():
    def __init__(self, filename, password, new_account=False, data=None):
        self.__filename = filename
        self.__filepath = f"{AC_DIR}{os.sep}{filename}"
        self.__crypto_object = crypto_handler(password)

        if new_account:
            self.encrypt(data)
            return

        if not os.path.isfile(f"{self.__filepath}.{POSTFIX}"):
            print("Error: This account is not in the database")
            sys.exit(-1)

    def encrypt(self, data):
        try:
            with open(f"{self.__filepath}.{POSTFIX}", "wb") as write_object:
                write_object.write(self.__crypto_object.encrypt(json.dumps(data).encode()))
        except Exception as ex:
            print("Error: encryption went wrong", ex)
            sys.exit(-1)

    def decrypt(self):
        try:
            with open(f"{self.__filepath}.{POSTFIX}", "rb") as read_object:
                return json.loads(self.__crypto_object.decrypt(read_object.read()).decode())
        except Exception as ex:
            print("Error: Decryption went wrong", ex)
            sys.exit(-1)


if __name__=="__main__":
    pass
