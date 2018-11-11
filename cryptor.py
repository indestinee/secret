from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
import pickle
from utils import *
import time
import getpass

def padding(text, block_size):
    text = text + b'\0' * ((block_size - len(text)) % block_size)
    return text

class Cryptor(object):
    def __init__(self, path, name, mode=AES.MODE_CBC,\
            *args, **kwargs):
        self.exipire_time = 300
        self.start_time = time.time()
        self._db = DataBase(path, name)
        self.key, self.mode = self.get_key(), mode
        self.help()
        self.display_items()

    def get_key(self):
        while True:
            cp.wrn('you must remember the key, otherwise lose all data')
            key = getpass.getpass('[I N] key: ')
            if len(key) == 0:
                continue
            return (key * (32 // len(key) + 1))[:32]
        return None


    def help(self):
        cp(
            '(#b) -- order -------------------------------------------\n'
            '(#y)   1. cryptor.display_items()  (#b) display all items\n'
            '(#y)   2. cryptor.load(id=x)       (#b) load item (ID: x)\n'
            '(#y)   3. cryptor.dump(data, name) (#b) save data        \n'
            '(#y)   4. cryptor.help()           (#b) that\'s me (#g):)\n'
            '(#b) ----------------------------------------------------\n'
        )

    def items(self):
        raw_items = self._db.select('information', keys=['id', 'name'],\
                return_dict=True)
        for item in raw_items:
            item['name'] = self.decrypt(item['name'])

        return raw_items

    def display_items(self):
        items = self.items()
        cp('(#y)'+'-'*64)
        for item in items:
            id = item['id']
            name = item['name']
            cp(
                '  (#b)id(##): (#y){}(##)  (#b)name(##): (#y){}(##)'.format(id, name)
            )
        cp('(#y)'+'-'*64)

    def __iter__(self):
        for name in self.items():
            yield name, self[name]

    def __getitem__(self, name):
        if name in self.items():
            return self.load(name)
        return None

    def __setitem__(self, name, data):
        self.dump(name, data)

    def remove(self, name):
        super().remove(name)
    
    def expire(self):
        if time.time() - self.start_time > self.exipire_time:
            cp.wrn('key expired')
            self.key = self.get_key()
            self.start_time = time.time()
            return None


    def encrypt(self, data):
        self.expire()
        iv = Random.new().read(AES.block_size)
        text = padding(pickle.dumps(data), AES.block_size)
        cryptor = AES.new(self.key, self.mode, iv)
        text = cryptor.encrypt(text)
        return iv+text

    def decrypt(self, data):
        self.expire()
        iv = data[0:AES.block_size]
        code = data[AES.block_size:]
        cryptor = AES.new(self.key, self.mode, iv)
        data = cryptor.decrypt(code)
        return pickle.loads(data)

    def dump(self, data, name, *args, **kwargs):
        data = self.encrypt(data)
        name = self.encrypt(name)
        self._db.add_row('information', {'data': data, 'name': name})


    def load(self, id, *args, **kwargs):
        item, = self._db.select('information', keys=['name', 'data'],\
                limitation={'id': id})
        for key in item:
            item[key] = self.decrypt(item[key])
        return item
