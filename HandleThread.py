
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
                    "inner_preAddressInfo": DD.dict_order.get('装机地址', "None"),
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
            self.signal_go.emit("入参不完整")

        self.go_page()

    def get_area(self):
        if '成安' in self.address:
            return '成安县'
        elif '磁县' in self.address:
            return '磁县'
        elif '大名' in self.address:
            return '大名县'
        elif '肥乡' in self.address:
            return '肥乡县'
        elif '峰峰' in self.address:
            return '峰峰矿区'
        elif '管陶' in self.address or '馆陶' in self.address:
            return '馆陶县'
        elif '广平' in self.address:
            return '广平县'
        elif '鸡泽' in self.address:
            return '鸡泽县'
        elif '临漳' in self.address:
            return '临漳县'
        elif '邱县' in self.address:
            return '邱县'
        elif '曲周' in self.address:
            return '曲周县'
        elif '涉县' in self.address:
            return '涉县'
        elif '魏县' in self.address:
            return '魏县'
        elif '武安' in self.address:
            return '武安市'
        elif '永年' in self.address:
            return '永年县'
        elif '冀南新区' in self.address:
            return '磁县'
        elif '丛台' in self.address:
            return '丛台区'
        elif '邯山' in self.address:
            return '邯山区'
        elif '复兴' in self.address:
            return '复兴区'
        else:
            return '丛台区'

    def go_page(self):
        import time
        from selenium.webdriver.common.by import By
        W.open("https://m.10010.com/scaffold-show/push/18Nsm4M1Kjd")

        time.sleep(3)
        W.click_js((By.CSS_SELECTOR, "#deliverychoose"))
        time.sleep(1)
        W.click_js((By.XPATH, "//li[text()='河北']"))
        time.sleep(1)
        W.click_js((By.XPATH, "//li[text()='邯郸市']"))
        time.sleep(1)

        W.click_js((By.XPATH, "//li[text()='%s']" % self.get_area()))

        W.send_key((By.CSS_SELECTOR, "#address"), self.address)
        W.send_key((By.CSS_SELECTOR, "#certName"), self.custName)
        W.send_key((By.CSS_SELECTOR, "#certNo"), self.mainPsptId)
        W.send_key((By.CSS_SELECTOR, "#mobilePhone"), self.contactTel)

        W.click_js((By.CSS_SELECTOR, "#submitBtn"))
        time.sleep(3)
        err_keys = ['请输入正确的身份证号', '详细地址太短', '姓名必须至少包含2个汉字', "请填写详细地址", "您已经下过一笔单"]
        for err_key in err_keys:
            if W.is_page_contains(err_key):
                print(err_key)
                self.signal_go.emit(err_key)
                return

        ret_str = "未知，请检查是否录入成功"
        for _ in range(10):
            if W.is_page_contains("提交成功"):
                ret_str = "提交成功"
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
        print("第 {} 行开始".format(self.row_num))
        ret_int = 0
        import random
        import time

        t = random.randint(30, 60)
        time.sleep(t/10)
        self.signal_test_table.emit((self.row_num, t))

    


