#!/usr/bin/env python3
import json

questions = []

# ================== SWEET 批次 ==================
# 1
questions.append({
    "id": "liubian_sweet_1",
    "type": "sweet",
    "dimension": ["S2", "S8"],
    "source_character": "刘辩",
    "text": "劉辯突然湊近你，手指繞著自己的髮梢，問你喜歡直髮還是卷髮。",
    "options": [
        {
            "label": "A",
            "text": "笑著說「都喜歡」，伸手揉亂他的頭髮。",
            "scores": {"S2": 5, "S8": 3},
            "tendency": "H",
            "reasoning": "主動表達喜愛→S2:5，揉亂頭髮是親暱戲弄，不算特別溫柔→S8:3"
        },
        {
            "label": "B",
            "text": "認真端詳後說「直髮更適合你」。",
            "scores": {"S2": 3, "S8": 5},
            "tendency": "M",
            "reasoning": "認真回應表達中度情感→S2:3，體貼給出誠實意見→S8:5"
        },
        {
            "label": "C",
            "text": "反問「你喜歡哪種？」，把問題拋回去。",
            "scores": {"S2": 1, "S8": 3},
            "tendency": "L",
            "reasoning": "回避直接情感表達→S2:1，但沒有拒絕互動，保持禮貌→S8:3"
        }
    ],
    "reveal": "劉辯台詞：「我来问，广陵王是喜欢直发，还是喜欢卷发？」（夕情欢馀·刘辩/活动剧情）"
})

# 2
questions.append({
    "id": "liubian_sweet_2",
    "type": "sweet",
    "dimension": ["S2", "S5"],
    "source_character": "刘辩",
    "text": "劉辯抓起你的手貼在自己臉側，說他的頭髮比綢緞還順滑，讓你摸摸看。",
    "options": [
        {
            "label": "A",
            "text": "順勢撫摸他的頭髮，稱讚手感很好。",
            "scores": {"S2": 5, "S5": 3},
            "tendency": "H",
            "reasoning": "接受親密接觸，情感表達高→S2:5，行動上順從但被動→S5:3"
        },
        {
            "label": "B",
            "text": "抽回手，笑著說「別鬧了」。",
            "scores": {"S2": 3, "S5": 1},
            "tendency": "L",
            "reasoning": "溫和拒絕但保持友好→S2:3，行動上退縮→S5:1"
        },
        {
            "label": "C",
            "text": "反過來握住他的手，說「你的手更涼」。",
            "scores": {"S2": 3, "S5": 5},
            "tendency": "M",
            "reasoning": "主動轉移焦點，情感表達中等→S2:3，行動上主導互動→S5:5"
        }
    ],
    "reveal": "劉辯台詞：「我的头发也很好打理，你摸，肯定比绸缎还要顺滑。」（夕情欢馀·刘辩/活动剧情）"
})

# 3
questions.append({
    "id": "liubian_sweet_3",
    "type": "sweet",
    "dimension": ["S2", "S4"],
    "source_character": "刘辩",
    "text": "劉辯湊近你頸邊輕嗅，然後抬頭問你覺得他是什麼味道。",
    "options": [
        {
            "label": "A",
            "text": "說「降真香的煙火氣」。",
            "scores": {"S2": 3, "S4": 5},
            "tendency": "M",
            "reasoning": "給出客觀描述，情感表達中等→S2:3，回答帶有面具感（官方說法）→S4:5"
        },
        {
            "label": "B",
            "text": "笑著說「一股酒味」。",
            "scores": {"S2": 5, "S4": 1},
            "tendency": "H",
            "reasoning": "用玩笑表達親密，情感表達高→S2:5，直言不諱，無面具→S4:1"
        },
        {
            "label": "C",
            "text": "推開他，說「沒聞到」。",
            "scores": {"S2": 1, "S4": 3},
            "tendency": "L",
            "reasoning": "回避親密互動，情感表達低→S2:1，用藉口掩飾，有點面具→S4:3"
        }
    ],
    "reveal": "劉辯台詞：「你呢，觉得我是什么味道？」（夕情欢馀·刘辩/活动剧情）"
})

# 4
questions.append({
    "id": "liubian_sweet_4",
    "type": "sweet",
    "dimension": ["S2", "S8"],
    "source_character": "刘辩",
    "text": "劉辯突然抱住你，在你耳邊低聲說「我就知道，我的廣陵王肯定喜歡我」。",
    "options": [
        {
            "label": "A",
            "text": "回抱他，輕聲說「嗯」。",
            "scores": {"S2": 5, "S8": 5},
            "tendency": "H",
            "reasoning": "直接接受並回應情感→S2:5，動作溫柔體貼→S8:5"
        },
        {
            "label": "B",
            "text": "拍拍他的背，說「別鬧了」。",
            "scores": {"S2": 3, "S8": 3},
            "tendency": "M",
            "reasoning": "溫和回應但略帶距離→S2:3，動作友善但不算親密→S8:3"
        },
        {
            "label": "C",
            "text": "推開他，轉身就走。",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "L",
            "reasoning": "拒絕情感表達→S2:1，動作粗魯不溫柔→S8:1"
        }
    ],
    "reveal": "劉辯台詞：「我就知道，我的广陵王肯定喜欢我……」（夕情欢馀·刘辩/活动剧情）"
})

