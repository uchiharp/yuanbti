import json

with open('questions/yuanji.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修正映射 (id, label) -> 新scores
fixes = {
    ('yuanji_sweet_02', 'C'): {'S2': 3, 'S8': 2},
    ('yuanji_sweet_04', 'B'): {'S5': 4, 'S8': 5},
    ('yuanji_sweet_04', 'C'): {'S5': 5, 'S8': 4},
    ('yuanji_funny_02', 'A'): {'S5': 1, 'S7': 3},
    ('yuanji_funny_03', 'C'): {'S3': 1, 'S4': 2},
    ('yuanji_angst_04', 'A'): {'S6': 5, 'S10': 4},
    ('yuanji_angst_04', 'B'): {'S6': 3, 'S10': 4},
    ('yuanji_angst_04', 'C'): {'S6': 1, 'S10': 2},
    ('yuanji_angst_05', 'B'): {'S2': 5, 'S8': 4},
    ('yuanji_angst_05', 'C'): {'S2': 1, 'S8': 2},
    ('yuanji_scheme_02', 'A'): {'S1': 1, 'S9': 2},
    ('yuanji_scheme_02', 'C'): {'S1': 5, 'S9': 4},
    ('yuanji_classic_05', 'B'): {'S2': 5, 'S6': 4},
}

for q in data:
    for opt in q['options']:
        key = (q['id'], opt['label'])
        if key in fixes:
            opt['scores'] = fixes[key]

# 验证所有选项是否差异化
errors = []
for q in data:
    for opt in q['options']:
        scores = list(opt['scores'].values())
        if len(scores) == 2 and scores[0] == scores[1]:
            errors.append((q['id'], opt['label'], scores))
if errors:
    print('仍有相同分数:', errors)
else:
    print('所有选项分数均已差异化。')

# 写回文件
with open('questions/yuanji.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('修正完成。')