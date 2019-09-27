#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov



import os


def clear(path):
    """
    clear all duplicates in directory path
    :param path: directory
    :return: None
    """
    files = {}  #  (filename, size) :  absolute path
    for cur in os.walk(path):
        cur_path, _, cur_files = cur
        for file in cur_files:
            res = os.path.join(cur_path, file)
            size = os.path.getsize(res)


            if (file, size) not in files.keys():
                files[(file, size)] = res
            else:
                if files[(file, size)].count('/') < res.count('/'):
                    os.remove(res)
                    print(f'remove file ...... {res}')
                else:
                    os.remove(files[(file, res)])
                    print(f'remove file ...... {files[(file, res)]}')
                    files[(file, res)] = res



if __name__ == '__main__':
    clear('test')