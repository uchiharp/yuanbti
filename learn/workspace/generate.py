import json

questions = []

# 批次1: sweet
questions.append({
    "id": "furong_sweet_1",
    "type": "sweet",
    "dimension": ["S2", "S8"],
    "source_character": "傅融",
    "text": "傅融嘴上说飞云是狗，却总是偷偷照顾它。今天飞云又弄脏了你的文书，傅融一边抱怨一边收拾。",
    "options": [
        {
            "label": "A",
            "text": "笑着说“飞云真是调皮，下次不许了”",
            "scores": {"S2": 3, "S8": 5},
            "tendency": "L",
            "reasoning": "用笑声表达对宠物的宽容，语气温柔，情感表达中等（S2:3），温柔程度高（S8:5）。"
        },
        {
            "label": "B",
            "text": "摸摸飞云的头，帮傅融一起收拾",
            "scores": {"S2": 5, "S8": 3},
            "tendency": "M",
            "reasoning": "通过肢体接触和帮忙表达强烈情感（S2:5），行动务实，温柔程度中等（S8:3）。"
        },
        {
            "label": "C",
            "text": "严肃地说“傅融，你太宠它了”",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "H",
            "reasoning": "聚焦纪律而非情感，语气严肃，缺乏情感表达（S2:1）和温柔（S8:1）。"
        }
    ],
    "reveal": "傅融曾说：“飞云今天立功了，我放它遛一圈，待会儿回去。” 他嘴上嫌弃，行动上却总是纵容飞云，典型的嘴硬心软。"
})

questions.append({
    "id": "furong_sweet_2",
    "type": "sweet",
    "dimension": ["S2", "S4"],
    "source_character": "傅融",
    "text": "七夕夜，傅融和你一起看烟花，他的护手不小心勾住了你的袖子。",
    "options": [
        {
            "label": "A",
            "text": "假装没发现，继续看烟花",
            "scores": {"S2": 1, "S4": 3},
            "tendency": "L",
            "reasoning": "回避情感互动，情感表达低（S2:1），维持表面平静（S4:3）。"
        },
        {
            "label": "B",
            "text": "轻轻把袖子抽出来，笑着说“勾住了”",
            "scores": {"S2": 3, "S4": 5},
            "tendency": "M",
            "reasoning": "自然处理尴尬，中等情感表达（S2:3），用笑容掩饰内心（S4:5）。"
        },
        {
            "label": "C",
            "text": "反手握住他的手，说“这样就不会勾住了”",
            "scores": {"S2": 5, "S4": 1},
            "tendency": "H",
            "reasoning": "主动亲密接触，情感表达高（S2:5），直接打破距离感（S4:1）。"
        }
    ],
    "reveal": "傅融在夜晈既明中说：“……就是护手勾住了袖子！” 他表面冷静，实则可能心跳加速，用抱怨掩饰羞涩。"
})

questions.append({
    "id": "furong_sweet_3",
    "type": "sweet",
    "dimension": ["S3", "S8"],
    "source_character": "傅融",
    "text": "你生病卧床，傅融来汇报公务，一边说一边帮你整理被角。",
    "options": [
        {
            "label": "A",
            "text": "让他继续汇报，自己闭目养神",
            "scores": {"S3": 5, "S8": 1},
            "tendency": "L",
            "reasoning": "优先公务，务实高效（S3:5），但忽略温柔互动（S8:1）。"
        },
        {
            "label": "B",
            "text": "打断他，说“这些事不急，你先休息会儿”",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M",
            "reasoning": "平衡工作与关心，中等务实（S3:3）和中等温柔（S8:3）。"
        },
        {
            "label": "C",
            "text": "拉住他的手，说“别说了，陪我躺一会儿”",
            "scores": {"S3": 1, "S8": 5},
            "tendency": "H",
            "reasoning": "完全转向亲密，放弃工作（S3:1），温柔体贴高（S8:5）。"
        }
    ],
    "reveal": "傅融在宠爱中说：“想睡就往后靠，闭目休息一会。” 他即使在汇报公务时也不忘关心你的身体。"
})

