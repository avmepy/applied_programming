#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import re


def main(filename):

    res = []
    patt = re.compile(r'[\w\.]+@([\w-]+\.)+[\w-]{2,4}')
    with open(filename, 'r') as fin:
        for lines in fin:
            res += list(map(lambda x: x.group(), patt.finditer(lines)))


    return res

if __name__ == '__main__':
    for mail in main('input.txt'):
        print(mail)