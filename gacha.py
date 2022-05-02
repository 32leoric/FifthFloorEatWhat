# ver 1.0.1

import os
import random
import sqlite3
import sys
import time
from collections import defaultdict

import xlrd
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMessageBox

illegal_char_list = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    ",",
    ".",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    " ",
    "(",
    ")",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "+",
    "-",
    "*",
    "/",
]


def get_students_list():
    data = xlrd.open_workbook("students.xlsx")
    table = data.sheet_by_name("Sheet1")
    names = table.col_values(0)
    for i, name in enumerate(names):
        if type(name) == float:
            names[i] = str(int(names[i]))

    return names


def mixstudents(li):
    print("正在打乱学生名单", end="")
    for i in range(100000):
        if i % 10000 == 0:
            print("○", end="")
        random.shuffle(li)
    print("完成")


def name_process(name):
    p_name = ""
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

    def get_students(self, li, li2):
        for s in li:
            self.students.append(s)
        for s in li2:
            self.students.append(s)

    def get_foods(self, types, nums):
        for i in range(len(types)):
            self.food[types[i]] = nums[i]

    # 获得志愿时，检查日期，学生是否在学生列表，以及是否多次填写。杜绝了多次填写，改名等手段
    def get_wills(self, date):
        data = xlrd.open_workbook("food.xlsx")
        table = data.sheet_by_name("Sheet1")

        dates = table.col_values(6)
        names = table.col_values(7)
        first = table.col_values(8)
        second = table.col_values(9)
        third = table.col_values(10)

        for i, n in enumerate(names):
            if type(n) == float:
                names[i] = str(int(n))

        for row in range(0, len(names)):
            if dates[row] == date and names[row] in self.students:
                if self.wills[names[row]] != []:
                    self.wills[names[row]] = []
                self.wills[names[row]].append(first[row])
                self.wills[names[row]].append(second[row])
                self.wills[names[row]].append(third[row])


if __name__ == "__main__":  # 主程序

    # 在下面填日期，食物种类和数量
    food_type = ["奶茶", "炒饭", "炒粉", "鱼粉", "麻辣鸡块面", "油泼面"]
    food_num = [10, 2, 3, 3, 5, 9]
    date = "4.25"

    conn = sqlite3.connect("record.db")
    cur = conn.cursor()

    sql = f"SELECT * FROM record"

    try:
        del_names = cur.execute(sql)
    except Exception:
        print(f"生成学生名单失败")

    # 获取前一天抽到的人，放进另一个list里，和其余同学的list分别打乱并重组。
    del_names = del_names.fetchall()
    del_names = del_names[::-1]
    if len(del_names) != 0:
        date0 = del_names[0][1]
    else:
        date0 = "0.00"
    all_names = get_students_list()
    student_list = []
    student_list_2 = []

    namelist2 = []
    for data in del_names:
        if data[1] == date0:
            namelist2.append(data[0])
        else:
            break

    for name in all_names:
        if name not in namelist2:
            student_list.append(name)
        else:
            student_list_2.append(name)

    mixstudents(student_list)
    mixstudents(student_list_2)
    student_list += student_list_2

    # 获取一下食物的种类和份数，学生名单，学生志愿。
    w = Wills()
    w.get_students(student_list, student_list_2)
    w.get_foods(food_type, food_num)
    w.get_wills(date)

    # 从学生列表头开始，根据当前同学的志愿顺序发放餐券，如果三种都发完了就运气不是很好，直到餐券全部发放完毕。
    result = []
    while len(result) < sum(food_num) and student_list != []:
        stu = student_list.pop(0)
        for foodname in w.wills[stu]:
            if w.food[foodname] >= 1:
                result.append((foodname, stu))
                w.food[foodname] -= 1
                break

    result.sort()
    lucky = defaultdict(list)
    for i in result:
        lucky[i[0]].append(i[1])

    app = QApplication(sys.argv)
    wid = QWidget()

    # 生成一个结果字符串
    luckers = ""
    for key in lucky:
        luckers += f"分到{key}的学生有：\n{lucky[key]}，共{len(lucky[key])}人\n\n"
    for key in w.food:
        luckers += f"{key}剩余：{w.food[key]}份\n"

    yes = QMessageBox.question(
        wid,
        "message",
        f"选取完成，以下是选取结果，是否采用？\n{luckers}",
        QMessageBox.Yes | QMessageBox.Cancel,
    )
    if yes == QMessageBox.Yes:
        print(luckers)

        for key in lucky:
            for n in lucky[key]:
                sql = f"INSERT INTO record (name, date) values('{n}', '{date}')"
                try:
                    cur.execute(sql)
                    conn.commit()
                except Exception:
                    print(f"数据插入失败：{name} {date}")
