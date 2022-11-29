#! /usr/bin/env python3
from PyQt5.QtCore import pyqtSignal
from WebUi import WebBrowser
from BaseFunc import (
    except_err,
    print_pt,
    get_file_last_modify_leave_now,
    input_choise,
    get_captcha_by_baidu_ocr,
    setColor,
    jsonDataToCookiesParams,
)
from Config import USERNAME, PASSWORD, WAIT_TIME
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re, datetime, time, requests, json
from urllib import parse
import pandas as pd


class Nsop:
    def __init__(self):
        self.captcha = ""
        self.token = None
        self.ck_2 = None
        self.dict_cookie = dict()
        self.web = None
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://ibos.newbuy.chinaunicom.cn/ibos-eos/main.html",
            "Host": "ibos.newbuy.chinaunicom.cn",
            "Origin": "https://ibos.newbuy.chinaunicom.cn",
        }
        # df_change_info = pd.read_excel(r"./cbss_config.xlsx", sheet_name="change_info")
        # self.jsessionid = df_change_info.iloc[0][0]
        # print(self.jsessionid)

    # 登录订单系统获取
    def login(self):
        if self.web is None:
            self.web = WebBrowser("FireFox", mode=True, remote_addr="")
            # mode:True无头模式 False正常模式
            # web = WebBrowser("IE", mode=False, remote_addr="") # mode:True无头模式 False正常模式
            self.web.set_implicitly_wait(WAIT_TIME)
        else:
            print("已经启动了一个浏览器")

        while True:
            try:
                url = "https://nsop.10010.com/"
                self.web.open(url)
                self.web.send_key((By.CSS_SELECTOR, "#usenameNew"), USERNAME)
                self.web.send_key((By.CSS_SELECTOR, "#input-password-New"), PASSWORD)
                self.web.click_js((By.CSS_SELECTOR, "#provinceCodeNew"))
                self.web.click_js((By.XPATH, "//div[@value='18']"))
                while True:
                    self.web.click_js((By.CSS_SELECTOR, "#codeNew"))
                    time.sleep(1)
                    _scshot = self.web.find_element((By.CSS_SELECTOR, "#codeNew"))
                    _scshot.screenshot("./nsop.png")  # type: ignore

                    result = get_captcha_by_baidu_ocr("./nsop.png")
                    # result = input("请输入图片验证码:")

                    captcha = re.sub("[^a-zA-Z0-9]", "", result, count=0, flags=re.S)
                    if len(captcha) == 4:
                        print("captcha:", captcha)
                        self.captcha = captcha
                        break
                    # 发射信号

                self.web.send_key((By.CSS_SELECTOR, "#code_validationNew"), captcha)
                self.web.click_js((By.CSS_SELECTOR, "#btn-login-new"))
                if self.web.is_page_contains("验证码错误"):
                    print("图片验证码错误")
                    continue

                try:
                    locator = (By.XPATH, "//span[text()='已配置']")
                    self.web.click_js(locator, timeout=3)
                except Exception:
                    pass

                try:
                    locator = (By.XPATH, "//span[@aria-label='close']")
                    self.web.click_js(locator, timeout=3)
                except Exception:
                    pass

                # 订单交付（集成版）
                locator = (By.XPATH, "//span[text()='核心应用专区']")
                self.web.click(locator)
                try:
                    ActionChains(self.web.driver).move_to_element(
                        self.web.find_element(locator, timeout=5)
                    ).perform()
                    self.web.click_js(locator)
                except Exception:
                    continue

                locator = (By.XPATH, "//span[text()='订单交付（集成版）']")
                if self.web.find_element(locator):
                    self.web.click(locator, timeout=3)
                    time.sleep(5)
                    cookies = self.web.driver.get_cookies()
                    if self.get_token(self.web) is False:
                        continue
                else:
                    cookies = None
                    continue

                # locator = (By.XPATH, "//span[text()='查询订单']")
                # self.web.click(locator)
                # time.sleep(1)
                # locator = (By.XPATH, "//span[text()='订单数据查询']")
                # self.web.click(locator)
                # time.sleep(3)

                # 河北订单中心二级研发
                # locator = (By.XPATH, "//span[text()='省分二级运营']")
                # self.web.click(locator)
                # try:
                #     ActionChains(self.web.driver).move_to_element(self.web.find_element(locator)).perform()
                #     self.web.click_js(locator)
                # except Exception:
                #     pass

                # locator = (By.XPATH, "//span[text()='河北订单中心二级研发']")
                # if self.web.find_element(locator):
                #     self.web.click(locator, timeout=3)
                #     time.sleep(5)
                # else:
                #     continue

                self.ck_2 = dict()
                try:
                    url = (
                        "http://10.238.25.133:8080/order/face/orderQuery/queryOrderPage"
                    )
                    self.web.open(url)

                    ck_2 = self.web.driver.get_cookies()

                    for l in ck_2:
                        if l["name"] == "JSESSIONID":
                            self.ck_2 = {
                                "name": l["name"],
                                "value": l["value"],
                                "domain": l["domain"],
                            }
                            break

                except:
                    pass

                # print(222, self.ck_2)

                # locator = (By.XPATH, "//span[text()='审单']")
                # self.web.click(locator)
                # time.sleep(1)
                # locator = (By.XPATH, "//span[text()='订单审核']")
                # self.web.click(locator)
                # time.sleep(3)
                # locator = (By.XPATH, "//button[text()='查询']")
                # self.web.click(locator)
                # time.sleep(3)

                url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderTakingSwitch/manageInit"
                self.web.open(url)

                # url = "https://nsop.10010.com/om-portal-web/open/menu/special/systemMenu"
                # self.web.open(url)
                # time.sleep(3)

                cookies.extend(self.web.driver.get_cookies())
                print(self.ck_2)
                if self.ck_2 is not None:
                    cookies.append(self.ck_2)
                break

            except Exception as err:
                except_err(err)
                print("访问网页失败!")
                time.sleep(3)
                break

        # 保存Cookies
        jsonCookies = json.dumps(cookies)
        self.save_cookie(jsonCookies)

        # 读取Cookies
        self.load_ck_token()
        self.web.quit()
        with open("./captcha.txt", mode="a+", encoding="utf-8") as f:
            f.write(self.captcha)
        print("登录成功!")

        return True

    # 获取token
    def get_token(self, web):
        try:
            self.token = self.web.driver.execute_script(
                "return window.sessionStorage.getItem('token')"
            )
            # print("token:", self.token)
            if self.token is not None:
                # 保存token
                with open("D:/Onedrive/fcbss/token.tk", "w") as f:
                    f.write(self.token)
                return True
        except Exception:
            print("Get Token Failed!")
            return False

    # 保存cookie
    def save_cookie(self, cookie):
        with open("D:/Onedrive/fcbss/nsop_cookies.json", "w") as f:
            f.write(cookie)

    # 读取cookie和token
    def load_ck_token(self):
        with open("D:/Onedrive/fcbss/nsop_cookies.json", "r", encoding="utf-8") as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            self.dict_cookie[cookie["name"]] = cookie["value"]
        with open("D:/Onedrive/fcbss/token.tk", "r", encoding="utf-8") as f:
            self.token = f.read()

        self.headers.update({"Authorization": json.loads(self.token)["token"]})

    # 监控工单池
    def watch_pool(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://ibos.newbuy.chinaunicom.cn/",
            "Host": "ibos.newbuy.chinaunicom.cn",
            "Origin": "http://ibos.newbuy.chinaunicom.cn",
        }
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderTakingSwitch/queryGroupStaffList"
        data = "page=1&limit=10"
        resp = requests.post(
            url=url,
            data=data,
            headers=headers,
            cookies=self.dict_cookie,
        )

        try:
            if resp.status_code == 200:
                ret_text = ''
                for l in resp.json()["data"]["list"]:
                    if l["isReceived"] == "1":
                        l["isReceived"] = "开启"
                    else:
                        l["isReceived"] = "关闭"
                    ret_text += "{}状态:{}\n".format(l["groupName"], l["isReceived"])
                return ret_text
            else:
                print(resp.json())
                return "查询失败"
        except:
            return "查询出错,请检查登录状态"

    def modify_second_pool(self, mod_type):
        if mod_type == "close":
            state = 0
        elif mod_type == "open":
            state = 1

        url = "http://10.238.25.133:8080/order/face/orderDeal/doWorkPoolRelState"
        data = {
            "state": state,
        }
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }
        resp = requests.post(
            url=url,
            json=data,
            headers=headers,
            cookies=self.dict_cookie,
        )
        try:
            if resp.json()['success'] is True:
                ret_text = "{}二级工单池操作结果：成功".format(mod_type)
            else:
                ret_text = "{}二级工单池操作结果：失败".format(mod_type)
        except:
            ret_text = "{}二级工单池执行出错".format(mod_type)

        return ret_text

    # 管理工单池
    def modify_order_pool(self, group, mod_type):
        """
        group:0 邯郸市区集中预受理工号池:202104261800000012
        group:1 邯郸倒装机工号池:202104261800000010
        type:"close" 关闭工单池
        type:"open" 开启工单池

        """
        if group == 0:
            groupId = "202104261800000012"
            group_name = "预受理"
        elif group == 1:
            groupId = "202104261800000010"
            group_name = "倒装机"
        else:
            return "输入参数group有误,请核实!"

        if mod_type == "close":
            isReceived = "0"
        elif mod_type == "open":
            isReceived = "1"
        else:
            return "输入参数mod_type有误,请核实!"
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderTakingSwitch/updateGroupStaff"
        data = {
            "groupId": groupId,
            "staffId": USERNAME,
            "provinceCode": "18",
            "isReceived": isReceived,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://ibos.newbuy.chinaunicom.cn/",
            "Host": "ibos.newbuy.chinaunicom.cn",
            "Origin": "http://ibos.newbuy.chinaunicom.cn",
        }
        resp = requests.post(
            url=url,
            data=jsonDataToCookiesParams(data),
            headers=headers,
            cookies=self.dict_cookie,
        )
        return "{} {}:{}".format(mod_type, group_name, resp.text)

    # 订单数据查询
    def get_order_list(
            self,
            days=30,
            minTime="",
            maxTime="",
            extOrderId="",
            orderNo="",
            orderSourceTag=[],
            isSuspend="",
            inModeCode=[],
            tradeTypeCode=[],
            custName="",
            phoneNumber="",
            mobilePhone="",
            psptNo="",
            dealStaffId="",
            isClaim="2",
            isAutoIom="3",
            sceneType=[],
    ):

        if minTime == "":
            minTime = datetime.datetime.now() - datetime.timedelta(days=days)
            minTime = minTime.strftime("%Y-%m-%d")
            # minTime=minTime.strftime('%Y-%m-%d %H:%M:%S')

        if maxTime == "":
            maxTime = datetime.datetime.now() - datetime.timedelta(days=days - 30)
            maxTime = maxTime.strftime("%Y-%m-%d")
            # maxTime=maxTime.strftime('%Y-%m-%d %H:%M:%S')

        untreatedTime = datetime.datetime.now().strftime("%Y-%m-%d")

        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-service/OrderDataQuery/query/new"
        data = {
            "businessType": "",
            "cancelTag": [],
            "cityCode": ["186"],
            "custIp": "",
            "custName": custName,
            # custName:客户名称
            "dateType": "",
            "dealStaffId": dealStaffId,
            # dealStaffId:操作员工号
            "deliverMaxTime": "",
            "deliverMinTime": "",
            "dispatchAutoTag": "4",
            "distributeOrderFlag": "2",
            "districtCode": "",
            "extOrderId": extOrderId,
            # extOrderId:触点单号
            "goodsName": "",
            "iccid": "",
            "imei": "",
            "inModeCode": inModeCode,
            # inModeCode:触点来源 列表list
            "isAutoIom": isAutoIom,
            # isAutoIom:IOM转派方式
            # "0":非自动
            # "1":自动
            # "2":非预判自动
            # "3":全部
            "isClaim": isClaim,
            # isClaim:是否分配
            # "0":否
            # "1":是
            # "2":全部
            "isReverse": "ALL",
            "isSuspend": isSuspend,
            # isSuspend:订单挂起状态
            # "1":是
            # "0":否
            "lgtsOrder": "",
            "mashanggouBackState": [],
            "mashanggouTag": [],
            "maxTime": maxTime,
            # maxTime:时间段结束 2021-07-29 不能跨越30天
            "minTime": minTime,
            # minTime:时间段开始 2021-07-22
            "mobilePhone": mobilePhone,
            # mobilePhone:联系电话
            "netTypeCode": [],
            "orderKind": "",
            "orderNo": orderNo,
            # orderNo:订单编号
            "orderSourceTag": orderSourceTag,
            # orderSourceTag: 列表list
            # "0":沃掌通标准应用
            # "1":沃掌通省分专区
            # "2":2i订单
            # "3":中台线上订单
            # "4":码上购
            "orderStaffId": "",
            "orderStaffRole": "",
            "orderState": [],
            "pageNum": 1,
            "pageSize": 99,
            "payId": "",
            "payState": [],
            "payType": [],
            "phoneNumber": phoneNumber,
            # phoneNumber:业务号码
            "postTypeList": [],
            "provinceCode": "18",
            "psptNo": psptNo,
            # psptNo:证件号码
            "sceneType": sceneType,
            # 场景类型 list
            # 400073:一家亲跨省异地宽带意向单
            "tradeTypeCode": tradeTypeCode,
            # tradeTypeCode:业务类型 list
            "untreatedTime": untreatedTime,
            # untreatedTime:选择时间
            "userTag": [],
        }

        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )
        # print(resp.json())
        try:
            num = resp.json()["data"]["total"]
        except Exception:
            print(resp.json())
            return None

        print("%s ---- 本次查询到 %d 条工单" % (str(datetime.datetime.now())[:19], num))
        if num > 0:
            return_list = []
            order_list = resp.json()["data"]["orderList"]
            for order in order_list:
                # print(order['list'])
                # createTime = order['list']['createTime']
                # extOrderId = order['list']['extOrderId']
                # orderId = order['list']['orderId']
                # mobilePhone = order['list']['mobilePhone']
                # orderSource	= order['list']['orderSource']
                # inModeCode = order['list']['inModeCode']
                # orderKind = order['list']['orderKind']
                # sceneType = order['list']['sceneType']
                # dealStaffName = order['list']['dealStaffName']

                extOrderId = order["list"]["extOrderId"]
                createTime = order["list"]["createTime"]
                phoneNumber = order["list"]["phoneNumber"]
                mobilePhone = order["list"]["mobilePhone"]
                custName = order["list"]["custName"]
                addressDetail = order["list"]["addressDetail"]
                orderNodeName = order["list"]["orderNodeName"]
                orderNodeStateName = order["list"]["orderNodeStateName"]
                dealStaffName = order["list"]["dealStaffName"]
                orderSource = order["list"]["orderSource"]
                tradeType = order["list"]["tradeType"]
                orderNo = order["list"]["orderNo"]
                inModeCode = order["list"]["inModeCode"]
                orderNodeStateName = order["list"]["orderNodeStateName"]
                orderNodeName = order["list"]["orderNodeName"]
                referrerName = order["list"]["referrerName"]
                return_list.append(
                    (
                        referrerName,
                        extOrderId,
                        createTime,
                        phoneNumber,
                        mobilePhone,
                        custName,
                        addressDetail,
                        orderNodeName,
                        orderNodeStateName,
                        dealStaffName,
                        orderSource,
                        tradeType,
                        orderNo,
                        inModeCode,
                        orderNodeStateName,
                        orderNodeName,
                    )
                )
            return return_list
        else:
            return None

    # 订单生产
    def orderaccount(self):
        # url = "https://2i.10010.com:10000/order-account/ryy/accountInit"
        url = (
            "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-account/ryy/accountInit"
        )
        data = {
            # "startDate": "2022-01-22 00:00:00",
            # "endDate": "2022-04-22 23:59:59",
            "pageNum": 1,
            "pageSize": 99,
            "orderSourceTag": ["0", "1", "2", "3", "4"],
            "isSuspend": "0",
            "inModeCode": [
                "1011",
                "1013",
                "1014",
                "1018",
                "1019",
                "1022",
                "1024",
                "1025",
                "1026",
                "1029",
                "1030",
                "1032",
                "1041",
                "1045",
                "1048",
                "1050",
                "1051",
                "1053",
                "1054",
                "1056",
                "2002",
                "2001",
                "2002",
                "2003",
                "2004",
                "2005",
                "2006",
                "2008",
                "2009",
                "2010",
                "2011",
                "2015",
                "2115",
                "9004",
                "9005",
                "9007",
                "9008",
                "9010",
                "9011",
                "9012",
                "9013",
                "9014",
                "9016",
                "9017",
                "9018",
                "9019",
                "9021",
                "9022",
                "9023",
                "9024",
                "9026",
                "9050",
                "9051",
                "9052",
                "9053",
                "9056",
                "9057",
                "9058",
                "9059",
                "1118",
                "5018",
                "5118",
                "5218",
                "5318",
                "5418",
                "5518",
                "5618",
                "5718",
                "5818",
                "5918",
                "6018",
                "6118",
                "6218",
                "6318",
                "6418",
                "6518",
                "6618",
                "6718",
                "6818",
                "6918",
                "7018",
                "7118",
                "7218",
                "7318",
                "7418",
                "7518",
                "7618",
                "7718",
                "7818",
                "7918",
                "8018",
                "8118",
                "8218",
                "8318",
                "8418",
                "8518",
                "8618",
                "8718",
                "8818",
                "8918",
                "1015",
                "9001",
                "9002",
                "9003",
                "9006",
                "9015",
                "9020",
                "9025",
                "9065",
                "9061",
            ],
            "orderByTime": "0",
            "orderStaffId": "",
            "orderStaffRole": "",
            "isReverse": "ALL",
            "dispatchAutoTag": "4",
            "distributeOrderFlag": "2",
            "noBroadType": "1",
        }
        # data = '{"pageNum":1,"pageSize":10,"orderSourceTag":["0","1","2","3","4"],"isSuspend":"0","inModeCode":["1011","1013","1014","1018","1019","1022","1024","1025","1026","1029","1030","1032","1041","1045","1050","1051","1053","1054","1056","2002","2001","2002","2003","2004","2005","2006","2008","2009","2010","2011","2015","2115","9004","9005","9007","9008","9010","9011","9012","9013","9014","9016","9017","9018","9019","9021","9022","9023","9024","9026","9050","9051","9052","9053","9056","9057","9058","9059","1118","5018","5118","5218","5318","5418","5518","5618","5718","5818","5918","6018","6118","6218","6318","6418","6518","6618","6718","6818","6918","7018","7118","7218","7318","7418","7518","7618","7718","7818","7918","8018","8118","8218","8318","8418","8518","8618","8718","8818","8918","1015","9001","9002","9003","9006","9015","9020","9025","9065","9061","1048"],"startDate":"2022-01-22 00:00:00","endDate":"2022-04-22 23:59:59","orderByTime":"0","orderStaffId":"","orderStaffRole":"","isReverse":"ALL","dispatchAutoTag":"4","distributeOrderFlag":"2","noBroadType":"1"}'
        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )
        # print(resp.text)
        num = resp.json()["orderList"]["total"]
        # print("订单生产", "-->", num)
        return num

        if num > 0:
            order_list = resp.json()["orderList"]["list"]
            for order in order_list:
                orderTime = order["orderTime"]
                extOrderId = order["extOrderId"]
                orderId = order["orderId"]
                contactPhone = order["contactPhone"]
                orderSource = order["orderSource"]
                inModeCode = order["inModeCode"]
                orderKind = order["orderKind"]
                sceneType = order["sceneType"]
                dealStaffName = order["dealStaffName"]
                print(
                    orderTime,
                    ",",
                    extOrderId,
                    ",",
                    orderId,
                    ",",
                    contactPhone,
                    ",",
                    orderSource,
                    ",",
                    inModeCode,
                    ",",
                    orderKind,
                    ",",
                    sceneType,
                    ",",
                    dealStaffName,
                )

    # 查询退单清单
    def get_return_order_list(self, startDate, endDate):
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-cancel/v2/cancel/page/query"
        data = {
            "chipState": "",
            "cityCode": "",
            "custName": "",
            "custPhone": "",
            "dateType": "1",
            "endDate": endDate,  # 2022-06-13 23:59:59
            "extOrderId": "",
            "inModeCode": [
                "1011",
                "1013",
                "1014",
                "1018",
                "1019",
                "1022",
                "1024",
                "1025",
                "1026",
                "1029",
                "1030",
                "1032",
                "1041",
                "1045",
                "1050",
                "1051",
                "1053",
                "1054",
                "1056",
                "2002",
                "2001",
                "2002",
                "2003",
                "2004",
                "2005",
                "2006",
                "2008",
                "2009",
                "2010",
                "2011",
                "2015",
                "2115",
                "9004",
                "9005",
                "9007",
                "9008",
                "9010",
                "9011",
                "9012",
                "9013",
                "9014",
                "9016",
                "9017",
                "9018",
                "9019",
                "9021",
                "9022",
                "9023",
                "9024",
                "9026",
                "9050",
                "9051",
                "9052",
                "9053",
                "9057",
                "9058",
                "9059",
                "1118",
                "5018",
                "5118",
                "5218",
                "5318",
                "5418",
                "5518",
                "5618",
                "5718",
                "5818",
                "5918",
                "6018",
                "6118",
                "6218",
                "6318",
                "6418",
                "6518",
                "6618",
                "6718",
                "6818",
                "6918",
                "7018",
                "7118",
                "7218",
                "7318",
                "7418",
                "7518",
                "7618",
                "7718",
                "7818",
                "7918",
                "8018",
                "8118",
                "8218",
                "8318",
                "8418",
                "8518",
                "8618",
                "8718",
                "8818",
                "8918",
                "9001",
                "9002",
                "9003",
                "9006",
                "9015",
                "9020",
                "9025",
                "9065",
                "9061",
                "1048",
                "1057",
                "1021",
                "9068",
                "9056",
                "1015",
            ],
            "mashanggou": "",
            "orderNo": "",
            "orderSourceTag": ["2", "4"],
            "pageNum": 1,
            "pageSize": 999,
            "psptId": "",
            "sceneType": [],
            "serialNumber": "",
            "startDate": startDate,  # 2022-06-01 00:00:00
            "startOrderTime": "",
            "timeSort": "asc",
        }

        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )
        try:
            print("本次查询工单数量:", resp.json()["rsp"]["data"]["total"], end="\t")
        except:
            try:
                print("查询失败:", resp.json()["rsp"]["respDesc"])
            except:
                print("查询失败!")
            return

        input("回车开始处理退单")

        i = 1
        for list in resp.json()["rsp"]["data"]["list"]:
            try:
                orderId = list["orderId"]
                if len(orderId) == 0:
                    print(list, orderId)

                print("")
                print("第 %i 条订单,编号:%s" % (i, orderId))
                i = i + 1

                phoneNumber = self.get_return_phonen_number(orderId)
                if len(phoneNumber) == 11:
                    result = self.return_order(orderId, phoneNumber)
                    print("---- 处理结果:", result)
                    if "选占号码证件号码和证件类型与选占记录不相同" in result or "无权释放号码" in result:
                        self.return_order_one_two_sell(orderId, phoneNumber)
                else:
                    print("未找到关联手机号码:", orderId)
            except:
                pass

    # 退单一号双卖
    def return_order_one_two_sell(self, orderId, phoneNumber):
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-cancel/v2/api/order/cancel/one/two/sell"
        data = {
            "orderId": orderId,
            "phoneNumber": phoneNumber,
            "remark": "申请退单",
            "type": "1",
        }
        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )
        print("---- ---- 一号双卖处理结果:", resp.text)

    # 获取退单详情号码
    def get_return_phonen_number(self, orderid):
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-cancel/v2/cancel/number/query"
        data = {"cartType": "2", "orderId": str(orderid)}
        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )

        try:
            mainphoneNumber = resp.json()["rsp"]["data"]["mainCardInfo"]["phoneNumber"]
            return mainphoneNumber

        except:
            mainphoneNumber = ""

        try:
            vicephoneNumber = resp.json()["rsp"]["data"]["viceCardInfoList"][0][
                "phoneNumber"
            ]
            return vicephoneNumber
        except:
            vicephoneNumber = ""

        return ""

    # 退单
    def return_order(self, order_id, phoneNumber):
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-cancel/v2/api/order/cancel/order/cancel"
        data = {"orderId": order_id, "phoneNumber": phoneNumber, "remark": "同意退单"}
        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )
        return resp.text

    # 执行退单
    def run_return_order(self):
        startDate = input("请输入查询开始日期(格式:20210601,直接回车为前55天0时):")
        try:
            time.strptime(startDate, "%Y%m%d")
            startDate = (
                    startDate[:4]
                    + "-"
                    + startDate[4:6]
                    + "-"
                    + startDate[6:8]
                    + " 00:00:00"
            )

        except Exception:
            startDate = datetime.datetime.now() - datetime.timedelta(days=55)
            startDate = startDate.strftime("%Y-%m-%d 00:00:00")
        print("开始日期:", startDate)

        endDate = input("请输入查询结束日期(格式:20210618,直接回车为前25天24时):")
        try:
            time.strptime(endDate, "%Y%m%d")
            endDate = (
                    endDate[:4] + "-" + endDate[4:6] + "-" + endDate[6:8] + " 23:59:59"
            )
        except Exception:
            endDate = datetime.datetime.now() - datetime.timedelta(days=25)
            endDate = endDate.strftime("%Y-%m-%d 23:59:59")
        print("结束时间:", endDate)
        nsop.get_return_order_list(startDate=startDate, endDate=endDate)

    # 订单调度（中台线上订/2I）
    def orderManualDispatcher(
            self,
            groupBin,
            orderSourceTag_list,
            cityCode_list=[],
            districtCodePost="",
            provinceCode="",
    ):
        """
        orderSourceTag  中台线上订单:3
                        2i订单:2
                        码上购订单：4
        """

        startDate = datetime.datetime.now() - datetime.timedelta(days=89)
        startDate = startDate.strftime("%Y-%m-%d 00:00:00")

        endDate = datetime.datetime.now() - datetime.timedelta(days=0)
        endDate = endDate.strftime("%Y-%m-%d 23:59:59")

        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/codebuy-dispatch/orderManualDispatcher/ryy/query"
        data = {
            "cityCode": cityCode_list,  # "186_130400"
            "districtCodePost": districtCodePost,  # "130402,130403,130404"
            "groupBin": groupBin,
            "inModeCode": [
                "1011",
                "1013",
                "1014",
                "1018",
                "1019",
                "1022",
                "1024",
                "1025",
                "1026",
                "1029",
                "1030",
                "1032",
                "1041",
                "1045",
                "1050",
                "1051",
                "1053",
                "1054",
                "1056",
                "2002",
                "2001",
                "2002",
                "2003",
                "2004",
                "2005",
                "2006",
                "2008",
                "2009",
                "2010",
                "2011",
                "2015",
                "2115",
                "9004",
                "9005",
                "9007",
                "9008",
                "9010",
                "9011",
                "9012",
                "9013",
                "9014",
                "9016",
                "9017",
                "9018",
                "9019",
                "9021",
                "9022",
                "9023",
                "9024",
                "9026",
                "9050",
                "9051",
                "9052",
                "9053",
                "9057",
                "9058",
                "9059",
                "1118",
                "5018",
                "5118",
                "5218",
                "5318",
                "5418",
                "5518",
                "5618",
                "5718",
                "5818",
                "5918",
                "6018",
                "6118",
                "6218",
                "6318",
                "6418",
                "6518",
                "6618",
                "6718",
                "6818",
                "6918",
                "7018",
                "7118",
                "7218",
                "7318",
                "7418",
                "7518",
                "7618",
                "7718",
                "7818",
                "7918",
                "8018",
                "8118",
                "8218",
                "8318",
                "8418",
                "8518",
                "8618",
                "8718",
                "8818",
                "8918",
                "9001",
                "9002",
                "9003",
                "9006",
                "9015",
                "9020",
                "9025",
                "9065",
                "9061",
                "1048",
                "1057",
                "1021",
                "9068",
                "9056",
                "1015",
            ],
            "netTypeCode": [],
            "orderByType": "",
            "orderCreatTimeEnd": endDate,  # "2022-07-18 23:59:59",
            "orderCreatTimeStart": startDate,  # "2022-04-20 00:00:00",
            "orderSourceTag": orderSourceTag_list,
            "orderUpdateTimeEnd": "",
            "orderUpdateTimeStart": "",
            "pageNum": 1,
            "pageSize": 199,
            "provinceCode": provinceCode,  # 18_130000
            "sceneType": [],
        }

        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )
        return resp.json()["manualDispatcherOrderPages"]["total"]

    # 查询 订单生产（新宽融）
    def toQueryOrderManageList(self, orderState):
        startDate = datetime.datetime.now() - datetime.timedelta(days=30)
        startDate = startDate.strftime("%Y-%m-%d 00:00:00")

        endDate = datetime.datetime.now() - datetime.timedelta(days=0)
        endDate = endDate.strftime("%Y-%m-%d 23:59:59")

        # print(startDate, endDate)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://ibos.newbuy.chinaunicom.cn/ibos-eos/main.html",
            "Host": "ibos.newbuy.chinaunicom.cn",
            "Origin": "https://ibos.newbuy.chinaunicom.cn",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        if len(orderState) == 0:
            url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderManage/queryOrderDealNum"
            data = "provinceCode=18&eparchyCode=186"
            resp = requests.post(
                url=url, data=data, headers=headers, cookies=self.dict_cookie
            )
            return (resp.json()["ORDER"]["FAST_NUM"], resp.json()["ORDER"]["SLOW_NUM"])

        else:
            headers.pop("Content-Type")
            url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderManage/toQueryOrderManageList"
            data = {
                "boardIntegrate": "1",
                "certId": "",
                "custName": "",
                "custPhone": "",
                "endDate": endDate,  # "2022-07-18 23:59:59",
                "eparchyCode": "186",
                "extOrderId": "",
                "inModeCode": "",
                "isMainOrderQry": "Y",
                "netTypeCode": "",
                "orderId": "",
                "orderKind": "",
                "orderSourceTag": "3",
                "orderState": orderState,
                "page": 1,
                "pageSize": 99,
                "provinceCode": "18",
                "sceneType": "",
                "serialNumber": "",
                "startDate": startDate,  # "2022-07-11 00:00:00",
                "timeSort": "desc",
                "tradeTypeCode": "",
            }
            resp = requests.post(
                url=url, json=data, headers=headers, cookies=self.dict_cookie
            )
            # print(resp.text)
            # print("新宽融生产(", orderStateName, ") --> ", resp.json()["SUM_NUMBER"])

            count = 0
            for order in resp.json()["ORDER"]:
                # print(order['ORDER_SHOW_SORT'])
                if order["ORDER_SHOW_SORT"] != "80":
                    count = str(int(count) + 1)
            return count

    # 订单审核-超时25天退单
    def return_order_over_25(self, groupBin, isSuspend):
        startDate = datetime.datetime.now() - datetime.timedelta(days=90)
        startDate = startDate.strftime("%Y-%m-%d 00:00:00")

        endDate = datetime.datetime.now() - datetime.timedelta(days=0)
        endDate = endDate.strftime("%Y-%m-%d 23:59:59")

        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialVerify/batchQueryMyOrders"
        data = {
            "ageChoose": "",
            "businessType": "",
            "certificateModify": "",
            "channel": "",
            "checkPass": "",
            "chunicomFlag": "",
            "confTimeTab": "0",
            "crossCity": [],
            "deliveryAddrModify": "",
            "districtNamePost": [],
            "endTime": endDate,  # "2022-08-09 23:59:59",
            "exCode": "",
            "frontEssProvinceCode": "",
            "groupBin": groupBin,
            "inModeCode": [
                "1011",
                "1013",
                "1014",
                "1018",
                "1019",
                "1022",
                "1024",
                "1025",
                "1026",
                "1029",
                "1030",
                "1032",
                "1041",
                "1045",
                "1050",
                "1051",
                "1053",
                "1054",
                "1056",
                "2002",
                "2001",
                "2002",
                "2003",
                "2004",
                "2005",
                "2006",
                "2008",
                "2009",
                "2010",
                "2011",
                "2015",
                "2115",
                "9004",
                "9005",
                "9007",
                "9008",
                "9010",
                "9011",
                "9012",
                "9013",
                "9014",
                "9016",
                "9017",
                "9018",
                "9019",
                "9021",
                "9022",
                "9023",
                "9024",
                "9026",
                "9050",
                "9051",
                "9052",
                "9053",
                "9057",
                "9058",
                "9059",
                "1118",
                "5018",
                "5118",
                "5218",
                "5318",
                "5418",
                "5518",
                "5618",
                "5718",
                "5818",
                "5918",
                "6018",
                "6118",
                "6218",
                "6318",
                "6418",
                "6518",
                "6618",
                "6718",
                "6818",
                "6918",
                "7018",
                "7118",
                "7218",
                "7318",
                "7418",
                "7518",
                "7618",
                "7718",
                "7818",
                "7918",
                "8018",
                "8118",
                "8218",
                "8318",
                "8418",
                "8518",
                "8618",
                "8718",
                "8818",
                "8918",
                "9001",
                "9002",
                "9003",
                "9006",
                "9015",
                "9020",
                "9025",
                "9065",
                "9061",
                "1048",
                "1057",
                "1021",
                "9068",
                "9056",
                "1015",
                "9076",
                "7476",
                "9075",
                "9074",
                "9073",
                "1060",
                "7676",
                "9077",
            ],
            "isSuspend": isSuspend,
            "kingGroundFlag": "",
            "mashanggou": "",
            "mashanggouBackState": [],
            "noBroadType": "1",
            "orderSourceTag": ["2", "4"],
            "pageNum": 1,
            "pageSize": 199,
            "phoneModify": "",
            "sceneType": [],
            "specialBusinessParentCode": "",
            "startTime": startDate,  # "2022-05-11 00:00:00",
            "verifyExcode": "",
        }

        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )

        # print(resp.json())
        print("查询到", resp.json()["pageInfo"]["total"], "条待审核订单")
        for list in resp.json()["pageInfo"]["orderList"]:
            orderId = list["orderId"]
            phoneNumber = list["phoneNumber"]
            delayTime = list["delayTime"]
            try:
                postBlackFlag = list["blackMap"]["postBlackFlag"]
            except:
                postBlackFlag = False

            try:
                exRemark = list["exRemark"]
            except Exception:
                exRemark = ""

            order_remarks = list["remarks"]

            print("---- 开始处理:", orderId, phoneNumber, delayTime, exRemark)
            remark = ""
            specRemark = ""

            if int(delayTime[: delayTime.find("天")]) >= 25:
                print("******", "超时订单", "******")
                remark = "超期订单"
                specRemark = "其他原因"
                exReasonCode = "0502"

                # 解挂
                url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                data = {
                    "operatorType": "0005",
                    "orderId": orderId,
                    "reasonCode": "",
                    "reasonDesc": "",
                    "remarks": "",
                }
                resp = requests.post(
                    url=url, json=data, headers=self.headers, cookies=self.dict_cookie
                )
                print("---- ---- 解挂结果:", resp.json())
                time.sleep(1)

                # 退单
                url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-cancel/v2/api/order/cancel/apply"
                data = {
                    "backOrderSource": "KX",
                    "exReasonCode": exReasonCode,
                    "exType": "02",
                    "orderId": orderId,
                    "phoneNumber": phoneNumber,
                    "remark": remark,
                    "specRemark": specRemark,
                    "type": "1",
                }
                resp = requests.post(
                    url=url, json=data, headers=self.headers, cookies=self.dict_cookie
                )
                print("---- ---- 退单结果:", resp.json())
                time.sleep(1)

            elif postBlackFlag is True and groupBin in ["1", "0"]:
                print("******", "黑名单", "******")
                # 挂起
                url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                data = {
                    "operatorType": "0004",
                    "orderId": orderId,
                    "reasonCode": "03",
                    "reasonDesc": "其他",
                    "remarks": "收件地址黑名单",
                }
                resp = requests.post(
                    url=url, json=data, headers=self.headers, cookies=self.dict_cookie
                )
                print("---- ---- 挂起结果:", resp.json())

            elif "用户要求退单" in exRemark:
                print("******", "用户要求退单", "******")
                remark = exRemark

                # 挂起
                url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                data = {
                    "operatorType": "0004",
                    "orderId": orderId,
                    "reasonCode": "03",
                    "reasonDesc": "其他",
                    "remarks": exRemark,
                }
                resp = requests.post(
                    url=url, json=data, headers=self.headers, cookies=self.dict_cookie
                )
                print("---- ---- 挂起结果:", resp.json())

            elif "客户资料校验一证五户未通过" in exRemark and groupBin in ["1", "0"]:
                print("******", "客户资料校验一证五户未通过", "******")

                # 挂起
                url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                data = {
                    "operatorType": "0004",
                    "orderId": orderId,
                    "reasonCode": "03",
                    "reasonDesc": "其他",
                    "remarks": exRemark,
                }
                resp = requests.post(
                    url=url, json=data, headers=self.headers, cookies=self.dict_cookie
                )
                print("---- ---- 挂起结果:", resp.json())

            elif len(order_remarks) > 0:
                for i in range(len(order_remarks) - 1, -1, -1):
                    if "【上门】用户拒收" in order_remarks[i]["remarks"]:
                        print("******", order_remarks[i]["remarks"], "******")
                        remark = order_remarks[i]["remarks"]
                        specRemark = "客户拒收"

                        # 挂起
                        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                        data = {
                            "operatorType": "0004",
                            "orderId": orderId,
                            "reasonCode": "03",
                            "reasonDesc": "其他",
                            "remarks": remark,
                        }
                        resp = requests.post(
                            url=url,
                            json=data,
                            headers=self.headers,
                            cookies=self.dict_cookie,
                        )
                        print("---- ---- 挂起结果:", resp.json())
                        break

                    elif "【重新审单】用户要求退单" in order_remarks[i]["remarks"]:
                        print("******", order_remarks[i]["remarks"], "******")
                        remark = order_remarks[i]["remarks"]
                        specRemark = "客户申请退单"
                        exReasonCode = "0402"

                        # 挂起
                        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                        data = {
                            "operatorType": "0004",
                            "orderId": orderId,
                            "reasonCode": "03",
                            "reasonDesc": "其他",
                            "remarks": remark,
                        }
                        resp = requests.post(
                            url=url,
                            json=data,
                            headers=self.headers,
                            cookies=self.dict_cookie,
                        )
                        print("---- ---- 挂起结果:", resp.json())
                        break

                    elif "【上门】其他-没订购" in order_remarks[i]["remarks"]:
                        print("******", order_remarks[i]["remarks"], "******")
                        remark = order_remarks[i]["remarks"]
                        specRemark = "客户申请退单"
                        exReasonCode = "0402"

                        # 挂起
                        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                        data = {
                            "operatorType": "0004",
                            "orderId": orderId,
                            "reasonCode": "03",
                            "reasonDesc": "其他",
                            "remarks": remark,
                        }
                        resp = requests.post(
                            url=url,
                            json=data,
                            headers=self.headers,
                            cookies=self.dict_cookie,
                        )
                        print("---- ---- 挂起结果:", resp.json())
                        break

                    elif "【其他】本人未购买" in order_remarks[i]["remarks"]:
                        print("******", order_remarks[i]["remarks"], "******")
                        remark = order_remarks[i]["remarks"]
                        specRemark = "客户申请退单"
                        exReasonCode = "0402"

                        # 挂起
                        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                        data = {
                            "operatorType": "0004",
                            "orderId": orderId,
                            "reasonCode": "03",
                            "reasonDesc": "其他",
                            "remarks": remark,
                        }
                        resp = requests.post(
                            url=url,
                            json=data,
                            headers=self.headers,
                            cookies=self.dict_cookie,
                        )
                        print("---- ---- 挂起结果:", resp.json())
                        break
                    elif "用户不要了" in order_remarks[i]["remarks"]:
                        print("******", order_remarks[i]["remarks"], "******")
                        remark = order_remarks[i]["remarks"]
                        specRemark = "客户申请退单"
                        exReasonCode = "0402"

                        # 挂起
                        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                        data = {
                            "operatorType": "0004",
                            "orderId": orderId,
                            "reasonCode": "03",
                            "reasonDesc": "其他",
                            "remarks": remark,
                        }
                        resp = requests.post(
                            url=url,
                            json=data,
                            headers=self.headers,
                            cookies=self.dict_cookie,
                        )
                        print("---- ---- 挂起结果:", resp.json())
                        break

            if list["mashanggouBackCount"] == 3 and len(remark) == 0:
                print("******", "剩余可转码上购次数0次，不可转码上购", "******")
                exRemark = "剩余可转码上购次数0次，不可转码上购"

                # 挂起
                url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-verify/RyyArtificialModify/orderSuspendOrRegain"
                data = {
                    "operatorType": "0004",
                    "orderId": orderId,
                    "reasonCode": "03",
                    "reasonDesc": "其他",
                    "remarks": exRemark,
                }
                resp = requests.post(
                    url=url, json=data, headers=self.headers, cookies=self.dict_cookie
                )
                print("---- ---- 挂起结果:", resp.json())

    # 订单领取查询
    def queryClaimOrderNum(
            self, crossCity_list, postCityCode, postDistrictCode_list, postProvinceCode
    ):
        startDate = datetime.datetime.now() - datetime.timedelta(days=90)
        startDate = startDate.strftime("%Y-%m-%d")

        endDate = datetime.datetime.now() - datetime.timedelta(days=0)
        endDate = endDate.strftime("%Y-%m-%d")
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/allocation-claim/AllocationReceive/queryClaimOrderNum"
        data = {
            "beginTime": startDate,  # "2022-05-11",
            "businessType": [
                "73",
                "70",
                "98",
                "69",
                "S06",
                "330",
                "333",
                "328",
                "332",
                "66",
                "260",
                "321",
                "248",
                "406",
                "CB01",
                "CB11",
                "BC11",
                "CB03",
                "CB02",
                "S32",
                "S10",
                "96",
                "129",
                "S24",
                "111",
                "1000",
                "S04",
                "236",
                "430",
                "415",
                "305",
                "304",
                "64",
                "278",
                "215",
                "276",
                "216",
                "91",
                "271",
                "329",
                "228",
                "160",
                "119",
                "279",
                "244",
                "110",
                "175",
                "169",
                "218",
                "221",
                "E01",
                "209",
                "10",
                "38",
                "83",
                "137",
                "34",
                "55",
                "212",
                "287",
                "243",
                "19",
                "239",
                "45",
                "121",
                "BHK",
                "156",
                "87",
                "205",
                "207",
                "303",
                "307",
                "319",
                "380",
                "379",
                "376",
                "234",
                "423",
                "246",
                "109",
                "17",
                "187",
                "194",
                "M194",
                "222",
                "CY01",
                "192",
                "CI01",
                "150",
                "B05",
                "B06",
                "B11",
                "364",
                "102",
                "50",
                "242",
                "277",
                "128",
                "B02",
                "35",
                "231",
                "401",
                "403",
                "M270",
                "315",
                "301",
                "M232",
                "M231",
                "269",
                "258",
                "S08",
                "223",
                "15",
                "92",
                "81",
                "09",
                "325",
                "104",
                "320",
                "S20",
                "DHG",
                "BCP",
                "139",
                "186",
                "79",
                "12",
                "67",
                "280",
                "153",
                "B15",
                "B13",
                "B14",
                "B18",
                "B16",
                "B17",
                "265",
                "225",
                "197",
                "21",
                "E02",
                "48",
                "22",
                "183",
                "155",
                "S14",
                "36",
                "P02",
                "P01",
                "S22",
                "256",
                "G01",
                "419",
                "421",
                "422",
                "G02",
                "127",
                "123",
                "126",
                "S05",
                "90",
                "JY02",
                "37",
                "383",
                "118",
                "29",
                "217",
                "238",
                "117",
                "41",
                "282",
                "146",
                "S23",
                "S27",
                "J99",
                "229",
                "230",
                "CB12",
                "308",
                "261",
                "S13",
                "182",
                "71",
                "S16",
                "B03",
                "11",
                "112",
                "S21",
                "94",
                "93",
                "164",
                "02",
                "106",
                "49",
                "RH01",
                "382",
                "174",
                "196",
                "B01",
                "249",
                "95",
                "259",
                "378",
                "427",
                "405",
                "S28",
                "345",
                "377",
                "373",
                "372",
                "429",
                "357",
                "355",
                "358",
                "409",
                "344",
                "371",
                "356",
                "360",
                "361",
                "374",
                "359",
                "384",
                "290",
                "53",
                "318",
                "310",
                "414",
                "413",
                "418",
                "386",
                "368",
                "408",
                "369",
                "370",
                "367",
                "428",
                "296",
                "363",
                "398",
                "366",
                "411",
                "412",
                "394",
                "393",
                "397",
                "390",
                "391",
                "392",
                "410",
                "385",
                "395",
                "396",
                "389",
                "387",
                "388",
                "362",
                "306",
                "407",
                "311",
                "327",
                "417",
                "416",
                "291",
                "402",
                "381",
                "240",
                "425",
                "426",
                "424",
                "52",
                "S09",
                "176",
                "07",
                "115",
                "226",
                "39",
                "298",
                "27",
                "97",
                "65",
                "268",
                "132",
                "135",
                "25",
                "275",
                "227",
                "201",
                "B04",
                "61",
                "72",
                "167",
                "16",
                "151",
                "154",
                "58",
                "W01",
                "W02",
                "32",
                "84",
                "01",
                "BCD",
                "247",
                "233",
                "323",
                "322",
                "324",
                "74",
                "171",
                "295",
                "206",
                "173",
                "Q01",
                "181",
                "299",
                "172",
                "S19",
                "232",
                "ZD02",
                "148",
                "S03",
                "S18",
                "NSD",
                "F06",
                "F02",
                "F04",
                "F07",
                "F03",
                "F13",
                "F01",
                "F10",
                "F09",
                "F08",
                "F05",
                "F11",
                "F12",
                "420",
                "CI01",
                "CI02",
                "CB04",
                "CB06",
                "CB05",
                "S17",
                "193",
                "170",
                "ZD03",
                "86",
                "185",
                "255",
                "75",
                "S26",
                "297",
                "78",
                "77",
                "103",
                "263",
                "270",
                "289",
                "317",
                "316",
                "F15",
                "177",
                "08",
                "114",
                "144",
                "365",
                "334",
                "346",
                "354",
                "335",
                "353",
                "336",
                "352",
                "337",
                "350",
                "338",
                "351",
                "339",
                "348",
                "340",
                "349",
                "342",
                "341",
                "347",
                "326",
                "147",
                "245",
                "219",
                "264",
                "210",
                "FT08",
                "89",
                "266",
                "288",
                "03",
                "76",
                "105",
                "180",
                "122",
                "267",
                "257",
                "300",
                "400",
                "262",
                "399",
                "312",
                "313",
                "168",
                "TY01",
                "31",
                "24",
                "179",
                "S07",
                "62",
                "M201",
                "178",
                "S30",
                "165",
                "250",
                "60",
                "140",
                "220",
                "33",
                "14",
                "272",
                "125",
                "136",
                "251",
                "157",
                "40",
                "42",
                "158",
                "162",
                "211",
                "214",
                "59",
                "343",
                "213",
                "375",
                "141",
                "44",
                "152",
                "116",
                "B07",
                "B19",
                "B09",
                "331",
                "143",
                "163",
                "30",
                "302",
                "S25",
                "188",
                "294",
                "CB10",
                "47",
                "46",
                "F14",
                "X01",
                "X02",
                "S31",
                "108",
                "149",
                "293",
                "82",
                "88",
                "274",
                "80",
                "273",
                "235",
                "V01",
                "161",
                "120",
                "M134",
                "142",
                "S29",
                "S11",
                "130",
                "134",
                "184",
                "252",
                "133",
                "204",
                "166",
                "18",
                "S15",
                "26",
                "191",
                "203",
                "224",
                "284",
                "202",
                "285",
                "286",
                "189",
                "198",
                "254",
                "237",
                "314",
                "56",
                "57",
                "113",
                "124",
                "131",
                "23",
                "20",
                "13",
                "404",
                "101",
                "B12",
                "B08",
                "43",
                "190",
                "241",
                "208",
                "63",
                "145",
                "68",
                "107",
                "85",
                "ZD01",
                "S12",
                "51",
                "138",
                "281",
                "159",
            ],
            "cityCode": ["186"],
            "crossCity": crossCity_list,
            "dispatchAutoTag": "4",
            "distributeOrderFlag": "2",
            "endTime": endDate,  # "2022-08-09",
            "inModeCode": [
                "1011",
                "1013",
                "1014",
                "1018",
                "1019",
                "1022",
                "1024",
                "1025",
                "1026",
                "1029",
                "1030",
                "1032",
                "1041",
                "1045",
                "1050",
                "1051",
                "1053",
                "1054",
                "1056",
                "2002",
                "2001",
                "2002",
                "2003",
                "2004",
                "2005",
                "2006",
                "2008",
                "2009",
                "2010",
                "2011",
                "2015",
                "2115",
                "9004",
                "9005",
                "9007",
                "9008",
                "9010",
                "9011",
                "9012",
                "9013",
                "9014",
                "9016",
                "9017",
                "9018",
                "9019",
                "9021",
                "9022",
                "9023",
                "9024",
                "9026",
                "9050",
                "9051",
                "9052",
                "9053",
                "9057",
                "9058",
                "9059",
                "1118",
                "5018",
                "5118",
                "5218",
                "5318",
                "5418",
                "5518",
                "5618",
                "5718",
                "5818",
                "5918",
                "6018",
                "6118",
                "6218",
                "6318",
                "6418",
                "6518",
                "6618",
                "6718",
                "6818",
                "6918",
                "7018",
                "7118",
                "7218",
                "7318",
                "7418",
                "7518",
                "7618",
                "7718",
                "7818",
                "7918",
                "8018",
                "8118",
                "8218",
                "8318",
                "8418",
                "8518",
                "8618",
                "8718",
                "8818",
                "8918",
                "9001",
                "9002",
                "9003",
                "9006",
                "9015",
                "9020",
                "9025",
                "9065",
                "9061",
                "1048",
                "1057",
                "1021",
                "9068",
                "9056",
                "1015",
                "9076",
                "7476",
                "7676",
            ],
            "mashanggou": [],
            "mashanggouBackState": [],
            "netTypeCode": [],
            "orderSourceTag": ["2", "4"],
            "orderStaffId": "",
            "orderStaffRole": "",
            "orderState": "B0",
            "postCityCode": postCityCode,  # 130400
            "postDistrictCode": postDistrictCode_list,  # ["130402", "130403", "130404"]
            "postProvinceCode": postProvinceCode,  # 130000
            "sceneType": [],
            "serialNumber": "",
        }
        resp = requests.post(
            url=url, json=data, headers=self.headers, cookies=self.dict_cookie
        )
        return resp.json()["claimAmount"]

    # 退单审核通过
    def orderBackDeal_auditOrder(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "btnuuid": "584bce494a4873a4b7933c2cc687b2ba",
            # "X-Tingyun": "c=B|VLw6nMkIkVw;x=f84d8ad081f049a9",
        }

        while True:
            orderid = input("请输入退单单号:")
            if len(orderid) == 16:
                url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderBackDeal/auditOrder"
                data = {
                    "ORDER_ID": orderid,
                    "OPERATOR_TYPE": "00",
                    "OPERATOR_RESULT": "00",
                    "REASON_CODE": "RETURN_REASON_1",
                    "REASON_DESC": "用户退单",
                    "REASON2CODE": "04",
                    "REASON2DESC": "联系不上用户",
                    "OPERATOR_CONTENT": "联系不上用户",
                }
                ck = {
                    "SESSION": "4ebe0fc6-4b73-49d0-a08c-e8f0f628df00;",
                    "UC_SSO_SESSIONID_WEB": "969B193A05BA4161AFCDA1AAA1A09878;",
                    "SERVERID": "3976e6bea0aded1502b0137d6a0b005f|1663481726|1663481589; sessionId=e6014083885647589ad1b4b4027",
                }

                resp = requests.post(
                    url=url, json=data, headers=headers, cookies=self.dict_cookie
                )
                print(resp.status_code)
                print(resp.json())
            elif orderid == "0":
                break

    # 订单详细信息
    def get_dd_detail(self, innerOrderId):
        url = (
                "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderDetail/toOrderDetailIndex?orderId="
                + innerOrderId
                + "&inModeCode="
        )
        resp = requests.get(url=url, headers=self.headers, cookies=self.dict_cookie)

        try:
            developStaffName = re.search(r"发展人名称:(.*?)</span>", resp.text, re.S).group(
                0
            )
            developStaffName = re.search(
                r"<span>(.*?)</span>", developStaffName, re.S
            ).group(1)
        except:
            developStaffName = ""

        try:
            developStaffPhone = re.search(r"发展人电话:(.*?)</span>", resp.text, re.S).group(
                0
            )
            developStaffPhone = re.search(
                r"<span>(.*?)</span>", developStaffPhone, re.S
            ).group(1)
        except:
            developStaffPhone = ""

        try:
            developDepartName = re.search(
                r"发展人部门名称:(.*?)</span>", resp.text, re.S
            ).group(0)
            developDepartName = re.search(
                r"<span>(.*?)</span>", developDepartName, re.S
            ).group(1)
        except:
            developDepartName = ""

        try:
            PowerStaffName = re.search(r"能人经理名称:(.*?)</span>", resp.text, re.S).group(0)
            PowerStaffName = re.search(
                r"<span>(.*?)</span>", PowerStaffName, re.S
            ).group(1)
        except:
            PowerStaffName = ""

        try:
            PowerStaffPhone = re.search(r"能人经理电话:(.*?)</span>", resp.text, re.S).group(
                0
            )
            PowerStaffPhone = re.search(
                r"<span>(.*?)</span>", PowerStaffPhone, re.S
            ).group(1)
        except:
            PowerStaffPhone = ""

        try:
            order_fee = re.search(
                '应收费用合计:.*?<input type="text" name="name" class="no-border red-word" value="(.*?)元" readonly>',
                resp.text,
                re.S,
            ).group(1)
        except:
            order_fee = ""

        try:
            # inner_remark = re.search('订单备注:.*?<input type="text" class="no-border" style="width: 100%" value="(.*?)" readonly>', resp.text, re.S).group(1)
            inner_remark = re.search(
                "订单备注:.*?<span>(.*?)</span>", resp.text, re.S
            ).group(1)
            print(inner_remark)
        except:
            inner_remark = ""

        try:
            inner_custName = re.search(
                '客户姓名:.*?<input type="text" name="custName" class="no-border" value="(.*?)"',
                resp.text,
                re.S,
            ).group(1)
        except:
            inner_custName = ""

        try:
            inner_ContactTel = re.search(
                '联系电话:.*?<input type="text" id="mainContactTel".*?value="(.*?)"',
                resp.text,
                re.S,
            ).group(1)
        except:
            inner_ContactTel = ""

        try:
            inner_mainPsptId = re.search(
                '证件号码:.*?<input.*?id="mainPsptId".*?value="(.*?)"',
                resp.text,
                re.S,
            ).group(1)
        except:
            inner_mainPsptId = ""

        try:
            inner_preAddressInfo = re.search(
                '装机地址:.*?<span>(.*?)</span>',
                resp.text,
                re.S,
            ).group(1)
        except:
            inner_preAddressInfo = ""

        try:
            inner_isiptv = re.search(
                '是否订购IPTV:.*?<input type="text" name="name" class="no-border" value="(.*?)"',
                resp.text,
                re.S,
            ).group(1)
        except:
            inner_isiptv = ""

        inner_ad_no = ""
        inner_ad_device = ""
        iptv_device = ""

        try:
            inner_device_text = re.search(
                '<table id="macroCommodityTable" lay-filter="macroCommodityTable">(.*?)</table>',
                resp.text,
                re.S,
            ).group(0)
            inner_device_list = re.findall("<tr>.*?</tr>", inner_device_text, re.S)
            for inner_device in inner_device_list:
                inner_device_td_list = re.findall("<td>(.*?)</td>", inner_device, re.S)
                if len(inner_device_td_list) >= 9:
                    if (
                            len(inner_device_td_list[0]) == 12
                            and inner_device_td_list[0][:5] == "03100"
                    ):
                        # 宽带号码
                        inner_ad_no = inner_device_td_list[0]
                        # continue

                if len(inner_device_td_list) >= 6:
                    if inner_device_td_list[3] == "ONU光猫":
                        # 宽带设备名称
                        inner_ad_device = inner_device_td_list[5]
                        continue

                if len(inner_device_td_list) >= 6:
                    if inner_device_td_list[3] == "机顶盒":
                        # IPTV设备名称
                        iptv_device = inner_device_td_list[5]

        except Exception as error:
            except_err(error)

        ret_dict = {
                "developStaffName": developStaffName,
                "developStaffPhone": developStaffPhone,
                "developDepartName": developDepartName,
                "PowerStaffName": PowerStaffName,
                "PowerStaffPhone": PowerStaffPhone,
                "order_fee": order_fee,
                "inner_remark": inner_remark,
                "inner_custName": inner_custName,
                "inner_ad_no": inner_ad_no,
                "inner_ad_device": inner_ad_device,
                "inner_isiptv": inner_isiptv,
                "iptv_device": iptv_device,
                "inner_ContactTel": inner_ContactTel,
                "inner_mainPsptId": inner_mainPsptId,
                "inner_preAddressInfo": inner_preAddressInfo,
            }

        return ret_dict

    # 二级
    def second_query(self):
        startDate = datetime.datetime.now() - datetime.timedelta(days=90)
        startDate = startDate.strftime("%Y-%m-%d 00:00:00")

        endDate = datetime.datetime.now() - datetime.timedelta(days=0)
        endDate = endDate.strftime("%Y-%m-%d 23:59:59")

        url = "http://10.238.25.133:8080/order/face/orderQuery/queryOrderPage"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }
        data = {
            "createEnd": endDate,
            "createStart": startDate,
            "isHang": "0",  # "0":未挂起 "1":挂起 "2":全部
            "pageNum": 1,
            "pageSize": 99,
            "queryType": "order_deal",
        }
        cookie = {
            "JSESSIONID": self.jsessionid,
        }
        resp = requests.post(
            url=url, json=data, headers=headers, cookies=self.dict_cookie
        )
        r = resp.json()["RSP"]["DATA"]
        if len(r) > 0:
            return r[0]["total"]
        else:
            return 0

    # 绑定单号
    def orderBondUpdateQryCB(self):
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderBondUpdate/orderBondUpdateQryCB"
        data = {
            "orderId": "6322101403322477",
            "cbOrderId": "1822101447306538",
            "provinceCode": "18",
        }

    # 解挂and挂起
    def orderSuspendOrRegain(self, order_id, order_line_id, operator_type, remarks=""):
        if operator_type == "lock":
            operator_type = "0004"
        elif operator_type == "unlock":
            operator_type = "0005"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://ibos.newbuy.chinaunicom.cn/ibos-eos/main.html",
            "Host": "ibos.newbuy.chinaunicom.cn",
            "Origin": "https://ibos.newbuy.chinaunicom.cn",
        }

        url = "https://ibos.newbuy.chinaunicom.cn/ibos-order/orderExamine/orderSuspendOrRegain"
        data = {
            "ORDER_ID": order_id,
            "ORDER_LINE_ID": order_line_id,  # orderLineId
            "OPERATOR_TYPE": operator_type,  # 解挂 "0005"
            "REASON_CODE": "",
            "REASON_DESC": "",
            "REASON2_CODE": "",
            "REASON2_DESC": "",
            "REMARKS": "",
            "PRE_SOLUTION_HANG_TIME": "",
        }
        resp = requests.post(
            url=url,
            data=jsonDataToCookiesParams(data),
            headers=headers,
            cookies=self.dict_cookie,
        )
        print(resp.json())

        data = {
            "ORDER_ID": order_id,
            "ORDER_LINE_ID": order_line_id,  # orderLineId
            "OPERATOR_TYPE": operator_type,  # 挂起 "0004"
            "REASON_CODE": "03",
            "REASON_DESC": parse.quote("其他"),
            "REASON2_CODE": "03",
            "REASON2_DESC": parse.quote("其他"),
            "REMARKS": parse.quote(remarks),
            "PRE_SOLUTION_HANG_TIME": "",
        }
        resp = requests.post(
            url=url,
            data=jsonDataToCookiesParams(data),
            headers=headers,
            cookies=self.dict_cookie,
        )
        print(resp.json())

    def query_new_firstpage(self, orderNo):
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-service/OrderDataQuery/query/new"
        data = {
            "businessType": "",
            "cancelTag": [],
            "cityCode": [
                "186"
            ],
            "custIp": "",
            "custName": "",
            "dateType": "",
            "dealStaffId": "",
            "deliverMaxTime": "",
            "deliverMinTime": "",
            "dispatchAutoTag": "4",
            "distributeOrderFlag": "2",
            "districtCode": "",
            "extOrderId": "",
            "getCount": "1",
            "goodsName": "",
            "iccid": "",
            "imei": "",
            "inModeCode": [],
            "isAutoIom": "3",
            "isClaim": "2",
            "isReverse": "ALL",
            "isSuspend": "",
            "lgtsOrder": "",
            "mashanggouBackState": [],
            "mashanggouTag": [],
            "maxTime": "2022-09-30",
            "minTime": "2022-09-01",
            "mobilePhone": "",
            "netTypeCode": [],
            "orderKind": "",
            "orderNo": orderNo,
            "orderSourceTag": [
                "01",
                "0",
                "1",
                "2",
                "30",
                "3",
                "4"
            ],
            "orderStaffId": "",
            "orderStaffRole": "",
            "orderState": [],
            "pageNum": 1,
            "pageSize": 5,
            "payId": "",
            "payState": [],
            "payType": [],
            "phoneNumber": "",
            "postTypeList": [],
            "provinceCode": "18",
            "psptNo": "",
            "sceneType": [],
            "timeSort": "desc",
            "tradeTypeCode": [
                "10000",
                "1029",
                "110",
                "1104",
                "12",
                "12000",
                "126",
                "127",
                "136",
                "190",
                "192",
                "1920",
                "196",
                "240",
                "269",
                "270",
                "272",
                "273",
                "274",
                "276",
                "340",
                "381",
                "503",
                "5034",
                "505",
                "592",
                "594",
                "64",
                "65",
                "69",
                "690",
                "7302",
                "9003",
                "790",
                "2152",
                "210028",
                "79",
                "2104",
                "2106",
                "2001",
                "2201",
                "1000",
                "1001",
                "1002",
                "2000",
                "2002",
                "2003",
                "2004",
                "2101",
                "2102",
                "2103",
                "2105",
                "2107",
                "2108",
                "2109",
                "2110",
                "2114",
                "2115",
                "2120",
                "2125",
                "2130",
                "2131",
                "2202",
                "2203",
                "2230",
                "2231",
                "2232",
                "2233",
                "2500",
                "4000",
                "4001",
                "4002",
                "4003",
                "4004",
                "4005",
                "4006",
                "4007",
                "4008",
                "4009",
                "4016",
                "4017",
                "4018",
                "5001",
                "5002",
                "5003",
                "5004",
                "5005",
                "5006",
                "5007",
                "5008",
                "5009",
                "5010",
                "5011",
                "5012",
                "5013",
                "5014",
                "5015",
                "5016",
                "5017",
                "5018",
                "5019",
                "5020",
                "5021",
                "5022",
                "5023",
                "9001",
                "9002",
                "5026",
                "11000",
                "120",
                "141",
                "31",
                "10",
                "11001",
                "11999",
                "3410"
            ],
            "untreatedTime": "2022-11-20",
            "userTag": []
        }
        resp = requests.post(url=url, json=data, headers=self.headers, cookies=self.dict_cookie)
        # print(resp.json())
        try:
            if len(resp.json()['data']['orderList']) == 1:
                return resp.json()['data']['orderList'][0]['list']['orderState']
            else:
                print("多条返回")
                return "多条返回"
        except:
            print("执行出错")
            return "执行出错"

    def backToDispatch(self, orderId, reason):
        """
        订单调回
        """
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/codebuy-dispatch/orderDispatched/ryy/backToDispatch"
        data = {
            "cityCodePost": "130400",
            "districtCodePost": "",
            "dn": "null",
            "logDn": "null",
            "orderCityCode": "186",
            "orderId": orderId,
            "orderProvinceCode": "18",
            "phoneNumber": "",
            "provinceCodePost": "130000",
            "reason": reason,
            "remark": "null",
            "rsyncTag": 2
        }
        resp = requests.post(url=url, json=data, headers=self.headers, cookies=self.dict_cookie)
        try:
            res = resp.json()['code']
            print("backToDispatch", res)
            return res
        except:
            return "error"

    def order_cancel_apply(self, orderId, remark):
        """
        申请退单
        """
        url = "https://ibos.newbuy.chinaunicom.cn/ibos-eos/order-cancel/v2/api/order/cancel/apply"
        data = {
            "backOrderSource": "RX",
            "exReasonCode": "0502",
            "exType": "02",
            "orderId": orderId,
            "remark": remark,
            "specRemark": "其他原因",
            "type": "1"
        }
        resp = requests.post(url=url, json=data, headers=self.headers, cookies=self.dict_cookie)
        print("order_cancel_apply", resp.json())


