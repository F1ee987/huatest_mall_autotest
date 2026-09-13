"""
@Project:huatest_mall_autotest
@File   :__init__.py.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/12 20:20
"""
try:
    from .loaders import AutoLoader
    from .api_client import ApiClient
except ImportError as e:
    raise ImportError(f"无法导入数据加载模块: {e}") from e

__all__ = ["AutoLoader", "ApiClient"]