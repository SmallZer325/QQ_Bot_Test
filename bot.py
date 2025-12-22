"""
QQ机器人主程序
功能：
1. AI智能对话
2. /看风景 - 随机显示风景图
3. /看涩图 - 随机显示涩图
4. /每日金句 - 输出夸赞作者的金句
"""

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter

# 初始化NoneBot（会自动加载nonebot_config.py）
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

# 加载插件
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run()

