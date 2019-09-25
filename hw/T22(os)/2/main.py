#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov



import os


def compare(path1, path2, filename='result.txt'):
    set1 = set()
    set2 = set()

    for cur in os.walk(path1):
        cur_path, _, cur_files = cur
        for file in cur_files:
            set1.add('/'.join(os.path.join(cur_path, file).split('/')[1:]))

    for cur in os.walk(path2):
        cur_path, _, cur_files = cur
        for file in cur_files:
            set2.add('/'.join(os.path.join(cur_path, file).split('/')[1:]))

    with open(filename, 'w') as fout:
        fout.write('\n'.join(set1 ^ set2))


if __name__ == '__main__':
    compare('dir1', 'dir2')