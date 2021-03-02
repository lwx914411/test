# -*- coding: utf-8 -*-
import yaml,json

class OperationYaml():

    def __init__(self):
        pass

    def read_yaml(self,path):
        """
        获取yaml文件中的数据
        :param path: yaml文件地址
        :return:
        """
        with open(path, 'rb') as y:
            cont = y.read()                             # 获取yaml文件中的所有信息
        yaml.warnings({'YAMLLoadWarning': False})       # 禁用加载器warnings报警
        return yaml.load(cont)                            # 将bytes格式转成dict格式

    def write_yaml(self,path,parameter,):
        """
        将数据写入yaml文件
        :param path: yaml文件地址
        :param parameter: 写入的参数
        :return:
        """
        with open(path, "a+", encoding="utf-8") as f:
            # 注：此模式为追加模式,若想直接重写则将open函数中的模式'a+'改为'w'
            yaml.dump(parameter, f)

    def read_yaml_api(self,path):
        for i in self.read_yaml(path):
            print(i)

if __name__ == '__main__':
    o = OperationYaml()
    o.read_yaml_api(r'../data/api测试用例模板2.yaml')
    # with open(r'../data/api测试用例模板2.yaml', 'rb') as y:
    #     cont = y.read()  # 获取yaml文件中的所有信息
    # yaml.warnings({'YAMLLoadWarning': False})  # 禁用加载器warnings报警
    # cf = yaml.load(cont)
    # print(cf)