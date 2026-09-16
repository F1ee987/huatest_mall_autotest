"""
@Project:huatest_mall_autotest
@File   :logger.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/16 20:29
"""
import logging

class Logger:
    """
    日志记录器封装类
    """

    _level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(
            self,
            name: str,
            log_file: str | None = None,
            log_level: str = "DEBUG",
            fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ):
        self.logger = logging.getLogger(name)

        # 避免重复添加 handler
        if self.logger.handlers:
            return

        level = self._level_map.get(log_level.upper(), logging.DEBUG)
        self.logger.setLevel(level)

        formatter = logging.Formatter(fmt)

        # 控制台 handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件 handler
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """记录信息信息"""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """记录错误信息"""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """记录严重错误信息"""
        self.logger.critical(message)

    def close(self):
        """关闭日志记录器"""
        for handler in self.logger.handlers:
            handler.close()