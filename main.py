import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Nsop import nsop
from PyQt5.QtGui import QPixmap
import pandas as pd


class MyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(MyLabel, self).__init__(*args, **kwargs)

    def mousePressEvent(self, *args, **kwargs):
        super(MyLabel, self).mousePressEvent(*args, **kwargs)
        self.parent().changeImg()  # type: ignore


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.n = nsop()

    def setUI(self):
        self.setFixedSize(640, 480)
        self.setWindowTitle("PyGames")

        maniLayout = QGridLayout(self)
        maniLayout.setSpacing(10)
        self.my_label_name = QLabel("工号", self)
        self.my_line_name = QLineEdit("zhangzl37", self)
        maniLayout.addWidget(self.my_label_name, 0, 0, 1, 1)
        maniLayout.addWidget(self.my_line_name, 0, 1, 1, 1)
        maniLayout.columnStretch(5)

        self.my_label_pass = QLabel("密码", self)
        self.my_line_pass = QLineEdit("zhangzl37", self)
        maniLayout.addWidget(self.my_label_pass, 1, 0)
        maniLayout.addWidget(self.my_line_pass, 1, 1)

        # 验证码图片
        self.my_image_label = MyLabel("image图片", self)
        maniLayout.addWidget(self.my_image_label, 2, 0)

        # 验证码输入框
        self.le_image = QLineEdit("", self)
        # self.le_image.textChanged.connect(self.login)
        maniLayout.addWidget(self.le_image, 2, 1)

        # 登陆按钮
        self.my_button_login = QPushButton("Login", self)
        self.my_button_login.setToolTip("别点我")
        maniLayout.addWidget(self.my_button_login, 3, 0)
        self.my_button_login.clicked.connect(self.login)

        # 输出按钮
        self.teOutput = QTextEdit(self)
        maniLayout.addWidget(self.teOutput, 6, 0, 3, 6)

        # 复选框
        self.cb1 = QCheckBox("111111", self)
        self.cb2 = QCheckBox("2222", self)
        self.cb3 = QCheckBox("33333", self)
        self.cb4 = QCheckBox("44444444", self)
        maniLayout.addWidget(self.cb1, 4, 0, 1, 2)
        maniLayout.addWidget(self.cb2, 4, 2, 1, 2)
        maniLayout.addWidget(self.cb3, 4, 4, 1, 2)
        maniLayout.addWidget(self.cb4, 4, 6, 1, 2)

        # 监控按钮
        self.my_button_watch = QPushButton("监控", self)
        self.my_button_watch.setToolTip("别点我")
        self.my_button_watch.clicked.connect(self.watch)
        maniLayout.addWidget(self.my_button_watch, 5, 0)

        maniLayout.setColumnStretch(9, 1)
        maniLayout.setRowStretch(8, 1)
        self.setLayout(maniLayout)

    # 槽
    def login(self):
        while True:
            if self.n.login():
                self.printImage()
                self.le_image.setText(self.n.captcha)
                break

    def watch(self):
        if self.cb1.isChecked():
            print("cb1选中")
        if self.cb2.isChecked():
            print("cb2选中")
        if self.cb3.isChecked():
            print("cb3选中")
        if self.cb4.isChecked():
            print("cb4选中")

        self.n.load_ck_token()
        self.n.listen_pool()
        # for i in range(2):
        #     r = self.n.modify_order_pool(i, "close")
        #     self.teOutput.append(r)

    def printImage(self):
        self.my_image_label.setPixmap(QPixmap("./nsop.png"))

    # cao
    def changeImg(self):
        self.printImage()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