questions.append({
    "id": "furong_sweet_4",
    "type": "sweet",
    "dimension": ["S5", "S2"],
    "source_character": "傅融",
    "text": "雪山上，傅融躺在雪地里说“雪能生百谷”，邀请你一起躺下。",
    "options": [
        {
            "label": "A",
            "text": "拒绝，说“太冷了，快起来”",
            "scores": {"S5": 1, "S2": 1},
            "tendency": "L",
            "reasoning": "拒绝互动，行动力低（S5:1），情感表达低（S2:1）。"
        },
        {
            "label": "B",
            "text": "在他身边坐下，但不躺下",
            "scores": {"S5": 3, "S2": 3},
            "tendency": "M",
            "reasoning": "部分参与，行动力中等（S5:3），情感表达中等（S2:3）。"
        },
        {
            "label": "C",
            "text": "直接躺在他旁边，握住他的手",
            "scores": {"S5": 5, "S2": 5},
            "tendency": "H",
            "reasoning": "完全投入，行动力高（S5:5），情感表达高（S2:5）。"
        }
    ],
    "reveal": "傅融在密会中说：“雪能生百谷。我现在拿雪埋住自己，明年开春，说不定能长出许多的五铢钱。” 他用玩笑掩饰浪漫。"
})

questions.append({
    "id": "furong_sweet_5",
    "type": "sweet",
    "dimension": ["S6", "S2"],
    "source_character": "傅融",
    "text": "高粱地里，傅融被你按在秸秆堆上，他轻声说“开弓没有回头箭”。",
    "options": [
        {
            "label": "A",
            "text": "松开他，说“我开玩笑的”",
            "scores": {"S6": 5, "S2": 1},
            "tendency": "L",
            "reasoning": "守住底线，停止冒险（S6:5），但情感表达退缩（S2:1）。"
        },
        {
            "label": "B",
            "text": "继续压着他，但问“你怕了吗？”",
            "scores": {"S6": 3, "S2": 3},
            "tendency": "M",
            "reasoning": "维持暧昧，底线中等（S6:3），情感表达中等（S2:3）。"
        },
        {
            "label": "C",
            "text": "吻他，说“那就不回头了”",
            "scores": {"S6": 1, "S2": 5},
            "tendency": "H",
            "reasoning": "突破底线，大胆行动（S6:1），情感表达高（S2:5）。"
        }
    ],
    "reveal": "傅融在高粱地说：“开弓没有回头箭……我赌是我。” 他在亲密时刻仍带着赌徒般的决心。"
})

# 批次2: funny (5题)
questions.append({
    "id": "furong_funny_1",
    "type": "funny",
    "dimension": ["S7", "S4"],
    "source_character": "傅融",
    "text": "傅融和你在闹鬼的司马吉堡探险，他被游魂吓得大叫。",
    "options": [
        {
            "label": "A",
            "text": "躲到他身后，说“我好怕”",
            "scores": {"S7": 1, "S4": 5},
            "tendency": "L",
            "reasoning": "展现脆弱，锋芒低（S7:1），用伪装掩饰真实胆量（S4:5）。"
        },
        {
            "label": "B",
            "text": "拉着他往前冲，说“都是假的，快走”",
            "scores": {"S7": 3, "S4": 3},
            "tendency": "M",
            "reasoning": "带头行动，中等锋芒（S7:3），中等掩饰（S4:3）。"
        },
        {
            "label": "C",
            "text": "故意学鬼叫，吓唬他",
            "scores": {"S7": 5, "S4": 1},
            "tendency": "H",
            "reasoning": "主动挑衅，锋芒高（S7:5），毫不掩饰恶作剧（S4:1）。"
        }
    ],
    "reveal": "傅融在双魂成行中说：“你看真的有鬼啊！这跟我那套凶宅的情况完全不是一个级别啊！” 他怕鬼的样子反差很大。"
})

questions.append({
    "id": "furong_funny_2",
    "type": "funny",
    "dimension": ["S3", "S7"],
    "source_character": "傅融",
    "text": "傅融和醋老头吵架，回来跟你抱怨老头脾气差。",
    "options": [
        {
            "label": "A",
            "text": "安慰他“别跟老人家计较”",
            "scores": {"S3": 1, "S7": 1},
            "tendency": "L",
            "reasoning": "回避冲突，务实低（S3:1），锋芒低（S7:1）。"
        },
        {
            "label": "B",
            "text": "提议“下次我陪你去，帮你吵”",
            "scores": {"S3": 3, "S7": 3},
            "tendency": "M",
            "reasoning": "实用支持，中等务实（S3:3），中等锋芒（S7:3）。"
        },
        {
            "label": "C",
            "text": "大笑“原来傅副官吵架也会输”",
            "scores": {"S3": 5, "S7": 5},
            "tendency": "H",
            "reasoning": "直面问题（务实高，S3:5），锋芒高（S7:5）地调侃他。"
        }
    ],
    "reveal": "傅融在夜晈既明中说：“醋老头脾气很差的，会对着我们的背影骂娘，回家都还能听见他骂娘的声音。” 他无奈又好笑。"
})

