"""
@Project:huatest_mall_autotest
@File   :test_register.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/16 18:53
"""
import allure
from requests import Response
from utils import AutoLoader, ApiClient, set_allure_dynamic, attach_request, attach_response, attach_expect
import pytest
from config.settings import REGISTER_URL, replace_env_vars, HEADERS

try:
    loader = AutoLoader()
    register_cases = loader.load("data/register.yaml").get("register")
    _loaded = True
    case_map: dict[str, dict[str, dict]] = {c["case_id"]: c for c in register_cases}
except (FileNotFoundError, KeyError):
    register_cases = []  # 假设注册用例为空
    _loaded = False

@pytest.mark.skipif(not _loaded, reason="数据文件缺失或格式错误")
@allure.epic("注册模块")
class TestRegister:
    @pytest.mark.parametrize(
        "case_id",
        list(case_map.keys()),
        ids=lambda cid: f"{cid}_{case_map[cid]['case']}"
    )
    def test_register_success(self, case_id: str, api_client: ApiClient):
        """
        测试注册成功
        """
        case: dict[str, dict] = case_map[case_id]
        set_allure_dynamic(case)

        with allure.step("发起注册请求"):
            request_data: dict[str, str] = replace_env_vars(case.get('request', {}))

            resp: Response = api_client.post(REGISTER_URL, json=request_data, headers=HEADERS)

        with allure.step("验证响应状态"):
            try:
                assert resp.status_code == 200, f"注册请求失败，状态码为{resp.status_code}"
                result = resp.json()
                assert result, f"注册请求返回的数据为空"
            except AssertionError as e:
                attach_request(REGISTER_URL, request_data, HEADERS)
                attach_response(resp.status_code, resp.text if 'resp' in locals() else None)
                raise

        with allure.step("验证注册结果"):
            expect: dict[str, str] = case.get('expect')
            try:
                assert result.get('code') == expect.get('code'), \
                    f"注册结果错误，预期code={expect.get('code')}，实际code={result.get('code')}"
                assert result.get('msg') == expect.get('msg'), \
                    f"注册结果错误，预期msg={expect.get('msg')}，实际msg={result.get('msg')}"
            except AssertionError as e:
                attach_request(REGISTER_URL, request_data, HEADERS)
                attach_response(resp.status_code, result)
                attach_expect(expect)
                raise