# 5
questions.append({
    "id": "liubian_sweet_5",
    "type": "sweet",
    "dimension": ["S2", "S9"],
    "source_character": "刘辩",
    "text": "劉辯捧著你的臉，認真地說「我的真愛可是無價之寶」。",
    "options": [
        {
            "label": "A",
            "text": "笑著說「那我也用無價之寶換」。",
            "scores": {"S2": 5, "S9": 3},
            "tendency": "H",
            "reasoning": "用同等浪漫回應，情感表達高→S2:5，但未挑戰他的權力主張→S9:3"
        },
        {
            "label": "B",
            "text": "握住他的手說「我收下了」。",
            "scores": {"S2": 3, "S9": 5},
            "tendency": "M",
            "reasoning": "接受但略被動，情感表達中等→S2:3，確認他對真愛的支配權→S9:5"
        },
        {
            "label": "C",
            "text": "移開視線，說「別說這種話」。",
            "scores": {"S2": 1, "S9": 1},
            "tendency": "L",
            "reasoning": "回避情感表達→S2:1，拒絕他的權力展示→S9:1"
        }
    ],
    "reveal": "劉辯台詞：「我的真爱可是无价之宝。」（夕情欢馀·刘辩/活动剧情）"
})

# ================== FUNNY 批次 ==================
# 6
questions.append({
    "id": "liubian_funny_1",
    "type": "funny",
    "dimension": ["S4", "S7"],
    "source_character": "刘辩",
    "text": "劉辯得意地說他創立了五斗咪道，問你要不要加入。",
    "options": [
        {
            "label": "A",
            "text": "一本正經地說「加入有什麼好處？」。",
            "scores": {"S4": 5, "S7": 3},
            "tendency": "M",
            "reasoning": "配合演出但帶現實考量，面具深→S4:5，鋒芒中等（提問）→S7:3"
        },
        {
            "label": "B",
            "text": "笑著說「你這是蹭張修的名望吧」。",
            "scores": {"S4": 1, "S7": 5},
            "tendency": "H",
            "reasoning": "直接戳破，無面具→S4:1，鋒芒高（調侃）→S7:5"
        },
        {
            "label": "C",
            "text": "搖頭說「別鬧了，正經點」。",
            "scores": {"S4": 3, "S7": 1},
            "tendency": "L",
            "reasoning": "略帶面具（不直接拒絕）→S4:3，鋒芒低（制止）→S7:1"
        }
    ],
    "reveal": "劉辯台詞：「加入五斗咪，什么都会有的。」（咪教模拟器/活动剧情）"
})

# 7
questions.append({
    "id": "liubian_funny_2",
    "type": "funny",
    "dimension": ["S3", "S7"],
    "source_character": "刘辩",
    "text": "劉辯說「真經上寫了，愛哭的男人最好命」，然後眼巴巴看著你。",
    "options": [
        {
            "label": "A",
            "text": "點頭說「對，你最好命」。",
            "scores": {"S3": 1, "S7": 3},
            "tendency": "L",
            "reasoning": "不務實（順著胡鬧）→S3:1，鋒芒中等（附和）→S7:3"
        },
        {
            "label": "B",
            "text": "笑著說「哪本真經？我看看」。",
            "scores": {"S3": 3, "S7": 5},
            "tendency": "M",
            "reasoning": "務實（要求證據）→S3:3，鋒芒高（挑戰）→S7:5"
        },
        {
            "label": "C",
            "text": "轉身就走，說「沒空聽你胡扯」。",
            "scores": {"S3": 5, "S7": 1},
            "tendency": "H",
            "reasoning": "極度務實（拒絕浪費時間）→S3:5，鋒芒低（回避）→S7:1"
        }
    ],
    "reveal": "劉辯台詞：「真经上写了，爱哭的男人最好命。」（夕情欢馀·刘辩/活动剧情）"
})

