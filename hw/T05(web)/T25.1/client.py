#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import socket

HOST = 'localhost'
PORT = 20004


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    to_send = input('enter date: ')
    if not to_send:
        break
    s.sendall(bytes(to_send, encoding='utf-8'))
    data = s.recv(1024)
    print(data.decode('utf-8'))
s.close()

