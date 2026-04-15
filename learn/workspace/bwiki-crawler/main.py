#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BWIKI（代号鸢）剧情爬虫 — 入口脚本

用法:
    python3 main.py --category "密探传唤"   # 爬取单个分类
    python3 main.py --all                    # 爬取所有分类
    python3 main.py --status                 # 查看进度
    python3 main.py --resume                 # 继续上次中断的爬取
"""

import argparse
import json
import os
import sys
from urllib.parse import quote

from config import CATEGORIES, OUTPUT_DIR
from base import (
    fetch_category_members, fetch_page_content, fetch_allpages_prefix,
    load_progress, save_progress, mark_page_done, mark_page_failed,
)


def get_category_config(name):
    """根据分类名获取配置"""
    for cat in CATEGORIES:
        if cat["name"] == name:
            return cat
    return None


def crawl_category(cat_config, progress):
    """爬取单个分类"""
    cat_name = cat_config["name"]
    output_dir = os.path.join(OUTPUT_DIR, cat_config["output"])
    os.makedirs(output_dir, exist_ok=True)

    # 获取页面列表
    if cat_config["type"] == "allpages_prefix":
        all_titles = []
        for prefix in cat_config["prefixes"]:
            all_titles.extend(fetch_allpages_prefix(prefix))
    else:
        all_titles = fetch_category_members(cat_name)

    total = len(all_titles)
    if total == 0:
        print(f"⚠ 分类 {cat_name} 下没有页面")
        return

    # 统计已完成数量
    done_count = sum(1 for t in all_titles if progress["pages"].get(t, {}).get("status") == "done")
    print(f"📊 {cat_name}: 共 {total} 页，已完成 {done_count}，待爬 {total - done_count}")

    # 更新分类进度
    if cat_name not in progress["categories"]:
        progress["categories"][cat_name] = {"status": "in_progress", "total": total, "crawled": done_count}
    progress["categories"][cat_name]["total"] = total

    # 逐页爬取
    for i, title in enumerate(all_titles, 1):
        # 跳过已完成
        if progress["pages"].get(title, {}).get("status") == "done":
            continue

        print(f"  [{i}/{total}] 爬取: {title}")
        try:
            raw_text = fetch_page_content(title)
            # 解析内容
            from parser import parse_wikitext
            result = parse_wikitext(title, cat_name, raw_text)
            # 保存 JSON
            safe_name = quote(title, safe="")
            filepath = os.path.join(output_dir, f"{safe_name}.json")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            mark_page_done(progress, title)
            progress["categories"][cat_name]["crawled"] += 1
            progress["categories"][cat_name]["last_page"] = title
            print(f"    ✓ 已保存")
        except Exception as e:
            print(f"    ✗ 失败: {e}")
            mark_page_failed(progress, title)

    # 标记分类完成
    progress["categories"][cat_name]["status"] = "done"
    save_progress(progress)
    print(f"✅ 分类 {cat_name} 爬取完成！")


def show_status(progress):
    """显示当前进度"""
    print("=" * 50)
    print("📋 BWIKI 爬虫进度")
    print("=" * 50)

    stats = progress.get("stats", {})
    print(f"  总计已爬: {stats.get('total_crawled', 0)} 页")
    print(f"  失败: {stats.get('total_failed', 0)} 页")
    if stats.get("start_time"):
        print(f"  开始时间: {stats['start_time']}")
    if stats.get("last_update"):
        print(f"  最后更新: {stats['last_update']}")

    cats = progress.get("categories", {})
    if cats:
        print(f"\n📂 分类进度 ({len(cats)} 个):")
        for name, info in cats.items():
            status = info.get("status", "unknown")
            total = info.get("total", 0)
            crawled = info.get("crawled", 0)
            bar_len = 20
            filled = int(bar_len * crawled / total) if total > 0 else 0
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"  {name}: [{bar}] {crawled}/{total} ({status})")

    failed = stats.get("failed_pages", [])
    if failed:
        print(f"\n❌ 失败页面: {', '.join(failed)}")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="BWIKI（代号鸢）剧情爬虫")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--category", type=str, help="爬取指定分类")
    group.add_argument("--all", action="store_true", help="爬取所有分类")
    group.add_argument("--status", action="store_true", help="查看进度")
    group.add_argument("--resume", action="store_true", help="继续上次中断的爬取")
    args = parser.parse_args()

    progress = load_progress()

    # 初始化开始时间
    if progress["stats"]["start_time"] is None:
        from datetime import datetime
        progress["stats"]["start_time"] = datetime.now().isoformat()
        save_progress(progress)

    if args.status:
        show_status(progress)
        return

    if args.resume:
        # 继续所有 in_progress 的分类
        todo = [cat for cat in CATEGORIES
                if progress["categories"].get(cat["name"], {}).get("status") != "done"]
        if not todo:
            print("🎉 所有分类已爬取完成！")
            show_status(progress)
            return
        print(f"▶ 继续爬取 {len(todo)} 个未完成的分类")
        for cat in todo:
            crawl_category(cat, progress)
        show_status(progress)
        return

    if args.category:
        cat_config = get_category_config(args.category)
        if not cat_config:
            print(f"❌ 未知分类: {args.category}")
            print(f"可用分类: {', '.join(c['name'] for c in CATEGORIES)}")
            sys.exit(1)
        crawl_category(cat_config, progress)
        show_status(progress)
        return

    if args.all:
        print(f"🚀 开始全量爬取，共 {len(CATEGORIES)} 个分类")
        for cat in CATEGORIES:
            crawl_category(cat, progress)
        show_status(progress)
        return


if __name__ == "__main__":
    main()
