"""
@Project:huatest_mall_autotest
@File   :test_add_cart.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/17 22:06
"""
import re
import pytest
from typing import Any, Optional
from config.settings import ADD_CART_URL, DELETE_CART_URL, CART_URL, HEADERS
import allure
from utils import ApiClient, set_allure_dynamic, attach_request, attach_response, attach_expect, AutoLoader


try:
    _loader = AutoLoader()
    _case_data = _loader.load_cases("data/cart_data.yaml")
    if _case_data.loaded:
        _case_map = _case_data.case_map
        _loaded = True
    else:
        raise ValueError("购物车用例数据格式错误")
except (FileNotFoundError, KeyError, ValueError):
    _case_map = {}
    _loaded = False

# 把 case_map 按 case_id 前缀分组，作为本模块参数化的固定列表
ADD_CART_IDS = [cid for cid in _case_map if cid.startswith("ADD_CART")]
DELETE_CART_IDS = [cid for cid in _case_map if cid.startswith("DELETE_CART")]


def _find_cart_id_by_goods(client: ApiClient, goods_id: int) -> int:
    """通过查询 CART_URL 反查某 goods_id 对应购物车记录的 id。

    /index/cart/index.html 是**页面接口**，返回 JSON 包装的 HTML 字符串
    （content-type 虽是 application/json，但 data 是整页 HTML），
    购物车记录 id 并不在 JSON 字段里，而是嵌在商品行 <tr> 的属性上：

        <tr id="data-list-10086" data-id="10086" data-goods-id="1" ...>

    因此从 HTML 中按 data-goods-id 定位行，再取同行 data-id 作为记录 id。
    未找到则 pytest.fail，并在断言信息里附上页面关键片段便于排查。
    """
    resp = client.post(CART_URL)
    assert resp is not None and resp.status_code == 200, "查询购物车列表接口请求失败"

    # 兼容三种返回形态：JSON 包装的 HTML 字符串 / JSON data 字段里带 HTML / 纯 HTML
    html = resp.text
    try:
        body = resp.json()
    except ValueError:
        body = None
    if isinstance(body, str):
        html = body
    elif isinstance(body, dict) and isinstance(body.get("data"), str):
        html = body["data"]

    cart_id = _extract_cart_id(html, goods_id)
    if cart_id is None:
        snippet = re.sub(r"\s+", " ", html[:2000])
        pytest.fail(
            f"未在购物车页面中找到 goods_id={goods_id} 对应的记录 id，"
            f"页面开头片段：{snippet}"
        )
    return cart_id


def _extract_cart_id(html: str, goods_id: int) -> Optional[int]:
    """从购物车页面 HTML 中提取指定 goods_id 行的记录 id（data-id）。"""
    for tr_match in re.finditer(r"<tr\b[^>]*>", html):
        tr = tr_match.group(0)
        goods_match = re.search(r'data-goods-id="(\d+)"', tr)
        if not goods_match or int(goods_match.group(1)) != int(goods_id):
            continue
        id_match = re.search(r'data-id="(\d+)"', tr)
        if id_match:
            return int(id_match.group(1))
    return None


def _assert_cart_expect(
    result: dict[str, Any],
    expect: dict[str, Any],
    url: str,
    request_data: dict[str, Any],
) -> None:
    """统一的购物车接口断言辅助函数，断言失败时保留请求/响应/期望便于排查"""
    try:
        assert result.get("code") == expect.get("code"), \
            f"结果错误，预期code={expect.get('code')}，实际code={result.get('code')}"
        assert result.get("msg") == expect.get("msg"), \
            f"结果错误，预期msg={expect.get('msg')}，实际msg={result.get('msg')}"
    except AssertionError:
        attach_request(url, request_data, HEADERS)
        attach_response(200, result)
        attach_expect(expect)
        raise


@pytest.mark.skipif(not _loaded, reason="购物车数据文件缺失或格式错误")
@allure.epic("购物车模块")
class TestAddCart:
    """购物车测试类 - 数据驱动

    - test_add_cart    ：参数化执行 data/cart_data.yaml 中所有 ADD_CART 用例
    - test_delete_cart ：参数化执行 data/cart_data.yaml 中所有 DELETE_CART 用例
    """

    @pytest.mark.parametrize(
        "case_id",
        ADD_CART_IDS,
        ids=lambda cid: f"{cid}_{_case_map[cid]['case']}",
    )
    def test_add_cart(self, case_id: str, successful_login: ApiClient):
        """测试加入购物车"""
        case: dict[str, Any] = _case_map[case_id]
        set_allure_dynamic(case)

        request_data: dict[str, Any] = case.get("goods", {})
        with allure.step("发起加车请求"):
            resp = successful_login.post(ADD_CART_URL, data=request_data)

        assert resp is not None, "加车请求失败：未获取到响应"
        with allure.step("验证响应状态与加车结果"):
            try:
                assert resp.status_code == 200, f"加车请求失败，状态码为{resp.status_code}"
                result = resp.json()
                assert result, "加车请求返回的数据为空"
            except AssertionError:
                attach_request(ADD_CART_URL, request_data, HEADERS)
                attach_response(resp.status_code, resp.text)
                raise
            attach_response(resp.status_code, result)
            expect: dict[str, Any] = case.get("expect", {})
            _assert_cart_expect(result, expect, ADD_CART_URL, request_data)

    @pytest.mark.parametrize(
        "case_id",
        DELETE_CART_IDS,
        ids=lambda cid: f"{cid}_{_case_map[cid]['case']}",
    )
    def test_delete_cart(self, case_id: str, successful_login: ApiClient):
        """从购物车删除商品

        - case 含 goods_id 时：先实际调用加车接口确保购物车中有此商品，
          再按 goods_id 反查真实 cart id 删除（不依赖参数化顺序）。
        - case 含   id    时：直接显式删除（YAML 中通常写入不存在的负数 id）。
        """
        case: dict[str, Any] = _case_map[case_id]
        set_allure_dynamic(case)

        with allure.step("计算待删除的 cart_id"):
            if "goods_id" in case:
                goods_id: int = case["goods_id"]
                with allure.step(f"前置调用加车接口，确保购物车中存在 goods_id={goods_id}"):
                    add_resp = successful_login.post(
                        ADD_CART_URL,
                        data={"goods_id": goods_id, "stock": 1},
                    )
                    assert add_resp is not None and add_resp.status_code == 200, "加车请求失败"
                    add_result = add_resp.json()
                    assert add_result, "加车请求返回的数据为空"
                with allure.step(f"反查 goods_id={goods_id} 对应的购物车记录 id"):
                    cart_id: int = _find_cart_id_by_goods(successful_login, goods_id)
            elif "id" in case:
                cart_id = case["id"]
            else:
                pytest.fail(f"case {case_id} 缺少 goods_id 或 id 字段")

        request_data = {"id": cart_id}
        with allure.step(f"发起删除购物车请求 id={cart_id}"):
            resp = successful_login.post(DELETE_CART_URL, data=request_data)

        assert resp is not None, "删除购物车请求失败：未获取到响应"
        with allure.step("验证响应状态与删除结果"):
            try:
                assert resp.status_code == 200, f"删除购物车请求失败，状态码为{resp.status_code}"
                result = resp.json()
                assert result, "删除购物车请求返回的数据为空"
            except AssertionError:
                attach_request(DELETE_CART_URL, request_data, HEADERS)
                attach_response(resp.status_code, resp.text)
                raise
            attach_response(resp.status_code, result)
            expect: dict[str, Any] = case.get("expect", {})
            _assert_cart_expect(result, expect, DELETE_CART_URL, request_data)