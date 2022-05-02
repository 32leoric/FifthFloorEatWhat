# ver 1.0.1

import logging
import sqlite3
import sys
from collections import defaultdict
from random import shuffle

import xlrd
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_students_list():
    data = xlrd.open_workbook("students.xlsx")
    table = data.sheet_by_name("Sheet1")
    names = table.col_values(0)
    for i, name in enumerate(names):
        if type(name) == float:
            names[i] = str(int(names[i]))

    return names


class Wills:
    def __init__(self):
        self.wills = defaultdict(list)
        self.foods = defaultdict(int)
        self.students = []

    def get_students(self, li, li2):
        self.students = li + li2

    def get_foods(self, foods: dict):
        self.foods |= foods

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
                if self.wills[names[row]]:
                    self.wills[names[row]] = []
                self.wills[names[row]].append(first[row])
                self.wills[names[row]].append(second[row])
                self.wills[names[row]].append(third[row])


def main():
    # 在下面填日期，食物种类和数量
    foods = {"奶茶": 10, "炒饭": 2, "炒粉": 3, "鱼粉": 3, "麻辣鸡块面": 5, "油泼面": 9}
    date = "4.25"

    conn = sqlite3.connect("record.db")
    cur = conn.cursor()

    sql = f"SELECT * FROM record"

    try:
        del_names = cur.execute(sql)
    except sqlite3.OperationalError:
        logging.critical(f"生成学生名单失败")
        raise

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

    shuffle(student_list)
    shuffle(student_list_2)
    student_list += student_list_2

    # 获取一下食物的种类和份数，学生名单，学生志愿。
    w = Wills()
    w.get_students(student_list, student_list_2)
    w.get_foods(foods)
    w.get_wills(date)

    # 从学生列表头开始，根据当前同学的志愿顺序发放餐券，如果三种都发完了就运气不是很好，直到餐券全部发放完毕。
    result = []
    while len(result) < sum(foods.values()) and student_list != []:
        stu = student_list.pop(0)
        for food_name in w.wills[stu]:
            if w.foods[food_name] >= 1:
                result.append((food_name, stu))
                w.foods[food_name] -= 1
                break

    result.sort()
    lucky = defaultdict(list)
    for i in result:
        lucky[i[0]].append(i[1])

    QApplication(sys.argv)
    wid = QWidget()

    # 生成一个结果字符串
    luckers = ""
    for k, v in lucky.items():
        luckers += f"分到{k}的学生有：\n{v}，共{len(v)}人\n\n"
    for k, v in w.foods.items():
        luckers += f"{k}剩余：{v}份\n"

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
                except sqlite3.OperationalError:
                    logging.critical(f"数据插入失败：{n} {date}")
                    raise


if __name__ == "__main__":
    main()
