#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


from threading import Thread
from time import sleep
from queue import Queue
import random

q = Queue()

t1 = 2
t2 = 2


def f1():
    while True:
        sleep(random.randrange(1, t1))
        q.put(''.join([chr(random.randint(1, 1000)) for _ in range(random.randint(2, 20))]))


def f2():
    while True:
        sleep(random.randrange(1, t2))
        print(q.get())

th1 = Thread(target=f1, daemon=True)
th2 = Thread(target=f2, daemon=True)

th1.start()
th2.start()

th1.join()
th2.join()