"""
@Project:huatest_mall_autotest
@File   :conftest.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/12 20:38
"""
from utils import ApiClient
import pytest
from typing import Generator

@pytest.fixture(scope='function')
def api_client() -> Generator[ApiClient, None, None]:
    """
    提供带 Session 的 ApiClient 实例。

    使用 yield 确保测试结束后正确释放 Session 资源。
    """
    client = ApiClient(use_session=True)
    try:
        yield client
    finally:
        client.close()