"""
@Project:huatest_mall_autotest
@File   :api_client.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/13 21:52
"""
import requests
from requests import Response
from typing import Optional, Any

class ApiClient:
    """基础 HTTP API 客户端封装，支持单次请求和 Session 复用。"""

    def __init__(self, use_session: bool = False) -> None:
        """
        初始化 API 客户端。

        :param use_session: 是否使用 requests.Session。
                            使用 Session 可在多次请求间复用 TCP 连接和 Cookie，
                            适合高频调用或需要保持会话状态的场景。
        """
        self.__session: Optional[requests.Session] = (
            requests.Session() if use_session else None
        )

    def _request(self, method: str, url: str, **kwargs: Any) -> Optional[Response]:
        """
        发送 HTTP 请求的统一入口。

        :param method: HTTP 请求方法，如 'GET', 'POST', 'PUT', 'DELETE'
        :param url: 请求地址
        :param kwargs: requests 原生参数，如：
                      - params: 查询参数
                      - json / data: 请求体
                      - headers: 请求头
                      - timeout: 超时时间
                      - verify: SSL 校验
        :return: requests.Response 对象；请求失败时返回 None
        """
        if self.__session:
            return self.__session.request(method, url, **kwargs)
        return requests.request(method, url, **kwargs)

    def get(self, url: str, **kwargs: Any) -> Optional[Response]:
        """
        发送 GET 请求。

        :param url: 请求地址
        :param kwargs: requests 原生参数（如 params, headers, timeout 等）
        :return: requests.Response 对象；请求失败时返回 None
        """
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> Optional[Response]:
        """
        发送 POST 请求。

        :param url: 请求地址
        :param kwargs: requests 原生参数（如 json, data, headers, timeout 等）
        :return: requests.Response 对象；请求失败时返回 None
        """
        return self._request("POST", url, **kwargs)

    @property
    def cookie_str(self) -> str:
        """
        返回当前 Session 的 Cookie 字符串（用于日志 / Allure / 断言）。
        示例：PHPSESSID=abc123; token=xyz
        """
        if not self.__session:
            return ""

        cookies = self.__session.cookies
        if not cookies:
            return ""

        return "; ".join(
            f"{k}={v}" for k, v in cookies.items()
        )

    def close(self) -> None:
        """
        关闭 Session（若存在）。

        在启用 use_session=True 时，建议显式调用，
        或使用 with 语句管理生命周期。
        """
        if self.__session:
            self.__session.close()

if __name__ == '__main__':
    from config.settings import REGISTER_URL
    client = ApiClient(use_session=True)
    response = client.post(REGISTER_URL, json={
        "accounts": "sgsdx",
        "pwd": "1",
        "type": "username"
    },headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3",
        "x-requested-with": "XMLHttpRequest",
    })
    