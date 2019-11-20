#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

import sqlite3
from datetime import datetime




class BirthdayDB:

    YEAR = int(3.154e+7)
    WEEK = 604800

    def __init__(self, filename):
        self.filename = filename


    def create(self):

        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("CREATE TABLE friends_table (name TEXT, birthday TEXT)")

        conn.commit()
        conn.close()


    def append(self, name, birthday):
        birthday = int(datetime.strptime(birthday, '%Y-%m-%d').strftime('%s'))
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute("INSERT INTO friends_table VALUES (?, ?)", (name, birthday))

        conn.commit()
        conn.close()


    def find(self, name):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("SELECT birthday FROM friends_table WHERE name = ?", (name, ))
        res = curs.fetchone()

        if res:
            birthday = res[0]
        else:
            birthday = "not found"

        conn.commit()
        conn.close()
        return birthday

    def find_less_week(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("""SELECT name FROM  friends_table 
                    WHERE abs(strftime('%s','now') % ?  - birthday % ? ) < ? % ?""",
                     (BirthdayDB.YEAR, BirthdayDB.YEAR, BirthdayDB.WEEK, BirthdayDB.YEAR))

        res = curs.fetchall()
        conn.commit()
        conn.close()
        return res


if __name__ == '__main__':
    filename = "birthdays.db"

    bdb = BirthdayDB(filename)

    bdb.create()

    bdb.append(name='K', birthday='2001-11-25')
    bdb.append(name='V', birthday='2000-11-23')

    bdb.append(name='L', birthday='2040-10-10')
    print(bdb.find('K'))
    print(bdb.find_less_week())