# 8
questions.append({
    "id": "liubian_funny_3",
    "type": "funny",
    "dimension": ["S5", "S8"],
    "source_character": "刘辩",
    "text": "劉辯衣服被口水弄濕，大喊「我要換衣服！黏糊糊的！！」。",
    "options": [
        {
            "label": "A",
            "text": "幫他找乾淨衣服，說「快換上」。",
            "scores": {"S5": 5, "S8": 5},
            "tendency": "H",
            "reasoning": "行動力高（直接幫忙）→S5:5，溫柔體貼→S8:5"
        },
        {
            "label": "B",
            "text": "笑著說「活該」。",
            "scores": {"S5": 1, "S8": 1},
            "tendency": "L",
            "reasoning": "無行動（嘲笑）→S5:1，不溫柔→S8:1"
        },
        {
            "label": "C",
            "text": "遞給他一塊布，說「自己擦擦」。",
            "scores": {"S5": 3, "S8": 3},
            "tendency": "M",
            "reasoning": "中度行動（提供工具）→S5:3，中度溫柔（有限幫助）→S8:3"
        }
    ],
    "reveal": "劉辯台詞：「我要换衣服！黏糊糊的！！」（咪教模拟器/活动剧情）"
})

# 9
questions.append({
    "id": "liubian_funny_4",
    "type": "funny",
    "dimension": ["S4", "S6"],
    "source_character": "刘辩",
    "text": "劉辯說「小酒坛子的存钱罐里捞出来的」，把錢給你。",
    "options": [
        {
            "label": "A",
            "text": "收下錢，說「謝謝小酒坛子」。",
            "scores": {"S4": 5, "S6": 3},
            "tendency": "M",
            "reasoning": "配合他的幽默，面具深→S4:5，底線中等（接受來路不明的錢）→S6:3"
        },
        {
            "label": "B",
            "text": "拒絕，說「你自己留著吧」。",
            "scores": {"S4": 3, "S6": 5},
            "tendency": "H",
            "reasoning": "略帶面具（不直接說奇怪）→S4:3，底線高（拒絕可疑錢財）→S6:5"
        },
        {
            "label": "C",
            "text": "問「你從哪騙來的？」",
            "scores": {"S4": 1, "S6": 1},
            "tendency": "L",
            "reasoning": "無面具（直接質問）→S4:1，底線低（不介意騙錢）→S6:1"
        }
    ],
    "reveal": "劉辯台詞：「小酒坛子的存钱罐里捞出来的。」（夕情欢馀·刘辩/活动剧情）"
})

# 10
questions.append({
    "id": "liubian_funny_5",
    "type": "funny",
    "dimension": ["S3", "S5"],
    "source_character": "刘辩",
    "text": "劉辯說「燒起來了！快幫我！」，道袍袖口著火。",
    "options": [
        {
            "label": "A",
            "text": "立刻用茶水潑滅火。",
            "scores": {"S3": 5, "S5": 5},
            "tendency": "H",
            "reasoning": "務實（有效滅火）→S3:5，行動力高（快速反應）→S5:5"
        },
        {
            "label": "B",
            "text": "趕忙幫他拍打火焰。",
            "scores": {"S3": 3, "S5": 3},
            "tendency": "M",
            "reasoning": "中度務實（方法較慢）→S3:3，行動力中等→S5:3"
        },
        {
            "label": "C",
            "text": "站著看，說「你自己弄的」。",
            "scores": {"S3": 1, "S5": 1},
            "tendency": "L",
            "reasoning": "不務實（不解決問題）→S3:1，行動力低→S5:1"
        }
    ],
    "reveal": "劉辯台詞：「烧起来了！快帮我！」（夕情欢馀·刘辩/活动剧情）"
})

# ================== ANGST 批次 ==================
# 11
questions.append({
    "id": "liubian_angst_1",
    "type": "angst",
    "dimension": ["S2", "S9"],
    "source_character": "刘辩",
    "text": "劉辯握著你的手，輕聲說「我一直想和你死在一起」。",
    "options": [
        {
            "label": "A",
            "text": "握緊他的手，說「好」。",
            "scores": {"S2": 5, "S9": 5},
            "tendency": "H",
            "reasoning": "情感表達高（接受死亡盟約）→S2:5，權力高（確認共同支配）→S9:5"
        },
        {
            "label": "B",
            "text": "抽回手，說「別說傻話」。",
            "scores": {"S2": 3, "S9": 3},
            "tendency": "M",
            "reasoning": "情感表達中等（拒絕但關心）→S2:3，權力中等（否定他的主張）→S9:3"
        },
        {
            "label": "C",
            "text": "轉身離開，不回應。",
            "scores": {"S2": 1, "S9": 1},
            "tendency": "L",
            "reasoning": "情感表達低（回避）→S2:1，權力低（不參與）→S9:1"
        }
    ],
    "reveal": "劉辯台詞：「我一直想和你死在一起。」（夕情欢馀·刘辩/活动剧情）"
})

