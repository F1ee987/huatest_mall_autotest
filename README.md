# huatest_mall_autotest

Huatest Mall 自动化接口测试项目，基于 **pytest + requests + allure** 实现，支持数据驱动测试、环境变量管理及测试报告生成。

## 技术栈

| 工具/库 | 说明 |
|---------|------|
| pytest | 测试框架 |
| allure-pytest | 测试报告（动态标题、标签、严重级别、附件） |
| requests | HTTP 请求（支持 Session 复用） |
| PyYAML | YAML 测试数据加载 |
| python-dotenv | 环境变量管理（`.env`） |

## 项目结构

```
.
├── config/
│   ├── settings.py        # 配置（ENV 加载 / 占位符替换 / URL）
│   └── conf.json          # 基础配置（BASE_URL）
├── data/
│   └── login.yaml         # 测试数据（YAML）
├── testcases/
│   └── test_login.py      # 测试用例
├── utils/
│   ├── api_client.py      # HTTP 客户端封装
│   └── loaders.py         # 数据加载器（YAML/JSON/CSV）
├── conftest.py            # pytest fixtures
├── pytest.ini             # pytest 配置
├── run.py                 # 运行入口（pytest + allure 报告）
└──  .env                   # 环境变量
```

## 快速开始

### 1. 安装依赖

```bash
pip install pytest requests allure-pytest pyyaml python-dotenv
```

并安装 allure CLI。

### 2. 配置

运行前配置 `.env`:

```env
PASSWORD=你的密码
WRONG_PASSWORD=错误的密码
```

配置 `config/conf.json` 中的 `BASE_URL`。

### 3. 运行

```bash
python run.py
```

运行后自动生成 HTML 报告：`reports/html/index.html`

## 特性

- **数据驱动**: YAML 定义测试用例，`AutoLoader` 自动识别格式
- **环境变量**: YAML 中使用 `${PASSWORD}` 占位符，运行时由 `settings.py` 替换
- **.Session 复用**: `ApiClient` 支持 Session 模式保持 Cookie
- **Allure 动态属性**: 标题、标签、严重级别、描述从 YAML 动态注入
- **失败重试**: `pytest.ini` 配置 `--reruns=2`

## YAML 用例格式

```yaml
login:
  - case_id: LOGIN_001
    case: 正常登录
    tags: [smoke, login]
    severity: critical
    description: 使用正确的用户名和密码登录
    request:
      accounts: huace_xm
      pwd: "${PASSWORD}"
      type: username
    expect:
      code: 0
      msg: 登录成功
      cookie:
        exists:
          - PHPSESSID
```
