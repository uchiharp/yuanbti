#!/usr/bin/env python3
import json

# 读取现有题目
with open('liubian.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f'Currently have {len(questions)} questions')

# 第4题 (sweet)
q4 = {
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
}

# 第5题 (sweet)
q5 = {
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
}

questions.append(q4)
questions.append(q5)

print(f'Added 2 sweet questions, now {len(questions)} total')

# 保存
with open('liubian.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print('Saved')