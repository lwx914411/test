# -*- coding: utf-8 -*-
import traceback
from selenium.common.exceptions import TimeoutException
from common.operation_log import logger


class OperationError():

    def __init__(self):
        from common.base_ui_copy import BaseUI
        self.log = logger()

    @staticmethod
    def selenium_error(func):
        def wrapper(*args, **kwargs):
            try:
                print(args)
                return func(args[0], args[1])
            except TimeoutException:
                OperationError().log.info('%s元素没有定位到' % str(args[1]))
                return False
            except Exception:
                OperationError().log.error(traceback.format_exc())
                return False

        return wrapper





if __name__ == '__main__':
    pass