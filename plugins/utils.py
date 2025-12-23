"""
工具函数
提供通用的辅助功能，如获取用户名等
"""

from botpy.message import GroupMessage


def get_user_name(message: GroupMessage) -> str:
    """获取用户QQ名（昵称）"""
    try:
        # 尝试从message.author获取用户名
        if hasattr(message, 'author') and message.author:
            # 尝试获取member_nick（群昵称）
            if hasattr(message.author, 'member_nick') and message.author.member_nick:
                return message.author.member_nick
            # 尝试获取username（用户名）
            if hasattr(message.author, 'username') and message.author.username:
                return message.author.username
            # 尝试获取nick（昵称）
            if hasattr(message.author, 'nick') and message.author.nick:
                return message.author.nick
    except Exception as e:
        print(f"[Debug] 获取用户名失败: {e}")
    
    # 如果都获取不到，返回默认值
    return "朋友"