# 12
questions.append({
    "id": "liubian_angst_2",
    "type": "angst",
    "dimension": ["S6", "S2"],
    "source_character": "刘辩",
    "text": "劉辯說「愛是什麼輕飄飄的東西。能實實在在握在手中的東西，只有一起去死」。",
    "options": [
        {
            "label": "A",
            "text": "抱住他，說「我就在這裡」。",
            "scores": {"S6": 5, "S2": 5},
            "tendency": "H",
            "reasoning": "底線高（拒絕死亡選擇，提供替代）→S6:5，情感表達高（給予安全感）→S2:5"
        },
        {
            "label": "B",
            "text": "沉默不語，握住他的手。",
            "scores": {"S6": 3, "S2": 3},
            "tendency": "M",
            "reasoning": "底線中等（不表態）→S6:3，情感表達中等（無言安慰）→S2:3"
        },
        {
            "label": "C",
            "text": "說「那你就去死吧」。",
            "scores": {"S6": 1, "S2": 1},
            "tendency": "L",
            "reasoning": "底線低（鼓勵死亡）→S6:1，情感表達低（殘忍）→S2:1"
        }
    ],
    "reveal": "劉辯台詞：「爱？爱是什么轻飘飘的东西。能实实在在握在手中的东西，只有一起去死。」（夕情欢馀·刘辩/活动剧情）"
})

# 13
questions.append({
    "id": "liubian_angst_3",
    "type": "angst",
    "dimension": ["S2", "S10"],
    "source_character": "刘辩",
    "text": "劉辯說「時間已經一點意義都沒有了」，眼神空洞。",
    "options": [
        {
            "label": "A",
            "text": "拉他去曬太陽，說「現在就有意義」。",
            "scores": {"S2": 5, "S10": 3},
            "tendency": "H",
            "reasoning": "情感表達高（積極介入）→S2:5，秩序中等（引入新規律）→S10:3"
        },
        {
            "label": "B",
            "text": "陪他坐著，不說話。",
            "scores": {"S2": 3, "S10": 1},
            "tendency": "M",
            "reasoning": "情感表達中等（陪伴）→S2:3，秩序低（不改變現狀）→S10:1"
        },
        {
            "label": "C",
            "text": "說「那你慢慢想」，離開。",
            "scores": {"S2": 1, "S10": 5},
            "tendency": "L",
            "reasoning": "情感表達低（回避）→S2:1，秩序高（維持原有節奏）→S10:5"
        }
    ],
    "reveal": "劉辯台詞：「时间已经一点意义都没有了。」（夕情欢馀·刘辩/活动剧情）"
})

# 14
questions.append({
    "id": "liubian_angst_4",
    "type": "angst",
    "dimension": ["S9", "S8"],
    "source_character": "刘辩",
    "text": "劉辯問「你想穿什麼衣服一起死？」",
    "options": [
        {
            "label": "A",
            "text": "說「隨便，你決定」。",
            "scores": {"S9": 5, "S8": 3},
            "tendency": "H",
            "reasoning": "權力高（讓他掌控）→S9:5，溫柔中等（順從）→S8:3"
        },
        {
            "label": "B",
            "text": "說「我才不想死」。",
            "scores": {"S9": 3, "S8": 1},
            "tendency": "M",
            "reasoning": "權力中等（拒絕他的規劃）→S9:3，溫柔低（直接拒絕）→S8:1"
        },
        {
            "label": "C",
            "text": "認真回答「那件紅色的」。",
            "scores": {"S9": 1, "S8": 5},
            "tendency": "L",
            "reasoning": "權力低（配合他的幻想）→S9:1，溫柔高（細心回應）→S8:5"
        }
    ],
    "reveal": "劉辯台詞：「我想问……我们一起死去之时，你想穿什么衣服？」（夕情欢馀·刘辩/活动剧情）"
})

# 15
questions.append({
    "id": "liubian_angst_5",
    "type": "angst",
    "dimension": ["S6", "S5"],
    "source_character": "刘辩",
    "text": "劉辯說「你為什麼不來……我恨你……」，聲音哽咽。",
    "options": [
        {
            "label": "A",
            "text": "抱住他，說「對不起」。",
            "scores": {"S6": 5, "S5": 5},
            "tendency": "H",
            "reasoning": "底線高（承擔責任）→S6:5，行動力高（主動安慰）→S5:5"
        },
        {
            "label": "B",
            "text": "站在原地，說「那時候我沒辦法」。",
            "scores": {"S6": 3, "S5": 3},
            "tendency": "M",
            "reasoning": "底線中等（解釋）→S6:3，行動力中等（不靠近）→S5:3"
        },
        {
            "label": "C",
            "text": "轉身離開。",
            "scores": {"S6": 1, "S5": 1},
            "tendency": "L",
            "reasoning": "底線低（逃避）→S6:1，行動力低（退縮）→S5:1"
        }
    ],
    "reveal": "劉辯台詞：「你為什麼不來……我恨你……」（咪教模拟器/活动剧情/普通线）"
})

