# -*- coding: utf-8 -*-
# @Time    : 2021-01-27 18:57
# @Author  : admin
# @FileName: base_api.py
# @Software: PyCharm

import requests,json,traceback,jmespath,yaml,allure,pytest
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from common.operation_log import logger
from config.config import *
from string import Template

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class BaseAPI():

    def __init__(self):
        self.session = requests.session()   # 在同一个 Session 实例发出的所有请求之间保持 cookie
        self.verify = framewor['verify']    # 获取SSL证书验证开关
        self.timeout = int(framewor['timeout'])  # 获取请求超时时间

    def requests_http(self,parameter):
        """
        requests二次封装，根据指定数据格式传入，进行请求
        :param parameter:
        parameter={
            "method":"请求方式，str格式，必填"
            "url":"请求url，str格式，必填"
            "headers":"请求头，str格式，必填"
            "body":"请求参数，str或dict格式"
            "cookies":"cookies值，默认为空，str格式"
            }
        当headers为multipart/form-data：
        上传文件组装对象  (文件名，文件对象open(路径，打开方式)，文件类型)
               body = {'file': (name, open(path, 'rb'), type)}
               多个文件接口：{"文件名1":(),"文件名2":(),"文件名3":()}
        :return:
        """

        # 入参校验
        if parameter.get('method') == None:
            raise {'code':'2','error':f'参数中缺少请求方式method'}
        elif parameter.get('url') == None:
            raise {'code':'2','error':f'参数中缺少地址url'}
        elif parameter.get('headers') == None:
            raise {'code':'2','error':f'参数中缺少请求头headers'}
        elif parameter.get('body') == None:
            parameter['body'] = {}

        data = None
        files = None
        params = None
        cookies = None

        # 判断请求头是否为表单提交方式
        if 'application/x-www-form-urlencoded' in parameter['headers']['Content-Type']:
            # 判断请求参数是否为字典格式,如果不是则转换成字典格式
            if type(parameter['body']) != dict:
                try:
                    if parameter['method'].lower() == 'get':
                        params = json.loads(parameter['body'])
                    else:
                        data = json.loads(parameter['body'])
                except Exception as err:
                    logger().error(traceback.format_exc())
                    raise err
            else:
                if parameter['method'].lower() == 'get':
                    params = parameter['body']
                else:
                    data = parameter['body']

        # 判断请求头是否为JSON提交方式
        elif 'application/json' in parameter['headers']['Content-Type']:
            # 判断请求参数是否为字符串格式,如果不是则转换成字符串格式
            if type(parameter['body']) != str:
                try:
                    data = json.dumps(parameter['body'])
                except Exception as err:
                    logger().error(traceback.format_exc())
                    raise err
            else:
                data = parameter['body']

        # 判断请求头是否为表单上传提交方式
        elif 'multipart/form-data' in parameter['headers']['Content-Type']:
            # 判断请求参数是否为字典格式,如果不是则转换成字典格式
            if type(parameter['body']) != dict:
                try:
                    files = json.loads(parameter['body'])
                except Exception as err:
                    logger().error(traceback.format_exc())
                    raise err
            else:
                files = parameter['body']

        # 执行请求
        try:
            return self.session.request(
                                 method = parameter['method'],    # 请求方式
                                 headers = parameter['headers'],  # 请求头
                                 url = parameter['url'],          # 请求URL
                                 params = params,                 # get方式的请求参数，默认为空
                                 data = data,                     # post方式的请求参数，默认为空
                                 files = files,                   # 文件上传请求方式，默认为空
                                 cookies = cookies,               # 请求cookies，默认为空
                                 verify = self.verify,            # SSL证书验证关闭
                                 timeout = self.timeout           # 连接超时时间
            )
        except Exception as err:
            logger().error(traceback.format_exc())
            raise err

    def batch_execution_cases(self,testCase):
        """
        测试用例执行，自动获取接口返回变量，对请求参数进行变量的替换
        :param testCase: 测试用例，dict格式
        :return:
        """

        result = None       # 接口返回
        variate = {}        # 接口返回值变量存储
        response = []       # 接口参数储存
        for t in testCase['测试步骤']:
            url = environment['host'] + t['请求地址']  # 拼接请求地址
            body = json.dumps(t['请求参数'])
            # 替换环境变量和接口返回值变量，替换失败则不进行替换
            for var in [environment, variate]:
                try:
                    body = Template(body).substitute(var)
                except:
                    continue
                parameter = {"method": t['请求方式'], "url": url, "headers": t['请求头'], "body": body}
                result = self.requests_http(parameter)

                # 判断接口返回值是否可以转换成json字符串
                try:
                    result = result.json()
                except json.decoder.JSONDecodeError:
                    result = result.text

            # 返回取值为字典格式，根据字典的键值对进行取值，并加入接口返回值变量
            if type(t['返回取值']) == dict:
                for key, value in t['返回取值'].items():
                    variate[key] = jmespath.search(value, result)

            response.append({'接口名称': t['接口名称'],
                             '请求方式': t['请求方式'],
                             '请求头': t['请求头'],
                             '请求地址': url,
                             '请求参数': body,
                             '预期结果': t['预期结果'],
                             '实际结果':result})

        return response

    def write_allure(self,testCase):
        allure.dynamic.feature(testCase['模块名称'])
        allure.dynamic.title(testCase['测试用例名称'])
        result = self.batch_execution_cases(testCase)
        for r in result:
            with allure.step(r['接口名称']):
                with allure.step(f'''发送请求-->'''):
                    with allure.step(f'请求方式: {r["请求方式"]}'):
                        pass
                    with allure.step(f'请求地址: {r["请求地址"]}'):
                        pass
                    with allure.step(f'请求头: {r["请求头"]}'):
                        pass
                    with allure.step(f'请求参数: {r["请求参数"]}'):
                        pass
                    with allure.step(f'响应结果: {r["实际结果"]}'):
                        pass
                with allure.step('进行预期结果与实际结果的断言'):
                    for key, value in r['预期结果'].items():
                        with allure.step(f'{key}断言：预期结果：{value[0]}，实际结果：{jmespath.search(value[1], r["实际结果"])}'):
                            # assert value[0] == jmespath.search(value[1], r['实际结果'])
                            pytest.assume(value[0] == jmespath.search(value[1],r['实际结果']))

if __name__ == '__main__':
    b = BaseAPI()
    with open(r'../data/api测试用例模板2.yaml', 'rb') as y:
        cont = y.read()  # 获取yaml文件中的所有信息
    yaml.warnings({'YAMLLoadWarning': False})  # 禁用加载器warnings报警
    cf = yaml.load(cont)
    # pprint.pprint(cf)
    # b.batch_execution_cases(cf[2])
    print(b.batch_execution_cases(cf[2]))
