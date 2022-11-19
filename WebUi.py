#! /usr/bin/env python3
from BaseFunc import except_err
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  # 处理鼠标事件
from selenium.webdriver.support.select import Select  # 用于处理下拉框
from selenium.common.exceptions import TimeoutException  # 用于处理异常
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
# from PIL import Image, ImageEnhance
import time


class WebBrowser(object):
    def __init__(self, browser="IE", mode=False, remote_addr=''):
        # 打开浏览器
        if browser in ["ie", "IE", "Ie"]:
            ie_options = webdriver.IeOptions()
            # 控制显示页面
            # ie_options.ensure_clean_session = True
            ie_options.add_argument('--disable-gpu')
            ie_options.add_argument('--no-sandbox')
            ie_options.add_argument('--disable-dev-shm-usage')
            # ie_options.add_argument('--inprivate')
            # 是否加载图片连接
            ie_options.add_argument('blink-settings=imagesEnabled=false')
            # return webdriver.Ie(options=ie_options)
            self.driver = webdriver.Ie(options=ie_options)  # Alt+Enter

        elif browser in ["Chrome", "chrome"]:
            chrome_options = webdriver.ChromeOptions()
            if mode is True:
                chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--window-size=1024x768')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--incognito')
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--allow-insecure-localhost')
            # chrome_options.add_argument('--proxy-server=socks5://172.18.0.1:10808')
            self.driver = webdriver.Chrome(options=chrome_options)  # Alt+Enter
            self.driver = webdriver.Remote(command_executor=remote_addr,desired_capabilities=chrome_options.to_capabilities())
        
        elif browser in ["Firefox", "firefox", "FireFox"]:
            firefox_options = webdriver.FirefoxOptions()
            if mode is True:
                firefox_options.add_argument('--headless')
            firefox_options.add_argument('--disable-gpu')
            firefox_options.add_argument('--incognito')
            firefox_options.add_argument('--ignore-ssl-errors=yes')
            firefox_options.add_argument('--ignore-certificate-errors')
            firefox_options.add_argument('--allow-insecure-localhost')
            # profile_driectory = r'./i3snwly4.workprofile'
            # profile = webdriver.FirefoxProfile(profile_driectory)
            # self.driver = webdriver.Firefox(firefox_profile=profile, options=firefox_options)  # Alt+Enter
            
            self.driver = webdriver.Firefox(options=firefox_options)
            

    def set_implicitly_wait(self, wait):
        self.driver.implicitly_wait(wait)

    def open(self, url, title='', timeout=10):
        u"""打开浏览器，并最大化，判断title是否为预期"""
        self.driver.get(url)
        # self.driver.maximize_window()
        try:
            WebDriverWait(self.driver, timeout,
                          1).until(EC.title_contains(title))
        except TimeoutException:
            print("open %s title error" % url)
        except Exception as msg:
            print("Error:%s" % msg)

    def find_element(self, locator, timeout=10):
        u"""定位元素，参数locator为原则"""
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(
                EC.presence_of_element_located(locator))
            return element
        except Exception:
            # print("%s 未找到元素 %s" % (self,locator))
            return None

    def is_find_element(self, locator, timeout=10):
        u"""定位元素，参数locator为原则"""
        try:
            if WebDriverWait(self.driver, timeout,
                             1).until(EC.presence_of_element_located(locator)):
                return True
        except Exception:
            # print("%s 未找到元素 %s" % (self,locator))
            return False

    def find_elements(self, locator, timeout=10):
        u"""定位一组元素"""
        try:
            elements = WebDriverWait(self.driver, timeout, 1).until(
                EC.presence_of_all_elements_located(locator))
            return elements
        except Exception:
            return None

    def click(self, locator, timeout=10):
        u"""封装点击操作,找到了执行点击并返回True,没找到返回False"""
        try:
            element = self.find_element(locator, timeout)
            if element is None:
                return False
            element.click()
            return True
        except Exception:
            return False

    def click_js(self, locator, timeout=10):
        u"""封装点击操作,找到了执行点击并返回True,没找到返回False"""
        try:
            element = self.find_element(locator, timeout)
            if element is None:
                return False
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception:
            return False

    def send_key(self, locator, text, flag=True):
        u"""发送文本后清除内容"""
        element = self.find_element(locator)
        if flag is True:
            element.clear()
        element.send_keys(text)

    def is_text_in_element(self, locator, text, timeout=10):
        u"""判断是否定位到元素"""
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(
                EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            print
            u"元素未定位到:" + str(locator)
            return False
        else:
            return result

    def is_title(self, title, timeout=10):
        u"""判断title完全相等"""
        result = WebDriverWait(self.driver, timeout,
                               1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        u"""判断是否包含title"""
        result = WebDriverWait(self.driver, timeout,
                               1).until(EC.title_contains(title))
        return result

    def is_page_contains(self, text):
        u"""判断页面包含text"""
        if text in self.driver.page_source:
            return True
        else:
            return False

    def is_select(self, locator, timeout=10):
        u"""判断元素是否被选中"""
        result = WebDriverWait(self.driver, timeout, 1).until(
            EC.element_located_to_be_selected(locator))
        return result

    def is_select_be(self, locator, timeout=10, selected=True):
        u"""判断元素的状态"""
        try:
            if WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(locator, selected)):
                return True
        except Exception:
            pass
        return False

    def is_alert_present(self, timeout=10):
        u"""判断页面有无alert弹出框，有alert返回alert，无alert返回FALSE"""
        try:
            return WebDriverWait(self.driver, timeout,
                                 1).until(EC.alert_is_present())
        except Exception:
            print("No Alert Present")

    def is_visibility(self, locator, timeout=10):
        u"""判断元素是否可见，可见返回本身，不可见返回FALSE"""
        try:
            if WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locator)):
                return True
        except Exception:
            pass
        return False

    def is_invisibility(self, locator, timeout=10):
        u"""判断元素是否可见，不可见，未找到元素返回True"""
        try:
            if WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(locator)):
                return True
        except Exception:
            pass
        return False
        
    def is_clickable(self, locator, timeout=10):
        u"""判断元素是否可以点击，可以点击返回本身，不可点击返回FALSE"""
        return WebDriverWait(self.driver, timeout,
                             1).until(EC.element_to_be_clickable(locator))

    def is_located(self, locator, timeout=10):
        u"""判断元素是否定位到（元素不一定是可见），如果定位到返回Element，未定位到返回FALSE"""
        return WebDriverWait(self.driver, timeout,
                             1).until(EC.presence_of_element_located(locator))

    def switch_available_to(self, locator, timeout=10):
        u"""判断frame是否可以切入,可以切入就切进去"""
        return WebDriverWait(self.driver, timeout, 1).until(
            EC.frame_to_be_available_and_switch_to_it(locator))
    
    def switch_to_frame_list(self, frame_list, default, timeout=10):
        u"""安层级依次进入一组frame,frame_list是由#ID按层级组成的列表"""
        if default:
            self.switch_to_default()
        for frame in frame_list:
            locator = (By.CSS_SELECTOR, "#%s" % frame)
            self.switch_available_to(locator, timeout)

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    def switch_to_parent(self):
        self.driver.switch_to.parent_frame()

    def move_is_element(self, locator):
        u"""鼠标悬停操作"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def back(self):
        u"""返回到旧的窗口"""
        self.driver.back()

    def forward(self):
        u"""前进到新窗口"""
        self.driver.forward()

    def close(self):
        u"""关闭窗口"""
        self.driver.close()

    def quit(self):
        u"""关闭driver和所有窗口"""
        self.driver.quit()

    def get_title(self):
        u"""获取当前窗口的title"""
        return self.driver.title

    def get_current_url(self):
        u"""获取当前页面url"""
        return self.driver.current_url

    def get_text(self, locator, timeout=10):
        u"""获取文本内容"""
        return self.find_element(locator, timeout=timeout).text

    def get_browser_log_level(self):
        u"""获取浏览器错误日志级别"""
        lists = self.driver.get_log('browser')
        list_value = []
        if lists.__len__() != 0:
            for dicts in lists:
                for key, value in dicts.items():
                    list_value.append(value)
        if 'SEVERE' in list_value:
            return "SEVERE"
        elif 'WARNING' in list_value:
            return "WARNING"
        return "SUCCESS"

    def get_attribute(self, locator, attr, timeout=10):
        u"""获取属性"""
        try:
            return self.find_element(locator, timeout=timeout).get_attribute(attr)
        except Exception:
            return ''

    def is_ele_attr_value_equle(self, locator, attr, value, timeout=10):
        u"""元素是某属性值是否与提供的相等"""
        try:
            if self.find_element(locator,
                                 timeout=timeout).get_attribute(attr) == value:
                return True
            return False
        except Exception:
            return False

    def is_ele_text_equle(self, locator, text, timeout=10):
        u"""元素是text是否与提供的相等"""
        try:
            if self.get_text(locator) == text:
                return True
            return False
        except Exception:
            return False

    def is_ele_text_has_value(self, locator, timeout=10):
        u"""元素是否text,并且不为空"""
        try:
            if len(self.get_text(locator)) > 0:
                return True
            return False
        except Exception:
            return False

    def is_ele_has_attr_value(self, locator, attr, timeout=10):
        u"""元素是否包含某属性,并且取值不为空"""
        try:
            if len(
                    self.find_element(
                        locator, timeout=timeout).get_attribute(attr)) > 0:
                return True
            return False
        except Exception:
            return False

    def js_execute(self, js):
        u"""执行js"""
        return self.driver.execute_script(js)

    def js_fours_element(self, locator):
        u"""聚焦元素"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def js_scroll_top(self):
        u"""滑动到页面顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        u"""滑动到页面底部"""
        js = "window.scrollTo(0, document.body.scrollHeight)"
        self.driver.execute_script(js)

    def select_by_index(self, locator, index):
        u"""通过所有index，0开始,定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        u"""通过value定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        u"""通过text定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text)

    def click_verify(self,
                     func_click,
                     func_verify,
                     func_check,
                     f_click_args=dict(),
                     f_verify_args=dict(),
                     times=5,
                     wait_seconds=3):
        u"""验证点击是否成功,默认3次,成功返回True,失败返回False,停留wait_seconds再次尝试,尝试次数times,func_check为验证出错窗口的程序"""
        for _ in range(times):
            try:
                if func_click(**f_click_args) is False:
                    time.sleep(wait_seconds)
                    continue
                time.sleep(0.5)
                if func_verify(**f_verify_args):
                    return True
                else:
                    if func_check is not None:
                        if func_check():
                            return False
            except Exception as err:
                except_err(err)
                if func_check is not None:
                    if func_check():
                        return False
        return False

    def screen_to_file(self, file):
        u"""保存当前截图到文件"""
        self.driver.get_screenshot_as_file(file)


if __name__ == "__main__":
    pass
