# 快速启动指南

## 5分钟快速上手

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

### 第二步：配置环境

1. 复制环境变量文件：
```bash
# Windows PowerShell
Copy-Item .env.example .env

# 或手动创建 .env 文件
```

2. 编辑 `.env` 文件，设置go-cqhttp的连接信息：
```
HOST=127.0.0.1
PORT=8080
```

3. 编辑 `nonebot_config.py`，设置你的QQ号：
```python
SUPERUSERS = {你的QQ号}
```

### 第三步：配置go-cqhttp

1. 下载go-cqhttp：https://github.com/Mrs4s/go-cqhttp/releases
2. 运行go-cqhttp，首次运行会生成`config.yml`
3. 编辑`config.yml`，配置HTTP API或反向WebSocket：

**HTTP API配置示例：**
```yaml
servers:
  - http:
      host: 127.0.0.1
      port: 8080
```

**反向WebSocket配置示例（推荐）：**
```yaml
servers:
  - ws-reverse:
      universal: ws://127.0.0.1:8080/ws
```

4. 登录QQ并启动go-cqhttp

### 第四步：启动机器人

```bash
python bot.py
```

或者使用nb命令：
```bash
nb run
```

### 第五步：测试功能

在QQ中发送以下命令测试：

- `/看风景` - 获取风景图
- `/看涩图` - 获取涩图
- `/每日金句` - 获取金句
- 直接发送消息（私聊）或@机器人（群聊）进行AI对话

## 常见问题

### Q: 机器人没有响应？
A: 检查以下几点：
1. go-cqhttp是否正常运行
2. `.env`中的HOST和PORT是否与go-cqhttp配置一致
3. 查看控制台是否有错误信息

### Q: AI对话功能不工作？
A: AI对话功能默认使用简单回复模式。如需完整功能：
1. 在`.env`中配置`AI_API_KEY`
2. 配置`AI_BASE_URL`（默认是OpenAI API地址）

### Q: 如何修改涩图的R18设置？
A: 编辑`plugins/setu.py`，修改第24行的`r18`参数：
- `0` = 非R18（默认）
- `1` = R18
- `2` = 混合

## 需要帮助？

查看完整的`README.md`文档获取更多信息。