questions.append({
    "id": "furong_funny_3",
    "type": "funny",
    "dimension": ["S5", "S10"],
    "source_character": "傅融",
    "text": "傅融滑雪失控摔进雪坑，脑袋砸出一个人形。",
    "options": [
        {
            "label": "A",
            "text": "赶紧拉他出来，检查伤势",
            "scores": {"S5": 5, "S10": 3},
            "tendency": "L",
            "reasoning": "快速行动救助（S5:5），维持秩序（S10:3）。"
        },
        {
            "label": "B",
            "text": "笑他“好像个萝卜”，拍照留念",
            "scores": {"S5": 3, "S10": 1},
            "tendency": "M",
            "reasoning": "行动中等（S5:3），打破秩序开玩笑（S10:1）。"
        },
        {
            "label": "C",
            "text": "自己也跳进坑里，说“对称了”",
            "scores": {"S5": 1, "S10": 5},
            "tendency": "H",
            "reasoning": "行动力低（S5:1），但追求对称秩序（S10:5）。"
        }
    ],
    "reveal": "傅融在密会中说：“哈哈哈……我们的脑袋拔出了两个坑！” 他即使摔倒也能苦中作乐。"
})

questions.append({
    "id": "furong_funny_4",
    "type": "funny",
    "dimension": ["S3", "S9"],
    "source_character": "傅融",
    "text": "傅融推销小毛驴，说它“吃得少，成本低，可亲可爱”。",
    "options": [
        {
            "label": "A",
            "text": "认真考虑买驴，问价钱",
            "scores": {"S3": 5, "S9": 1},
            "tendency": "L",
            "reasoning": "务实考量（S3:5），不争夺主导权（S9:1）。"
        },
        {
            "label": "B",
            "text": "开玩笑“那你和驴谁更划算”",
            "scores": {"S3": 3, "S9": 3},
            "tendency": "M",
            "reasoning": "中等务实（S3:3），中等权力调侃（S9:3）。"
        },
        {
            "label": "C",
            "text": "说“不买，我要你驮我”",
            "scores": {"S3": 1, "S9": 5},
            "tendency": "H",
            "reasoning": "不务实（S3:1），但掌握主导权（S9:5）。"
        }
    ],
    "reveal": "傅融在回乡的诱惑中说：“你看，驴，既能通勤，又能下地；吃得少，成本低。吃苦耐劳，可亲可爱。” 他连推销都带着精打细算。"
})

questions.append({
    "id": "furong_funny_5",
    "type": "funny",
    "dimension": ["S8", "S10"],
    "source_character": "傅融",
    "text": "傅融教飞云背诗，说“回去就开始背《急就篇》，明年送去辟雍读《大学》”。",
    "options": [
        {
            "label": "A",
            "text": "附和“好，让它考个状元”",
            "scores": {"S8": 3, "S10": 5},
            "tendency": "L",
            "reasoning": "温柔附和（S8:3），强调秩序规则（S10:5）。"
        },
        {
            "label": "B",
            "text": "吐槽“飞云是狗，读什么书”",
            "scores": {"S8": 1, "S10": 3},
            "tendency": "M",
            "reasoning": "不够温柔（S8:1），中等秩序感（S10:3）。"
        },
        {
            "label": "C",
            "text": "抱起飞云说“别听他的，玩最重要”",
            "scores": {"S8": 5, "S10": 1},
            "tendency": "H",
            "reasoning": "温柔宠溺（S8:5），打破秩序（S10:1）。"
        }
    ],
    "reveal": "傅融在宠爱中说：“给你买了那么多玩具，回去就开始背《急就篇》，明年送去辟雍读《大学》。” 他对飞云有种望子成龙的执着。"
})

