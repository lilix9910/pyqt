import datetime
import time

import pandas
from BaseFunc import except_err
from window import Ui_Form
import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from HandleThread import ThreadLogin, ThreadWatch, ThreadOpen, ThreadClose, ThreadGetDetail, ThreadTestTable


class Window(QWidget, Ui_Form):
    def __init__(self):
        super(Window, self).__init__()
        self.thread_login = None
        self.thread_watch = None
        self.thread_open = None
        self.thread_close = None
        self.setupUI()
        self.mk_signal()

    def setupUI(self):
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.tw_dd_output.setSelectionBehavior(QAbstractItemView.SelectRows)

    def mk_signal(self):
        # tab1
        self.btn_open.clicked.connect(self.slot_btn_open)
        self.btn_close.clicked.connect(self.slot_btn_close)
        self.btn_watch.clicked.connect(self.slot_btn_watch)
        self.btn_login.clicked.connect(self.slot_btn_login)

        # tab2
        self.pushButton.clicked.connect(self.slot_pushButton)
        self.pushButton_2.clicked.connect(self.slot_pushButton2)

        # self.tw_dd_output.itemClicked.connect(self.slot_tw)
        # self.tw_dd_output.cellPressed.connect(self.slot_tw)
        # self.tw_dd_output.cellPressed.connect(self.slot_tw)
        # self.tw_dd_output.itemChanged.connect(self.slot_tw)
        # self.tw_dd_output.itemActivated.connect(self.slot_tw)
        # self.tw_dd_output.cellActivated.connect(self.slot_tw)
        # self.tw_dd_output.pressed.connect(self.slot_tw)

    # slot
    def slot_btn_open(self):
        self.thread_open = ThreadOpen()
        if self.cb_cbss.isChecked():
            self.thread_open.cbss = True
        else:
            self.thread_open.cbss = False

        if self.cb_dd.isChecked():
            self.thread_open.dd = True
        else:
            self.thread_open.dd = False

        if self.cb_second.isChecked():
            self.thread_open.second = True
        else:
            self.thread_open.second = False

        if self.cb_old.isChecked():
            self.thread_open.old = True
        else:
            self.thread_open.old = False

        self.thread_open.signal_open.connect(self.rollback_open)
        self.thread_open.start()

    def slot_btn_close(self):
        self.thread_close = ThreadClose()
        if self.cb_cbss.isChecked():
            self.thread_close.cbss = True
        else:
            self.thread_close.cbss = False

        if self.cb_dd.isChecked():
            self.thread_close.dd = True
        else:
            self.thread_close.dd = False

        if self.cb_second.isChecked():
            self.thread_close.second = True
        else:
            self.cb_second.second = False

        if self.cb_old.isChecked():
            self.thread_close.old = True
        else:
            self.thread_close.old = False

        self.thread_close.signal_close.connect(self.rollback_close)
        self.thread_close.start()

    def slot_btn_watch(self):
        self.thread_watch = ThreadWatch()
        self.thread_watch.signal_watch.connect(self.rollback_watch)
        self.thread_watch.start()

    def slot_btn_login(self):
        self.thread_login = ThreadLogin()
        self.thread_login.signal_login.connect(self.rollback_login)
        self.thread_login.start()

    # tab2 btn
    def slot_pushButton(self):
        self.thread_get_detail = ThreadGetDetail()
        self.thread_get_detail.signal_get_detail.connect(self.rollback_get_detail)
        self.thread_get_detail.start()

    def slot_tw(self, QItem):
        from PyQt5.QtGui import QBrush, QColor
        if QItem.isSelected() is False:
            print("no select")
            QItem.setSelected(True)
            QItem.setBackground(QBrush(QColor(0, 255, 0)))
        else:
            print("yes select")
            QItem.setSelected(False)
            QItem.setBackground(QBrush(QColor(0, 0, 0)))
        print(datetime.datetime.now().strftime("%Y-%M-%d %T"), "--->", QItem.text())

    def slot_pushButton2(self):
        a = self.tw_dd_output.selectedIndexes()
        row_set = set()
        for i in a:
            # print(i.row(), i.column(), i.data())
            row_set.add(i.row())

        self.th_dict = dict()
        for i in row_set:
            # th_lst.append(ThreadTestTable())
            # print(th_lst[len(th_lst)-1])
            # th_lst[len(th_lst)-1].signal_test_table.connect(self.rollback_test_table)
            # th_lst[len(th_lst)-1].start()
            self.thread_test_table = ThreadTestTable(i)
            self.thread_test_table.signal_test_table.connect(self.rollback_test_table)
            self.th_dict.update({i: self.thread_test_table})
            self.thread_test_table.start()

        # self.tw_dd_output.sortByColumn()

        # d = self.tw_dd_output.selectedRanges()
        # for b in d:
        #     # print(i.rowCount())
        #     # print(b.rowCount(), b.columnCount(), b.topRow(), b.leftColumn())
        #     for i in range(b.topRow(), b.topRow()+b.rowCount()):
        #         for j in range(b.leftColumn(), b.leftColumn()+b.columnCount()):
        #             print(i, j, self.tw_dd_output.item(i, j).text())

        # c = self.tw_dd_output.selectedItems()
        # print("c", len(c))
        # for i in c:
        #     print(i.row(), i.column(), i.text())

    # 回调
    def rollback_login(self, return_str):
        self.te_output.append(return_str)

    def rollback_watch(self, return_str):
        self.te_output.append(return_str)

    def rollback_open(self, return_str):
        self.te_output.append(return_str)

    def rollback_close(self, return_str):
        self.te_output.append(return_str)

    def rollback_get_detail(self, return_df):
        # return_df = pd.read_csv("./1.txt")
        self.tw_dd_output.insert_df(return_df)

    def rollback_test_table(self, ret_tuple):
        # print("第%s行结束" % str(ret_tuple))
        self.tw_dd_output.setItem(ret_tuple[0], 0, QTableWidgetItem(str(ret_tuple[1])))
        print(self.th_dict)
        self.th_dict.pop(ret_tuple[0])
        self.pushButton_2.setText(str(len(self.th_dict)))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
