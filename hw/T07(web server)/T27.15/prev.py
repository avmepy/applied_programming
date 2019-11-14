#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

from copy import deepcopy

EXCH = [("UAH", "USD",	0.041), ("UAH",	"EUR", 0.037), ("GBP",	"EUR", 1.17)]
S = '<option value="{}"> {} </option>'

def prepare():
    s1 = ''
    s2 = ''
    with open('page_exch.html', 'r') as f:
        cur = f.read()
    print(cur)

    for pair in EXCH:
        c1, c2, _ = pair
        t1 = deepcopy(S)
        t2 = deepcopy(S)
        s1 += t1.format(c1, c1) + '\n'
        s2 += t2.format(c2, c2) + '\n'

    cur = cur.format(s1, s2, '{}')

    with open('page_exch.html', 'w') as f:
        f.write(cur)

if __name__ == '__main__':
    prepare()