# 批次3: angst (5题)
questions.append({
    "id": "furong_angst_1",
    "type": "angst",
    "dimension": ["S2", "S6"],
    "source_character": "傅融",
    "text": "傅融重伤，你说要带他回去，他低声说“还不如上一次……至少……没被你看见这副样子”。",
    "options": [
        {
            "label": "A",
            "text": "握紧他的手，说“我背你回去”",
            "scores": {"S2": 5, "S6": 3},
            "tendency": "L",
            "reasoning": "强烈情感支持（S2:5），底线中等（坚持救助）（S6:3）。"
        },
        {
            "label": "B",
            "text": "轻声说“别说了，保存体力”",
            "scores": {"S2": 3, "S6": 5},
            "tendency": "M",
            "reasoning": "中等情感表达（S2:3），底线高（优先生存）（S6:5）。"
        },
        {
            "label": "C",
            "text": "吻他的额头，说“我看见了，很美”",
            "scores": {"S2": 1, "S6": 1},
            "tendency": "H",
            "reasoning": "情感表达偏离（S2:1），底线低（忽略伤势）（S6:1）。"
        }
    ],
    "reveal": "傅融在丹书白马/25中说：“还不如上一次……至少……没被你看见这副样子。” 他不想让你看到他脆弱的样子。"
})

questions.append({
    "id": "furong_angst_2",
    "type": "angst",
    "dimension": ["S1", "S2"],
    "source_character": "傅融",
    "text": "城楼夜谈，傅融问你“你打算这样，到什么时候？”，指的是你女扮男装的身份。",
    "options": [
        {
            "label": "A",
            "text": "反问“你呢？打算什么时候离开绣衣楼？”",
            "scores": {"S1": 5, "S2": 1},
            "tendency": "L",
            "reasoning": "权谋反击（S1:5），情感表达低（S2:1）。"
        },
        {
            "label": "B",
            "text": "沉默片刻，说“不知道”",
            "scores": {"S1": 3, "S2": 3},
            "tendency": "M",
            "reasoning": "中等权谋（不暴露）（S1:3），中等情感（S2:3）。"
        },
        {
            "label": "C",
            "text": "握住他的手，说“直到你陪我走下去”",
            "scores": {"S1": 1, "S2": 5},
            "tendency": "H",
            "reasoning": "权谋低（S1:1），情感表达高（S2:5）。"
        }
    ],
    "reveal": "傅融在城楼夜谈中说：“今夜想问你，你打算这样，到什么时候？” 这是他罕见的直白关心。"
})

questions.append({
    "id": "furong_angst_3",
    "type": "angst",
    "dimension": ["S5", "S9"],
    "source_character": "傅融",
    "text": "傅融必须执行一项危险任务，可能一去不回。",
    "options": [
        {
            "label": "A",
            "text": "命令他不准去，派别人去",
            "scores": {"S5": 1, "S9": 5},
            "tendency": "L",
            "reasoning": "行动力低（阻止）（S5:1），权力高（S9:5）。"
        },
        {
            "label": "B",
            "text": "说“我跟你一起去”",
            "scores": {"S5": 5, "S9": 3},
            "tendency": "M",
            "reasoning": "行动力高（S5:5），权力中等（分享决策）（S9:3）。"
        },
        {
            "label": "C",
            "text": "拥抱他，说“我等你回来”",
            "scores": {"S5": 3, "S9": 1},
            "tendency": "H",
            "reasoning": "行动力中等（S5:3），权力低（S9:1）。"
        }
    ],
    "reveal": "傅融在任务前曾说：“保证过……会陪你……走下去的……” 他即使赴死也会记得承诺。"
})

questions.append({
    "id": "furong_angst_4",
    "type": "angst",
    "dimension": ["S4", "S6"],
    "source_character": "傅融",
    "text": "傅融发现你的真实身份可能带来灾祸，他独自在院子里呆坐。",
    "options": [
        {
            "label": "A",
            "text": "走过去，默默坐在他身边",
            "scores": {"S4": 5, "S6": 3},
            "tendency": "L",
            "reasoning": "面具高（不捅破）（S4:5），底线中等（陪伴）（S6:3）。"
        },
        {
            "label": "B",
            "text": "直接问“你在想什么？”",
            "scores": {"S4": 3, "S6": 5},
            "tendency": "M",
            "reasoning": "中等面具（S4:3），底线高（直面问题）（S6:5）。"
        },
        {
            "label": "C",
            "text": "从背后抱住他，什么也不说",
            "scores": {"S4": 1, "S6": 1},
            "tendency": "H",
            "reasoning": "面具低（身体接触）（S4:1），底线低（回避问题）（S6:1）。"
        }
    ],
    "reveal": "傅融有时会独处思考，他说过：“有时候忙完了，会来这一待会儿。” 他有自己的心事。"
})

