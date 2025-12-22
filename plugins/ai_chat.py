"""
AI智能对话功能
当用户发送消息时，如果不是命令，则作为AI对话处理
支持接入OpenAI、Claude等AI API
"""

import httpx
import os
from nonebot import on_message, get_driver
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.rule import Rule
from nonebot.params import CommandArg
from nonebot.log import logger

# 获取配置
driver = get_driver()
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")

# 检查消息是否为命令
def is_not_command(event: Event) -> bool:
    """检查消息是否不是命令（不以/开头）"""
    msg = str(event.get_message()).strip()
    return not msg.startswith('/')

# 创建消息处理器
ai_chat = on_message(rule=Rule(is_not_command), priority=10, block=False)

@ai_chat.handle()
async def handle_ai_chat(bot: Bot, event: Event):
    """处理AI对话"""
    # 忽略群聊中的@消息（避免刷屏）
    if event.message_type == "group":
        # 检查是否@了机器人
        if event.to_me:
            user_msg = str(event.get_message()).strip()
            # 移除@机器人的部分
            user_msg = user_msg.replace(f"[CQ:at,qq={event.self_id}]", "").strip()
        else:
            return  # 群聊中未@机器人，不响应
    else:
        user_msg = str(event.get_message()).strip()
    
    # 如果消息为空或是命令，不处理
    if not user_msg or user_msg.startswith('/'):
        return
    
    try:
        # 使用简单的AI回复（可以替换为实际的AI API）
        # 这里使用一个简单的回复逻辑，你可以替换为OpenAI、Claude等API
        reply = await get_ai_reply(user_msg)
        
        await ai_chat.finish(reply)
    except Exception as e:
        logger.error(f"AI对话处理错误: {e}")
        await ai_chat.finish("抱歉，我现在有点困惑，稍后再试吧~")

async def get_ai_reply(user_msg: str) -> str:
    """
    获取AI回复
    如果配置了AI_API_KEY，则调用真实的AI API
    否则使用简单的规则回复
    """
    # 如果配置了AI API密钥，调用真实API
    if AI_API_KEY:
        try:
            return await call_ai_api(user_msg)
        except Exception as e:
            logger.error(f"调用AI API失败: {e}")
            # API调用失败时回退到简单回复
            pass
    
    # 简单的关键词回复（未配置API时的备用方案）
    greetings = ["你好", "hello", "hi", "在吗", "在"]
    if any(g in user_msg.lower() for g in greetings):
        return "你好！我是ZerD开发的智能机器人，有什么可以帮助你的吗？"
    
    questions = ["什么", "怎么", "如何", "为什么"]
    if any(q in user_msg for q in questions):
        return "这是一个很好的问题！让我想想...（AI功能需要配置API密钥才能使用完整功能）"
    
    # 默认回复
    return f"我理解你说的是：{user_msg}\n（提示：AI对话功能需要配置API密钥，当前为简单回复模式）"

async def call_ai_api(user_msg: str) -> str:
    """
    调用AI API（OpenAI格式）
    可以根据需要修改为其他AI服务
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",  # 可以修改为其他模型
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个友好的QQ机器人助手，由ZerD开发。请用简短、友好的方式回复用户的问题。"
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ],
            "max_tokens": 150,  # 限制回复长度，保持简短
            "temperature": 0.7
        }
        
        response = await client.post(
            f"{AI_BASE_URL}/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

