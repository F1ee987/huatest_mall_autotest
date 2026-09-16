# huatest_mall_autotest

Huatest Mall 自动化接口测试项目，基于 **pytest + requests + allure** 实现，支持数据驱动测试、环境变量管理、动态 Allure 报告及测试报告生成。

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
│   ├── settings.py        # 配置（ENV 加载 / 占位符替换 / URL / 随机用户名生成）
│   └── conf.json          # 基础配置（BASE_URL）
├── data/
│   ├── login.yaml         # 登录测试数据（YAML）
│   └── register.yaml      # 注册测试数据（YAML）
├── testcases/
│   ├── test_login.py      # 登录测试用例
│   └── test_register.py   # 注册测试用例
├── utils/
│   ├── api_client.py      # HTTP 客户端封装
│   ├── loaders.py         # 数据加载器（YAML/JSON/CSV）
│   └──  allure_utils.py    # Allure 工具函数（动态属性/附件）
├── conftest.py            # pytest fixtures
├── pytest.ini             # pytest 配置
├──run.py                 # 运行入口（pytest + allure 报告）
└── .env                   # 环境变量
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
- **随机用户名**: 支持 `${random_username}` 占位符，自动生成随机用户名（8位小写字母+数字）
- **Session 复用**: `ApiClient` 支持 Session 模式保持 Cookie
- **Allure 动态属性**: 标题、标签、严重级别、描述从 YAML 动态注入
- **Allure 附件**: 自动附加请求信息、响应信息、预期结果到报告
- **失败重试**: `pytest.ini` 配置 `--reruns=2`

## Allure 工具函数

### `set_allure_dynamic(case)`

动态设置 Allure 测试属性（标题、标签、严重级别、描述）。

### `attach_request(url, request_data, headers)`

附加请求信息到 Allure 报告（URL、参数、Headers）。

### `attach_response(status_code, response_data)`

附加响应信息到 Allure 报告（状态码、响应体）。

### `attach_expect(expect)`

附加预期结果到 Allure 报告。

## YAML 用例格式

### 登录用例

```yaml
login:
  - case_id: LOGIN_001
    case: 正常登录
    tags: 
     - smoke
     - login
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

### 注册用例

```yaml
register:
  - case_id: REGISTER_005
    case: 用户名和密码都正确
    tags: 
     - register
     - smoke
    severity: critical
    description: 用户名和密码都正确，预期返回注册成功提示
    request:
      accounts: "${random_username}"
      pwd: "${PASSWORD}"
      type: username
    expect:
      code: 0
      msg: 注册成功
```

## 环境变量占位符

| 占位符 | 说明 |
|--------|------|
| `${PASSWORD}` | 正确密码（从 `.env` 读取） |
| `${WRONG_PASSWORD}` | 错误密码（从 `.env` 读取） |
| `${random_username}` | 随机生成的8位用户名（小写字母+数字） |
