"""
@Project:huatest_mall_autotest
@File   :settings.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/13 21:40
"""
import os
from pathlib import Path
from typing import Any, Dict, Mapping
from dotenv import load_dotenv
from utils import AutoLoader

# 加载 .env 文件
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(str(env_path))

# 环境变量
PASSWORD: str | None = os.getenv("PASSWORD")
WRONG_PASSWORD: str | None = os.getenv("WRONG_PASSWORD")

BASE_URL: str = AutoLoader().load(file_path="config/conf.json").get("BASE_URL")
LOGIN_URL: str = f"{BASE_URL}?s=/index/user/login.html"
REGISTER_URL: str = f"{BASE_URL}?s=/index/user/reg.html"

# 请求头
HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.3",
    "x-requested-with": "XMLHttpRequest",
}

def replace_env_vars(data: Mapping[str, Any]) -> Dict[str, str]:
    """
    递归替换字典中的环境变量占位符。

    支持：
    - ${ENV_NAME} 形式的占位符
    - 系统环境变量（通过 os.path.expandvars）

    注意：
    - 非字符串值会原样返回
    - 若环境变量未设置，占位符不会被替换
    """
    env_map: Dict[str, str | None] = {
        "PASSWORD": PASSWORD,
        "WRONG_PASSWORD": WRONG_PASSWORD,
    }

    result: Dict[str, Any] = {}

    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = replace_env_vars(value)

        elif isinstance(value, str):
            new_value: str = value
            for env_name, env_value in env_map.items():
                if env_value is not None:
                    placeholder = f"${{{env_name}}}"
                    if placeholder in new_value:
                        new_value = new_value.replace(placeholder, env_value)

            # 支持系统环境变量兜底
            result[key] = os.path.expandvars(new_value)

        else:
            result[key] = value

    return result