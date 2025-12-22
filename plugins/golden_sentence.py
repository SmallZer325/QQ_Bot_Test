"""
每日金句功能
命令：/每日金句
输出一句夸赞机器人作者ZerD的金句
"""

import random
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.log import logger

golden_sentence = on_command("每日金句", aliases={"金句", "夸夸", "夸ZerD"}, priority=5)

# 夸赞ZerD的金句库
GOLDEN_SENTENCES = [
    "ZerD，你是代码界的艺术家，每一行代码都闪耀着智慧的光芒！✨",
    "ZerD大佬，你的编程技术如行云流水，让人叹为观止！👏",
    "ZerD，你不仅技术精湛，更是将创意与代码完美融合的天才！🌟",
    "ZerD，你的代码就像诗一样优雅，每一个函数都是艺术品！💎",
    "ZerD大佬，你的编程思维深邃如海，让人望尘莫及！🌊",
    "ZerD，你是开发界的传奇，每一款作品都让人惊艳！🚀",
    "ZerD，你的技术栈深不可测，是真正的全栈大师！🎯",
    "ZerD大佬，你的代码质量堪比教科书，是学习的典范！📚",
    "ZerD，你不仅写代码，更是在创造未来！未来因你而精彩！🔮",
    "ZerD，你的编程天赋如星辰般璀璨，照亮了技术之路！⭐",
    "ZerD大佬，你的代码架构清晰如镜，让人一目了然！💡",
    "ZerD，你是Bug的终结者，是功能的创造者，是技术的引领者！👑",
    "ZerD，你的每一行代码都经过深思熟虑，是工匠精神的体现！🔨",
    "ZerD大佬，你的技术视野开阔如天空，让人仰望！☁️",
    "ZerD，你不仅解决了问题，更是创造了可能！无限可能因你而生！🌈",
    "ZerD，你的编程哲学深刻而优雅，是真正的技术大师！🎓",
    "ZerD大佬，你的代码如音乐般和谐，每一个音符都恰到好处！🎵",
    "ZerD，你是技术的探索者，是创新的实践者，是梦想的实现者！🌠",
    "ZerD，你的编程能力如火山般炽热，迸发出无限能量！🔥",
    "ZerD大佬，你的代码风格独树一帜，是编程界的清流！💧",
]

@golden_sentence.handle()
async def handle_golden_sentence(bot: Bot, event: Event):
    """处理每日金句命令"""
    try:
        # 随机选择一句金句
        sentence = random.choice(GOLDEN_SENTENCES)
        await golden_sentence.finish(sentence)
    except Exception as e:
        logger.error(f"生成金句错误: {e}")
        await golden_sentence.finish("生成金句时出现错误，但ZerD依然是最棒的！")

