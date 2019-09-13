#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import re


WORDS = ['error', 'warning', 'critical']


def main(filename_input, filename_output, words, register=True, whole=True):

    with open(filename_input, 'r') as fin:
        st = fin.read()

    for word in words:

        if register and whole:
            patt = re.compile(word)
        elif not register and whole:
            patt = re.compile(word, re.IGNORECASE)
        elif register and not whole:
            patt = re.compile(f'\\b\\w*{word}\\w*\\b')
        else:
            patt = re.compile(f'\\b\\w*{word}\\w*\\b', re.IGNORECASE)


        st = patt.sub('', st)

    with open(filename_output, 'w') as fout:
        fout.write(st)




if __name__ == '__main__':
    main('input.txt', 'output.txt', words=WORDS, register=False, whole=False)

