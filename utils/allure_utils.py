"""Allure 动态属性设置工具"""
import allure


def set_allure_dynamic(case: dict) -> None:
    """
    动态设置 Allure 测试属性
    
    Args:
        case: 测试用例数据字典
    """
    allure.dynamic.title(f"{case.get('case_id', 'unknown')}:{case.get('case', 'unknown')}")
    for tag in case.get("tags", []):
        allure.dynamic.tag(tag)
    allure.dynamic.severity(case.get("severity", "unknown"))
    allure.dynamic.description(case.get("description", "无"))