# ================== SCHEME 批次 ==================
# 16
questions.append({
    "id": "liubian_scheme_1",
    "type": "scheme",
    "dimension": ["S1", "S6"],
    "source_character": "刘辩",
    "text": "劉辯提議趁張修不在，把鬼城據為己有，問你合作否。",
    "options": [
        {
            "label": "A",
            "text": "同意，說「需要我做什麼？」",
            "scores": {"S1": 5, "S6": 3},
            "tendency": "H",
            "reasoning": "權謀高（參與奪取）→S1:5，底線中等（不問道德）→S6:3"
        },
        {
            "label": "B",
            "text": "拒絕，說「這太冒險」。",
            "scores": {"S1": 3, "S6": 5},
            "tendency": "M",
            "reasoning": "權謀中等（考慮風險）→S1:3，底線高（謹慎）→S6:5"
        },
        {
            "label": "C",
            "text": "說「你自己決定」。",
            "scores": {"S1": 1, "S6": 1},
            "tendency": "L",
            "reasoning": "權謀低（不參與）→S1:1，底線低（不表態）→S6:1"
        }
    ],
    "reveal": "劉辯台詞：「趁着张修不在，让我们把此地据为己有吧！咪教，成……」（咪教模拟器/活动剧情）"
})

# 17
questions.append({
    "id": "liubian_scheme_2",
    "type": "scheme",
    "dimension": ["S9", "S10"],
    "source_character": "刘辩",
    "text": "劉辯說「我們五斗咪道全城放糧！只要依附於我，就能免於飢苦！」",
    "options": [
        {
            "label": "A",
            "text": "幫忙組織放糧，擴大影響。",
            "scores": {"S9": 5, "S10": 3},
            "tendency": "H",
            "reasoning": "權力高（協助掌控）→S9:5，秩序中等（建立新秩序）→S10:3"
        },
        {
            "label": "B",
            "text": "提醒他「小心被反噬」。",
            "scores": {"S9": 3, "S10": 5},
            "tendency": "M",
            "reasoning": "權力中等（警告）→S9:3，秩序高（注重穩定）→S10:5"
        },
        {
            "label": "C",
            "text": "說「隨你便」。",
            "scores": {"S9": 1, "S10": 1},
            "tendency": "L",
            "reasoning": "權力低（不關心）→S9:1，秩序低（無所謂）→S10:1"
        }
    ],
    "reveal": "劉辯台詞：「今天，我们五斗咪道全城放粮！张修已经不会回来了，但只要依附于我，就能免于饥苦！」（咪教模拟器/活动剧情/龙女线）"
})

# 18
questions.append({
    "id": "liubian_scheme_3",
    "type": "scheme",
    "dimension": ["S1", "S4"],
    "source_character": "刘辩",
    "text": "劉辯說「我們挑一個對象，把一切推到他身上，如何？」",
    "options": [
        {
            "label": "A",
            "text": "贊成，說「選誰？」",
            "scores": {"S1": 5, "S4": 5},
            "tendency": "H",
            "reasoning": "權謀高（參與算計）→S1:5，面具深（配合陰謀）→S4:5"
        },
        {
            "label": "B",
            "text": "猶豫，說「這樣好嗎？」",
            "scores": {"S1": 3, "S4": 3},
            "tendency": "M",
            "reasoning": "權謀中等（搖擺）→S1:3，面具中等（不直接拒絕）→S4:3"
        },
        {
            "label": "C",
            "text": "反對，說「不行」。",
            "scores": {"S1": 1, "S4": 1},
            "tendency": "L",
            "reasoning": "權謀低（拒絕算計）→S1:1，面具低（直接表態）→S4:1"
        }
    ],
    "reveal": "劉辯台詞：「我知道了……那，既然广陵王愿意联手，我也不介意冰释前嫌。这样，我们挑一个对象，把一切推到他身上，如何？」（咪教模拟器/活动剧情/龙女线）"
})

# 19
questions.append({
    "id": "liubian_scheme_4",
    "type": "scheme",
    "dimension": ["S6", "S9"],
    "source_character": "刘辩",
    "text": "劉辯抓到騙子，問你「你說，怎麼處置這個騙子？」",
    "options": [
        {
            "label": "A",
            "text": "說「交給官府」。",
            "scores": {"S6": 5, "S9": 3},
            "tendency": "H",
            "reasoning": "底線高（依法處理）→S6:5，權力中等（不自行處置）→S9:3"
        },
        {
            "label": "B",
            "text": "說「讓他賠錢，然後放走」。",
            "scores": {"S6": 3, "S9": 5},
            "tendency": "M",
            "reasoning": "底線中等（實用主義）→S6:3，權力高（決定處置）→S9:5"
        },
        {
            "label": "C",
            "text": "說「隨你處置」。",
            "scores": {"S6": 1, "S9": 1},
            "tendency": "L",
            "reasoning": "底線低（不關心）→S6:1，權力低（放棄決定）→S9:1"
        }
    ],
    "reveal": "劉辯台詞：「你说，怎么处置这个骗子？」（咪教模拟器/活动剧情）"
})

