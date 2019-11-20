#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


from threading import RLock, Thread
from random import randrange
from queue import Queue
import time
import logging

logging.basicConfig(level=logging.DEBUG)

path = True
direct = ''
time_to_free = time.time()


t1 = 1
t2 = 3


t3 = 3
t4 = 5


q_right = Queue()
q_left = Queue()
q_time = Queue()

lock = RLock()


def f_right():
    while True:
        time.sleep(randrange(t3, t4))
        q_right.put('left')
        logging.info('added (left)')

def f_left():
    while True:
        time.sleep(randrange(t3, t4))
        q_left.put('right')
        logging.info('added (right)')


def worker(direction):

    global path, direct, time_to_free


    while True:
        cur = q_right.get() if direction == 'right' else q_left.get()
        temp_time = randrange(t1, t2)

        if not (path or direct == cur):
            while True:
                if time.time() > time_to_free:
                    break
                else:
                    time.sleep(time_to_free-time.time())
        with lock:

            time_to_free = max(time.time() + temp_time, time_to_free)
            direct = direction
            Thread(target=tmp, args=(temp_time, direct), daemon=True).start()
        time.sleep(0)


def tmp(tim, direct):
    logging.info(f'train from {direct} started, will arrive at {time.time() + time_to_free}')
    time.sleep(tim)
    logging.info(f'train arrived!')



if __name__ == '__main__':
    th1 = Thread(target=worker, args=('left', ), daemon=True)
    th2 = Thread(target=worker, args=('right', ), daemon=True)

    th3 = Thread(target=f_left, args=(), daemon=True)
    th4 = Thread(target=f_right, args=(), daemon=True)

    th3.start()
    th4.start()
    th1.start()
    th2.start()


    th1.join()








