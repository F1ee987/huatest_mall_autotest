import allure
from utils import AutoLoader

loader = AutoLoader()
loader.load('login.yaml')

@allure.title("登录测试")
class TestLogin:
    def test_login(self) -> None:
        ...