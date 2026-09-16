"""Allure 动态属性设置工具"""
from typing import Any
import allure

def set_allure_dynamic(
    case: dict[str, Any],
    *,
    title_sep: str = ":",
    default_title: str = "unknown",
    default_severity: str = "normal",
    default_description: str = "无",
) -> None:
    """
    动态设置 Allure 测试属性

    Args:
        case: 测试用例数据字典
        title_sep: 标题中 case_id 与 case 名称之间的分隔符
        default_title: 缺失 case_id 或 case 时的默认值
        default_severity: 缺失 severity 时的默认值
        default_description: 缺失 description 时的默认值
    """
    case_id = case.get("case_id") or default_title
    case_name = case.get("case") or default_title
    allure.dynamic.title(f"{case_id}{title_sep}{case_name}")

    for tag in case.get("tags") or []:
        allure.dynamic.tag(tag)

    allure.dynamic.severity(case.get("severity") or default_severity)
    allure.dynamic.description(case.get("description") or default_description)
