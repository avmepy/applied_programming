#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import re
import random


changes = {"в": "фф", "а": "о", "о": "а", "и": "ы", "я": "йа", "е": "и", "к": "г", "п": "б", "х": "г", "ш": "ж", "ж": "ш", "з": "с", "ь": ""}

up = {}

for key, value in changes.items():
    up.update({key.upper(): value.upper()})

changes.update(up)


def main(filename_input, filename_output, freq=0.8):

    def change(word: re.match) -> str:

        w = word.group()

        if random.random() < freq:

            chang_num = random.randint(0, 1) + 1

            cur = 0

            while chang_num and cur < len(w) - 1:
                if w[cur] in changes.keys():
                    w = w[:cur] + changes[w[cur]] + w[cur+1:]
                    chang_num -= 1
                cur += 1

        return w


    patt = re.compile(r'\b[a-zа-я]+\b', re.IGNORECASE)

    with open(filename_input, 'r') as fin:
        st = fin.read()
    res = patt.sub(change, st)

    with open(filename_output, 'w') as fout:
        fout.write(res)




if __name__ == '__main__':
    main('input.txt', 'output.txt')

