#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


from http.server import HTTPServer, CGIHTTPRequestHandler
from copy import deepcopy
import pandas as pd

HOST = ''
PORT = 8000

# EXCH = [("UAH", "USD",	0.041), ("UAH",	"EUR", 0.037), ("GBP",	"EUR", 1.17)]
S = '<option value="{}"> {} </option>'


def get_data(filename="data/exchange.xlsx"):
    df = pd.read_excel(filename)
    return [tuple(list(df.iloc[i])[1:]) for i in range(df.shape[0])]

EXCH = get_data()

def prepare():
    s1 = ''
    s2 = ''
    set1 = set()
    set2 = set()
    with open('example.html', 'r') as f:
        cur = f.read()

    for pair in EXCH:
        c1, c2, _ = pair
        if c1 not in set1:
            t1 = deepcopy(S)
            s1 += t1.format(c1, c1) + '\n'
        set1.add(c1)

        if c2 not in set2:
            t2 = deepcopy(S)
            s2 += t2.format(c2, c2) + '\n'
        set2.add(c2)

    cur = cur.format(s1, s2, '{}')

    with open('page_exch.html', 'w') as f:
        f.write(cur)

prepare()
print('=== Local webserver ===')
print(f'http://localhost:{PORT}/page_exch.html')
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
