import sqlite3

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

from gacha import *


def select(food_type, food_num, date):
    conn = sqlite3.connect('record.db')
    cur = conn.cursor()

    sql = f'SELECT * FROM record'

    del_names = 0
    try:
        del_names = cur.execute(sql)
    except Exception:
        print(f'生成学生名单失败')

    # 获取前一天抽到的人，放进另一个list里，和其余同学的list分别打乱并重组。
    del_names = del_names.fetchall()
    del_names = del_names[::-1]
    if len(del_names) != 0:
        date0 = del_names[0][1]
    else:
        date0 = '0.00'
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
    w.get_students(student_list)
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

    wid = QWidget()

    # 生成一个结果字符串
    luckers = ''
    for key in lucky:
        luckers += f'分到{key}的学生有：\n{lucky[key]}，共{len(lucky[key])}人\n\n'
    for key in w.food:
        if key in food_type:
            luckers += f'{key}剩余：{w.food[key]}份\n'
        else:
            luckers += f'{key}(不在名单中)剩余：{w.food[key]}份\n'

    yes = QMessageBox.question(wid, 'message', f'选取完成，以下是选取结果，是否采用？\n{luckers}', QMessageBox.Yes | QMessageBox.Cancel)
    if yes == QMessageBox.Yes:
        print(luckers)

        for key in lucky:
            for n in lucky[key]:
                sql = f'INSERT INTO record (name, date) values(\'{n}\', \'{date}\')'
                try:
                    cur.execute(sql)
                    conn.commit()
                except Exception:
                    print(f'数据插入失败：{n} {date}')
        QMessageBox.information(wid, 'Complete', '数据导入完成', QMessageBox.Yes)
