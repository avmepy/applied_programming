#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import re
import datetime

def main(input, output):
    with open(input, 'r') as f:
        st = f.read()

    dates = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', st)

    st = st.replace('__.__.____', str(datetime.datetime.now().date()))

    with open(output, 'w') as g:
        g.write(st)


    return dates


if __name__ == '__main__':
    print(main('input.txt', 'output.txt'))