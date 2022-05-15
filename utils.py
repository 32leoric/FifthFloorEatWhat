import datetime

import xlrd

def auto_date():
    m = datetime.date.today().month
    d = datetime.date.today().day
    ret = m + 0.01 * d if d >= 10 else m + 0.1 * d
    return ret

def legal_date(date):
    try:
        date = float(date)
    except Exception:
        return False

    if date >= 13 or date < 1 or date % 1 > 31:
        return False
    return True

def auto_food_list(dt = auto_date(), willpath = 'food.xlsx'):
    dt = str(dt)
    try:
        data = xlrd.open_workbook(willpath)
    except Exception:
        return -1
    table = data.sheet_by_name('Sheet1')
    foods = []

    dates = table.col_values(6)
    first = table.col_values(8)
    second = table.col_values(9)
    third = table.col_values(10)

    for row in range(0, len(dates)):
        if str(dates[row]) == dt:
            if first[row] not in foods:
                foods.append(first[row])
            if second[row] not in foods:
                foods.append(second[row])
            if third[row] not in foods:
                foods.append(third[row])

    return foods

def div_text(text):
    start = 0
    flag = 0  #0表示正在接收菜品，1表示正在接收数字，-1表示寄了

    foodname = ''
    foods = []

    i = 0
    while i < len(text):
        if text[i] == ' ' or text[i] == '\n':
            text = text[:i]+text[i+1:] if i != len(text)-1 else text[:i]
        i += 1

    for i, c in enumerate(text):
        if flag == 0:
            if ord(c) >= 48 and ord(c) <= 57:
                foodname = text[start:i]
                start = i
                flag = 1
        elif flag == 1:
            if ord(c) < 48 or ord(c) > 57:
                try:
                    foodnum = int(text[start:i])
                    foods.append((foodname, foodnum))
                    start = i
                    flag = 0
                except Exception:
                    print('Wrong Input')
                    flag = -1
        elif flag == -1:
            break
    if flag == 1:
        try:
            foodnum = int(text[start:])
            foods.append((foodname, foodnum))
        except Exception:
            print('Wrong Input')
    return foods

def str_compare(str1, str2):
    l1 = len(str1)
    l2 = len(str2)
    if l1 == 0 or l2 == 0:
        return 0.00
    else:
        cp_table = [[0 for _ in range(l1)] for _ in range(l2)]
        cp_table[0][0] = 0 if str1[0] == str2[0] else 1

        for i in range(1, l1):
            cp_table[0][i] = cp_table[0][i-1] if str1[i] == str2[0] else cp_table[0][i-1]+1
        for i in range(1, l2):
            cp_table[i][0] = cp_table[i-1][0] if str1[0] == str2[i] else cp_table[i-1][0]+1
        for i in range(1, l1):
            for j in range(1, l2):
                t = min(cp_table[j-1][i], cp_table[j][i-1], cp_table[j-1][i-1])
                cp_table[j][i] = t if str1[i] == str2[j] else t+1
        return 1-cp_table[-1][-1]/max(l1, l2)
