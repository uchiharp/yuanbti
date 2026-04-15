#!/usr/bin/env python3
"""Classify 密探故事 world lines and time periods."""

import json
import re
from collections import defaultdict

# Character-based time estimates for 代号鸢
# Based on historical Three Kingdoms period, the game roughly covers 190-220 AD
CHARACTER_ERA = {
    # Late Han figures
    "卢植": {"earliest": 160, "latest": 192, "note": "卢植约192年去世"},
    "刘辩": {"earliest": 189, "latest": 190, "note": "刘辩189年即位，190年被废"},
    "董卓": {"earliest": 189, "latest": 192, "note": "董卓189-192年掌权"},
    "何进": {"earliest": 184, "latest": 189, "note": "何进189年被杀"},
    "吕布": {"earliest": 190, "latest": 198, "note": "吕布198年下邳败亡"},
    "张辽": {"earliest": 194, "latest": 220, "note": "张辽活跃于194年后"},
    "张郃": {"earliest": 191, "latest": 220, "note": "张郃官渡前后活跃"},
    "庞德": {"earliest": 194, "latest": 219, "note": "庞德219年樊城战死"},
    "孔融": {"earliest": 190, "latest": 208, "note": "孔融208年被杀"},
    "华佗": {"earliest": 190, "latest": 208, "note": "华佗约208年去世"},
    "干吉": {"earliest": 184, "latest": 200, "note": "干吉太平道"},
    "周瑜": {"earliest": 195, "latest": 210, "note": "周瑜210年去世"},
    "小乔": {"earliest": 199, "latest": 220, "note": "小乔与周瑜同期"},
    "孙权": {"earliest": 200, "latest": 220, "note": "孙权200年后主事"},
    "凌统": {"earliest": 200, "latest": 220, "note": "凌统活跃于孙吴时期"},
    "吕蒙": {"earliest": 200, "latest": 220, "note": "吕蒙活跃于孙吴时期"},
    "士燮": {"earliest": 190, "latest": 210, "note": "士燮交州割据"},
    "刘表": {"earliest": 190, "latest": 208, "note": "刘表208年去世"},
    "刘璋": {"earliest": 194, "latest": 214, "note": "刘璋214年投降刘备"},
    "刘繇": {"earliest": 194, "latest": 197, "note": "刘繇197年去世"},
    "刘豹": {"earliest": 195, "latest": 220, "note": "刘豹南匈奴"},
    "庞统": {"earliest": 208, "latest": 214, "note": "庞统214年落凤坡战死"},
    "安期": {"earliest": 190, "latest": 220, "note": "安期为游戏原创角色"},
    "周忠": {"earliest": 190, "latest": 220, "note": "周忠为游戏原创角色"},
    "阿蝉": {"earliest": 190, "latest": 220, "note": "阿蝉为游戏原创角色"},
}

# Time keyword patterns for specific years
TIME_PATTERNS = {
    "太平": {"year": 184, "note": "太平道起义184年"},
    "初平": {"year": 190, "note": "初平元年190年"},
    "建安": {"year": 196, "note": "建安元年196年"},
    "兴平": {"year": 194, "note": "兴平元年194年"},
    "黄巾": {"year": 184, "note": "黄巾起义184年"},
    "官渡": {"year": 200, "note": "官渡之战200年"},
    "赤壁": {"year": 208, "note": "赤壁之战208年"},
}

# Worldline classification keywords
DREAM_KEYWORDS = {"梦", "梦境", "大梦", "如梦", "梦中"}
CROSSWORLD_KEYWORDS = {"穿越", "另一个世界", "异世界", "时空", "时间裂缝"}
PARALLEL_KEYWORDS = {"如果", "假如", "平行", "IF", "另一个", "不同的未来", "命运改变"}
LOOP_KEYWORDS = {"轮回", "循环", "重置", "重来", "回到", "重复", "时间闭环"}
SOUL_KEYWORDS = {"魂", "魂魄", "前世", "因果", "命数", "命运", "天命", "三千世界"}


def get_character(title):
    return title.split("-")[0]


