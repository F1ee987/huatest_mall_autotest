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
    @pytest.mark.parametrize("case", login_cases, ids=lambda c: f"{c.get('case_id', '')}_{c.get('case', '')}")
    def test_login(self, case: dict, api_client: ApiClient) -> None:
        #----------------------动态设置allure动态属性-------------------------------
        allure.dynamic.title(f"{case.get('case_id','unknown')}:{case.get('case', 'unknown')}"
        )
        allure.dynamic.tag(case.get("mark", "unknown"))
        allure.dynamic.severity(case.get("severity", "unknown"))
        allure.dynamic.description(case.get("description", "无"))

        with allure.step("发送登录请求"):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/58.0.3029.110 Safari/537.3",
                    "x-requested-with": "XMLHttpRequest",
                }
                resp = api_client.post(LOGIN_URL, headers=headers, data=case.get('request'))
                assert resp.status_code == 200, f"登录请求失败，状态码：{resp.status_code}"
                result = resp.json()
            except JSONDecodeError:
                pytest.fail("响应内容不是合法的 JSON 格式")

        expect = case.get('expect')

        with allure.step("校验登录返回结果"):
            assert result.get("code") == expect.get("code"), (
                f"登录状态码校验失败：预期 {expect.get('code')}，实际 {result.get('code')}"
            )
            assert result.get("msg") == expect.get("msg"), (
                f"登录提示信息校验失败：预期 '{expect.get('msg')}'，实际 '{result.get('msg')}'"
            )
        if result.get("code") == 0:
            with allure.step("保存登录会话服务端 Cookie"):
                cookie_str = api_client.cookie_str
                assert cookie_str, "登录成功但 Cookie 为空"

                allure.attach(
                    cookie_str,
                    name="服务端 Cookie（PHPSESSID）",
                    attachment_type=allure.attachment_type.TEXT
                )