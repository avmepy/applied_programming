#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import cgi
import time



def get_page():
    with open('start_page.html', 'r') as f:
        page = f.read()

    page = "Content-type: text/html; charset='utf-8'\n\n" + page
    return page


def get_cities() -> set:
    with open("city_list.txt", 'r') as fin:
        return {i for i in fin.read().split()}


def get_used(filename="cities.txt"):
    with open(filename, 'r') as fin:
        s = [i for i in fin.read().split()]
    return s



HTML_PAGE = get_page()

data = cgi.FieldStorage()

res = ''
status = ''

used = get_used()
cities = get_cities()

if 'city' in data:



    word = str(data['city'].value)

    success = False


    if  len(used) == 0 or word[0].upper() == used[-1][-1].upper():

        if word in cities:
            if word not in used:
                status = 'accepted'
                used.append(word)
                with open("cities.txt", 'a') as f:
                    f.write(word + ' ')
                success = True
            else:
                status = 'words already used! Try again'
        else:
            status = 'this city doesn`t exist'
    else:
        status = 'letters don`t match'

    if success:
        for i in list(cities):
            if i not in used and i[0].upper() == word[-1].upper():
                res = i
                with open("cities.txt", 'a') as f:
                    f.write(i + ' ')
                break
            else:
                res = 'you win'
    else:
        res = '{}'


    f = open("time.txt", 'r')
    tim = f.read()
    if str(tim) == '':
        f.close()
        f = open("time.txt", 'w')
        f.write(str(time.time()))
        f.close()

    else:
        if abs(float(time.time()) - float(tim)) > 60:
            res = 'you lose'
print(HTML_PAGE.format(status, used, res))

