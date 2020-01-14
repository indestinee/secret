import argparse
from config import cfg
from cryptor import Cryptor
import numpy as np
from IPython import embed
from utils import *

def get_args():
    parser = argparse.ArgumentParser(description='Secret Manager')
    return parser.parse_args()


tables = [{
    'name': 'information',
    'attr': [{
            'key': 'id',
            'type': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        }, {
            'key': 'name',
            'type': 'text NOT NULL',
        }, {
            'key': 'data',
            'type': 'text',
        }],
    }
]

def init(cryptor):
    cryptor._db.add_tables(tables)

def transfer(cryptor):
    cryptor._db.__destroy__()
    init(cryptor)
    for each in cryptor.cache.items():
        if each[:-3] == '.db' or each == '__key__':
            continue
        cp.log(each)
        data = cryptor.decrypt(cryptor.cache.load(each, 'bin'))
        print(data, each)
        cryptor.dump(data, each)

if __name__ == '__main__':
    args = get_args()
    cryptor = Cryptor(cfg.cache, name=cfg.database_name, default='bin')

    embed()
    exit(0)
