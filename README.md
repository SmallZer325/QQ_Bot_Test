# QQ机器人测试项目

一个功能丰富的QQ机器人，由ZerD开发。基于腾讯官方 `qq-botpy` SDK。

## 功能列表

1. **AI智能对话** - 与机器人进行简短对话（需要配置AI API）
2. **看风景** - 随机显示风景图
3. **看setu** - 随机显示图片
4. **每日金句** - 获取夸赞作者ZerD的金句
5. **成语接龙** - 与机器人进行成语接龙游戏（最大50轮）

## 可用命令

### 群聊命令（需要@机器人）

| 命令 | 别名 | 功能说明 |
|------|------|----------|
| `/看风景` | `/风景` | 获取随机风景图 |
| `/看setu` | `/setu`、`/看涩图`、`/涩图` | 获取随机图片 |
| `/每日金句` | `/金句`、`/夸夸` | 获取夸赞ZerD的金句 |
| `/成语接龙` | `/接龙` | 开始成语接龙游戏 |
| `/help` | 任意未识别命令 | 显示帮助信息 |
| 直接发送消息（非命令） | - | 进行AI对话 |

### 私聊命令

| 命令 | 功能说明 |
|------|----------|
| `/每日金句`、`/金句`、`/夸夸` | 获取夸赞ZerD的金句 |
| 其他功能 | 私聊功能开发中，请在群聊中使用 |

### 命令使用示例

```
@机器人 /看风景          # 获取风景图
@机器人 /看setu          # 获取随机图片
@机器人 /夸夸            # 获取金句
@机器人 /成语接龙        # 开始成语接龙
@机器人 你好             # AI对话
```

## 系统要求

- **Python 3.8 或更高版本**（必需，qq-botpy需要Python 3.8+）
- Windows / Linux / macOS

## 安装步骤

### 0. 检查Python版本

```bash
python --version
```

如果版本低于3.8，请先升级Python或使用conda创建新环境（参考`PYTHON_VERSION.md`）。

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

如果遇到SSL证书问题，可以使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置机器人

#### 2.1 获取QQ机器人凭证

1. 访问 [QQ开放平台](https://bot.q.qq.com/)
2. 创建机器人应用，获取 `AppID` 和 `Secret`
3. 配置机器人的权限和回调地址

#### 2.2 编辑配置文件

编辑 `config.yaml` 文件：

```yaml
# 机器人配置
appid: "Your_Bot_Id"          # 替换为你的AppID
secret: "Enter_Your_Bot_Secret_Here"  # 替换为你的Secret

# AI API配置（可选）
# AI_API_KEY: "your_api_key_here"
# AI_BASE_URL: "https://api.openai.com/v1"
```

### 3. 运行机器人

```bash
python bot.py
```

**注意**：代码中 `is_sandbox=True` 表示使用沙箱环境（测试环境），生产环境请改为 `False`。

## 功能详细说明

### 1. AI智能对话

- **触发方式**：在群聊中@机器人后，直接发送消息（非命令）
- **功能**：与机器人进行简短对话
- **配置**：需要在 `config.yaml` 中配置 `AI_API_KEY` 和 `AI_BASE_URL` 才能使用完整AI功能
- **默认模式**：未配置API时使用简单回复模式

### 2. 看风景

- **命令**：`/看风景` 或 `/风景`
- **功能**：随机获取并显示风景图
- **API**：`https://t.alcy.cc/fj`

### 3. 看setu

- **命令**：`/看setu`、`/setu`、`/看涩图`、`/涩图`
- **功能**：随机获取并显示图片
- **API**：`https://hatsunemiku-tov.imwork.net/api/miku/?redirect=1`

### 4. 每日金句

- **命令**：`/每日金句`、`/金句`、`/夸夸`
- **功能**：随机输出一句夸赞作者ZerD的金句
- **特点**：包含20+条不同的夸赞语句

### 5. 成语接龙

- **命令**：`/成语接龙` 或 `/接龙`
- **功能**：开始成语接龙游戏
- **规则**：
  - 机器人先出一个成语
  - 用户回复以该成语尾字开头的成语
  - 机器人验证并接下一个成语
  - 最大接龙数：50轮
  - 如果用户输入不是成语或首字不匹配，游戏结束
- **状态**：每个群独立游戏状态，可同时进行多场游戏

## API说明

### 风景图API
- **地址**：`https://t.alcy.cc/fj`
- **类型**：直接返回图片（重定向）
- **说明**：API会重定向到实际的图片URL

### Setu图片API
- **地址**：`https://hatsunemiku-tov.imwork.net/api/miku/?redirect=1`
- **类型**：直接返回图片（重定向）
- **说明**：API会重定向到实际的图片URL

### 成语接龙API
- **验证API**：`https://chengyu.bmcx.com/{word}__chengyu/` - 验证是否为成语
- **搜索API**：`https://chengyujielong.bmcx.com/{char}__chengyujielong/` - 根据首字搜索成语
- **说明**：使用内置成语库和在线API相结合的方式

## 项目结构

```
QQ_Bot_Test/
├── bot.py                 # 主程序入口
├── config.yaml            # 配置文件（需要配置appid和secret）
├── requirements.txt       # Python依赖
├── pyproject.toml         # 项目配置
├── README.md             # 说明文档
├── QUICKSTART.md         # 快速启动指南
├── INSTALL.md            # 安装问题解决指南
└── plugins/              # 插件目录
    ├── __init__.py
    ├── utils.py          # 工具函数（获取用户名等）
    ├── ai_chat.py        # AI对话功能
    ├── scenery.py        # 风景图功能
    ├── setu_new.py       # Setu图片功能
    ├── golden_sentence.py # 每日金句功能
    └── chengyu.py        # 成语接龙功能
```

## 注意事项

1. **QQ开放平台配置**：
   - 需要在QQ开放平台创建机器人应用
   - 配置机器人的消息接收地址（Webhook或WebSocket）
   - 确保机器人有发送消息的权限

2. **AI对话功能**：
   - 默认使用简单回复模式
   - 如需完整AI功能，在`config.yaml`中配置`AI_API_KEY`和`AI_BASE_URL`
   - 支持OpenAI格式的API（如OpenAI、Azure OpenAI等）

3. **Setu功能**：
   - 使用新的API：`https://hatsunemiku-tov.imwork.net/api/miku/?redirect=1`
   - 直接返回图片，无需解析JSON

4. **图片发送**：
   - 使用QQ官方API的富媒体消息类型（msg_type=7）
   - 需要先通过`post_group_file`或`post_direct_file`上传文件资源
   - 然后使用返回的media对象发送消息

5. **成语接龙功能**：
   - 每个群独立游戏状态
   - 支持同时进行多场游戏
   - 游戏状态保存在内存中，重启后清空
   - 成语验证使用在线API和内置词库相结合

6. **沙箱环境**：
   - 代码中默认使用沙箱环境（`is_sandbox=True`）
   - 生产环境请修改为`is_sandbox=False`

## 开发框架

本项目使用腾讯官方 `qq-botpy` SDK，这是QQ机器人的官方Python SDK。

- 官方文档：https://bot.q.qq.com/wiki/develop/api/
- GitHub仓库：https://github.com/tencent-connect/botpy

## 开发者

ZerD - 代码界的艺术家，编程技术的引领者！

## 许可证

本项目仅供学习交流使用。