# 20
questions.append({
    "id": "liubian_scheme_5",
    "type": "scheme",
    "dimension": ["S1", "S3"],
    "source_character": "刘辩",
    "text": "劉辯說「廣陵王，我們隨身的錢不多了」，暗示需要籌錢。",
    "options": [
        {
            "label": "A",
            "text": "提議「去騙富戶」。",
            "scores": {"S1": 5, "S3": 1},
            "tendency": "H",
            "reasoning": "權謀高（不擇手段）→S1:5，務實低（非法手段）→S3:1"
        },
        {
            "label": "B",
            "text": "說「我還有積蓄，先拿去用」。",
            "scores": {"S1": 3, "S3": 5},
            "tendency": "M",
            "reasoning": "權謀中等（用現有資源）→S1:3，務實高（實際解決）→S3:5"
        },
        {
            "label": "C",
            "text": "說「省著點花」。",
            "scores": {"S1": 1, "S3": 3},
            "tendency": "L",
            "reasoning": "權謀低（消極）→S1:1，務實中等（節流）→S3:3"
        }
    ],
    "reveal": "劉辯台詞：「广陵王，我们随身的钱不多了。」（咪教模拟器/活动剧情/粮草线）"
})

# ================== DAILY 批次 ==================
# 21
questions.append({
    "id": "liubian_daily_1",
    "type": "daily",
    "dimension": ["S3", "S8"],
    "source_character": "刘辩",
    "text": "劉辯說「養他們這麼費錢，把他們全遣散，只留下小道嘛」。",
    "options": [
        {
            "label": "A",
            "text": "說「好，只留你」。",
            "scores": {"S3": 1, "S8": 5},
            "tendency": "H",
            "reasoning": "務實低（不考慮後果）→S3:1，溫柔高（順從他的任性）→S8:5"
        },
        {
            "label": "B",
            "text": "說「不行，他們都有用」。",
            "scores": {"S3": 5, "S8": 1},
            "tendency": "M",
            "reasoning": "務實高（理性決策）→S3:5，溫柔低（直接拒絕）→S8:1"
        },
        {
            "label": "C",
            "text": "說「別鬧了，想想辦法」。",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "L",
            "reasoning": "務實中等（折衷）→S3:3，溫柔中等（安撫）→S8:3"
        }
    ],
    "reveal": "劉辯台詞：「养他们这么费钱，把他们全遣散，只留下小道嘛。」（夕情欢馀·刘辩/活动剧情）"
})

# 22
questions.append({
    "id": "liubian_daily_2",
    "type": "daily",
    "dimension": ["S5", "S10"],
    "source_character": "刘辩",
    "text": "劉辯喝酒後對著心紙君說話，被你撞見。",
    "options": [
        {
            "label": "A",
            "text": "走過去陪他一起喝。",
            "scores": {"S5": 5, "S10": 1},
            "tendency": "H",
            "reasoning": "行動力高（加入）→S5:5，秩序低（打破常規）→S10:1"
        },
        {
            "label": "B",
            "text": "悄悄離開，不打擾。",
            "scores": {"S5": 1, "S10": 5},
            "tendency": "M",
            "reasoning": "行動力低（不干預）→S5:1，秩序高（維持現狀）→S10:5"
        },
        {
            "label": "C",
            "text": "出聲叫他，問「在幹嘛？」",
            "scores": {"S5": 3, "S10": 3},
            "tendency": "L",
            "reasoning": "行動力中等（介入）→S5:3，秩序中等（打破安靜）→S10:3"
        }
    ],
    "reveal": "劉辯台詞：「喝酒呀，一个人去蒹葭滩上、雪地里、地宫里……一直对着你的心纸君说话，直到你回覆我。」（夕情欢馀·刘辩/活动剧情）"
})

