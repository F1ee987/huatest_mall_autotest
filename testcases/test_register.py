"""
@Project:huatest_mall_autotest
@File   :test_register.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/16 18:53
"""
import allure
from utils import AutoLoader, ApiClient, set_allure_dynamic
import pytest

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
        assert case_id