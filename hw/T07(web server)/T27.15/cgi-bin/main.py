#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import cgi
import pandas as pd



def get_page():
    with open('page_exch.html', 'r') as f:
        page = f.read()

    page = "Content-type: text/html; charset='utf-8'\n\n" + page
    return page



# EXCH = [("UAH", "USD",	0.041), ("UAH",	"EUR", 0.037), ("GBP",	"EUR", 1.17)]

def get_data(filename="data/exchange.xlsx"):
    df = pd.read_excel(filename)
    return [tuple(list(df.iloc[i])[1:]) for i in range(df.shape[0])]

EXCH = get_data()


def calc(curr1, curr2, num, filename="exchange.xlsx"):
    success = False
    res = 0
    for pair in EXCH:
        if pair[0] == curr1 and pair[1] == curr2:
            res = num * float(pair[2])
            success = True
            break

    return res, success


data = cgi.FieldStorage()

res = ''



if "currency1" in data and "currency2" in data and "val" in data:
    c1 = str(data["currency1"].value)
    c2 = str(data["currency2"].value)
    v = str(data["val"].value)
    ans, b = calc(c1, c2, float(v))
    if b:
        res = f'{v} {c1} = {ans} {c2}'
    else:
        res = f'not found'


HTML_PAGE = get_page()

print(HTML_PAGE.format(str(res)))

