import json

# 读取现有题目
with open('questions/zuoci.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 定义funny批次题目
funny_questions = [
    {
        "id": "zuoci_funny_01",
        "type": "funny",
        "dimension": ["S3", "S7"],
        "source_character": "左慈",
        "text": "左慈对你说：'投壶投进十支能得到奖品……好。'",
        "options": [
            {"label": "A", "text": "无奈地叹气。", "scores": {"S3": 1, "S7": 1}, "tendency": "L"},
            {"label": "B", "text": "笑着说：'师尊，我们还是去别处吧。'", "scores": {"S3": 3, "S7": 3}, "tendency": "M"},
            {"label": "C", "text": "跟着一起捣乱：'再加点风！'", "scores": {"S3": 5, "S7": 5}, "tendency": "H"}
        ],
        "reveal": "出自『七夕欢情·左慈/活动剧情』。左慈说：'投壶投进十支能得到奖品……好。'"
    },
    {
        "id": "zuoci_funny_02",
        "type": "funny",
        "dimension": ["S4", "S5"],
        "source_character": "左慈",
        "text": "左慈对你说：'十支，十支，十支……嗯？老板为什么掀桌了？'",
        "options": [
            {"label": "A", "text": "拉着他赶紧离开。", "scores": {"S4": 1, "S5": 1}, "tendency": "L"},
            {"label": "B", "text": "笑着打圆场：'老板别生气，我们这就走。'", "scores": {"S4": 3, "S5": 3}, "tendency": "M"},
            {"label": "C", "text": "也跟着拍桌子：'凭什么掀桌！'", "scores": {"S4": 5, "S5": 5}, "tendency": "H"}
        ],
        "reveal": "出自『七夕欢情·左慈/活动剧情』。左慈说：'十支，十支，十支……嗯？老板为什么掀桌了？'"
    },
    {
        "id": "zuoci_funny_03",
        "type": "funny",
        "dimension": ["S3", "S7"],
        "source_character": "左慈",
        "text": "左慈对你说：'不能用仙术操控箭直接进壶？可是规则上没写……'",
        "options": [
            {"label": "A", "text": "小声提醒：'师尊，这样作弊不好。'", "scores": {"S3": 1, "S7": 1}, "tendency": "L"},
            {"label": "B", "text": "无奈地笑：'规则是没写，但也不能这样。'", "scores": {"S3": 3, "S7": 3}, "tendency": "M"},
            {"label": "C", "text": "帮腔：'对！规则没写就可以！'", "scores": {"S3": 5, "S7": 5}, "tendency": "H"}
        ],
        "reveal": "出自『七夕欢情·左慈/活动剧情』。左慈说：'不能用仙术操控箭直接进壶？可是规则上没写……'"
    },
    {
        "id": "zuoci_funny_04",
        "type": "funny",
        "dimension": ["S4", "S5"],
        "source_character": "左慈",
        "text": "左慈对你说：'风伯，召来……呃，不小心把摊主吹走了……'",
        "options": [
            {"label": "A", "text": "赶紧去找摊主道歉。", "scores": {"S4": 1, "S5": 1}, "tendency": "L"},
            {"label": "B", "text": "哭笑不得：'师尊，你闯祸了。'", "scores": {"S4": 3, "S5": 3}, "tendency": "M"},
            {"label": "C", "text": "大笑：'吹得好！我们再吹一次！'", "scores": {"S4": 5, "S5": 5}, "tendency": "H"}
        ],
        "reveal": "出自『七夕欢情·左慈/活动剧情』。左慈说：'风伯，召来……呃，不小心把摊主吹走了……'"
    },
    {
        "id": "zuoci_funny_05",
        "type": "funny",
        "dimension": ["S3", "S7"],
        "source_character": "左慈",
        "text": "左慈对你说：'菜牌上居然有那么多字……正常冰，去冰，常温，温热，热……全糖，半糖，无糖……'",
        "options": [
            {"label": "A", "text": "帮他选一个最普通的。", "scores": {"S3": 1, "S7": 1}, "tendency": "L"},
            {"label": "B", "text": "笑着解释：'这是现在流行的喝法。'", "scores": {"S3": 3, "S7": 3}, "tendency": "M"},
            {"label": "C", "text": "逗他：'每个口味都来一杯！'", "scores": {"S3": 5, "S7": 5}, "tendency": "H"}
        ],
        "reveal": "出自『七夕欢情·左慈/活动剧情』。左慈说：'菜牌上居然有那么多字……正常冰，去冰，常温，温热，热……全糖，半糖，无糖……'"
    }
]

# 追加
data.extend(funny_questions)

# 写回
with open('questions/zuoci.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"已追加 {len(funny_questions)} 道funny题目，现在共有 {len(data)} 道题")