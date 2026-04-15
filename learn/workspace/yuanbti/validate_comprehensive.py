#!/usr/bin/env python3
"""
代号鸢BTI性格测试题全面质检脚本
包含更详细的内容检查
"""

import json
import os
import re
from typing import Dict, List, Tuple, Set, Any

# 维度定义
VALID_DIMENSIONS = {f"S{i}" for i in range(1, 11)}  # S1-S10
VALID_TYPES = {"sweet", "funny", "angst", "scheme", "daily", "classic"}
VALID_TENDENCY = {"L", "M", "H"}
VALID_SCORES = {1, 3, 5}

# 角色人设关键词
CHARACTER_KEYWORDS = {
    "袁基": ["绿茶", "操控", "算计", "温文尔雅", "面具", "试探", "权谋"],
    "刘辩": ["死心塌地", "撒娇", "装疼", "先帝", "天师", "依赖"],
    "傅融": ["务实", "节俭", "守护", "嘴硬心软", "财务", "算账"],
    "孙策": ["直球", "热烈", "豪爽", "小霸王", "保护", "霸气"],
    "左慈": ["超然", "师尊", "关心", "钓鱼", "耐心", "清冷"]
}

class ComprehensiveValidator:
    """全面验证器"""
    
    def __init__(self, character: str):
        self.character = character
        self.format_issues = []
        self.content_issues = []
        self.passed_count = 0
        self.total_count = 0
        
    def validate_question(self, question: Dict) -> bool:
        """验证单个题目，返回是否通过"""
        self.total_count += 1
        qid = question.get("id", "unknown")
        
        # 检查格式
        format_ok = self._check_format(qid, question)
        
        # 检查内容
        content_ok = self._check_content(qid, question)
        
        if format_ok and content_ok:
            self.passed_count += 1
            return True
        return False
    
    def _check_format(self, qid: str, question: Dict) -> bool:
        """格式检查"""
        issues = []
        
        # 1. type检查
        qtype = question.get("type")
        if qtype not in VALID_TYPES:
            issues.append(f"type无效: {qtype} (应为{sorted(VALID_TYPES)})")
        
        # 2. dimension检查
        dimensions = question.get("dimension", [])
        if not isinstance(dimensions, list):
            issues.append(f"dimension不是数组: {dimensions}")
        else:
            invalid_dims = [d for d in dimensions if d not in VALID_DIMENSIONS]
            if invalid_dims:
                issues.append(f"dimension包含无效维度: {invalid_dims}")
            if len(dimensions) < 2 or len(dimensions) > 3:
                issues.append(f"dimension数量应为2-3个，实际: {len(dimensions)}")
        
        # 3. 选项数量检查
        options = question.get("options", [])
        if len(options) != 3:
            issues.append(f"选项数量不为3: {len(options)}")
        
        # 4. 每个选项的检查
        for i, opt in enumerate(options):
            label = opt.get("label", f"Option{i}")
            
            # tendency检查
            tendency = opt.get("tendency")
            if tendency not in VALID_TENDENCY:
                issues.append(f"{label}: tendency无效: {tendency} (应为L/M/H)")
            
            # scores检查
            scores = opt.get("scores", {})
            # 检查scores的key是否和dimension一致
            if set(scores.keys()) != set(dimensions):
                issues.append(f"{label}: scores的key与dimension不一致: {set(scores.keys())} vs {set(dimensions)}")
            
            # 分值检查
            for dim, score in scores.items():
                if score not in VALID_SCORES:
                    issues.append(f"{label}: {dim}分值无效: {score} (应为1/3/5)")
            
            # reasoning检查（存在性）
            if "reasoning" not in opt:
                issues.append(f"{label}: 缺少reasoning字段")
            
            # 选项文本检查：不以"你"或"广陵王"开头
            text = opt.get("text", "")
            if text.startswith("你") or text.startswith("广陵王"):
                issues.append(f"{label}: 选项以'你'或'广陵王'开头: {text[:20]}...")
        
        # 5. reveal检查
        if "reveal" not in question:
            issues.append("缺少reveal字段")
        
        if issues:
            self.format_issues.append((qid, issues))
            return False
        return True
    
    def _check_content(self, qid: str, question: Dict) -> bool:
        """内容检查"""
        issues = []
        dimensions = question.get("dimension", [])
        options = question.get("options", [])
        text = question.get("text", "")
        
        # 1. reasoning合理性检查
        for i, opt in enumerate(options):
            label = opt.get("label", f"Option{i}")
            reasoning = opt.get("reasoning", "")
            scores = opt.get("scores", {})
            
            # reasoning是否解释了为什么这个分值？
            if not reasoning or len(reasoning) < 5:
                issues.append(f"{label}: reasoning太短或为空")
                continue
            
            # 检查reasoning是否提到维度
            for dim in dimensions:
                if dim not in reasoning:
                    issues.append(f"{label}: reasoning未解释{dim}分值")
            
            # 分值和reasoning的一致性检查（更智能）
            self._check_reasoning_consistency(label, reasoning, scores, issues)
        
        # 2. 选项排他性检查
        if len(options) == 3:
            texts = [opt.get("text", "").strip() for opt in options]
            # 检查是否有选项内容太接近
            for i in range(len(texts)):
                for j in range(i+1, len(texts)):
                    # 计算简单相似度（共同词汇）
                    words_i = set(re.findall(r'[\w\u4e00-\u9fff]+', texts[i]))
                    words_j = set(re.findall(r'[\w\u4e00-\u9fff]+', texts[j]))
                    common = words_i & words_j
                    if len(common) >= 5 and len(words_i) > 6 and len(words_j) > 6:
                        issues.append(f"选项{options[i]['label']}和{options[j]['label']}可能太接近（共同词汇{len(common)}个）")
        
        # 3. 广陵王形象检查
        rude_phrases = ["滚开", "闭嘴", "烦死了", "别烦我", "走开", "够了", "讨厌"]
        for opt in options:
            text = opt.get("text", "")
            for rude in rude_phrases:
                if rude in text:
                    issues.append(f"{opt['label']}: 选项包含粗鲁用语: '{rude}'")
        
        # 4. 人设准确性检查（简单检查）
        # 检查题干是否体现角色特点
        char_keywords = CHARACTER_KEYWORDS.get(self.character, [])
        if char_keywords:
            text_lower = text.lower()
            has_keyword = any(kw in text for kw in char_keywords)
            # 不强求每题都有人设关键词
        
        # 5. 选项内容与分值匹配检查（核心）
        self._check_option_score_match(qid, question, issues)
        
        if issues:
            self.content_issues.append((qid, issues))
            return False
        return True
    
    def _check_reasoning_consistency(self, label: str, reasoning: str, scores: Dict, issues: List):
        """检查reasoning与分值的一致性"""
        # S8（温柔）相关检查
        if "S8" in scores:
            score = scores["S8"]
            # 检查是否有温柔相关的表述
            gentle_words = ["温柔", "体贴", "关心", "暖心", "温暖"]
            ungentle_words = ["不温柔", "不算温柔", "不体贴", "不关心", "冷漠", "距离", "保持距离", "疏远"]
            
            has_gentle = any(word in reasoning for word in gentle_words)
            has_ungentle = any(word in reasoning for word in ungentle_words)
            
            if has_gentle and not has_ungentle and score == 1:
                issues.append(f"{label}: reasoning提到温柔但S8:1偏低")
            if has_ungentle and score == 5:
                issues.append(f"{label}: reasoning提到不温柔但S8:5偏高")
        
        # S2（情感表达）相关检查
        if "S2" in scores:
            score = scores["S2"]
            emotion_words = ["情感表达", "表达情感", "情感互动", "情感交流", "表白", "示爱"]
            no_emotion_words = ["不表达", "回避情感", "回避互动", "不互动", "拒绝", "回避", "掩饰情感"]
            
            has_emotion = any(word in reasoning for word in emotion_words)
            has_no_emotion = any(word in reasoning for word in no_emotion_words)
            
            # 特殊处理："情感互动"可能被误用
            if "情感互动" in reasoning and "→S2:1" in reasoning:
                # 这可能是在解释为什么S2是1分
                pass
            elif has_emotion and not has_no_emotion and score == 1:
                issues.append(f"{label}: reasoning提到情感表达但S2:1偏低")
            if has_no_emotion and score == 5:
                issues.append(f"{label}: reasoning提到不表达情感但S2:5偏高")
        
        # S7（表达锋芒）相关检查
        if "S7" in scores:
            score = scores["S7"]
            sharp_words = ["锋芒", "尖锐", "直接", "戳穿", "揭露", "挑衅"]
            mild_words = ["收敛", "委婉", "含蓄", "圆滑", "回避", "不直接"]
            
            has_sharp = any(word in reasoning for word in sharp_words)
            has_mild = any(word in reasoning for word in mild_words)
            
            if has_sharp and not has_mild and score == 1:
                issues.append(f"{label}: reasoning提到锋芒但S7:1偏低")
            if has_mild and score == 5:
                issues.append(f"{label}: reasoning提到收敛但S7:5偏高")
    
    def _check_option_score_match(self, qid: str, question: Dict, issues: List):
        """检查选项内容与分值是否匹配"""
        options = question.get("options", [])
        dimensions = question.get("dimension", [])
        
        # 对每个维度，检查选项内容与分值的逻辑关系
        for dim in dimensions:
            # 收集每个选项的文本和分值
            option_data = []
            for opt in options:
                text = opt.get("text", "")
                score = opt.get("scores", {}).get(dim, 0)
                option_data.append((opt["label"], text, score))
            
            # 根据维度类型进行逻辑检查
            if dim == "S8":  # 温柔
                gentle_keywords = ["握住", "温暖", "体贴", "关心", "照顾", "陪伴", "拥抱"]
                ungentle_keywords = ["拒绝", "抽身", "距离", "自重", "冷漠", "无视"]
                
                for label, text, score in option_data:
                    has_gentle = any(kw in text for kw in gentle_keywords)
                    has_ungentle = any(kw in text for kw in ungentle_keywords)
                    
                    if has_gentle and score == 1:
                        issues.append(f"{label}: 选项内容温柔但S8:1偏低: '{text[:30]}...'")
                    if has_ungentle and score == 5:
                        issues.append(f"{label}: 选项内容不温柔但S8:5偏高: '{text[:30]}...'")
            
            elif dim == "S2":  # 情感表达
                emotion_keywords = ["靠近", "倾听", "回应", "接受", "同意", "陪伴"]
                no_emotion_keywords = ["拒绝", "回避", "离开", "无视", "转移话题", "工作"]
                
                for label, text, score in option_data:
                    has_emotion = any(kw in text for kw in emotion_keywords)
                    has_no_emotion = any(kw in text for kw in no_emotion_keywords)
                    
                    if has_emotion and score == 1:
                        issues.append(f"{label}: 选项内容有情感互动但S2:1偏低: '{text[:30]}...'")
                    if has_no_emotion and score == 5:
                        issues.append(f"{label}: 选项内容回避情感但S2:5偏高: '{text[:30]}...'")
            
            elif dim == "S7":  # 表达锋芒
                sharp_keywords = ["戳穿", "揭露", "质问", "直接", "尖锐", "挑战"]
                mild_keywords = ["委婉", "含蓄", "回避", "转移", "不点破", "配合"]
                
                for label, text, score in option_data:
                    has_sharp = any(kw in text for kw in sharp_keywords)
                    has_mild = any(kw in text for kw in mild_keywords)
                    
                    if has_sharp and score == 1:
                        issues.append(f"{label}: 选项内容锋芒但S7:1偏低: '{text[:30]}...'")
                    if has_mild and score == 5:
                        issues.append(f"{label}: 选项内容含蓄但S7:5偏高: '{text[:30]}...'")
    
    def get_report(self) -> Dict:
        """获取验证报告"""
        return {
            "character": self.character,
            "total": self.total_count,
            "passed": self.passed_count,
            "need_fix": self.total_count - self.passed_count,
            "format_issues": self.format_issues,
            "content_issues": self.content_issues
        }


