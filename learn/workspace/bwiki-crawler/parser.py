# -*- coding: utf-8 -*-
"""BWIKI（代号鸢）剧情爬虫 — wikitext 解析器

将 wikitext 解析为结构化 JSON，提取对话、旁白、选项等内容。
"""

import re
from datetime import datetime
from urllib.parse import quote


# 需要跳过的非内容模板（BWIKI 自定义 UI 模板）
SKIP_TEMPLATES = {
    "板块", "折叠面板", "面包屑", "恋念背景", "JS", "CSS",
    "Template", "Infobox", "信息栏", "导航", "提示框",
    "切换显示", "tabs", "tab", "左侧目录", "右侧目录",
    "折叠", "展开", "引用", "参考", "ref", "note",
    "clear", "br", "hr", "navbox", "sidebar",
}


def parse_wikitext(title, category, raw_text):
    """解析 wikitext 为结构化字典

    Args:
        title: 页面标题
        category: 分类名
        raw_text: 原始 wikitext

    Returns:
        dict: 结构化 JSON
    """
    characters = set()
    content = []

    # 1. 先清理掉需要跳过的模板整行
    lines = raw_text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # 跳过非内容模板行（模板名匹配 SKIP_TEMPLATES）
        if _is_skip_template(stripped):
            continue
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)

    # 2. 提取对话模板: {{对话|角色名|对话内容}} 或 {{对话|角色名|表情|对话内容}}
    #    也兼容 {{D|角色|内容}} 等变体
    dialogue_pattern = re.compile(
        r"\{\{(?:对话|D|dialogue)\|([^|}]+)\|([^|}]*(?:\|[^|}]*)*)\}\}",
        re.IGNORECASE,
    )
    # 先收集对话位置，后续处理非对话内容
    dialogue_spans = []
    for m in dialogue_pattern.finditer(text):
        start, end = m.span()
        parts = m.group(2).split("|")
        speaker = m.group(1).strip()
        characters.add(speaker)
        if len(parts) >= 2:
            # 可能有表情描述
            emotion = parts[0].strip()
            dialog_text = parts[1].strip()
        else:
            emotion = ""
            dialog_text = parts[0].strip()
        dialogue_spans.append((start, end))
        content.append({
            "type": "dialogue",
            "speaker": speaker,
            "text": dialog_text,
            "emotion": emotion,
        })

    # 3. 提取选项: {{选项|选项A}} 或 {{选项|选项A|结果}}
    choice_pattern = re.compile(r"\{\{(?:选项|choice)\|([^|}]+)(?:\|([^|}]*))?\}\}", re.IGNORECASE)
    for m in choice_pattern.finditer(text):
        opt_text = m.group(1).strip()
        opt_result = m.group(2).strip() if m.group(2) else ""
        content.append({
            "type": "choice",
            "options": [{"text": opt_text, "result": opt_result}],
        })

    # 4. 提取表情/动作模板: {{表情|描述}} 或 {{动作|描述}}
    emotion_pattern = re.compile(r"\{\{(?:表情|动作|emotion|action)\|([^}]+)\}\}", re.IGNORECASE)

    # 5. 提取旁白：去掉所有模板后的纯文本段落
    #    去掉所有 {{...}} 和 [[...]] 标记后，取有意义的文本行
    text_no_templates = re.sub(r"\{\{[^}]*\}\}", "", text)
    text_no_links = re.sub(r"\[\[([^|\]]*\|)?([^\]]*)\]\]", r"\2", text_no_templates)
    # 提取有内容的文本行作为旁白
    for line in text_no_links.split("\n"):
        line = line.strip()
        if not line:
            continue
        # 跳过纯标记行（如 ----、===标题===、*列表项 但保留有内容的）
        if re.match(r"^-{3,}$", line):
            continue
        # 跳过只有特殊字符的行
        clean = re.sub(r"[=\-#*:|{}\[\]<>]", "", line).strip()
        if len(clean) < 2:
            continue
        content.append({"type": "narration", "text": clean})

    # 如果没有任何解析内容，保留原始文本
    if not content:
        content.append({"type": "raw", "text": raw_text[:500]})

    return {
        "title": title,
        "category": category,
        "characters": sorted(characters),
        "content": content,
        "source_url": f"https://wiki.biligame.com/yuan/{quote(title)}",
        "crawled_at": datetime.now().isoformat(),
        "raw_wikitext": raw_text,
    }


def _is_skip_template(line):
    """判断一行是否是应该跳过的非内容模板"""
    # 匹配 {{模板名|... 的模式
    m = re.match(r"^\{\{([^|}:]+)", line)
    if not m:
        return False
    tpl_name = m.group(1).strip()
    # 精确匹配
    if tpl_name in SKIP_TEMPLATES:
        return True
    # 前缀匹配（如 板块:xxx）
    for skip in SKIP_TEMPLATES:
        if tpl_name.startswith(skip + ":") or tpl_name.startswith(skip + "/"):
            return True
    return False
