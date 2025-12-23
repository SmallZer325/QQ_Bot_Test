"""
Setu功能（新API）
命令：/看setu
调用 https://hatsunemiku-tov.imwork.net/api/miku/?redirect=1 API 获取随机图片
"""

import httpx
from botpy.message import GroupMessage
from botpy import logging
from .utils import get_user_name

_log = logging.get_logger()


async def handle_setu(message: GroupMessage):
    """处理群聊看setu命令"""
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get("https://hatsunemiku-tov.imwork.net/api/miku/?redirect=1")
            response.raise_for_status()
            image_url = str(response.url)
            
            # 上传文件资源
            file_result = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,  # 1表示图片
                url=image_url
            )
            
            # 获取用户名
            user_name = get_user_name(message)
            # 发送图片消息
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=file_result,
                content=f"{user_name}，图片来啦~"
            )
    except Exception as e:
        user_name = get_user_name(message)
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=f"{user_name}，获取图片失败，请稍后再试~"
        )
        print(f"[Error] 获取setu失败: {e}")
        import traceback
        traceback.print_exc()

