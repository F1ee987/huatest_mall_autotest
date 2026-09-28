"""
@Project:huatest_mall_autotest
@File   :test_add_cart.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/17 22:06
"""
import pytest
from config.settings import ADD_CART_URL, DELETE_CART_URL
import allure
from utils import ApiClient, attach_response
from random import randint
from typing import Any

@allure.epic("购物车模块")
class TestAddCart:
    """
    购物车测试类
    """
    _successful_add_cart_dict: dict[str, Any] = {
        "goods": {
            "goods_id": randint(1, 10),
            "stock": randint(1,2)
        },
        "expect": {
            "code": 0,
            "msg": "成功"
        }
    }
    _nonexistent_goods_dict: dict[str, Any] = {
        "goods": {
            "goods_id": randint(-10, -1),
            "stock": randint(1,2)
        },
        "expect": {
            "code": -2,
            "msg": "不存在"
        }
    }

    _failed_add_cart_dict: dict[str, Any] = {
        "goods": {
            "goods_id": randint(1, 10),
            "stock": 8888888888888
        },
        "expect": {
            "code": -1,
            "msg": "库存不足"
        }
    }

    _delete_cart_dict: dict[str, Any] = {
        "id": 4130,
        "expect": {
            "code": 0,
            "msg": "删除成功"
        }
    }

    _delete_nonexistent_cart_dict: dict[str, Any] = {
        "id": 4130,
        "expect": {
            "code": -100,
            "msg": "不存在"
        }
    }


    @pytest.mark.parametrize(
        "goods, expect", [(_successful_add_cart_dict.get("goods"), _successful_add_cart_dict.get("expect")),
                           (_failed_add_cart_dict.get("goods"), _failed_add_cart_dict.get("expect")),
                          (_nonexistent_goods_dict.get("goods"), _nonexistent_goods_dict.get("expect"))
                          ],
        ids=["正向添加-库存充足-期望成功", "异常添加-库存不足-期望失败", "异常添加-商品不存在-期望失败"]
    )
    def test_add_cart(self, successful_login: ApiClient, goods: dict[str, int], expect: dict[str, int|str]) -> None:
        """
        测试加入购物车
        """
        allure.dynamic.title(f"加入购物车-商品ID:{goods['goods_id']},库存:{goods['stock']},预期:{expect['msg']}")
        with allure.step("添加商品到购物车"):
            resp = successful_login.post(ADD_CART_URL, data={"goods_id": goods.get("goods_id"), "stock": goods.get("stock")})
            assert resp.status_code == 200, "添加商品到购物车接口请求失败"
            assert resp.json()
        with allure.step("验证商品是否成功加入购物车"):
            body = resp.json()
            attach_response(resp.status_code, body)
            assert expect.get("code") == body.get("code") , "商品加入购物车接口返回错误码"
            assert expect.get("msg") in body.get("msg") , "商品加入购物车接口返回错误信息"

    @pytest.mark.parametrize(
        "category_id, expect", [(_delete_cart_dict.get("id"), _delete_cart_dict.get("expect")),
                                (_delete_nonexistent_cart_dict.get("id"), _delete_nonexistent_cart_dict.get("expect")),
                          ],
        ids=["删除购物车商品"]
    )
    def test_delete_cart(self, successful_login: ApiClient, category_id: int, expect: dict[str, int|str]) -> None:
        """
        从购物车删除商品
        """
        allure.dynamic.title(f"删除购物车商品-购物车ID:{category_id},预期:{expect['msg']}")
        with allure.step("删除购物车商品"):
            resp = successful_login.post(DELETE_CART_URL, data={"id": category_id})
            assert resp.status_code == 200, "删除购物车商品接口请求失败"
            assert resp.json()
        with allure.step("验证商品是否成功从购物车删除"):
            body = resp.json()
            attach_response(resp.status_code, body)
            assert expect.get("code") == body.get("code") , "删除商品接口返回错误码"
            assert expect.get("msg") in body.get("msg") , "商品删除接口返回错误信息"