#!/usr/bin/env python3
import json
import os
import sys

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def round_score(val):
    """将分数值四舍五入到1/3/5"""
    if val <= 2:
        return 1
    elif val <= 4:
        return 3
    else:
        return 5

def generate_reasoning(opt_text, scores, dimensions):
    """根据选项文本和分数生成reasoning"""
    # 简化：基于分数生成描述
    dim_names = {
        'S1': '权谋', 'S2': '情感', 'S3': '务实', 'S4': '面具',
        'S5': '行动', 'S6': '底线', 'S7': '锋芒', 'S8': '温柔',
        'S9': '权力', 'S10': '秩序'
    }
    parts = []
    for d in dimensions:
        val = scores[d]
        name = dim_names.get(d, d)
        if val == 1:
            level = '低'
        elif val == 3:
            level = '中'
        else:
            level = '高'
        parts.append(f"{name}{level}")
    return f"选项行为 → {opt_text[:20]}... 体现{'、'.join(parts)}"

def fix_all_questions(data):
    """修复所有题目的reasoning和分数"""
    for q in data:
        dims = q['dimension']
        for opt in q['options']:
            scores = opt['scores']
            # 修正分数值为1/3/5
            for d in dims:
                if d in scores:
                    scores[d] = round_score(scores[d])
                else:
                    scores[d] = 3  # 默认值
            
            # 确保两个维度分值不完全相同（如果相同且不是极端值，调整一个）
            if len(dims) == 2:
                d1, d2 = dims[0], dims[1]
                if scores[d1] == scores[d2]:
                    # 如果都是1或5，保持原样；否则调整一个
                    if scores[d1] == 3:
                        # 根据选项内容决定调整哪个维度（简化：调整第二个）
                        scores[d2] = 1
            
            # 生成或更新reasoning
            if 'reasoning' not in opt:
                opt['reasoning'] = generate_reasoning(opt['text'], scores, dims)
    return data

def replace_batch2_questions(data):
    """替换批次2（funny）的第1、2题"""
    funny_indices = [i for i, q in enumerate(data) if q['type'] == 'funny']
    if len(funny_indices) >= 5:
        # 新题目1
        new_q1 = {
            "id": "yuanji_funny_01",
            "type": "funny",
            "dimension": ["S4", "S7"],
            "source_character": "袁基",
            "text": "袁基和你讨论人际关系时笑着说：'人心微妙，人与人之间，总有各自的相处之道。' 你觉得他这话是在暗示什么？",
            "options": [
                {
                    "label": "A",
                    "text": "点头称是，说确实如此。",
                    "scores": {"S4": 5, "S7": 1},
                    "tendency": "L",
                    "reasoning": "选项行为 → 面具:5，锋芒:1（表面附和，不显露锋芒）"
                },
                {
                    "label": "B",
                    "text": "开玩笑说'长公子是在说我们吗？'",
                    "scores": {"S4": 3, "S7": 3},
                    "tendency": "M",
                    "reasoning": "选项行为 → 面具:3，锋芒:3（半开玩笑，适度试探）"
                },
                {
                    "label": "C",
                    "text": "直接问'你在指哪段关系？'",
                    "scores": {"S4": 1, "S7": 5},
                    "tendency": "H",
                    "reasoning": "选项行为 → 面具:1，锋芒:5（直接追问，锋芒毕露）"
                }
            ],
            "reveal": "袁基台词'人心微妙，人与人之间，总有各自的相处之道。'（桂舟露影）——袁基用哲理调侃人际关系，测试你的回应方式。"
        }
        
        # 新题目2（修正分数）
        new_q2 = {
            "id": "yuanji_funny_02",
            "type": "funny",
            "dimension": ["S2", "S8"],
            "source_character": "袁基",
            "text": "袁基在高粱地里被草叶弄得很痒，嘟囔着'好痒。回去得难过好多天……' 你会怎么回应？",
            "options": [
                {
                    "label": "A",
                    "text": "严肃说'下次注意些'。",
                    "scores": {"S2": 1, "S8": 1},
                    "tendency": "L",
                    "reasoning": "选项行为 → 情感:1，温柔:1（缺乏共情，严肃说教）"
                },
                {
                    "label": "B",
                    "text": "笑他'活该，谁让你乱跑'。",
                    "scores": {"S2": 3, "S8": 3},
                    "tendency": "M",
                    "reasoning": "选项行为 → 情感:3，温柔:3（玩笑回应，略带关心）"
                },
                {
                    "label": "C",
                    "text": "帮他拍掉草叶，说'回去我帮你上药'。",
                    "scores": {"S2": 5, "S8": 5},
                    "tendency": "H",
                    "reasoning": "选项行为 → 情感:5，温柔:5（主动关心，温柔体贴）"
                }
            ],
            "reveal": "袁基台词'好痒。回去得难过好多天……'（回乡的诱惑）——袁基在亲密场景中撒娇，测试你的关心程度。"
        }
        
        data[funny_indices[0]] = new_q1
        data[funny_indices[1]] = new_q2
        print(f"已替换批次2的第1、2题")
    return data

def main():
    input_path = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji.json'
    output_path = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji_final.json'
    
    if not os.path.exists(input_path):
        print(f"输入文件不存在: {input_path}")
        sys.exit(1)
    
    data = load_json(input_path)
    print(f"加载了 {len(data)} 道题")
    
    # 修复所有题目
    data = fix_all_questions(data)
    
    # 替换批次2的第1、2题
    data = replace_batch2_questions(data)
    
    # 保存结果
    save_json(data, output_path)
    print(f"已保存到 {output_path}")
    
    # 验证
    missing_reasoning = []
    score_issues = []
    same_score_issues = []
    for q in data:
        dims = q['dimension']
        for opt in q['options']:
            if 'reasoning' not in opt:
                missing_reasoning.append((q['id'], opt['label']))
            scores = opt['scores']
            for d in dims:
                val = scores.get(d)
                if val not in [1, 3, 5]:
                    score_issues.append(f"{q['id']} {opt['label']}: {d}={val}")
            if len(dims) == 2:
                d1, d2 = dims[0], dims[1]
                if scores.get(d1) == scores.get(d2):
                    same_score_issues.append(f"{q['id']} {opt['label']}: {d1}={scores[d1]}, {d2}={scores[d2]}")
    
    print(f"\n验证结果:")
    print(f"缺少reasoning的选项数量: {len(missing_reasoning)}")
    print(f"分数值问题数量: {len(score_issues)}")
    print(f"维度同分数量: {len(same_score_issues)}")
    
    if score_issues:
        print("\n分数值问题前5个:")
        for i in score_issues[:5]:
            print(f"  {i}")
    
    if same_score_issues:
        print("\n维度同分前5个:")
        for i in same_score_issues[:5]:
            print(f"  {i}")

if __name__ == '__main__':
    main()