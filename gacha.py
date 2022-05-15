from collections import defaultdict
from random import shuffle

import xlrd

illegal_char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z',
                     ',', '.', '!', '@', '#', '$', '%', '^', '&', ' ', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8',
                     '9', '0', '+', '-', '*', '/']


def get_students_list(student_path):
    try:
        data = xlrd.open_workbook(student_path)
    except Exception:
        print('无法读取学生数据')
        return
    table = data.sheet_by_name('Sheet1')
    names = table.col_values(0)
    for i, name in enumerate(names):
        if type(name) == float:
            names[i] = str(int(names[i]))
    return names


def mixstudents(li):
    print('正在打乱学生名单', end='')
    for i in range(10):
        if i % 10000 == 0:
            print('○', end='')
        shuffle(li)
    print('完成')


def name_process(name):
    p_name = ''
    for c in name:
        if c not in illegal_char_list:
            p_name += c
    return p_name


class Wills:
    wills = defaultdict(list)
    food = defaultdict(int)
    students = []

    def __init__(self):
        pass

    def get_students(self, li):
        for s in li:
            self.students.append(s)

    def get_foods(self, types, nums):
        for i in range(len(types)):
            self.food[types[i]] = nums[i]

    # 获得志愿时，检查日期，学生是否在学生列表，以及是否多次填写。杜绝了多次填写，改名等手段
    def get_wills(self, date, willpath):
        try:
            data = xlrd.open_workbook(willpath)
        except Exception:
            print('无法读取学生志愿数据')
            return

        table = data.sheet_by_name('Sheet1')

        dates = table.col_values(6)
        names = table.col_values(7)
        first = table.col_values(8)
        second = table.col_values(9)
        third = table.col_values(10)

        for row in range(0, len(names)):
            if dates[row] == str(date) and names[row] in self.students:
                self.wills[names[row]] = [first[row], second[row], third[row]]
