"""
@Project:huatest_mall_autotest
@File   :run.py
@IDE    :PyCharm
@Author :zhousha
@Date   :2026/9/12 20:20
"""
import subprocess
import pytest

def main() -> None:
    pytest.main()
    subprocess.run(
        'allure generate ./reports/allure_report -o ./reports/html --clean',
            check=True,
            shell=True,
    )

if __name__ == '__main__':
    main()