#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ''
PORT = 8000


print('=== Local webserver ===')
print(f'http://localhost:{PORT}/page.html')
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
