# 任务计划：BWIKI 代号鸢剧情爬虫
创建时间：2026-04-12 21:46
总体状态：🔄 进行中

## 任务概览
| 轮次 | 模块 | 状态 | Agent | 备注 |
|------|------|------|-------|------|
| 0 | 基础框架 | ✅ 完成 | crawler-framework | API封装+断点续爬+解析器 |
| 1A | 密探相关 | ✅ 完成 | crawler-1A-mitan | 传唤239+故事1098+留音21+羁绊46=1404 |
| 1B | 剧情内容 | ✅ 完成 | crawler-1B-juqing | 主线150+活动366+恋念29=545 |
| 1C | 男主+鸢记 | ✅ 完成 | crawler-1C-nanzhu-yuanji | 花笺295+恋念之音223+约会63+鸢记52+留音11=644 |
| 2 | 数据清洗验证 | ✅ 完成 | crawler-2-validate | metadata+report |
| 3 | 最终报告 | ✅ 完成 | - | 已含在轮次2中 |

## 详细任务

### 轮次0: 基础框架
- 状态: 🔄 进行中
- 产出: `/Users/sunwenyong/.openclaw/agents/learn/workspace/bwiki-crawler/`
  - `config.py` — 配置（URL、延迟、UA、Referer）
  - `base.py` — MediaWiki API 封装（分页遍历、指数退避重试、进度保存）
  - `parser.py` — wikitext 内容解析器（dialogue/narration/choice 识别）
  - `main.py` — 入口脚本
- 技术要点:
  - 必须带 Referer + UA（BWIKI 反爬 567）
  - 指数退避：失败后 delay *= 2，初始 3s，最大 60s
  - 断点续爬：progress.json 记录已爬页面
  - 并发 ≤ 3
  - 随机延迟 1-3s
- 完成: -

### 轮次1A: 密探相关
- 状态: ⏳ 待开始
- 分类: 密探传唤(239) + 密探故事(500+有分页) + 密探留音(21) + 密探羁绊(46)
- 产出: `bwiki-crawler/密探/` 4个子目录
- 依赖: 轮次0 完成

### 轮次1B: 剧情内容
- 状态: ⏳ 待开始
- 分类: 主线剧情(150+有分页) + 活动剧情(366) + 恋念剧情(29)
- 产出: `bwiki-crawler/剧情/` 3个子目录
- 依赖: 轮次0 完成

### 轮次1C: 男主+鸢记
- 状态: ⏳ 待开始
- 分类: 红鸾花笺(295) + 恋念之音(223) + 约会(63) + 鸢记(52) + 男主留音(11，跳过字幕版)
- 产出: `bwiki-crawler/男主/` + `bwiki-crawler/鸢记/`
- 依赖: 轮次0 完成

### 轮次2: 数据清洗验证
- 状态: ⏳ 待开始
- 产出: `bwiki-crawler/metadata.json`
- 依赖: 轮次1 全部完成

### 轮次3: 最终报告
- 状态: ⏳ 待开始
- 产出: `bwiki-crawler/report.md`
- 依赖: 轮次2 完成

## 数据规模
- 总计 ~2000 页面
- BWIKI 基础 URL: https://wiki.biligame.com/yuan/
- API: MediaWiki API（需 Referer + UA）
- 男主留音通过 allpages 前缀匹配获取，不走分类
