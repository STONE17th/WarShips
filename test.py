#!/usr/bin/python3

import os

with open('1') as f:
    str_lst = f.readlines()
    for i in range(1,len(str_lst)):
        if str_lst[i].split()[0] == '<none>':
            rm_str = str_lst[i].split()[2]
            print(rm_str)

            os.system(f'docker image rm {rm_str}')
