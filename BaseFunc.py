#! /usr/bin/env python3
import requests
import re
from functools import wraps
import prettytable as pt
import pandas
import base64
import time
import os

# json 转 geturlparams参数
def jsonDataToCookiesParams(params_data):
    strParams = ""
    nums = 0
    max_nums = len(params_data)
    for key in params_data:
        nums = nums + 1
        if nums == max_nums:
            strParams += str(key) + '=' + str(params_data[key])
        else:
            strParams += str(key) + '=' + str(params_data[key]) + '&'
    return str(strParams)


# 设置输入背景文字颜色
def setColor(B_color, F_color):
    import ctypes
 
    STD_INPUT_HANDLE = -10 
    STD_OUTPUT_HANDLE= -11 
    STD_ERROR_HANDLE = -12 
    
    # F_BLACK = 0x00
    # F_BLUE = 0x01
    # F_GREEN = 0x02
    # F_SKYBLUE = 0x03
    # F_RED = 0x04
    # F_VIOLET = 0x05
    # F_YELLOW = 0x06
    # F_WHITE = 0x07
    # F_GRAY = 0x08
    # F_HBLUE = 0x09
    # F_HGREEN = 0x0A
    # F_HSKYBLUE = 0x0B
    # F_HRED = 0x0C
    # F_HVIOLET = 0x0D
    # F_HYELLOW = 0x0E
    # F_HWHITE = 0x0F
    
    # B_BLACK = 0x00
    # B_BLUE = 0x10
    # B_GREEN = 0x20
    # B_SKYBLUE = 0x30
    # B_RED = 0x40
    # B_VIOLET = 0x50
    # B_YELLOW = 0x60
    # B_WHITE = 0x70
    # B_GRAY = 0x80
    # B_HBLUE = 0x90
    # B_HGREEN = 0xA0
    # B_HSKYBLUE = 0xB0
    # B_HRED = 0xC0
    # B_HVIOLET = 0xD0
    # B_HYELLOW = 0xE0
    # B_HWHITE = 0xF0
    std_out_handle=ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    Bool=ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, B_color|F_color)
    return Bool

# 写入文件
def write_file_with_txt(file, text):
    with open(file, mode="a+", encoding="utf-8") as f:
        f.write(text)

# 获取文件与现在时间间隔(分钟)
def get_file_last_modify_leave_now(file):
    filetime = os.path.getmtime(file)
    return (time.time() - filetime) / 60

# 将str分行，每行num个char
def cut_str(str, num):
    n = len(str) // num
    s = ''
    for x in range(n):
        s = s + str[num*x:num*(x+1)] + "\n"
    s = s + str[num*n:]
    return s


# 判断所有入参类型是否一致,并且为t
def is_type(t):
    def __f(func):
        @wraps(func)
        def _f(*args, **kwargs):
            for _t in args:
                try:
                    assert type(_t) is t
                except Exception:
                    print("入参 %s 不是 %s 类型" % (_t, t))
                    return False
            return func(*args, **kwargs)
        return _f
    return __f


# 打印 df
@is_type(t=pandas.core.frame.DataFrame)
def print_df(df):
    table = pt.PrettyTable()
    
    table.field_names = list(df)
    for row in df.values.tolist():
        table.add_row(row)
    
    table.align = 'l'
    table.left_padding_width = 0
    print(table)


# 打印 pt表格
@is_type(t=list)
def print_pt(*args, **kwargs):
    list_len = len(args)
    if list_len == 0:
        print("入参不能为空，列表长度需要一致!")
        return

    table = pt.PrettyTable()
    for _x in range(list_len):
        if _x == 0:
            _tiltelen = len(args[_x])
            table.field_names = args[_x]
        else:
            if len(args[_x]) != _tiltelen:
                print("所有入参列表长度必须一致!")
                return
            table.add_row(args[_x])
    table.align = 'l'
    table.valign = 't'
    table.left_padding_width = 0
    table.set_style(pt.DEFAULT)
    if "head" in kwargs.keys() and kwargs["head"] is not True:
        table.header = False
    print(table)


# 打印字典
def print_dict(type=''):
    def __f(func):
        @wraps(func)
        def _f(*args, **kwargs):
            if len(type) > 0:
                print(type)
            for x in args:
                for k, v in x.items():
                    print('\t', k, ":", v)
            return func(*args, **kwargs)
        return _f
    return __f


@print_dict()
def input_choise(dict):
    while True:
        choise = input("请输入:").upper()
        if len(choise) == 0:
            if "Y" in dict.keys():
                choise = "Y"
            elif "1" in dict.keys():
                choise = "1"
        if choise in dict.keys():
            print("您的选择是:", dict[choise])
            print('*' * 38)
            return choise


