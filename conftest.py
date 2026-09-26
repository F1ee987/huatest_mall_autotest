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
from config.settings import LOGIN_URL, HEADERS, replace_env_vars

#-------------------私有辅助函数-------------------
_loader = AutoLoader()

def _authorized_user() -> dict[str, Any]:
    """
    返回一个成功登录的用户信息字典。
    :return: 用户信息字典
    :raises ValueError: 如果未找到正常登录的用户信息。
    """
    user_infos = _loader.load("data/login.yaml").get("login")
    for user_info in user_infos:
        if user_info.get('case') == '正常登录':
            success_user = user_info
            return replace_env_vars(success_user)
    raise ValueError("未找到正常登录的用户信息")

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
def api_client() -> Generator[ApiClient]:
    """
    提供带 Session 的 ApiClient 实例。

    使用 yield 确保测试结束后正确释放 Session 资源。
    """
    client: ApiClient = ApiClient(use_session=True)
    client.set_headers(HEADERS)  # 设置请求头
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

@pytest.fixture(scope='function')
def successful_login(api_client: ApiClient) -> Generator[ApiClient]:
    """
    使用已登录的用户 ApiClient 实例进行登录操作。
    """
    _user = _authorized_user()
    resp = api_client.post(LOGIN_URL, json=_user.get('request'))
    if resp.json().get('code') != _user.get('expect').get('code'):
        pytest.fail("登录失败")
    yield api_client
    api_client.close()