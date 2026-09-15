"""
@Project:huatest_mall_autotest
@File   :settings.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/13 21:40
"""
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from utils import AutoLoader

# 加载 .env 文件
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(str(env_path))

# 环境变量
PASSWORD = os.getenv("PASSWORD")
WRONG_PASSWORD = os.getenv("WRONG_PASSWORD")

BASE_URL = AutoLoader().load(file_path="config/conf.json").get('BASE_URL')
LOGIN_URL = f"{BASE_URL}?s=/index/user/login.html"  # 登录URL


def replace_env_vars(data: dict) -> dict:
    """递归替换字典中的环境变量占位符"""
    result: dict[str, Any] = {}
    env_map: dict[str, str] = {
        'PASSWORD': PASSWORD,
        'WRONG_PASSWORD': WRONG_PASSWORD,
    }
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = replace_env_vars(value)
        elif isinstance(value, str):
            for env_name, env_value in env_map.items():
                placeholder = f"${{{env_name}}}"
                if placeholder in value and env_value is not None:
                    value = value.replace(placeholder, env_value)
            # 也支持直接读取系统环境变量作为后备
            value = os.path.expandvars(value)
            result[key] = value
        else:
            result[key] = value
    return result