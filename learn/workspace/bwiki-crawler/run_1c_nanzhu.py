#!/usr/bin/env python3
"""爬取男主内容和鸢记"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
from config import OUTPUT_DIR
import base
import parser as parser_mod

# Re-export for convenience
fetch_category_members = base.fetch_category_members
fetch_page_content = base.fetch_page_content
fetch_allpages_prefix = base.fetch_allpages_prefix
parse_wikitext = parser_mod.parse_wikitext

# 分类爬取
categories = [
    {"name": "红鸾花笺", "output": "男主/红鸾花笺"},
    {"name": "恋念之音", "output": "男主/恋念之音"},
    {"name": "约会", "output": "男主/约会"},
    {"name": "鸢记", "output": "鸢记"},
]

for cat in categories:
    print(f"\n{'='*50}")
    print(f"开始爬取: {cat['name']}")
    print(f"{'='*50}")

    output_dir = os.path.join(OUTPUT_DIR, cat['output'])
    os.makedirs(output_dir, exist_ok=True)

    all_pages = fetch_category_members(cat['name'])
    print(f"共 {len(all_pages)} 个页面")

    success = 0
    failed = 0

    for i, title in enumerate(all_pages):
        print(f"  [{i+1}/{len(all_pages)}] {title}...", end=" ", flush=True)

        safe_name = title.replace("/", "_")
        json_file = os.path.join(output_dir, f"{safe_name}.json")
        if os.path.exists(json_file):
            print("跳过(已存在)")
            success += 1
            continue

        try:
            wikitext = fetch_page_content(title)
            if wikitext:
                parsed = parse_wikitext(title, cat['name'], wikitext)
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(parsed, f, ensure_ascii=False, indent=2)
                print("✅")
                success += 1
            else:
                print("⚠️ 无内容")
                failed += 1
        except Exception as e:
            print(f"❌ {e}")
            failed += 1

    print(f"\n{cat['name']} 完成: 成功 {success}, 失败 {failed}")

# 特殊处理:男主留音(allpages 前缀匹配)
print(f"\n{'='*50}")
print(f"开始爬取: 男主留音(前缀匹配)")
print(f"{'='*50}")

output_dir = os.path.join(OUTPUT_DIR, "男主/留音")
os.makedirs(output_dir, exist_ok=True)

prefixes = ["刘辩-留音", "傅融-留音", "袁基-留音", "左慈-留音", "孙策-留音"]
all_pages = []
for prefix in prefixes:
    pages = fetch_allpages_prefix(prefix)
    all_pages.extend(pages)

# 去重
all_pages = list(set(all_pages))
print(f"共 {len(all_pages)} 个页面(已去字幕版和去重)")

success = 0
failed = 0
for i, title in enumerate(all_pages):
    print(f"  [{i+1}/{len(all_pages)}] {title}...", end=" ", flush=True)

    safe_name = title.replace("/", "_")
    json_file = os.path.join(output_dir, f"{safe_name}.json")
    if os.path.exists(json_file):
        print("跳过(已存在)")
        success += 1
        continue

    try:
        wikitext = fetch_page_content(title)
        if wikitext:
            parsed = parse_wikitext(title, "男主留音", wikitext)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, ensure_ascii=False, indent=2)
            print("✅")
            success += 1
        else:
            print("⚠️ 无内容")
            failed += 1
    except Exception as e:
        print(f"❌ {e}")
        failed += 1

print(f"\n男主留音 完成: 成功 {success}, 失败 {failed}")
print("\n全部爬取完成!")
