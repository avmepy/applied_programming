#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import socket
import re


mails = []


def mail(string):
    global mails

    patt = re.compile(r'[\w\.]+@([\w-]+\.)+[\w-]{2,4}')
    mails += list(map(lambda x: x.group(), patt.finditer(string)))


HOST = ''
PORT = 20006

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = conn.recv(1024)
    if not data:
        break

    pal = str(data, encoding='utf-8')
    mail(pal)
    res = bytes('\n'.join(mails), encoding='utf-8')
    conn.sendall(res)
conn.close()
