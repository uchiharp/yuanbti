import json

with open('liubian.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修复函数
def fix_question(q):
    qid = q['id']
    dims = q['dimension']
    if len(dims) != 2:
        return False
    
    options = q['options']
    # 检查是否所有选项两个维度分值相同
    all_same = True
    for opt in options:
        scores = list(opt['scores'].values())
        if len(scores) == 2 and scores[0] != scores[1]:
            all_same = False
            break
    
    if not all_same:
        return False
    
    # 修复：让每个选项的两个维度分值不同
    # 模式：A:5-5, B:3-1, C:1-3 或类似
    dim1, dim2 = dims[0], dims[1]
    
    # 根据题目类型和内容决定如何调整
    # 简单方案：随机调整但保持逻辑
    # 这里采用固定模式：A保持高分，B调低第二个维度，C调低第一个维度
    for i, opt in enumerate(options):
        s1, s2 = opt['scores'][dim1], opt['scores'][dim2]
        if i == 0:  # A选项：通常是最积极的选择，保持高分
            pass  # 不变
        elif i == 1:  # B选项：降低第二个维度
            new_s2 = 1 if s2 == 5 else (1 if s2 == 3 else 1)
            opt['scores'][dim2] = new_s2
            # 更新reasoning
            opt['reasoning'] = opt['reasoning'].replace(f'{dim2}:{s2}', f'{dim2}:{new_s2}')
        elif i == 2:  # C选项：降低第一个维度
            new_s1 = 1 if s1 == 5 else (1 if s1 == 3 else 1)
            opt['scores'][dim1] = new_s1
            opt['reasoning'] = opt['reasoning'].replace(f'{dim1}:{s1}', f'{dim1}:{new_s1}')
    
    return True

# 应用修复
fixed_count = 0
for q in data:
    if fix_question(q):
        fixed_count += 1
        print(f'Fixed: {q[\"id\"]}')

print(f'Fixed {fixed_count} questions')

# 保存
with open('liubian_fixed2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved to liubian_fixed2.json')