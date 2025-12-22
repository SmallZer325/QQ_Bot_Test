"""
AI智能对话功能
当用户发送消息时，如果不是命令，则作为AI对话处理
支持接入OpenAI、Claude等AI API
"""

import httpx
import os
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, DirectMessage
from botpy import logging

_log = logging.get_logger()

# 读取配置
# 从plugins目录向上一级到项目根目录
config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
config = read(os.path.normpath(config_path))
AI_API_KEY = config.get("AI_API_KEY", "")
AI_BASE_URL = config.get("AI_BASE_URL", "https://api.openai.com/v1")


async def handle_ai_chat(message: GroupMessage):
    """处理群聊AI对话"""
    user_msg = message.content.strip()
    
    # 如果消息为空或是命令，不处理
    if not user_msg or user_msg.startswith('/'):
        return
    
    try:
        # 获取AI回复
        reply = await get_ai_reply(user_msg)
        
        # 发送回复
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=reply
        )
    except Exception as e:
        _log.error(f"AI对话处理错误: {e}")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content="抱歉，我现在有点困惑，稍后再试吧~"
        )


async def handle_ai_chat_dm(message: DirectMessage):
    """处理私聊AI对话"""
    user_msg = message.content.strip()
    
    # 如果消息为空或是命令，不处理
    if not user_msg or user_msg.startswith('/'):
        return
    
    try:
        # 获取AI回复
        reply = await get_ai_reply(user_msg)
        
        # 发送回复
        await message._api.post_direct_message(
            guild_id=message.guild_id,
            msg_type=0,
            msg_id=message.id,
            content=reply
        )
    except Exception as e:
        _log.error(f"AI对话处理错误: {e}")
        await message._api.post_direct_message(
            guild_id=message.guild_id,
            msg_type=0,
            msg_id=message.id,
            content="抱歉，我现在有点困惑，稍后再试吧~"
        )


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
            _log.error(f"调用AI API失败: {e}")
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
