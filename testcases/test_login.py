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
        allure.dynamic.title(f"登录测试 - {case.get('case', 'unknown')}")
        allure.dynamic.description(
            f"测试登录功能，输入用户名和密码："
            f"{case.get('username', 'unknown')},"
            f"{case.get('password', 'unknown')}"
        )
        with allure.step("发起登录请求"):
            resp = api_client.post(LOGIN_URL, data=case)
            print(resp.json())
