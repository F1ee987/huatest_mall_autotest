"""Allure 动态属性设置工具"""
import json
from typing import Any, Mapping
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


def attach_request(
    url: str,
    request_data: dict[str, Any],
    headers: Mapping[str, str] | None = None,
) -> None:
    """
    附加请求信息到 Allure 报告

    Args:
        url: 请求 URL
        request_data: 请求参数
        headers: 请求头
    """
    payload: dict[str, Any] = {
        "url": url,
        "params": request_data,
    }
    if headers:
        payload["headers"] = dict(headers)
    allure.attach(
        json.dumps(payload, ensure_ascii=False, indent=2),
        name="请求信息",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_response(
    status_code: int,
    response_data: dict[str, Any] | str,
) -> None:
    """
    附加响应信息到 Allure 报告

    Args:
        status_code: HTTP 状态码
        response_data: 响应数据（字典或字符串）
    """
    payload: dict[str, Any] = {"status_code": status_code, "body": response_data}
    allure.attach(
        json.dumps(payload, ensure_ascii=False, indent=2),
        name="响应信息",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_expect(expect: dict[str, Any]) -> None:
    """
    附加预期结果到 Allure 报告

    Args:
        expect: 预期结果字典
    """
    allure.attach(
        json.dumps(expect, ensure_ascii=False, indent=2),
        name="预期结果",
        attachment_type=allure.attachment_type.JSON,
    )
