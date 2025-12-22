"""
风景图功能
命令：/看风景
调用 https://t.alcy.cc/fj API 获取随机风景图
"""

import httpx
from botpy.message import GroupMessage, DirectMessage
from botpy import logging

_log = logging.get_logger()


async def handle_scenery(message: GroupMessage):
    """处理群聊看风景命令"""
    try:
        # 调用API获取风景图
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            # 根据文档，风景横图的API是 https://t.alcy.cc/fj
            response = await client.get("https://t.alcy.cc/fj")
            response.raise_for_status()
            
            # API直接返回图片，获取最终URL
            image_url = str(response.url)
            
            # 先上传文件资源
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
                media=file_result,
                content="美丽的风景图来啦~"
            )
            
    except httpx.TimeoutException:
        _log.error("获取风景图超时")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content="获取风景图超时，请稍后再试~"
        )
    except httpx.HTTPStatusError as e:
        _log.error(f"获取风景图HTTP错误: {e}")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content="获取风景图失败，服务器可能暂时不可用~"
        )
    except Exception as e:
        _log.error(f"获取风景图错误: {e}")
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content="获取风景图时出现错误，请稍后再试~"
        )


async def handle_scenery_dm(message: DirectMessage):
    """处理私聊看风景命令"""
    try:
        # 调用API获取风景图
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            # 根据文档，风景横图的API是 https://t.alcy.cc/fj
            response = await client.get("https://t.alcy.cc/fj")
            response.raise_for_status()
            
            # API直接返回图片，获取最终URL
            image_url = str(response.url)
            
            # 私聊消息发送图片（使用通用API，根据实际API调整）
            # 注意：qq-botpy的私聊API可能不同，这里使用通用方式
            try:
                # 尝试使用私聊文件上传API
                file_result = await message._api.post_direct_file(
                    guild_id=message.guild_id,
                    file_type=1,
                    url=image_url
                )
                await message._api.post_direct_message(
                    guild_id=message.guild_id,
                    msg_type=7,
                    msg_id=message.id,
                    media=file_result,
                    content="美丽的风景图来啦~"
                )
            except AttributeError:
                # 如果API不存在，发送图片URL
                await message._api.post_direct_message(
                    guild_id=message.guild_id,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"美丽的风景图来啦~\n{image_url}"
                )
            
    except httpx.TimeoutException:
        _log.error("获取风景图超时")
        try:
            await message._api.post_direct_message(
                guild_id=message.guild_id,
                msg_type=0,
                msg_id=message.id,
                content="获取风景图超时，请稍后再试~"
            )
        except:
            pass
    except httpx.HTTPStatusError as e:
        _log.error(f"获取风景图HTTP错误: {e}")
        try:
            await message._api.post_direct_message(
                guild_id=message.guild_id,
                msg_type=0,
                msg_id=message.id,
                content="获取风景图失败，服务器可能暂时不可用~"
            )
        except:
            pass
    except Exception as e:
        _log.error(f"获取风景图错误: {e}")
        try:
            await message._api.post_direct_message(
                guild_id=message.guild_id,
                msg_type=0,
                msg_id=message.id,
                content="获取风景图时出现错误，请稍后再试~"
            )
        except:
            pass
