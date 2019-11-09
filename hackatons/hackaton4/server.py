#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import socketserver
import socket
import hashlib

d_hash = {}

HOST = ''
PORT = 20004




def make_dict(filename):
    global d_hash

    with open(filename, 'r') as fin:
        for word in fin:
            checksum = hashlib.md5()
            word = word.strip('\n')
            checksum.update(word.encode())
            digest = checksum.hexdigest()
            d_hash[digest] = word





class Handler(socketserver.StreamRequestHandler):


    def handle(self):
        global d_hash
        print('connected from', self.client_address)
        while True:
            data = self.rfile.readline().strip()
            print(f'client: {data}')
            if not data:
                break
            hash = str(data, encoding='utf-8').strip('\n')
            # перевірити на паліндром та відправити відповідь

            res = ''

            if hash in d_hash.keys():

                res = f'{hash}, {d_hash[hash]}'

            else:

                res = f'{hash}, '

            res = bytes(res, encoding='utf-8') + b'\n'
            print(f'server: {res}')
            self.wfile.write(res)
        print('disconnected', self.client_address)



if __name__ == '__main__':
    make_dict('HT05/words_alpha.txt')
    # c = 0
    # with open('HT05/input.txt', 'r') as f:
    #     for h in f:
    #         if h.strip('\n') in d_hash.keys():
    #             c += 1
    # print(c)
    socketserver.TCPServer((HOST, PORT), Handler).serve_forever()
