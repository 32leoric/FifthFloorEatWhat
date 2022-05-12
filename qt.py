from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QToolTip, QMainWindow, QLineEdit, QLabel, QPushButton, QMessageBox, QWidget, QGridLayout

import select
from utils import *


class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

    def initUI(self):

        self.ttext = ''

        QToolTip.setFont(QFont('SansSerif', 12))
        self.setWindowTitle('五层今天吃什么')

        self.resize(600, 420)

        self.label_title = QLabel('餐券列表')

        self.food_inputs = []
        for i, fo in enumerate(auto_food_list()):
            self.food_inputs.append((QLineEdit(self), QLineEdit(self)))
            self.food_inputs[i][0].setText(fo)
        self.foodtype_cnt = len(self.food_inputs)

        self.button_new_ticket = QPushButton('增加新餐券')
        self.button_new_ticket.clicked.connect(self.new_ticket)

        self.label_date = QLabel('请输入日期：')

        self.date_input = QLineEdit(self)
        self.date_input.setText(str(auto_date()))

        self.button_execute = QPushButton('十连\n（消耗1600原石）')
        self.button_execute.clicked.connect(self.execute_gacha)

        self.button_statis = QPushButton('数据统计')
        self.button_statis.clicked.connect(self.statis_on_someone)

        self.button_about = QPushButton('关于')
        self.button_about.clicked.connect(self.about_info)

        self.moe_pic = QLabel(self)
        self.moe_pic.setPixmap(QPixmap('moe.jpg'))
        self.moe_pic.setScaledContents(True)

        self.mainLayout = QGridLayout(self)

        self.mainLayout.addWidget(self.label_title, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.button_new_ticket, 1, 2, 1, 1)

        for i, ticket in enumerate(self.food_inputs):
            self.mainLayout.addWidget(ticket[0], i + 2, 1, 1, 1)
            self.mainLayout.addWidget(ticket[1], i + 2, 2, 1, 1)

        self.mainLayout.addWidget(self.label_date, 1, 3, 1, 1)
        self.mainLayout.addWidget(self.date_input, 1, 4, 1, 1)
        self.mainLayout.addWidget(self.button_execute, 2, 3, 2, 2)
        self.mainLayout.addWidget(self.button_statis, 4, 3, 2, 1)
        self.mainLayout.addWidget(self.button_about, 4, 4, 2, 1)
        self.mainLayout.addWidget(self.moe_pic, 6, 3, 7, 2)

        self.mainFrame = QWidget()
        self.mainFrame.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainFrame)

    def new_ticket(self):
        self.food_inputs.append((QLineEdit(self), QLineEdit(self)))
        self.foodtype_cnt += 1
        self.mainLayout.addWidget(self.food_inputs[-1][0], self.foodtype_cnt + 1, 1, 1, 1)
        self.mainLayout.addWidget(self.food_inputs[-1][1], self.foodtype_cnt + 1, 2, 1, 1)

    def execute_gacha(self):
        f_list = []
        f_num = []
        if not legal_date():
            QMessageBox.information(self, 'error', '日期错误')
        for tic in self.food_inputs:

            try:
                t = (tic[0].text(), int(tic[1].text()))
            except Exception:
                QMessageBox.information(self, 'Error', f'有错误餐券喵\n{tic[0].text()} {tic[1].text()}')
                continue

            if not legal_ticket(t) or t[0] in f_list:
                QMessageBox.information(self, 'Error', f'有错误餐券喵\n{tic[0].text()} {tic[1].text()}')
            else:
                f_list.append(t[0])
                f_num.append(t[1])
        date = float(self.date_input.text())
        select.select(f_list, f_num, date)

    def statis_on_someone(self):
        QMessageBox.information(self, 'yee', "No available")

    def about_info(self):
        QMessageBox.information(self, 'About', '抽餐券系统，作者32yy&猫猫bot\n项目地址：https://github.com/32yy/FifthFloorEatWhat')


def legal_date():
    return True


def legal_ticket(ticket):
    if type(ticket[0]) != str or len(ticket[0]) == 0:
        return False
    if ticket[1] <= 0:
        return False
    return True
