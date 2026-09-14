from json import JSONDecodeError
import allure
import pytest
from utils import AutoLoader, ApiClient
from data.settings import LOGIN_URL

try:
    loader = AutoLoader()
    login_cases = loader.load('data/login.yaml').get('登录', [])
    if not login_cases:
        raise KeyError("登录数据缺失或格式错误")
    _data_loaded = True
except (FileNotFoundError, KeyError, Exception):
    login_cases = []
    _data_loaded = False

@pytest.mark.skipif(not _data_loaded, reason="数据文件缺失或格式错误")
@allure.story("登录测试")
@allure.severity("critical")
class TestLogin:
    @pytest.mark.parametrize("case", login_cases, ids=lambda c: c.get("case", "unknown"))
    def test_login(self, case: dict, api_client: ApiClient) -> None:
        allure.dynamic.title(f"登录测试 - {case.get('case', 'unknown')},"
                             f"预期{"success" if case.get("code") == 0 else "failure"}"
        )
        allure.dynamic.description(
            f"测试登录功能，输入用户名和密码："
            f"{case.get('accounts', 'unknown')},"
            f"{case.get('pwd', 'unknown')}"
        )
        with allure.step("发送登录请求"):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/58.0.3029.110 Safari/537.3",
                    "x-requested-with": "XMLHttpRequest",
                }
                resp = api_client.post(LOGIN_URL, headers=headers, data=case)
                assert resp.status_code == 200, f"登录请求失败，状态码：{resp.status_code}"
                result = resp.json()
            except JSONDecodeError:
                pytest.fail("响应内容不是合法的 JSON 格式")

        with allure.step("校验登录返回结果"):
            assert result.get("code") == case.get("code"), (
                f"登录状态码校验失败：预期 {case.get('code')}，实际 {result.get('code')}"
            )
            assert result.get("msg") == case.get("msg"), (
                f"登录提示信息校验失败：预期 '{case.get('msg')}'，实际 '{result.get('msg')}'"
            )