import json

questions = []

# ==================== SWEET 批次 (5题) ====================

# 1. 南有乔木/15 - 整夜守护
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

# 2. 南有乔木/22 - 游猎遇山贼
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

# 3. 围城受伤安慰
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

# 4. 七夕五子棋连输
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
    "reveal": "「啊……又输了……连输十七把了……」（七夕欢情）孙策五子棋连输十七把，展现反差萌。他好胜但面对你时只剩笨拙的真诚。"
})

# 5. 南有乔木/23 - 夸好看
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

# ==================== FUNNY 批次 (5题) ====================

# 6. 七夕投壶连中二十支炫耀
questions.append({
    "id": "sunce_funny_01",
    "type": "funny",
    "dimension": ["S3", "S7"],
    "source_character": "孙策",
    "text": "七夕夜市上，孙策投壶连中二十支，得意地向你炫耀。",
    "options": [
        {
            "label": "A",
            "text": "淡淡夸一句不错，继续逛别的",
            "scores": {"S3": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "鼓掌说他厉害，配合他的炫耀",
            "scores": {"S3": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说这不算什么，我闭着眼睛也能中",
            "scores": {"S3": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「连进二十支！牛不牛！投壶小意思，我投飞矛都没失过手！」（七夕欢情）孙策像孩子一样炫耀战绩，求夸奖的样子很可爱。"
})

# 7. 七夕套圈套不到泥娃娃
questions.append({
    "id": "sunce_funny_02",
    "type": "funny",
    "dimension": ["S3", "S5"],
    "source_character": "孙策",
    "text": "孙策套圈花光零钱都没套到想要的泥娃娃，却发现你套到了'江东小霸王'款。",
    "options": [
        {
            "label": "A",
            "text": "把泥娃娃收起来，不提这事",
            "scores": {"S3": 1, "S5": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "把泥娃娃递给他看，笑他手气差",
            "scores": {"S3": 3, "S5": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "把泥娃娃送他，说'小霸王归你了'",
            "scores": {"S3": 5, "S5": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「零钱都花完了还没套到……啥？你套到了？给我看看！——江东小霸王的泥娃娃？」（七夕欢情）孙策套不到自己形象的泥娃娃，反差搞笑。"
})

# 8. 七夕钓鱼不行徒手抓
questions.append({
    "id": "sunce_funny_03",
    "type": "funny",
    "dimension": ["S5", "S7"],
    "source_character": "孙策",
    "text": "孙策钓鱼毫无耐心，最后掏金块给老板说要徒手抓鱼。",
    "options": [
        {
            "label": "A",
            "text": "劝他算了，钓鱼本来就要耐心",
            "scores": {"S5": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "笑着看他徒手抓，等他出糗",
            "scores": {"S5": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "也掏钱说'我也来，看谁先抓到'",
            "scores": {"S5": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「老子就不信今天抓不到鱼！老板，这金块给你！我徒手抓！」（七夕欢情）孙策用最豪横的方式解决钓鱼难题，典型孙策式思维。"
})

# 9. 劈开九连环/鲁班锁
questions.append({
    "id": "sunce_funny_04",
    "type": "funny",
    "dimension": ["S3", "S5"],
    "source_character": "孙策",
    "text": "孙策看着九连环和鲁班锁，嘀咕'怎么看都是锁死的，要不还是大力出奇迹'。",
    "options": [
        {
            "label": "A",
            "text": "拿过来自己解，不让他破坏",
            "scores": {"S3": 1, "S5": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "教他怎么解，让他试试",
            "scores": {"S3": 3, "S5": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说'劈吧，我也想看看大力出奇迹'",
            "scores": {"S3": 5, "S5": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「还有个九连环？到底怎么把环解开啊，怎么看都是锁死的，要不还是大力出奇迹？」（剧情）孙策面对智力玩具第一反应是暴力破解，很符合人设。"
})

# 10. 吃饵糕烫舌头
questions.append({
    "id": "sunce_funny_05",
    "type": "funny",
    "dimension": ["S3", "S8"],
    "source_character": "孙策",
    "text": "孙策买了两份饵糕，自己先咬一大口，结果烫得直跳脚。",
    "options": [
        {
            "label": "A",
            "text": "递水给他，让他小心点",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "笑他心急，帮他吹凉",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说'我也试试'，小口咬自己的饵糕",
            "scores": {"S3": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「看我一口吞——啊呜……呜……□□□□□□……好烫！」（剧情）孙策吃东西莽撞被烫，狼狈又可爱。"
})

# ==================== ANGST 批次 (5题) ====================

# 11. 围城生死关头
questions.append({
    "id": "sunce_angst_01",
    "type": "angst",
    "dimension": ["S2", "S6"],
    "source_character": "孙策",
    "text": "围城战中，孙策浑身是伤，却对你说'大丈夫为心上人死，死得坦坦荡荡'。",
    "options": [
        {
            "label": "A",
            "text": "劝他先撤退，保住性命最重要",
            "scores": {"S2": 1, "S6": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "握紧武器说'要死一起死'",
            "scores": {"S2": 3, "S6": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "吻他说'不许死，我要你活着娶我'",
            "scores": {"S2": 5, "S6": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「大丈夫为心上人死，死得坦坦荡荡。」（围城）孙策在生死关头坦然表达爱意，将你的安危置于自己生命之上。"
})

# 12. 梦入浮生断义相决
questions.append({
    "id": "sunce_angst_02",
    "type": "angst",
    "dimension": ["S1", "S2"],
    "source_character": "孙策",
    "text": "梦境中，孙策与你因立场对立不得不刀剑相向。他说'这是最后一次了'。",
    "options": [
        {
            "label": "A",
            "text": "收剑离开，不愿与他战斗",
            "scores": {"S1": 1, "S2": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "拔剑应对，尊重这场对决",
            "scores": {"S1": 3, "S2": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "扔下剑说'要杀就杀，我下不了手'",
            "scores": {"S1": 5, "S2": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「……也好……说不定，这是最后一次了。」（梦入浮生）孙策在梦境中面对与你的对立，流露出深深的无奈和悲伤。"
})

# 13. 权力太可怕了讨论
questions.append({
    "id": "sunce_angst_03",
    "type": "angst",
    "dimension": ["S9", "S10"],
    "source_character": "孙策",
    "text": "孙策对你说'权力对我来说太可怕了'，他打天下是为了太平，不是为了权力。",
    "options": [
        {
            "label": "A",
            "text": "说权力必要，劝他接受现实",
            "scores": {"S9": 1, "S10": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认同他的观点，说权力确实腐蚀人心",
            "scores": {"S9": 3, "S10": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握住他的手说'我们一起创造不要权力的天下'",
            "scores": {"S9": 5, "S10": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「权力对我来说太可怕了。」「嗯，是最可怕的东西，比毒药还会腐蚀犬心。」（犬都纪事）孙策清醒认识到权力的危害，保持初心。"
})

# 14. 受伤后说'别弄脏了'
questions.append({
    "id": "sunce_angst_04",
    "type": "angst",
    "dimension": ["S2", "S8"],
    "source_character": "孙策",
    "text": "孙策受伤流血，却推开你说'别弄脏了……等明天，你还要穿着这身常服，毫发无伤地站出去呢'。",
    "options": [
        {
            "label": "A",
            "text": "退开叫军医，尊重他的意愿",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "不顾阻拦上前为他包扎",
            "scores": {"S2": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "撕下自己的衣角为他止血，说'脏了就一起脏'",
            "scores": {"S2": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「别弄脏了……等明天，你还要穿着这身常服，毫发无伤地站出去呢。」（围城）孙策自己重伤却只关心你的形象，温柔到令人心痛。"
})

# 15. '你若想走，我护你走'
questions.append({
    "id": "sunce_angst_05",
    "type": "angst",
    "dimension": ["S2", "S6"],
    "source_character": "孙策",
    "text": "孙策看着你说'你想走吗？你若想走，我护你走'，给你自由选择的机会。",
    "options": [
        {
            "label": "A",
            "text": "说谢谢，然后离开",
            "scores": {"S2": 1, "S6": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "摇头说'我不走'，留下陪他",
            "scores": {"S2": 3, "S6": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "抱住他说'要走一起走，要留一起留'",
            "scores": {"S2": 5, "S6": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「你想走吗？你若想走，我护你走。」（围城）孙策在生死关头仍尊重你的选择，爱不是占有而是成全。"
})

# ==================== SCHEME 批次 (5题) ====================

# 16. 犬都纪事权力讨论
questions.append({
    "id": "sunce_scheme_01",
    "type": "scheme",
    "dimension": ["S1", "S9"],
    "source_character": "孙策",
    "text": "孙策说'绝大多数的犬心里想的还是，自己想要天下和权力吧'，但他自己对权力没兴趣。",
    "options": [
        {
            "label": "A",
            "text": "提醒他权力是必要的工具，不该排斥",
            "scores": {"S1": 1, "S9": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "赞同他的看法，说权力确实会腐蚀人",
            "scores": {"S1": 3, "S9": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说'我们一起建立不靠权力的新秩序'",
            "scores": {"S1": 5, "S9": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「绝大多数的犬心里想的还是，自己想要天下和权力吧。不过，权力对我来说太可怕了。」（犬都纪事）孙策对权力有清醒认知，不忘初心。"
})

# 17. 士族虚伪讨论
questions.append({
    "id": "sunce_scheme_02",
    "type": "scheme",
    "dimension": ["S1", "S4"],
    "source_character": "孙策",
    "text": "孙策评论士族'公敌是可以被塑造的。士族想要延续这个公敌，避免犬都开始内斗'。",
    "options": [
        {
            "label": "A",
            "text": "说士族也有苦衷，不必过于批判",
            "scores": {"S1": 1, "S4": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认同他的分析，士族确实在操控舆论",
            "scores": {"S1": 3, "S4": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "提议'我们一起打破士族的游戏规则'",
            "scores": {"S1": 5, "S4": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「公敌是可以被塑造的。士族想要延续这个公敌，避免犬都开始内斗。」（犬都纪事）孙策看穿士族维持统治的手段，展现政治洞察力。"
})

# 18. 围城政治立场
questions.append({
    "id": "sunce_scheme_03",
    "type": "scheme",
    "dimension": ["S1", "S6"],
    "source_character": "孙策",
    "text": "围城时孙策说'和袁术喝酒的是我爹，又不是我'，划清与袁术的界限。",
    "options": [
        {
            "label": "A",
            "text": "质疑他的立场，要他明确表态",
            "scores": {"S1": 1, "S6": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "接受他的解释，共同守城",
            "scores": {"S1": 3, "S6": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说'我相信你，我们一起打出新天地'",
            "scores": {"S1": 5, "S6": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「放屁。和袁术喝酒的是我爹，又不是我。」（围城）孙策明确自己的政治立场，不被家族关系绑架。"
})

# 19. 玉玺传言应对
questions.append({
    "id": "sunce_scheme_04",
    "type": "scheme",
    "dimension": ["S1", "S5"],
    "source_character": "孙策",
    "text": "孙策因玉玺传言被各方势力盯上，他对你说'不知哪个赤佬在外面胡扯，说玉玺在我家'。",
    "options": [
        {
            "label": "A",
            "text": "建议他低调处理，避免冲突",
            "scores": {"S1": 1, "S5": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "帮他加强守卫，应对可能的袭击",
            "scores": {"S1": 3, "S5": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "提议'主动放出假消息，引蛇出洞'",
            "scores": {"S1": 5, "S5": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「不知哪个赤佬在外面胡扯，说玉玺在我家，所以时不时就有人过来搞事。」（南有乔木/15）孙策面对玉玺传言的态度务实，加强防备而非逃避。"
})

# 20. 袁术关系处理
questions.append({
    "id": "sunce_scheme_05",
    "type": "scheme",
    "dimension": ["S1", "S4"],
    "source_character": "孙策",
    "text": "孙策评价袁术'早就看你不顺眼了，天天在袁术耳朵边吹风'，展现对袁术阵营的不满。",
    "options": [
        {
            "label": "A",
            "text": "劝他隐忍，暂时不要与袁术冲突",
            "scores": {"S1": 1, "S4": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "支持他的判断，袁术确实有问题",
            "scores": {"S1": 3, "S4": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说'我们联手，迟早取代袁术'",
            "scores": {"S1": 5, "S4": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「早就看你不顺眼了，天天在袁术耳朵边吹风……」（围城）孙策对袁术阵营有清醒认识，不因亲戚关系而盲从。"
})

# ==================== DAILY 批次 (5题) ====================

# 21. 切肉不弄花妆
questions.append({
    "id": "sunce_daily_01",
    "type": "daily",
    "dimension": ["S3", "S8"],
    "source_character": "孙策",
    "text": "孙策替你切肉，说'你今天的妆好看，肯定用心画了，不想弄花'。",
    "options": [
        {
            "label": "A",
            "text": "自己切肉，说不用麻烦他",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "让他切，感谢他的细心",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "也帮他切一份，说'互相照顾'",
            "scores": {"S3": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「我替你切肉。你今天的妆好看，肯定用心画了，不想弄花。」（剧情）孙策注意到你的妆容细节，展现粗犷外表下的细腻温柔。"
})

# 22. 捕蝇草惹炸了
questions.append({
    "id": "sunce_daily_02",
    "type": "daily",
    "dimension": ["S3", "S7"],
    "source_character": "孙策",
    "text": "孙策好奇捕蝇草，用手戳它结果被'咬'住，兴奋地说'这花有意思'。",
    "options": [
        {
            "label": "A",
            "text": "拉开他的手，说别玩危险的东西",
            "scores": {"S3": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "笑他孩子气，教他怎么和捕蝇草玩",
            "scores": {"S3": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "也伸手去戳，说'看谁先被咬'",
            "scores": {"S3": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「我戳、我戳……它会动！这花有意思！叫什么……捕蝇草？」（剧情）孙策对新鲜事物的好奇和孩子气的一面。"
})

# 23. 日常守护细节
questions.append({
    "id": "sunce_daily_03",
    "type": "daily",
    "dimension": ["S5", "S8"],
    "source_character": "孙策",
    "text": "孙策总走在你外侧，说'有我在，什么车马都撞不到你'。",
    "options": [
        {
            "label": "A",
            "text": "说不用这么小心，自己会注意",
            "scores": {"S5": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "接受他的保护，走在他内侧",
            "scores": {"S5": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "也走到他外侧，说'我也保护你'",
            "scores": {"S5": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "孙策习惯性走在危险一侧保护你，是刻进骨子里的守护本能。"
})

# 24. 笨拙照顾
questions.append({
    "id": "sunce_daily_04",
    "type": "daily",
    "dimension": ["S3", "S8"],
    "source_character": "孙策",
    "text": "你生病时孙策笨手笨脚地照顾，药洒了半碗，他挠头说'我再煮一碗'。",
    "options": [
        {
            "label": "A",
            "text": "说不用麻烦，自己来就好",
            "scores": {"S3": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "笑他笨，让他小心点再煮",
            "scores": {"S3": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "握住他的手说'笨点也没关系，有这份心就够了'",
            "scores": {"S3": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "孙策不擅长照顾人，但愿意为你尝试，笨拙却真诚。"
})

# 25. 直球求婚
questions.append({
    "id": "sunce_daily_05",
    "type": "daily",
    "dimension": ["S2", "S7"],
    "source_character": "孙策",
    "text": "孙策看着你说'把那套什么广陵王妃的礼服，照我的尺寸改改'，直球暗示想嫁给你。",
    "options": [
        {
            "label": "A",
            "text": "假装没听懂，转移话题",
            "scores": {"S2": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "笑他不知羞，说'想得美'",
            "scores": {"S2": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说'不用改，我娶你，你穿我的礼服'",
            "scores": {"S2": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "孙策的求婚方式也充满个人风格——直球、热烈、不带丝毫犹豫。"
})

# ==================== CLASSIC 批次 (5题) ====================

# 26. 围城一人守城
questions.append({
    "id": "sunce_classic_01",
    "type": "classic",
    "dimension": ["S5", "S7"],
    "source_character": "孙策",
    "text": "围城战最激烈时，孙策一人挡在城门前，说'今晚我就要一个人战到底，杀性起了，谁都不能过来'。",
    "options": [
        {
            "label": "A",
            "text": "劝他退回来，大家一起守",
            "scores": {"S5": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "在城墙上为他掠阵，随时支援",
            "scores": {"S5": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "提剑站到他身旁，说'要战一起战'",
            "scores": {"S5": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「今晚我就要一个人战到底，杀性起了，谁都不能过来。」（围城）孙策在战场上的霸气与决绝，一人可当千军。"
})

# 27. 南有乔木/22游猎经典
questions.append({
    "id": "sunce_classic_02",
    "type": "classic",
    "dimension": ["S5", "S8"],
    "source_character": "孙策",
    "text": "山贼包围你们时，孙策将你护在身后，说'怕的话就叫出声，我不笑你'。",
    "options": [
        {
            "label": "A",
            "text": "保持安静，不干扰他战斗",
            "scores": {"S5": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "轻声说'不怕，有你在'",
            "scores": {"S5": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "大声说'不怕！我们一起打跑他们'",
            "scores": {"S5": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「怕的话就叫出声，我不笑你。」「有我在，你什么都不用怕。」（南有乔木/22）孙策在危险中先顾及你的情绪，是经典守护场景。"
})

# 28. 七夕欢情综合
questions.append({
    "id": "sunce_classic_03",
    "type": "classic",
    "dimension": ["S3", "S7"],
    "source_character": "孙策",
    "text": "七夕夜孙策带你玩遍所有摊子，投壶、套圈、钓鱼、下棋，每一样都玩得兴高采烈。",
    "options": [
        {
            "label": "A",
            "text": "适度参与，保持矜持",
            "scores": {"S3": 1, "S7": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "陪他玩，享受节日的快乐",
            "scores": {"S3": 3, "S7": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "比他玩得更嗨，主动挑战新项目",
            "scores": {"S3": 5, "S7": 5},
            "tendency": "H"
        }
    ],
    "reveal": "七夕欢情是孙策反差萌的集中展现：战场猛将变约会笨蛋，每一面都真实可爱。"
})

# 29. 南有乔木/15守护经典
questions.append({
    "id": "sunce_classic_04",
    "type": "classic",
    "dimension": ["S2", "S8"],
    "source_character": "孙策",
    "text": "孙策因玉玺传言亲自整夜守在客房外，说'我整夜都在客房外。有什么风吹草动，全都能听见'。",
    "options": [
        {
            "label": "A",
            "text": "说不用这么辛苦，让护卫守就行",
            "scores": {"S2": 1, "S8": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "接受他的守护，安心休息",
            "scores": {"S2": 3, "S8": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "开门说'外面冷，进来守着吧'",
            "scores": {"S2": 5, "S8": 5},
            "tendency": "H"
        }
    ],
    "reveal": "「我整夜都在客房外。有什么风吹草动，全都能听见。」（南有乔木/15）孙策用实际行动证明他的守护誓言。"
})

# 30. 权力是石头讨论
questions.append({
    "id": "sunce_classic_05",
    "type": "classic",
    "dimension": ["S1", "S9"],
    "source_character": "孙策",
    "text": "孙策说'权力是石头，拿起石头，先让他们恐惧你，才能让他们爱你'，但随即说权力对自己太可怕。",
    "options": [
        {
            "label": "A",
            "text": "说权力是必要之恶，劝他接受",
            "scores": {"S1": 1, "S9": 1},
            "tendency": "L"
        },
        {
            "label": "B",
            "text": "认同权力的两面性，需谨慎对待",
            "scores": {"S1": 3, "S9": 3},
            "tendency": "M"
        },
        {
            "label": "C",
            "text": "说'我们创造不需要恐惧的天下'",
            "scores": {"S1": 5, "S9": 5},
            "tendency": "H"
        }
    ],
    "reveal": "孙策对权力的认知深刻而清醒，他明白权力的运作规则，但选择不被权力异化。"
})

print(f"Generated {len(questions)} questions")

# 写入文件
output_path = "/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/sunce.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Saved to {output_path}")

# 检查维度覆盖
all_dims = set()
for q in questions:
    for dim in q["dimension"]:
        all_dims.add(dim)
print(f"覆盖维度: {sorted(all_dims)}")
print(f"总维度数: {len(all_dims)}/10")

# 检查每个批次数量
batch_counts = {}
for q in questions:
    batch_counts[q["type"]] = batch_counts.get(q["type"], 0) + 1
print("批次分布:", batch_counts)