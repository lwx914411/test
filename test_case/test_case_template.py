# -*- coding: utf-8 -*-
# @Time    : 2020-12-07 19:05
# @Author  : admin
# @FileName: test_case_template.py
# @Software: PyCharm

import os,pytest
from common.base_api import BaseAPI
from common.operation_yaml import OperationYaml

base = BaseAPI()
o = OperationYaml()

# pytest测试用例模板
class Test_template():

    def setup_class(self):
        """
        初始化
        :return:
        """
        self.base = BaseAPI()

    @pytest.mark.parametrize('testCase', o.read_yaml(r'./data/api测试用例模板2.yaml'))
    def test_add_food_type1(self, testCase):
        self.base.write_allure(testCase)


if __name__ == '__main__':
    # 本地运行处理历史数据
    try:
        for one in os.listdir('../report/tmp'):  # os.listdir('../report/tmp')列出路径下所有的文件
            if 'json' in one:
                os.remove(f'../report/tmp/{one}')
    except:
        print('pytest---是第一次运行')
    # 1- 生成报告所需的数据    --alluredir ../report/tmp
    pytest.main(['test_case_template.py', '-s', '--alluredir', '../report/tmp'])  # -s 打印print信息
    # pytest.main(['test_case_template.py', '-s','-m','smoke_test', '--alluredir', '../report/tmp'])     # -m 根据标签执行用例
    # 2- 生成打开测试报告---自动打开报告的服务
    # 需要默认设置下浏览器
    os.system('allure serve ../report/tmp')
    '''
    报告的流程：
        1- 生成报告所需的数据    --alluredir ../report/tmp
        2- 使用工具让数据生成可视化报告  cmd里运行 allure  serve
    '''


