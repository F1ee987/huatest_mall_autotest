"""
@Project:huatest_mall_autotest
@File   :test_add_cart.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/17 22:06
"""
from config.settings import ADD_CART_URL, HEADERS
import allure
from utils import ApiClient, attach_response
from random import randint

@allure.epic("购物车模块")
class TestAddCart:
    """
    加入购物车测试类
    """
    @allure.title("测试加入购物车成功")
    def test_add_cart_success(self, successful_login: ApiClient) -> None:
        """
        测试加入购物车成功
        """
        with allure.step("添加商品到购物车"):
            goods_id = randint(1, 10)
            resp = successful_login.post(ADD_CART_URL, data={"goods_id": goods_id})
            assert resp.status_code == 200, "添加商品到购物车失败"
            print(resp.json())
        # with allure.step("验证商品是否成功加入购物车"):
        #     attach_response(resp.status_code, resp.json())