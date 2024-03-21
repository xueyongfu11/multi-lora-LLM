import re
import os
import logging
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, logfile, logging_level):

        if not os.path.exists(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))

        logger = logging.getLogger()
        logging_level_c = self.get_logging_class(logging_level)
        logger.setLevel(logging_level_c)

        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(filename)s %(message)s')

        streamhandler = logging.StreamHandler()
        # ============================================================================#
        # 设置日志的handler格式：                                                                                                                                                     #
        # * handler: 每 1(interval) 天(when) 重写1个文件,保留30(backupCount) 个旧文件                                                                  #
        # * when还可以是s/m/h, 大小写不区分                                                                                                                                    #
        # ============================================================================#
        filehandler = TimedRotatingFileHandler(logfile, when='d', interval=1, backupCount=30, encoding='utf-8')
        filehandler.suffix = r"%Y-%m-%d_%H-%M-%S.log"  # 设置历史文件后缀
        filehandler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.log$")

        filehandler.setFormatter(formatter)
        streamhandler.setFormatter(formatter)

        logger.addHandler(filehandler)
        logger.addHandler(streamhandler)
        # 先输出hyper_params到日志中
        # logger.info('logger testing !')
        self.logger = logger

    def get_logging_class(self, logging_level):
        if logging_level == 'debug':
            return logging.DEBUG
        elif logging_level == 'info':
            return logging.INFO
        elif logging_level == 'warning':
            return logging.WARNING
        elif logging_level == 'error':
            return logging.ERROR
        else:
            raise Exception(f'not support logging level: {logging_level}')
