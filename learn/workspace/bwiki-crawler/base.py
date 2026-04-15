# -*- coding: utf-8 -*-
"""BWIKI（代号鸢）剧情爬虫 — MediaWiki API 封装"""

import json
import time
import random
import os
from datetime import datetime
from urllib.parse import quote

import requests

from config import (
    BASE_URL, HEADERS, MIN_DELAY, MAX_DELAY,
    RETRY_INITIAL_DELAY, RETRY_MAX_DELAY, RETRY_MAX_ATTEMPTS,
    PROGRESS_FILE, SKIP_KEYWORDS,
)


# ── 进度管理 ──────────────────────────────────────────────

def load_progress():
    """读取进度文件，不存在则返回空结构"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": {}, "pages": {}, "stats": {
        "total_crawled": 0, "total_failed": 0,
        "failed_pages": [], "start_time": None, "last_update": None,
    }}


def save_progress(progress):
    """保存进度到文件"""
    progress["stats"]["last_update"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def mark_page_done(progress, title):
    """标记页面已完成"""
    progress["pages"][title] = {
        "status": "done",
        "crawled_at": datetime.now().isoformat(),
    }
    progress["stats"]["total_crawled"] += 1
    save_progress(progress)


def mark_page_failed(progress, title):
    """标记页面失败"""
    if title not in progress["stats"]["failed_pages"]:
        progress["stats"]["failed_pages"].append(title)
        progress["stats"]["total_failed"] += 1
    save_progress(progress)


# ── 请求层（指数退避 + 随机延迟）──────────────────────────

def _should_skip(title):
    """检查标题是否需要跳过"""
    for kw in SKIP_KEYWORDS:
        if kw in title:
            return True
    return False


def _api_get(params):
    """带指数退避的 API GET 请求，返回 JSON"""
    delay = RETRY_INITIAL_DELAY
    for attempt in range(1, RETRY_MAX_ATTEMPTS + 1):
        try:
            resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                # 成功后随机延迟
                time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                return data
            print(f"  ⚠ HTTP {resp.status_code} (尝试 {attempt}/{RETRY_MAX_ATTEMPTS})")
        except requests.RequestException as e:
            print(f"  ⚠ 请求异常: {e} (尝试 {attempt}/{RETRY_MAX_ATTEMPTS})")
        if attempt < RETRY_MAX_ATTEMPTS:
            print(f"  ⏳ {delay}s 后重试...")
            time.sleep(delay)
            delay = min(delay * 2, RETRY_MAX_DELAY)
    raise RuntimeError(f"API 请求失败，已重试 {RETRY_MAX_ATTEMPTS} 次")


# ── 核心 API 方法 ─────────────────────────────────────────

def fetch_category_members(category_name):
    """获取分类下所有页面标题（自动分页）"""
    titles = []
    cmcontinue = None
    print(f"📂 获取分类成员: {category_name}")
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category_name}",
            "cmlimit": 500,
            "format": "json",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        data = _api_get(params)
        members = data.get("query", {}).get("categorymembers", [])
        for m in members:
            title = m["title"]
            if not _should_skip(title):
                titles.append(title)
        # 检查是否还有下一页
        if "continue" in data and "cmcontinue" in data["continue"]:
            cmcontinue = data["continue"]["cmcontinue"]
        else:
            break
    print(f"  ✓ 共 {len(titles)} 个页面（已跳过字幕版）")
    return titles


def fetch_page_content(page_title):
    """获取单个页面的 wikitext 原始内容"""
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": page_title,
        "rvprop": "content",
        "rvlimit": 1,
        "format": "json",
    }
    data = _api_get(params)
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if "missing" in page:
            raise ValueError(f"页面不存在: {page_title}")
        revisions = page.get("revisions", [])
        if revisions:
            return revisions[0].get("*", "")
    raise ValueError(f"无法获取页面内容: {page_title}")


def fetch_allpages_prefix(prefix):
    """按前缀获取页面列表（用于男主留音等）"""
    titles = []
    apcontinue = None
    print(f"📂 按前缀获取页面: {prefix}")
    while True:
        params = {
            "action": "query",
            "list": "allpages",
            "apprefix": prefix,
            "aplimit": 500,
            "format": "json",
        }
        if apcontinue:
            params["apfrom"] = apcontinue
        data = _api_get(params)
        pages = data.get("query", {}).get("allpages", [])
        for p in pages:
            title = p["title"]
            if not _should_skip(title):
                titles.append(title)
        if "continue" in data and "apcontinue" in data["continue"]:
            apcontinue = data["continue"]["apcontinue"]
        else:
            break
    print(f"  ✓ 共 {len(titles)} 个页面")
    return titles
