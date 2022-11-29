from go_ui import Ui_Form
from HandleThread import ThreadLogin, ThreadGetDetail, ThreadGo, ThreadLoginDD, ThreadWatch, ThreadOpen, ThreadClose
import sys
from PyQt5.QtWidgets import QWidget, QApplication


class Window(QWidget, Ui_Form):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUI()
        self.mk_signal()

    def setupUI(self):
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.textEdit.setEnabled(False)

    def mk_signal(self):
        # tab1
        self.btn_open.clicked.connect(self.slot_btn_open)
        self.btn_close.clicked.connect(self.slot_btn_close)
        self.btn_watch.clicked.connect(self.slot_btn_watch)
        self.pushbtn_login_dd.clicked.connect(self.slot_pushbtn_login_dd)
        self.pushbtn_login.clicked.connect(self.slot_pushbtn_login)

        # tab2
        self.pushbtn_search.clicked.connect(self.slot_pushbtn_search)
        self.pushbtn_go.clicked.connect(self.slot_pushbtn_go)

    # tab1 slot
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

    def slot_pushbtn_login_dd(self):
        """
        槽函数 系统登陆 o
        :return:
        """
        print("槽函数 系统登陆 o")

        self.pushbtn_login_dd.setEnabled(False)
        self.textEdit.append("正在登录...")
        self.thread_login_dd = ThreadLoginDD()
        self.thread_login_dd.signal_login_dd.connect(self.rollback_pushbtn_login_dd)
        self.thread_login_dd.start()

    def slot_pushbtn_login(self):
        """
        槽函数 系统登陆
        :return:
        """
        print("槽函数 系统登陆 1")

        self.pushbtn_login.setEnabled(False)
        self.textEdit.append("正在登录...")
        self.thread_login = ThreadLogin()
        self.thread_login.signal_login.connect(self.rollback_pushbtn_login)
        self.thread_login.start()

    # tab2 slot
    def slot_pushbtn_search(self):
        """
        槽函数 系统登陆 o
        :return:
        """
        print("槽函数 slot_pushbtn_search")
        self.le_name.setText('')
        self.le_telnum.setText('')
        self.le_pspid.setText('')
        self.le_address.setText('')

        self.textEdit.setText("正在查询...")
        self.thread_search = ThreadGetDetail(self.le_orderid.text().strip())
        self.thread_search.signal_get_detail.connect(self.rollback_pushbtn_search)
        self.pushbtn_go.setEnabled(False)
        self.pushbtn_search.setEnabled(False)
        self.thread_search.start()

    def slot_pushbtn_go(self):
        """

        :return:
        """
        print("槽函数 slot_pushbtn_go")
        self.le_name.setEnabled(False)
        self.le_telnum.setEnabled(False)
        self.le_pspid.setEnabled(False)
        self.le_address.setEnabled(False)

        input_dict = {
            "inner_custName": self.le_name.text(),
            "inner_ContactTel": self.le_telnum.text(),
            "inner_mainPsptId": self.le_pspid.text(),
            "inner_preAddressInfo": self.le_address.text(),
        }

        self.textEdit.setText("开始录入...")
        # self.textEdit.append("-" * 10)
        self.textEdit.append("姓名:{}".format(input_dict.get('inner_custName', "None")))
        self.textEdit.append("联系电话:{}".format(input_dict.get('inner_ContactTel', "None")))
        self.textEdit.append("证件号码:{}".format(input_dict.get('inner_mainPsptId', "None")))
        self.textEdit.append("地址:{}".format(input_dict.get('inner_preAddressInfo', "None")))
        # self.textEdit.append("-" * 10)


        self.thread_go = ThreadGo(input_dict)
        self.thread_go.signal_go.connect(self.rollback_pushbtn_go)
        self.pushbtn_search.setEnabled(False)
        self.pushbtn_go.setEnabled(False)
        self.thread_go.start()

    # tab1 rollback
    def rollback_watch(self, return_str):
        self.te_output.append(return_str)

    def rollback_open(self, return_str):
        self.te_output.append(return_str)

    def rollback_close(self, return_str):
        self.te_output.append(return_str)

    def rollback_pushbtn_login(self, ret_str):
        """
        回调函数 系统登陆
        :param ret_str:
        :return:
        """
        self.textEdit.append(ret_str)
        self.pushbtn_login.setEnabled(True)

    def rollback_pushbtn_login_dd(self, ret_str):
        """
        回调函数 系统登陆
        :param ret_str:
        :return:
        """
        self.textEdit.append(ret_str)
        self.pushbtn_login_dd.setEnabled(True)

    # tab2 rollback
    def rollback_pushbtn_search(self, ret_dict):
        """
        回调函数
        :param ret_str:
        :return:
        """
        # self.textEdit.setText("")
        # self.textEdit.append("姓名:{}".format(ret_dict.get('inner_custName', "None")))
        # self.textEdit.append("联系电话:{}".format(ret_dict.get('inner_ContactTel', "None")))
        # self.textEdit.append("证件号码:{}".format(ret_dict.get('inner_mainPsptId', "None")))
        # self.textEdit.append("地址:{}".format(ret_dict.get('inner_preAddressInfo', "None")))
        self.le_name.setText(ret_dict.get('inner_custName', "None"))
        self.le_telnum.setText(ret_dict.get('inner_ContactTel', "None"))
        self.le_pspid.setText(ret_dict.get('inner_mainPsptId', "None"))
        self.le_address.setText(ret_dict.get('inner_preAddressInfo', "None"))

        self.pushbtn_go.setEnabled(True)
        self.pushbtn_search.setEnabled(True)
        self.textEdit.setText("查询结束")

    def rollback_pushbtn_go(self, ret_str):
        """
        回调函数
        :param ret_str:
        :return:
        """
        self.textEdit.append("录入结果:{}".format(ret_str))
        self.pushbtn_search.setEnabled(True)
        self.pushbtn_go.setEnabled(True)
        self.le_name.setEnabled(True)
        self.le_telnum.setEnabled(True)
        self.le_pspid.setEnabled(True)
        self.le_address.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