questions.append({
    "id": "furong_angst_5",
    "type": "angst",
    "dimension": ["S3", "S10"],
    "source_character": "傅融",
    "text": "傅融为了救你，不得不违反绣衣楼的规矩。",
    "options": [
        {
            "label": "A",
            "text": "事后帮他补全手续，掩盖过去",
            "scores": {"S3": 5, "S10": 1},
            "tendency": "L",
            "reasoning": "务实高效（S3:5），秩序低（S10:1）。"
        },
        {
            "label": "B",
            "text": "主动向上级坦白，承担责任",
            "scores": {"S3": 3, "S10": 5},
            "tendency": "M",
            "reasoning": "中等务实（S3:3），秩序高（S10:5）。"
        },
        {
            "label": "C",
            "text": "说“规矩不重要，你最重要”",
            "scores": {"S3": 1, "S10": 3},
            "tendency": "H",
            "reasoning": "务实低（S3:1），秩序中等（S10:3）。"
        }
    ],
    "reveal": "傅融曾说：“已经中计，现在撤退也来不及了。” 他在危急时刻会做出务实选择。"
})

# 批次4: scheme (5题)
questions.append({
    "id": "furong_scheme_1",
    "type": "scheme",
    "dimension": ["S1", "S5"],
    "source_character": "傅融",
    "text": "曹操诱敌，傅融冷静分析局势，说“已经中计，现在撤退也来不及了”。",
    "options": [
        {
            "label": "A",
            "text": "听从他的建议，立即调整战术",
            "scores": {"S1": 3, "S5": 5},
            "tendency": "L",
            "reasoning": "权谋中等（采纳）（S1:3），行动力高（S5:5）。"
        },
        {
            "label": "B",
            "text": "质疑“你有几成把握？”",
            "scores": {"S1": 5, "S5": 3},
            "tendency": "M",
            "reasoning": "权谋高（谨慎）（S1:5），行动力中等（S5:3）。"
        },
        {
            "label": "C",
            "text": "说“不管了，直接突围”",
            "scores": {"S1": 1, "S5": 1},
            "tendency": "H",
            "reasoning": "权谋低（S1:1），行动力低（鲁莽）（S5:1）。"
        }
    ],
    "reveal": "傅融在丹书白马/07中说：“已经中计，现在撤退也来不及了。” 他能在危机中保持冷静分析。"
})

questions.append({
    "id": "furong_scheme_2",
    "type": "scheme",
    "dimension": ["S9", "S10"],
    "source_character": "傅融",
    "text": "绣衣楼内部出现分歧，傅融需要决定支持哪一方。",
    "options": [
        {
            "label": "A",
            "text": "支持实力更强的一方",
            "scores": {"S9": 5, "S10": 3},
            "tendency": "L",
            "reasoning": "权力倾向明显（S9:5），秩序中等（S10:3）。"
        },
        {
            "label": "B",
            "text": "保持中立，调解矛盾",
            "scores": {"S9": 3, "S10": 5},
            "tendency": "M",
            "reasoning": "权力中等（S9:3），秩序高（S10:5）。"
        },
        {
            "label": "C",
            "text": "支持你个人倾向的一方",
            "scores": {"S9": 1, "S10": 1},
            "tendency": "H",
            "reasoning": "权力低（随性）（S9:1），秩序低（S10:1）。"
        }
    ],
    "reveal": "傅融作为校尉，需要在权力和秩序之间找到平衡。"
})

questions.append({
    "id": "furong_scheme_3",
    "type": "scheme",
    "dimension": ["S3", "S6"],
    "source_character": "傅融",
    "text": "傅融处理财务报销，发现一笔可疑账目。",
    "options": [
        {
            "label": "A",
            "text": "严格驳回，要求重新报账",
            "scores": {"S3": 5, "S6": 5},
            "tendency": "L",
            "reasoning": "务实高（S3:5），底线高（S6:5）。"
        },
        {
            "label": "B",
            "text": "私下询问当事人，了解情况",
            "scores": {"S3": 3, "S6": 3},
            "tendency": "M",
            "reasoning": "中等务实（S3:3），中等底线（S6:3）。"
        },
        {
            "label": "C",
            "text": "睁只眼闭只眼，通过报销",
            "scores": {"S3": 1, "S6": 1},
            "tendency": "H",
            "reasoning": "务实低（S3:1），底线低（S6:1）。"
        }
    ],
    "reveal": "傅融对钱很敏感，常说“少来。记得报销这次的车马费”。"
})

