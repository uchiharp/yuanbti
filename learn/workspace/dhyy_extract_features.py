#!/usr/bin/env python3
"""Extract timeline features from dhyy_data for world-line classification."""

import json
import re
import psycopg2
from collections import Counter

TIME_KEYWORDS = [
    "初平", "建安", "光和", "中平", "永汉", "兴平", "延康", "黄初",
    "太和", "青龙", "景初", "正始", "嘉平", "正元", "甘露", "景元",
    "咸熙", "泰始", "太康", "元康", "永平", "永安", "建兴", "延熙",
    "景耀", "炎兴", "太平", "天纪", "天玺", "凤凰", "天册", "天佑",
    "宝鼎", "建衡", "凤凰", "天纪", "黄武", "黄龙", "嘉禾", "赤乌",
    "太元", "神凤", "五凤", "太平", "永安",
    "元年", "二年", "三年", "四年", "五年", "六年", "七年", "八年", "九年", "十年",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "公元", "年", "月", "日", "时辰", "子时", "丑时", "寅时", "卯时", "辰时",
    "巳时", "午时", "未时", "申时", "酉时", "戌时", "亥时",
]

LOCATION_KEYWORDS = [
    "雒阳", "洛阳", "长安", "许都", "许昌", "邺城", "邺", "广陵", "江东",
    "荆州", "成都", "宛城", "官渡", "赤壁", "下邳", "徐州", "兖州", "冀州",
    "青州", "幽州", "并州", "凉州", "益州", "扬州", "交州", "汉中", "襄阳",
    "江夏", "柴桑", "建业", "建康", "武昌", "夷陵", "夷道", "猇亭",
    "新野", "博望", "当阳", "长坂", "白门", "濮阳", "陈留", "东郡",
    "陈仓", "祁山", "街亭", "五丈原", "祁山", "斜谷", "汉中",
    "洛阳宫", "铜雀台", "凤仪亭", "白马", "延津", "仓亭", "黎阳",
    "合肥", "濡须", "濡须口", "石亭", "荆州城", "南郡", "零陵",
    "桂阳", "武陵", "长沙", "会稽", "吴郡", "庐江", "庐陵", "豫章",
    "南海", "苍梧", "郁林", "合浦", "交趾", "九真", "日南",
]

WORLDLINE_KEYWORDS = [
    "穿越", "世界", "宇宙", "梦境", "梦", "灵魂", "魂", "魂魄",
    "轮回", "重置", "平行", "另一个", "前世", "来世", "三千",
    "世界线", "时间线", "时空", "维度", "异世界", "梦醒", "大梦",
    "幻觉", "庄周", "蝴蝶", "黄粱", "南柯", "浮生", "如梦",
    "前世今生", "因果", "宿命", "天命", "命数", "命运",
    "镜中", "水中月", "虚幻", "真实", "假象", "幻境", "幻术",
]


def find_keywords(text, keywords):
    """Find all keywords present in text."""
    if not text:
        return []
    found = []
    for kw in keywords:
        if kw in text:
            found.append(kw)
    return found


