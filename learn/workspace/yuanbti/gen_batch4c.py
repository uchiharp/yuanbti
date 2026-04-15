#!/usr/bin/env python3
"""Batch 4C: Generate 2 questions each for 20 characters."""
import json, subprocess, os, random

QDIR = "/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions"

# Centroids from the file + reasonable defaults for missing ones
CENTROIDS = {
    "安期":     {"S1":4,"S2":2,"S3":2,"S4":4,"S5":2,"S6":4,"S7":3,"S8":2,"S9":4,"S10":3},
    "小乔":     {"S1":2,"S2":4,"S3":4,"S4":2,"S5":4,"S6":3,"S7":2,"S8":4,"S9":3,"S10":3},
    "孙尚香":   {"S1":2,"S2":4,"S3":2,"S4":2,"S5":4,"S6":3,"S7":3,"S8":4,"S9":3,"S10":2},
    "吕蒙":     {"S1":2,"S2":4,"S3":3,"S4":4,"S5":4,"S6":4,"S7":3,"S8":3,"S9":2,"S10":2},
    "张鲁":     {"S1":3,"S2":3,"S3":2,"S4":3,"S5":2,"S6":3,"S7":2,"S8":4,"S9":3,"S10":4},
    "公孙珊":   {"S1":2,"S2":4,"S3":2,"S4":2,"S5":3,"S6":4,"S7":2,"S8":4,"S9":2,"S10":4},
    "王粲":     {"S1":2,"S2":3,"S3":2,"S4":2,"S5":2,"S6":4,"S7":2,"S8":4,"S9":2,"S10":4},
    "张修":     {"S1":4,"S2":3,"S3":2,"S4":4,"S5":3,"S6":3,"S7":3,"S8":3,"S9":3,"S10":3},
    "干吉":     {"S1":3,"S2":3,"S3":2,"S4":3,"S5":2,"S6":4,"S7":3,"S8":4,"S9":2,"S10":4},
    "庞统":     {"S1":3,"S2":3,"S3":2,"S4":2,"S5":2,"S6":4,"S7":2,"S8":4,"S9":2,"S10":4},
    "蒯良":     {"S1":3,"S2":2,"S3":3,"S4":3,"S5":2,"S6":3,"S7":2,"S8":3,"S9":3,"S10":4},
    "周群":     {"S1":3,"S2":2,"S3":2,"S4":2,"S5":2,"S6":4,"S7":2,"S8":4,"S9":2,"S10":4},
    "蔡琰":     {"S1":2,"S2":4,"S3":2,"S4":2,"S5":2,"S6":4,"S7":2,"S8":4,"S9":2,"S10":3},
    "虞翻":     {"S1":2,"S2":3,"S3":2,"S4":2,"S5":4,"S6":4,"S7":3,"S8":3,"S9":2,"S10":4},
    "陆逊":     {"S1":4,"S2":2,"S3":3,"S4":3,"S5":2,"S6":4,"S7":2,"S8":3,"S9":3,"S10":4},
    "钟繇":     {"S1":3,"S2":2,"S3":3,"S4":3,"S5":2,"S6":4,"S7":2,"S8":3,"S9":3,"S10":4},
    "耿公子":   {"S1":3,"S2":3,"S3":3,"S4":3,"S5":3,"S6":3,"S7":3,"S8":3,"S9":3,"S10":3},
    "陈宫":     {"S1":4,"S2":3,"S3":2,"S4":3,"S5":3,"S6":3,"S7":3,"S8":2,"S9":3,"S10":3},
    "马腾":     {"S1":3,"S2":3,"S3":3,"S4":2,"S5":4,"S6":4,"S7":3,"S8":3,"S9":3,"S10":3},
    "伍丹":     {"S1":3,"S2":3,"S3":3,"S4":3,"S5":3,"S6":3,"S7":3,"S8":3,"S9":3,"S10":3},
}

def get_lmh(s):
    if s < 2.5: return "L"
    if s > 3.5: return "H"
    return "M"

def lmh(c):
    return {k: get_lmh(v) for k, v in c.items()}

def get_h_dims(c):
    return [k for k, v in lmh(c).items() if v == "H"]

def get_l_dims(c):
    return [k for k, v in lmh(c).items() if v == "L"]

def db_speaker(name):
    """Query dialogues for a speaker from db9"""
    try:
        r = subprocess.run(
            ["db9", "sql", "learn_test", "-q", 
             f"SELECT text FROM dialogues WHERE speaker='{name}' AND category='密探故事' ORDER BY RANDOM() LIMIT 20"],
            capture_output=True, text=True, timeout=15
        )
        lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
        return lines[:20]
    except:
        return []

