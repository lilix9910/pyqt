
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from Nsop import Nsop
from Dingdan import dingdan

NSOP = Nsop()
DD = dingdan()
DD.load_cookie()
from WebUi import WebBrowser
W = WebBrowser("Firefox", True)

class ThreadLogin(QThread):
    signal_login = pyqtSignal(str)

    def __init__(self):
        super(ThreadLogin, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        r = NSOP.login()
        self.signal_login.emit(str(r))


class ThreadLoginDD(QThread):
    signal_login_dd = pyqtSignal(str)

    def __init__(self):
        super(ThreadLoginDD, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        r = DD.login()
        self.signal_login_dd.emit(str(r))


class ThreadWatch(QThread):
    signal_watch = pyqtSignal(str)

    def __init__(self):
        super(ThreadWatch, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        NSOP.load_ck_token()
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
        NSOP.load_ck_token()
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
        NSOP.load_ck_token()
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
    signal_get_detail = pyqtSignal(dict)

    def __init__(self, orderid):
        self.orderid = orderid
        super(ThreadGetDetail, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        print(self.orderid)
        if len(self.orderid) == 16:
            NSOP.load_ck_token()
            ret_dict = NSOP.get_dd_detail(self.orderid)

        elif len(self.orderid) == 18:
            try:
                DD.dict_order = dict()
            except:
                pass
            try:
                DD.dict_cust = dict()
            except:
                pass
            DD.get_order_detail(self.orderid)

            try:
                ret_dict = {
                    "inner_custName": DD.dict_cust.get('cust_name', "None"),
                    "inner_ContactTel": DD.dict_cust.get('tel_num', "None"),
                    "inner_mainPsptId": DD.dict_cust.get('cert_num', "None"),
                    "inner_preAddressInfo": DD.dict_order.get('????????????', "None"),
                }
            except:
                ret_dict = {}
        else:
            ret_dict = {}

        self.signal_get_detail.emit(ret_dict)


class ThreadGo(QThread):
    signal_go = pyqtSignal(str)

    def __init__(self, input_dict):
        self.input_dict = input_dict
        super(ThreadGo, self).__init__()
        self.setupUI()
        
    def setupUI(self):
        pass

    def run(self):
        try:
            self.custName = self.input_dict['inner_custName']
            self.contactTel = self.input_dict['inner_ContactTel']
            self.mainPsptId = self.input_dict['inner_mainPsptId']
            self.address = self.input_dict['inner_preAddressInfo']
        except:
            self.signal_go.emit("???????????????")

        self.go_page()

    def get_area(self):
        if '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '??????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '????????????'
        elif '??????' in self.address or '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '??????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '??????'
        elif '??????' in self.address:
            return '??????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '?????????'
        elif '????????????' in self.address:
            return '??????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '?????????'
        elif '??????' in self.address:
            return '?????????'
        else:
            return '?????????'

    def go_page(self):
        import time
        from selenium.webdriver.common.by import By
        W.open("https://m.10010.com/scaffold-show/push/18Nsm4M1Kjd")

        time.sleep(3)
        W.click_js((By.CSS_SELECTOR, "#deliverychoose"))
        time.sleep(1)
        W.click_js((By.XPATH, "//li[text()='??????']"))
        time.sleep(1)
        W.click_js((By.XPATH, "//li[text()='?????????']"))
        time.sleep(1)

        W.click_js((By.XPATH, "//li[text()='%s']" % self.get_area()))

        W.send_key((By.CSS_SELECTOR, "#address"), self.address)
        W.send_key((By.CSS_SELECTOR, "#certName"), self.custName)
        W.send_key((By.CSS_SELECTOR, "#certNo"), self.mainPsptId)
        W.send_key((By.CSS_SELECTOR, "#mobilePhone"), self.contactTel)

        W.click_js((By.CSS_SELECTOR, "#submitBtn"))
        time.sleep(3)
        err_keys = ['??????????????????????????????', '??????????????????', '????????????????????????2?????????', "?????????????????????", "????????????????????????"]
        for err_key in err_keys:
            if W.is_page_contains(err_key):
                print(err_key)
                self.signal_go.emit(err_key)
                return

        ret_str = "????????????????????????????????????"
        for _ in range(10):
            if W.is_page_contains("????????????"):
                ret_str = "????????????"
                break
            else:
                time.sleep(1)
        self.signal_go.emit(ret_str)

class ThreadTestTable(QThread):
    signal_test_table = pyqtSignal(tuple)

    def __init__(self, row_num):
        self.row_num = row_num
        super(ThreadTestTable, self).__init__()
        self.setupUI()

    def setupUI(self):
        pass

    def run(self):
        print("??? {} ?????????".format(self.row_num))
        ret_int = 0
        import random
        import time

        t = random.randint(30, 60)
        time.sleep(t/10)
        self.signal_test_table.emit((self.row_num, t))

    


