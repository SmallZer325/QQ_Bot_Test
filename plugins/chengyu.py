"""
成语接龙功能
命令：/成语接龙 或 /接龙
实现成语接龙游戏，最大接龙量为50
使用 idiom.json 作为成语数据库
"""

import json
import os
import random
from botpy.message import GroupMessage
from botpy import logging
from .utils import get_user_name

_log = logging.get_logger()

# 成语接龙状态管理器
chengyu_games = {}

# 成语数据库（延迟加载）
_idiom_db = None
_idiom_dict_by_word = None  # 按成语文本索引：{word: idiom_data}
_idiom_dict_by_first_char = None  # 按首字索引：{first_char: [idiom_data, ...]}


def _load_idiom_db():
    """加载成语数据库"""
    global _idiom_db, _idiom_dict_by_word, _idiom_dict_by_first_char
    
    if _idiom_db is not None:
        return  # 已经加载过了
    
    try:
        # 获取idiom.json的路径
        idiom_path = os.path.join(os.path.dirname(__file__), "idiom.json")
        
        print(f"[Info] 正在加载成语数据库：{idiom_path}")
        with open(idiom_path, 'r', encoding='utf-8') as f:
            _idiom_db = json.load(f)
        
        # 构建索引
        _idiom_dict_by_word = {}
        _idiom_dict_by_first_char = {}
        
        for idiom in _idiom_db:
            word = idiom.get('word', '')
            if word and len(word) == 4:  # 只处理4字成语
                # 按成语文本索引
                _idiom_dict_by_word[word] = idiom
                
                # 按首字索引
                first_char = word[0]
                if first_char not in _idiom_dict_by_first_char:
                    _idiom_dict_by_first_char[first_char] = []
                _idiom_dict_by_first_char[first_char].append(idiom)
        
        print(f"[Info] 成语数据库加载完成，共 {len(_idiom_db)} 条成语")
        print(f"[Info] 4字成语：{len(_idiom_dict_by_word)} 条")
        
    except Exception as e:
        print(f"[Error] 加载成语数据库失败: {e}")
        import traceback
        traceback.print_exc()
        _idiom_db = []
        _idiom_dict_by_word = {}
        _idiom_dict_by_first_char = {}


def check_chengyu(word: str) -> bool:
    """检查是否为成语（同步函数）"""
    # 确保数据库已加载
    _load_idiom_db()
    
    # 首先检查基本格式：4个汉字
    if len(word) != 4 or not all('\u4e00' <= char <= '\u9fff' for char in word):
        return False
    
    # 在数据库中查找
    return word in _idiom_dict_by_word


def find_next_chengyu(last_char: str) -> str:
    """根据尾字查找下一个成语（同步函数）"""
    # 确保数据库已加载
    _load_idiom_db()
    
    # 在数据库中查找以last_char开头的成语
    if last_char in _idiom_dict_by_first_char:
        idioms = _idiom_dict_by_first_char[last_char]
        if idioms:
            # 随机选择一个成语
            selected = random.choice(idioms)
            return selected.get('word', '')
    
    return None


def get_random_chengyu() -> str:
    """获取随机成语作为起始（同步函数）"""
    # 确保数据库已加载
    _load_idiom_db()
    
    if not _idiom_dict_by_word:
        # 如果数据库为空，使用备用列表
        common_chengyu = [
            "画龙点睛", "一马当先", "三心二意", "五湖四海", "七上八下",
            "九牛一毛", "十全十美", "百发百中", "千军万马", "万紫千红",
            "一心一意", "二话不说", "三言两语", "四面八方", "五颜六色",
            "六神无主", "七嘴八舌", "八仙过海", "九死一生", "十拿九稳"
        ]
        return random.choice(common_chengyu)
    
    # 从数据库中随机选择
    word = random.choice(list(_idiom_dict_by_word.keys()))
    return word


async def handle_chengyu_start(message: GroupMessage):
    """开始成语接龙游戏"""
    group_openid = message.group_openid
    user_name = get_user_name(message)
    
    # 初始化游戏状态
    start_chengyu = get_random_chengyu()
    chengyu_games[group_openid] = {
        'active': True,
        'current': start_chengyu,
        'count': 1,
        'last_char': start_chengyu[-1],  # 最后一个字
        'used_words': {start_chengyu}  # 已使用的成语集合，避免重复
    }
    
    reply = f"{user_name}，成语接龙开始！\n我来出题：{start_chengyu}\n请回复一个以「{start_chengyu[-1]}」开头的成语~"
    
    try:
        await message._api.post_group_message(
            group_openid=group_openid,
            msg_type=0,
            msg_id=message.id,
            content=reply
        )
        print(f"[Info] 成语接龙开始，起始成语：{start_chengyu}，群ID：{group_openid}")
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
        print(f"[Debug] 群 {group_openid} 没有进行中的游戏")
        return
    
    game_state = chengyu_games[group_openid]
    
    # 如果游戏未激活，忽略
    if not game_state.get('active', False):
        print(f"[Debug] 群 {group_openid} 的游戏未激活")
        return
    
    print(f"[Debug] 处理成语接龙回复：用户输入={user_input}，当前轮数={game_state['count']}，期望首字={game_state['last_char']}")
    
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
    if not check_chengyu(user_input):
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
    
    # 检查是否重复使用
    if user_input in game_state.get('used_words', set()):
        reply = f"{user_name}，您输入的「{user_input}」已经使用过了，游戏结束！\n共接龙 {game_state['count']} 轮。"
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
    game_state['used_words'].add(user_input)  # 记录已使用的成语
    
    # 查找下一个成语（避免重复）
    next_chengyu = None
    candidates = []
    
    if last_char in _idiom_dict_by_first_char:
        idioms = _idiom_dict_by_first_char[last_char]
        # 过滤掉已使用的成语
        unused_idioms = [idiom for idiom in idioms if idiom.get('word', '') not in game_state['used_words']]
        if unused_idioms:
            selected = random.choice(unused_idioms)
            next_chengyu = selected.get('word', '')
    
    if not next_chengyu:
        reply = f"{user_name}，您输入的「{user_input}」很好！但我找不到以「{last_char}」开头的未使用成语了，游戏结束！\n共接龙 {game_state['count']} 轮。"
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
    game_state['used_words'].add(next_chengyu)  # 记录机器人使用的成语
    
    reply = f"{user_name}，「{user_input}」✓\n我接：{next_chengyu}\n请回复一个以「{next_chengyu[-1]}」开头的成语~（第{game_state['count']}/50轮）"
    
    try:
        await message._api.post_group_message(
            group_openid=group_openid,
            msg_type=0,
            msg_id=message.id,
            content=reply
        )
        print(f"[Info] 成语接龙继续，当前轮数：{game_state['count']}，用户成语：{user_input}，机器人成语：{next_chengyu}")
    except Exception as e:
        print(f"[Error] 发送接龙消息失败: {e}")
        game_state['active'] = False


def is_chengyu_game_active(group_openid: str) -> bool:
    """检查指定群是否正在进行成语接龙"""
    return group_openid in chengyu_games and chengyu_games[group_openid].get('active', False)
