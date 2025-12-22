"""
QQ机器人主程序 - 使用qq-botpy框架
功能：
1. AI智能对话
2. /看风景 - 随机显示风景图
3. /看涩图 - 随机显示涩图
4. /每日金句 - 输出夸赞作者的金句
"""

import os
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, DirectMessage

# 导入插件
from plugins import ai_chat, scenery, setu, golden_sentence

# 读取配置
config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()


class MyClient(botpy.Client):
    """QQ机器人客户端"""
    
    async def on_ready(self):
        """机器人准备就绪"""
        _log.info(f"机器人 「{self.robot.name}」 已启动！")
        print(f"[Info] 机器人 「{self.robot.name}」 已启动！")
    
    async def on_group_at_message_create(self, message: GroupMessage):
        """处理群@消息"""
        msg = message.content.strip()
        member_openid = message.author.member_openid
        group_openid = message.group_openid
        
        print(f"[Info] 收到群消息：{msg}")
        
        # 移除@机器人的部分
        if "@" in msg:
            # 简单处理，移除@部分
            msg = msg.split("@")[0].strip()
        
        # 处理命令
        if msg.startswith("/看风景") or msg.startswith("/风景"):
            await scenery.handle_scenery(message)
        
        elif msg.startswith("/看涩图") or msg.startswith("/涩图") or msg.startswith("/setu"):
            await setu.handle_setu(message)
        
        elif msg.startswith("/每日金句") or msg.startswith("/金句") or msg.startswith("/夸夸"):
            await golden_sentence.handle_golden_sentence(message)
        
        elif msg.startswith("/"):
            # 其他命令，发送帮助信息
            help_text = """
可用命令：
/看风景 - 获取随机风景图
/看涩图 - 获取随机涩图
/每日金句 - 获取夸赞ZerD的金句

直接发送消息（非命令）可进行AI对话
            """
            await message._api.post_group_message(
                group_openid=group_openid,
                msg_type=0,
                msg_id=message.id,
                content=help_text.strip()
            )
        
        else:
            # 非命令消息，作为AI对话处理
            await ai_chat.handle_ai_chat(message)
    
    async def on_direct_message_create(self, message: DirectMessage):
        """处理私聊消息"""
        msg = message.content.strip()
        print(f"[Info] 收到私聊消息：{msg}")
        
        # 处理命令
        if msg.startswith("/看风景") or msg.startswith("/风景"):
            await scenery.handle_scenery_dm(message)
        
        elif msg.startswith("/看涩图") or msg.startswith("/涩图") or msg.startswith("/setu"):
            await setu.handle_setu_dm(message)
        
        elif msg.startswith("/每日金句") or msg.startswith("/金句") or msg.startswith("/夸夸"):
            await golden_sentence.handle_golden_sentence_dm(message)
        
        elif msg.startswith("/"):
            # 其他命令，发送帮助信息
            help_text = """
可用命令：
/看风景 - 获取随机风景图
/看涩图 - 获取随机涩图
/每日金句 - 获取夸赞ZerD的金句

直接发送消息（非命令）可进行AI对话
            """
            await message._api.post_direct_message(
                guild_id=message.guild_id,
                msg_type=0,
                msg_id=message.id,
                content=help_text.strip()
            )
        
        else:
            # 非命令消息，作为AI对话处理
            await ai_chat.handle_ai_chat_dm(message)


if __name__ == "__main__":
    # 设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True, direct_message=True)
    
    # 创建客户端（is_sandbox=True 表示沙箱环境，生产环境设为False）
    client = MyClient(intents=intents, is_sandbox=True)
    
    # 运行机器人
    client.run(appid=config["appid"], secret=config["secret"])