def validate_all_questions():
    """验证所有角色的题目"""
    data_dir = os.path.dirname(__file__)
    questions_dir = os.path.join(data_dir, "questions")
    
    if not os.path.exists(questions_dir):
        print(f"错误: 目录不存在: {questions_dir}")
        return
    
    character_files = {
        "袁基": "yuanji.json",
        "刘辩": "liubian.json", 
        "傅融": "furong.json",
        "孙策": "sunce.json",
        "左慈": "zuoci.json"
    }
    
    all_results = {}
    total_passed = 0
    total_questions = 0
    
    for character, filename in character_files.items():
        filepath = os.path.join(questions_dir, filename)
        if not os.path.exists(filepath):
            print(f"警告: 文件不存在: {filepath}")
            continue
        
        print(f"正在验证: {character} ({filename})...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                questions = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  JSON解析错误: {e}")
            continue
        except Exception as e:
            print(f"  读取文件错误: {e}")
            continue
        
        validator = ComprehensiveValidator(character)
        for q in questions:
            validator.validate_question(q)
        
        results = validator.get_report()
        all_results[character] = results
        total_passed += results["passed"]
        total_questions += results["total"]
        
        print(f"  {character}: 通过 {results['passed']}/{results['total']} 题")
    
    # 生成报告
    generate_report(all_results, total_questions, total_passed)


