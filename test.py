from selenium.webdriver.common.by import By

from WebUi import WebBrowser
import time

w = WebBrowser("Firefox")
w.open("https://m.10010.com/scaffold-show/push/18Nsm4M1Kjd")

time.sleep(3)
print("Go")
w.click_js((By.CSS_SELECTOR, "#deliverychoose"))
time.sleep(1)
w.click_js((By.XPATH, "//li[text()='河北']"))
time.sleep(1)
w.click_js((By.XPATH, "//li[text()='邯郸市']"))
time.sleep(1)
w.click_js((By.XPATH, "//li[text()='邱县']"))
# w.click_js((By.CSS_SELECTOR, "#deliverychoose"))
w.send_key((By.CSS_SELECTOR, "#address"), "详111111111详")
w.send_key((By.CSS_SELECTOR, "#certName"), "详111111111详")
w.send_key((By.CSS_SELECTOR, "#certNo"), "certNo")
w.send_key((By.CSS_SELECTOR, "#mobilePhone"), "mobilePhone")
w.click_js((By.CSS_SELECTOR, "#submitBtn"))

err_keys = ['请输入正确的身份证号', '详细地址太短', '姓名必须至少包含2个汉字']
for err_key in err_keys:
    if w.is_page_contains(err_key):
        print(err_key)

if w.is_page_contains("成功"):
    print("录入成功")


# 详细地址太短
# 姓名必须至少包含2个汉字
# 请输入正确的身份证号
""