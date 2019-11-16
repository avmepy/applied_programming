#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


from http.server import HTTPServer, CGIHTTPRequestHandler
import os
from urllib.request import urlretrieve, urlopen
from urllib.parse import urlencode, quote
from re import compile
from html.parser import HTMLParser
import pandas as pd

import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


HOST = ''
PORT = 8000



k = 0
in_table = False
rez = []


k = 0
k2 = 0
in_table = False
in_row = False
col2 = False
rez = []


class MyParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global k, k2, in_table, rez, col2

        if tag == "kr":
            in_row = True
        if tag == "td":
            k2 += 1
            if k2 == 1:
                col2 = True
            else:
                col2 = False

        if tag == "table":
            k += 1
            if k == 2:
                in_table = True

        elif tag == "a" and in_table and col2:
            t = list(filter(lambda x: x[0]=="title", attrs))
            if t:
                rez.append(t[0][1])



    def handle_endtag(self, tag):
        global in_table, k2, in_row
        if tag == "table":
            in_table = False
        if tag == "tr":
            k2 = 0
            in_row = False


def main():
    parser = MyParser()
    res = urlopen("https://uk.wikipedia.org/wiki/" + quote("Міста-мільйонники_світу"), context=ctx)
    content = res.read().decode(res.headers.get_content_charset())
    parser.feed(content)
    return rez


def main2(URL="https://uk.wikipedia.org/wiki/" + quote("Міста-мільйонники_світу")):
    df = pd.read_html(URL)[1]
    df.to_csv('beautifulsoup_pandas.csv', header=0, index=False)
    cities = list(df.ix[:, 0])
    return cities


city_list = main()
with open("city_list.txt", 'w') as f:
    f.write(' '.join(city_list))


f = open("cities.txt", 'w')
f.close()
f = open("time.txt", 'w')
f.close()
print('=== Local webserver ===')
print(f'http://localhost:{PORT}/start_page.html')
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
