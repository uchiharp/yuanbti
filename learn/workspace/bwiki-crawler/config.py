# -*- coding: utf-8 -*-
"""BWIKI（代号鸢）剧情爬虫 — 配置文件"""

# MediaWiki API 地址
BASE_URL = "https://wiki.biligame.com/yuan/api.php"

# 请求头（BWIKI 反爬必须携带，否则返回 567）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://wiki.biligame.com/yuan/",
    "Accept": "application/json",
}

# 请求延迟配置
MIN_DELAY = 1        # 最小延迟秒数
MAX_DELAY = 3        # 最大延迟秒数
MAX_CONCURRENT = 3   # 最大并发数

# 指数退避重试配置
RETRY_INITIAL_DELAY = 3   # 初始退避延迟（秒）
RETRY_MAX_DELAY = 60      # 最大退避延迟（秒）
RETRY_MAX_ATTEMPTS = 5    # 最大重试次数

# 输出目录
OUTPUT_DIR = "/Users/sunwenyong/.openclaw/agents/learn/workspace/bwiki-crawler"

# 进度文件路径
PROGRESS_FILE = "/Users/sunwenyong/.openclaw/agents/learn/workspace/bwiki-crawler/progress.json"

# 分类配置列表
CATEGORIES = [
    # 密探相关
    {"name": "密探传唤", "type": "category", "output": "密探/传唤"},
    {"name": "密探故事", "type": "category", "output": "密探/故事"},
    {"name": "密探留音", "type": "category", "output": "密探/留音"},
    {"name": "密探羁绊", "type": "category", "output": "密探/羁绊"},
    # 剧情内容
    {"name": "主线剧情", "type": "category", "output": "剧情/主线"},
    {"name": "活动剧情", "type": "category", "output": "剧情/活动"},
    {"name": "恋念剧情", "type": "category", "output": "剧情/恋念"},
    # 男主相关
    {"name": "红鸾花笺", "type": "category", "output": "男主/红鸾花笺"},
    {"name": "恋念之音", "type": "category", "output": "男主/恋念之音"},
    {"name": "约会", "type": "category", "output": "男主/约会"},
    {"name": "鸢记", "type": "category", "output": "鸢记"},
    # 男主留音 — 特殊处理（allpages 前缀匹配）
    {"name": "男主留音", "type": "allpages_prefix",
     "prefixes": ["刘辩-留音", "傅融-留音", "袁基-留音", "左慈-留音", "孙策-留音"],
     "output": "男主/留音"},
]

# 需要跳过的页面标题关键词
SKIP_KEYWORDS = ["字幕版"]
