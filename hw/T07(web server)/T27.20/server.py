#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import cgi
from datetime import datetime

PORT = 8000


class Person:

    def __init__(self, name=None, byear=None):
        self.name = name
        self.byear = byear

    def input(self):
        self.name = input("enter name: ")
        self.byear = input("enter byear: ")

    def print(self):
        print(self.name, self.byear, end=" ")


class Driver(Person):

    def __init__(self, name=None, byear=None, cost=None, capacity=None):
        Person.__init__(self, name=name, byear=byear)
        self.cost = cost
        self.capacity = capacity

    def input(self):
        Person.input(self)
        self.cost = input("enter cost: ")
        self.capacity = input("enter capacity: ")

    def print(self):
        Person.print(self)
        print(self.cost, self.capacity, end=" ")

    def get_pay(self, km):
        return self.capacity * km * self.cost


def prepare(filename="driver_list.txt"):
    PAT = '<option value="{}"> {} </option>'
    names = []
    with open(filename, 'r') as fin:
        for line in fin:
            names.append(PAT.format(line.split()[0], line.split()[0]))

    with open("main.html", 'r') as page:
        page = page.read().format('\n'.join(names), '{answer}')
    return page


def get_add_page():
    with open("add_page.html") as fin:
        page = fin.read()
    return page


def application(environ, start_response, filename="driver_list.txt"):
    if environ.get('PATH_INFO', '').lstrip('/') == '':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        result = ''
        HTML_PAGE = prepare()
        if "drivers" in form and "date_from" in form and "date_to" in form:
            name = str(form['drivers'].value)
            date_from = datetime.strptime(str(form['date_from'].value), "%Y-%M-%d")
            date_to = datetime.strptime(str(form['date_to'].value), "%Y-%M-%d")
            res = [name, 0]
            with open(filename, 'r') as fin:
                for line in fin:
                    cur_name, _, cur_km = line.split()
                    cur_date = datetime.strptime(_, "%Y-%M-%d")
                    if cur_name == res[0] and date_from <= cur_date <= date_to:
                        res[1] += int(cur_km) * 3.5
            result = res[0] + " " + str(res[1])

        if 'add' in form:
            HTML_PAGE = get_add_page()

        if 'back' in form:
            HTML_PAGE = prepare()

        if 'driver_name' in form and 'driver_date' in form and 'driver_km' in form and 'driver_cost' in form:
            with open(filename, 'a') as fap:
                fap.write(str(form['driver_name'].value) + " " +
                          str(form['driver_date'].value) + " " +
                          str(form['driver_km'].value) + "\n")



        body = HTML_PAGE.format(answer=result)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])


    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        body = 'Сторінку не знайдено'
    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    print(f'http://localhost:{PORT}')
    httpd = make_server('localhost', PORT, application)
    httpd.serve_forever()


