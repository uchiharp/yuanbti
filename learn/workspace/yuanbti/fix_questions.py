import json

# 读取现有文件
with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 修改第23题（原日常守护细节）改为"揉耳垂烫了摸耳垂就好"场景
for i, q in enumerate(questions):
    if q["id"] == "sunce_daily_03":
        q["text"] = "你被烫到，孙策教你'揉着我耳垂，烫了摸耳垂就好'，然后自然地伸手帮你揉耳垂。"
        q["options"] = [
            {
                "label": "A",
                "text": "避开他的手，说自己来",
                "scores": {"S5": 1, "S8": 1},
                "tendency": "L"
            },
            {
                "label": "B",
                "text": "让他揉，说这个方法真有用",
                "scores": {"S5": 3, "S8": 3},
                "tendency": "M"
            },
            {
                "label": "C",
                "text": "也伸手揉他的耳垂，说'互相帮忙'",
                "scores": {"S5": 5, "S8": 5},
                "tendency": "H"
            }
        ]
        q["reveal"] = "「揉着我耳垂，烫了摸耳垂就好。」（剧情）孙策用江东土方帮你缓解烫伤，动作自然亲昵。"
        break

# 修改第24题（笨拙照顾）改为"你肩上的伤重不重？要不要试试我军中的伤药？"场景
for i, q in enumerate(questions):
    if q["id"] == "sunce_daily_04":
        q["text"] = "孙策注意到你肩上有伤，说'你肩上的伤重不重？要不要试试我军中的伤药？'"
        q["options"] = [
            {
                "label": "A",
                "text": "婉拒说不用，伤不重",
                "scores": {"S3": 1, "S8": 1},
                "tendency": "L"
            },
            {
                "label": "B",
                "text": "接受他的伤药，让他帮忙敷",
                "scores": {"S3": 3, "S8": 3},
                "tendency": "M"
            },
            {
                "label": "C",
                "text": "说'你帮我敷药，我也帮你检查有没有伤'",
                "scores": {"S3": 5, "S8": 5},
                "tendency": "H"
            }
        ]
        q["reveal"] = "「你肩上的伤重不重？要不要试试我军中的伤药？」（剧情）孙策细心注意到你的伤势，主动提供帮助。"
        break

# 写回文件
with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Fixed 2 questions")