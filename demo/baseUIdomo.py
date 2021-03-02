# -*- coding: utf-8 -*-
import os
import time
from PIL import Image
from selenium import webdriver
from appium import webdriver as app
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from common.logger import Log
from common import read_config


def open_browser(browser='chrome'):
    """打开浏览器函数。"firefox"、"chrome"、"ie",'phantomjs'"""

    # 驱动路径
    driver_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    try:
        if browser == 'firefox':
            executable_path = os.path.join(driver_path, 'driver\\geckodriver.exe')
            # executable_path = os.path.join(driver_path, 'driver/geckodriver')
            driver = webdriver.Firefox(executable_path=executable_path)
            return driver
        elif browser == 'chrome':
            # 加启动配置,忽略 Chrome正在受到自动软件的控制 提示
            option = webdriver.ChromeOptions()
            option.add_argument('disable-infobars')
            # chrome启动静默模式;默认显示浏览器界面
            if read_config.chrome_interface != 'True':
                option.add_argument('headless')
            executable_path = os.path.join(driver_path, 'driver\\chromedriver.exe')
            # executable_path = os.path.join(driver_path, 'driver/chromedriver')
            driver = webdriver.Chrome(chrome_options=option, executable_path=executable_path)
            return driver
        elif browser == 'ie':
            driver = webdriver.Ie()
            return driver
        elif browser == 'js':
            driver = webdriver.PhantomJS()
            return driver
        else:
            Log().warning('额，暂不支持此浏览器诶。先试试firefox、chrome、ie、phantomJS浏览器吧。')
            return
    except Exception as msg:
        Log().error('浏览器出错了呀！%s' % msg)
        return


def open_app():
    try:
        desired_caps = {
            'platformName': read_config.platform_name,

            'deviceName': read_config.device_name,

            'platformVersion': read_config.platform_version,

            'appPackage': read_config.app_package,

            'appActivity': read_config.app_activity,

            'noReset': True,

            # 隐藏手机默认键盘
            'unicodeKeyboard': True,

            'resetKeyboard': True
        }
        # 关联appium
        driver = app.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        return driver
    except Exception as e:
        raise Exception('连接 Appium 出错：{}'.format(e))


class Crazy:
    """基于原生的selenium框架做二次封装"""

    def __init__(self, driver):
        """启动浏览器参数化，默认启动chrome"""
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.timeout = 5  # 显示等待超时时间
        self.t = 1
        self.log = Log()

    def open(self, url, t=''):
        """get url，最大化浏览器，判断title"""
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        # 是否最大化浏览器
        if read_config.maximize != 'True':
            self.driver.maximize_window()
        try:
            WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(t))
            self.log.info('打开网页成功！')
        except TimeoutException:
            self.log.error('打开%s title错误，超时' % url)
        except Exception as msg:
            self.log.error('打开网页产生的其他错误：%s' % msg)

    def find_element(self, locator):
        """重写元素定位方法"""
        if not isinstance(locator, tuple):
            self.log.error('locator参数必须是元组类型，而不是：{}'.format(type(locator)))
            return ""
        else:
            try:
                element = WebDriverWait(self.driver, self.timeout, self.t).until(
                    EC.presence_of_element_located(locator))
                if element.is_displayed():
                    return element
            except:
                self.log.info('%s页面中未能找到元素%s' % (self, locator))
                return ""

    def find_elements(self, locator):
        """定位一组元素"""
        if not isinstance(locator, tuple):
            self.log.error('locator参数必须是元组类型，而不是：{}'.format(type(locator)))
            return ""
        else:
            try:
                elements = WebDriverWait(self.driver, self.timeout, self.t).until(
                    EC.presence_of_all_elements_located(locator))
                return elements
            except:
                self.log.info('%s页面中未能找到元素%s' % (self, locator))
                return ""











    def switch_frame(self, frame):
        """切换ifarm"""
        try:
            self.driver.switch_to_frame(self.find_element(frame))
            self.log.info('切换iframe成功！')
        except:
            self.log.warning('没有发现iframe元素%s' % frame)















    def swipeDown(self, t=500, n=1):
        '''向下滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5  # x坐标
        y1 = l['height'] * 0.25  # 起始y坐标
        y2 = l['height'] * 0.75  # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

    def swipeUp(self, t=500, n=1):
        '''向上滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5  # x坐标
        y1 = l['height'] * 0.65  # 起始y坐标
        y2 = l['height'] * 0.25  # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)


if __name__ == '__main__':
    driver = open_browser()
    driver.get('file:///D:/UIAutomation/report/2019-01-15%2017-40-10report.html')