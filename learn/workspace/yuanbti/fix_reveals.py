import json

with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 修复题目24 (sunce_daily_05)
for i, q in enumerate(questions):
    if q["id"] == "sunce_daily_05":
        q["reveal"] = "「把那套什么广陵王妃的礼服，照我的尺寸改改……」（剧情）孙策的求婚方式充满个人风格——直球、热烈、不带丝毫犹豫。"
        break

# 修复题目27 (sunce_classic_03)
for i, q in enumerate(questions):
    if q["id"] == "sunce_classic_03":
        q["reveal"] = "「连进二十支！牛不牛！投壶小意思，我投飞矛都没失过手！」（七夕欢情）七夕夜孙策带你玩遍所有摊子，战场猛将变约会笨蛋，每一面都真实可爱。"
        break

# 写回文件
with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Fixed 2 reveals")