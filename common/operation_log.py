# -*- coding: utf-8 -*-

import os,datetime,time,traceback
from nb_log import get_logger
from config.config import logConfig

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log')     # 自动获取日志文件夹默认存放路径
flieName = f'{datetime.datetime.now().strftime("%Y-%m-%d")}.log'    # 按日期生成日志文件名称

def clear_log(date,path=path):
    """
    按当天与创建的间隔时间，清除日志格式的文件
    :param data: 清除的间隔时间
    :return:
    """
    for i in os.listdir(path):
        if '.lock' in i or '.log' in i:
            fileTime = os.path.getctime(os.path.join(path,i))   # 获取文件的创建时间
            # 当天日期 - 创建日期 > 间隔时间
            if int(datetime.datetime.now().strftime("%Y%m%d")) - int(time.strftime("%Y%m%d",time.localtime(fileTime))) > date:
                os.remove(os.path.join(path,i))     # 删除文件

def logger(name='AutomatedTesting',path=path,flieName=flieName):
    """
    日志调用封装
    :param name: 日志命名空间,默认为AutomatedTesting
    :param path: 日志的文件夹存放路径，默认为项目下的log文件夹
    :param flieName: 日志的名字，默认以当天时间命名
    :return:
    """
    return get_logger(
        name,  # 日志命名空间
        log_level_int = int(logConfig['log_level']),  # 日志输出级别，设置为 1 2 3 4 5，分别对应原生logging.DEBUG(10)，logging.INFO(20)
        log_path = path,  # 日志的文件夹路径
        log_filename = flieName,  # 日志的名字
        formatter_template = int(logConfig['formatter_template']),  # 日志模板，1为formatter_dict的详细模板，2为简要模板,5为最好模板
        is_add_stream_handler = logConfig['stream_handler'],  # 是否打印日志到控制台
        do_not_use_color_handler = logConfig['color_handler']  # 是否禁止使用color彩色日志
    )


clear_log(7)    # 默认导入这个包就会执行清除日志方法

if __name__ == '__main__':
    # 日志调用
    logger().debug('一个debug级别的日志。' * 5)
    logger().info('一个info级别的日志。' * 5)
    logger().warning('一个warning级别的日志。' * 5)
    logger().error('一个error级别的日志。' * 5)
    logger().critical('一个critical级别的日志。' * 5)
    # # 异常调用日志示例
    # try:
    #     with open('123') as f:
    #         pass
    # except Exception as err:
    #     logger.error(traceback.format_exc())
    #     raise err
    # # clear_log(7)



