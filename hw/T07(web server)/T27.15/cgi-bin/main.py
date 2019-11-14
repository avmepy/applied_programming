#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import cgi
import openpyxl



def get_page():
    with open('page_exch.html', 'r') as f:
        page = f.read()

    page = "Content-type: text/html; charset='utf-8'\n\n" + page
    return page



EXCH = [("UAH", "USD",	0.041), ("UAH",	"EUR", 0.037), ("GBP",	"EUR", 1.17)]


def calc(curr1, curr2, num, filename="exchange.xlsx"):
    res = 0
    for pair in EXCH:
        if pair[0] == curr1 and pair[1] == curr2:
            res = num * float(pair[2])
            break

    return res


data = cgi.FieldStorage()

res = 0



if "currency1" in data and "currency2" in data and "val" in data:
    res = calc(str(data["currency1"].value), str(data["currency2"].value), float(data["val"].value))

HTML_PAGE = get_page()

print(HTML_PAGE.format(str(res)))

