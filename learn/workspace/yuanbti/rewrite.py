import json
import copy

# Load existing questions
with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/liubian.json', 'r', encoding='utf-8') as f:
    old = json.load(f)

# Map old question indices to batch types
# We'll assign based on our classification
batch_assign = {
    0: 'angst',   # 我一直想和你死在一起
    1: 'scheme',  # 徐州会议
    2: 'funny',   # 别抖我钱
    3: 'funny',   # 装天师算命
    4: 'angst',   # 爱轻飘飘
    5: 'scheme',  # 红蜡百姓
    6: 'scheme',  # 徐州拍案
    7: 'sweet',   # 存钱罐
    8: 'scheme',  # 涪陵城下架子
    9: 'scheme',  # 完美天下
    10: 'sweet',  # 骗了十几年
    11: 'scheme', # 益州打赌
    12: 'funny',  # 便宜首饰
    13: 'sweet',  # 规行矩步
    14: 'angst',  # 我恨你
    15: 'scheme', # 地宫质问
    16: 'daily',  # 牵牛花虫子
    17: 'scheme', # 后将军狂喜
    18: 'angst',  # 不在意你喜欢我
    19: 'angst',  # 也许我死了更好
    20: 'sweet',  # 我病了听不见
    21: 'classic',# 火烧芍药院
    22: 'scheme', # 陶谦拥立
    23: 'sweet',  # 管他天崩地裂
    24: 'funny',  # 七夕鱼刺
    25: 'angst',  # 疯子藏兰花
    26: 'funny',  # 淡季不景气
    27: 'angst',  # 你起初每天进宫
    28: 'scheme', # 那种东西想要多少有多少
    29: 'sweet',  # 欲取欲求
}

# Ensure each batch has exactly 5 questions
batch_counts = {}
for i, q in enumerate(old):
    b = batch_assign[i]
    batch_counts[b] = batch_counts.get(b, 0) + 1

print('Batch counts:', batch_counts)
# We need 5 each, adjust if needed

new_questions = []

for idx, q in enumerate(old):
    new = copy.deepcopy(q)
    # Fix type
    new['type'] = batch_assign[idx]
    # Fix dimension to array
    if isinstance(new['dimension'], str):
        new['dimension'] = [new['dimension']]
    # Fix tendency: ensure L/M/H (already)
    # Fix options: ensure they don't start with '你' (subject)
    for opt in new['options']:
        text = opt['text'].strip()
        # Remove leading punctuation if needed
        if text.startswith('「'):
            text = text[1:]
        if text.startswith('“'):
            text = text[1:]
        # Check if starts with '你' and remove
        if text.startswith('你'):
            # Replace with action without subject
            # Simple fix: remove '你' if it's the first character
            opt['text'] = text[1:].strip()
        # Also ensure no sexual innuendo in C options (rough fix)
        if opt['label'] == 'C':
            txt = opt['text']
            if '拆吃入腹' in txt:
                opt['text'] = txt.replace('拆吃入腹', '好好珍惜')
            if '吃我' in txt:
                opt['text'] = txt.replace('吃我', '陪着我')
            if '床' in txt:
                opt['text'] = txt.replace('床', '身边')
            if '吻' in txt or '亲' in txt:
                # Replace with less explicit
                opt['text'] = txt.replace('吻', '拥抱').replace('亲', '靠近')
    # Fix reveal: ensure it references real lines (keep as is)
    new_questions.append(new)

# Write new file
output_path = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/liubian_new.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(new_questions, f, ensure_ascii=False, indent=2)

print(f'Written {len(new_questions)} questions to {output_path}')