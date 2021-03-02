# -*- coding: utf-8 -*-
import os,pytest
# try:
#     for one in os.listdir('../report/tmp'):  # os.listdir('../report/tmp')列出路径下所有的文件
#         if 'json' in one:
#             os.remove(f'../report/tmp/{one}')
# except:
#     print('pytest---是第一次运行')
# 1- 生成报告所需的数据    --alluredir ../report/tmp
pytest.main(['./test_case/test_case_template.py', '-s', '--alluredir', '../report/tmp'])  # -s 打印print信息
# pytest.main(['test_case_template.py', '-s','-m','smoke_test', '--alluredir', '../report/tmp'])     # -m 根据标签执行用例
# 2- 生成打开测试报告---自动打开报告的服务
# 需要默认设置下浏览器
# os.system('allure serve ../report/tmp')