#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import socket

HOST = 'localhost'
PORT = 20006


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
with open('input.txt', 'r') as f:
    st = f.readlines()

i = 0
while True:
    to_send = st[i]
    i += 1
    if i == len(st):
        data = s.recv(1024)
        print(data.decode('utf-8'))
        break
    s.sendall(bytes(to_send, encoding='utf-8'))
    # data = s.recv(1024)
    # print(data.decode('utf-8'))
s.close()

