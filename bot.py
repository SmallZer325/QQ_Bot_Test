"""
QQ机器人主程序 - 使用qq-botpy框架（QQ群机器人）
功能通过plugins模块实现
"""

import os
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, DirectMessage

# 导入插件
from plugins import scenery, golden_sentence, ai_chat, chengyu, utils
from plugins import setu_new as setu

# 读取配置
config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()


class MyClient(botpy.Client):
    """QQ机器人客户端（QQ群）"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_messages = set()  # 用于去重，避免重复处理同一条消息
        # 将成语接龙状态管理器传递给插件
        chengyu.chengyu_games = {}
    
    async def on_ready(self):
        """机器人准备就绪"""
        _log.info(f"机器人 「{self.robot.name}」 已启动！")
        print(f"[Info] 机器人 「{self.robot.name}」 已启动！")
        print(f"[Info] 机器人ID: {self.robot.id}")
        print("[Info] 等待接收消息...")
    
    async def on_group_at_message_create(self, message: GroupMessage):
        """处理QQ群@消息"""
        try:
            # 消息去重：如果已经处理过这条消息，直接返回
            if message.id in self.processed_messages:
                print(f"[Debug] 消息 {message.id} 已处理过，跳过")
                return
            
            # 标记消息已处理
            self.processed_messages.add(message.id)
            # 限制去重集合大小，避免内存泄漏（保留最近1000条）
            if len(self.processed_messages) > 1000:
                # 移除最旧的一些消息ID（简单处理：清空一半）
                self.processed_messages = set(list(self.processed_messages)[500:])
            
            print(f"[Debug] ========== 收到QQ群@消息 ==========")
            print(f"[Debug] 消息对象类型: {type(message)}")
            print(f"[Debug] 消息原始内容: {repr(message.content)}")
            
            msg = message.content.strip() if hasattr(message, 'content') else ''
            group_openid = message.group_openid if hasattr(message, 'group_openid') else 'N/A'
            member_openid = message.author.member_openid if hasattr(message, 'author') and hasattr(message.author, 'member_openid') else 'N/A'
            
            # 获取用户名
            user_name = utils.get_user_name(message)
            print(f"[Info] 收到QQ群@消息：{msg}")
            print(f"[Debug] 消息ID: {message.id}, 群ID: {group_openid}, 用户ID: {member_openid}, 用户名: {user_name}")
            
            # 移除@机器人的部分
            if "@" in msg:
                # 简单处理，移除@部分
                msg = msg.split("@")[0].strip()
            
            print(f"[Debug] 处理后的消息：{msg}")
            
            # 检查是否正在进行成语接龙
            if chengyu.is_chengyu_game_active(group_openid):
                # 如果正在进行接龙，优先处理接龙逻辑
                print("[Debug] 检测到正在进行成语接龙，处理接龙逻辑")
                await chengyu.handle_chengyu_reply(message, msg)
                return
            
            # 处理命令
            if msg.startswith("/看风景") or msg.startswith("/风景"):
                print("[Debug] 执行看风景命令")
                await scenery.handle_scenery(message)
            
            elif msg.startswith("/看setu") or msg.startswith("/setu") or msg.startswith("/看涩图") or msg.startswith("/涩图"):
                print("[Debug] 执行看setu命令")
                await setu.handle_setu(message)
            
            elif msg.startswith("/每日金句") or msg.startswith("/金句") or msg.startswith("/夸夸"):
                print("[Debug] 执行每日金句命令")
                await golden_sentence.handle_golden_sentence(message)
            
            elif msg.startswith("/成语接龙") or msg.startswith("/接龙"):
                print("[Debug] 执行成语接龙命令")
                await chengyu.handle_chengyu_start(message)
            
            elif msg.startswith("/"):
                # 其他命令，发送帮助信息
                print("[Debug] 执行帮助命令")
                help_text = f"""{user_name}，可用命令：
/看风景 - 获取随机风景图
/看setu - 获取随机图片
/每日金句 - 获取夸赞ZerD的金句
/夸夸 - 获取夸赞ZerD的金句
/成语接龙 - 开始成语接龙游戏

直接发送消息（非命令）可进行AI对话"""
                try:
                    await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=help_text
                    )
                    print("[Debug] 帮助消息发送成功")
                except Exception as e:
                    print(f"[Error] 发送帮助消息失败: {e}")
                    import traceback
                    traceback.print_exc()
            
            else:
                # 非命令消息，作为AI对话处理
                print("[Debug] 执行AI对话")
                await ai_chat.handle_ai_chat(message)
        
        except Exception as e:
            _log.error(f"处理QQ群消息时出错: {e}")
            print(f"[Error] 处理QQ群消息时出错: {e}")
            import traceback
            traceback.print_exc()
    
    async def on_direct_message_create(self, message: DirectMessage):
        """处理私聊消息"""
        try:
            print(f"[Debug] ========== 收到私聊消息 ==========")
            print(f"[Debug] 消息对象类型: {type(message)}")
            print(f"[Debug] 消息原始内容: {repr(message.content)}")
            
            msg = message.content.strip()
            print(f"[Info] 收到私聊消息：{msg}")
            
            # 处理命令（私聊暂时使用文本回复）
            if msg.startswith("/每日金句") or msg.startswith("/金句") or msg.startswith("/夸夸"):
                await golden_sentence.handle_golden_sentence_dm(message)
            else:
                await message._api.post_direct_message(
                    guild_id=message.guild_id,
                    msg_type=0,
                    msg_id=message.id,
                    content="私聊功能开发中，请在群聊中使用命令"
                )
        
        except Exception as e:
            _log.error(f"处理私聊消息时出错: {e}")
            print(f"[Error] 处理私聊消息时出错: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # 设置需要监听的事件通道
    # 对于QQ群机器人，需要监听公域消息
    # public_messages=True 表示监听公域消息（包括群@消息）
    # direct_message=True 表示监听私聊消息
    intents = botpy.Intents(public_messages=True, direct_message=True)
    
    # 创建客户端
    # is_sandbox=True 表示沙箱环境（测试环境）
    # is_sandbox=False 表示生产环境（会真正发送消息）
    # 注意：您在QQ开放平台配置的是沙箱环境，所以这里应该设为True
    client = MyClient(intents=intents, is_sandbox=True)
    
    print(f"[Info] 机器人配置: appid={config['appid']}, is_sandbox=True")
    print("[Info] 开始启动机器人...")
    
    # 运行机器人
    client.run(appid=config["appid"], secret=config["secret"])
