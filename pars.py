import xlrd
from re import sub
from os import remove
from config import *


def file_read(name_file):
    rb = xlrd.open_workbook(name_file, formatting_info=False)
    sheet = rb.sheet_by_index(0)
    data = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        data.append(row)
    return data


def pars(data, groop, name):
    t = False
    for stroka_raspisania in range(len(data)):
        for i in range(len(data[stroka_raspisania])):
            if groop in data[stroka_raspisania][i]:
                t = True
                break
        if t:
            break
    ret = []
    ret.append('расписание на ' + sub('.xlsx', '', name))
    para_number = 1
    for n in range(stroka_raspisania+1, stroka_raspisania+7):
        para = str(para_number)+'.'+data[n][i]
        if len(para) == 2:
            para += '-----'
        ret.append(para)
        para_number += 1
    for i in range(len(ret)):
        if 'УП' in ret[i]:
            ret[i + 1] = str(i+1) + '.УП'
            ret[i + 2] = str(i+3) + '.УП'
            break
    file = open(path_to_rasp + groop + '_' + sub('.xlsx', '', name) + '.txt', 'w')
    file.write('\n'.join(ret))
    file.close()


def parsing(name):
    non_groop = []
    otvet = False
    file = open(patt_to_groop, 'r')
    groop = file.readlines()
    file.close()
    try:
        data = file_read(path_to_parsing + name)
        for ng in groop:
            try:
                pars(data, sub('\n', '', ng), name)
            except Exception as e:
                non_groop.append(ng)
        remove(path_to_parsing + name)
    except Exception as e:
        remove(path_to_parsing + name)
        otvet = True
    return [otvet, non_groop]


if __name__ == '__main__':
    pass