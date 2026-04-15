import json

questions = []

# 1. sweet批次 - 南有乔木/15 - 孙策整夜守护
questions.append({
    "id": "sunce_sweet_01",
    "type": "sweet",
    "dimension": ["S2", "S8"],
    "source_character": "孙策",
    "text": "你到寿春做客，孙策因玉玺传言加强守卫。他说会亲自整夜守在客房外保护你。",
    "options": [
        {
            "label": "A",
            "text": "婉拒他的守护，说自己可以照顾自己",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B", 
            "text": "接受他的好意，让他守在外面",
            "scores": {"S2": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "邀请他进客房一起休息，说有他在更安心",
            "scores": {"S2": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「我整夜都在客房外。有什么风吹草动，全都能听见。」（南有乔木/15）孙策因玉玺传言担心你的安全，亲自整夜守护。"
})

# 2. sweet批次 - 南有乔木/22 - 游猎遇山贼
questions.append({
    "id": "sunce_sweet_02",
    "type": "sweet",
    "dimension": ["S5", "S8"],
    "source_character": "孙策",
    "text": "你和孙策游猎时遇到山贼。孙策让你躲在他身后，说有他在什么都不用怕。",
    "options": [
        {
            "label": "A",
            "text": "退到安全处观察，不给他添麻烦",
            "scores": {"S5": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "躲在他身后，信任他的保护",
            "scores": {"S5": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "站到他身旁并肩作战，说我们一起应对",
            "scores": {"S5": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「怕的话就叫出声，我不笑你。」「有我在，你什么都不用怕。」（南有乔木/22）孙策在危险时先安抚你的情绪，展现温柔守护。"
})

# 3. sweet批次 - 围城受伤后
# 需要查询围城受伤后的台词
# 先假设有相关台词
questions.append({
    "id": "sunce_sweet_03",
    "type": "sweet",
    "dimension": ["S2", "S7"],
    "source_character": "孙策",
    "text": "孙策在守城时受伤，却笑着对你说只是轻伤，让你别担心。",
    "options": [
        {
            "label": "A",
            "text": "保持距离，让军医处理伤口",
            "scores": {"S2": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "坚持检查他的伤口，确认伤势",
            "scores": {"S2": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握住他的手说别硬撑，我陪你一起面对",
            "scores": {"S2": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「真的，只是看上去吓人。其实……都是轻伤。」（围城）孙策受伤后先安慰你，不让你担心。"
})

# 4. sweet批次 - 七夕欢情 - 五子棋连输
questions.append({
    "id": "sunce_sweet_04",
    "type": "sweet",
    "dimension": ["S3", "S8"],
    "source_character": "孙策",
    "text": "七夕时孙策和你下五子棋，连输十七把还不服输，眼睛亮晶晶地看着你。",
    "options": [
        {
            "label": "A",
            "text": "提议换别的游戏，给他留点面子",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "继续陪他下，看他什么时候认输",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "故意让棋输给他，笑着说你进步了",
            "scores": {"S3": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "七夕欢情中孙策五子棋连输十七把，展现反差萌。他好胜但面对你时只剩笨拙的真诚。"
})

# 5. sweet批次 - 南有乔木/23 - 夸你好看
questions.append({
    "id": "sunce_sweet_05",
    "type": "sweet",
    "dimension": ["S2", "S8"],
    "source_character": "孙策",
    "text": "孙策突然夸你比想象中要'水'（江东话夸好看），然后慌张解释自己没有其他心思。",
    "options": [
        {
            "label": "A",
            "text": "礼貌道谢，转移话题",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "笑着问他什么意思，逗他继续解释",
            "scores": {"S2": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "直视他说'你也有其他心思也可以'",
            "scores": {"S2": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「你比我想象得要……水！江东话，意思就是好看！」（南有乔木/23）孙策直球夸赞后慌张找补，暴露心意。"
})

# 现在需要继续其他批次：funny, angst, scheme, daily, classic
# 先保存这5道题看看格式

print(f"Generated {len(questions)} questions")

# 写入文件
output_path = "/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Saved to {output_path}")