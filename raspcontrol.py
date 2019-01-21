from config import path_to_rasp, date
from os import listdir, remove
from re import sub
from time import sleep

path = path_to_rasp
while True:
    datas = [date(i) for i in range(7)]
    share = listdir(path)
    if not share == []:
        for file in share:
            name = sub('....$', '', file)
            name = sub('^....', '', name)
            if name not in datas:
                try:
                    remove(path + file)
                except Exception as e:
                    pass
    sleep(3600)
    