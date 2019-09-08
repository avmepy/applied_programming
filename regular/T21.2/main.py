#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import re

def main(filename):

    with open(filename, 'r') as f:
        st = f.read()

    return re.split(r'[ \n]', st)


if __name__ == '__main__':
    print(main('test.txt'))