questions.append({
    "id": "furong_scheme_4",
    "type": "scheme",
    "dimension": ["S1", "S7"],
    "source_character": "傅融",
    "text": "傅融得到一份情报，可能影响多方势力平衡。",
    "options": [
        {
            "label": "A",
            "text": "立即销毁，避免卷入",
            "scores": {"S1": 1, "S7": 1},
            "tendency": "L",
            "reasoning": "权谋低（逃避）（S1:1），锋芒低（S7:1）。"
        },
        {
            "label": "B",
            "text": "暗中调查，掌握更多信息",
            "scores": {"S1": 5, "S7": 3},
            "tendency": "M",
            "reasoning": "权谋高（S1:5），锋芒中等（S7:3）。"
        },
        {
            "label": "C",
            "text": "公开情报，引发混乱渔利",
            "scores": {"S1": 3, "S7": 5},
            "tendency": "H",
            "reasoning": "权谋中等（S1:3），锋芒高（S7:5）。"
        }
    ],
    "reveal": "傅融在情报处理上既有谨慎也有锋芒。"
})

questions.append({
    "id": "furong_scheme_5",
    "type": "scheme",
    "dimension": ["S2", "S9"],
    "source_character": "傅融",
    "text": "傅融需要在忠诚于你和服从朝廷命令之间选择。",
    "options": [
        {
            "label": "A",
            "text": "选择忠诚于你，违抗朝廷",
            "scores": {"S2": 5, "S9": 1},
            "tendency": "L",
            "reasoning": "情感高（S2:5），权力低（放弃官方权力）（S9:1）。"
        },
        {
            "label": "B",
            "text": "试图找到两全之法",
            "scores": {"S2": 3, "S9": 3},
            "tendency": "M",
            "reasoning": "情感中等（S2:3），权力中等（S9:3）。"
        },
        {
            "label": "C",
            "text": "选择朝廷，但向你解释",
            "scores": {"S2": 1, "S9": 5},
            "tendency": "H",
            "reasoning": "情感低（S2:1），权力高（S9:5）。"
        }
    ],
    "reveal": "傅融的立场始终是保护你，但他也有自己的原则。"
})

# 批次5: daily (5题)
questions.append({
    "id": "furong_daily_1",
    "type": "daily",
    "dimension": ["S3", "S8"],
    "source_character": "傅融",
    "text": "傅融提醒你“记得报销这次的车马费”。",
    "options": [
        {
            "label": "A",
            "text": "笑着说“知道了，小气鬼”",
            "scores": {"S3": 3, "S8": 5},
            "tendency": "L",
            "reasoning": "中等务实（S3:3），温柔高（S8:5）。"
        },
        {
            "label": "B",
            "text": "立刻掏钱给他",
            "scores": {"S3": 5, "S8": 3},
            "tendency": "M",
            "reasoning": "务实高（S3:5），温柔中等（S8:3）。"
        },
        {
            "label": "C",
            "text": "假装没听见，转移话题",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "H",
            "reasoning": "务实低（S3:1），温柔低（S8:1）。"
        }
    ],
    "reveal": "傅融常说：“少来。记得报销这次的车马费。” 他连浪漫时刻都不忘报销。"
})

questions.append({
    "id": "furong_daily_2",
    "type": "daily",
    "dimension": ["S5", "S10"],
    "source_character": "傅融",
    "text": "傅融提醒你该发工资了。",
    "options": [
        {
            "label": "A",
            "text": "马上发，并多给一些奖金",
            "scores": {"S5": 5, "S10": 3},
            "tendency": "L",
            "reasoning": "行动力高（S5:5），秩序中等（S10:3）。"
        },
        {
            "label": "B",
            "text": "说“月底一起发”",
            "scores": {"S5": 3, "S10": 5},
            "tendency": "M",
            "reasoning": "行动力中等（S5:3），秩序高（S10:5）。"
        },
        {
            "label": "C",
            "text": "装可怜“没钱了，下个月补”",
            "scores": {"S5": 1, "S10": 1},
            "tendency": "H",
            "reasoning": "行动力低（S5:1），秩序低（S10:1）。"
        }
    ],
    "reveal": "傅融对工资很执着，这是他务实的一面。"
})

