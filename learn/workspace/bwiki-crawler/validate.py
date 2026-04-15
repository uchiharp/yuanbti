#!/usr/bin/env python3
"""BWIKI 代号鸢爬虫数据验证脚本"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_MAP = {
    "密探/传唤": "密探传唤",
    "密探/故事": "密探故事",
    "密探/留音": "密探留音",
    "密探/羁绊": "密探羁绊",
    "剧情/主线": "主线剧情",
    "剧情/活动": "活动剧情",
    "剧情/恋念": "恋念剧情",
    "男主/红鸾花笺": "红鸾花笺",
    "男主/恋念之音": "恋念之音",
    "男主/约会": "约会",
    "男主/留音": "男主留音",
    "鸢记": "鸢记",
}

REQUIRED_FIELDS = ["title", "category", "content", "source_url", "crawled_at"]


def check_crawled_at(val):
    try:
        datetime.fromisoformat(val)
        return True
    except:
        return False


def is_suspicious(data):
    """Check if a file is suspicious (empty content, only template, etc.)"""
    reasons = []
    content = data.get("content", [])
    if not content:
        reasons.append("content为空")
    else:
        # Check if all content items are raw wikitext (not parsed)
        all_raw = all(item.get("type") == "raw" for item in content)
        if all_raw and content:
            reasons.append("全部为raw未解析")
        
        # Check if content looks like HTML/layout remnants
        html_patterns = re.compile(r'__NOTOC__|div class|colxs|colsm|colmd|collg|用户头像')
        html_count = sum(1 for item in content if html_patterns.search(item.get("text", "")))
        if html_count > len(content) * 0.5:
            reasons.append(f"大量HTML残留({html_count}/{len(content)}条)")
    
    return reasons


def main():
    results = {}  # category -> stats
    all_files = []
    title_map = defaultdict(list)  # title -> [filepath]
    quality = {
        "json_valid": 0,
        "json_invalid": 0,
        "missing_fields": 0,
        "empty_content": 0,
        "duplicates": 0,
        "suspicious_files": [],
    }
    samples = {}  # category -> sample file content preview

    for subdir, cat_name in CATEGORY_MAP.items():
        dir_path = os.path.join(BASE_DIR, subdir)
        if not os.path.isdir(dir_path):
            continue
        
        cat_stats = {"total": 0, "success": 0, "failed": 0, "empty_content": 0}
        json_files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
        
        # Pick one random sample per category
        if json_files:
            sample_file = random.choice(json_files)
        
        for jf in json_files:
            filepath = os.path.join(dir_path, jf)
            cat_stats["total"] += 1
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                quality["json_valid"] += 1
            except (json.JSONDecodeError, Exception) as e:
                quality["json_invalid"] += 1
                cat_stats["failed"] += 1
                quality["suspicious_files"].append({"file": filepath, "reason": f"JSON解析失败: {e}"})
                continue
            
            # Check required fields
            missing = [f for f in REQUIRED_FIELDS if f not in data or not data[f]]
            if missing:
                quality["missing_fields"] += 1
                quality["suspicious_files"].append({"file": filepath, "reason": f"缺失字段: {missing}"})
            
            # Check content
            content = data.get("content", [])
            if not content:
                quality["empty_content"] += 1
                cat_stats["empty_content"] += 1
            
            # Check raw_wikitext
            if not data.get("raw_wikitext"):
                quality["suspicious_files"].append({"file": filepath, "reason": "raw_wikitext为空"})
            
            # Check crawled_at format
            if not check_crawled_at(data.get("crawled_at", "")):
                quality["suspicious_files"].append({"file": filepath, "reason": "crawled_at格式错误"})
            
            # Track titles for duplicate detection
            title_map[data.get("title", "")].append(filepath)
            
            # Check suspicious
            reasons = is_suspicious(data)
            if reasons:
                quality["suspicious_files"].append({"file": filepath, "reason": "; ".join(reasons)})
            
            cat_stats["success"] += 1
            
            # Collect sample
            if jf == sample_file:
                samples[cat_name] = {
                    "file": jf,
                    "title": data.get("title", ""),
                    "content_preview": content[:3] if content else [],
                }
            
            all_files.append(filepath)
        
        results[cat_name] = {**cat_stats, "output_dir": subdir}
    
    # Count duplicates
    dup_count = 0
    for title, paths in title_map.items():
        if len(paths) > 1:
            dup_count += len(paths) - 1
            quality["suspicious_files"].append({"file": paths[0], "reason": f"重复title: '{title}' 出现{len(paths)}次"})
    quality["duplicates"] = dup_count
    
    # Build metadata
    total_pages = sum(c["total"] for c in results.values())
    total_success = sum(c["success"] for c in results.values())
    total_failed = sum(c["failed"] for c in results.values())
    
    metadata = {
        "crawl_info": {
            "crawl_time": "2026-04-12",
            "total_pages": total_pages,
            "total_success": total_success,
            "total_failed": total_failed,
            "source": "https://wiki.biligame.com/yuan/",
        },
        "categories": results,
        "quality": quality,
    }
    
    with open(os.path.join(BASE_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"✅ metadata.json 已生成")
    
    # Generate report
    report_lines = [
        "# BWIKI 代号鸢剧情爬取验证报告",
        "",
        "## 概览",
        f"- 爬取时间：2026-04-12",
        f"- 数据总量：{total_pages} 页",
        f"- 成功率：{total_success}/{total_pages} ({total_success*100//total_pages if total_pages else 0}%)",
        f"- 失败页面：{total_failed}",
        "",
        "## 各分类详情",
        "| 分类 | 总页面 | 成功 | 失败 | 空内容 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for cat_name, stats in results.items():
        report_lines.append(f"| {cat_name} | {stats['total']} | {stats['success']} | {stats['failed']} | {stats['empty_content']} |")
    
    report_lines += [
        "",
        "## 数据质量",
        f"- JSON 格式合法：{quality['json_valid']}/{total_pages}",
        f"- JSON 格式非法：{quality['json_invalid']}",
        f"- 缺失必填字段：{quality['missing_fields']}",
        f"- content 为空：{quality['empty_content']}",
        f"- 重复页面（相同 title）：{quality['duplicates']}",
    ]
    
    if quality["suspicious_files"]:
        report_lines.append(f"- 可疑文件总数：{len(quality['suspicious_files'])}")
        report_lines.append("")
        report_lines.append("### 可疑文件列表")
        report_lines.append("| 文件 | 原因 |")
        report_lines.append("| --- | --- |")
        for sf in quality["suspicious_files"][:50]:  # limit
            rel_path = sf["file"].replace(BASE_DIR + "/", "")
            report_lines.append(f"| `{rel_path}` | {sf['reason']} |")
        if len(quality["suspicious_files"]) > 50:
            report_lines.append(f"| ... 还有 {len(quality['suspicious_files'])-50} 个 | |")
    else:
        report_lines.append("- 可疑文件：无")
    
    report_lines += [
        "",
        "## 抽样检查",
        "从每个分类随机抽取 1 个文件，展示 content 前 3 条：",
        "",
    ]
    
    for cat_name, sample in samples.items():
        report_lines.append(f"### {cat_name} — `{sample['file']}`")
        report_lines.append(f"**title**: {sample['title']}")
        if sample["content_preview"]:
            for i, item in enumerate(sample["content_preview"][:3]):
                t = item.get("type", "?")
                text = item.get("text", "")[:120]
                speaker = item.get("speaker", "")
                if speaker:
                    report_lines.append(f"  {i+1}. [{t}] **{speaker}**: {text}")
                else:
                    report_lines.append(f"  {i+1}. [{t}] {text}")
        else:
            report_lines.append("  *(content 为空)*")
        report_lines.append("")
    
    report_lines += [
        "## 增量更新说明",
        "如需后续增量爬取，运行对应分类的脚本即可（已存在文件会自动跳过）。",
    ]
    
    with open(os.path.join(BASE_DIR, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"✅ report.md 已生成")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"总页面: {total_pages}")
    print(f"JSON合法: {quality['json_valid']}")
    print(f"JSON非法: {quality['json_invalid']}")
    print(f"缺失字段: {quality['missing_fields']}")
    print(f"空内容: {quality['empty_content']}")
    print(f"重复: {quality['duplicates']}")
    print(f"可疑文件: {len(quality['suspicious_files'])}")


if __name__ == "__main__":
    main()
