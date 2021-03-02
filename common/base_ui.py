# -*- coding: utf-8 -*-

import traceback
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from common.operation_log import logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


class BaseUI():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.log = logger()
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)     # 鼠标事件
        # self.driver.implicitly_wait(10)
        self.driver.get(r'https://www.runoob.com/try/try.php?filename=tryjs_alert')
        self.timeOut = 0.5          # 显示等待超时时间
        self.pollTime = 0.1         # 显示等待轮询时间

    def according_wait(self, method):
        """
        显示等待
        :param method: 显示等待until方法所需的对象
        :return:WebDriverWait对象
        """
        try:
            return WebDriverWait(self.driver, self.timeOut, self.pollTime).until(method)
        except TimeoutException:
            self.log.info('在显示等待，或隐式等待中，查找元素超时，也就是找不到元素' )
            return False
        except Exception:
            self.log.error(traceback.format_exc())


    def find_element(self, locator):
        """
        查找可见元素
        :param locator: 要求传入的参数是一个元组，表示元素定位方法和表达式。如(By.XPATH, "//*[@text='照片']")
        :return: 返回可见元素对象
        """
        if not isinstance(locator, tuple):
            self.log.error(f'locator参数{locator}必须是元组类型，而不是：{type(locator)}')
        else:
            return self.according_wait(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        """
        查找可见元素
        :param locator: 要求传入的参数是一个元组，表示元素定位方法和表达式。如(By.XPATH, "//*[@text='照片']")
        :return: 返回可见元素列表
        """
        if not isinstance(locator, tuple):
            self.log.error(f'locator参数{locator}必须是元组类型，而不是：{type(locator)}')
        else:
            return self.according_wait(EC.visibility_of_any_elements_located(locator))

    def click(self, locator):
        """点击操作"""
        self.find_element(locator).click()

    def submit(self, locator):
        """查找到表单（from）直接调用submit"""
        self.find_element(locator).submit()

    def clear(self, locator):
        """清空输入框内容"""
        self.find_element(locator).clear()

    def send_keys(self, locator, text):
        """发送文本，清空后输入"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def back(self):
        """返回之前的网页"""
        self.driver.back()

    def forward(self):
        """前往下一个网页"""
        self.driver.forward()

    def close(self):
        """关闭当前网页"""
        self.driver.close()

    def quit(self):
        """关闭所有网页"""
        self.driver.quit()

    def get_texts(self, locator, n):
        """获取一组相同元素中的指定文本"""
        return (self.find_elements(locator)[n]).text

    def get_text(self, locator):
        """获取文本"""
        return self.find_element(locator).text

    def get_attribute(self, locator, name):
        """获取属性"""
        return self.find_element(locator).get_attribute(name)

    def get_title(self):
        """获取当前页面title"""
        return self.driver.title

    def value_of_css_property(self, locator):
        """
        获取CSS的属性值
        :param locator: locator元素定位方法必须为CSS，(By.CSS_SELECTOR, "//*[@text='照片']")
        :return:
        """
        return self.find_element(locator).value_of_css_property(locator)

    def get_cookies(self):
        """获取cookies"""
        return self.driver.get_cookies()

    def add_cookie(self,cookie):
        """添加cookie"""
        self.driver.add_cookie(cookie)

    def delete_all_cookies(self):
        """删除浏览器所有的cookies"""
        return self.driver.delete_all_cookies()

    def delete_cookie(self,cookie):
        """删除指定的cookie"""
        self.driver.delete_cookie(cookie)

    def tag_name(self, locator):
        """返回元素的tagName"""
        return self.find_element(locator).tag_name

    def size(self, locator):
        """获取元素的大小"""
        return self.find_element(locator).size

    def location(self, locator):
        """获取元素坐标"""
        return self.find_element(locator).location

    def get_window_position(self):
        """获取当前窗口的坐标"""
        return self.driver.get_window_position()

    def get_window_size(self):
        """获取当前窗口的长和宽"""
        return self.driver.get_window_size()

    def select_by_index(self, locator, index):
        """通过索引，index是第几个，从0开始, 下拉框"""
        Select(self.find_element(locator)).select_by_index(index)

    def select_by_value(self, locator, value):
        """通过value属性"""
        Select(self.find_element(locator)).select_by_value(value)

    def select_by_text(self, locator, text):
        """通过text属性"""
        Select(self.find_element(locator)).select_by_visible_text(text)

    def save_screenshot(self, imgPath):
        """
        获取电脑屏幕截屏
        :param imgPath: 截图存放路径
        :return:
        """
        self.driver.save_screenshot(imgPath)

    def save_report_html(self):
        """可以在html报告中使用的截图"""
        self.driver.get_screenshot_as_base64()

    def current_url(self):
        """获取当前页面URl"""
        return self.driver.current_url

    def current_window_handle(self):
        """浏览器handle"""
        return self.driver.current_window_handle

    def open_new_window(self, url):
        """
        打开新窗口
        :param url: 新窗口打开的页面URL
        :return:
        """
        self.driver.execute_script(f'window.open("{url}")')

    def switch_window_handle(self, n):
        """切换handle"""
        if not isinstance(n, int):
            self.driver.switch_to.window(n)
        else:
            self.driver.switch_to.window(self.driver.window_handles[n])

    def js_execute(self, js):
        """执行js"""
        return self.driver.execute_script(js)

    def js_focus_element(self, locator):
        """聚焦元素"""
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(locator))

    def js_scroll_top(self):
        """滚动到顶部"""
        self.driver.execute_script("var q=document.documentElement.scrollTop=0")

    def js_scroll_bottom(self):
        """滚动到底部"""
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")

    def double_click(self, locator):
        """双击鼠标左键操作"""
        self.action.double_click(self.find_element(locator)).perform()

    def context_click(self, locator):
        """点击鼠标右键操作"""
        self.action.context_click(self.find_element(locator)).perform()

    def move_to_element(self, locator):
        """鼠标悬停操作"""
        self.action.move_to_element(self.find_element(locator)).perform()

    def drag_and_drop(self, locator, locator1):
        """将元素dragger拖拽指定元素element位置"""
        dragger = self.find_element(locator)
        element = self.find_element(locator1)
        self.action.drag_and_drop(dragger, element).perform()

    def send_keys_enter(self):
        """敲回车键"""
        self.action.send_keys(Keys.ENTER).perform()

    def send_keys_down(self):
        """敲方向键-下键"""
        self.action.send_keys(Keys.DOWN).perform()

    def send_keys_up(self):
        """敲方向键-下键"""
        self.action.send_keys(Keys.UP).perform()

    def send_keys_right(self):
        """敲方向键-右键"""
        self.action.send_keys(Keys.RIGHT).perform()

    def send_keys_left(self):
        """敲方向键-左键"""
        self.action.send_keys(Keys.LEFT).perform()

    def is_displayed(self, locator):
        """判断元素是否显示"""
        try:
            return self.find_element(locator).is_displayed()
        except TimeoutException:
            self.log.info('%s元素没有定位到' % str(locator))
            return False

    def enabled(self, locator):
        """判断元素是否被使用"""
        try:
            return self.find_element(locator).enabled()
        except TimeoutException:
            self.log.info('%s元素没有定位到' % str(locator))
            return False

    def is_switch_frame(self, frame):
        """判断该frame是否可以switch进去，如果可以的话，返回True并且switch进去，否则返回False"""
        return self.according_wait(EC.frame_to_be_available_and_switch_to_it(frame))

    def parent_frame(self, frame):
        """返回上一层iframe"""
        try:
            self.driver.switch_to.parent_frame(frame)
        except Exception:
            self.log.error(traceback.format_exc())

    def default_content(self, frame):
        """从iframe返回主页面"""
        try:
            self.driver.switch_to.default_content(frame)
        except Exception:
            self.log.error(traceback.format_exc())


    def is_text_in_element(self, locator, text):
        """判断文本在元素里，没定位到元素返回False，定位到返回判断结果布尔值"""
        return self.according_wait(EC.text_to_be_present_in_element(locator, text))

    def is_text_in_value(self, locator, value):
        """判断元素的value值，没有定位到返回False，定位到返回判断结果布尔值"""
        return self.according_wait(EC.text_to_be_present_in_element_value(locator, value))

    def is_title(self, title):
        """判断title完全等于"""
        return self.according_wait(EC.title_is(title))

    def is_title_contains(self, title):
        """判断title包含"""
        return self.according_wait(EC.title_contains(title))

    def is_selected(self, locator):
        """判断元素被选中，返回布尔值， 一般用在下拉框"""
        return self.according_wait(EC.element_to_be_selected(locator))

    def is_selected_be(self, locator, selected=True):
        """判断某个元素的选中状态是否符合预期，selected是期望的参数True/False，返回布尔值"""
        return self.according_wait(EC.element_selection_state_to_be(locator, selected))

    def is_alert_present(self):
        """判断页面上是否存在alert、confirm、prompt对话框,如果有就切换到alert并返回alert的内容"""
        return self.according_wait(EC.alert_is_present())

    def alert_accept(self):
        """点击alert、confirm、prompt弹窗确认按钮"""
        self.is_alert_present().accept()

    def alert_dismiss(self):
        """点击confirm、prompt弹窗取消按钮"""
        self.is_alert_present().dismiss()

    def alert_text(self):
        """获取alert、confirm、prompt对话框文本值"""
        return self.is_alert_present().text

    def alert_send_keys(self,text):
        """在prompt弹窗输入信息"""
        self.is_alert_present().send_keys(text)

    def is_visibility(self, locator):
        """元素可见返回本身，不可见返回False"""
        return self.according_wait(EC.visibility_of_element_located(locator))

    def is_invisibility(self, locator):
        """元素可见返回本身，不可见返回True，没有找到元素也返回True"""
        return self.according_wait(EC.invisibility_of_element_located(locator))

    def is_clickAble(self, locator):
        """元素可以点击返回本身，不可点击返回False"""
        return self.according_wait(EC.element_to_be_clickable(locator))

    def is_element_located(self, locator):
        """判断元素有没有被定位到（并不意味着可见），定位到返回element，没有定位到返回False"""
        return self.according_wait(EC.presence_of_element_located(locator))

    def is_elements_located(self, locator):
        """判断是否至少有1个元素存在于dom树中，如果定位到就返回列表"""
        return self.according_wait(EC.presence_of_all_elements_located(locator))



if __name__ == '__main__':
    b = BaseUI()
    # b.is_switch_frame('iframeResult')
    # b.click((By.CSS_SELECTOR,'[value="显示警告框"]'))
    # print(b.alert_text())
    print(b.find_element((By.ID,'kw1')))

