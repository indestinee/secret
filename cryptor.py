from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
import pickle
from utils import *

def padding(text, block_size):
    text = text + b'\0' * ((block_size - len(text)) % block_size)
    return text

class Cryptor(Cache):
    def __init__(self, path, key, mode=AES.MODE_CBC,\
            *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self.key, self.mode = key, mode
        if '__key__' in self.items():
            try:
                key = self.load('__key__')
            except:
                key = ''
            assert key == self.key, '[ERR] key error'
        else:
            self.dump(key, '__key__')

    def encrypt(self, data):
        iv = Random.new().read(AES.block_size)
        text = padding(pickle.dumps(data), AES.block_size)
        cryptor = AES.new(self.key, self.mode, iv) 
        text = cryptor.encrypt(text)
        return iv+text

    def decrypt(self, data):
        iv = data[0:AES.block_size]
        code = data[AES.block_size:]
        cryptor = AES.new(self.key, self.mode, iv) 
        data = cryptor.decrypt(code)
        return pickle.loads(data)

    def dump(self, data, *args, **kwargs):
        data = self.encrypt(data)
        super().dump(data, *args, **kwargs)

    def load(self, name, *args, **kwargs):
        data = super().load(name, *args, **kwargs)
        return self.decrypt(data)