# 划块验证码缺口查找
def identify_gap(bg, tp):
    '''

    bg: 背景图片

    tp: 缺口图片

    out:输出图片

    '''

    # 读取背景图片和缺口图片

    bg_img = cv2.imread(bg)  # 背景图片

    tp_img = cv2.imread(tp)  # 缺口图片

    # cv2.imshow("tp_img", tp_img)

    # input()

    # 识别图片边缘

    bg_edge = cv2.Canny(bg_img, 75, 100)

    tp_edge = cv2.Canny(tp_img, 75, 100)

    # cv2.imwrite("bg.png", bg_edge) # 保存在本地

    # cv2.imwrite("tp.png", tp_edge) # 保存在本地

    # 转换图片格式

    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)

    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # cv2.imwrite("bg.png", bg_pic) # 保存在本地

    # cv2.imwrite("tp.png", tp_img) # 保存在本地

    # 缺口匹配

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)

    _, _, _, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

    # min_val, max_val, min_loc, max_loc = cv2. # 寻找最优匹配

    # 绘制方框

    # th, tw = tp_img.shape[:2]

    # tl = max_loc # 左上角点的坐标

    # # print(tl)

    # br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标

    # cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形

    # cv2.imwrite(out, bg_img) # 保存在本地

    # 返回缺口的X坐标

    return max_loc[0]


# 去重空行和重复行
def del_mult(file):
    list_out = []
    for i in open(file, encoding='utf-8'):
        if i in list_out or len(i) <= 1:
            continue
        list_out.append(i)
    with open(file, 'w', encoding='utf-8') as handle:
        handle.writelines(list_out)


def check_allow():

    url = "http://10.49.181.186:9090/"
    try:
        resp = requests.get(url)
        if resp.text == "OK":
            return True
        else:
            return False
    except Exception:
        return False


# 编码转为utf8
def toutf8(str):

    str = re.sub(r"\n|\r", "", str, re.S)

    re_str = ""

    while len(str) > 0:

        if str[:2] == "&#":

            re_str = re_str + chr(int(str[2:7]))

            str = str[8:]

        else:

            i = str.find("&#")

            if i > 0:

                re_str = re_str + str[:str.find("&#")]

                str = str[str.find("&#"):]

            else:

                re_str = re_str + str

                str = ""

    return re_str


# 通过地址转换服务区
def get_area(str):
    if '成安' in str:
        return '成安分公司'
    elif '磁县' in str:
        return '磁县分公司'
    elif '大名' in str:
        return '大名分公司'
    elif '肥乡' in str:
        return '肥乡分公司'
    elif '峰峰' in str:
        return '峰峰分公司'
    elif '管陶' in str or '馆陶' in str:
        return '馆陶分公司'
    elif '广平' in str:
        return '广平分公司'
    elif '鸡泽' in str:
        return '鸡泽分公司'
    elif '临漳' in str:
        return '临漳分公司'
    elif '邱县' in str:
        return '邱县分公司'
    elif '曲周' in str:
        return '曲周分公司'
    elif '涉县' in str:
        return '涉县分公司'
    elif '魏县' in str:
        return '魏县分公司'
    elif '武安' in str:
        return '武安分公司'
    elif '永年' in str:
        return '永年分公司'
    elif '冀南新区' in str:
        return '磁县分公司'
    else:
        return '市分公司'


# 全角字符转为半角字符
def strQ2B(ustring):
    """全角字符转为半角字符"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring


# 打印调试出错信息
def except_err(e):
    print('出错文件:', e.__traceback__.tb_frame.f_globals['__file__'])
    print('出错行号:', e.__traceback__.tb_lineno)
    print('出错内容:', e)


# 判断输入是否为Ctrl+r，中断
def get_interrupt_key_ctrl_r(timeout):

    from pynput import keyboard
    import time

    a = time.time()
    with keyboard.Events() as events:
        event = events.get(timeout)
    if event is None:
        return False
    elif event.key is keyboard.Key.ctrl_r:
        return True
    else:
        b = time.time()
        time.sleep(timeout - b + a)
        return False


# 检查str里是否包含一组关键字里的任一，含任一返回true，否则返回false
def does_str_contains_any_key(str, key_list):
    for key in key_list:
        if key in str:
            return True
    return False


# 检查str里是不否包含一组关键字里的任一，不含任一返回true，含任一返回false
def does_str_not_contains_any_key(str, key_list):
    for key in key_list:
        if key in str:
            return False
    return True


# 检查str里是包含一组关键字里的所有，包含所有返回true，否则返回false
def does_str_contains_all_key(str, key_list):
    for key in key_list:
        if key not in str:
            return False
    return True


# 通过baidu ocr 获取验证码
def get_captcha_by_baidu_ocr(pic_url):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = "i1j3ShzGEzHBGyfzh8IdmQeG"
    client_secret = "srKWWKEw4KGnPph2ivX0vX2GSpzrVRsN"
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(host)
    if response:
        access_token = response.json()['access_token']

    requrest_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    f = open(pic_url, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    request_url = requrest_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    
    if response:
        words_result = response.json()['words_result']
        # print(words_result)
        if len(words_result) == 0:
            return ""
        else:
            return re.sub(' ', '', words_result[0]['words'])
    else:
        return "Requests Error"

if __name__ == "__main__":
    pass
