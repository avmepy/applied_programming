#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import cgi



HTML_PAGE = """Content-type: text/html; charset='utf-8'\n\n
<html>
<title>factorial check</title>
<body>
<h3>check result:</h3>
<br>
{}
<br>
</body>
</html>
"""

def is_factorial(n :int) -> bool:
    cur = 1
    i = 1
    success = False
    while cur < n:
        cur *=  i
        i += 1
    if cur == n:
        success = True
    return success


data = cgi.FieldStorage()

res = ''

if 'val' in data:
    res = str(is_factorial(int(data['val'].value)))

print(HTML_PAGE.format(res))