def classify_worldline(story):
    wl_kw = story.get("worldline_keywords", []) or []
    wl_str = " ".join(wl_kw)
    chars = story.get("characters", []) or []
    loc = story.get("location_keywords", []) or []
    
    # Check for explicit parallel/IF indicators
    if any(k in wl_str for k in PARALLEL_KEYWORDS):
        if "梦" not in wl_str and "梦境" not in wl_str:
            return "World-P", "包含平行世界/IF线关键词", "if线"
    
    # Check for time loop
    if any(k in wl_str for k in LOOP_KEYWORDS):
        return "Loop-L", "包含时间循环/重置关键词", "时间循环"
    
    # Check for cross-world
    if any(k in wl_str for k in CROSSWORLD_KEYWORDS):
        return "World-C", "包含穿越/时空关键词", "穿越世界"
    
    # Dreams - mostly still main world
    if any(k in wl_str for k in DREAM_KEYWORDS):
        return "World-0", "梦境内容，发生在主世界", "本体"
    
    # Soul/spiritual themes - usually still main world
    if any(k in wl_str for k in SOUL_KEYWORDS):
        # "三千世界" might indicate World-C
        if "三千" in wl_str and "世界" in wl_str:
            return "World-C", "涉及三千世界概念", "穿越世界"
        if "前世" in wl_str:
            return "World-0", "涉及前世元素，属主世界设定", "本体"
        return "World-0", "涉及魂魄/天命元素，属主世界观", "本体"
    
    # Default: main world
    return "World-0", "无特殊世界线标记，默认主世界", "本体"


def estimate_time(story):
    """Estimate time period based on available signals."""
    char = get_character(story["title"])
    time_kw = story.get("time_keywords", []) or []
    loc = story.get("location_keywords", []) or []
    chars_in_story = story.get("characters", []) or []
    wl_kw = story.get("worldline_keywords", []) or []
    wl_str = " ".join(wl_kw)
    
    # Check explicit time patterns
    for kw in time_kw:
        for pattern, info in TIME_PATTERNS.items():
            if pattern in kw:
                return f"约{info['year']}年", info["year"], info["note"]
    
    # Check for chapter number hints
    chapter = story["title"].split("/")[-1] if "/" in story["title"] else ""
    
    # Use character era
    if char in CHARACTER_ERA:
        era = CHARACTER_ERA[char]
        return f"约{era['earliest']}-{era['latest']}年", era["earliest"], era["note"]
    
    return "时间未知", 0, "无法确定时间节点"


def classify_story(story):
    world_line, wl_reason, glw_state = classify_worldline(story)
    est_year, year_sort, time_note = estimate_time(story)
    
    # Confidence based on available signals
    has_wl = bool(story.get("worldline_keywords"))
    has_time = bool(story.get("time_keywords"))
    confidence = "high" if (has_wl or has_time) else "low"
    if has_wl and has_time:
        confidence = "medium"
    
    # Build summary from characters and locations
    chars = story.get("characters", []) or []
    loc = story.get("location_keywords", []) or []
    summary_parts = []
    if chars:
        named = [c for c in chars if c != "我" and "头像" not in c]
        if named:
            summary_parts.append(f"出场角色: {'、'.join(named[:5])}")
    if loc:
        summary_parts.append(f"地点: {'、'.join(loc[:3])}")
    if story.get("worldline_keywords"):
        summary_parts.append(f"关键词: {'、'.join(story['worldline_keywords'][:5])}")
    
    return {
        "title": story["title"],
        "world_line": world_line,
        "estimated_year": est_year,
        "year_sort": year_sort,
        "confidence": confidence,
        "reasoning": f"{wl_reason}。{time_note}",
        "story_summary": "；".join(summary_parts) if summary_parts else "信息不足",
        "guanglingwang_state": glw_state,
    }


def main():
    all_results = []
    all_data = []
    
    # Load all batches
    for i in range(19):
        fn = f"dhyy_features_mitan_{i:02d}.json"
        with open(fn) as f:
            data = json.load(f)
        all_data.extend(data)
    
    # Deduplicate by title (keep first occurrence)
    seen = set()
    unique_data = []
    for story in all_data:
        if story["title"] not in seen:
            seen.add(story["title"])
            unique_data.append(story)
    
    print(f"Total: {len(all_data)}, Unique: {len(unique_data)}")
    
    # Classify each
    for story in unique_data:
        result = classify_story(story)
        all_results.append(result)
    
    # Stats
    wl_dist = defaultdict(int)
    for r in all_results:
        wl_dist[r["world_line"]] += 1
    
    print("\nWorld line distribution:")
    for wl, count in sorted(wl_dist.items()):
        print(f"  {wl}: {count}")
    
    # Write output
    with open("dhyy_classified_密探故事.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\nOutput: dhyy_classified_密探故事.json ({len(all_results)} entries)")


if __name__ == "__main__":
    main()
