#!/usr/bin/env python3
"""爬取剧情内容：主线剧情、活动剧情、恋念剧情"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
from config import OUTPUT_DIR
from base import fetch_category_members, fetch_page_content
from parser import parse_wikitext

categories = [
    {"name": "主线剧情", "output": "剧情/主线"},
    {"name": "活动剧情", "output": "剧情/活动"},
    {"name": "恋念剧情", "output": "剧情/恋念"},
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
            print("跳过（已存在）")
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

print("\n全部爬取完成！")
