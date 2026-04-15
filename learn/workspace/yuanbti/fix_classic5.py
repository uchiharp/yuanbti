import json

with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 找到并替换第30题（sunce_classic_05）
for i, q in enumerate(questions):
    if q["id"] == "sunce_classic_05":
        questions[i] = {
            "id": "sunce_classic_05",
            "type": "classic",
            "dimension": ["S5", "S7"],
            "source_character": "孙策",
            "text": "孙策受伤后满不在乎地说'别担心我，我命硬'，继续战斗。",
            "options": [
                {
                    "label": "A",
                    "text": "劝他退下治疗，身体要紧",
                    "scores": {"S5": 1, "S7": 1},
                    "tendency": "L"
                },
                {
                    "label": "B",
                    "text": "为他包扎伤口，让他小心点",
                    "scores": {"S5": 3, "S7": 3},
                    "tendency": "M"
                },
                {
                    "label": "C",
                    "text": "说'我命也硬，我们一起战到底'",
                    "scores": {"S5": 5, "S7": 5},
                    "tendency": "H"
                }
            ],
            "reveal": "「你也经常一身的伤啊……别担心我，我命硬。」（围城）孙策受伤后先安慰你，展现武将的坚韧与担当。"
        }
        break

# 写回文件
with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Replaced classic_05 with '我命硬' scene")