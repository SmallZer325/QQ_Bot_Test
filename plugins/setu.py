"""
涩图功能
命令：/看涩图
调用 https://api.lolicon.app/setu/v2 API 获取随机涩图
API返回JSON格式，图片链接在json.data[0].urls.original中
"""

import httpx
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger

setu = on_command("看涩图", aliases={"涩图", "色图", "setu"}, priority=5)

@setu.handle()
async def handle_setu(bot: Bot, event: Event):
    """处理看涩图命令"""
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
                await setu.finish(f"API返回错误：{data['error']}")
            
            # 获取图片信息
            if not data.get("data") or len(data["data"]) == 0:
                await setu.finish("没有找到图片，请稍后再试~")
            
            image_info = data["data"][0]
            image_url = image_info.get("urls", {}).get("original")
            
            if not image_url:
                await setu.finish("图片链接获取失败~")
            
            # 构建消息，包含图片和相关信息
            title = image_info.get("title", "未知标题")
            author = image_info.get("author", "未知作者")
            pid = image_info.get("pid", "未知")
            
            # 发送图片和文字信息
            message = f"标题：{title}\n作者：{author}\nPID：{pid}\n"
            await setu.send(message)
            await setu.finish(MessageSegment.image(image_url))
            
    except httpx.TimeoutException:
        logger.error("获取涩图超时")
        await setu.finish("获取涩图超时，请稍后再试~")
    except json.JSONDecodeError as e:
        logger.error(f"解析JSON错误: {e}")
        await setu.finish("解析API响应失败，请稍后再试~")
    except httpx.HTTPStatusError as e:
        logger.error(f"获取涩图HTTP错误: {e}")
        await setu.finish("获取涩图失败，服务器可能暂时不可用~")
    except Exception as e:
        logger.error(f"获取涩图错误: {e}")
        await setu.finish(f"获取涩图时出现错误：{str(e)}")

