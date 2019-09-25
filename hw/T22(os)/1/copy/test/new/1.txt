#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov



import re

def main(filename):
    patt = re.compile(r'(?P<real>\d+\.?\d*?)\s?\+\s?i(?P<imag>\d*\.?\d*)')
    a = patt.finditer(open(filename, 'r').read())
    s = complex(0, 0)
    for i in a:
        s += complex(float(i['real']), float(i['imag']))
    return s





if __name__ == '__main__':
    print(main('input.txt'))