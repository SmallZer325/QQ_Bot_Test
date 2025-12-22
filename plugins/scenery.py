"""
风景图功能
命令：/看风景
调用 https://t.alcy.cc/fj API 获取随机风景图
"""

import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger

scenery = on_command("看风景", aliases={"风景", "风景图"}, priority=5)

@scenery.handle()
async def handle_scenery(bot: Bot, event: Event):
    """处理看风景命令"""
    try:
        # 调用API获取风景图
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 根据文档，风景横图的API是 https://t.alcy.cc/fj
            response = await client.get("https://t.alcy.cc/fj", follow_redirects=True)
            response.raise_for_status()
            
            # API直接返回图片，获取最终URL
            image_url = str(response.url)
            
            # 发送图片
            await scenery.finish(MessageSegment.image(image_url))
            
    except httpx.TimeoutException:
        logger.error("获取风景图超时")
        await scenery.finish("获取风景图超时，请稍后再试~")
    except httpx.HTTPStatusError as e:
        logger.error(f"获取风景图HTTP错误: {e}")
        await scenery.finish("获取风景图失败，服务器可能暂时不可用~")
    except Exception as e:
        logger.error(f"获取风景图错误: {e}")
        await scenery.finish("获取风景图时出现错误，请稍后再试~")

