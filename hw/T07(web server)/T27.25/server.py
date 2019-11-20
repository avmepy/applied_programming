#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import cgi
from copy import deepcopy

PORT = 8000

TRAVEL_PAGE = """<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	</head>

	<title>ticket price</title>
	<body>
		<h3>ticket price</h3>
		<form method=POST action="">
            <p>Enter name: </p>
                <input type=text name=name value="">
            <p>Enter byear: </p>
                <input type=text name=byear value="">
			<p>Enter departure: </p>
				<input type=text name=departure value="">
            <p>Enter destination: </p>
                <input type=text name=destination value="">
				<input type=submit value="get price">
		</form>
        <p>
            {}
        </p>
	</body>
</html>
"""

ADD_PAGE = ''

HTML_PAGE = deepcopy(TRAVEL_PAGE)


class Person:

    def __init__(self, name=None, byear=None):
        self.name = name
        self.byear = byear

    def input(self):
        self.name = input("enter name: ")
        self.byear = input("enter byear: ")

    def print(self):
        print(self.name, self.byear, end=" ")


class Passenger(Person):

    def __init__(self, name=None, byear=None, departure=None, destination=None):
        Person.__init__(self, name=name, byear=byear)
        self.departure = departure
        self.destination = destination

    def input(self):
        Person.input(self)
        self.departure = input("enter departure: ")
        self.destination = input("enter destination: ")

    def print(self):
        Person.print(self)
        print(self.departure, self.destination, end=" ")

    def get_price(self, filename="travel.txt"):
        with open(filename, 'r') as fin:
            travel_list = [i.split() for i in fin]
        price = -1
        for route in travel_list:
            if ((route[0] == self.departure and route[1] == self.destination) or
                (route[1] == self.departure and route[0] == self.destination)):
                price = 2.5 * float(route[2])
                break

        return price



def application(environ, start_response, filename="travel.txt"):
    """Викликається WSGI-сервером.

       Отримує оточення environ та функцію,
       яку треба викликати у відповідь: start_response.
       Повертає відповідь, яка передається клієнту.
    """
    if environ.get('PATH_INFO', '').lstrip('/') == '':
        # отримати словник параметрів, переданих з HTTP-запиту
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        result = ''
        HTML_PAGE = TRAVEL_PAGE
        if 'departure' in form and 'destination' in form and 'name' in form and 'byear' in form:
            name = str(form['name'].value)
            byear = str(form['byear'].value)
            departure = str(form['departure'].value)
            destination = str(form['destination'].value)

            p = Passenger(name=name, byear=byear, departure=departure, destination=destination)

            result = f'{name}{byear} , departure: {departure}, destination {destination}, ticket price = {p.get_price()}'

            HTML_PAGE = deepcopy(TRAVEL_PAGE)

        elif 'depar' in form and 'destin' in form and 'price' in form:
            depar = str(form['depar'].value)
            destin = str(form['destin'].value)
            price = str(form['price'].value)
            with open(filename, 'a') as f:
                f.write(f'{depar} {destin} {price}')

            HTML_PAGE = ADD_PAGE

        body = HTML_PAGE.format(result)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])


    else:
        # якщо команда невідома, то виникла помилка
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        body = 'Сторінку не знайдено'
    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    # створити та запуститити WSGI-сервер
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    print(f'http://localhost:{PORT}')
    httpd = make_server('localhost', PORT, application)
    httpd.serve_forever()



