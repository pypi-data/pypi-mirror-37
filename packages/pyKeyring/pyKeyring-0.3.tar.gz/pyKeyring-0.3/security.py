from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
from enum import Enum

class StorageFormat(Enum):
    BSON = 2
    JSON = 1

# CryptographyDependencies format
# salt_size (4 bytes) | salt (salt_size bytes) | storage_format (4 byte) 
class DefaultCryptography:

    SALT_BYTES = 4
    STORAGE_BYTES = 4
    SALT_LENGTH = 64

    def __init__(self, password, dependencies):
        self.salt_length = int.from_bytes(dependencies[:self.SALT_BYTES], byteorder='big')
        self.salt = dependencies[self.SALT_BYTES:self.salt_length+self.SALT_BYTES]
        self.storage_format = StorageFormat(int.from_bytes(dependencies[self.salt_length+self.SALT_BYTES:self.salt_length+self.SALT_BYTES+self.STORAGE_BYTES], byteorder='big'))

        self.password = password
        if (type(self.password) == str):
            self.password = self.password.encode("utf-8")
        self.key = self.deriveKey()
        self.f = Fernet(self.key)


    @staticmethod
    def generateCryptographyDependencies(storage_format=StorageFormat.BSON):
        salt = os.urandom(DefaultCryptography.SALT_LENGTH)
        salt_length_bytes = DefaultCryptography.SALT_LENGTH.to_bytes(DefaultCryptography.SALT_BYTES, byteorder='big')
        return salt_length_bytes + salt + storage_format.value.to_bytes(DefaultCryptography.STORAGE_BYTES, byteorder='big')
    
    def deriveKey(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(self.password)
        return base64.urlsafe_b64encode(key)

    def encrypt(self, raw_data):
        if (type(raw_data) == str):
            raw_data = raw_data.encode("utf-8")
        return self.f.encrypt(raw_data)

    def decrypt(self, encrypted_data):
        return self.f.decrypt(encrypted_data)

    def hash(self, raw_data):
        return hashes.SHA256(raw_data)