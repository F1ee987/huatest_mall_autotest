"""
@Project:huatest_mall_autotest
@File   :logger.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/16 20:29
"""
import logging

class Logger:
    def __init__(self, name, log_file: str = None, log_level: str = 'DEBUG'):
        # 创建一个logger对象
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)  # 设置日志级别为DEBUG
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
