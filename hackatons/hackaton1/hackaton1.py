#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import re

TEMP = '_$#-+=@&'
WORDS = open('words.txt', 'r').read().replace('\n', ' ')
trash = list(map(lambda x: x.replace('\n', ''), open('trashed.txt', 'r').readlines()))
TRASHED = []

for line in trash:
    TRASHED += line.split()


def main():
    phrase = []
    for word in TRASHED:
        for i in TEMP:
            word = word.replace(i, '.')
        if not re.findall(word, WORDS):
            phrase.append(word)
    return phrase

if __name__ == '__main__':
    print(main())