questions.append({
    "id": "furong_daily_3",
    "type": "daily",
    "dimension": ["S4", "S7"],
    "source_character": "傅融",
    "text": "傅融帮你编病假，应付宫里的点卯。",
    "options": [
        {
            "label": "A",
            "text": "接受，并感谢他",
            "scores": {"S4": 5, "S7": 1},
            "tendency": "L",
            "reasoning": "面具高（配合伪装）（S4:5），锋芒低（S7:1）。"
        },
        {
            "label": "B",
            "text": "拒绝，说“我自己能应付”",
            "scores": {"S4": 3, "S7": 5},
            "tendency": "M",
            "reasoning": "中等面具（S4:3），锋芒高（S7:5）。"
        },
        {
            "label": "C",
            "text": "开玩笑“你越来越像我的同谋了”",
            "scores": {"S4": 1, "S7": 3},
            "tendency": "H",
            "reasoning": "面具低（S4:1），锋芒中等（S7:3）。"
        }
    ],
    "reveal": "傅融会默默帮你处理这些琐事，是他关心的方式。"
})

questions.append({
    "id": "furong_daily_4",
    "type": "daily",
    "dimension": ["S2", "S5"],
    "source_character": "傅融",
    "text": "傅融遛狗时问你要不要一起去。",
    "options": [
        {
            "label": "A",
            "text": "答应，并和他并肩散步",
            "scores": {"S2": 3, "S5": 5},
            "tendency": "L",
            "reasoning": "情感中等（S2:3），行动力高（S5:5）。"
        },
        {
            "label": "B",
            "text": "拒绝，说“我还有事”",
            "scores": {"S2": 1, "S5": 3},
            "tendency": "M",
            "reasoning": "情感低（S2:1），行动力中等（S5:3）。"
        },
        {
            "label": "C",
            "text": "说“你带飞云去，我等你回来”",
            "scores": {"S2": 5, "S5": 1},
            "tendency": "H",
            "reasoning": "情感高（S2:5），行动力低（S5:1）。"
        }
    ],
    "reveal": "傅融的邀请往往很含蓄，需要你细心察觉。"
})

questions.append({
    "id": "furong_daily_5",
    "type": "daily",
    "dimension": ["S3", "S8"],
    "source_character": "傅融",
    "text": "傅融下厨做菜，问你咸淡。",
    "options": [
        {
            "label": "A",
            "text": "说“正好，很好吃”",
            "scores": {"S3": 5, "S8": 5},
            "tendency": "L",
            "reasoning": "务实高（准确评价）（S3:5），温柔高（S8:5）。"
        },
        {
            "label": "B",
            "text": "说“有点淡，再加点盐”",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M",
            "reasoning": "中等务实（S3:3），中等温柔（S8:3）。"
        },
        {
            "label": "C",
            "text": "从他手里拿过勺子尝一口",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "H",
            "reasoning": "务实低（S3:1），温柔低（S8:1）。"
        }
    ],
    "reveal": "傅融在夜晈既明中做过菜，还抱怨醋布太苦。"
})

# 批次6: classic (5题)
questions.append({
    "id": "furong_classic_1",
    "type": "classic",
    "dimension": ["S5", "S8"],
    "source_character": "傅融",
    "text": "进宫点卯前，傅融帮你整理仪容，嘴上说“别动，还想不想进宫点卯了？”。",
    "options": [
        {
            "label": "A",
            "text": "乖乖站着让他整理",
            "scores": {"S5": 1, "S8": 5},
            "tendency": "L",
            "reasoning": "行动力低（被动）（S5:1），温柔高（接受照顾）（S8:5）。"
        },
        {
            "label": "B",
            "text": "自己整理，说“我自己来”",
            "scores": {"S5": 5, "S8": 3},
            "tendency": "M",
            "reasoning": "行动力高（S5:5），温柔中等（S8:3）。"
        },
        {
            "label": "C",
            "text": "抓住他的手，说“不急”",
            "scores": {"S5": 3, "S8": 1},
            "tendency": "H",
            "reasoning": "行动力中等（S5:3），温柔低（打断）（S8:1）。"
        }
    ],
    "reveal": "傅融说：“别动，还想不想进宫点卯了？” 他嘴上凶，动作却很轻。"
})

