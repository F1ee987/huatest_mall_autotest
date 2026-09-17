"""
@Project:huatest_mall_autotest
@File   :test_add_cart.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/17 22:06
"""
from config.settings import ADD_CART_URL
import allure
import pytest

@allure.epic("购物车模块")
class TestAddCart:
    """
    加入购物车测试类
    """
    def test_add_cart_success(self) -> None:
        """
        测试加入购物车成功
        """