# 23
questions.append({
    "id": "liubian_daily_3",
    "type": "daily",
    "dimension": ["S2", "S3"],
    "source_character": "刘辩",
    "text": "劉辯問「你的錢一般都花去哪了？」",
    "options": [
        {
            "label": "A",
            "text": "認真列出開支。",
            "scores": {"S2": 3, "S3": 5},
            "tendency": "H",
            "reasoning": "情感表達中等（分享）→S2:3，務實高（詳細）→S3:5"
        },
        {
            "label": "B",
            "text": "說「養你了」。",
            "scores": {"S2": 5, "S3": 1},
            "tendency": "M",
            "reasoning": "情感表達高（甜蜜）→S2:5，務實低（玩笑）→S3:1"
        },
        {
            "label": "C",
            "text": "說「不關你事」。",
            "scores": {"S2": 1, "S3": 3},
            "tendency": "L",
            "reasoning": "情感表達低（拒絕）→S2:1，務實中等（隱瞞）→S3:3"
        }
    ],
    "reveal": "劉辯台詞：「换、换我问！你的钱一般都花去哪了？」（夕情欢馀·刘辩/活动剧情）"
})

# 24
questions.append({
    "id": "liubian_daily_4",
    "type": "daily",
    "dimension": ["S8", "S9"],
    "source_character": "刘辩",
    "text": "劉辯說「我們一家三口齊齊整整」，指你、他和小酒坛子。",
    "options": [
        {
            "label": "A",
            "text": "笑著說「對，一家三口」。",
            "scores": {"S8": 5, "S9": 5},
            "tendency": "H",
            "reasoning": "溫柔高（接納）→S8:5，權力高（確認家庭權力結構）→S9:5"
        },
        {
            "label": "B",
            "text": "說「誰跟你一家」。",
            "scores": {"S8": 1, "S9": 1},
            "tendency": "M",
            "reasoning": "溫柔低（拒絕）→S8:1，權力低（否認關係）→S9:1"
        },
        {
            "label": "C",
            "text": "轉移話題，說「小酒坛子餓了」。",
            "scores": {"S8": 3, "S9": 3},
            "tendency": "L",
            "reasoning": "溫柔中等（不直接拒絕）→S8:3，權力中等（避開主張）→S9:3"
        }
    ],
    "reveal": "劉辯台詞：「让小酒坛子封穴前跳进来，小酒坛子变成小土坛子，我们一家三口齐齐整整。」（夕情欢馀·刘辩/活动剧情）"
})

# 25
questions.append({
    "id": "liubian_daily_5",
    "type": "daily",
    "dimension": ["S4", "S7"],
    "source_character": "刘辩",
    "text": "劉辯說「上班哪有那麼恐怖，好像天都要塌了似的。沒有班上才恐怖吧？」",
    "options": [
        {
            "label": "A",
            "text": "點頭說「你說得對」。",
            "scores": {"S4": 5, "S7": 1},
            "tendency": "H",
            "reasoning": "面具深（附和）→S4:5，鋒芒低（不爭辯）→S7:1"
        },
        {
            "label": "B",
            "text": "反駁「你沒上過班才這麼說」。",
            "scores": {"S4": 1, "S7": 5},
            "tendency": "M",
            "reasoning": "面具低（直接反對）→S4:1，鋒芒高（挑戰）→S7:5"
        },
        {
            "label": "C",
            "text": "苦笑不語。",
            "scores": {"S4": 3, "S7": 3},
            "tendency": "L",
            "reasoning": "面具中等（不表態）→S4:3，鋒芒中等（無聲抗議）→S7:3"
        }
    ],
    "reveal": "劉辯台詞：「上班哪有那么恐怖，好像天都要塌了似的。没有班上才恐怖吧？」（夕情欢馀·刘辩/活动剧情）"
})

# ================== CLASSIC 批次 ==================
# 26
questions.append({
    "id": "liubian_classic_1",
    "type": "classic",
    "dimension": ["S6", "S10"],
    "source_character": "刘辩",
    "text": "劉辯在隱鳶閣把渾儀推亂，所有人都觀不到星，他問你怎麼辦。",
    "options": [
        {
            "label": "A",
            "text": "說「我去修」。",
            "scores": {"S6": 5, "S10": 5},
            "tendency": "H",
            "reasoning": "底線高（承擔責任）→S6:5，秩序高（恢復秩序）→S10:5"
        },
        {
            "label": "B",
            "text": "說「你怎麼這麼調皮」。",
            "scores": {"S6": 3, "S10": 3},
            "tendency": "M",
            "reasoning": "底線中等（指責但溫和）→S6:3，秩序中等（不緊急）→S10:3"
        },
        {
            "label": "C",
            "text": "說「不管了」。",
            "scores": {"S6": 1, "S10": 1},
            "tendency": "L",
            "reasoning": "底線低（逃避）→S6:1，秩序低（放任混亂）→S10:1"
        }
    ],
    "reveal": "劉辯台詞：「呃……好早以前，我把隐鸢阁观星台浑仪推乱了，所有人都观不到橙星。」（夕情欢馀·刘辩/活动剧情）"
})

