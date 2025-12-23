"""
成语接龙功能
命令：/成语接龙 或 /接龙
实现成语接龙游戏，最大接龙量为50
"""

import httpx
import re
import random
from botpy.message import GroupMessage
from botpy import logging
from .utils import get_user_name

_log = logging.get_logger()

# 成语接龙状态管理器（在bot.py中初始化）
chengyu_games = {}


async def check_chengyu(word: str) -> bool:
    """检查是否为成语"""
    # 首先检查基本格式：4个汉字
    if len(word) != 4 or not all('\u4e00' <= char <= '\u9fff' for char in word):
        return False
    
    try:
        # 使用成语查询API验证
        async with httpx.AsyncClient(timeout=5.0) as client:
            # 使用多个API源进行验证
            # API 1: 便民查询网
            url1 = f"https://chengyu.bmcx.com/{word}__chengyu/"
            try:
                response = await client.get(url1, follow_redirects=True, timeout=3.0)
                if response.status_code == 200:
                    content = response.text
                    # 检查页面是否包含成语相关信息
                    if word in content and ("成语" in content or "释义" in content or "解释" in content or "拼音" in content):
                        return True
            except:
                pass
    except Exception as e:
        print(f"[Debug] 成语验证API调用失败: {e}")
    
    # 如果API验证失败，至少通过格式验证就认为可能是成语
    return True


async def find_next_chengyu(last_char: str) -> str:
    """根据尾字查找下一个成语"""
    # 内置成语库（按首字索引）
    chengyu_dict = {
        '点': ['点石成金', '点铁成金', '点头哈腰'],
        '睛': ['睛目不凡'],
        '先': ['先发制人', '先见之明', '先来后到'],
        '意': ['意气风发', '意味深长', '意犹未尽'],
        '海': ['海阔天空', '海纳百川', '海市蜃楼'],
        '下': ['下不为例', '下里巴人'],
        '毛': ['毛遂自荐', '毛骨悚然'],
        '中': ['中流砥柱', '中庸之道'],
        '马': ['马到成功', '马不停蹄', '马马虎虎'],
        '红': ['红红火火', '红颜知己'],
        '说': ['说三道四', '说一不二'],
        '语': ['语重心长', '语无伦次'],
        '方': ['方兴未艾', '方方正正'],
        '色': ['色厉内荏', '色胆包天'],
        '主': ['主次分明', '主观臆断'],
        '舌': ['舌战群儒', '舌敝唇焦'],
        '生': ['生龙活虎', '生机勃勃', '生不逢时'],
        '稳': ['稳如泰山', '稳操胜券'],
        '金': ['金玉满堂', '金科玉律', '金枝玉叶'],
        '堂': ['堂而皇之', '堂堂正正'],
        '之': ['之乎者也', '之死靡它'],
        '对': ['对牛弹琴', '对答如流'],
        '琴': ['琴棋书画', '琴瑟和鸣'],
        '画': ['画蛇添足', '画龙点睛', '画饼充饥'],
        '户': ['户枢不蠹', '户限为穿'],
    }
    
    # 先从内置字典查找
    if last_char in chengyu_dict:
        return random.choice(chengyu_dict[last_char])
    
    # 如果内置字典没有，尝试使用API
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # 使用成语接龙查询API
            url = f"https://chengyujielong.bmcx.com/{last_char}__chengyujielong/"
            response = await client.get(url, follow_redirects=True, timeout=3.0)
            if response.status_code == 200:
                content = response.text
                # 查找以last_char开头的4字成语
                pattern = rf'{re.escape(last_char)}[\u4e00-\u9fff]{{3}}'
                matches = re.findall(pattern, content)
                if matches:
                    # 随机返回一个匹配的成语
                    return random.choice(matches[:5])  # 取前5个，随机选一个
    except Exception as e:
        print(f"[Debug] 成语搜索API调用失败: {e}")
    
    # 如果都失败，返回None
    return None


async def get_random_chengyu() -> str:
    """获取随机成语作为起始"""
    # 常用成语列表（作为备选）
    common_chengyu = [
        "画龙点睛", "一马当先", "三心二意", "五湖四海", "七上八下",
        "九牛一毛", "十全十美", "百发百中", "千军万马", "万紫千红",
        "一心一意", "二话不说", "三言两语", "四面八方", "五颜六色",
        "六神无主", "七嘴八舌", "八仙过海", "九死一生", "十拿九稳"
    ]
    return random.choice(common_chengyu)


