#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import re


def separate(filename_input: str, filename_output: str):
    """

    splits the contents of file input into a sentence and writes to file output

    :param filename_input: input filename
    :param filename_output: output filename
    :return: None
    """

    with open('input.txt', 'r') as fin:
        st = fin.read()

    patt = re.compile(r'[A-Z].*?[\.\?!]{1,4}', re.DOTALL)

    sentences = patt.finditer(st)


    res = ''

    row = 1  # number of row

    ind = 0  # position in row

    for s in sentences:

        tmp = len(re.findall(r'\n', s.group()))

        res += str(row) + ' ' + str(ind) + ' '+ s.group().replace('\n', ' ').strip() + '\n'

        row += tmp

        ind = len(s.group()[s.group().rfind('\n') + 1:])

    with open(filename_output, 'w') as fout:
        fout.write(res)





if __name__ == '__main__':
    separate('input.txt', 'output.txt')


