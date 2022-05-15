from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QToolTip, QMainWindow, QLineEdit, QLabel, QPushButton, QMessageBox, QWidget, QGridLayout, QInputDialog, QFileDialog
from PyQt5.QtCore import QDir

import select
from utils import *
import os.path

class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

    def initUI(self):

        self.ttext = ''

        if os.path.exists('food.xlsx'):
            self.willpath = 'food.xlsx'
        else:
            self.willpath = '未选择'

        if os.path.exists('students.xlsx'):
            self.studentpath = 'students.xlsx'
        else:
            self.studentpath = '未选择'

        QToolTip.setFont(QFont('SansSerif', 12))
        self.setWindowTitle('五层今天吃什么')

        self.resize(600, 420)

        self.label_title = QLabel('餐券列表')

        self.food_inputs = []
        if self.willpath != '未选择':
            for i, fo in enumerate(auto_food_list()):
                self.food_inputs.append((QLineEdit(self), QLineEdit(self)))
                self.food_inputs[i][0].setText(fo)
        self.foodtype_cnt = len(self.food_inputs)

        self.button_new_ticket = QPushButton('新增餐券')
        self.button_new_ticket.clicked.connect(self.new_ticket)

        self.button_delete_ticket = QPushButton('删除餐券')
        self.button_delete_ticket.clicked.connect(self.delete_ticket)

        self.label_date = QLabel('请输入日期：')

        self.date_input = QLineEdit(self)
        self.date_input.setText(str(auto_date()))
        self.date_input.editingFinished.connect(self.date_or_path_change)

        self.button_execute = QPushButton('十连\n（消耗1600原石）')
        self.button_execute.clicked.connect(self.execute_gacha)
        if self.willpath == '未选择' or self.studentpath == '未选择':
            self.button_execute.setEnabled(False)

        self.label_studentpath1 = QLabel('学生名单文件：')
        self.label_studentpath2 = QLabel(self.studentpath)
        self.label_willpath1 = QLabel('餐券意愿文件：')
        self.label_willpath2 = QLabel(self.willpath)

        self.button_textinput = QPushButton('文本输入')
        self.button_textinput.clicked.connect(self.text_input)

        self.button_file_choose = QPushButton('手动选择文件')
        self.button_file_choose.clicked.connect(self.file_choose)

        self.button_about = QPushButton('关于')
        self.button_about.clicked.connect(self.about_info)

        self.moe_pic = QLabel(self)
        self.moe_pic.setPixmap(QPixmap('moe.jpg'))
        self.moe_pic.setScaledContents(True)

        self.mainLayout = QGridLayout(self)

        self.mainLayout.addWidget(self.label_title, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.button_new_ticket, 2, 1, 1, 1)
        self.mainLayout.addWidget(self.button_delete_ticket, 2, 2, 1, 1)

        for i, ticket in enumerate(self.food_inputs):
            self.mainLayout.addWidget(ticket[0], i + 3, 1, 1, 1)
            self.mainLayout.addWidget(ticket[1], i + 3, 2, 1, 1)

        self.mainLayout.addWidget(self.label_date, 1, 3, 1, 1)
        self.mainLayout.addWidget(self.date_input, 1, 4, 1, 1)
        self.mainLayout.addWidget(self.button_execute, 2, 3, 2, 2)
        self.mainLayout.addWidget(self.button_textinput, 4, 3, 1, 1)
        self.mainLayout.addWidget(self.button_file_choose, 4, 4, 1, 1)
        self.mainLayout.addWidget(self.label_studentpath1, 5, 3, 1, 1)
        self.mainLayout.addWidget(self.label_studentpath2, 5, 4, 1, 1)
        self.mainLayout.addWidget(self.label_willpath1, 6, 3, 1, 1)
        self.mainLayout.addWidget(self.label_willpath2, 6, 4, 1, 1)
        self.mainLayout.addWidget(self.moe_pic, 7, 3, 7, 2)
        self.mainLayout.addWidget(self.button_about, 14, 4, 1, 1)

        self.mainFrame = QWidget()
        self.mainFrame.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainFrame)

    def new_ticket(self):
        self.food_inputs.append((QLineEdit(self), QLineEdit(self)))
        self.foodtype_cnt += 1
        self.mainLayout.addWidget(self.food_inputs[-1][0], self.foodtype_cnt + 2, 1, 1, 1)
        self.mainLayout.addWidget(self.food_inputs[-1][1], self.foodtype_cnt + 2, 2, 1, 1)

    def delete_ticket(self):
        if self.foodtype_cnt == 0:
            QMessageBox.information(self, '没有惹', '已经被你删完惹')
            return
        self.food_inputs[-1][0].deleteLater()
        self.food_inputs[-1][1].deleteLater()
        self.food_inputs.pop(-1)
        self.foodtype_cnt -= 1

    def date_or_path_change(self):
        f_list = auto_food_list(self.date_input.text(), willpath=self.willpath)
        if f_list == -1:
            self.button_execute.setEnabled(False)
            return
        for i in range(self.foodtype_cnt):
            if f_list == []:
                for _ in range(i, self.foodtype_cnt):
                    self.delete_ticket()
            else:
                self.food_inputs[i][0].setText(f_list.pop(0))
        while f_list != []:
            self.new_ticket()
            self.food_inputs[-1][0].setText(f_list.pop(0))
        self.foodtype_cnt = len(self.food_inputs)

        if self.willpath != '未选择' and self.studentpath != '未选择':
            self.button_execute.setEnabled(True)
        if self.willpath == '' or self.studentpath == '':
            self.button_execute.setEnabled(False)


    def execute_gacha(self):
        f_list = []
        f_num = []
        if not legal_date(self.date_input.text()):
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
        select.select(f_list, f_num, date, self.studentpath, self.willpath)

    def text_input(self):
        q = QInputDialog.getMultiLineText(self, '文本输入', '请输入全部菜品及其数量：', '示例：\n炒饭32\n炒面24\n奶茶10')
        for f in self.food_inputs:
            f[1].setText('')
        p_input = div_text(q[0])

        unpaired_list = []
        for fo in p_input:
            flag = 0
            for ti in self.food_inputs:
                if fo[0] == ti[0].text():
                    ti[1].setText(str(fo[1]))
                    flag = 1
                    continue
            if flag == 0:
                unpaired_list.append(fo)
        warn_text = ''
        for fo in unpaired_list:
            for ti in self.food_inputs:
                if ti[1].text() == '':
                     print(str_compare(fo[0], ti[0].text()), fo[0], ti[0].text())
                     if str_compare(fo[0], ti[0].text()) > 0.5:
                         warn_text += f'\"{fo[0]}\"与\"{ti[0].text()}\"的匹配度达到{round(str_compare(fo[0], ti[0].text()), 2)}，已自动匹配\n\n'
                         ti[1].setText(str(fo[1]))
                         continue
        QMessageBox.information(self, 'Auto_Pairing', warn_text)

    def file_choose(self):
        QMessageBox.information(self, '注意', '请选择学生列表，通常为"student.xlsx"')
        self.studentpath = QFileDialog.getOpenFileName(self,'打开文件',QDir.currentPath(),"Execl files (*.xlsx)")[0]
        if len(self.studentpath) >= 30:
            self.label_studentpath2.setText('...'+self.studentpath[-30:])
        else:
            self.label_studentpath2.setText(self.studentpath)

        QMessageBox.information(self, '注意', '请选择学生列表，通常为"food.xlsx"')
        self.willpath = QFileDialog.getOpenFileName(self, '打开文件', QDir.currentPath(), "Execl files (*.xlsx)")[0]
        if len(self.willpath) >= 30:
            self.label_willpath2.setText('...'+self.willpath[-30:])
        else:
            self.label_willpath2.setText(self.willpath)
        self.date_or_path_change()

    def about_info(self):
        QMessageBox.information(self, 'About', '抽餐券系统，作者32yy&猫猫bot\n项目地址：https://github.com/32yy/FifthFloorEatWhat')

def legal_ticket(ticket):
    if type(ticket[0]) != str or len(ticket[0]) == 0:
        return False
    if ticket[1] <= 0:
        return False
    return True
