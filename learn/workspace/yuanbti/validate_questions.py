#!/usr/bin/env python3
"""
代号鸢BTI性格测试题质检脚本

对5个角色的题库进行全面质检，包括格式检查和内容检查。
输出详细的质检报告。
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Set, Any

# 维度定义
VALID_DIMENSIONS = {f"S{i}" for i in range(1, 11)}  # S1-S10
VALID_TYPES = {"sweet", "funny", "angst", "scheme", "daily", "classic"}
VALID_TENDENCY = {"L", "M", "H"}
VALID_SCORES = {1, 3, 5}

# 角色人设描述（用于内容检查）
CHARACTER_PERSONAS = {
    "袁基": "绿茶/操控型，表面温文尔雅实际在算计",
    "刘辩": "从废帝到天师，死心塌地",
    "傅融": "务实守护型",
    "孙策": "热烈直球、豪爽",
    "左慈": "表面超然实际深切在意"
}

class QuestionValidator:
    """题目验证器"""
    
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
        
        # 1. reasoning合理性检查
        for i, opt in enumerate(options):
            label = opt.get("label", f"Option{i}")
            reasoning = opt.get("reasoning", "")
            scores = opt.get("scores", {})
            
            # reasoning是否解释了为什么这个分值？
            if not reasoning or len(reasoning) < 10:
                issues.append(f"{label}: reasoning太短或为空: {reasoning[:50]}...")
            
            # 分值和reasoning是否一致？
            # 更精细的检查逻辑
            # 检查S8（温柔）相关
            if "S8" in scores:
                # 检查是否有否定词
                has_negation = any(word in reasoning for word in ["不温柔", "不算温柔", "不体贴", "不关心", "保持距离", "距离", "冷漠"])
                is_positive = any(word in reasoning for word in ["温柔", "体贴", "关心", "亲密", "温暖"])
                
                if has_negation and scores["S8"] == 5:
                    issues.append(f"{label}: reasoning含有否定词但S8:5偏高 - '{reasoning[:30]}...'")
                elif is_positive and not has_negation and scores["S8"] == 1:
                    issues.append(f"{label}: reasoning说'温柔'但S8:1偏低 - '{reasoning[:30]}...'")
            
            # 检查S2（情感表达）相关
            if "S2" in scores:
                has_negation = any(word in reasoning for word in ["不表达", "回避情感", "回避互动", "不互动", "回避", "拒绝"])
                is_positive = any(word in reasoning for word in ["表达情感", "情感表达", "互动", "回应", "表白"])
                
                if has_negation and scores["S2"] == 5:
                    issues.append(f"{label}: reasoning含有否定词但S2:5偏高 - '{reasoning[:30]}...'")
                elif is_positive and not has_negation and scores["S2"] == 1:
                    issues.append(f"{label}: reasoning说'表达情感'但S2:1偏低 - '{reasoning[:30]}...'")
        
        # 2. 选项排他性检查
        if len(options) == 3:
            texts = [opt.get("text", "") for opt in options]
            # 检查A和B是否太接近（简单字符串相似度）
            for i in range(len(texts)):
                for j in range(i+1, len(texts)):
                    # 简单检查：如果选项文本前10个字符相同，可能太接近
                    if texts[i][:10] == texts[j][:10] and len(texts[i]) > 15:
                        issues.append(f"选项{options[i]['label']}和{options[j]['label']}可能太接近: '{texts[i][:30]}...' vs '{texts[j][:30]}...'")
        
        # 3. 广陵王形象检查（选项是否粗鲁/没礼貌）
        rude_words = ["滚", "闭嘴", "烦死了", "别烦我", "走开"]
        for opt in options:
            text = opt.get("text", "")
            for rude in rude_words:
                if rude in text:
                    issues.append(f"{opt['label']}: 选项包含粗鲁用语: '{rude}'")
        
        # 4. 人设准确性检查（简单关键词检查）
        character = self.character
        if character == "袁基":
            # 检查是否体现绿茶/操控特性
            pass
        elif character == "刘辩":
            # 检查是否体现死心塌地特性
            pass
        # 其他角色类似
        
        if issues:
            self.content_issues.append((qid, issues))
            return False
        return True
    
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
        
        validator = QuestionValidator(character)
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
    
    report_lines.append("# 代号鸢BTI性格测试题质检报告")
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
    report_path = os.path.join(os.path.dirname(__file__), "validation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\n报告已生成: {report_path}")


if __name__ == "__main__":
    validate_all_questions()