if __name__ == "__main__":
    nsop = Nsop()

    # nsop.load_ck_token()
    # nsop.close_2()
    #
    # exit()

    try:
        file_time_life = get_file_last_modify_leave_now("./nsop_cookies.json")
        if file_time_life > 120:
            nsop.login()
    except:
        nsop.login()

    nsop.load_ck_token()
    try:
        while True:
            print("请选择操作类型:")
            choises = {
                "1": "订单监控",
                "2": "订单审核退单(超25天/黑名单)",
                "3": "订单退单",
                "4": "退单审核通过",
                "5": "超期订单解挂",
                "6": "订单详细查询",
                "0": "退出",
            }

            s = input_choise(choises)

            if s == "1":
                # list_o = ["0","0","0","0","0","0","0","0","0","0"]
                i = 0
                while True:
                    i = i + 1
                    # 订单生产新宽融
                    try:
                        ret1 = nsop.toQueryOrderManageList(orderState="CA")  # 快速
                        ret2 = nsop.toQueryOrderManageList(orderState="C5")  # 急速
                        ret1a, ret2a = nsop.toQueryOrderManageList(orderState="")
                    except:
                        ret1, ret2, ret1a, ret2a = "N", "N", "N", "N"

                    # 订单生产
                    try:
                        ret3 = nsop.orderaccount()
                    except:
                        ret3 = "N"

                    # 订单调度
                    try:
                        ret4 = nsop.orderManualDispatcher(
                            groupBin=1, orderSourceTag_list=["3"]
                        )
                        ret5 = nsop.orderManualDispatcher(
                            groupBin=0, orderSourceTag_list=["3"]
                        )
                        ret6 = nsop.orderManualDispatcher(
                            groupBin=1,
                            orderSourceTag_list=["2", "4"],
                            cityCode_list=["186_130400"],
                            districtCodePost="130402,130403,130404",
                            provinceCode="18_130000",
                        )
                        ret7 = nsop.orderManualDispatcher(
                            groupBin=0,
                            orderSourceTag_list=["2", "4"],
                            cityCode_list=["186_130400"],
                            districtCodePost="130402,130403,130404",
                            provinceCode="18_130000",
                        )
                    except:
                        ret4, ret5, ret6, ret7 = "N", "N", "N", "N"

                    # 订单领取
                    try:
                        ret8 = nsop.queryClaimOrderNum(
                            crossCity_list=[],
                            postCityCode="130400",
                            postDistrictCode_list=["130402", "130403", "130404"],
                            postProvinceCode="130000",
                        )
                        ret9 = nsop.queryClaimOrderNum(
                            crossCity_list=["1", "2"],
                            postCityCode="",
                            postDistrictCode_list=[],
                            postProvinceCode="",
                        )
                    except:
                        ret8, ret9 = "N", "N"

                    # 二级
                    try:
                        ret10 = nsop.second_query()
                    except:
                        ret10 = "N"

                    list_n = [
                        ret3,
                        ret1,
                        ret2,
                        ret10,
                        ret4,
                        ret5,
                        ret6,
                        ret7,
                        ret8,
                        ret9,
                    ]
                    color_list = [0, 1, 2, 3]

                    title = ["第%d次:" % i]
                    row1 = (
                            str(ret3)
                            + "|"
                            + str(ret1a)
                            + "-"
                            + str(ret2a)
                            + "|"
                            + str(ret10)
                    )
                    row2 = (
                            str(ret4) + "-" + str(ret5) + "|" + str(ret6) + "-" + str(ret7)
                    )
                    row3 = str(ret8) + "-" + str(ret9)
                    row = [row1 + "\n" + row2 + "\n" + row3]

                    # 黑底白色
                    colorB, colorF = 0x00, 0x07
                    for _c in color_list:
                        try:
                            if int(list_n[_c]) > 0:
                                # B_HSKYBLUE, F_YELLOW
                                colorB, colorF = 0xB0, 0x06
                                break
                        except:
                            continue

                    setColor(colorB, colorF)
                    print_pt(title, row, head=True)

                    time.sleep(30)

            elif s == "2":
                print("急速:")
                nsop.return_order_over_25(groupBin="1", isSuspend="0")
                print("快速:")
                nsop.return_order_over_25(groupBin="0", isSuspend="0")
                print("异常:")
                nsop.return_order_over_25(groupBin="2", isSuspend="0")

            elif s == "3":
                nsop.run_return_order()

            elif s == "4":
                nsop.orderBackDeal_auditOrder()

            elif s == "5":
                nsop.return_order_over_25(groupBin="0", isSuspend="1")
                nsop.return_order_over_25(groupBin="1", isSuspend="1")
                nsop.return_order_over_25(groupBin="2", isSuspend="1")

            elif s == "6":

                # innerOrderId = input("请输入内部订单号:")
                nsop.get_dd_detail("6322100202180254")

            elif s == "0":
                break

    except Exception as error:
        except_err(error)
        print("Cookies已失效,请重新运行!")
