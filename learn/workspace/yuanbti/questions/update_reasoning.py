#!/usr/bin/env python3
import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_reasoning(opt_text, scores, dimensions):
    """生成符合示例格式的reasoning"""
    dim_map = {
        'S1': ('权谋', '权谋水平'),
        'S2': ('情感', '情感表达'),
        'S3': ('务实', '务实程度'),
        'S4': ('面具', '面具深度'),
        'S5': ('行动', '行动力'),
        'S6': ('底线', '底线坚持'),
        'S7': ('锋芒', '锋芒显露'),
        'S8': ('温柔', '温柔程度'),
        'S9': ('权力', '权力倾向'),
        'S10': ('秩序', '秩序遵循')
    }
    parts = []
    for d in dimensions:
        val = scores[d]
        name, desc = dim_map.get(d, (d, d))
        if val == 1:
            level = '低'
            expl = '少'
        elif val == 3:
            level = '中'
            expl = '中等'
        else:
            level = '高'
            expl = '多'
        # 根据选项文本前几个字判断行为
        action = opt_text[:8]
        if '婉拒' in opt_text or '拒绝' in opt_text:
            action_desc = '婉拒回避'
        elif '主动' in opt_text or '握住' in opt_text:
            action_desc = '主动回应'
        elif '提议' in opt_text or '建议' in opt_text:
            action_desc = '提议'
        elif '严肃' in opt_text or '批评' in opt_text:
            action_desc = '严肃对待'
        elif '笑' in opt_text or '玩笑' in opt_text:
            action_desc = '玩笑回应'
        elif '安慰' in opt_text or '关心' in opt_text:
            action_desc = '关心安慰'
        else:
            action_desc = '选择'
        
        if d == 'S2':
            if val == 1:
                reason = f'{action_desc}情感互动→{d}:{val}'
            elif val == 3:
                reason = f'{action_desc}情感表达中等→{d}:{val}'
            else:
                reason = f'{action_desc}情感表达充分→{d}:{val}'
        elif d == 'S8':
            if val == 1:
                reason = f'保持距离不算温柔→{d}:{val}'
            elif val == 3:
                reason = f'适度温柔→{d}:{val}'
            else:
                reason = f'温柔体贴→{d}:{val}'
        elif d == 'S4':
            if val == 1:
                reason = f'直率无面具→{d}:{val}'
            elif val == 3:
                reason = f'适度掩饰→{d}:{val}'
            else:
                reason = f'戴面具深→{d}:{val}'
        elif d == 'S7':
            if val == 1:
                reason = f'收敛锋芒→{d}:{val}'
            elif val == 3:
                reason = f'适度锋芒→{d}:{val}'
            else:
                reason = f'锋芒毕露→{d}:{val}'
        else:
            reason = f'{desc}{level}→{d}:{val}'
        parts.append(reason)
    return '，'.join(parts)

def main():
    input_path = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji.json'
    output_path = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji_final_v2.json'
    
    data = load_json(input_path)
    
    for q in data:
        dims = q['dimension']
        for opt in q['options']:
            scores = opt['scores']
            # 确保分数是1/3/5
            for d in dims:
                val = scores[d]
                if val not in [1, 3, 5]:
                    if val <= 2:
                        scores[d] = 1
                    elif val <= 4:
                        scores[d] = 3
                    else:
                        scores[d] = 5
            # 更新reasoning
            opt['reasoning'] = generate_reasoning(opt['text'], scores, dims)
    
    save_json(data, output_path)
    print(f'已更新reasoning并保存到 {output_path}')
    
    # 复制到主文件
    import shutil
    shutil.copy2(output_path, input_path)
    print(f'已复制到 {input_path}')
    
    # 验证
    missing = 0
    for q in data:
        for opt in q['options']:
            if 'reasoning' not in opt:
                missing += 1
    print(f'缺少reasoning的选项: {missing}')

if __name__ == '__main__':
    main()