questions.append({
    "id": "furong_classic_2",
    "type": "classic",
    "dimension": ["S2", "S6"],
    "source_character": "傅融",
    "text": "乌云白云，傅融捡到流浪狗，嘴上说“等它伤好了就送走”。",
    "options": [
        {
            "label": "A",
            "text": "说“好，送走前给它取个名字吧”",
            "scores": {"S2": 3, "S6": 5},
            "tendency": "L",
            "reasoning": "情感中等（S2:3），底线高（尊重他的决定）（S6:5）。"
        },
        {
            "label": "B",
            "text": "说“别送了，我们养着吧”",
            "scores": {"S2": 5, "S6": 3},
            "tendency": "M",
            "reasoning": "情感高（S2:5），底线中等（S6:3）。"
        },
        {
            "label": "C",
            "text": "说“随你，反正我不喜欢狗”",
            "scores": {"S2": 1, "S6": 1},
            "tendency": "H",
            "reasoning": "情感低（S2:1），底线低（S6:1）。"
        }
    ],
    "reveal": "傅融最终给狗取名“飞云”，一直养在身边，典型的嘴硬心软。"
})

questions.append({
    "id": "furong_classic_3",
    "type": "classic",
    "dimension": ["S2", "S9"],
    "source_character": "傅融",
    "text": "丹书白马/25，傅融重伤时说“保证过……会陪你……走下去的……”。",
    "options": [
        {
            "label": "A",
            "text": "握紧他的手，说“我等你”",
            "scores": {"S2": 5, "S9": 1},
            "tendency": "L",
            "reasoning": "情感高（S2:5），权力低（S9:1）。"
        },
        {
            "label": "B",
            "text": "说“别说了，省点力气”",
            "scores": {"S2": 3, "S9": 5},
            "tendency": "M",
            "reasoning": "情感中等（S2:3），权力高（命令他）（S9:5）。"
        },
        {
            "label": "C",
            "text": "吻他，说“我们一起走”",
            "scores": {"S2": 1, "S9": 3},
            "tendency": "H",
            "reasoning": "情感低（不合时宜）（S2:1），权力中等（S9:3）。"
        }
    ],
    "reveal": "这是傅融最直白的情感流露之一，重伤仍记得承诺。"
})

questions.append({
    "id": "furong_classic_4",
    "type": "classic",
    "dimension": ["S4", "S10"],
    "source_character": "傅融",
    "text": "夜晈既明，傅融在烟花下说“夜空很美……我也见到了比星子和烟花更亮的东西。”",
    "options": [
        {
            "label": "A",
            "text": "假装没听懂，说“烟花确实很美”",
            "scores": {"S4": 5, "S10": 3},
            "tendency": "L",
            "reasoning": "面具高（S4:5），秩序中等（S10:3）。"
        },
        {
            "label": "B",
            "text": "看着他眼睛，问“是什么？”",
            "scores": {"S4": 3, "S10": 5},
            "tendency": "M",
            "reasoning": "中等面具（S4:3），秩序高（追问）（S10:5）。"
        },
        {
            "label": "C",
            "text": "亲他一下，说“我也看到了”",
            "scores": {"S4": 1, "S10": 1},
            "tendency": "H",
            "reasoning": "面具低（S4:1），秩序低（S10:1）。"
        }
    ],
    "reveal": "傅融难得说情话，却说得含蓄又浪漫。"
})

questions.append({
    "id": "furong_classic_5",
    "type": "classic",
    "dimension": ["S5", "S7"],
    "source_character": "傅融",
    "text": "密会滑雪，傅融失控大喊“停、停不住了！越滑越快！”。",
    "options": [
        {
            "label": "A",
            "text": "试图拉住他，一起摔倒",
            "scores": {"S5": 5, "S7": 3},
            "tendency": "L",
            "reasoning": "行动力高（S5:5），锋芒中等（S7:3）。"
        },
        {
            "label": "B",
            "text": "大笑“看你怎么办”",
            "scores": {"S5": 3, "S7": 5},
            "tendency": "M",
            "reasoning": "行动力中等（S5:3），锋芒高（S7:5）。"
        },
        {
            "label": "C",
            "text": "呆住，不知所措",
            "scores": {"S5": 1, "S7": 1},
            "tendency": "H",
            "reasoning": "行动力低（S5:1），锋芒低（S7:1）。"
        }
    ],
    "reveal": "傅融滑雪失控的样子难得一见，他平时总是冷静自持。"
})

# 写入文件
with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/furong.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f'Generated {len(questions)} questions')