#!/usr/bin/env python3
import json, os, sys

def check_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    name = os.path.basename(filepath).replace('.json', '')
    total = len(data)
    
    # 统计题型
    type_counts = {}
    dimension_counts = {}
    
    for q in data:
        t = q['type']
        d = q['dimension']
        type_counts[t] = type_counts.get(t, 0) + 1
        if d:
            dimension_counts[d] = dimension_counts.get(d, 0) + 1
    
    # 剧情题统计
    story_total = type_counts.get('story_known', 0) + type_counts.get('story_anon', 0)
    story_known_pct = type_counts.get('story_known', 0) / story_total if story_total > 0 else 0
    story_anon_pct = type_counts.get('story_anon', 0) / story_total if story_total > 0 else 0
    
    return {
        'name': name,
        'total': total,
        'types': type_counts,
        'dimensions': dimension_counts,
        'story_total': story_total,
        'story_known_pct': story_known_pct,
        'story_anon_pct': story_anon_pct
    }

if __name__ == '__main__':
    target_files = [
        'zhangmiao', 'achan', 'xushu', 'chendeng', 'guojia',
        'zhouyu', 'miheng', 'xixue', 'zhangliao', 'dongfeng', 'wangyi'
    ]
    
    base_dir = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions'
    
    print("角色题目统计:")
    print("-" * 80)
    for name in target_files:
        filepath = os.path.join(base_dir, f'{name}.json')
        if not os.path.exists(filepath):
            print(f"{name}: 文件不存在")
            continue
            
        stats = check_questions(filepath)
        
        # 检查是否符合要求
        ok_20_25 = 20 <= stats['total'] <= 25
        ok_story_pct = stats['story_total'] / stats['total'] >= 0.55  # 剧情题至少55%
        ok_story_known_pct = stats['story_known_pct'] >= 0.55 if stats['story_total'] > 0 else True  # 已知剧情至少55%
        
        status = []
        if ok_20_25:
            status.append("数量✓")
        else:
            status.append(f"数量{stats['total']}")
        
        if ok_story_pct:
            status.append("剧情比例✓")
        else:
            status.append(f"剧情{stats['story_total']}/{stats['total']}")
            
        if ok_story_known_pct:
            status.append("已知剧情✓")
        else:
            status.append(f"已知{stats['types'].get('story_known',0)}/{stats['story_total']}")
        
        print(f"{stats['name']:10} {stats['total']:2}题 | "
              f"类型: {dict(stats['types'])} | "
              f"状态: {' '.join(status)}")