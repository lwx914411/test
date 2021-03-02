# -*- coding: utf-8 -*-

import os,configparser,traceback
from configparser import RawConfigParser

#ini文件操作类
class OperationIni():

    """默认获取config.ini配置文件的路径，os.path.abspath(__file__)获取当前文件的绝对路径，os.path.dirname()获取当前工作目录的绝对路径"""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config\\', 'config.ini')
    def __init__(self, path=path):
        self.path = path        # 文件存放地址
        # 判断文件路径是否存在
        if not os.path.isfile(self.path):
            raise FileNotFoundError({'code': '2', 'error': f'文件路径不存在，请检查路径是否正确：{self.path}'})
        self.conf = RawConfigParser()   # 创建管理对象
        self.conf.read(self.path, encoding='utf-8')     # 读ini文件

    def read_ini_section(self, section):
        """
        获取ini文件中指定section标签的数据
        :param section: ini文件的section标签
        :return:
        """
        try:
            items = {}
            for con in self.conf.items(section):
                # 判断字符串是否为布尔值的字符串，是则将该字符串转成对应的布尔值
                if con[1].title() == 'True':
                    items[con[0]] = True
                    continue
                elif con[1].title() == 'False':
                    items[con[0]] = False
                    continue
                elif con[1].title() == 'None':
                    items[con[0]] = None
                    continue
                items[con[0]] = con[1]
            return items
        except configparser.NoSectionError as err:
            raise {'code':'2','error':f'{self.path}文件中没有{section}标签'}
        except Exception as err:
            raise {'code': '2', 'error': err}

    def read_all_ini(self):
        """
        获取ini文件中所有的数据
        :return:
        """
        sections = {}
        try:
            for s in self.conf.sections():      # 获取所有的section
                sections[s] = self.read_ini_section(s)     # 获取section标签的数据
            return sections
        except Exception as err:
            raise {'code': '2', 'error': err}

if __name__ == '__main__':
    o = OperationIni()
    print(o.read_ini_section('数据库'))
    # print(o.read_all_ini())
    s = o.read_ini_section('数据库')
    # s['t'] = bool(s['t'])
    print(type(s['f']))
    # print(type(True))
    # print('ssd'.title())
