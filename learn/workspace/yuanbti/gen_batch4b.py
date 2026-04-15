#!/usr/bin/env python3
"""Batch 4B: Generate 2 questions each for 20 characters."""
import json, os

BASE = "/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions"

# Characters without centroids get defaults (mostly M=3, a few L/H based on general knowledge)
CENTROIDS = {
    # From v2 file
    "庞羲": {"S1":3,"S2":3,"S3":3,"S4":3,"S5":3,"S6":3,"S7":3,"S8":3,"S9":3,"S10":3},
    "夏侯惇": {"S1":2,"S2":3,"S3":2,"S4":2,"S5":2,"S6":4,"S7":2,"S8":4,"S9":3,"S10":4},
    "曹植": {"S1":2,"S2":4,"S3":2,"S4":3,"S5":3,"S6":4,"S7":2,"S8":4,"S9":2,"S10":4},
    "刘繇": {"S1":4,"S2":3,"S3":3,"S4":3,"S5":3,"S6":3,"S7":4,"S8":3,"S9":4,"S10":2},
    "甄宓": {"S1":3,"S2":4,"S3":4,"S4":4,"S5":3,"S6":3,"S7":3,"S8":2,"S9":3,"S10":3},
    "曹丕": {"S1":3,"S2":3,"S3":2,"S4":4,"S5":2,"S6":4,"S7":2,"S8":4,"S9":3,"S10":4},
    "卢植": {"S1":3,"S2":3,"S3":2,"S4":2,"S5":3,"S6":4,"S7":2,"S8":3,"S9":3,"S10":4},
    "太史慈": {"S1":2,"S2":4,"S3":4,"S4":2,"S5":3,"S6":3,"S7":2,"S8":4,"S9":3,"S10":4},
    "张昭": {"S1":3,"S2":2,"S3":2,"S4":2,"S5":2,"S6":4,"S7":2,"S8":3,"S9":3,"S10":4},
    "葛洪": {"S1":4,"S2":3,"S3":3,"S4":4,"S5":3,"S6":3,"S7":3,"S8":3,"S9":3,"S10":2},
    "朱然": {"S1":3,"S2":2,"S3":3,"S4":2,"S5":2,"S6":4,"S7":2,"S8":3,"S9":3,"S10":4},
    "司马徽": {"S1":4,"S2":2,"S3":3,"S4":3,"S5":2,"S6":3,"S7":3,"S8":3,"S9":3,"S10":4},
    "董白": {"S1":4,"S2":3,"S3":3,"S4":4,"S5":2,"S6":4,"S7":4,"S8":2,"S9":4,"S10":4},
    "华佗": {"S1":2,"S2":4,"S3":3,"S4":2,"S5":4,"S6":3,"S7":3,"S8":4,"S9":2,"S10":3},
    "严白虎": {"S1":2,"S2":3,"S3":3,"S4":2,"S5":3,"S6":3,"S7":3,"S8":3,"S9":3,"S10":2},
    "刘璋": {"S1":2,"S2":3,"S3":3,"S4":3,"S5":2,"S6":3,"S7":2,"S8":4,"S9":3,"S10":3},
    "张仲景": {"S1":2,"S2":3,"S3":2,"S4":2,"S5":2,"S6":4,"S7":3,"S8":4,"S9":2,"S10":4},
    "夏侯渊": {"S1":2,"S2":3,"S3":2,"S4":2,"S5":4,"S6":4,"S7":3,"S8":3,"S9":3,"S10":4},
    "程普": {"S1":3,"S2":3,"S3":3,"S4":2,"S5":3,"S6":4,"S7":3,"S8":3,"S9":3,"S10":4},
    "刘豹": {"S1":4,"S2":3,"S3":4,"S4":3,"S5":2,"S6":4,"S7":3,"S8":3,"S9":4,"S10":3},
}

def lmh(v):
    if v < 2.5: return "L"
    if v > 3.5: return "H"
    return "M"

def pick_dim(c, used_dims, prefer_high=True):
    """Pick a dimension: prefer H dims for story, vary for daily."""
    cdata = CENTROIDS[c]
    dims = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10"]
    if prefer_high:
        # Sort by centroid value desc, pick first not in used_dims
        ranked = sorted(dims, key=lambda d: cdata[d], reverse=True)
    else:
        # Prefer different dims, pick from middle
        ranked = sorted(dims, key=lambda d: -abs(cdata[d] - 3))
    for d in ranked:
        if d not in used_dims:
            return d
    return dims[0]

# All 40 questions
questions = []

