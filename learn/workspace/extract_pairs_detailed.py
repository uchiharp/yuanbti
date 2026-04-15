#!/usr/bin/env python3
import json
import sys
from collections import defaultdict

# Skip NPCs
NPC_SET = {'众人','侍从','侍卫','流民','百姓','平民','村民','难民','士兵','宦官','宫女','路人','门卫','群臣','旁白','（',''}
def is_npc(name):
    if name in NPC_SET:
        return True
    if name.endswith('甲') or name.endswith('乙') or name.endswith('丙') or name.endswith('丁'):
        return True
    if name.startswith('山贼') or name.startswith('士兵') or name.startswith('百姓') or name.startswith('村民'):
        return True
    if name.startswith('流民') or name.startswith('宫女') or name.startswith('宦官') or name.startswith('群臣'):
        return True
    if name.startswith('路人') or name.startswith('门卫'):
        return True
    return False

def process_line(line):
    parts = line.strip().split('|', 2)
    if len(parts) < 3:
        return None
    title, category, content_str = parts
    try:
        content = json.loads(content_str)
    except json.JSONDecodeError:
        return None
    
    speakers = set()
    for d in content:
        speaker = d.get('speaker', '').strip()
        if speaker and not is_npc(speaker):
            speakers.add(speaker)
    return title, category, list(speakers)

def main():
    pair_info = defaultdict(lambda: {
        'char_a': '',
        'char_b': '',
        'chapters': [],
        'categories': set(),
        'dialogue_count': 0
    })
    
    line_count = 0
    with open('/tmp/all_stories.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line_count += 1
            if line_count % 500 == 0:
                print(f'Processed {line_count} lines...', file=sys.stderr)
            
            result = process_line(line)
            if not result:
                continue
            title, category, speakers = result
            speakers.sort()
            
            # Add all pairs
            for i in range(len(speakers)):
                for j in range(i+1, len(speakers)):
                    a, b = speakers[i], speakers[j]
                    key = f'{a}|||{b}'
                    info = pair_info[key]
                    if not info['char_a']:
                        info['char_a'] = a
                        info['char_b'] = b
                    info['chapters'].append(title)
                    info['categories'].add(category)
                    info['dialogue_count'] += 1
    
    # Convert to list
    pairs = []
    for key, info in pair_info.items():
        pairs.append({
            'char_a': info['char_a'],
            'char_b': info['char_b'],
            'chapters': info['chapters'],
            'chapter_count': len(info['chapters']),
            'categories': list(info['categories']),
            'dialogue_count': info['dialogue_count']
        })
    
    # Sort by chapter_count descending
    pairs.sort(key=lambda x: x['chapter_count'], reverse=True)
    
    print(f'Total pairs: {len(pairs)}', file=sys.stderr)
    
    # Save
    with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/dhyy_all_pairs_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    
    # Print stats
    thresholds = [1, 2, 3, 5, 10, 20]
    for t in thresholds:
        count = sum(1 for p in pairs if p['chapter_count'] >= t)
        print(f'Pairs with ≥{t} chapters: {count}', file=sys.stderr)
    
    # Top 20
    print('\nTop 20 pairs:', file=sys.stderr)
    for p in pairs[:20]:
        print(f"  {p['char_a']} ↔ {p['char_b']}: {p['chapter_count']}章, {p['dialogue_count']}对话", file=sys.stderr)

if __name__ == '__main__':
    main()