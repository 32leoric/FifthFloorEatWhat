import datetime

import xlrd


def auto_date():
    m = datetime.date.today().month
    d = datetime.date.today().day
    ret = m + 0.01 * d if d >= 10 else m + 0.1 * d
    return ret


def auto_food_list():
    data = xlrd.open_workbook("food.xlsx")
    table = data.sheet_by_name('Sheet1')
    dt = auto_date()
    foods = []

    dates = table.col_values(6)
    first = table.col_values(8)
    second = table.col_values(9)
    third = table.col_values(10)

    for row in range(0, len(dates)):
        if dates[row] == str(dt):
            if first[row] not in foods:
                foods.append(first[row])
            if second[row] not in foods:
                foods.append(second[row])
            if third[row] not in foods:
                foods.append(third[row])

    return foods
