#!/usr/bin/env python3
import json

# 题目列表
questions = []

# 1. sweet批次 (甜蜜暧昧)
questions.append({
    "id": "zuoci_sweet_01",
    "type": "sweet",
    "dimension": ["S8", "S2"],
    "source_character": "左慈",
    "text": "左慈教你钓鱼，你等了一整夜都没钓到，困得直打瞌睡。",
    "options": [
        {
            "label": "A",
            "text": "找个借口先回去，明天再来。",
            "scores": {"S8": 1, "S2": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "继续陪着左慈，听他讲钓鱼的耐心。",
            "scores": {"S8": 3, "S2": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "轻轻靠在他肩头小睡，让他继续钓。",
            "scores": {"S8": 5, "S2": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“你靠着睡一会吧。吾今夜一定能钓到。”——左慈在七夕欢情钓鱼时，让广陵王安心休息，自己坚持等待。"
})

questions.append({
    "id": "zuoci_sweet_02",
    "type": "sweet",
    "dimension": ["S8", "S4"],
    "source_character": "左慈",
    "text": "左慈辟谷不食，却为你烤肉。你看着他专注翻烤的样子。",
    "options": [
        {
            "label": "A",
            "text": "默默吃完，道谢后离开。",
            "scores": {"S8": 1, "S4": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "问他为什么不吃，劝他也尝一点。",
            "scores": {"S8": 3, "S4": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "夹起一块肉，递到他嘴边请他试试。",
            "scores": {"S8": 5, "S4": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“吾辟谷，不食炙肉，你吃吧。”“没事，你慢慢吃。吾替你烤。”——左慈在七夕欢情中虽不食肉，却亲手为广陵王烤肉。"
})

questions.append({
    "id": "zuoci_sweet_03",
    "type": "sweet",
    "dimension": ["S2", "S10"],
    "source_character": "左慈",
    "text": "左慈带你去看麒麟，说它的眼睛能看见寿数。你有些害怕。",
    "options": [
        {
            "label": "A",
            "text": "拒绝观看，转移话题去看别的。",
            "scores": {"S2": 1, "S10": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "听从左慈的指导，小心地观察麒麟。",
            "scores": {"S2": 3, "S10": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握紧左慈的手，问他是否也见过自己的寿数。",
            "scores": {"S2": 5, "S10": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“很漂亮吧？若久视它的双眼，可以见到自己的寿数。”——左慈在垂麒坠中向广陵王展示麒麟，语气平静却充满深意。"
})

questions.append({
    "id": "zuoci_sweet_04",
    "type": "sweet",
    "dimension": ["S8", "S6"],
    "source_character": "左慈",
    "text": "左慈喝醉了，难得露出脆弱的样子，拉着你的手说对不起。",
    "options": [
        {
            "label": "A",
            "text": "扶他躺下休息，自己离开让他静一静。",
            "scores": {"S8": 1, "S6": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "陪在他身边，轻声安慰说没事。",
            "scores": {"S8": 3, "S6": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握住他的手，告诉他你一直在，不会离开。",
            "scores": {"S8": 5, "S6": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“对不起……在你面前露出这副样子。”“为什么……那么多次……为什么……还要回来……”——左慈在七载相逢中醉酒后的真情流露。"
})

questions.append({
    "id": "zuoci_sweet_05",
    "type": "sweet",
    "dimension": ["S2", "S4"],
    "source_character": "左慈",
    "text": "左慈说，有你在的人间，他便会记得自己是谁。",
    "options": [
        {
            "label": "A",
            "text": "笑笑说师尊又说奇怪的话了。",
            "scores": {"S2": 1, "S4": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认真回答，我会一直陪着师尊。",
            "scores": {"S2": 3, "S4": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "轻轻抱住他，说我就是你的锚点。",
            "scores": {"S2": 5, "S4": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“有你在的人间，左慈便在。”——左慈在古艳歌中表达广陵王对他存在的意义。"
})

# 2. funny批次 (搞笑玩梗)
questions.append({
    "id": "zuoci_funny_01",
    "type": "funny",
    "dimension": ["S3", "S7"],
    "source_character": "左慈",
    "text": "左慈投壶连中十支，老板掀桌了。他一脸无辜地问为什么。",
    "options": [
        {
            "label": "A",
            "text": "赶紧拉走左慈，说我们去玩别的。",
            "scores": {"S3": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "跟老板道歉，解释左慈不是故意的。",
            "scores": {"S3": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "帮左慈理论，规则又没写不能用仙术。",
            "scores": {"S3": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“十支，十支，十支……嗯？老板为什么掀桌了？”“不能用仙术操控箭直接进壶？可是规则上没写……”——左慈在七夕欢情中凭实力（仙术）砸场子。"
})

questions.append({
    "id": "zuoci_funny_02",
    "type": "funny",
    "dimension": ["S5", "S9"],
    "source_character": "左慈",
    "text": "左慈下棋赢了观星台六个月的收益，问你满意了吗。",
    "options": [
        {
            "label": "A",
            "text": "见好就收，说够了我们走吧。",
            "scores": {"S5": 1, "S9": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "开心收下，夸师尊真厉害。",
            "scores": {"S5": 3, "S9": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "怂恿他再赢六个月，凑够一年。",
            "scores": {"S5": 5, "S9": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“一夜之间赢了六个月的收益，满意了？哈……心满意足了，就去下一个地方吧。”——左慈在七夕欢情中展现高超棋艺和宠徒弟的一面。"
})

questions.append({
    "id": "zuoci_funny_03",
    "type": "funny",
    "dimension": ["S3", "S10"],
    "source_character": "左慈",
    "text": "左慈研究奶茶菜单，被全糖半糖去冰温热搞得头大。",
    "options": [
        {
            "label": "A",
            "text": "直接帮他点一杯最普通的。",
            "scores": {"S3": 1, "S10": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "耐心解释每种选项的意思。",
            "scores": {"S3": 3, "S10": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "每样都点一杯，让他都尝尝。",
            "scores": {"S3": 5, "S10": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“菜牌上居然有那么多字……正常冰，去冰，常温，温热，热……全糖，半糖，无糖……”“居然还要放蜜饯，栗子、花生碎、枸杞？这到底是饮品还是八宝粥……”——左慈面对现代饮料的困惑。"
})

questions.append({
    "id": "zuoci_funny_04",
    "type": "funny",
    "dimension": ["S7", "S4"],
    "source_character": "左慈",
    "text": "左慈用仙术帮摊主造冰做凉面，摊主目瞪口呆。",
    "options": [
        {
            "label": "A",
            "text": "赶紧付钱拉走左慈，避免引起骚动。",
            "scores": {"S7": 1, "S4": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "向摊主解释这是隐鸢阁的秘术。",
            "scores": {"S7": 3, "S4": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "大声夸赞师尊真厉害，再来一桶冰。",
            "scores": {"S7": 5, "S4": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“凉面卖完了？因为没有冰吗……稍等。”“好了，吾替他造了一桶冰。可以点凉面了。”——左慈用仙术解决夏日吃凉面的实际问题。"
})

questions.append({
    "id": "zuoci_funny_05",
    "type": "funny",
    "dimension": ["S5", "S8"],
    "source_character": "左慈",
    "text": "左慈回忆你小时候撬沉香神像，从塔顶滚下去引发雪崩的糗事。",
    "options": [
        {
            "label": "A",
            "text": "尴尬地打断，说别提这些了。",
            "scores": {"S5": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "笑着听他说完，补充细节。",
            "scores": {"S5": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "反问他当时是不是很头疼，但又舍不得丢下你。",
            "scores": {"S5": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“然后一起从塔顶滑下去，抱着神像从雪山往下滚，最后神像碎了，撞塌宿舍五间，引发雪崩，一个摔断了左手一个摔断了右腿。”——左慈在七载相逢中回忆广陵王儿时的调皮。"
})

# 3. angst批次 (扎心虐心)
questions.append({
    "id": "zuoci_angst_01",
    "type": "angst",
    "dimension": ["S2", "S6"],
    "source_character": "左慈",
    "text": "左慈说，雪球一旦从山顶滚落，无论你有多大的勇气都无法阻挡。",
    "options": [
        {
            "label": "A",
            "text": "沉默不语，接受这个残酷的现实。",
            "scores": {"S2": 1, "S6": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "问他那我们应该怎么办。",
            "scores": {"S2": 3, "S6": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握住他的手说，至少师尊会陪我一起面对。",
            "scores": {"S2": 5, "S6": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“雪球一旦开始从山顶滚落……无论你抱有多大的意志和勇气张开双臂，都无法阻挡它的滚落。”——左慈在犬都纪事中对时局的悲观判断。"
})

questions.append({
    "id": "zuoci_angst_02",
    "type": "angst",
    "dimension": ["S4", "S10"],
    "source_character": "左慈",
    "text": "左慈说，有时他会忘记自己的名字，活得太久记忆在流失。",
    "options": [
        {
            "label": "A",
            "text": "避开这个话题，说点开心的。",
            "scores": {"S4": 1, "S10": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "轻轻叫他一声“左慈”，帮他记住。",
            "scores": {"S4": 3, "S10": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "抱住他说，我会一遍遍叫你，直到你永远记得。",
            "scores": {"S4": 5, "S10": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“有时，吾会忘记自己的名字。”——左慈在七载相逢中透露长生带来的副作用。"
})

questions.append({
    "id": "zuoci_angst_03",
    "type": "angst",
    "dimension": ["S8", "S2"],
    "source_character": "左慈",
    "text": "左慈说，真想看你穿上嫁衣的那日，但又怕等不到。",
    "options": [
        {
            "label": "A",
            "text": "笑着说师尊又说笑了。",
            "scores": {"S8": 1, "S2": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认真地说，我会让师尊看到的。",
            "scores": {"S8": 3, "S2": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握住他的手说，那师尊要活到那一天，亲自为我披上嫁衣。",
            "scores": {"S8": 5, "S2": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“真想看你穿上它的那日。”——左慈在古艳歌中流露出对广陵王未来的期许与不舍。"
})

questions.append({
    "id": "zuoci_angst_04",
    "type": "angst",
    "dimension": ["S6", "S9"],
    "source_character": "左慈",
    "text": "左慈说，权力是石头，拿起石头先让他们恐惧你，才能让他们爱你。",
    "options": [
        {
            "label": "A",
            "text": "表示不想用恐惧统治。",
            "scores": {"S6": 1, "S9": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "请教他如何平衡恐惧与爱。",
            "scores": {"S6": 3, "S9": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "告诉他，我不需要他们爱我，我只要有师尊就够了。",
            "scores": {"S6": 5, "S9": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“权力是石头，你把它裹上丝绸也好、染成彩色也好，它的本质都是石头。拿起石头，先让他们恐惧你，才能让他们爱你。”——左慈在犬都纪事中传授权力本质。"
})

questions.append({
    "id": "zuoci_angst_05",
    "type": "angst",
    "dimension": ["S2", "S4"],
    "source_character": "左慈",
    "text": "左慈说，乱世恩仇皆是明月芦花，唯有他会永远站在你这边。",
    "options": [
        {
            "label": "A",
            "text": "感谢他的支持，但说自己可以独立面对。",
            "scores": {"S2": 1, "S4": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "点头说，我知道师尊会一直在。",
            "scores": {"S2": 3, "S4": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "靠在他肩上说，那师尊要说话算话，永远不能离开我。",
            "scores": {"S2": 5, "S4": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“乱世恩仇，皆是明月芦花。唯有吾，无论发生何事，都会站在你那一边。”——左慈在乌飞中给广陵王的承诺。"
})

# 4. scheme批次 (权谋博弈)
questions.append({
    "id": "zuoci_scheme_01",
    "type": "scheme",
    "dimension": ["S1", "S9"],
    "source_character": "左慈",
    "text": "左慈分析里八华，说这个组织存在千年，擅长伪装、渗透、离间。",
    "options": [
        {
            "label": "A",
            "text": "表示担忧，问能否避开他们。",
            "scores": {"S1": 1, "S9": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "请教他如何识别和防范里八华。",
            "scores": {"S1": 3, "S9": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "提出主动渗透里八华，以彼之道还施彼身。",
            "scores": {"S1": 5, "S9": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“除了吾，不要相信任何人。”——左慈在东郡太守中揭示里八华的存在，并提醒广陵王警惕。"
})

questions.append({
    "id": "zuoci_scheme_02",
    "type": "scheme",
    "dimension": ["S9", "S10"],
    "source_character": "左慈",
    "text": "左慈说，想要安定就要牺牲掉、亲手扼杀掉一些有趣的东西。",
    "options": [
        {
            "label": "A",
            "text": "表示不愿牺牲有趣的东西。",
            "scores": {"S9": 1, "S10": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "问他如何平衡安定与自由。",
            "scores": {"S9": 3, "S10": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说那由我来做扼杀者，师尊只需看着就好。",
            "scores": {"S9": 5, "S10": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“想要安定，就要牺牲掉、亲手扼杀掉一些东西。光暗一体，没有十全十美遂人愿的人间。”——左慈在七载相逢中对治理的冷酷见解。"
})

questions.append({
    "id": "zuoci_scheme_03",
    "type": "scheme",
    "dimension": ["S1", "S6"],
    "source_character": "左慈",
    "text": "左慈教你，抱着成为下一个公敌的觉悟，做你觉得正确的事。",
    "options": [
        {
            "label": "A",
            "text": "表示不想成为公敌，会谨慎行事。",
            "scores": {"S1": 1, "S6": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "接受教导，做好心理准备。",
            "scores": {"S1": 3, "S6": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "笑着说，那师尊要陪我一起当公敌。",
            "scores": {"S1": 5, "S6": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“抱着成为下一个公敌的觉悟，做你觉得正确的事吧。”——左慈在犬都纪事中鼓励广陵王坚持自己的道路。"
})

questions.append({
    "id": "zuoci_scheme_04",
    "type": "scheme",
    "dimension": ["S9", "S4"],
    "source_character": "左慈",
    "text": "左慈说，人世间的安定最终依赖于没收刀兵、制定律法、约束道德。",
    "options": [
        {
            "label": "A",
            "text": "觉得这些太理想化，难以实现。",
            "scores": {"S9": 1, "S4": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "请教他具体如何实施。",
            "scores": {"S9": 3, "S4": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说那我要成为制定律法的人，请师尊辅佐我。",
            "scores": {"S9": 5, "S4": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“你最后会发现，无论作恶还是为善，人间的安定，最终都依赖于没收刀兵、制定律法、约束道德。”——左慈在七载相逢中对社会治理的总结。"
})

questions.append({
    "id": "zuoci_scheme_05",
    "type": "scheme",
    "dimension": ["S1", "S10"],
    "source_character": "左慈",
    "text": "左慈分析朝堂局势，说清君侧需要先占领武库，封锁内廷外朝消息。",
    "options": [
        {
            "label": "A",
            "text": "表示这些太危险，不如静观其变。",
            "scores": {"S1": 1, "S10": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认真记下他的策略，以备不时之需。",
            "scores": {"S1": 3, "S10": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "追问细节，计划如何具体执行。",
            "scores": {"S1": 5, "S10": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“有那一天的话，不能直白叫造反，要先找个清君侧或者衣带诏的名目，先占领武库，封锁内廷外朝消息往来……”——左慈在七载相逢中详细讲解政变步骤。"
})

# 5. daily批次 (日常温馨)
questions.append({
    "id": "zuoci_daily_01",
    "type": "daily",
    "dimension": ["S3", "S8"],
    "source_character": "左慈",
    "text": "左慈提醒你晚上饿了可以吃点心，饿着入睡一整夜都睡不好。",
    "options": [
        {
            "label": "A",
            "text": "答应一声，但没放在心上。",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "谢谢他的关心，说会记得吃。",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "撒娇说那师尊要提醒我，不然我会忘记。",
            "scores": {"S3": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“要带一些回去吗？你晚上饿了可以吃。”“现在还会吃睡前点心吗？饿着入睡，一整夜都是睡不好的。”——左慈在七夕欢情中关心广陵王的饮食起居。"
})

questions.append({
    "id": "zuoci_daily_02",
    "type": "daily",
    "dimension": ["S8", "S5"],
    "source_character": "左慈",
    "text": "左慈帮你串麒麟鳞片玉佩，问你想要什么形状的配饰。",
    "options": [
        {
            "label": "A",
            "text": "说随便，师尊决定就好。",
            "scores": {"S8": 1, "S5": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "选择经典的环形，方便佩戴。",
            "scores": {"S8": 3, "S5": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说要师尊形状的，戴在身上就像师尊陪着。",
            "scores": {"S8": 5, "S5": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“麒麟的鳞片，也是世间少有的宝物，可辟除病邪毒物。吾帮你串吧，将玉佩拿来。”“想要什么形状的配饰？环形？兽头？”——左慈在垂麒坠中为广陵王制作护身符。"
})

questions.append({
    "id": "zuoci_daily_03",
    "type": "daily",
    "dimension": ["S10", "S3"],
    "source_character": "左慈",
    "text": "左慈检查你的行李，提醒你日常的保养品宁滥勿缺，路途遥远要带够。",
    "options": [
        {
            "label": "A",
            "text": "嫌麻烦，说少带点没关系。",
            "scores": {"S10": 1, "S3": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认真清点，确保都带齐了。",
            "scores": {"S10": 3, "S3": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "抱住他说，师尊比我还在意我的身体。",
            "scores": {"S10": 5, "S3": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“吾看看，你要吃的药都带上了吗……路途遥远，日常的保养品宁滥勿缺。”——左慈在房中术中像家长一样操心广陵王的行李。"
})

questions.append({
    "id": "zuoci_daily_04",
    "type": "daily",
    "dimension": ["S2", "S8"],
    "source_character": "左慈",
    "text": "左慈说，你给不给我养老送终，我的遗产都是你的。",
    "options": [
        {
            "label": "A",
            "text": "尴尬地转移话题，说这些还早。",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认真说，我会给师尊养老送终的。",
            "scores": {"S2": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "笑着说，那师尊要活很久很久，让我继承好多好多遗产。",
            "scores": {"S2": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“你给不给吾养老送终，吾的遗产都是你的。”“等吾入道仙解的那日，你就把云帝宫当居丧的倚庐，不问世事住三年。”——左慈在房中术中谈论身后事，语气轻松却深情。"
})

questions.append({
    "id": "zuoci_daily_05",
    "type": "daily",
    "dimension": ["S3", "S6"],
    "source_character": "左慈",
    "text": "左慈叮嘱你，外面遇到麻烦不要硬扛，要及时跟他说。",
    "options": [
        {
            "label": "A",
            "text": "嘴上答应，心里还是想自己解决。",
            "scores": {"S3": 1, "S6": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "点头说知道了，有事会找师尊。",
            "scores": {"S3": 3, "S6": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "扑进他怀里说，那师尊要随时准备好帮我。",
            "scores": {"S3": 5, "S6": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“外面遇到麻烦不要硬扛，要及时跟吾说。”——左慈在房中术中展现师长般的保护欲。"
})

# 6. classic批次 (名场面还原)
questions.append({
    "id": "zuoci_classic_01",
    "type": "classic",
    "dimension": ["S4", "S9"],
    "source_character": "左慈",
    "text": "左慈被当街指控，他脱下法袍制药，展示天人羽衣。",
    "options": [
        {
            "label": "A",
            "text": "站在人群中静静观看，不介入。",
            "scores": {"S4": 1, "S9": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "出面为他辩护，证明他的清白。",
            "scores": {"S4": 3, "S9": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "走到他身边，当众宣布他是你的师尊，谁敢动他便是与你为敌。",
            "scores": {"S4": 5, "S9": 5},
            "tendency": "H"
        }
    ],
    "reveal": "古艳歌名场面：左慈被指控为妖道，他从容脱下法袍制药，展示天人羽衣，证明自己的仙家身份。"
})

questions.append({
    "id": "zuoci_classic_02",
    "type": "classic",
    "dimension": ["S8", "S2"],
    "source_character": "左慈",
    "text": "左慈带你去找复文箓，说十四岁时你离开他，现在又回到他身边。",
    "options": [
        {
            "label": "A",
            "text": "沉默不语，专注于找复文箓。",
            "scores": {"S8": 1, "S2": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "轻声说，我回来了，师尊。",
            "scores": {"S8": 3, "S2": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握住他的手说，这次不会再离开了。",
            "scores": {"S8": 5, "S2": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“十四岁时，你离开吾。”——乌飞名场面：左慈带广陵王寻找复文箓，感慨时光流逝与重逢。"
})

questions.append({
    "id": "zuoci_classic_03",
    "type": "classic",
    "dimension": ["S6", "S1"],
    "source_character": "左慈",
    "text": "左慈教你，除了他不要相信任何人，包括你最亲近的人。",
    "options": [
        {
            "label": "A",
            "text": "表示这太绝对了，我做不到。",
            "scores": {"S6": 1, "S1": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认真记下，但心里保留自己的判断。",
            "scores": {"S6": 3, "S1": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "看着他的眼睛说，那我只要相信师尊就够了。",
            "scores": {"S6": 5, "S1": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“除了吾，不要相信任何人。”——东郡太守名场面：左慈揭示里八华的存在，给广陵王最严厉也最关心的警告。"
})

questions.append({
    "id": "zuoci_classic_04",
    "type": "classic",
    "dimension": ["S9", "S10"],
    "source_character": "左慈",
    "text": "左慈说，梅树能活很久，比绝大多数人都久，只要活下去总有一天能恢复自由。",
    "options": [
        {
            "label": "A",
            "text": "感叹一句，然后转移话题。",
            "scores": {"S9": 1, "S10": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "理解他的隐喻，说我会耐心等待。",
            "scores": {"S9": 3, "S10": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说那师尊要像梅树一样，陪我很久很久。",
            "scores": {"S9": 5, "S10": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“梅树能活很久，比绝大多数人都久。只要活下去，总有一天能恢复自由。”——左慈用梅树比喻隐忍与希望。"
})

questions.append({
    "id": "zuoci_classic_05",
    "type": "classic",
    "dimension": ["S2", "S8"],
    "source_character": "左慈",
    "text": "左慈说，和你一起看的这片海，他会一直记得。",
    "options": [
        {
            "label": "A",
            "text": "笑笑说海有什么好记得的。",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "说我也记得，和师尊一起看的风景都很美。",
            "scores": {"S2": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "靠在他肩上说，那以后我们去看更多的海，让师尊永远记得。",
            "scores": {"S2": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "“和你一起看的这片海，吾会一直记得。”——左慈在古艳歌中表达与广陵王共度时光的珍贵记忆。"
})

# 写入JSON文件
output_path = "/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/zuoci.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"已生成 {len(questions)} 道题，保存至 {output_path}")