def main():
    conn = psycopg2.connect(dbname="dhyy_data")
    cur = conn.cursor()

    # Get all stories
    cur.execute("""
        SELECT title, category, characters, 
               (SELECT count(*) FROM dialogues d WHERE d.story_title = sp.title AND d.category = sp.category) as dlg_count
        FROM story_pages sp
        ORDER BY category, title
    """)
    stories = cur.fetchall()

    results = []
    for title, category, characters_json, dlg_count in stories:
        characters = characters_json if isinstance(characters_json, list) else []

        # Get dialogues for this story
        cur.execute("""
            SELECT speaker, text FROM dialogues 
            WHERE story_title = %s AND category = %s
            ORDER BY line_order
        """, (title, category))
        dialogues = cur.fetchall()

        first_dlg = [{"speaker": s, "text": t} for s, t in dialogues[:5]]
        last_dlg = [{"speaker": s, "text": t} for s, t in dialogues[-5:]]

        # Concatenate all dialogue text for keyword search
        all_text = "\n".join(t for _, t in dialogues)
        time_kw = list(set(find_keywords(all_text, TIME_KEYWORDS)))
        loc_kw = list(set(find_keywords(all_text, LOCATION_KEYWORDS)))
        wl_kw = list(set(find_keywords(all_text, WORLDLINE_KEYWORDS)))

        # Key quotes: dialogues containing time/location/worldline keywords
        key_quotes = []
        for speaker, text in dialogues:
            has_key = any(kw in text for kw in TIME_KEYWORDS[:10] + LOCATION_KEYWORDS[:20] + WORLDLINE_KEYWORDS)
            if has_key and text.strip():
                key_quotes.append(f"{speaker}: {text[:100]}")
                if len(key_quotes) >= 5:
                    break

        results.append({
            "title": title,
            "category": category,
            "characters": characters,
            "dialogue_count": dlg_count,
            "first_dialogues": first_dlg,
            "last_dialogues": last_dlg,
            "time_keywords": time_kw,
            "location_keywords": loc_kw,
            "worldline_keywords": wl_kw,
            "key_quotes": key_quotes,
        })

    with open("/Users/sunwenyong/.openclaw/agents/learn/workspace/dhyy_timeline_features.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Step 3: Character themes for 密探故事
    cur.execute("""
        SELECT title, characters, 
               (SELECT count(*) FROM dialogues d WHERE d.story_title = sp.title AND d.category = sp.category) as dlg_count
        FROM story_pages sp
        WHERE category = '密探故事'
        ORDER BY title
    """)
    char_stories = cur.fetchall()

    # Extract character name from title (usually format like "角色名/章节" or similar)
    character_data = {}
    for title, characters_json, dlg_count in char_stories:
        chars = characters_json if isinstance(characters_json, list) else []
        if not chars:
            # Try to extract from title
            parts = title.split("/")
            if len(parts) >= 1:
                main_char = parts[0].strip()
                chars = [main_char]

        char_name = chars[0] if chars else title.split("/")[0].strip()

        if char_name not in character_data:
            character_data[char_name] = {
                "name": char_name,
                "story_titles": [],
                "total_dialogues": 0,
                "all_characters": set(),
                "time_keywords": Counter(),
                "location_keywords": Counter(),
                "worldline_keywords": Counter(),
                "key_events": [],
            }

        cd = character_data[char_name]
        cd["story_titles"].append(title)
        cd["total_dialogues"] += dlg_count
        cd["all_characters"].update(chars)

        # Get dialogues
        cur.execute("""
            SELECT speaker, text FROM dialogues 
            WHERE story_title = %s AND category = %s
            ORDER BY line_order
        """, (title, "密探故事"))
        dialogues = cur.fetchall()
        all_text = "\n".join(t for _, t in dialogues)

        for kw in find_keywords(all_text, TIME_KEYWORDS[:20]):
            cd["time_keywords"][kw] += 1
        for kw in find_keywords(all_text, LOCATION_KEYWORDS):
            cd["location_keywords"][kw] += 1
        for kw in find_keywords(all_text, WORLDLINE_KEYWORDS):
            cd["worldline_keywords"][kw] += 1

        # Extract event hints from first/last dialogues
        if dialogues:
            first_text = dialogues[0][1][:80] if dialogues[0][1] else ""
            last_text = dialogues[-1][1][:80] if dialogues[-1][1] else ""
            cd["key_events"].append(f"[{title}] 开: {first_text} | 结: {last_text}")

    char_themes = []
    for name, cd in character_data.items():
        char_themes.append({
            "name": name,
            "story_count": len(cd["story_titles"]),
            "total_dialogues": cd["total_dialogues"],
            "stories": cd["story_titles"][:5],  # First 5
            "main_interactions": sorted(cd["all_characters"] - {name})[:10],
            "time_keywords": dict(cd["time_keywords"].most_common(10)),
            "location_keywords": dict(cd["location_keywords"].most_common(10)),
            "worldline_keywords": dict(cd["worldline_keywords"].most_common(10)),
            "has_worldline_elements": len(cd["worldline_keywords"]) > 0,
            "key_events": cd["key_events"][:3],
        })

    with open("/Users/sunwenyong/.openclaw/agents/learn/workspace/dhyy_character_themes.json", "w", encoding="utf-8") as f:
        json.dump(char_themes, f, ensure_ascii=False, indent=2)

    print(f"Done: {len(results)} stories, {len(char_themes)} characters")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
