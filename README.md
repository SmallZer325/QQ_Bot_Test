# QQ机器人测试项目

一个功能丰富的QQ机器人，由ZerD开发。

## 功能列表

1. **AI智能对话** - 与机器人进行简短对话（需要配置AI API）
2. **看风景** - 使用 `/看风景` 命令随机显示风景图
3. **看涩图** - 使用 `/看涩图` 命令随机显示涩图（来自lolicon API）
4. **每日金句** - 使用 `/每日金句` 命令获取夸赞作者ZerD的金句

## 安装步骤

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Windows CMD
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件，配置go-cqhttp的连接信息。

### 2.5. 配置机器人设置

编辑 `nonebot_config.py`，设置你的QQ号为超级用户：

```python
SUPERUSERS = {你的QQ号}
```

### 3. 配置go-cqhttp

本项目使用NoneBot2框架，需要配合go-cqhttp使用。

1. 下载go-cqhttp：https://github.com/Mrs4s/go-cqhttp/releases
2. 配置go-cqhttp的`config.yml`，设置HTTP API地址和端口
3. 启动go-cqhttp

### 4. 运行机器人

```bash
python bot.py
```

或者使用nb命令：

```bash
nb run
```

## 命令说明

- `/看风景` 或 `/风景` - 获取随机风景图
- `/看涩图` 或 `/涩图` 或 `/setu` - 获取随机涩图
- `/每日金句` 或 `/金句` 或 `/夸夸` - 获取夸赞ZerD的金句

## API说明

### 风景图API
- 地址：`https://t.alcy.cc/fj`
- 类型：直接返回图片

### 涩图API
- 地址：`https://api.lolicon.app/setu/v2`
- 类型：返回JSON格式
- 图片链接位置：`data[0].urls.original`

## 项目结构

```
QQ_Bot_Test/
├── bot.py                 # 主程序入口
├── requirements.txt       # Python依赖
├── pyproject.toml         # 项目配置
├── .env.example          # 环境变量示例
├── README.md             # 说明文档
└── plugins/              # 插件目录
    ├── __init__.py
    ├── ai_chat.py        # AI对话功能
    ├── scenery.py        # 风景图功能
    ├── setu.py           # 涩图功能
    └── golden_sentence.py # 每日金句功能
```

## 注意事项

1. **AI对话功能**：
   - 默认使用简单回复模式
   - 如需完整AI功能，在`.env`中配置`AI_API_KEY`和`AI_BASE_URL`
   - 支持OpenAI格式的API（如OpenAI、Azure OpenAI等）
   - 群聊中使用AI对话功能需要@机器人

2. **涩图功能**：
   - 默认返回非R18内容（`r18=0`）
   - 可在`plugins/setu.py`中修改`r18`参数：
     - `0` = 非R18
     - `1` = R18
     - `2` = 混合

3. **go-cqhttp配置**：
   - 确保go-cqhttp正常运行
   - 配置HTTP API地址和端口与`.env`中的配置一致
   - 建议使用反向WebSocket连接，更稳定

4. **其他**：
   - 风景图API直接返回图片，无需额外处理
   - 涩图API返回JSON，程序会自动解析并提取图片链接

## 开发者

ZerD - 代码界的艺术家，编程技术的引领者！

## 许可证

本项目仅供学习交流使用。

