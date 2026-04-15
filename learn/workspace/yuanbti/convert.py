import re, json

with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/character-centroids.md') as f:
    text = f.read()

lines = text.split('\n')

# Find character names and their data rows
char_data = {}
current_name = None

def parse_val(s):
    m = re.match(r'([LMH])\((\d)\)', s.strip())
    if m:
        return int(m.group(2))
    return None

for i, line in enumerate(lines):
    # Detect character name from ## headers
    if line.startswith('## '):
        name = line[3:].strip()
        if name in ('总结', '注意事项'):
            current_name = None
            continue
        current_name = name
        continue
    
    # Detect data rows (start with | and contain L/M/H patterns)
    if current_name and line.startswith('|') and re.search(r'[LMH]\(\d\)', line):
        # Skip header rows
        if 'S1' in line and '权谋' in line:
            continue
        if '---' in line:
            continue
        
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) != 12:
            continue
        
        vals = [parse_val(c) for c in cells]
        if any(v is None for v in vals):
            continue
        
        # Check if this character was already added (some have multiple tables)
        if current_name not in char_data:
            char_data[current_name] = vals

# Skip characters without valid data (pets etc)
skip = {'绣球', '飞云', '黄盖'}

def to7(v):
    return v + 1

result_md = "# 鸢BTI 角色质心 v2（10维7级）\n\n"
result_json = {}

dim_keys = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10']

for name, old in char_data.items():
    if name in skip:
        continue
    
    # S1-S7: old[0..6], S8=old[9](温柔), S9=old[10](权力), S10=old[11](秩序)
    new_vals = [to7(old[i]) for i in range(7)] + [to7(old[9]), to7(old[10]), to7(old[11])]
    
    # Special overrides
    if name == '张邈':
        new_vals[8] = 2  # S9权力 M→L
    elif name == '孙策':
        new_vals[8] = 3  # S9权力 H→M
        new_vals[9] = 3  # S10秩序 L→M
    
    result_json[name] = {dim_keys[i]: new_vals[i] for i in range(10)}
    
    lmh = []
    for v in new_vals:
        if v < 2.5: lmh.append('L')
        elif v <= 3.5: lmh.append('M')
        else: lmh.append('H')
    
    result_md += f"## {name}\n"
    result_md += "| S1权谋 | S2情感 | S3金钱 | S4面具 | S5行动 | S6底线 | S7锋芒 | S8温柔 | S9权力 | S10秩序 |\n"
    result_md += "|--------|--------|--------|--------|--------|--------|--------|--------|--------|----------|\n"
    result_md += "| " + " | ".join(str(v) for v in new_vals) + " |\n\n"
    result_md += "### L/M/H分类\n"
    result_md += ", ".join(f"{dim_keys[i]}:{lmh[i]}" for i in range(10)) + "\n(<2.5=L, 2.5-3.5=M, >3.5=H)\n\n"

with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/character-centroids-v2.md', 'w') as f:
    f.write(result_md)

with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/character-centroids-v2.json', 'w') as f:
    json.dump(result_json, f, ensure_ascii=False, indent=2)

print(f"Done. {len(result_json)} characters converted.")
