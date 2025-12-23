"""
涩图功能
命令：/看涩图
调用 https://api.lolicon.app/setu/v2 API 获取随机涩图
API返回JSON格式，图片链接在json.data[0].urls.original中
"""

import httpx
import json
from botpy.message import GroupMessage, DirectMessage
from botpy import logging
from .utils import get_user_name

_log = logging.get_logger()

setu = None  # 占位符，保持兼容性


async def handle_setu(message: GroupMessage):
    """处理群聊看涩图命令"""
    try:
        # 调用API获取涩图信息
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 调用lolicon API，参数可以自定义
            params = {
                "r18": 0,  # 0为非R18，1为R18，2为混合
                "num": 1,  # 返回数量
                "size": "original"  # 图片大小：original, regular, small
            }
            
            response = await client.get(
                "https://api.lolicon.app/setu/v2",
                params=params
            )
            response.raise_for_status()
            
            # 解析JSON响应
            data = response.json()
            
            # 检查是否有错误
            if data.get("error"):
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"API返回错误：{data['error']}"
                )
                return
            
            # 获取图片信息
            if not data.get("data") or len(data["data"]) == 0:
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="没有找到图片，请稍后再试~"
                )
                return
            
            image_info = data["data"][0]
            image_url = image_info.get("urls", {}).get("original")
            
            if not image_url:
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="图片链接获取失败~"
                )
                return
            
            # 构建消息，包含图片和相关信息
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
                file_type=1,  # 1表示图片
                url=image_url
            )
            
            # 发送图片消息（富媒体类型）
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=file_result
            )
            
    except httpx.TimeoutException:
        _log.error("获取涩图超时")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content="获取涩图超时，请稍后再试~"
        )
    except json.JSONDecodeError as e:
        _log.error(f"解析JSON错误: {e}")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content="解析API响应失败，请稍后再试~"
        )
    except httpx.HTTPStatusError as e:
        _log.error(f"获取涩图HTTP错误: {e}")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content="获取涩图失败，服务器可能暂时不可用~"
        )
    except Exception as e:
        _log.error(f"获取涩图错误: {e}")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=f"获取涩图时出现错误：{str(e)}"
        )


async def handle_setu_dm(message: DirectMessage):
    """处理私聊看涩图命令"""
    try:
        # 调用API获取涩图信息
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 调用lolicon API，参数可以自定义
            params = {
                "r18": 0,  # 0为非R18，1为R18，2为混合
                "num": 1,  # 返回数量
                "size": "original"  # 图片大小：original, regular, small
            }
            
            response = await client.get(
                "https://api.lolicon.app/setu/v2",
                params=params
            )
            response.raise_for_status()
            
            # 解析JSON响应
            data = response.json()
            
            # 检查是否有错误
            if data.get("error"):
                await message._api.post_direct_message(
                    guild_id=message.guild_id,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"API返回错误：{data['error']}"
                )
                return
            
            # 获取图片信息
            if not data.get("data") or len(data["data"]) == 0:
                await message._api.post_direct_message(
                    guild_id=message.guild_id,
                    msg_type=0,
                    msg_id=message.id,
                    content="没有找到图片，请稍后再试~"
                )
                return
            
            image_info = data["data"][0]
            image_url = image_info.get("urls", {}).get("original")
            
            if not image_url:
                await message._api.post_direct_message(
                    guild_id=message.guild_id,
                    msg_type=0,
                    msg_id=message.id,
                    content="图片链接获取失败~"
                )
                return
            
            # 构建消息，包含图片和相关信息
            title = image_info.get("title", "未知标题")
            author = image_info.get("author", "未知作者")
            pid = image_info.get("pid", "未知")
            
            # 先发送文字信息
            text_content = f"标题：{title}\n作者：{author}\nPID：{pid}"
            await message._api.post_direct_message(
                guild_id=message.guild_id,
                msg_type=0,
                msg_id=message.id,
                content=text_content
            )
            
            # 上传文件资源
            file_result = await message._api.post_direct_file(
                guild_id=message.guild_id,
                file_type=1,  # 1表示图片
                url=image_url
            )
            
            # 发送图片消息（富媒体类型）
            await message._api.post_direct_message(
                guild_id=message.guild_id,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=file_result
            )
            
    except httpx.TimeoutException:
        _log.error("获取涩图超时")
        await message._api.post_direct_message(
            guild_id=message.guild_id,
            msg_type=0,
            msg_id=message.id,
            content="获取涩图超时，请稍后再试~"
        )
    except json.JSONDecodeError as e:
        _log.error(f"解析JSON错误: {e}")
        await message._api.post_direct_message(
            guild_id=message.guild_id,
            msg_type=0,
            msg_id=message.id,
            content="解析API响应失败，请稍后再试~"
        )
    except httpx.HTTPStatusError as e:
        _log.error(f"获取涩图HTTP错误: {e}")
        await message._api.post_direct_message(
            guild_id=message.guild_id,
            msg_type=0,
            msg_id=message.id,
            content="获取涩图失败，服务器可能暂时不可用~"
        )
    except Exception as e:
        _log.error(f"获取涩图错误: {e}")
        await message._api.post_direct_message(
            guild_id=message.guild_id,
            msg_type=0,
            msg_id=message.id,
            content=f"获取涩图时出现错误：{str(e)}"
        )
