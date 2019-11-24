#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import sqlite3
from tkinter import *



class ToysDB:

    def __init__(self, filename):
        self.filename = filename


    def create(self):

        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        try:
            curs.execute("CREATE TABLE toys (name TEXT, cost INT, age1 INT, age2 INT)")
        except:
            pass
        conn.commit()
        conn.close()


    def append(self, name, cost, age1, age2):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute("INSERT INTO toys VALUES (?, ?, ?, ?)", (name, cost, age1, age2))

        conn.commit()
        conn.close()


    def find(self, cost_inp, age_inp):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        if age_inp != "" and cost_inp != "":
            curs.execute("SELECT name FROM toys WHERE ? >= cost AND age1 <= ? AND ? <= age2  ", (int(cost_inp), int(age_inp), int(age_inp)))
        elif age_inp != "" and cost_inp == "":
            curs.execute("SELECT name FROM toys WHERE age1 <= ? AND ? <= age2  ",  (int(age_inp), int(age_inp)))
        elif age_inp == "" and cost_inp != "":
            curs.execute("SELECT name FROM toys WHERE ? >= cost", (int(cost_inp), ))
        else:
            curs.execute("SELECT name FROM toys")

        res = curs.fetchall()
        conn.commit()
        conn.close()
        return res



file = "toys.db"

tdb = ToysDB(file)
tdb.create()




top = Tk()
Label(top, text="age: ").grid(row=0, column=0)
Label(top, text="cost: ").grid(row=1, column=0)

ent_age = Entry(top)
ent_age.grid(row=0, column=1)

ent_cost = Entry(top)
ent_cost.grid(row=1, column=1)

res = Label(top, text="result: ")
res.grid(row=4, column=1)


def find_toy():
    age = ent_age.get()
    cost = ent_cost.get()
    res.config(text='\n'.join(' '.join(i) for i in tdb.find(cost_inp=cost, age_inp=age)))


but_find = Button(top, text="find", command=find_toy)
but_find.grid(row=2, column=1)


def create_dialog_add():
    d = Tk()

    Label(d, text="name: ").grid(row=0, column=0)
    Label(d, text="cost: ").grid(row=1, column=0)
    Label(d, text="age (* - *): ").grid(row=2, column=0)

    ent_name_d = Entry(d)
    ent_name_d.grid(row=0, column=1)

    ent_cost_d = Entry(d)
    ent_cost_d.grid(row=1, column=1)

    ent_age_d = Entry(d)
    ent_age_d.grid(row=2, column=1)


    def append():
        name = ent_name_d.get()
        cost = int(ent_cost_d.get())
        age1, age2 = str(ent_age_d.get()).split("-")
        tdb.append(name=name, cost=cost, age1=int(age1), age2=int(age2))

    but_submit = Button(d, text="submit", command=append)
    but_submit.grid(row=3, column=1)



    but_close = Button(d, text="close", command=d.destroy)
    but_close.grid(row=4, column=1)

    d.mainloop()









add_but = Button(top, text="add", command=create_dialog_add)
add_but.grid(row=3, column=1)



top.mainloop()




