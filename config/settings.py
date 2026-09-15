"""
@Project:huatest_mall_autotest
@File   :settings.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/13 21:40
"""
from utils import AutoLoader

BASE_URL = AutoLoader().load(file_path="config/conf.json").get('BASE_URL')
LOGIN_URL = f"{BASE_URL}?s=/index/user/login.html" #登录URL