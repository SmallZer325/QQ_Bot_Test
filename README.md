# QQ机器人测试项目

一个功能丰富的QQ机器人，由ZerD开发。基于腾讯官方 `qq-botpy` SDK。

## 功能列表

1. **AI智能对话** - 与机器人进行简短对话（需要配置AI API）
2. **看风景** - 使用 `/看风景` 命令随机显示风景图
3. **看涩图** - 使用 `/看涩图` 命令随机显示涩图（来自lolicon API）
4. **每日金句** - 使用 `/每日金句` 命令获取夸赞作者ZerD的金句

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

## 命令说明

### 群聊命令（需要@机器人）

- `/看风景` 或 `/风景` - 获取随机风景图
- `/看涩图` 或 `/涩图` 或 `/setu` - 获取随机涩图
- `/每日金句` 或 `/金句` 或 `/夸夸` - 获取夸赞ZerD的金句
- 直接发送消息（非命令）可进行AI对话

### 私聊命令

- `/看风景` 或 `/风景` - 获取随机风景图
- `/看涩图` 或 `/涩图` 或 `/setu` - 获取随机涩图
- `/每日金句` 或 `/金句` 或 `/夸夸` - 获取夸赞ZerD的金句
- 直接发送消息（非命令）可进行AI对话

## API说明

### 风景图API
- 地址：`https://t.alcy.cc/fj`
- 类型：直接返回图片
- 说明：API会重定向到实际的图片URL

### 涩图API
- 地址：`https://api.lolicon.app/setu/v2`
- 类型：返回JSON格式
- 图片链接位置：`data[0].urls.original`
- 参数：
  - `r18`: 0=非R18, 1=R18, 2=混合
  - `num`: 返回数量
  - `size`: 图片大小（original, regular, small）

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
    ├── ai_chat.py        # AI对话功能
    ├── scenery.py        # 风景图功能
    ├── setu.py           # 涩图功能
    └── golden_sentence.py # 每日金句功能
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

3. **涩图功能**：
   - 默认返回非R18内容（`r18=0`）
   - 可在`plugins/setu.py`中修改`r18`参数：
     - `0` = 非R18
     - `1` = R18
     - `2` = 混合

4. **图片发送**：
   - 使用QQ官方API的富媒体消息类型（msg_type=7）
   - 需要先通过`post_group_file`或`post_direct_file`上传文件资源
   - 然后使用返回的media对象发送消息

5. **沙箱环境**：
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
