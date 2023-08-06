from tinydb.storages import Storage
from security import DefaultCryptography, StorageFormat
import os
import json
import bson

# File header
# header_length (4 bytes) | crypt_dependencies (header_length bytes)

class SecureStorage(Storage):

    def __init__(self, filename, password):
        if (os.path.isfile(filename)):
            self.file = open(filename, "rb+")


            self.header_length = int.from_bytes(self.file.read(4), byteorder='big')
            crypt_dependencies = self.file.read(self.header_length)


            self.cript = DefaultCryptography(password, crypt_dependencies)

            #Try to decrypt
            self.file.seek(4+self.header_length)

            if (self.cript.storage_format == StorageFormat.JSON):
                a = self.file.read()
                self.cript.decrypt(a).decode("utf-8")
            else:
                self.cript.decrypt(self.file.read())

        else:
            raise FileNotFoundError("Database file not found")

    @staticmethod
    def create(filename, password, storage_format=StorageFormat.JSON):
        if (os.path.isfile(filename)):
            raise Exception("Database file already exists")
        else:
            with open(filename, 'wb+') as file:
                crypt_dependencies = DefaultCryptography.generateCryptographyDependencies(storage_format=storage_format)
                cript = DefaultCryptography(password, crypt_dependencies)

                length_bytes = len(crypt_dependencies).to_bytes(4, byteorder='big') #4 bytes
                file.write(length_bytes)
                file.write(crypt_dependencies)
                
                if (storage_format == StorageFormat.BSON):   
                    data = cript.encrypt(bson.dumps({}))
                else:
                    data = cript.encrypt('{}')
                file.write(data)

    
    def read(self):
        self.file.seek(4+self.header_length)
        
        if (self.cript.storage_format == StorageFormat.BSON): 
            data = self.cript.decrypt(self.file.read())
            return bson.loads(data)
        else:
            data = self.cript.decrypt(self.file.read()).decode("utf-8")
            return json.loads(data)

    def write(self, data):
        self.file.seek(4+self.header_length)
        if (self.cript.storage_format == StorageFormat.BSON):      
            crypted = self.cript.encrypt(bson.dumps(data))
        else:
            crypted = self.cript.encrypt(json.dumps(data).encode("utf-8"))
        self.file.write(crypted)
        self.file.flush()
        os.fsync(self.file.fileno())
        self.file.truncate()

    def close(self):
        self.file.close()
        