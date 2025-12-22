# 快速启动指南

## 5分钟快速上手

### 前置要求

**重要**：需要 Python 3.8 或更高版本！

检查Python版本：
```bash
python --version
```

如果版本低于3.8，请先升级Python（参考`PYTHON_VERSION.md`或`SETUP_GUIDE.md`）。

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

如果遇到SSL证书问题或权限问题，使用国内镜像并添加`--user`参数：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

### 第二步：获取QQ机器人凭证

1. 访问 [QQ开放平台](https://bot.q.qq.com/)
2. 登录并创建机器人应用
3. 获取 `AppID` 和 `Secret`
4. 配置机器人的消息接收方式（Webhook或WebSocket）

### 第三步：配置机器人

编辑 `config.yaml` 文件：

```yaml
# 机器人配置
appid: "你的AppID"
secret: "你的Secret"
```

### 第四步：启动机器人

```bash
python bot.py
```

### 第五步：测试功能

在QQ中测试以下功能：

**群聊**（需要@机器人）：
- `/看风景` - 获取风景图
- `/看涩图` - 获取涩图
- `/每日金句` - 获取金句
- 直接发送消息进行AI对话

**私聊**：
- `/看风景` - 获取风景图
- `/看涩图` - 获取涩图
- `/每日金句` - 获取金句
- 直接发送消息进行AI对话

## 常见问题

### Q: 机器人没有响应？
A: 检查以下几点：
1. `config.yaml`中的appid和secret是否正确
2. QQ开放平台中机器人应用是否已启用
3. 机器人的消息接收配置是否正确
4. 查看控制台是否有错误信息

### Q: AI对话功能不工作？
A: AI对话功能默认使用简单回复模式。如需完整功能：
1. 在`config.yaml`中配置`AI_API_KEY`
2. 配置`AI_BASE_URL`（默认是OpenAI API地址）

### Q: 如何修改涩图的R18设置？
A: 编辑`plugins/setu.py`，修改第25行的`r18`参数：
- `0` = 非R18（默认）
- `1` = R18
- `2` = 混合

### Q: 沙箱环境和生产环境的区别？
A: 
- 沙箱环境（`is_sandbox=True`）：用于测试，消息不会真正发送
- 生产环境（`is_sandbox=False`）：正式环境，消息会真实发送

### Q: 如何配置消息接收？
A: 在QQ开放平台中：
1. 选择Webhook方式：需要提供公网可访问的回调地址
2. 选择WebSocket方式：需要配置WebSocket连接地址

## 需要帮助？

查看完整的`README.md`文档获取更多信息。

