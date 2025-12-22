"""
QQ机器人主程序 - 使用qq-botpy框架（QQ群机器人）
功能：
1. AI智能对话
2. /看风景 - 随机显示风景图
3. /看涩图 - 随机显示涩图
4. /每日金句 - 输出夸赞作者的金句
"""

import os
import botpy
import httpx
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, DirectMessage

# 读取配置
config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()


class MyClient(botpy.Client):
    """QQ机器人客户端（QQ群）"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_messages = set()  # 用于去重，避免重复处理同一条消息
    
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
            
            print(f"[Info] 收到QQ群@消息：{msg}")
            print(f"[Debug] 消息ID: {message.id}, 群ID: {group_openid}, 用户ID: {member_openid}")
            
            # 移除@机器人的部分
            if "@" in msg:
                # 简单处理，移除@部分
                msg = msg.split("@")[0].strip()
            
            print(f"[Debug] 处理后的消息：{msg}")
            
            # 处理命令
            if msg.startswith("/看风景") or msg.startswith("/风景"):
                print("[Debug] 执行看风景命令")
                await self._handle_scenery_group(message)
            
            elif msg.startswith("/看涩图") or msg.startswith("/涩图") or msg.startswith("/setu"):
                print("[Debug] 执行看涩图命令")
                await self._handle_setu_group(message)
            
            elif msg.startswith("/每日金句") or msg.startswith("/金句") or msg.startswith("/夸夸"):
                print("[Debug] 执行每日金句命令")
                await self._handle_golden_sentence_group(message)
            
            elif msg.startswith("/"):
                # 其他命令，发送帮助信息
                print("[Debug] 执行帮助命令")
                help_text = """可用命令：
/看风景 - 获取随机风景图
/看涩图 - 获取随机涩图
/每日金句 - 获取夸赞ZerD的金句

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
                await self._handle_ai_chat_group(message)
        
        except Exception as e:
            _log.error(f"处理QQ群消息时出错: {e}")
            print(f"[Error] 处理QQ群消息时出错: {e}")
            import traceback
            traceback.print_exc()
    
    async def _handle_scenery_group(self, message: GroupMessage):
        """处理QQ群看风景命令"""
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.get("https://t.alcy.cc/fj")
                response.raise_for_status()
                image_url = str(response.url)
                
                # 上传文件资源
                file_result = await message._api.post_group_file(
                    group_openid=message.group_openid,
                    file_type=1,  # 1表示图片
                    url=image_url
                )
                
                # 发送图片消息
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=7,  # 7表示富媒体类型
                    msg_id=message.id,
                    media=file_result,
                    content="美丽的风景图来啦~"
                )
        except Exception as e:
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content="获取风景图失败，请稍后再试~"
            )
            print(f"[Error] 获取风景图失败: {e}")
            import traceback
            traceback.print_exc()
    
    async def _handle_setu_group(self, message: GroupMessage):
        """处理QQ群看涩图命令"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                params = {"r18": 0, "num": 1, "size": "original"}
                response = await client.get("https://api.lolicon.app/setu/v2", params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("error") or not data.get("data"):
                    await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="没有找到图片，请稍后再试~"
                    )
                    return
                
                image_info = data["data"][0]
                image_url = image_info.get("urls", {}).get("original")
                title = image_info.get("title", "未知标题")
                author = image_info.get("author", "未知作者")
                pid = image_info.get("pid", "未知")
                
                # 先发送文字信息
                text_content = f"标题：{title}\n作者：{author}\nPID：{pid}"
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=text_content
                )
                
                # 上传文件资源
                file_result = await message._api.post_group_file(
                    group_openid=message.group_openid,
                    file_type=1,
                    url=image_url
                )
                
                # 发送图片消息
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=7,
                    msg_id=message.id,
                    media=file_result
                )
        except Exception as e:
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content="获取涩图失败，请稍后再试~"
            )
            print(f"[Error] 获取涩图失败: {e}")
            import traceback
            traceback.print_exc()
    
    async def _handle_golden_sentence_group(self, message: GroupMessage):
        """处理QQ群每日金句命令"""
        import random
        sentences = [
            "ZerD，你是代码界的艺术家，每一行代码都闪耀着智慧的光芒！✨",
            "ZerD大佬，你的编程技术如行云流水，让人叹为观止！👏",
            "ZerD，你不仅技术精湛，更是将创意与代码完美融合的天才！🌟",
            "ZerD，你的代码就像诗一样优雅，每一个函数都是艺术品！💎",
            "ZerD大佬，你的编程思维深邃如海，让人望尘莫及！🌊",
        ]
        sentence = random.choice(sentences)
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=sentence
        )
    
    async def _handle_ai_chat_group(self, message: GroupMessage):
        """处理QQ群AI对话"""
        user_msg = message.content.strip() if hasattr(message, 'content') else ''
        if not user_msg:
            return
        
        reply = "我理解你说的是：" + user_msg + "\n（提示：AI对话功能需要配置API密钥）"
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=reply
        )
    
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
                import random
                sentences = [
                    "ZerD，你是代码界的艺术家，每一行代码都闪耀着智慧的光芒！✨",
                    "ZerD大佬，你的编程技术如行云流水，让人叹为观止！👏",
                ]
                sentence = random.choice(sentences)
                await message._api.post_direct_message(
                    guild_id=message.guild_id,
                    msg_type=0,
                    msg_id=message.id,
                    content=sentence
                )
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