# 27
questions.append({
    "id": "liubian_classic_2",
    "type": "classic",
    "dimension": ["S2", "S5"],
    "source_character": "刘辩",
    "text": "劉辯在畫廊裡說「你說謊了，回廊一直延伸不讓我們出去」。",
    "options": [
        {
            "label": "A",
            "text": "承認「我說謊了」。",
            "scores": {"S2": 5, "S5": 5},
            "tendency": "H",
            "reasoning": "情感表達高（誠實）→S2:5，行動力高（直面問題）→S5:5"
        },
        {
            "label": "B",
            "text": "堅持「我沒說謊」。",
            "scores": {"S2": 1, "S5": 3},
            "tendency": "M",
            "reasoning": "情感表達低（隱瞞）→S2:1，行動力中等（堅持）→S5:3"
        },
        {
            "label": "C",
            "text": "轉移話題「我們找出口」。",
            "scores": {"S2": 3, "S5": 1},
            "tendency": "L",
            "reasoning": "情感表達中等（回避）→S2:3，行動力低（逃避）→S5:1"
        }
    ],
    "reveal": "劉辯台詞：「你看，画里的回廊一直延伸，不让我们出去，说明你说谎了。」（夕情欢馀·刘辩/活动剧情）"
})

# 28
questions.append({
    "id": "liubian_classic_3",
    "type": "classic",
    "dimension": ["S1", "S9"],
    "source_character": "刘辩",
    "text": "劉辯在咪教模擬器中傳道，問你覺得他的教義如何。",
    "options": [
        {
            "label": "A",
            "text": "稱讚「很有吸引力」。",
            "scores": {"S1": 5, "S9": 5},
            "tendency": "H",
            "reasoning": "權謀高（支持他的影響力）→S1:5，權力高（認可他的領導）→S9:5"
        },
        {
            "label": "B",
            "text": "說「還需要改進」。",
            "scores": {"S1": 3, "S9": 3},
            "tendency": "M",
            "reasoning": "權謀中等（保留意見）→S1:3，權力中等（有限認可）→S9:3"
        },
        {
            "label": "C",
            "text": "說「不怎麼樣」。",
            "scores": {"S1": 1, "S9": 1},
            "tendency": "L",
            "reasoning": "權謀低（否定）→S1:1，權力低（打擊）→S9:1"
        }
    ],
    "reveal": "劉辯台詞：「不要小看我的魅力，我往这一坐，立刻就有人前仆后继来投。」（咪教模拟器/活动剧情）"
})

# 29
questions.append({
    "id": "liubian_classic_4",
    "type": "classic",
    "dimension": ["S3", "S8"],
    "source_character": "刘辩",
    "text": "劉辯說「我為你流下的都是真情實感的眼淚」。",
    "options": [
        {
            "label": "A",
            "text": "幫他擦淚，說「我知道」。",
            "scores": {"S3": 5, "S8": 5},
            "tendency": "H",
            "reasoning": "務實高（實際行動）→S3:5，溫柔高（體貼）→S8:5"
        },
        {
            "label": "B",
            "text": "說「別哭了」。",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M",
            "reasoning": "務實中等（制止）→S3:3，溫柔中等（安慰）→S8:3"
        },
        {
            "label": "C",
            "text": "不理會。",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "L",
            "reasoning": "務實低（不處理）→S3:1，溫柔低（冷漠）→S8:1"
        }
    ],
    "reveal": "劉辯台詞：「我为你流下的都是真情实感的眼泪。」（夕情欢馀·刘辩/活动剧情）"
})

# 30
questions.append({
    "id": "liubian_classic_5",
    "type": "classic",
    "dimension": ["S4", "S6"],
    "source_character": "刘辩",
    "text": "劉辯說「我雖然對錢沒什麼感覺，但也覺得這個數有點過分了。廣陵王，要信他嗎？」",
    "options": [
        {
            "label": "A",
            "text": "說「不信，我們走」。",
            "scores": {"S4": 1, "S6": 5},
            "tendency": "H",
            "reasoning": "面具低（直接判斷）→S4:1，底線高（謹慎）→S6:5"
        },
        {
            "label": "B",
            "text": "說「再觀察一下」。",
            "scores": {"S4": 5, "S6": 3},
            "tendency": "M",
            "reasoning": "面具深（不露態度）→S4:5，底線中等（不立即決定）→S6:3"
        },
        {
            "label": "C",
            "text": "說「信吧，反正沒損失」。",
            "scores": {"S4": 3, "S6": 1},
            "tendency": "L",
            "reasoning": "面具中等（隨意）→S4:3，底線低（輕信）→S6:1"
        }
    ],
    "reveal": "劉辯台詞：「……我虽然对钱没什么感觉，但也觉得这个数有点过分了。广陵王，要信他吗？」（咪教模拟器/活动剧情）"
})

# 輸出
with open('liubian.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f'Generated {len(questions)} questions.')