# === ALL 40 QUESTIONS ===
QUESTIONS = {
    "安期": [
        {
            "id": "q_anqi_1",
            "dimension": "S4",
            "cross_dimension": "S1",
            "type": "story_known",
            "source_character": "安期",
            "source_story": "山隐鸢阁",
            "route_hint": ["西蜀线"],
            "city_hint": "成都",
            "text": "安期身为鸢阁仙门中人，常以温润如玉的面目示人，内心却深藏算计。若有人以利相诱，要你背叛鸢阁的秘密——",
            "options": [
                {"label": "A", "text": "欣然应允，趁势套取对方更多信息", "scores": {"S4": 1, "S1": 4}, "tendency": "L"},
                {"label": "B", "text": "不动声色，既不拒绝也不答应，静观其变", "scores": {"S4": 3, "S1": 3}, "tendency": "M"},
                {"label": "C", "text": "当面拒绝，绝不以虚伪的面目掩盖真心", "scores": {"S4": 5, "S1": 1}, "tendency": "H"},
            ],
            "reveal": "安期选择：以笑意为刃，暗中布局，让对方以为自己掌控全局。"
        },
        {
            "id": "q_anqi_2",
            "dimension": "S9",
            "cross_dimension": "S4",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「欲掌天下，先掌人心。」你更认同以下哪种说法？",
            "options": [
                {"label": "A", "text": "人心不足蛇吞象，不如以势压人来得直接", "scores": {"S9": 1, "S4": 2}, "tendency": "L"},
                {"label": "B", "text": "势可借一时，心可驭一世，二者缺一不可", "scores": {"S9": 3, "S4": 3}, "tendency": "M"},
                {"label": "C", "text": "人心如水，善驭者无形无迹，方为上策", "scores": {"S9": 5, "S4": 4}, "tendency": "H"},
            ],
            "reveal": "此题暗合安期之理念——以无形之术驭有形之势。"
        },
    ],
    "小乔": [
        {
            "id": "q_xiaoqiao_1",
            "dimension": "S8",
            "cross_dimension": "S2",
            "type": "story_known",
            "source_character": "小乔",
            "source_story": "江东日常",
            "route_hint": None,
            "city_hint": None,
            "text": "小乔在绣衣楼中素来温柔体贴，总在密探们疲惫时送来亲手煮的茶点。若有密探因任务失败而自责落泪——",
            "options": [
                {"label": "A", "text": "直言失败不可怕，下次务必成功", "scores": {"S8": 1, "S5": 3}, "tendency": "L"},
                {"label": "B", "text": "默默陪着坐一会儿，等对方情绪平复再说", "scores": {"S8": 3, "S2": 3}, "tendency": "M"},
                {"label": "C", "text": "轻轻递上手帕，柔声说「有我在，不要怕」", "scores": {"S8": 5, "S2": 4}, "tendency": "H"},
            ],
            "reveal": "小乔的选择：柔声安慰，用自己的温暖化解对方的不安。"
        },
        {
            "id": "q_xiaoqiao_2",
            "dimension": "S5",
            "cross_dimension": "S3",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "绣衣楼要举办一场宴会筹措经费，你负责——",
            "options": [
                {"label": "A", "text": "精打细算，用最少的花费办成体面的宴会", "scores": {"S5": 3, "S3": 4}, "tendency": "L"},
                {"label": "B", "text": "主动张罗，亲自跑遍广陵置办物资", "scores": {"S5": 4, "S3": 3}, "tendency": "M"},
                {"label": "C", "text": "只要大家开心就好，花多少都无所谓", "scores": {"S5": 3, "S3": 1}, "tendency": "H"},
            ],
            "reveal": "小乔的日常：会亲力亲为，用行动让每个人感到温暖。"
        },
    ],
    "孙尚香": [
        {
            "id": "q_sunshangxiang_1",
            "dimension": "S5",
            "cross_dimension": "S2",
            "type": "story_known",
            "source_character": "孙尚香",
            "source_story": "江东之虎",
            "route_hint": None,
            "city_hint": None,
            "text": "孙尚香自幼习武，性情刚烈，从不甘于闺阁之中。面对兄长要将她许配联姻的安排——",
            "options": [
                {"label": "A", "text": "虽然心有不甘，但为家族大局只能顺从", "scores": {"S5": 1, "S2": 2}, "tendency": "L"},
                {"label": "B", "text": "表面答应，暗中继续习武，保留自己的锋芒", "scores": {"S5": 3, "S2": 3}, "tendency": "M"},
                {"label": "C", "text": "当面拒绝，自己的命运只能由自己决定", "scores": {"S5": 5, "S2": 4}, "tendency": "H"},
            ],
            "reveal": "孙尚香的选择：以弓刀为伴，誓不做笼中鸟。"
        },
        {
            "id": "q_sunshangxiang_2",
            "dimension": "S7",
            "cross_dimension": "S5",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「宁可枝头抱香死，何曾吹落北风中。」你更认同哪种处世态度？",
            "options": [
                {"label": "A", "text": "顺势而为，活着才有翻盘的机会", "scores": {"S7": 1, "S5": 2}, "tendency": "L"},
                {"label": "B", "text": "该低头时低头，但骨子里不能丢了自己的性子", "scores": {"S7": 3, "S5": 3}, "tendency": "M"},
                {"label": "C", "text": "宁可粉身碎骨，也不弯腰低头", "scores": {"S7": 5, "S5": 4}, "tendency": "H"},
            ],
            "reveal": "孙尚香正是这般宁折不弯之人。"
        },
    ],
    "吕蒙": [
        {
            "id": "q_lvmeng_1",
            "dimension": "S5",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "吕蒙",
            "source_story": "白衣渡江",
            "route_hint": None,
            "city_hint": None,
            "text": "吕蒙以白衣渡江之计奇袭荆州，此计虽险却一举成功。面对一个必须冒险才能成功的任务——",
            "options": [
                {"label": "A", "text": "寻找更稳妥的方案，不愿让弟兄们冒险", "scores": {"S5": 1, "S6": 4}, "tendency": "L"},
                {"label": "B", "text": "评估风险后再决定，必要时果断出手", "scores": {"S5": 3, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "毫不犹豫，机会稍纵即逝，犹豫就是失败", "scores": {"S5": 5, "S6": 2}, "tendency": "H"},
            ],
            "reveal": "吕蒙的选择：当断则断，以迅雷不及掩耳之势取荆州。"
        },
        {
            "id": "q_lvmeng_2",
            "dimension": "S4",
            "cross_dimension": "S8",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "你接到了一个需要伪装成商人的卧底任务，目标是一位与你有旧交的老友——",
            "options": [
                {"label": "A", "text": "拒绝任务，旧交不可利用", "scores": {"S4": 1, "S8": 4}, "tendency": "L"},
                {"label": "B", "text": "接受任务，但尽量不伤害旧友", "scores": {"S4": 3, "S8": 3}, "tendency": "M"},
                {"label": "C", "text": "完美扮演商人角色，公私分明", "scores": {"S4": 5, "S8": 2}, "tendency": "H"},
            ],
            "reveal": "吕蒙深谙伪装之道，白衣渡江便是极致体现。"
        },
    ],
    "张鲁": [
        {
            "id": "q_zhanglu_1",
            "dimension": "S10",
            "cross_dimension": "S8",
            "type": "story_known",
            "source_character": "张鲁",
            "source_story": "汉中五斗米道",
            "route_hint": ["西蜀线"],
            "city_hint": "成都",
            "text": "张鲁在汉中以五斗米道教化百姓，设义舍免费供食，以规矩治民。若有人滥用义舍之粮——",
            "options": [
                {"label": "A", "text": "睁一只眼闭一只眼，人心本善，总会改的", "scores": {"S10": 1, "S8": 4}, "tendency": "L"},
                {"label": "B", "text": "派人劝诫，屡教不改者才施以惩戒", "scores": {"S10": 3, "S8": 3}, "tendency": "M"},
                {"label": "C", "text": "立下铁规，违者必罚，以儆效尤", "scores": {"S10": 5, "S8": 2}, "tendency": "H"},
            ],
            "reveal": "张鲁的选择：以法治教，令行禁止，但心存仁念。"
        },
        {
            "id": "q_zhanglu_2",
            "dimension": "S8",
            "cross_dimension": "S10",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「治世以大德，不以小惠。」你更认同哪种治民之道？",
            "options": [
                {"label": "A", "text": "小恩小惠收买人心最有效", "scores": {"S8": 3, "S10": 1}, "tendency": "L"},
                {"label": "B", "text": "恩威并施，让百姓既感恩又敬畏", "scores": {"S8": 3, "S10": 3}, "tendency": "M"},
                {"label": "C", "text": "以德化人，制度为本，人心自归", "scores": {"S8": 4, "S10": 5}, "tendency": "H"},
            ],
            "reveal": "张鲁治汉中，义舍与法度并行，正是此道。"
        },
    ],
    "公孙珊": [
        {
            "id": "q_gongsunshan_1",
            "dimension": "S6",
            "cross_dimension": "S2",
            "type": "story_known",
            "source_character": "公孙珊",
            "source_story": "幽州风云",
            "route_hint": ["幽州线"],
            "city_hint": "幽州",
            "text": "公孙珊身在幽州公孙瓒麾下，却心怀百姓。面对公孙瓒下令屠城的军令——",
            "options": [
                {"label": "A", "text": "军令如山，执行便是", "scores": {"S6": 1, "S2": 1}, "tendency": "L"},
                {"label": "B", "text": "试图劝阻，但若无效则遵令行事", "scores": {"S6": 3, "S2": 3}, "tendency": "M"},
                {"label": "C", "text": "拼死相谏，哪怕抗命也不忍屠戮无辜", "scores": {"S6": 5, "S2": 5}, "tendency": "H"},
            ],
            "reveal": "公孙珊的选择：宁违军令，不伤无辜。"
        },
        {
            "id": "q_gongsunshan_2",
            "dimension": "S8",
            "cross_dimension": "S6",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "绣衣楼中有位密探受伤后性情大变，对同僚恶语相向。你会——",
            "options": [
                {"label": "A", "text": "以其人之道还治其身，让他知道错", "scores": {"S8": 1, "S6": 2}, "tendency": "L"},
                {"label": "B", "text": "保持距离，等他自己想通", "scores": {"S8": 2, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "耐心陪伴，理解他的痛苦，用温柔化解戾气", "scores": {"S8": 5, "S6": 4}, "tendency": "H"},
            ],
            "reveal": "公孙珊的温柔源于对苦难的深刻理解。"
        },
    ],
    "王粲": [
        {
            "id": "q_wangcan_1",
            "dimension": "S8",
            "cross_dimension": "S10",
            "type": "story_known",
            "source_character": "王粲",
            "source_story": "登楼赋",
            "route_hint": None,
            "city_hint": None,
            "text": "王粲登楼远眺，心怀家国却身不由己，写下《登楼赋》抒发思乡之情。若你在异乡不得归——",
            "options": [
                {"label": "A", "text": "既然回不去，便就地扎根，不必感伤", "scores": {"S8": 1, "S2": 1}, "tendency": "L"},
                {"label": "B", "text": "将思念化为笔墨，以文章寄托情怀", "scores": {"S8": 3, "S2": 3}, "tendency": "M"},
                {"label": "C", "text": "日夜牵挂故土，每念及此泪湿衣襟", "scores": {"S8": 5, "S2": 5}, "tendency": "H"},
            ],
            "reveal": "王粲的选择：登楼赋志，以笔为刃，以文为泪。"
        },
        {
            "id": "q_wangcan_2",
            "dimension": "S10",
            "cross_dimension": "S6",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「虽有周公之美，不如守道之贞。」面对乱世中的道德崩塌——",
            "options": [
                {"label": "A", "text": "乱世求生为先，道德是奢侈品", "scores": {"S10": 1, "S6": 1}, "tendency": "L"},
                {"label": "B", "text": "在不伤害他人的前提下灵活变通", "scores": {"S10": 3, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "即使世道崩坏，也要守住心中的道义", "scores": {"S10": 5, "S6": 5}, "tendency": "H"},
            ],
            "reveal": "王粲虽寄人篱下，却始终守着文人的骨气。"
        },
    ],
    "张修": [
        {
            "id": "q_zhangxiu2_1",
            "dimension": "S4",
            "cross_dimension": "S1",
            "type": "story_known",
            "source_character": "张修",
            "source_story": "五斗米道之争",
            "route_hint": ["西蜀线"],
            "city_hint": "成都",
            "text": "张修与张鲁同为五斗米道教主，后张鲁夺取教权。若你辛辛苦苦建立的事业被亲近之人夺走——",
            "options": [
                {"label": "A", "text": "坦然放手，名利不过是过眼云烟", "scores": {"S4": 1, "S1": 1}, "tendency": "L"},
                {"label": "B", "text": "表面隐忍，暗中积蓄力量等待时机", "scores": {"S4": 4, "S1": 4}, "tendency": "M"},
                {"label": "C", "text": "当面对质，光明正大地讨回公道", "scores": {"S4": 2, "S1": 2}, "tendency": "H"},
            ],
            "reveal": "张修在代号鸢中善于隐藏真意，以退为进。"
        },
        {
            "id": "q_zhangxiu2_2",
            "dimension": "S1",
            "cross_dimension": "S4",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "绣衣楼接到线报：一位密探可能是敌方卧底，但证据不足。你负责处理此事——",
            "options": [
                {"label": "A", "text": "直接审问，打草惊蛇也无妨", "scores": {"S1": 2, "S4": 1}, "tendency": "L"},
                {"label": "B", "text": "设局试探，不动声色地观察", "scores": {"S1": 4, "S4": 4}, "tendency": "M"},
                {"label": "C", "text": "向上级汇报，等待指示再做打算", "scores": {"S1": 2, "S4": 3}, "tendency": "H"},
            ],
            "reveal": "张修的处理方式：以静制动，让对手自露马脚。"
        },
    ],
    "干吉": [
        {
            "id": "q_ganji_1",
            "dimension": "S6",
            "cross_dimension": "S8",
            "type": "story_known",
            "source_character": "干吉",
            "source_story": "太平道",
            "route_hint": None,
            "city_hint": None,
            "text": "干吉创太平道，以符水治病救人。若有人利用他的符水欺骗百姓牟利——",
            "options": [
                {"label": "A", "text": "怒不可遏，当众揭露骗子的真面目", "scores": {"S6": 4, "S7": 3}, "tendency": "L"},
                {"label": "B", "text": "不动声色，暗中调查后再做处理", "scores": {"S6": 3, "S8": 3}, "tendency": "M"},
                {"label": "C", "text": "以德报怨，用真正的道法感化对方", "scores": {"S6": 5, "S8": 5}, "tendency": "H"},
            ],
            "reveal": "干吉的选择：坚守道义底线，以慈悲之心化解恶意。"
        },
        {
            "id": "q_ganji_2",
            "dimension": "S8",
            "cross_dimension": "S6",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「救人一命胜造七级浮屠。」面对一个素不相识的重伤之人——",
            "options": [
                {"label": "A", "text": "先确认此人是否值得救", "scores": {"S8": 1, "S6": 2}, "tendency": "L"},
                {"label": "B", "text": "能救就救，但也不会把自己搭进去", "scores": {"S8": 3, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "不问来历，不计代价，全力以赴救治", "scores": {"S8": 5, "S6": 5}, "tendency": "H"},
            ],
            "reveal": "干吉以符水济世，从不问来者身份。"
        },
    ],
    "庞统": [
        {
            "id": "q_pangtong_1",
            "dimension": "S8",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "庞统",
            "source_story": "落凤坡",
            "route_hint": ["西蜀线"],
            "city_hint": "成都",
            "text": "庞统虽貌不惊人，却胸怀锦绣。面对旁人的嘲笑与轻视——",
            "options": [
                {"label": "A", "text": "以牙还牙，让他们见识自己的厉害", "scores": {"S8": 1, "S7": 4}, "tendency": "L"},
                {"label": "B", "text": "一笑置之，用实力说话", "scores": {"S8": 3, "S7": 2}, "tendency": "M"},
                {"label": "C", "text": "反以温和的态度待他们，以德化人", "scores": {"S8": 5, "S6": 4}, "tendency": "H"},
            ],
            "reveal": "庞统选择：大智若愚，以温和掩饰锋芒。"
        },
        {
            "id": "q_pangtong_2",
            "dimension": "S10",
            "cross_dimension": "S1",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「天下有道则见，无道则隐。」面对乱世——",
            "options": [
                {"label": "A", "text": "乱世出英雄，正是大显身手之时", "scores": {"S10": 1, "S1": 4}, "tendency": "L"},
                {"label": "B", "text": "待价而沽，择明主而仕", "scores": {"S10": 3, "S1": 3}, "tendency": "M"},
                {"label": "C", "text": "道之不存，不如归隐山林", "scores": {"S10": 5, "S1": 1}, "tendency": "H"},
            ],
            "reveal": "庞统虽出山辅佐刘备，内心始终有归隐之意。"
        },
    ],
    "蒯良": [
        {
            "id": "q_kuailiang_1",
            "dimension": "S10",
            "cross_dimension": "S1",
            "type": "story_known",
            "source_character": "蒯良",
            "source_story": "荆州谋士",
            "route_hint": None,
            "city_hint": "长沙",
            "text": "蒯良为荆州蒯氏一族的核心谋士，在刘表帐下出谋划策。面对荆州内部的派系之争——",
            "options": [
                {"label": "A", "text": "站队表态，壮大自己一方的势力", "scores": {"S10": 1, "S1": 4}, "tendency": "L"},
                {"label": "B", "text": "居中调停，维持荆州内部的平衡", "scores": {"S10": 3, "S1": 3}, "tendency": "M"},
                {"label": "C", "text": "以制度和规矩约束各方，不许越界", "scores": {"S10": 5, "S1": 2}, "tendency": "H"},
            ],
            "reveal": "蒯良选择：以礼法为纲，维系荆州秩序。"
        },
        {
            "id": "q_kuailiang_2",
            "dimension": "S1",
            "cross_dimension": "S10",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "绣衣楼收到三方势力的密信，每封都附带不同的利益交换。你会——",
            "options": [
                {"label": "A", "text": "谁给的利益大就跟谁合作", "scores": {"S1": 4, "S3": 4, "S10": 1}, "tendency": "L"},
                {"label": "B", "text": "权衡利弊后选择对绣衣楼最有利的", "scores": {"S1": 3, "S10": 3}, "tendency": "M"},
                {"label": "C", "text": "按规矩办事，不因利益动摇立场", "scores": {"S1": 2, "S10": 5}, "tendency": "H"},
            ],
            "reveal": "蒯良会以大局和规矩为重。"
        },
    ],
    "周群": [
        {
            "id": "q_zhouqun_1",
            "dimension": "S10",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "周群",
            "source_story": "益州占星",
            "route_hint": ["西蜀线"],
            "city_hint": "成都",
            "text": "周群精通天文历法，能观星象而知天命。若他观测到一场大灾将至，而告知百姓可能引起恐慌——",
            "options": [
                {"label": "A", "text": "先通知权贵，让他们做好准备", "scores": {"S10": 2, "S6": 2}, "tendency": "L"},
                {"label": "B", "text": "以隐晦的方式提醒百姓，避免直接引发恐慌", "scores": {"S10": 3, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "如实告知，宁可被指责散布谣言也要救人", "scores": {"S10": 5, "S6": 5}, "tendency": "H"},
            ],
            "reveal": "周群选择：尽人事以听天命，该说的绝不含糊。"
        },
        {
            "id": "q_zhouqun_2",
            "dimension": "S8",
            "cross_dimension": "S10",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「知天命而不违，尽人事而听天。」你如何看待命运？",
            "options": [
                {"label": "A", "text": "命运掌握在自己手中，与天无关", "scores": {"S8": 1, "S10": 1}, "tendency": "L"},
                {"label": "B", "text": "天命有定，但人可以努力改变", "scores": {"S8": 3, "S10": 3}, "tendency": "M"},
                {"label": "C", "text": "顺应天道，心怀敬畏地做好每一件事", "scores": {"S8": 4, "S10": 5}, "tendency": "H"},
            ],
            "reveal": "周群观星知命，却从不以此自傲。"
        },
    ],
    "蔡琰": [
        {
            "id": "q_caiyan_1",
            "dimension": "S2",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "蔡琰",
            "source_story": "胡笳十八拍",
            "route_hint": None,
            "city_hint": None,
            "text": "蔡琰被掳至南匈奴十二年，写下《胡笳十八拍》。身陷异乡，日夜思念故土与亲人——",
            "options": [
                {"label": "A", "text": "强忍思念，接受现实，在异乡重新开始", "scores": {"S2": 1, "S5": 3}, "tendency": "L"},
                {"label": "B", "text": "以琴音寄托哀思，等待归乡的机会", "scores": {"S2": 3, "S5": 2}, "tendency": "M"},
                {"label": "C", "text": "每一日都是煎熬，魂牵梦萦皆为故土亲人", "scores": {"S2": 5, "S5": 1}, "tendency": "H"},
            ],
            "reveal": "蔡琰的选择：以血泪成诗，胡笳十八拍字字断肠。"
        },
        {
            "id": "q_caiyan_2",
            "dimension": "S6",
            "cross_dimension": "S2",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「身不由己，心不由人。」面对无法改变的命运——",
            "options": [
                {"label": "A", "text": "命运既然如此，便随波逐流", "scores": {"S6": 1, "S2": 1}, "tendency": "L"},
                {"label": "B", "text": "身体可以被困，但灵魂和才华不会", "scores": {"S6": 3, "S2": 3}, "tendency": "M"},
                {"label": "C", "text": "即使在绝境中，也要守住做人的底线", "scores": {"S6": 5, "S2": 4}, "tendency": "H"},
            ],
            "reveal": "蔡琰在匈奴十二年，始终未忘文人风骨。"
        },
    ],
    "虞翻": [
        {
            "id": "q_yufan_1",
            "dimension": "S5",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "虞翻",
            "source_story": "东吴直臣",
            "route_hint": None,
            "city_hint": None,
            "text": "虞翻以直言敢谏闻名东吴，多次触怒孙权却从不退缩。面对上位者的错误决策——",
            "options": [
                {"label": "A", "text": "私下劝谏即可，当众反驳太冒犯了", "scores": {"S5": 2, "S6": 3}, "tendency": "L"},
                {"label": "B", "text": "据理力争，但注意措辞和场合", "scores": {"S5": 3, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "不管对方是谁，错了就要当面指出", "scores": {"S5": 5, "S6": 4}, "tendency": "H"},
            ],
            "reveal": "虞翻的选择：宁被贬谪，也不做应声虫。"
        },
        {
            "id": "q_yufan_2",
            "dimension": "S10",
            "cross_dimension": "S7",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "绣衣楼新来了一个不守规矩但才华出众的密探，你会——",
            "options": [
                {"label": "A", "text": "规矩就是规矩，必须遵守", "scores": {"S10": 5, "S7": 2}, "tendency": "L"},
                {"label": "B", "text": "给他一些灵活空间，但底线不能碰", "scores": {"S10": 3, "S7": 3}, "tendency": "M"},
                {"label": "C", "text": "有才华的人就该特殊对待", "scores": {"S10": 1, "S7": 4}, "tendency": "H"},
            ],
            "reveal": "虞翻认为规矩是立身之本，不可轻废。"
        },
    ],
    "陆逊": [
        {
            "id": "q_luxun_1",
            "dimension": "S1",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "陆逊",
            "source_story": "夷陵之战",
            "route_hint": None,
            "city_hint": None,
            "text": "陆逊以火烧连营之计大败刘备，一战成名。面对以少敌多的绝境——",
            "options": [
                {"label": "A", "text": "力拼到底，宁战死不退缩", "scores": {"S1": 1, "S5": 4}, "tendency": "L"},
                {"label": "B", "text": "冷静分析局势，寻找对手的破绽", "scores": {"S1": 4, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "假意示弱诱敌深入，一举歼灭", "scores": {"S1": 5, "S6": 4}, "tendency": "H"},
            ],
            "reveal": "陆逊的选择：隐忍数月不战，待蜀军疲惫后一击致命。"
        },
        {
            "id": "q_luxun_2",
            "dimension": "S6",
            "cross_dimension": "S1",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「智者千虑，必有一失。」当你精心布局的计划出现纰漏时——",
            "options": [
                {"label": "A", "text": "立刻调整计划，随机应变", "scores": {"S6": 2, "S1": 3}, "tendency": "L"},
                {"label": "B", "text": "权衡利弊后决定是继续还是放弃", "scores": {"S6": 3, "S1": 3}, "tendency": "M"},
                {"label": "C", "text": "即便计划有误，也绝不做违背底线的事来弥补", "scores": {"S6": 5, "S1": 2}, "tendency": "H"},
            ],
            "reveal": "陆逊的底线坚如磐石，谋略可以变，原则不可改。"
        },
    ],
    "钟繇": [
        {
            "id": "q_zhongyao_1",
            "dimension": "S10",
            "cross_dimension": "S9",
            "type": "story_known",
            "source_character": "钟繇",
            "source_story": "镇守关中",
            "route_hint": None,
            "city_hint": None,
            "text": "钟繇受命镇守关中，在曹操后方维持稳定。面对关中各路诸侯的明争暗斗——",
            "options": [
                {"label": "A", "text": "联合一方打压另一方，以战止战", "scores": {"S10": 1, "S9": 3}, "tendency": "L"},
                {"label": "B", "text": "以朝廷法度为准则，公正处理各方争端", "scores": {"S10": 4, "S9": 3}, "tendency": "M"},
                {"label": "C", "text": "严刑峻法，铁腕治关，不许任何人越雷池", "scores": {"S10": 5, "S9": 4}, "tendency": "H"},
            ],
            "reveal": "钟繇的选择：以法度镇关中，恩威并施。"
        },
        {
            "id": "q_zhongyao_2",
            "dimension": "S6",
            "cross_dimension": "S10",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "你发现绣衣楼的档案中有一份关于你至亲的不利记录——",
            "options": [
                {"label": "A", "text": "偷偷销毁记录，保护至亲", "scores": {"S6": 2, "S10": 1}, "tendency": "L"},
                {"label": "B", "text": "如实上报，让组织来处理", "scores": {"S6": 4, "S10": 4}, "tendency": "M"},
                {"label": "C", "text": "主动请缨负责此案，确保公正处理", "scores": {"S6": 5, "S10": 5}, "tendency": "H"},
            ],
            "reveal": "钟繇会以法度为先，公私分明。"
        },
    ],
    "耿公子": [
        {
            "id": "q_genggongzi_1",
            "dimension": "S2",
            "cross_dimension": "S4",
            "type": "story_known",
            "source_character": "耿公子",
            "source_story": "广陵往事",
            "route_hint": None,
            "city_hint": "广陵",
            "text": "耿公子出入广陵名流圈，表面潇洒不羁，内心却有自己的坚持。面对朋友的背叛——",
            "options": [
                {"label": "A", "text": "断绝来往，再不与此人有任何交集", "scores": {"S2": 1, "S4": 2}, "tendency": "L"},
                {"label": "B", "text": "表面如常，但心中已有了防备", "scores": {"S2": 2, "S4": 3}, "tendency": "M"},
                {"label": "C", "text": "坦诚沟通，若对方真有苦衷可以原谅", "scores": {"S2": 4, "S4": 1}, "tendency": "H"},
            ],
            "reveal": "耿公子重情义，但也并非毫无城府。"
        },
        {
            "id": "q_genggongzi_2",
            "dimension": "S3",
            "cross_dimension": "S2",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「千金散尽还复来。」你对金钱的态度是？",
            "options": [
                {"label": "A", "text": "钱是用来花的，够用就行，不必执着", "scores": {"S3": 1, "S2": 3}, "tendency": "L"},
                {"label": "B", "text": "该花的花，该省的省，量入为出", "scores": {"S3": 3, "S2": 3}, "tendency": "M"},
                {"label": "C", "text": "钱是安身立命之本，必须精打细算", "scores": {"S3": 5, "S2": 2}, "tendency": "H"},
            ],
            "reveal": "耿公子看似潇洒，实则深谙理财之道。"
        },
    ],
    "陈宫": [
        {
            "id": "q_chengong_1",
            "dimension": "S1",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "陈宫",
            "source_story": "下邳之战",
            "route_hint": None,
            "city_hint": "下邳",
            "text": "陈宫辅佐吕布，明知布非明主却忠心不二。面对曹操招降——",
            "options": [
                {"label": "A", "text": "识时务者为俊杰，降曹保命", "scores": {"S1": 4, "S6": 1}, "tendency": "L"},
                {"label": "B", "text": "犹豫不决，既不甘心又不想死", "scores": {"S1": 2, "S6": 2}, "tendency": "M"},
                {"label": "C", "text": "宁可赴死，也不背弃自己的选择", "scores": {"S1": 2, "S6": 5}, "tendency": "H"},
            ],
            "reveal": "陈宫的选择：慷慨赴死，至死不渝。"
        },
        {
            "id": "q_chengong_2",
            "dimension": "S6",
            "cross_dimension": "S1",
            "type": "value",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": "「择主而事，忠臣不事二主。」你怎么看待忠诚？",
            "options": [
                {"label": "A", "text": "良禽择木而栖，跟对人最重要", "scores": {"S6": 1, "S1": 4}, "tendency": "L"},
                {"label": "B", "text": "一旦选择便负责到底，但前提是对方值得", "scores": {"S6": 3, "S1": 3}, "tendency": "M"},
                {"label": "C", "text": "忠义二字重于泰山，不可背弃", "scores": {"S6": 5, "S1": 1}, "tendency": "H"},
            ],
            "reveal": "陈宫以死明志，诠释了何为忠义。"
        },
    ],
    "马腾": [
        {
            "id": "q_mateng_1",
            "dimension": "S5",
            "cross_dimension": "S6",
            "type": "story_known",
            "source_character": "马腾",
            "source_story": "西凉雄狮",
            "route_hint": ["西凉线"],
            "city_hint": None,
            "text": "马腾起兵西凉，以勇武著称。面对董卓残暴治下的百姓哀号——",
            "options": [
                {"label": "A", "text": "暂且隐忍，积蓄力量再举义旗", "scores": {"S5": 1, "S6": 3}, "tendency": "L"},
                {"label": "B", "text": "联络各路诸侯共同讨伐", "scores": {"S5": 3, "S6": 3}, "tendency": "M"},
                {"label": "C", "text": "立即起兵，就算只有自己一人也要 fight", "scores": {"S5": 5, "S6": 4}, "tendency": "H"},
            ],
            "reveal": "马腾的选择：西凉铁骑出征，只为还百姓一个公道。"
        },
        {
            "id": "q_mateng_2",
            "dimension": "S6",
            "cross_dimension": "S5",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "你的同袍在战斗中临阵脱逃，导致小队陷入险境。事后——",
            "options": [
                {"label": "A", "text": "上军事法庭，按军法处置", "scores": {"S6": 5, "S5": 2}, "tendency": "L"},
                {"label": "B", "text": "严厉批评，但给他一个将功折罪的机会", "scores": {"S6": 3, "S5": 3}, "tendency": "M"},
                {"label": "C", "text": "先问问原因，也许有不得已的苦衷", "scores": {"S6": 2, "S5": 2}, "tendency": "H"},
            ],
            "reveal": "马腾治军严明，但重情义，会视情况而定。"
        },
    ],
    "伍丹": [
        {
            "id": "q_wudan_1",
            "dimension": "S3",
            "cross_dimension": "S1",
            "type": "story_known",
            "source_character": "伍丹",
            "source_story": "绣衣楼密探",
            "route_hint": None,
            "city_hint": "广陵",
            "text": "伍丹在绣衣楼中执行任务时常需要打点各方关系。面对一笔数目不小的额外开销——",
            "options": [
                {"label": "A", "text": "自掏腰包，不该让组织承担", "scores": {"S3": 1, "S6": 3}, "tendency": "L"},
                {"label": "B", "text": "如实上报，按流程报销", "scores": {"S3": 3, "S10": 3}, "tendency": "M"},
                {"label": "C", "text": "精打细算，用最少的钱办最大的事", "scores": {"S3": 5, "S1": 3}, "tendency": "H"},
            ],
            "reveal": "伍丹善于在有限的资源中最大化效用。"
        },
        {
            "id": "q_wudan_2",
            "dimension": "S1",
            "cross_dimension": "S3",
            "type": "daily",
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": "广陵",
            "text": "你得知一位富商掌握着关键情报，但他要求高额报酬才肯交出——",
            "options": [
                {"label": "A", "text": "给钱，情报比金钱重要", "scores": {"S1": 3, "S3": 1}, "tendency": "L"},
                {"label": "B", "text": "讨价还价，用最少的代价拿到情报", "scores": {"S1": 4, "S3": 4}, "tendency": "M"},
                {"label": "C", "text": "另辟蹊径，不花钱也能搞到情报", "scores": {"S1": 5, "S3": 5}, "tendency": "H"},
            ],
            "reveal": "伍丹的信条：能用脑子解决的问题，绝不浪费钱。"
        },
    ],
}

# === DB验证 ===
def verify_dialogues():
    """Check dialogues for story questions"""
    results = {}
    for char, qs in QUESTIONS.items():
        lines = db_speaker(char)
        results[char] = len(lines)
        if lines:
            print(f"  {char}: {len(lines)} lines from DB")
    return results

# === WRITE FILES ===
FILE_MAP = {
    "安期": "anqi.json",
    "小乔": "xiaoqiao.json",
    "孙尚香": "sunshangxiang.json",
    "吕蒙": "lvmeng.json",
    "张鲁": "zhanglu.json",
    "公孙珊": "gongsunshan.json",
    "王粲": "wangcan.json",
    "张修": "zhangxiu2.json",
    "干吉": "ganji.json",
    "庞统": "pangtong.json",
    "蒯良": "kuailiang.json",
    "周群": "zhouqun.json",
    "蔡琰": "caiyan.json",
    "虞翻": "yufan.json",
    "陆逊": "luxun.json",
    "钟繇": "zhongyao.json",
    "耿公子": "genggongzi.json",
    "陈宫": "chengong.json",
    "马腾": "mateng.json",
    "伍丹": "wudan.json",
}

def main():
    os.makedirs(QDIR, exist_ok=True)
    
    # Verify dialogues from DB
    print("=== 验证数据库台词 ===")
    db_results = verify_dialogues()
    
    # Write question files
    print("\n=== 写入题库文件 ===")
    total = 0
    for char, filename in FILE_MAP.items():
        qs = QUESTIONS[char]
        filepath = os.path.join(QDIR, filename)
        
        # Load existing if exists, else create new array
        existing = []
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    existing = json.load(f)
                except:
                    existing = []
        
        # Add new questions (avoid duplicates by id)
        existing_ids = {q["id"] for q in existing}
        new_count = 0
        for q in qs:
            if q["id"] not in existing_ids:
                existing.append(q)
                new_count += 1
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        
        total += new_count
        print(f"  {char} -> {filename}: +{new_count} (total: {len(existing)})")
    
    print(f"\n总计新增: {total} 道")

if __name__ == "__main__":
    main()
