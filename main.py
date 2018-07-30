import argparse
from config import cfg
from cryptor import Cryptor
import numpy as np
from IPython import embed
import getpass

def get_args():
    parser = argparse.ArgumentParser(description='Secret Manager')
    parser.add_argument('-p', '--path', type=str, default=cfg.cache,\
            help='Storage path')
    return parser.parse_args()

def get_key():
    while True:
        print('[WRN] you must remember the key, otherwise lose all data')
        key = getpass.getpass('[I N] key: ')
        if len(key) == 0:
            continue
        return (key * (32 // len(key) + 1))[:32]
    return None

if __name__ == '__main__':
    args = get_args()
    key = get_key()
    cryptor = Cryptor(cfg.cache, key=key, default='bin')
    embed()
    exit(0)