def generate_report(results: Dict, total_questions: int, total_passed: int):
    """生成质检报告"""
    report_lines = []
    
    report_lines.append("# 代号鸢BTI性格测试题全面质检报告")
    report_lines.append(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"总题数: {total_questions}，通过: {total_passed}，需修正: {total_questions - total_passed}")
    report_lines.append("")
    
    for character, result in results.items():
        report_lines.append(f"=== {character} ===")
        report_lines.append(f"通过/需修正: {result['passed']}/{result['total']}")
        
        if result['format_issues']:
            report_lines.append("格式问题:")
            for qid, issues in result['format_issues']:
                for issue in issues:
                    report_lines.append(f"  {qid}: {issue}")
        else:
            report_lines.append("格式问题: 无")
        
        if result['content_issues']:
            report_lines.append("内容问题:")
            for qid, issues in result['content_issues']:
                for issue in issues:
                    report_lines.append(f"  {qid}: {issue}")
        else:
            report_lines.append("内容问题: 无")
        
        report_lines.append("")
    
    report_lines.append(f"总结: 5角色共{total_questions}题，通过{total_passed}题，需修正{total_questions - total_passed}题")
    
    # 写入文件
    report_path = os.path.join(os.path.dirname(__file__), "validation_report_comprehensive.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\n全面质检报告已生成: {report_path}")


if __name__ == "__main__":
    validate_all_questions()