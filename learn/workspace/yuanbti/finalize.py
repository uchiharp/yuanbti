import json
import copy

with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/liubian.json', 'r', encoding='utf-8') as f:
    old = json.load(f)

# Define new batch assignment (indices 0-29)
new_types = [
    'classic',   # 0 死在一起 (名场面)
    'scheme',    # 1 徐州会议
    'funny',     # 2 别抖我钱
    'funny',     # 3 装天师算命
    'angst',     # 4 爱轻飘飘
    'scheme',    # 5 红蜡百姓
    'classic',   # 6 徐州拍案 (名场面)
    'sweet',     # 7 存钱罐
    'classic',   # 8 涪陵城下架子 (名场面)
    'scheme',    # 9 完美天下
    'sweet',     # 10 骗了十几年
    'scheme',    # 11 益州打赌
    'daily',     # 12 便宜首饰 (日常)
    'sweet',     # 13 规行矩步
    'angst',     # 14 我恨你
    'scheme',    # 15 地宫质问
    'daily',     # 16 牵牛花虫子
    'classic',   # 17 后将军狂喜 (名场面)
    'angst',     # 18 不在意你喜欢我
    'angst',     # 19 也许我死了更好
    'sweet',     # 20 我病了听不见
    'classic',   # 21 火烧芍药院
    'scheme',    # 22 陶谦拥立
    'daily',     # 23 管他天崩地裂 (日常温馨?)
    'daily',     # 24 七夕鱼刺 (日常)
    'angst',     # 25 疯子藏兰花
    'funny',     # 26 淡季不景气
    'daily',     # 27 你起初每天进宫 (日常)
    'scheme',    # 28 那种东西想要多少有多少
    'sweet',     # 29 欲取欲求
]

# Verify each batch has 5
from collections import Counter
print('Batch counts:', Counter(new_types))

# Fix functions
def fix_dimension(dim):
    if isinstance(dim, str):
        return [dim]
    return dim

def fix_option_text(text):
    # Remove leading '你' if it's the first character (after optional punctuation)
    # Keep the punctuation
    if text.startswith('「'):
        # Handle Chinese quotation
        if len(text) > 1 and text[1] == '你':
            return '「' + text[2:]
    if text.startswith('“'):
        if len(text) > 1 and text[1] == '你':
            return '“' + text[2:]
    # If starts with '你' directly
    if text.startswith('你'):
        return text[1:]
    return text

def fix_sexual_innuendo(text):
    # Replace explicit phrases
    replacements = {
        '拆吃入腹': '好好珍惜',
        '吃我': '陪着我',
        '床': '身边',
        '吻': '拥抱',
        '亲': '靠近',
        '按在墙上': '轻轻拉住',
        '拽过来': '拉过来',
        '堵住他的嘴': '轻轻按住他的唇',
        '尝一口': '感受一下',
        '检查每一寸': '仔细看看',
        '试试到底好不好养': '看看是不是真的好养',
        '把我变得只属于你': '让我只属于你',
        '做点别的事': '单独待一会儿',
        '演示一下什么叫真正的不择手段': '让你看看什么叫不择手段',
        '生不如死': '难忘的回忆',
        '火中鸳鸯': '火中相伴',
    }
    for k, v in replacements.items():
        if k in text:
            text = text.replace(k, v)
    return text

new_questions = []
for idx, q in enumerate(old):
    new = copy.deepcopy(q)
    # Assign type
    new['type'] = new_types[idx]
    # Fix dimension
    new['dimension'] = fix_dimension(new['dimension'])
    # Fix options
    for opt in new['options']:
        opt['text'] = fix_option_text(opt['text'])
        # Fix sexual innuendo only for C options (since they tend to be bolder)
        if opt['label'] == 'C':
            opt['text'] = fix_sexual_innuendo(opt['text'])
        # Ensure tendency is L/M/H (already)
    new_questions.append(new)

# Write final file
output_path = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/liubian_final.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(new_questions, f, ensure_ascii=False, indent=2)

print(f'Written {len(new_questions)} questions to {output_path}')
print('Batch distribution:')
for batch in ['sweet','funny','angst','scheme','daily','classic']:
    count = sum(1 for q in new_questions if q['type'] == batch)
    print(f'  {batch}: {count}')