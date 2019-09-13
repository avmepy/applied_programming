#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import re


def roman_to_int(num):
    roman= {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    result = 0
    for i, c in enumerate(num):
        if (i+1) == len(num) or roman[c] >= roman[num[i+1]]:
            result += roman[c]
        else:
            result -= roman[c]
    return result

def main(filename_input, filename_output):

    patt = re.compile(r'[IVXLCDM]+')

    with open(filename_input, 'r') as fin:
        st = fin.read()

    res = patt.findall(st)

    res.sort(key=lambda x: roman_to_int(x))

    with open(filename_output ,'w') as fout:
        fout.write('\n'.join(res))


if __name__ == '__main__':
    main('input.txt', 'output.txt')