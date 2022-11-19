
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from Nsop import Nsop
from Dingdan import dingdan

NSOP = Nsop()
NSOP.load_ck_token()
DD = dingdan()
DD.load_cookie()


class ThreadLogin(QThread):
    signal_login = pyqtSignal(str)

    def __init__(self):
        super(ThreadLogin, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        print("login run...")
        r = NSOP.login()
        self.signal_login.emit(str(r))


class ThreadWatch(QThread):
    signal_watch = pyqtSignal(str)

    def __init__(self):
        super(ThreadWatch, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        print("watch run...")
        r = NSOP.watch_pool()
        self.signal_watch.emit(str(r))


class ThreadOpen(QThread):
    signal_open = pyqtSignal(str)
    cbss = None
    dd = None
    second = None
    old = None

    def __init__(self):
        super(ThreadOpen, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        print("open run...")
        ret_text = ''
        if self.cbss is True:
            ret_text += NSOP.modify_order_pool(0, "open") + "\n"

        if self.dd is True:
            ret_text = NSOP.modify_order_pool(1, "open") + "\n"

        if self.second is True:
            ret_text += NSOP.modify_second_pool("open") + "\n"

        if self.old is True:
            ret_text += DD.open_pool("1700122117083558500001") + "\n"

        self.signal_open.emit(str(ret_text))


class ThreadClose(QThread):
    signal_close = pyqtSignal(str)
    cbss = None
    dd = None
    second = None
    old = None

    def __init__(self):
        super(ThreadClose, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        print("close run...")
        ret_text = ''
        if self.cbss is True:
            print(1)
            ret_text += NSOP.modify_order_pool(0, "close") + "\n"

        if self.dd is True:
            print(2)
            ret_text += NSOP.modify_order_pool(1, "close") + "\n"

        if self.second is True:
            print(3)
            ret_text += NSOP.modify_second_pool("close") + "\n"

        if self.old is True:
            ret_text += DD.close_pool("1700122117083558500001") + "\n"

        self.signal_close.emit(ret_text)


class ThreadGetDetail(QThread):
    from pandas import DataFrame
    signal_get_detail = pyqtSignal(DataFrame)

    def __init__(self):
        super(ThreadGetDetail, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        # print("get detail run...")
        # ret_df = DD.get_order_detail('223001745064308876')
        ret_df = pd.read_csv("./1.txt")
        self.signal_get_detail.emit(ret_df)


class ThreadTestTable(QThread):
    signal_test_table = pyqtSignal(tuple)

    def __init__(self, row_num):
        self.row_num = row_num
        super(ThreadTestTable, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        print("第 {} 行开始".format(self.row_num))
        ret_int = 0
        import random
        import time
        while True:
            t = random.randint(30, 60)
            time.sleep(t/10)
            self.signal_test_table.emit((self.row_num, t))

    


