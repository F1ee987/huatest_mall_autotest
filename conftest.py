"""
@Project:huatest_mall_autotest
@File   :conftest.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/12 20:38
"""
from utils import ApiClient, Logger, AutoLoader
import pytest
from typing import Generator, Any
from config.settings import LOGIN_URL

#-------------------私有辅助函数-------------------
_loader = AutoLoader()

def _authorized_user() -> dict[str, Any]:
    """
    返回一个成功登录的用户信息字典。
    :return:
    """
    user_info = _loader.load("data/login.yaml").get("login")
    return user_info

print(_authorized_user())

#-------------------fixture----------------------

@pytest.fixture(scope='function')
def logged_in() -> Generator[ApiClient]:
    """
    提供已登录的用户 ApiClient 实例。
    """
    client: ApiClient = ApiClient()
    client.post(LOGIN_URL)
    yield client
    client.close()

@pytest.fixture(scope='function')
def api_client() -> Generator[ApiClient, None, None]:
    """
    提供带 Session 的 ApiClient 实例。

    使用 yield 确保测试结束后正确释放 Session 资源。
    """
    client: ApiClient = ApiClient(use_session=True)
    try:
        yield client
    finally:
        client.close()

@pytest.fixture(scope='function')
def logger() -> Generator[Logger]:
    """
    提供 Logger 实例。

    使用 yield 确保测试结束后正确释放 Logger 资源。
    """
    logger_instance: Logger = Logger(__name__)
    try:
        yield logger_instance
    finally:
        logger_instance.close()