#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import os
import _io
from datetime import datetime
import time

CHUNK = 500 * 1024   # 500 KB

def main(name: str, fin:_io.TextIOWrapper) -> tuple:
    if len(fin.read(CHUNK)) == CHUNK:
        fin.close()
        name = f'{name}{datetime.now()}'
        fin = open(name, 'w')
    return  name, fin


def func(filename: str, name :str="test") -> tuple:
    tmp = f'{name}{datetime.now()}'

    with open(filename, 'r') as fin:
        with open(tmp, 'a') as fout:

            for line in fin:
                fout.write(f'{line}\n')

    fout = open(tmp, 'r')

    return name, fout

if __name__ == '__main__':
    print('start test_func.....')
    # file = 'Vojna i mir. Tom 1.txt'
    file = 'input.txt'
    name, fout = func(file)
    time.sleep(2)
    print('start main func......')
    name, f = main(name, fout)
    print(name)
    print(f)

