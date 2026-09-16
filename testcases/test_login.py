from json import JSONDecodeError
import allure
import pytest
from requests import Response
from utils import AutoLoader, ApiClient, set_allure_dynamic
from config.settings import LOGIN_URL, replace_env_vars, HEADERS

try:
    loader: AutoLoader = AutoLoader()
    login_cases: list[dict] = loader.load('data/login.yaml').get('login', [])
    if not login_cases:
        raise KeyError("登录数据缺失或格式错误")
    _data_loaded: bool = True
    case_map: dict[str, dict[str, dict]] = {c["case_id"]: c for c in login_cases}
except (FileNotFoundError, KeyError, Exception):
    login_cases = []
    _data_loaded = False

@pytest.mark.skipif(not _data_loaded, reason="数据文件缺失或格式错误")
@allure.story("登录测试")
class TestLogin:
    @pytest.mark.parametrize(
        "case_id",
        list(case_map.keys()),
        ids=lambda cid: f"{cid}_{case_map[cid]['case']}"
    )
    def test_login(self, case_id: str, api_client: ApiClient):
        case: dict[str, dict] = case_map[case_id]
        set_allure_dynamic(case)

        with allure.step("发送登录请求"):
            request_data: dict[str, str] = replace_env_vars(case.get('request', {}))
            resp: Response = api_client.post(LOGIN_URL, headers=HEADERS, data=request_data)
            assert resp.status_code == 200, f"登录请求失败，状态码：{resp.status_code}"

            try:
                result = resp.json()
            except JSONDecodeError:
                pytest.fail("响应内容不是合法的 JSON 格式")

        with allure.step("校验登录返回结果"):
            expect: dict[str, str] = case.get('expect')
            assert result.get("code") == expect.get("code"), (
                f"登录状态码校验失败：预期 {expect.get('code')}，实际 {result.get('code')}"
            )
            assert result.get("msg") == expect.get("msg"), (
                f"登录提示信息校验失败：预期 '{expect.get('msg')}'，实际 '{result.get('msg')}'"
            )

        if result.get("code") == 0:
            with allure.step("保存登录会话 Cookie"):
                cookie_str: str = api_client.cookie_str
                assert cookie_str, "登录成功但 Cookie 为空"
                allure.attach(
                    cookie_str,
                    name="服务端 Cookie（PHPSESSID）",
                    attachment_type=allure.attachment_type.TEXT
                )