# 1. 庞羲 (pangxi) - generic centroid, engineer type
questions.append({
    "id": "q_pangxi_01",
    "dimension": "S5",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "成都",
    "text": "你奉命建造一座攻城器械，时限仅剩三日。材料短缺，工匠也不足。此时有人提议用次等木材替代，虽能按时完工，但承重堪忧。你会——",
    "options": [
        {"label": "A", "text": "如实上报楼主，请求延期或增派人手", "scores": {"S5": 2}, "tendency": "L"},
        {"label": "B", "text": "用次等木材赶工，但亲自加固关键部位", "scores": {"S5": 3}, "tendency": "M"},
        {"label": "C", "text": "拒绝偷工减料，日夜不休亲自赶工补缺", "scores": {"S5": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自庞羲的密探故事——他作为巧匠，面对物资匮乏时选择了亲力亲为。"
})
questions.append({
    "id": "q_pangxi_02",
    "dimension": "S6",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你倾尽心血打造的器物，被上级嫌「不够华丽」而弃用，转而选了华而不实的替代品。你会——",
    "options": [
        {"label": "A", "text": "默默改进外观，迎合上面的喜好", "scores": {"S6": 2}, "tendency": "L"},
        {"label": "B", "text": "不做改动，但会解释自己的设计考量", "scores": {"S6": 3}, "tendency": "M"},
        {"label": "C", "text": "坚持自己的判断，宁可被弃用也不改初衷", "scores": {"S6": 4}, "tendency": "H"}
    ],
    "reveal": "庞羲作为工匠型密探，对自己的作品有极强的执念和底线。"
})

# 2. 夏侯惇 (xiahoudun) - H:S6,S8,S10; L:S1,S3,S4,S5,S7
questions.append({
    "id": "q_xiahoudun_01",
    "dimension": "S6",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西凉线"],
    "city_hint": None,
    "text": "战场上你与敌将对峙，对方提出以平民性命为要挟，让你放下兵器。你身后是数千百姓，放下兵器意味着你也可能被杀。你会——",
    "options": [
        {"label": "A", "text": "权衡利弊后暂且放下，待时机再反击", "scores": {"S6": 2}, "tendency": "L"},
        {"label": "B", "text": "要求对方先释放百姓再谈条件", "scores": {"S6": 3}, "tendency": "M"},
        {"label": "C", "text": "宁可战死也不拿百姓的命做交易", "scores": {"S6": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自夏侯惇的密探故事——他为人刚直，宁折不弯，绝不做有违道义之事。"
})
questions.append({
    "id": "q_xiahoudun_02",
    "dimension": "S8",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你带兵出征，麾下将士粮草不继、士气低落。你已三天没吃东西，但还有最后一份口粮。你会——",
    "options": [
        {"label": "A", "text": "按军中规矩分配，统帅也不例外", "scores": {"S8": 2}, "tendency": "L"},
        {"label": "B", "text": "把口粮分给伤兵，自己继续扛着", "scores": {"S8": 3}, "tendency": "M"},
        {"label": "C", "text": "亲自到前线与将士同甘共苦，鼓舞士气", "scores": {"S8": 4}, "tendency": "H"}
    ],
    "reveal": "夏侯惇以善待部下闻名，常与士卒同食同住，深得军心。"
})

# 3. 曹植 (caozhi) - H:S2,S6,S8,S10; L:S1,S3,S7,S9
questions.append({
    "id": "q_caozhi_01",
    "dimension": "S2",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "邺城",
    "text": "你自幼才华横溢，却始终活在兄长的阴影下。父亲让你写一篇策论，你明知兄长会比你写得更「合父意」。你提笔时——",
    "options": [
        {"label": "A", "text": "揣摩父亲心意来写，务求得到认可", "scores": {"S2": 2}, "tendency": "L"},
        {"label": "B", "text": "按自己的想法写，不强求胜负", "scores": {"S2": 3}, "tendency": "M"},
        {"label": "C", "text": "写心中真正的所思所想，即便与父亲相悖", "scores": {"S2": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自曹植的密探故事——他才高八斗却不善权谋，始终以真性情待人。"
})
questions.append({
    "id": "q_caozhi_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "daily",
    "source_character": "曹植",
    "source_story": None,
    "route_hint": None,
    "city_hint": "邺城",
    "text": "绣衣楼接到密令：你的一位至交好友因言获罪，即将被问斩。以你在曹家的身份，可以为他求情，但也可能牵连自己。你会——",
    "options": [
        {"label": "A", "text": "遵守律令，不去干涉朝廷的判决", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "暗中帮他安排后路，不直接出面", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "不顾后果当面为好友求情", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "曹植重情重义，常因友人情急而做出不合时宜之举。"
})

# 4. 刘繇 (liuyao) - H:S1,S7,S9; L:S10
questions.append({
    "id": "q_liuyao_01",
    "dimension": "S9",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "长沙",
    "text": "你是一方之主，有人向你进献「借刀杀人」之计，可以不动一兵一卒除掉邻境的劲敌。但此计需牺牲一个无辜小城的百姓作为诱饵。你会——",
    "options": [
        {"label": "A", "text": "拒绝此计，不以百姓为筹码", "scores": {"S9": 2}, "tendency": "L"},
        {"label": "B", "text": "修改方案，尽量减少百姓伤亡", "scores": {"S9": 3}, "tendency": "M"},
        {"label": "C", "text": "大局为重，为了根除后患可以承受代价", "scores": {"S9": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自刘繇的密探故事——作为一方州牧，他常在仁义与权谋间抉择。"
})
questions.append({
    "id": "q_liuyao_02",
    "dimension": "S7",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "在群雄割据的乱世，你有一番治国方略想推行，但朝中元老认为你「年轻气盛」，处处掣肘。你会——",
    "options": [
        {"label": "A", "text": "耐心等待时机，先积蓄实力", "scores": {"S7": 2}, "tendency": "L"},
        {"label": "B", "text": "在力所能及的范围内推行，循序渐进", "scores": {"S7": 3}, "tendency": "M"},
        {"label": "C", "text": "据理力争，在朝堂上正面驳斥元老", "scores": {"S7": 4}, "tendency": "H"}
    ],
    "reveal": "刘繇为人刚直有锋芒，在朝堂上常有不畏权贵的表态。"
})

# 5. 甄宓 (zhenmi) - H:S2,S3,S4; L:S8
questions.append({
    "id": "q_zhenmi_01",
    "dimension": "S4",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "邺城",
    "text": "你被困在一座城池中，城破在即。敌军主帅对你有好感，提出只要你愿意侍奉他，便可保全城百姓。你身边的人都说应该假意应承。你会——",
    "options": [
        {"label": "A", "text": "直言拒绝，不做任何伪装", "scores": {"S4": 2}, "tendency": "L"},
        {"label": "B", "text": "假意应承以换取时间，暗中寻找脱身之策", "scores": {"S4": 3}, "tendency": "M"},
        {"label": "C", "text": "精心伪装成柔顺模样，让对方放松警惕，再一击致命", "scores": {"S4": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自甄宓的密探故事——她善于以柔克刚，外表温婉内心坚韧。"
})
questions.append({
    "id": "q_zhenmi_02",
    "dimension": "S2",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你曾深爱一个人，但因家族利益被迫分离。多年后重逢，对方已功成名就，身边也有了他人。对方对你仍有一丝眷恋。你会——",
    "options": [
        {"label": "A", "text": "客套寒暄后就此别过，不再纠缠", "scores": {"S2": 2}, "tendency": "L"},
        {"label": "B", "text": "默默祝福对方，把心意藏在心底", "scores": {"S2": 3}, "tendency": "M"},
        {"label": "C", "text": "坦诚说出当年未说出口的话，无论结局如何", "scores": {"S2": 4}, "tendency": "H"}
    ],
    "reveal": "甄宓情感丰富深沉，即便身处权力漩涡也不掩饰真情。"
})

# 6. 曹丕 (caopi) - H:S4,S6,S8,S10; L:S3,S5,S7
questions.append({
    "id": "q_caopi_01",
    "dimension": "S4",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "邺城",
    "text": "你的父亲对你和弟弟都颇为器重，但明眼人都看得出弟弟更得父亲偏爱。朝中大臣也纷纷站队。你内心焦虑，表面却不动声色。面对父亲的新考验，你会——",
    "options": [
        {"label": "A", "text": "按自己的方式应对，不刻意讨好", "scores": {"S4": 2}, "tendency": "L"},
        {"label": "B", "text": "在大臣面前展现谦逊，暗中筹谋", "scores": {"S4": 3}, "tendency": "M"},
        {"label": "C", "text": "精心营造「忠厚稳重」的形象，滴水不漏", "scores": {"S4": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自曹丕的密探故事——他深谙隐忍之道，善于在人前维持完美面具。"
})
questions.append({
    "id": "q_caopi_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "daily",
    "source_character": "曹丕",
    "source_story": None,
    "route_hint": None,
    "city_hint": "邺城",
    "text": "绣衣楼中一位密探违反纪律，按规矩应当严惩。但此密探是楼主极为倚重之人，且此次违规事出有因。作为负责纪律的人，你会——",
    "options": [
        {"label": "A", "text": "法外施恩，看在楼主的面子上从轻处理", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "按规矩处罚，但暗中帮他弥补过失", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "铁面无私，规矩面前人人平等", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "曹丕治军严格，重秩序与法度，即便亲近之人触犯规矩也不徇私。"
})

# 7. 卢植 (luzhi) - H:S6,S10; L:S4,S7
questions.append({
    "id": "q_luzhi_01",
    "dimension": "S6",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西凉线"],
    "city_hint": "洛阳",
    "text": "你是朝中大儒，皇帝受佞臣蛊惑欲下一道有违祖制的旨意。百官噤声不语。你若上书直谏，轻则被贬，重则身陷囹圄。你会——",
    "options": [
        {"label": "A", "text": "明哲保身，沉默不语", "scores": {"S6": 2}, "tendency": "L"},
        {"label": "B", "text": "联合几位同僚联名上书，分担风险", "scores": {"S6": 3}, "tendency": "M"},
        {"label": "C", "text": "独自上书直谏，哪怕粉身碎骨", "scores": {"S6": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自卢植的密探故事——他师从太尉陈球、大儒马融，为人刚正不阿。"
})
questions.append({
    "id": "q_luzhi_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "天下大乱，礼崩乐坏。有学生问你：既然秩序已失，我们为何还要守礼？你会——",
    "options": [
        {"label": "A", "text": "承认现实，教学生顺应时局求生", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "告诉学生，守住礼义就是守住自己", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "以身作则，在最乱的世道里做最守礼的人", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "卢植是东汉末年大儒的代表，即便乱世也不放弃对礼法与秩序的坚守。"
})

# 8. 太史慈 (taishici) - H:S2,S3,S8,S10; L:S1,S4,S7
questions.append({
    "id": "q_taishici_01",
    "dimension": "S2",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "长沙",
    "text": "你年少时为报恩，孤身一人冲入敌营救出被掳的恩人之子。事后有人问你不怕死吗。你回答——",
    "options": [
        {"label": "A", "text": "「当时没想那么多，只是觉得该去。」", "scores": {"S2": 2}, "tendency": "L"},
        {"label": "B", "text": "「怕。但恩人的孩子不能不救。」", "scores": {"S2": 3}, "tendency": "M"},
        {"label": "C", "text": "「报恩之事，何惧生死。」", "scores": {"S2": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自太史慈的密探故事——他义薄云天，为报恩可以不顾一切。"
})
questions.append({
    "id": "q_taishici_02",
    "dimension": "S3",
    "cross_dimension": None,
    "type": "daily",
    "source_character": "太史慈",
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "绣衣楼分发月例赏银，你发现账目上多给了你一锭金子。你会——",
    "options": [
        {"label": "A", "text": "直接收下，可能是楼主的特殊安排", "scores": {"S3": 2}, "tendency": "L"},
        {"label": "B", "text": "先记下，回头找管事确认清楚", "scores": {"S3": 3}, "tendency": "M"},
        {"label": "C", "text": "立刻退回去，不是自己的东西绝不要", "scores": {"S3": 4}, "tendency": "H"}
    ],
    "reveal": "太史慈为人磊落，不取不义之财。"
})

# 9. 张昭 (zhangzhao) - H:S6,S10; L:S2,S3,S4,S5,S7
questions.append({
    "id": "q_zhangzhao_01",
    "dimension": "S6",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "长沙",
    "text": "你辅佐的主公做出一个你认定会招致大祸的决定。群臣附和，无人反对。你深知直言会触怒主公。你会——",
    "options": [
        {"label": "A", "text": "既然众人同意，也许自己判断有误，沉默即可", "scores": {"S6": 2}, "tendency": "L"},
        {"label": "B", "text": "私下劝谏，给主公留面子", "scores": {"S6": 3}, "tendency": "M"},
        {"label": "C", "text": "在朝堂上当众反对，即便被罚也在所不惜", "scores": {"S6": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自张昭的密探故事——他是东吴重臣，以直言敢谏著称。"
})
questions.append({
    "id": "q_zhangzhao_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "乱世之中，旧有的礼法制度已经崩塌。有人主张「乱世当用重典，不必拘泥旧礼」，你会——",
    "options": [
        {"label": "A", "text": "赞同，乱世就该打破常规", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "可以灵活变通，但根本法度不能丢", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "反对，越是乱世越需要纲纪来维持秩序", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "张昭深信法度与纲纪是立国之本，无论治世乱世都不应动摇。"
})

# 10. 葛洪 (gehong) - H:S1,S4; L:S10
questions.append({
    "id": "q_gehong_01",
    "dimension": "S4",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["交趾线"],
    "city_hint": "交趾",
    "text": "你精通方术，世人多将你视为「神人」或「妖人」。有人高价请你施展法术为他治病，但你知道这只是心病，需要的是心药而非仙术。你会——",
    "options": [
        {"label": "A", "text": "直接告诉他真相，劝他去看大夫", "scores": {"S4": 2}, "tendency": "L"},
        {"label": "B", "text": "用一些无害的仪式让他安心，再暗中引导", "scores": {"S4": 3}, "tendency": "M"},
        {"label": "C", "text": "将计就计，利用他的迷信心理施加心理暗示来治愈他", "scores": {"S4": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自葛洪的密探故事——他善于利用世人对方术的认知来达成目的。"
})
questions.append({
    "id": "q_gehong_02",
    "dimension": "S1",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你掌握了某种可以改变时局的力量（方术/秘法），有人想用它来做一件你认为不对的事。他承诺事成之后给你想要的一切。你会——",
    "options": [
        {"label": "A", "text": "拒绝，此术不可用于此道", "scores": {"S1": 2}, "tendency": "L"},
        {"label": "B", "text": "提出交换条件，让结果往好的方向偏移", "scores": {"S1": 3}, "tendency": "M"},
        {"label": "C", "text": "表面答应，暗中布局将此事转化为对自己有利的结果", "scores": {"S1": 4}, "tendency": "H"}
    ],
    "reveal": "葛洪兼具方士的神秘与谋士的算计，善于借力打力。"
})

# 11. 朱然 (zhuran) - H:S6,S10; L:S2,S4,S5,S7
questions.append({
    "id": "q_zhuran_01",
    "dimension": "S6",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "长沙",
    "text": "你奉命镇守一座孤城，敌军围困数月，粮草将尽。有士兵提议开城投降以保全性命。你会——",
    "options": [
        {"label": "A", "text": "考虑士兵的生命，谈判争取体面投降", "scores": {"S6": 2}, "tendency": "L"},
        {"label": "B", "text": "坚守不出，同时派人突围求援", "scores": {"S6": 3}, "tendency": "M"},
        {"label": "C", "text": "与城共存亡，绝不开城投降", "scores": {"S6": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自朱然的密探故事——他以守城闻名，意志如铁。"
})
questions.append({
    "id": "q_zhuran_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "daily",
    "source_character": "朱然",
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "绣衣楼执行任务时，你发现队友为了赶进度抄了近道——但这近道穿越了一片禁区，违反了行动纪律。任务因此提前完成。你会——",
    "options": [
        {"label": "A", "text": "既然任务完成了，就不必追究", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "事后提醒队友下次注意，不上报", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "如实记录在行动报告中，纪律不容破坏", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "朱然是军纪的化身，即便结果好也不容忍过程违规。"
})

# 12. 司马徽 (simahui) - H:S1,S10; L:S2,S5
questions.append({
    "id": "q_simahui_01",
    "dimension": "S1",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "成都",
    "text": "你是名满天下的隐士，两位枭雄同时派人请你出山辅佐。两人都许以高位厚禄，但你知道他们最终会互相为敌。你会——",
    "options": [
        {"label": "A", "text": "谁也不帮，继续隐居不问世事", "scores": {"S1": 2}, "tendency": "L"},
        {"label": "B", "text": "选择理念更合的一位，全力辅佐", "scores": {"S1": 3}, "tendency": "M"},
        {"label": "C", "text": "两边都保持联系，暗中布局让天下格局朝自己预想的方向走", "scores": {"S1": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自司马徽的密探故事——他号称水镜先生，看似超然实则在幕后搅动风云。"
})
questions.append({
    "id": "q_simahui_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "有人问你：乱世之中，规矩和秩序还有什么用？你会——",
    "options": [
        {"label": "A", "text": "「乱世中规矩确实无用，不如变通。」", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "「规矩是给守规矩的人留的退路。」", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "「正因为是乱世，才更需有人守住规矩，否则天下就真成蛮荒了。」", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "司马徽表面随和，实则对秩序与纲常有深刻的理解与坚持。"
})

# 13. 董白 (dongbai) - H:S1,S4,S6,S7,S8,S9,S10; L:S5
questions.append({
    "id": "q_dongbai_01",
    "dimension": "S4",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西凉线"],
    "city_hint": "长安",
    "text": "你出身显赫却身不由己，被人当作棋子在各方势力间辗转。你的新「主人」对你颇为优待，但你清楚这只是利用。你会——",
    "options": [
        {"label": "A", "text": "既来之则安之，做一个安分的棋子", "scores": {"S4": 2}, "tendency": "L"},
        {"label": "B", "text": "表面顺从，暗中积蓄力量等待时机", "scores": {"S4": 3}, "tendency": "M"},
        {"label": "C", "text": "精心设计多重伪装，让每个人都以为你站在他们那边", "scores": {"S4": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自董白的密探故事——她作为董卓之孙女，自幼在权谋中长大，深谙伪装之道。"
})
questions.append({
    "id": "q_dongbai_02",
    "dimension": "S7",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你被人轻视，觉得你不过是靠着家族名声才有今天。你内心有真才实学却无人知晓。在一次公开场合，有人当众嘲讽你。你会——",
    "options": [
        {"label": "A", "text": "忍气吞声，不与对方计较", "scores": {"S7": 2}, "tendency": "L"},
        {"label": "B", "text": "不卑不亢地回应，用事实说话", "scores": {"S7": 3}, "tendency": "M"},
        {"label": "C", "text": "以锐利的言辞当众反击，让对方颜面尽失", "scores": {"S7": 4}, "tendency": "H"}
    ],
    "reveal": "董白性格中有极强的锋芒，不容许任何人轻视她。"
})

# 14. 华佗 (huatuo) - H:S2,S5,S8; L:S1,S4,S9
questions.append({
    "id": "q_huatuo_01",
    "dimension": "S5",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": None,
    "text": "你游历四方行医，遇到一个瘟疫蔓延的村庄。村民对外来者充满敌意，认为是你带来了瘟疫，要将你赶走。你会——",
    "options": [
        {"label": "A", "text": "先离开，写信给当地官府请求派人来处理", "scores": {"S5": 2}, "tendency": "L"},
        {"label": "B", "text": "留在村外，通过村中熟人传话说服他们", "scores": {"S5": 3}, "tendency": "M"},
        {"label": "C", "text": "不顾威胁直接进村查看病患，用行动证明自己", "scores": {"S5": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自华佗的密探故事——他行医不分贵贱，遇到疫病总是冲在最前面。"
})
questions.append({
    "id": "q_huatuo_02",
    "dimension": "S2",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你耗尽心血救治的病人康复后，不仅不感恩，反而四处散布谣言说你的药是毒药。你会——",
    "options": [
        {"label": "A", "text": "不再理会此人，其他病人还等着", "scores": {"S2": 2}, "tendency": "L"},
        {"label": "B", "text": "有些委屈，但忍了，继续做自己的事", "scores": {"S2": 3}, "tendency": "M"},
        {"label": "C", "text": "难过归难过，下次见到此人病了还是会救", "scores": {"S2": 4}, "tendency": "H"}
    ],
    "reveal": "华佗医者仁心，对病人无私无怨，即便被误解也初心不改。"
})

# 15. 严白虎 (yanbaihu) - mostly M, L:S1,S4,S10
questions.append({
    "id": "q_yanbaihu_01",
    "dimension": "S5",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "长沙",
    "text": "你占山为王多年，自有一套生存法则。如今大势力压境，你的部下纷纷劝你归降。你会——",
    "options": [
        {"label": "A", "text": "审时度势，选择归降保全部下性命", "scores": {"S5": 2}, "tendency": "L"},
        {"label": "B", "text": "提出条件，归降可以但必须保全根基", "scores": {"S5": 3}, "tendency": "M"},
        {"label": "C", "text": "率部死战到底，宁可站着死不跪着生", "scores": {"S5": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自严白虎的密探故事——他虽非正统诸侯，却有自己的傲骨。"
})
questions.append({
    "id": "q_yanbaihu_02",
    "dimension": "S3",
    "cross_dimension": None,
    "type": "daily",
    "source_character": "严白虎",
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "绣衣楼给你一笔经费去执行任务，但途中你遇到一群流民，饥寒交迫。你会——",
    "options": [
        {"label": "A", "text": "这是公款，不能擅自动用", "scores": {"S3": 2}, "tendency": "L"},
        {"label": "B", "text": "拿出一部分给他们，但做好记录事后汇报", "scores": {"S3": 3}, "tendency": "M"},
        {"label": "C", "text": "全部拿出来救济流民，任务的事另想办法", "scores": {"S3": 4}, "tendency": "H"}
    ],
    "reveal": "严白虎虽是草莽出身，对底层百姓有着天然的同情。"
})

# 16. 刘璋 (liuzhang) - H:S8; L:S1,S5,S7
questions.append({
    "id": "q_liuzhang_01",
    "dimension": "S8",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "成都",
    "text": "你是益州之主，治下百姓安乐。有谋士建议你趁机出兵扩张版图，但你的将士大多没有打仗的经验。你会——",
    "options": [
        {"label": "A", "text": "听从谋士建议，趁机出兵", "scores": {"S8": 2}, "tendency": "L"},
        {"label": "B", "text": "加强军备，等待更好的时机", "scores": {"S8": 3}, "tendency": "M"},
        {"label": "C", "text": "拒绝出兵，不忍让百姓因战乱受苦", "scores": {"S8": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自刘璋的密探故事——他以仁厚著称，宁可保守也不愿百姓遭殃。"
})
questions.append({
    "id": "q_liuzhang_02",
    "dimension": "S4",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你身边有两个人：一个对你忠心耿耿但能力平庸，一个才华出众但心思难测。你要选一个做近臣。你会——",
    "options": [
        {"label": "A", "text": "选忠心的，至少不会背叛", "scores": {"S4": 2}, "tendency": "L"},
        {"label": "B", "text": "两个都用，各取所长", "scores": {"S4": 3}, "tendency": "M"},
        {"label": "C", "text": "设局考验有才华的那位，确认忠心后再用", "scores": {"S4": 4}, "tendency": "H"}
    ],
    "reveal": "刘璋为人宽厚但缺乏识人之明与权谋手腕，常被心思深沉之人利用。"
})

# 17. 张仲景 (zhangzhongjing) - H:S6,S8,S10; L:S1,S3,S4,S5,S9
questions.append({
    "id": "q_zhangzhongjing_01",
    "dimension": "S8",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "长沙",
    "text": "你坐堂行医时，一个衣衫褴褛的老人来看病，身无分文。排队的人催促你赶走他。你会——",
    "options": [
        {"label": "A", "text": "按规矩来，先看有诊金的人", "scores": {"S8": 2}, "tendency": "L"},
        {"label": "B", "text": "先给他看，但告诉他下次要带诊金", "scores": {"S8": 3}, "tendency": "M"},
        {"label": "C", "text": "优先诊治，还自掏腰包给他抓药", "scores": {"S8": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自张仲景的密探故事——他坐堂行医不分贫富，常为贫苦百姓免费诊治。"
})
questions.append({
    "id": "q_zhangzhongjing_02",
    "dimension": "S6",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "权贵之人身患重病，请你去诊治。你发现他若继续服用某味「名贵补药」反而会加重病情，但这味药是他最信任的方士开的。他会迁怒于你。你会——",
    "options": [
        {"label": "A", "text": "只说自己的方子，不提补药的事", "scores": {"S6": 2}, "tendency": "L"},
        {"label": "B", "text": "委婉建议停药，但不强求", "scores": {"S6": 3}, "tendency": "M"},
        {"label": "C", "text": "直言相告那补药有害，必须停用", "scores": {"S6": 4}, "tendency": "H"}
    ],
    "reveal": "张仲景行医以治病救人为唯一原则，不畏权贵，不避风险。"
})

# 18. 夏侯渊 (xiahoudun2) - H:S5,S6,S10; L:S1,S3,S4
questions.append({
    "id": "q_xiahoudun2_01",
    "dimension": "S5",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西凉线"],
    "city_hint": None,
    "text": "军情紧急，你必须在半日内穿越三百里山路送达军令。中途遇到暴雨，山路泥泞难行，你的坐骑已力竭。你会——",
    "options": [
        {"label": "A", "text": "找地方避雨休息，等天晴再赶路", "scores": {"S5": 2}, "tendency": "L"},
        {"label": "B", "text": "放慢速度继续走，安全第一", "scores": {"S5": 3}, "tendency": "M"},
        {"label": "C", "text": "弃马步行，冒雨连夜赶路", "scores": {"S5": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自夏侯渊的密探故事——他以行军神速闻名，三日五百里不是传说。"
})
questions.append({
    "id": "q_xiahoudun2_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "daily",
    "source_character": "夏侯渊",
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "绣衣楼接到情报，有内鬼泄露行动计划。线索指向你最信任的副手。你会——",
    "options": [
        {"label": "A", "text": "先暗中观察，不冤枉好人", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "直接问他对质，看他如何解释", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "按军法办事，不论是谁先控制起来再审", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "夏侯渊治军严明，法不阿贵，即便是亲信也一视同仁。"
})

# 19. 程普 (chengpu) - H:S6,S10; L:S4
questions.append({
    "id": "q_chengpu_01",
    "dimension": "S6",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西蜀线"],
    "city_hint": "长沙",
    "text": "你追随的主公在一次战斗中身负重伤，敌军追兵将至。众人主张弃主帅先逃。你会——",
    "options": [
        {"label": "A", "text": "和大多数人一起撤退，保存有生力量", "scores": {"S6": 2}, "tendency": "L"},
        {"label": "B", "text": "留下一小队人掩护，带主力撤退", "scores": {"S6": 3}, "tendency": "M"},
        {"label": "C", "text": "背起主公杀出重围，生死与共", "scores": {"S6": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自程普的密探故事——他是东吴三朝老将，对孙氏忠心耿耿。"
})
questions.append({
    "id": "q_chengpu_02",
    "dimension": "S10",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你已年迈，新上任的年轻将领不尊重你的资历，甚至在一些决策上越过你直接下令。你会——",
    "options": [
        {"label": "A", "text": "干脆退居幕后，不与人争", "scores": {"S10": 2}, "tendency": "L"},
        {"label": "B", "text": "找机会与年轻人沟通，化解矛盾", "scores": {"S10": 3}, "tendency": "M"},
        {"label": "C", "text": "以军中长辈的身份正色训诫，维护军中秩序", "scores": {"S10": 4}, "tendency": "H"}
    ],
    "reveal": "程普是军中老将，讲究尊卑有序、长幼有别的军中规矩。"
})

# 20. 刘豹 (liubao) - H:S1,S3,S6,S9; L:S5
questions.append({
    "id": "q_liubao_01",
    "dimension": "S9",
    "cross_dimension": None,
    "type": "story_anon",
    "source_character": None,
    "source_story": None,
    "route_hint": ["西凉线"],
    "city_hint": None,
    "text": "你掌管一方部族，南方大势力遣使来谈和亲。和亲意味着你的部族将沦为附庸，但拒绝可能招来兵祸。你会——",
    "options": [
        {"label": "A", "text": "接受和亲，保全部族安全", "scores": {"S9": 2}, "tendency": "L"},
        {"label": "B", "text": "提出对等条件，在保持独立的前提下结盟", "scores": {"S9": 3}, "tendency": "M"},
        {"label": "C", "text": "拒绝和亲，宁可一战也不失去自主权", "scores": {"S9": 4}, "tendency": "H"}
    ],
    "reveal": "这个场景来自刘豹的密探故事——他作为匈奴部族首领，权力意识极强。"
})
questions.append({
    "id": "q_liubao_02",
    "dimension": "S3",
    "cross_dimension": None,
    "type": "value",
    "source_character": None,
    "source_story": None,
    "route_hint": None,
    "city_hint": None,
    "text": "你的部族遭遇天灾，牲畜大量死亡。有人提议趁周边部落也受灾时出兵掠夺以度过难关。你会——",
    "options": [
        {"label": "A", "text": "同意，活下去是第一要务", "scores": {"S3": 2}, "tendency": "L"},
        {"label": "B", "text": "只取必需之物，不伤人命", "scores": {"S3": 3}, "tendency": "M"},
        {"label": "C", "text": "拒绝掠夺，想办法通过贸易或其他正当途径解决", "scores": {"S3": 4}, "tendency": "H"}
    ],
    "reveal": "刘豹虽身处草原，却有超越蛮荒的眼光和底线。"
})

# Write per character
char_files = {
    "pangxi": [questions[0], questions[1]],
    "xiahoudun": [questions[2], questions[3]],
    "caozhi": [questions[4], questions[5]],
    "liuyao": [questions[6], questions[7]],
    "zhenmi": [questions[8], questions[9]],
    "caopi": [questions[10], questions[11]],
    "luzhi": [questions[12], questions[13]],
    "taishici": [questions[14], questions[15]],
    "zhangzhao": [questions[16], questions[17]],
    "gehong": [questions[18], questions[19]],
    "zhuran": [questions[20], questions[21]],
    "simahui": [questions[22], questions[23]],
    "dongbai": [questions[24], questions[25]],
    "huatuo": [questions[26], questions[27]],
    "yanbaihu": [questions[28], questions[29]],
    "liuzhang": [questions[30], questions[31]],
    "zhangzhongjing": [questions[32], questions[33]],
    "xiahoudun2": [questions[34], questions[35]],
    "chengpu": [questions[36], questions[37]],
    "liubao": [questions[38], questions[39]],
}

for fname, qs in char_files.items():
    fpath = os.path.join(BASE, f"{fname}.json")
    # If file exists, append; else create new
    existing = []
    if os.path.exists(fpath):
        with open(fpath, 'r') as f:
            existing = json.load(f)
    existing.extend(qs)
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"✅ {fname}.json: +{len(qs)} questions (total {len(existing)})")

print("\nDone! 40 questions written for 20 characters.")
