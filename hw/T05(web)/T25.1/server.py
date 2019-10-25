#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import socket


def change_date(date):
    if '-' in date:
        date = '.'.join(date.split('-')[::-1])
    if '/' in date:
        date = date.split('/')
        date = '.'.join((date[2], date[0], date[1]))
    return date


HOST = ''
PORT = 20004

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = conn.recv(1024)
    if not data:
        break

    date = str(data, encoding='utf-8')
    res = bytes(change_date(date), encoding='utf-8')
    conn.sendall(res)
conn.close()