async def handle_chengyu_start(message: GroupMessage):
    """开始成语接龙游戏"""
    group_openid = message.group_openid
    user_name = get_user_name(message)
    
    # 初始化游戏状态
    start_chengyu = await get_random_chengyu()
    chengyu_games[group_openid] = {
        'active': True,
        'current': start_chengyu,
        'count': 1,
        'last_char': start_chengyu[-1]  # 最后一个字
    }
    
    reply = f"{user_name}，成语接龙开始！\n我来出题：{start_chengyu}\n请回复一个以「{start_chengyu[-1]}」开头的成语~"
    
    try:
        await message._api.post_group_message(
            group_openid=group_openid,
            msg_type=0,
            msg_id=message.id,
            content=reply
        )
        print(f"[Info] 成语接龙开始，起始成语：{start_chengyu}")
    except Exception as e:
        print(f"[Error] 发送接龙开始消息失败: {e}")
        # 如果发送失败，清除游戏状态
        if group_openid in chengyu_games:
            del chengyu_games[group_openid]


async def handle_chengyu_reply(message: GroupMessage, user_input: str):
    """处理成语接龙回复"""
    group_openid = message.group_openid
    user_name = get_user_name(message)
    
    if group_openid not in chengyu_games:
        return
    
    game_state = chengyu_games[group_openid]
    
    # 如果游戏未激活，忽略
    if not game_state.get('active', False):
        return
    
    # 检查是否达到最大接龙数
    if game_state['count'] >= 50:
        reply = f"{user_name}，已达到最大接龙数（50），游戏结束！"
        game_state['active'] = False
        try:
            await message._api.post_group_message(
                group_openid=group_openid,
                msg_type=0,
                msg_id=message.id,
                content=reply
            )
        except Exception as e:
            print(f"[Error] 发送游戏结束消息失败: {e}")
        return
    
    # 验证用户输入是否为成语
    if not await check_chengyu(user_input):
        reply = f"{user_name}，您输入的「{user_input}」不是成语，游戏结束！\n共接龙 {game_state['count']} 轮。"
        game_state['active'] = False
        try:
            await message._api.post_group_message(
                group_openid=group_openid,
                msg_type=0,
                msg_id=message.id,
                content=reply
            )
        except Exception as e:
            print(f"[Error] 发送游戏结束消息失败: {e}")
        return
    
    # 检查首字是否匹配
    expected_char = game_state['last_char']
    if user_input[0] != expected_char:
        reply = f"{user_name}，您输入的「{user_input}」首字是「{user_input[0]}」，但需要以「{expected_char}」开头，游戏结束！\n共接龙 {game_state['count']} 轮。"
        game_state['active'] = False
        try:
            await message._api.post_group_message(
                group_openid=group_openid,
                msg_type=0,
                msg_id=message.id,
                content=reply
            )
        except Exception as e:
            print(f"[Error] 发送游戏结束消息失败: {e}")
        return
    
    # 用户输入有效，更新状态
    game_state['count'] += 1
    last_char = user_input[-1]
    game_state['last_char'] = last_char
    
    # 查找下一个成语
    next_chengyu = await find_next_chengyu(last_char)
    
    if not next_chengyu:
        reply = f"{user_name}，您输入的「{user_input}」很好！但我找不到以「{last_char}」开头的成语了，游戏结束！\n共接龙 {game_state['count']} 轮。"
        game_state['active'] = False
        try:
            await message._api.post_group_message(
                group_openid=group_openid,
                msg_type=0,
                msg_id=message.id,
                content=reply
            )
        except Exception as e:
            print(f"[Error] 发送游戏结束消息失败: {e}")
        return
    
    # 找到下一个成语，继续游戏
    game_state['current'] = next_chengyu
    game_state['last_char'] = next_chengyu[-1]
    game_state['count'] += 1
    
    reply = f"{user_name}，「{user_input}」✓\n我接：{next_chengyu}\n请回复一个以「{next_chengyu[-1]}」开头的成语~（第{game_state['count']}/50轮）"
    
    try:
        await message._api.post_group_message(
            group_openid=group_openid,
            msg_type=0,
            msg_id=message.id,
            content=reply
        )
        print(f"[Info] 成语接龙继续，当前轮数：{game_state['count']}")
    except Exception as e:
        print(f"[Error] 发送接龙消息失败: {e}")
        game_state['active'] = False


def is_chengyu_game_active(group_openid: str) -> bool:
    """检查指定群是否正在进行成语接龙"""
    return group_openid in chengyu_games and chengyu_games[group_openid].get('active', False)

