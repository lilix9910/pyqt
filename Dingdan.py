#! /usr/bin/env python3
from numpy import outer
from WebUi import WebBrowser
from selenium.webdriver import ActionChains
from BaseFunc import except_err, identify_gap, print_df
from Config import DING_BROWSER, DING_CAPTCHA_MODE, ALLOWS_LIST, ALL_ALLOWS_LIST, WAIT_TIME
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import re
import datetime
import time
import requests
import json
import base64
import pandas as pd


class dingdan:

    dict_cookie = dict()
    dict_cust = {}
    dict_order = {}
    df = None

    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Content-Type":
        "application/x-www-form-urlencoded",
        "Referer":
        "http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do",
        "Upgrade-Insecure-Requests":
        "1",
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }

    # 订单系统获取Cookie
    def login(self):
        from Config import USERNAME, PASSWORD
        if DING_CAPTCHA_MODE == 1:

            web = WebBrowser(DING_BROWSER, mode=False, remote_addr="")
            web.set_implicitly_wait(WAIT_TIME)

            web.open("http://133.96.12.18:10005/mgWeb/")
            web.click((By.CSS_SELECTOR, ".down"))
            web.click((By.XPATH, "//div[text()='河北']"))
            web.send_key((By.CSS_SELECTOR, "#login"), USERNAME)
            web.send_key((By.CSS_SELECTOR, "#password"), PASSWORD)
            print("登录后回车继续,25s")
            time.sleep(25)


        else:
            # 订单系统获取Cookies-划块验证码
            web = WebBrowser(DING_BROWSER, mode=False, remote_addr="")
            web.set_implicitly_wait(WAIT_TIME)

            while True:
                try:
                    # web.open("http://133.96.12.18:10005/mgWeb/?handle=old")
                    web.open("http://133.96.12.18:10005/mgWeb/")
                    web.click((By.CSS_SELECTOR, ".down"))
                    web.click((By.XPATH, "//div[text()='河北']"))
                    web.send_key((By.CSS_SELECTOR, "#login"), USERNAME)
                    web.send_key((By.CSS_SELECTOR, "#password"), PASSWORD)
                    sg = web.driver.page_source
                    big = re.findall("returnPath=(.*?)&quot;", sg, re.S)[0]
                    small = re.findall(
                        "&quot;data:image/png;base64,(.*?)&quot;", sg, re.S)[0]

                    url = "https://uac.sso.chinaunicom.cn/uac-sso-zq/getVerifyImage?returnPath=" + big
                    resp = requests.get(url)
                    with open("./big.png", "wb") as fi:
                        fi.write(resp.content)

                    with open("./small.png", "wb") as fi:
                        fi.write(base64.b64decode(small))

                    move_to = identify_gap("./big.png", "./tp_real.png")

                    if move_to == 0:
                        continue
                    # time.sleep(2)
                    # continue

                    ActionChains(web.driver).click_and_hold(
                        web.find_element(
                            (By.XPATH,
                             "//div[@id='drag']//div[3]"))).perform()

                    move_to = move_to + 5
                    ActionChains(web.driver).move_by_offset(
                        move_to * 2 / 3, 0).perform()
                    ActionChains(web.driver).move_by_offset(
                        move_to * 1 / 3, 0).perform()
                    ActionChains(web.driver).release().perform()
                    time.sleep(0.5)

                    web.click((By.CSS_SELECTOR, "#check"))

                    time.sleep(3)
                    handles = web.driver.window_handles
                    if len(handles) != 2:
                        continue

                    for handle in handles:
                        if web.driver.current_window_handle != handle:
                            web.driver.switch_to.window(handle)
                            break

                    # print(web.driver.page_source)
                    if "上次登录时间" in web.driver.page_source:
                        print("订单系统登录成功!")
                        break
                except Exception as err:
                    except_err(err)
                    print("订单中心系统登录异常错误,重新登录...")
                    time.sleep(3)

            # web.open("http://133.96.12.18:10005/mgWeb/")
            # input("To Be Continue...")

        cookies = web.driver.get_cookies()
        jsonCookies = json.dumps(cookies)
        self.save_cookie(jsonCookies)
        web.quit()
        self.load_cookie()
        return "登陆成功"

    def save_cookie(self, cookie):
        with open('d:/Onedrive/fcbss/dingdan_cookies.json', 'w') as f:
            f.write(cookie)

    def load_cookie(self):
        try:
            # with open("./dingdan_cookies.json", 'r', encoding='utf-8') as f:
            with open("d:/Onedrive/fcbss/dingdan_cookies.json", 'r', encoding='utf-8') as f:
                listCookies = json.loads(f.read())
            for cookie in listCookies:
                self.dict_cookie[cookie['name']] = cookie['value']
        except:
            pass

    # 获取意向单列表
    def get_pp_list(self):
        today = datetime.datetime.now()
        create_start = today.strftime('%Y-%m-%d 00:00:00')
        create_end = today.strftime('%Y-%m-%d 23:59:59')

        url = "http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do"
        data = {
            "btnType": "ordList",
            "params.query_btn_flag": "yes",
            "query_type": "order_view",
            "params.flow_id_c": "",
            "params.flow_id": "",
            "params.trade_eparchy_code_c": "",
            "params.trade_eparchy_code": "",
            "params.trade_depart": "",
            "params.trade_staff_id": "",
            "params.order_from_c": "",
            "params.order_from": "",
            "params.channel_type_c": "",
            "params.channel_type": "",
            "params.phone_owner_name": "",
            "params.link_phone": "",
            "params.tid_category_c": "监控单（意向单）,咨询单, 咨询单（省分）",
            "params.tid_category": "Z49,Z69,Z73",
            "order_channel": "Z49",
            "order_channel": "Z69",
            "order_channel": "Z73",
            "params.out_tid": "",
            "params.order_id": "",
            "params.create_start": create_start,
            "params.create_end": create_end,
            "params.lockusername": "",
            "params.status2": "",
            "params.order_is_his": "2",
            "params.order_is_return": "",
            "params.order_is_allot": "",
            "params.serial_num": "",
            "params.foStatusText": "",
            "params.foStatus": "",
            "params.openAccMode": "",
            "params.order_kind": "",
            "query_list_by_bt": "Y",
            "params.src_out_tid": "",
            "params.cert_card_num": "",
            "username": "",
            "params.lock_user_id": ""
        }

        inner_order_list = []
        while True:
            resp = requests.post(url=url,
                                 data=data,
                                 headers=self.headers,
                                 cookies=self.dict_cookie,
                                 verify=False)
            if "您尚未登录或登录已经超时" in resp.text:
                print("Cookies已经失效,请重新登录!")
                self.login()
                self.load_cookie()
            else:
                break

        # print(resp.text)
        try:
            # <div class="right_warp">
            # 把注释掉的代码删掉
            temp = re.sub(r'<!--.*?-->', '', resp.text, count=0, flags=re.S)
            res = re.search(
                r'<div class="right_warp">(.*?)<div class="page" >', temp,
                re.S).group(1)
            # print(res)
            tr_list = re.findall(r'<tr(.*?)</tr>', res, flags=re.S)
            count = len(tr_list) - 1
            # print("本次查询到 %d 条订单" % count)
            for x in range(1, len(tr_list)):
                td_list = re.findall(r'<td(.*?)</td>', tr_list[x], re.S)
                # 内部订单编号
                inner_no = re.findall(
                    r'<a name="inner_order_id" order_id="(.*?)"', td_list[1],
                    re.S)[0]
                # 分配时间
                assi_time = re.findall(r'<li><span>分配时间：</span>(.*?)</li>',
                                       td_list[3], re.S)[0]
                # li_list = re.findall(r'<li>(.*?)</li>', td_list[4], re.S)
                # # 受理方式
                # inner_type = re.findall(r'<span>(.*?)</span>', li_list[4], re.S)[1]
                # # 异常状态
                # inner_abnormal = re.sub(r'(异常状态：|<.*?>)', '', li_list[3], count=0, flags=re.S).strip()
                # 业务类型
                busi_type = re.findall(
                    r'<li><span>业务类型：</span><div>(.*?)</div></li>', td_list[1],
                    re.S)[0]
                # 订单来源
                order_resource = re.findall(
                    r'<li><span>订单来源：</span><div>(.*?)</div></li>', td_list[1],
                    re.S)[0]
                # 客户名称
                cust_name = re.findall(r'<p class="tit">客户名称：(.*?)</p>',
                                       td_list[2], re.S)[0].strip()
                # 客户联系方式
                cust_telnum = re.findall(r'<p class="tit">客户联系方式：(.*?)</p>',
                                         td_list[2], re.S)[0]
                # 渠道类型
                channel_type = re.findall(r'<li><span>渠道类型：</span>(.*?)</li>',
                                          td_list[4], re.S)[0].strip()
                # channel_type = channel_type.stripe()
                # 传回参数
                inner_order_list.append([
                    inner_no, cust_name, cust_telnum, assi_time, busi_type,
                    order_resource, channel_type
                ])
                # print(inner_order_list)

        except Exception:
            print("获取内部订单号错误!")
            return ''
        return inner_order_list, count

    # 获取订单具体信息及业务信息
    def get_order_detail(self, inner_order):

        self.dict_cust = {}
        self.dict_order = {}
        self.df = None
        self.table = None

        url = "http://133.96.12.18:10005/shop/admin/orderFlowAction!order_detail_view.do?order_id=" + inner_order + "&query_type=order_view&optType="
        while True:
            resp = requests.get(url=url,
                                headers=self.headers,
                                cookies=self.dict_cookie)
            if "您尚未登录或登录已经超时" in resp.text:
                print("订单系统Cookies已过期,正在重新登录...")
                self.login()
            else:
                break

        # 添加表格print
        try:
            listA = []
            b = re.search("<!-- 业务信息开始-->.*?<!-- 业务信息结束 -->", resp.text, re.S).group()
            c = re.findall("<tr.*?</tr>", b, re.S)
            for _c in c[1:]:
                listB = []
                d = re.findall("<td.*?</td>", _c, re.S)
                for _d in d:
                    try:
                        e = re.search('"this_cp\(this\)" >(.*?)<', _d, flags=re.S)
                        listB.append(e.group(1))
                    except:
                        listB.append("None")
                listA.append(listB[0:2] + listB[6:7] + listB[3:4])

            p = pd.DataFrame(listA)
        except:
            p = pd.DataFrame()
        
        self.table = p
        # return self.table

        try:
            self.dict_cust['cust_name'] = re.search(r"<th>客户名称：</th>(.*?)\(",
                                                    resp.text, re.S).group(1)
            self.dict_cust['cust_name'] = re.sub("\r|\n| |<(.*?)>", "",
                                                 self.dict_cust['cust_name'])
            self.dict_cust['cert_num'] = re.search(r"<th>证件号码：</th>(.*?)</td>",
                                                   resp.text, re.S).group(1)
            self.dict_cust['cert_num'] = re.sub("\r|\n| |<(.*?)>", "",
                                                self.dict_cust['cert_num'])
            self.dict_cust['tel_num'] = re.search(r"<th>联系电话：</th>(.*?)</td>",
                                                  resp.text, re.S).group(1)
            self.dict_cust['tel_num'] = re.sub("\r|\n| |<(.*?)>", "",
                                               self.dict_cust['tel_num'])
            self.dict_cust['cust_id'] = re.search(r"<th>客户名称：.*?\((.*?)\)",
                                                  resp.text, re.S).group(1)
            try:
                self.dict_cust['cust_address'] = re.search(
                    r'<th>住址：</th>.*?<td>(.*?)</td>', resp.text, re.S).group(1)
            except:
                self.dict_cust['cust_address'] = ''
            finally:
                if len(self.dict_cust['cust_address']) == 0:
                    self.dict_cust['cust_address'] = 'Null'

        except:
            print("订单基本用户信息失败!")

        try:
            txt = re.search(r"<!--订单基本信息开始-->(.*?)<!-- 订单基本信息结束 -->",
                            resp.text, re.S).group()
            tr = re.findall(r"<tr(.*?)</tr>", txt, re.S)
            for i in tr:
                th = re.findall(r"<th>(.*?)</th>", i, re.S)
                td = re.findall(r"<td(.*?)</td>", i, re.S)
                for j in range(len(th)):
                    x = re.sub(r"<(.*?)>|：|:", "", th[j], count=0, flags=re.S)

                    if "备注" in x:
                        y = re.sub(r"<(.*?)>",
                                   "",
                                   "<" + td[j],
                                   count=0,
                                   flags=re.S)
                    else:
                        y = re.sub(r"<(.*?)>|\r|\n",
                                   "",
                                   "<" + td[j],
                                   count=0,
                                   flags=re.S)

                    if len(x) == 0:
                        continue
                    self.dict_order[x.strip()] = y.strip()
        except:
            print("订单基本信息失败!")

        # 只有在cbss做的订单才需要下面的业务解析
        try:
            if self.dict_order['业务类型'] in ALL_ALLOWS_LIST:
            # 需要挂起的业务类型


                # print(self.dict_order['内部订单编号'])
                # 查询是否已经有cbss订单,有的话直接绑定,订单必须在自己可以做的业务里
                if self.dict_order['业务类型'] in ALLOWS_LIST:
                    bss_exist_order_no_list = re.findall(
                        r'name="bss_order_no[1-5]" value="(.*?)"/></td>',
                        resp.text, re.S)
                    for x in range(len(bss_exist_order_no_list)):
                        i = bss_exist_order_no_list[x]
                        if len(i) == 16:
                            print("bss_order_no%s: %s 已存在,直接绑定订单完成!" %
                                  (str(x + 1), i))
                            with open('./cbss_log/%s.txt' %
                                      datetime.datetime.now().strftime(
                                          '%Y-%m-%d'),
                                      'a+',
                                      encoding='utf-8') as f:
                                f.write(datetime.datetime.now().strftime(
                                    '%Y-%m-%d %H:%M:%S') + "----" +
                                        self.dict_order['内部订单编号'] + "----[" +
                                        i + "]----" + self.dict_order['业务类型'] +
                                        "----" + self.dict_cust['cust_name'] +
                                        "----" + self.dict_cust['tel_num'] +
                                        "----" + self.dict_cust['cert_num'] +
                                        "----" + self.dict_cust['cust_id'] +
                                        "----" +
                                        self.dict_cust['cust_address'] + "\n")
                            self.complete_order(i, x + 1)
                            return False

                    # for i in bss_exist_order_no_list:
                    #     if len(i) == 16:
                    #         print("bss_order_no: %s 已存在,直接业务完成!" % i)
                    #         self.complete_order(i)
                    #         return False
        except Exception:
            print("查找已存在的bss_order_no失败!")


    # 获得订单列表
    def get_order_list(self):
        create_start = datetime.datetime.now() - datetime.timedelta(weeks=5)
        create_start = create_start.strftime('%Y-%m-%d %H:%M:%S')
        create_end = datetime.datetime.today() + datetime.timedelta(hours=2)
        create_end = create_end.strftime('%Y-%m-%d %H:%M:%S')

        url = "http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do"
        data = {
            "btnType": "ordList",
            "params.query_btn_flag": "yes",
            "query_type": "order",
            "params.flow_id_c": "",
            "params.flow_id": "",
            "params.trade_eparchy_code_c": "",
            "params.trade_eparchy_code": "",
            "params.trade_depart": "",
            "params.trade_staff_id": "",
            "params.order_from_c": "",
            "params.order_from": "",
            "params.channel_type_c": "",
            "params.channel_type": "",
            "params.phone_owner_name": "",
            "params.link_phone": "",
            "params.tid_category_c": "",
            "params.tid_category": "",
            "params.out_tid": "",
            "params.order_id": "",
            "params.create_start": create_start,
            "params.create_end": create_end,
            "params.serial_num": "",
            "params.lockusername": "",
            "params.status2": "",
            "params.foStatusText": "",
            "params.foStatus": "",
            "query_list_by_bt": "Y",
            "params.src_out_tid": "",
            "params.cert_card_num": "",
            'pageSize': '499'
        }

        inner_order_list = []
        while True:
            resp = requests.post(url=url,
                                 data=data,
                                 headers=self.headers,
                                 cookies=self.dict_cookie,
                                 verify=False)
            if "您尚未登录或登录已经超时" in resp.text:
                print("Cookies已经失效,请重新登录!")
                self.login()
            else:
                break

        try:
            # <div class="right_warp">
            # 把注释掉的代码删掉
            temp = re.sub(r'<!--.*?-->', '', resp.text, count=0, flags=re.S)
            res = re.search(
                r'<div class="right_warp">(.*?)<div class="page" >', temp,
                re.S).group(1)
            tr_list = re.findall(r'<tr(.*?)</tr>', res, flags=re.S)
            count = len(tr_list) - 1
            # print("本次查询到 %d 条订单" % count)
            for x in range(1, len(tr_list)):
                td_list = re.findall(r'<td(.*?)</td>', tr_list[x], re.S)
                # 内部订单编号
                inner_no = re.findall(
                    r'<a name="inner_order_id" order_id="(.*?)"', td_list[1],
                    re.S)[0]
                # 分配时间
                assi_time = re.findall(r'<li><span>分配时间：</span>(.*?)</li>',
                                       td_list[3], re.S)[0]
                li_list = re.findall(r'<li>(.*?)</li>', td_list[4], re.S)
                # 受理方式
                inner_type = re.findall(r'<span>(.*?)</span>', li_list[4],
                                        re.S)[1]
                # 异常状态
                inner_abnormal = re.sub(r'(异常状态：|<.*?>)',
                                        '',
                                        li_list[3],
                                        count=0,
                                        flags=re.S).strip()
                # 业务类型
                busi_type = re.findall(
                    r'<li><span>业务类型：</span><div>(.*?)</div></li>', td_list[1],
                    re.S)[0]
                # 客户名称
                cust_name = re.findall(r'<p class="tit">客户名称：(.*?)</p>',
                                       td_list[2], re.S)[0]
                # 传回参数
                inner_order_list.append([
                    inner_no, inner_type, inner_abnormal, assi_time, busi_type,
                    cust_name
                ])

        except Exception:
            print("获取内部订单号错误!")
            return ''
        return inner_order_list, count

    # 获得移机终端类型 ONU移机 还是 IPTV移机
    def get_inst_detail(self, inst_id):

        url = "http://133.96.12.18:10005/shop/admin/orderFlowAction!busIncludePage.do"
        data = {
            "order_id": self.dict_order['内部订单编号'],
            "ajax": "yes",
            "includePage": "bro_terminal_info",
            "inst_id": inst_id
        }
        resp_terminal = requests.post(url=url,
                                      data=data,
                                      headers=self.headers,
                                      cookies=self.dict_cookie)
        r = re.sub(r"<!-- (.*?)-->",
                   '',
                   resp_terminal.text,
                   count=0,
                   flags=re.S)
        l = re.findall(r'<th>终端类型：</th>(.*?)<th>设备提供方式：</th>', r, flags=re.S)
        terminal_type_list = []
        for x in l:
            terminal_type_list.append(
                re.search(r'<td><p onClick="this_cp\(this\)" >(.*?)</p></td>',
                          x).group(1).strip())

        url = "http://133.96.12.18:10005/shop/admin/orderFlowAction!busIncludePage.do"
        data = {
            "order_id": self.dict_order['内部订单编号'],
            "ajax": "yes",
            "includePage": "bro_goods_info",
            "inst_id": inst_id
        }
        resp_goods = requests.post(url=url,
                                   data=data,
                                   headers=self.headers,
                                   cookies=self.dict_cookie)
        r = re.sub(r"<!-- (.*?)-->", '', resp_goods.text, count=0, flags=re.S)
        l = re.findall(r'<th>商品名称：</th>(.*?)<th>商品类型：</th>', r, flags=re.S)
        terminal_goods_list = []
        for x in l:
            terminal_goods_list.append(
                re.search(r'<td><p onClick="this_cp\(this\)" >(.*?)</p></td>',
                          x).group(1).strip())

        # 把质差的商品名称删掉
        for x in terminal_goods_list:
            if x in ["质差活动预存240元（分12个月转兑）", "质差活动预存240元（分12月转兑）", '光猫质差活动预存240元（分12月转兑）', '光猫质差活动预存120元（分12月转兑）', '机顶盒质差活动预存240元（分12个月转兑）']:
                terminal_goods_list.remove(x)

        type_goods_list = []
        # print(terminal_goods_list, terminal_type_list)
        if len(terminal_type_list) == len(terminal_goods_list):
            for x in range(len(terminal_type_list)):
                type_goods_list.append(terminal_type_list[x] + "|" +
                                       terminal_goods_list[x])
        else:
            print("解析附属设备失败!")
        return type_goods_list

    # 开启工单池
    def open_pool(self, pool_id):
        url = "http://133.96.12.18:10005/shop/admin/workerPoolAction!openWorkerPoolRelState.do"
        data = {
            "ajax": "yes",
            "workPoolRel.pool_ids": pool_id
        }

        resp = requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
        if resp.text == "{result : 0 }":
            return "老系统开启工单池结果为：成功"
        else:
            return "老系统开启工单池结果为：失败"

    # 关闭工单池
    def close_pool(self, pool_id):
        url = "http://133.96.12.18:10005/shop/admin/workerPoolAction!closeWorkerPoolRelState.do"
        data = {
            "ajax": "yes",
            "workPoolRel.pool_ids": pool_id
        }

        resp = requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
        if resp.text == "{result : 0 }":
            return "老系统关闭工单池结果为：成功"
        else:
            return "老系统关闭工单池结果为：失败"

    # 重新分配订单
    def update_lock(self, u):
        url = 'http://133.96.12.18:10005/shop/admin/ordAuto!updateLock.do'
        data = {
            'ajax':
            'yes',
            'userid':
            'zhangzl37',
            'realname':
            '%E5%BC%A0%E5%BF%A0%E9%9B%B7',
            'lockOrderIdStr':
            self.dict_order['内部订单编号'],
            'dep_name':
            '%E9%82%AF%E9%83%B8%E5%B8%82%E5%8C%BA%E9%A2%84%E5%8F%97%E7%90%86%E5%B7%A5%E5%8F%B7%E6%B1%A01'
        }
        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("订单重新分配结果为:")
        print(resp.text)

    # 挂起订单
    def lock_order(self, hang_code="03", lock_text=''):
        """code:03 hand_reason:其他 hand_desc:需要核实一下"""
        """hang_code: 05  hand_reason: 用户手机关机"""

        if hang_code == "05":
            hand_reason = "用户手机关机"
        else:
            hand_reason = "其他"

        # lock_text = re.sub(r'[^\u4e00-\u9fa5^a-z^A-Z^0-9]', ' ', lock_text, count=0, flags=re.S)
        url = "http://133.96.12.18:10005/shop/admin/shop/admin/orderFlowAction!orderHangs.do?ajax=yes"
        data = {
            "orders": "",
            "hand_desc": lock_text[:66],
            "hang_code": hang_code,
            "hand_reason": hand_reason,
            "order_id": self.dict_order['内部订单编号']
        }

        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("挂起订单结果为:")
        print(resp.text)

    # OZ撤销订单
    def oz_order(self, cbss_order_id):
        url = "http://133.96.12.18:10005/shop/admin/ordReturned!purOrderCancel.do?order_id=" + self.dict_order[
            '内部订单编号'] + "&dealDescIE8=&ajax=yes"
        data = {
            "query_type": "order_hang",
            "d_type": "apply",
            "oldCertNum": self.dict_cust['cert_num'],
            "order_city_code": "0310",
            "custId": self.dict_cust['cust_id'],
            "bss_order_no1:": "",
            "bss_order_no2:": "",
            "bss_order_no3:": "",
            "bss_order_no4:": "",
            "bss_order_no5:": "",
            "remark": ""
        }

        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("OZ订单撤销结果为:")
        print(resp.text)

    # 解锁订单
    def unlock_order(self):
        url = "http://133.96.12.18:10005/shop/admin/orderFlowAction!cancelTheOrderToHang.do?order_id=" + self.dict_order[
            '内部订单编号'] + "&dealDescIE8=&ajax=yes"
        data = {"query_type": "order_hang", "d_type": "apply"}
        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("解挂订单结果为:")
        print(resp.text)

    # 绑定订单
    def complete_order(self, cbss_order_id, bss_order_number=1):
        url = "http://133.96.12.18:10005/shop/admin/orderFlowAction!lockAccount.do?order_id=" + self.dict_order[
            '内部订单编号'] + "&dealDescIE8=&ajax=yes"
        data = {
            "query_type": "order",
            "d_type": "apply",
            "oldCertNum": self.dict_cust['cert_num'],
            "order_city_code": "0310",
            "custId": self.dict_cust['cust_id']
        }
        for x in range(1, 6):
            if x == bss_order_number:
                data["bss_order_no%s" % str(x)] = cbss_order_id
            else:
                data["bss_order_no%s" % str(x)] = ""

        # print(data)
        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("订单绑定结果:")
        print('^#^' * 6)
        print(resp.text)
        print('^#^' * 6)

    # 退单
    def return_order(self, back_text='', hand_code=('10', '其他原因')):
        url = "http://133.96.12.18:10005/shop/admin/shop/admin/ordReturned!returnedApply.do?ajax=yes&applyFrom=1"
        
        hang_code, hand_reason = hand_code
        data = {
            "hand_desc": back_text,
            "hang_code": hang_code,
            "hand_reason": hand_reason,
            "order_id": self.dict_order['内部订单编号'],
            "sub_hang_code": hang_code,
            "sub_hand_reason": hand_reason,
        }
        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("退单结果为:")
        print(resp.text)

    # 获取订单数量
    def get_count(self, user_name, start_date, end_date):

        url = "http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do?page=1"
        data = {
            'btnType': 'ordList',
            'params.query_btn_flag': 'yes',
            'query_type': 'order_view',
            'params.flow_id_c': '',
            'params.flow_id': '',
            'params.trade_eparchy_code_c': '',
            'params.trade_eparchy_code': '',
            'params.trade_depart': '',
            'params.trade_staff_id': '',
            'params.order_from_c': '',
            'params.order_from': '',
            'params.channel_type_c': '',
            'params.channel_type': '',
            'params.phone_owner_name': '',
            'params.link_phone': '',
            'params.tid_category_c':
            '融合新装,宽带新装,固网移机,固网变更,固网新装,融合变更,固网新装(预开通单),融合新装(预开通单),固网一号双机,IPTV加装,智能组网,固话新装（智能终端）,移网变更,宽带提速包',
            'params.tid_category':
            'Z12,Z10,Z18,Z17,Z16,Z26,Z33,Z32,Z42,Z39,Z47,Z45,Z51,Z68',
            'order_channel': 'Z12',
            'order_channel': 'Z10',
            'order_channel': 'Z18',
            'order_channel': 'Z17',
            'order_channel': 'Z16',
            'order_channel': 'Z26',
            'order_channel': 'Z33',
            'order_channel': 'Z32',
            'order_channel': 'Z42',
            'order_channel': 'Z39',
            'order_channel': 'Z47',
            'order_channel': 'Z45',
            'order_channel': 'Z51',
            'order_channel': 'Z68',
            'params.out_tid': '',
            'params.order_id': '',
            'params.create_start': start_date,
            'params.create_end': end_date,
            'params.lockusername': user_name,
            'params.status2': '',
            'params.order_is_his': '2',
            'params.order_is_return': '',
            'params.order_is_allot': '',
            'params.serial_num': '',
            'params.foStatusText': '',
            'params.foStatus': '',
            'params.openAccMode': '0',
            'params.order_kind': '',
            'query_list_by_bt': 'Y',
            'params.src_out_tid': '',
            'params.cert_card_num': '',
            'username': '',
            'params.lock_user_id': '',
            'pageSize': '499'
        }
        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        count = resp.text.count("外部编号")
        print(user_name, ":", count)

    # 半自动订单开户提交
    def harf_order_complete(self, speed=''):
        # 宽带新装 固网移机
        url = "http://133.96.12.18:10005/shop/admin/orderFlowAction!openAccountHandTouch.do?order_id=" + self.dict_order[
            '内部订单编号'] + "&dealDescIE8=&ajax=yes"
        data = {
            "query_type": "order",
            "d_type": "apply",
            "oldCertNum": self.dict_cust['cert_num'],
            "speed": speed,
            "order_city_code": "0310",
            "custId": self.dict_cust['cust_id'],
            "bss_order_no1": "",
            "bss_order_no2": "",
            "bss_order_no3": "",
            "bss_order_no4": "",
            "bss_order_no5": "",
            "remark:": ""
        }

        # 移机半自动，需要填充速率
        if self.dict_order['业务类型'] == '固网移机':
            data.update({
                "speed": speed,
            })

        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        return resp.text

    # 订单系统获得订单号通过联系电话
    def get_orderid_by_telnum(self, tel_num):
        create_start=datetime.datetime.now() - datetime.timedelta(hours=720)
        create_start=create_start.strftime('%Y-%m-%d %H:%M:%S')
        create_end=datetime.datetime.today() + datetime.timedelta(hours=2)
        create_end=create_end.strftime('%Y-%m-%d %H:%M:%S')
    
        url="http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do"
        data={
        "btnType": "ordList",
        "params.query_btn_flag": "yes",
        "query_type": "order_view",
        "params.flow_id_c": "",
        "params.flow_id": "",
        "params.trade_eparchy_code_c": "",
        "params.trade_eparchy_code": "",
        "params.trade_depart": "",
        "params.trade_staff_id": "",
        "params.order_from_c": "",
        "params.order_from": "",
        "params.channel_type_c": "",
        "params.channel_type": "",
        "params.phone_owner_name": "",
        "params.link_phone": tel_num,
        "params.tid_category_c": "预开通单",
        "params.tid_category": "Z29",
        "order_channel": "Z29",
        "params.out_tid": "",
        "params.order_id": "",
        "params.create_start": create_start,
        "params.create_end": create_end,
        "params.lockusername": "",
        "params.status2": "",
        "params.order_is_his": "2",
        "params.order_is_return": "",
        "params.order_is_allot": "",
        "params.serial_num": "",
        "params.foStatusText": "",
        "params.foStatus": "",
        "params.openAccMode": "",
        "params.order_kind": "",
        "query_list_by_bt": "Y",
        "params.cert_card_num": "",
        "username": "",
        "params.lock_user_id": ""
        }

        resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
        if "您尚未登录或登录已经超时" in resp.text:
            print("Cookies已经失效,请重新登录!")
            self.login()
            resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)

        try:
            # <div class="right_warp">
            # 把注释掉的代码删掉
            temp = re.sub(r'<!--.*?-->', '', resp.text, count=0, flags=re.S)
            res = re.search(r'<div class="right_warp">(.*?)<div class="page" >', temp, re.S).group(1)
            # print(res)
            tr_list = re.findall(r'<tr(.*?)</tr>', res, flags=re.S)

            if len(tr_list) >= 2:
                # print("本次查询到 %d 条订单" % count)
                # for x in range(1,len(tr_list)):
                x = len(tr_list)-1
                td_list = re.findall(r'<td(.*?)</td>', tr_list[x], re.S)
                # 内部订单编号
                inner_no = re.findall(r'<a name="inner_order_id" order_id="(.*?)"', td_list[1], re.S)[0]
                outer_no = re.findall(r'exptype="0" sq="02" href=".*?">(.*?)</a></div></li>', td_list[1], re.S)[0]
                # 分配时间
                assi_name = re.findall(r'<li><span>分配员工：</span>(.*?)</li>', td_list[3], re.S)[0]
                # li_list = re.findall(r'<li>(.*?)</li>', td_list[4], re.S)
                # # 受理方式
                # inner_type = re.findall(r'<span>(.*?)</span>', li_list[4], re.S)[1]
                # # 异常状态
                # inner_abnormal = re.sub(r'(异常状态：|<.*?>)', '', li_list[3], count=0, flags=re.S).strip()
                # 业务类型
                # 异常状态
                inner_abnormal = re.findall(r'<li><span>异常状态：</span>(.*?)</li>', td_list[4], re.S)[0].strip()
                # 订单状态
                order_status = re.findall(r'<li><span>订单状态：</span>(.*?)</li>', td_list[4], re.S)[0].strip()
                                
                busi_type = re.findall(r'<li><span>业务类型：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 订单来源
                order_resource = re.findall(r'<li><span>订单来源：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 客户名称
                cust_name = re.findall(r'<p class="tit">客户名称：(.*?)</p>', td_list[2], re.S)[0]
                # 客户联系方式
                cust_telnum = re.findall(r'<p class="tit">客户联系方式：(.*?)</p>', td_list[2], re.S)[0]
                
                # 受理时间
                assi_time = re.findall(r'<p class="tit">受理时间：(.*?)</p>', td_list[2], re.S)[0]
                # 受理员工
                assi_name = re.findall(r'<p class="tit">受理员工：(.*?)</p>', td_list[2], re.S)[0]
                
                # 传回参数
                # inner_order_list.append([inner_no, cust_name, cust_telnum, assi_time, busi_type, order_resource])
                # print(inner_order_list)
                # print(inner_no, outer_no, assi_time, assi_name, busi_type, order_resource, cust_name, cust_telnum)
                return inner_no, outer_no, assi_time, assi_name, busi_type, order_resource, cust_name, cust_telnum, inner_abnormal, order_status, assi_name
                
        except:
            print("获取内部订单号错误!")
        return None, None, None, None, None, None, None, None, None, None, None
        # return inner_order_list, count



        # try:
        #     s_time = re.findall(r'<p class="tit">受理时间：(.*?)</p>', resp.text, re.S)
        #     dingdan_zt = re.findall(r'<li><span>订单状态：</span>(.*?)</li>', resp.text, re.S)
        #     dingdan_hj = re.findall(r'<li><span>订单环节：</span>(.*?)</li>', resp.text, re.S)
        #     # inner_no=re.search(r'<a name="inner_order_id" order_id="(.*?)"',resp.text,re.S).group(1)
        #     # 取最后一张工单
        #     inner_no = re.findall(r'<a name="inner_order_id" order_id="(.*?)"', resp.text, re.S)
        #     outer_no = re.findall(r'exptype="0" sq="02" href=".*?">(.*?)</a></div></li>', resp.text, re.S)
            
        #     print(outer_no)
        #     print('-' * 38)
        #     print("受理时间:", s_time[-1])
        #     print("订单状态:", dingdan_zt[-1].strip())
        #     print("订单环节:", dingdan_hj[-1].strip())
        #     print("内部订单号:", inner_no[-1])
        #     print("外部订单号:", outer_no[-1])
        #     print('-' * 58)
        #     return inner_no[-1],outer_no[-1],s_time[-1]

        # except:
        #     print("未找到内部订单号!")
        #     return None,None,None

    def get_orderid_by_outid(self, out_tid):   
        create_start=datetime.datetime.now() - datetime.timedelta(hours=720)
        create_start=create_start.strftime('%Y-%m-%d %H:%M:%S')
        create_end=datetime.datetime.today() + datetime.timedelta(hours=2)
        create_end=create_end.strftime('%Y-%m-%d %H:%M:%S')
    
        url="http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do"
        data={
        "btnType": "ordList",
        "params.query_btn_flag": "yes",
        "query_type": "order_view",
        "params.flow_id_c": "",
        "params.flow_id": "",
        "params.trade_eparchy_code_c": "",
        "params.trade_eparchy_code": "",
        "params.trade_depart": "",
        "params.trade_staff_id": "",
        "params.order_from_c": "",
        "params.order_from": "",
        "params.channel_type_c": "",
        "params.channel_type": "",
        "params.tid_category_c": "预开通单",
        "params.busi_type": "A_YKTD",
        "busi_type": "A_YKTD",
        "params.sub_busi_type_c": "", 
        "params.tid_category": "Z29",
        "order_channel": "Z29",
        "params.phone_owner_name": "",
        "params.link_phone": "",
        "params.out_tid": out_tid,
        "params.order_id": "",
        "params.create_start": create_start,
        "params.create_end": create_end,
        "params.lockusername": "",
        "params.status2": "",
        "params.order_is_his": "2",
        "params.order_is_return": "",
        "params.order_is_allot": "",
        "params.serial_num": "",
        "params.foStatusText": "",
        "params.foStatus": "",
        "params.openAccMode": "",
        "params.order_kind": "",
        "query_list_by_bt": "Y",
        "params.cert_card_num": "",
        "username": "",
        "params.lock_user_id": ""
        }

        resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
        if "您尚未登录或登录已经超时" in resp.text:
            print("Cookies已经失效,请重新登录!")
            self.login()
            resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)

        try:
            # <div class="right_warp">
            # 把注释掉的代码删掉
            temp = re.sub(r'<!--.*?-->', '', resp.text, count=0, flags=re.S)
            res = re.search(r'<div class="right_warp">(.*?)<div class="page" >', temp, re.S).group(1)
            # print(res)
            tr_list = re.findall(r'<tr(.*?)</tr>', res, flags=re.S)

            if len(tr_list) >= 2:
                # print("本次查询到 %d 条订单" % count)
                # for x in range(1,len(tr_list)):
                x = len(tr_list)-1
                td_list = re.findall(r'<td(.*?)</td>', tr_list[x], re.S)
                # 内部订单编号
                inner_no = re.findall(r'<a name="inner_order_id" order_id="(.*?)"', td_list[1], re.S)[0]
                outer_no = re.findall(r'exptype="0" sq="02" href=".*?">(.*?)</a></div></li>', td_list[1], re.S)[0]
                # 分配时间
                assi_name = re.findall(r'<li><span>分配员工：</span>(.*?)</li>', td_list[3], re.S)[0]
                # li_list = re.findall(r'<li>(.*?)</li>', td_list[4], re.S)
                # # 受理方式
                # inner_type = re.findall(r'<span>(.*?)</span>', li_list[4], re.S)[1]
                # 异常状态
                inner_abnormal = re.findall(r'<li><span>异常状态：</span>(.*?)</li>', td_list[4], re.S)[0].strip()
                # 订单状态
                order_status = re.findall(r'<li><span>订单状态：</span>(.*?)</li>', td_list[4], re.S)[0].strip()
                  
                # 业务类型
                busi_type = re.findall(r'<li><span>业务类型：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 订单来源
                order_resource = re.findall(r'<li><span>订单来源：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 客户名称
                cust_name = re.findall(r'<p class="tit">客户名称：(.*?)</p>', td_list[2], re.S)[0]
                # 客户联系方式
                cust_telnum = re.findall(r'<p class="tit">客户联系方式：(.*?)</p>', td_list[2], re.S)[0]
                
                # 受理时间
                assi_time = re.findall(r'<p class="tit">受理时间：(.*?)</p>', td_list[2], re.S)[0]
                # 受理员工
                assi_name = re.findall(r'<p class="tit">受理员工：(.*?)</p>', td_list[2], re.S)[0]
                
                # 传回参数
                # inner_order_list.append([inner_no, cust_name, cust_telnum, assi_time, busi_type, order_resource])
                # print(inner_order_list)
                return inner_no, outer_no, assi_time, assi_name, busi_type, order_resource, cust_name, cust_telnum, inner_abnormal, order_status, assi_name
                
        except:
            print("获取内部订单号错误!")
        return None, None, None, None, None, None, None, None, None, None, None
        # return inner_order_list, count



        # try:
        #     s_time = re.findall(r'<p class="tit">受理时间：(.*?)</p>', resp.text, re.S)
        #     dingdan_zt = re.findall(r'<li><span>订单状态：</span>(.*?)</li>', resp.text, re.S)
        #     dingdan_hj = re.findall(r'<li><span>订单环节：</span>(.*?)</li>', resp.text, re.S)
        #     # inner_no=re.search(r'<a name="inner_order_id" order_id="(.*?)"',resp.text,re.S).group(1)
        #     # 取最后一张工单
        #     inner_no = re.findall(r'<a name="inner_order_id" order_id="(.*?)"', resp.text, re.S)
        #     outer_no = re.findall(r'exptype="0" sq="02" href=".*?">(.*?)</a></div></li>', resp.text, re.S)
            
        #     print(outer_no)
        #     print('-' * 38)
        #     print("受理时间:", s_time[-1])
        #     print("订单状态:", dingdan_zt[-1].strip())
        #     print("订单环节:", dingdan_hj[-1].strip())
        #     print("内部订单号:", inner_no[-1])
        #     print("外部订单号:", outer_no[-1])
        #     print('-' * 58)
        #     return inner_no[-1],outer_no[-1],s_time[-1]

        # except:
        #     print("未找到内部订单号!")
        #     return None,None,None

    def get_orderid(self, out_tid='', inner_order_id='', create_start='', create_end=''):
        if create_start == "" or create_end == "":
            create_start=datetime.datetime.now() - datetime.timedelta(hours=720)
            create_start=create_start.strftime('%Y-%m-%d %H:%M:%S')
            create_end=datetime.datetime.today() + datetime.timedelta(hours=2)
            create_end=create_end.strftime('%Y-%m-%d %H:%M:%S')
    
        url="http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do"
        data={
        "btnType": "ordList",
        "params.query_btn_flag": "yes",
        "query_type": "order_view",
        "params.flow_id_c": "",
        "params.flow_id": "",
        "params.trade_eparchy_code_c": "",
        "params.trade_eparchy_code": "",
        "params.trade_depart": "",
        "params.trade_staff_id": "",
        "params.order_from_c": "",
        "params.order_from": "",
        "params.channel_type_c": "",
        "params.channel_type": "",
        "params.tid_category_c": "",
        "params.busi_type": "",
        "busi_type": "",
        "params.sub_busi_type_c": "", 
        "params.tid_category": "",
        "order_channel": "",
        "params.phone_owner_name": "",
        "params.link_phone": "",
        "params.out_tid": out_tid,
        "params.order_id": inner_order_id,
        "params.create_start": create_start,
        "params.create_end": create_end,
        "params.lockusername": "",
        "params.status2": "",
        "params.order_is_his": "2",
        "params.order_is_return": "",
        "params.order_is_allot": "",
        "params.serial_num": "",
        "params.foStatusText": "",
        "params.foStatus": "",
        "params.openAccMode": "",
        "params.order_kind": "",
        "query_list_by_bt": "Y",
        "params.cert_card_num": "",
        "username": "",
        "params.lock_user_id": ""
        }

        resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
        # print(resp.text)

        if "您尚未登录或登录已经超时" in resp.text:
            print("Cookies已经失效,请重新登录!")
            self.login()
            resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
            
        try:
            # <div class="right_warp">
            # 把注释掉的代码删掉
            temp = re.sub(r'<!--.*?-->', '', resp.text, count=0, flags=re.S)
            res = re.search(r'<div class="right_warp">(.*?)<div class="page" >', temp, re.S).group(1)
            # print(res)
            tr_list = re.findall(r'<tr(.*?)</tr>', res, flags=re.S)

            if len(tr_list) >= 2:
                # print("本次查询到 %d 条订单" % count)
                # for x in range(1,len(tr_list)):
                x = len(tr_list)-1
                td_list = re.findall(r'<td(.*?)</td>', tr_list[x], re.S)
                # 内部订单编号
                inner_no = re.findall(r'<a name="inner_order_id" order_id="(.*?)"', td_list[1], re.S)[0]
                outer_no = re.findall(r'exptype="0" sq="02" href=".*?">(.*?)</a></div></li>', td_list[1], re.S)[0]
                # 分配时间
                assi_name = re.findall(r'<li><span>分配员工：</span>(.*?)</li>', td_list[3], re.S)[0]
                # li_list = re.findall(r'<li>(.*?)</li>', td_list[4], re.S)
                # # 受理方式
                # inner_type = re.findall(r'<span>(.*?)</span>', li_list[4], re.S)[1]
                # 异常状态
                inner_abnormal = re.findall(r'<li><span>异常状态：</span>(.*?)</li>', td_list[4], re.S)[0].strip()
                # 订单状态
                order_status = re.findall(r'<li><span>订单状态：</span>(.*?)</li>', td_list[4], re.S)[0].strip()
                  
                # 业务类型
                busi_type = re.findall(r'<li><span>业务类型：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 订单来源
                order_resource = re.findall(r'<li><span>订单来源：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 客户名称
                cust_name = re.findall(r'<p class="tit">客户名称：(.*?)</p>', td_list[2], re.S)[0]
                # 客户联系方式
                cust_telnum = re.findall(r'<p class="tit">客户联系方式：(.*?)</p>', td_list[2], re.S)[0]
                
                # 受理时间
                assi_time = re.findall(r'<p class="tit">受理时间：(.*?)</p>', td_list[2], re.S)[0]
                # 受理员工
                assi_name = re.findall(r'<p class="tit">受理员工：(.*?)</p>', td_list[2], re.S)[0]
                
                # 传回参数
                # inner_order_list.append([inner_no, cust_name, cust_telnum, assi_time, busi_type, order_resource])
                # print(inner_order_list)
                return inner_no, outer_no, assi_time, assi_name, busi_type, order_resource, cust_name, cust_telnum, inner_abnormal, order_status, assi_name
                
        except:
            print("获取内部订单号错误!")
        return None, None, None, None, None, None, None, None, None, None, None
        # return inner_order_list, count



        # try:
        #     s_time = re.findall(r'<p class="tit">受理时间：(.*?)</p>', resp.text, re.S)
        #     dingdan_zt = re.findall(r'<li><span>订单状态：</span>(.*?)</li>', resp.text, re.S)
        #     dingdan_hj = re.findall(r'<li><span>订单环节：</span>(.*?)</li>', resp.text, re.S)
        #     # inner_no=re.search(r'<a name="inner_order_id" order_id="(.*?)"',resp.text,re.S).group(1)
        #     # 取最后一张工单
        #     inner_no = re.findall(r'<a name="inner_order_id" order_id="(.*?)"', resp.text, re.S)
        #     outer_no = re.findall(r'exptype="0" sq="02" href=".*?">(.*?)</a></div></li>', resp.text, re.S)
            
        #     print(outer_no)
        #     print('-' * 38)
        #     print("受理时间:", s_time[-1])
        #     print("订单状态:", dingdan_zt[-1].strip())
        #     print("订单环节:", dingdan_hj[-1].strip())
        #     print("内部订单号:", inner_no[-1])
        #     print("外部订单号:", outer_no[-1])
        #     print('-' * 58)
        #     return inner_no[-1],outer_no[-1],s_time[-1]

        # except:
        #     print("未找到内部订单号!")
        #     return None,None,None

    def get_detail_by_inner(self, inner_no):
        create_start=datetime.datetime.now() - datetime.timedelta(days=66)
        create_start=create_start.strftime('%Y-%m-%d %H:%M:%S')
        create_end=datetime.datetime.today() + datetime.timedelta(hours=2)
        create_end=create_end.strftime('%Y-%m-%d %H:%M:%S')

        url = "http://133.96.12.18:10005/shop/admin/ordAuto!showOrderList.do"
        data={
            "btnType": "ordList",
            "params.query_btn_flag": "yes",
            "query_type": "order_view",
            "params.flow_id_c": "",
            "params.flow_id": "",
            "params.trade_eparchy_code_c": "",
            "params.trade_eparchy_code": "",
            "params.trade_depart": "",
            "params.trade_staff_id": "",
            "params.order_from_c": "",
            "params.order_from": "",
            "params.channel_type_c": "",
            "params.channel_type": "",
            "params.phone_owner_name": "",
            "params.link_phone": "",
            "params.tid_category_c": "",
            "params.tid_category": "",
            "order_channel": "",
            "params.out_tid": "",
            "params.order_id": inner_no,
            "params.create_start": create_start,
            "params.create_end": create_end,
            "params.lockusername": "",
            "params.status2": "",
            "params.order_is_his": "2",
            "params.order_is_return": "",
            "params.order_is_allot": "",
            "params.serial_num": "",
            "params.foStatusText": "",
            "params.foStatus": "",
            "params.openAccMode": "",
            "params.order_kind": "",
            "query_list_by_bt": "Y",
            "params.cert_card_num": "",
            "username": "",
            "params.lock_user_id": ""
        }

        resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
        if "您尚未登录或登录已经超时" in resp.text:
            print("Cookies已经失效,请重新登录!")
            self.login()
            resp=requests.post(url=url, data=data, cookies=self.dict_cookie, verify=False)
        
        try:
            print(resp.text)
            # <div class="right_warp">
            # 把注释掉的代码删掉
            temp = re.sub(r'<!--.*?-->', '', resp.text, count=0, flags=re.S)
            res = re.search(r'<div class="right_warp">(.*?)<div class="page" >', temp, re.S).group(1)
            # print(res)
            tr_list = re.findall(r'<tr(.*?)</tr>', res, flags=re.S)
            if len(tr_list) == 2:
            # print("本次查询到 %d 条订单" % count)
            # for x in range(1,len(tr_list)):
                x=1
                td_list = re.findall(r'<td(.*?)</td>', tr_list[x], re.S)
                # 内部订单编号
                inner_no = re.findall(r'<a name="inner_order_id" order_id="(.*?)"', td_list[1], re.S)[0]
                outer_no = re.findall(r'exptype="0" sq="02" href=".*?">(.*?)</a></div></li>', td_list[1], re.S)
                # 分配员工
                assi_name = re.findall(r'<li><span>分配员工：</span>(.*?)</li>', td_list[3], re.S)[0]
                # li_list = re.findall(r'<li>(.*?)</li>', td_list[4], re.S)
                # # 受理方式
                # inner_type = re.findall(r'<span>(.*?)</span>', li_list[4], re.S)[1]
                # # 异常状态
                # inner_abnormal = re.sub(r'(异常状态：|<.*?>)', '', li_list[3], count=0, flags=re.S).strip()
                # 业务类型
                busi_type = re.findall(r'<li><span>业务类型：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 订单来源
                order_resource = re.findall(r'<li><span>订单来源：</span><div>(.*?)</div></li>', td_list[1], re.S)[0]
                # 客户名称
                cust_name = re.findall(r'<p class="tit">客户名称：(.*?)</p>', td_list[2], re.S)[0]
                # 客户联系方式
                cust_telnum = re.findall(r'<p class="tit">客户联系方式：(.*?)</p>', td_list[2], re.S)[0]
                # 受理时间
                assi_time = re.findall(r'<p class="tit">受理时间：(.*?)</p>', td_list[3], re.S)[0]
                # 传回参数
                # inner_order_list.append([inner_no, cust_name, cust_telnum, assi_time, busi_type, order_resource])
                # print(inner_order_list)
                # return [inner_no, outer_no, assi_time, assi_name, busi_type, order_resource, cust_name, cust_telnum]
                ret_lst = [inner_no, outer_no, assi_time, assi_name, busi_type, order_resource, cust_name, cust_telnum]
                ret_text = ",".join(ret_lst)
                print(ret_text)
                return ret_text

        except:
            print("获取内部订单号错误!")
            return None
        # return inner_order_list, count

    # 通过外部单号获取装维电话
    def get_phone_by_outer_no(self, outer_no):
        try:
            url = "http://133.96.12.18:10005/shop/admin/ordAuto!getOrderYdkq.do"
            data = {
                "params.query_btn_flag": "yes",
                "params.order_id": outer_no
            }
            resp = requests.post(url=url, data=data, headers=self.headers, cookies=self.dict_cookie, verify=False)
            inner_no = re.search(r'queryPreIOMProcessLogs.do\?ajax=yes&localNetId=0310&order_id=(.*?)"', resp.text, flags=0).group(1)
            
            url = "http://133.96.12.18:10005/shop/admin/ordAuto!queryPreIOMProcessLogs.do?ajax=yes&localNetId=0310&order_id=" + inner_no
            resp = requests.post(url=url, headers=self.headers, cookies=self.dict_cookie, verify=False)
            for l in resp.json():
                if l["StepName"] in ("外线施工(装)", " 源核配"):
                    return (l["WoStaffName"], l["WoStaffPhone"])
            return None
        except Exception:
            return None

    # 发送短信
    def send_sms(self):
        url = "http://133.96.12.18:10005/shop/admin/shop/admin/orderFlowAction!sendMessage.do?ajax=yes"
        data = {"_sendMessageType": "1", "order_id": self.dict_order['内部订单编号']}
        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("发送短信结果:")
        print(resp.text)

    # 转派沃掌通
    def send_to_wzt(self, staffname, staffid, staffphone):
        url = "http://133.96.12.18:10005/shop/admin/shop/admin/orderFlowAction!sendData2WZT.do?ajax=yes"
        data = {
            "_staffName": staffname,
            "_staffId": staffid,
            "_level": "undefined",
            "_2WZTRemark": self.dict_order['remarks'],
            "order_id": self.dict_order['内部订单编号'],
            "addr_id": self.dict_order['addr_id'],
            "addr6": self.dict_order['addr_id'],
            "_staffPhone": staffphone,
            "_is_mob": "undefined",
            "_app_tag": "undefined"
        }
        resp = requests.post(url=url,
                             data=data,
                             headers=self.headers,
                             cookies=self.dict_cookie,
                             verify=False)
        print("发送沃掌通结果:")
        print(resp.text)


if __name__ == "__main__":
    pass