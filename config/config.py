from common.operation_ini import OperationIni

ini = OperationIni()    # 创建操作ini文件对象
logConfig = ini.read_ini_section('日志配置')       # 获取日志配置文件
environment = ini.read_ini_section('环境配置')       # 获取测试环境配置
framewor = ini.read_ini_section('框架配置')            # 获取框架配置信息
if __name__ == '__main__':

    print(framewor)