#!/usr/bin/env python3
import json

with open("/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"总共 {len(questions)} 道题")

allowed_types = {"sweet", "funny", "angst", "scheme", "daily", "classic"}
allowed_tendency = {"L", "M", "H"}
allowed_scores = {1, 3, 5}

issues = []

for i, q in enumerate(questions):
    # 检查type
    if q["type"] not in allowed_types:
        issues.append(f"第{i+1}题 id={q['id']} type错误: {q['type']}")
    
    # 检查dimension是数组
    if not isinstance(q["dimension"], list):
        issues.append(f"第{i+1}题 dimension不是数组: {q['dimension']}")
    else:
        for d in q["dimension"]:
            if not d.startswith("S") or not d[1:].isdigit() or int(d[1:]) < 1 or int(d[1:]) > 10:
                issues.append(f"第{i+1}题 dimension值错误: {d}")
    
    # 检查选项数量
    if len(q["options"]) != 3:
        issues.append(f"第{i+1}题 选项不是3个: {len(q['options'])}")
    
    # 检查每个选项
    for opt in q["options"]:
        # tendency
        if opt["tendency"] not in allowed_tendency:
            issues.append(f"第{i+1}题 选项{opt['label']} tendency错误: {opt['tendency']}")
        # scores
        for dim, score in opt["scores"].items():
            if score not in allowed_scores:
                issues.append(f"第{i+1}题 选项{opt['label']} 分值错误: {score}")
            if dim not in q["dimension"]:
                issues.append(f"第{i+1}题 选项{opt['label']} 评分维度{dim}不在题目dimension中")
        # 选项文本不以"你"开头
        if opt["text"].startswith("你"):
            issues.append(f"第{i+1}题 选项{opt['label']} 以'你'开头: {opt['text']}")
        # 选项不能是"你说XXX"形式（简单检查）
        if opt["text"].startswith("你说") or opt["text"].startswith("你问") or opt["text"].startswith("你"):
            # 但我们已经检查了以"你"开头，这里再检查一下
            pass
    
    # 检查reveal是否包含台词引用
    if "台词" not in q["reveal"] and "（" not in q["reveal"]:
        issues.append(f"第{i+1}题 reveal可能未引用台词: {q['reveal'][:50]}")

if issues:
    print("发现以下问题:")
    for issue in issues:
        print(" -", issue)
else:
    print("所有题目格式检查通过！")

# 统计维度覆盖
dim_count = {}
for q in questions:
    for d in q["dimension"]:
        dim_count[d] = dim_count.get(d, 0) + 1

print("\n维度覆盖统计:")
for dim in sorted(dim_count.keys()):
    print(f"  {dim}: {dim_count[dim]}题")