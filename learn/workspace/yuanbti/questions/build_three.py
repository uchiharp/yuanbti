#!/usr/bin/env python3
import json, os

# 20题维度分配：每维度2题，6种type：sweet×3, funny×4, angst×3, scheme×4, daily×3, classic×3
# S1-S10各2题
dims_schedule = [
    # sweet×3
    ("sweet", "S2"), ("sweet", "S8"), ("sweet", "S7"),
    # funny×4
    ("funny", "S7"), ("funny", "S5"), ("funny", "S4"), ("funny", "S3"),
    # angst×3
    ("angst", "S6"), ("angst", "S2"), ("angst", "S5"),
    # scheme×4
    ("scheme", "S1"), ("scheme", "S9"), ("scheme", "S6"), ("scheme", "S3"),
    # daily×3
    ("daily", "S8"), ("daily", "S10"), ("daily", "S5"),
    # classic×3
    ("classic", "S1"), ("classic", "S10"), ("classic", "S4"),
]

assert len(dims_schedule) == 20

# ========== 张辽 ==========
zhangliao_questions = [
    {
        "id": "zhangliao_sweet_01",
        "type": "sweet",
        "dimension": ["S2"],
        "source_character": "张辽",
        "text": "你从集市带回一只毛绒绒的小狐狸玩偶。张辽瞥了一眼，嘴角微微抽搐：「想变成狐狸围脖吗？要不是看在你是我最大的军功，我今天就扒了你的皮！」",
        "options": [
            {"label": "A", "text": "默默把玩偶收起来，当没发生过", "scores": {"S2": 1}, "tendency": "L", "reasoning": "回避互动，放弃情感表达机会→S2:1"},
            {"label": "B", "text": "笑嘻嘻地把玩偶往他脖子上一围，说这叫提前实习", "scores": {"S2": 3}, "tendency": "M", "reasoning": "用玩笑化解他的嘴硬，间接表达亲昵→S2:3"},
            {"label": "C", "text": "直接凑到他面前说那我要一直当你的军功，不许退货", "scores": {"S2": 5}, "tendency": "H", "reasoning": "正面回应他的占有式表达，毫不退缩→S2:5"}
        ],
        "reveal": "「想变成狐狸围脖吗？！要不是看在你是我最大的军功，我今天就扒了你的皮！」——犬都纪事。张辽的威胁翻译过来是：你很重要。"
    },
    {
        "id": "zhangliao_sweet_02",
        "type": "sweet",
        "dimension": ["S8"],
        "source_character": "张辽",
        "text": "夜晚军帐外，张辽默默往你这边挪了挪，把你挡在上风口。他什么都没说，只是背对着你哼了一声。",
        "options": [
            {"label": "A", "text": "安心地缩进披风里睡觉", "scores": {"S8": 1}, "tendency": "L", "reasoning": "接受照顾但没有回应温暖→S8:1"},
            {"label": "B", "text": "小声说了句谢谢，然后把随身带的干粮分他一半", "scores": {"S8": 3}, "tendency": "M", "reasoning": "用食物回礼，温和但不说破→S8:3"},
            {"label": "C", "text": "直接靠到他背上，说西凉的风太冷了你借我暖暖", "scores": {"S8": 5}, "tendency": "H", "reasoning": "主动制造身体接触，接纳他的守护→S8:5"}
        ],
        "reveal": "张辽不善言辞，但总是用行动把人护在身后。在西凉军中，他是那种先挡刀再说话的人。"
    },
    {
        "id": "zhangliao_sweet_03",
        "type": "sweet",
        "dimension": ["S7"],
        "source_character": "张辽",
        "text": "张辽看着你的新发型沉默了好一阵，终于开口：「……这种威胁真的会有威慑力吗？只是变一个发型而已……」语气嫌弃，但视线一直没移开。",
        "options": [
            {"label": "A", "text": "尴尬地摸摸头发，后悔换了发型", "scores": {"S7": 1}, "tendency": "L", "reasoning": "被他的态度击退，缺乏自信→S7:1"},
            {"label": "B", "text": "学着他的语气怼回去：这种吐槽真的会有杀伤力吗？只是嘴硬而已", "scores": {"S7": 3}, "tendency": "M", "reasoning": "用他自己的逻辑反将一军，势均力敌→S7:3"},
            {"label": "C", "text": "凑到他面前歪头问：那你倒是别一直盯着看啊", "scores": {"S7": 5}, "tendency": "H", "reasoning": "正面戳穿他的口是心非，锋芒毕露→S7:5"}
        ],
        "reveal": "「……这种威胁真的会有威慑力吗？只是变一个发型而已……」——犬都纪事。嫌弃归嫌弃，眼睛很诚实。"
    },
    {
        "id": "zhangliao_funny_01",
        "type": "funny",
        "dimension": ["S7"],
        "source_character": "张辽",
        "text": "犬都纪事中，张辽被狐狸砸了一脸泥，气得跳脚：「不许砸我！不许刨土砸我！！！可恶！！！」你在一旁看着",
        "options": [
            {"label": "A", "text": "假装没看见，低头整理自己的东西", "scores": {"S7": 1}, "tendency": "L", "reasoning": "给足面子不戳穿，但也不参与→S7:1"},
            {"label": "B", "text": "捡起一块小石子递给他：来，砸回去", "scores": {"S7": 3}, "tendency": "M", "reasoning": "加入混战但不嘲讽，帮忙不补刀→S7:3"},
            {"label": "C", "text": "当场笑到蹲下，说西凉猛将被一只狐狸欺负了", "scores": {"S7": 5}, "tendency": "H", "reasoning": "毫不留情地嘲笑，锋芒全开→S7:5"}
        ],
        "reveal": "「不许砸我！不许刨土砸我！！！可恶！！！」——犬都纪事。威风凛凛的西凉将军，在毛绒绒面前破防了。"
    },
    {
        "id": "zhangliao_funny_02",
        "type": "funny",
        "dimension": ["S5"],
        "source_character": "张辽",
        "text": "张辽跟阿蝉说话时一脸操心的老父亲表情：「你这孩子不能总闷声不响的，要多和人沟通，积极一点儿，放松一点儿，你看看人家。」你正好路过",
        "options": [
            {"label": "A", "text": "悄悄绕路走开，不打扰他们", "scores": {"S5": 1}, "tendency": "L", "reasoning": "回避加入，不给反应→S5:1"},
            {"label": "B", "text": "走过去拍拍他肩膀：张辽你偏心，怎么不跟我说这些", "scores": {"S5": 3}, "tendency": "M", "reasoning": "自然切入，用撒娇反客为主→S5:3"},
            {"label": "C", "text": "当场模仿他的语气跟阿蝉说：对啊你看看人家张辽多会沟通，每天哼五十遍", "scores": {"S5": 5}, "tendency": "H", "reasoning": "立刻行动，精准打击他的双标→S5:5"}
        ],
        "reveal": "「你这孩子不能总闷声不响的，要多和人沟通，积极一点儿，放松一点儿，你看看人家。」——绣衣楼团建。张辽劝别人积极沟通，自己一天说不了三句话。"
    },
    {
        "id": "zhangliao_funny_03",
        "type": "funny",
        "dimension": ["S4"],
        "source_character": "张辽",
        "text": "珠履三千中，张辽对养骑兵的事一顿吐槽：「人还没西凉马高，养骑兵？三天能耗掉你一年的官仓。」然后话锋一转：「……你是谁养大的？是谁把你背马背上带大的？就知道不能任由你野在外面！」",
        "options": [
            {"label": "A", "text": "低头说知道了，不回嘴", "scores": {"S4": 1}, "tendency": "L", "reasoning": "顺从接受训斥，不戴面具→S4:1"},
            {"label": "B", "text": "点头附和然后小声嘀咕：所以到底是嫌我花钱还是担心我", "scores": {"S4": 3}, "tendency": "M", "reasoning": "表面顺从实则一语道破→S4:3"},
            {"label": "C", "text": "一脸无辜地说：张辽你是不是想我了，拐弯抹角说这么多", "scores": {"S4": 5}, "tendency": "H", "reasoning": "用天真面具反将一军，精准拆穿→S4:5"}
        ],
        "reveal": "「人还没西凉马高，养骑兵？……你是谁养大的？就知道不能任由你野在外面！」——珠履三千。嫌弃和担心只隔了一句话。"
    },
    {
        "id": "zhangliao_funny_04",
        "type": "funny",
        "dimension": ["S3"],
        "source_character": "张辽",
        "text": "犬都纪事中，张辽对着战利品清单痛哭：「这个这个那个那个还有还有那个那个可恶可恶之前之前……」军功又被算在别人头上了。",
        "options": [
            {"label": "A", "text": "安静等他发泄完，递杯水", "scores": {"S3": 1}, "tendency": "L", "reasoning": "情感安慰优先，不解决问题→S3:1"},
            {"label": "B", "text": "帮他整理一下到底被吞了多少军功，列个清单", "scores": {"S3": 3}, "tendency": "M", "reasoning": "务实地帮忙理清状况→S3:3"},
            {"label": "C", "text": "直接说别数了，反正每次都被抢，跟我回广陵吧", "scores": {"S3": 5}, "tendency": "H", "reasoning": "一句话切断沉没成本，给出实际出路→S3:5"}
        ],
        "reveal": "「这个这个那个那个还有还有那个那个可恶可恶之前之前……」——犬都纪事。张辽的军功被吞了无数次，每次都气得语无伦次。"
    },
    {
        "id": "zhangliao_angst_01",
        "type": "angst",
        "dimension": ["S6"],
        "source_character": "张辽",
        "text": "犬都纪事，张辽重伤倒地，最后的力气用来交代后事：「……带她的骨骸……回去……西凉的孩子……不能死在……没有太阳的地方……」",
        "options": [
            {"label": "A", "text": "握紧他的手，一句话都说不出来", "scores": {"S6": 1}, "tendency": "L", "reasoning": "悲伤到失声，无法做出承诺→S6:1"},
            {"label": "B", "text": "红着眼眶点头，说好，我带你们回去", "scores": {"S6": 3}, "tendency": "M", "reasoning": "含泪应承遗愿，守住底线→S6:3"},
            {"label": "C", "text": "死死按住他的伤口说不许死，你不许死，你还欠我很多场架", "scores": {"S6": 5}, "tendency": "H", "reasoning": "用愤怒对抗绝望，绝不接受结局→S6:5"}
        ],
        "reveal": "「……西凉的……西凉的孩子……不能死在……没有太阳的地方……带她……回去……」——犬都纪事。临终想的不是自己，是西凉的孩子要晒太阳。"
    },
    {
        "id": "zhangliao_angst_02",
        "type": "angst",
        "dimension": ["S2"],
        "source_character": "张辽",
        "text": "魂魂版密探剧情中，张辽找到你，语气罕见地低沉：「当年为何要走？我们找了你很久。」「绣衣楼的人，知道你以前的事吗？」",
        "options": [
            {"label": "A", "text": "沉默不语，转身走开", "scores": {"S2": 1}, "tendency": "L", "reasoning": "完全切断情感对话→S2:1"},
            {"label": "B", "text": "轻声说那都是很久以前的事了", "scores": {"S2": 3}, "tendency": "M", "reasoning": "淡化过去但不否认他的感情→S2:3"},
            {"label": "C", "text": "看着他的眼睛说因为我害怕你们为我付出了太多", "scores": {"S2": 5}, "tendency": "H", "reasoning": "坦露内心恐惧，直面情感→S2:5"}
        ],
        "reveal": "「当年为何要走？我们找了你很久。」——魂魂版密探剧情。张辽很少追问别人的过去，但他追问了你的。"
    },
    {
        "id": "zhangliao_angst_03",
        "type": "angst",
        "dimension": ["S5"],
        "source_character": "张辽",
        "text": "七载相逢中，张辽听闻你在许都的处境，把户籍迁了过去，却被人散布流言逼入绝境。他说：「好不容易安定下来……都是老子自己靠军功和性命堆出来的！就这样结束了！」",
        "options": [
            {"label": "A", "text": "拉住他说不会结束的，一定还有办法", "scores": {"S5": 1}, "tendency": "L", "reasoning": "口头安慰但没行动→S5:1"},
            {"label": "B", "text": "冷静分析流言的来源，计划反击", "scores": {"S5": 3}, "tendency": "M", "reasoning": "理性应对，有步骤地行动→S5:3"},
            {"label": "C", "text": "直接去找散布流言的人，当面要个说法", "scores": {"S5": 5}, "tendency": "H", "reasoning": "立刻采取最直接行动，不计后果→S5:5"}
        ],
        "reveal": "「好不容易安定下来，好不容易有了许都的军职……没有！！！都是老子自己靠军功和性命堆出来的！」——七载相逢。张辽最不甘心的，是努力被轻易否定。"
    },
    {
        "id": "zhangliao_scheme_01",
        "type": "scheme",
        "dimension": ["S1"],
        "source_character": "张辽",
        "text": "珠履三千中，张辽直接警告你：「这人浑身上下都不可信。满嘴那套方士骗子的天命天道……」指的是你身边的某位谋士。",
        "options": [
            {"label": "A", "text": "不以为意，觉得张辽太武断了", "scores": {"S1": 1}, "tendency": "L", "reasoning": "缺乏警觉，不设防→S1:1"},
            {"label": "B", "text": "嘴上没表态，暗中多留了个心眼观察那人", "scores": {"S1": 3}, "tendency": "M", "reasoning": "有所警觉但不露声色→S1:3"},
            {"label": "C", "text": "反过来问张辽他具体发现了什么，同时不让他打草惊蛇", "scores": {"S1": 5}, "tendency": "H", "reasoning": "深挖情报同时控制信息扩散→S1:5"}
        ],
        "reveal": "「这人浑身上下都不可信。满嘴那套方士骗子的天命天道……」——珠履三千。张辽对人的判断很准，但他通常只说一遍，听不听在你。"
    },
    {
        "id": "zhangliao_scheme_02",
        "type": "scheme",
        "dimension": ["S9"],
        "source_character": "张辽",
        "text": "犬都纪事中，张辽判断局势后冷冷地说：「开战的借口有一千一万种……哼。不可能有尽头的……」有人想借广陵之名开战。",
        "options": [
            {"label": "A", "text": "委屈地说我们明明什么都没做", "scores": {"S9": 1}, "tendency": "L", "reasoning": "用道德视角看问题，缺乏权力意识→S9:1"},
            {"label": "B", "text": "问他那不如将计就计，反过来利用这个借口", "scores": {"S9": 3}, "tendency": "M", "reasoning": "想到利用局势但思路较浅→S9:3"},
            {"label": "C", "text": "问张辽对方的兵力部署，先算清楚值不值得打", "scores": {"S9": 5}, "tendency": "H", "reasoning": "从权力格局出发做理性判断→S9:5"}
        ],
        "reveal": "「开战的借口有一千一万种……哼。不可能有尽头的……」——犬都纪事。张辽看透了权力游戏的本质——想打你不需要理由。"
    },
    {
        "id": "zhangliao_scheme_03",
        "type": "scheme",
        "dimension": ["S6"],
        "source_character": "张辽",
        "text": "左慈-七载相逢中，张辽拔刀挡在你面前：「与其放你回去，再被你牵连，我不如在这就杀了你。」他指的是一个可能连累所有人的俘虏。",
        "options": [
            {"label": "A", "text": "拦住张辽，说不能杀俘虏", "scores": {"S6": 1}, "tendency": "L", "reasoning": "坚守道义底线，不考虑后果→S6:1"},
            {"label": "B", "text": "不表态，看看俘虏是否还有利用价值再决定", "scores": {"S6": 3}, "tendency": "M", "reasoning": "权衡利弊但仍在犹豫→S6:3"},
            {"label": "C", "text": "对张辽说杀不杀由我决定，然后把俘虏单独关押审讯", "scores": {"S6": 5}, "tendency": "H", "reasoning": "果断掌控局面，在底线和现实间找到路径→S6:5"}
        ],
        "reveal": "「……与其放你回去，再被你牵连，我不如在这就杀了你。」——左慈-七载相逢。张辽的底线很清楚：保护自己人的安全高于一切。"
    },
    {
        "id": "zhangliao_scheme_04",
        "type": "scheme",
        "dimension": ["S3"],
        "source_character": "张辽",
        "text": "朝歌之战中，张辽从战场带回一个人，先给她喝米粥养着。吕奉先不理解，张辽只说：「喝了那么多米粥，现在卖太亏了。前面有个黄金市集，能卖出好价。」",
        "options": [
            {"label": "A", "text": "觉得他太冷血了，想帮那个人逃走", "scores": {"S3": 1}, "tendency": "L", "reasoning": "情感优先，忽略实际局势→S3:1"},
            {"label": "B", "text": "看出来他不一定是真想卖人，但不点破", "scores": {"S3": 3}, "tendency": "M", "reasoning": "读懂言外之意但保持务实→S3:3"},
            {"label": "C", "text": "分析战况后建议留着人可能比卖掉更有用，前方缺向导", "scores": {"S3": 5}, "tendency": "H", "reasoning": "从实际利益出发提出更优解→S3:5"}
        ],
        "reveal": "「喝了那么多米粥，现在卖太亏了。前面有个黄金市集，能卖出好价。」——朝歌之战。张辽嘴上说着卖人，实际上一路上护着那个人，最后还托付给了马氏。"
    },
    {
        "id": "zhangliao_daily_01",
        "type": "daily",
        "dimension": ["S8"],
        "source_character": "张辽",
        "text": "张辽在院子里晒太阳，你走过去他也不挪窝，只是把旁边的空地让了让，嘴里嘟囔：「才没有哼！这里有什么好？！东西又贵房子又小，冬天冷夏天热，口音全都听不懂！」",
        "options": [
            {"label": "A", "text": "在旁边坐下，安静地一起晒太阳", "scores": {"S8": 1}, "tendency": "L", "reasoning": "默默陪伴但不主动互动→S8:1"},
            {"label": "B", "text": "把带的点心放在他旁边，说嘴上嫌弃身体倒是很诚实嘛", "scores": {"S8": 3}, "tendency": "M", "reasoning": "用食物和调侃传递关心→S8:3"},
            {"label": "C", "text": "顺势躺下，说那就回西凉吧，一起回去晒那里的太阳", "scores": {"S8": 5}, "tendency": "H", "reasoning": "把他的抱怨变成共同的未来计划→S8:5"}
        ],
        "reveal": "「才没有哼！这里有什么好？！东西又贵房子又小，冬天冷夏天热，口音全都听不懂！」——犬都纪事。张辽嘴上说不想待，身体却一直在你身边没走。"
    },
    {
        "id": "zhangliao_daily_02",
        "type": "daily",
        "dimension": ["S10"],
        "source_character": "张辽",
        "text": "犬都纪事中，张辽听说新君已立，叹了口气：「唉……又要开始劳碌了，唉……」然后停顿了很久：「不打仗了，还要我们武将干什么？」",
        "options": [
            {"label": "A", "text": "说你可以不当武将啊，想做什么做什么", "scores": {"S10": 1}, "tendency": "L", "reasoning": "否定既有秩序，自由散漫→S10:1"},
            {"label": "B", "text": "说你武将不干武将的事，那绣衣楼养你干嘛", "scores": {"S10": 3}, "tendency": "M", "reasoning": "用调侃维持秩序感，半认真半玩笑→S10:3"},
            {"label": "C", "text": "认真地说你的价值不只是打仗，但你需要自己找到新的位置", "scores": {"S10": 5}, "tendency": "H", "reasoning": "重建秩序认知，在变局中找新定位→S10:5"}
        ],
        "reveal": "「唉……又要开始劳碌了，唉……不打仗了，还要我们武将干什么？」——犬都纪事。张辽的焦虑很真实：一个人的全部价值被绑定在一件事上，那件事没了，他是谁？"
    },
    {
        "id": "zhangliao_daily_03",
        "type": "daily",
        "dimension": ["S5"],
        "source_character": "张辽",
        "text": "朝歌之战中，张辽对临时盟友说完「打输了自己找地方逃，打赢了回来烤羊」，就开始检查装备、清点弹药。嘴上随性，手上一点不含糊。",
        "options": [
            {"label": "A", "text": "等他忙完，不打扰他", "scores": {"S5": 1}, "tendency": "L", "reasoning": "被动等待，不主动参与→S5:1"},
            {"label": "B", "text": "过去帮忙清点，顺手问他重骑兵还需要什么补给", "scores": {"S5": 3}, "tendency": "M", "reasoning": "主动加入但跟着他的节奏→S5:3"},
            {"label": "C", "text": "抢过他手里的活说你去烤羊吧，后勤我来", "scores": {"S5": 5}, "tendency": "H", "reasoning": "果断分工，替他分担压力→S5:5"}
        ],
        "reveal": "「打输了自己找地方逃，打赢了回来烤羊。」——朝歌之战。张辽这种人的靠谱之处在于：嘴上越随意，手上越认真。"
    },
    {
        "id": "zhangliao_classic_01",
        "type": "classic",
        "dimension": ["S1"],
        "source_character": "张辽",
        "text": "魂魂版密探剧情，张辽找到你过去的同伴，说：「把话放出去，让广陵王知道又何妨？让那个人知道，养大你的人都不是好得罪的。否则，这种王公贵胄……哼。」",
        "options": [
            {"label": "A", "text": "说不用了，过去的事我不想追究", "scores": {"S1": 1}, "tendency": "L", "reasoning": "主动放弃筹码，不玩权谋→S1:1"},
            {"label": "B", "text": "问他具体打算怎么做，但别把事情闹大", "scores": {"S1": 3}, "tendency": "M", "reasoning": "想知道计划但控制范围→S1:3"},
            {"label": "C", "text": "意识到这是张辽在帮你立威，顺势让他放出消息", "scores": {"S1": 5}, "tendency": "H", "reasoning": "立刻理解棋局并配合行动→S1:5"}
        ],
        "reveal": "「让那个人知道，养大你的人都不是好得罪的。否则，这种王公贵胄……哼。」——魂魂版。张辽在替你打造护身符——让对方知道你有靠山。"
    },
    {
        "id": "zhangliao_classic_02",
        "type": "classic",
        "dimension": ["S10"],
        "source_character": "张辽",
        "text": "犬都纪事中，有人用旧帝生死来试探立场。张辽直接回应：「那个先帝怎么样都不重要了，死心吧。哼。」「黑色灰色什么的根本不重要！重要的是，朝中现在已经有新天子了。」",
        "options": [
            {"label": "A", "text": "小声说你就不念旧情吗", "scores": {"S10": 1}, "tendency": "L", "reasoning": "情感凌驾于现实判断→S10:1"},
            {"label": "B", "text": "点头说局势确实如此，但保留自己的看法", "scores": {"S10": 3}, "tendency": "M", "reasoning": "接受现实但维持独立判断→S10:3"},
            {"label": "C", "text": "认同他的判断，开始讨论如何在新格局中布局", "scores": {"S10": 5}, "tendency": "H", "reasoning": "快速接受新秩序并寻求最优解→S10:5"}
        ],
        "reveal": "「那个先帝怎么样都不重要了，死心吧。哼。」「重要的是，朝中现在已经有新天子了。」——犬都纪事。张辽的忠诚不绑在一个人身上，而是绑在秩序本身。"
    },
    {
        "id": "zhangliao_classic_03",
        "type": "classic",
        "dimension": ["S4"],
        "source_character": "张辽",
        "text": "珠履三千中，张辽对你说：「话里包着话的结果，很可能是脑袋被包进自己肚子里。」他一边警告你小心言辞，一边自己也全是话里有话。",
        "options": [
            {"label": "A", "text": "诚恳地说听不懂，你直接告诉我怎么办", "scores": {"S4": 1}, "tendency": "L", "reasoning": "坦诚不做作，放弃解读→S4:1"},
            {"label": "B", "text": "装作没听懂，但私下按照他暗示的方向去做", "scores": {"S4": 3}, "tendency": "M", "reasoning": "外愚内明，用行动回应暗示→S4:3"},
            {"label": "C", "text": "笑说张辽你这句话本身也包着话，咱俩谁先拆", "scores": {"S4": 5}, "tendency": "H", "reasoning": "用同样的语言游戏反拆他的面具→S4:5"}
        ],
        "reveal": "「话里包着话的结果，很可能是脑袋被包进自己肚子里。」——珠履三千。张辽的幽默方式是：用危险的话题讲道理，讲完道理还在危险里。"
    },
]

# ========== 董奉 ==========
dongfeng_questions = [
    {
        "id": "dongfeng_sweet_01",
        "type": "sweet",
        "dimension": ["S2"],
        "source_character": "董奉",
        "text": "猫邦掌故中，董奉在雨季的旧伤疼痛时说：「孟卓……屋里什么味道，好香……」醒来发现陈登在旁边守着。你看到董奉醒来第一句话不是问自己伤势，而是叫了陈登的名字。",
        "options": [
            {"label": "A", "text": "默默退出去，不打扰他们", "scores": {"S2": 1}, "tendency": "L", "reasoning": "回避情感场景，自觉退让→S2:1"},
            {"label": "B", "text": "轻声说你醒了就好，陈登很担心你", "scores": {"S2": 3}, "tendency": "M", "reasoning": "温和地传递他人的关心→S2:3"},
            {"label": "C", "text": "握住他的手说你不许再瞒着伤势了，我们都心疼", "scores": {"S2": 5}, "tendency": "H", "reasoning": "直接表达情感，不再含蓄→S2:5"}
        ],
        "reveal": "「孟卓……屋里什么味道，好香……」——猫邦掌故。半梦半醒间叫的是故人的名字，闻到的是记忆中的味道。"
    },
    {
        "id": "dongfeng_sweet_02",
        "type": "sweet",
        "dimension": ["S8"],
        "source_character": "董奉",
        "text": "朝歌之战密探剧情中，董奉叮嘱你：「把这个给她。她认得出我串的东西。」又轻声补充：「逃跑的路上，戴着它太招摇了，但是戴了太多年取不下来，就砸碎了。我只留了一半，另外半支没有留。」",
        "options": [
            {"label": "A", "text": "接过那半支信物，说我会替你交给她的", "scores": {"S8": 1}, "tendency": "L", "reasoning": "完成嘱托但保持距离→S8:1"},
            {"label": "B", "text": "看着他手中碎掉的信物，问这东西对你很重要吧", "scores": {"S8": 3}, "tendency": "M", "reasoning": "注意到他的情感但点到为止→S8:3"},
            {"label": "C", "text": "说那我把我的也分你一半，咱俩一人一半扯平了", "scores": {"S8": 5}, "tendency": "H", "reasoning": "用自己的方式回应他的失去→S8:5"}
        ],
        "reveal": "「戴着它太招摇了……但是戴了太多年取不下来，就砸碎了。我只留了一半，另外半支没有留。」——朝歌之战。董奉对旧物的珍重，藏在这些碎片的取舍里。"
    },
    {
        "id": "dongfeng_sweet_03",
        "type": "sweet",
        "dimension": ["S7"],
        "source_character": "董奉",
        "text": "猫邦纪事中，你被卡住了，董奉淡定地说：「对猫来说可是毫不费力哦，但你的骨头太硬了，要不放弃吧？」然后三二一就把你拔出来了。",
        "options": [
            {"label": "A", "text": "爬起来拍拍灰，小声说谢谢", "scores": {"S7": 1}, "tendency": "L", "reasoning": "道谢但不接他的梗→S7:1"},
            {"label": "B", "text": "说你刚才数三二一是认真的吗，又不是在拔萝卜", "scores": {"S7": 3}, "tendency": "M", "reasoning": "用吐槽回应他的冷幽默→S7:3"},
            {"label": "C", "text": "死死拽住他不撒手，说拔都拔了那你得负责把我装回去", "scores": {"S7": 5}, "tendency": "H", "reasoning": "反客为主，把尴尬局面变成撒娇→S7:5"}
        ],
        "reveal": "「三二一……噗叽——好了，握着你的嘴筒子把你拔出来了。」——猫邦纪事。董奉的温柔方式：先损你一句，然后利落地把你捞出来。"
    },
    {
        "id": "dongfeng_funny_01",
        "type": "funny",
        "dimension": ["S7"],
        "source_character": "董奉",
        "text": "朝歌之战中，董奉假装恭敬地说：「奴婢不敢。奴婢怎敢说公子一句的不是。」然后转头就疯狂吐槽你想把李君送人的事，笑得停不下来。",
        "options": [
            {"label": "A", "text": "尴尬地让他别笑了", "scores": {"S7": 1}, "tendency": "L", "reasoning": "被嘲笑后想终止对话→S7:1"},
            {"label": "B", "text": "跟着一起笑，说你笑够了没有，笑够了帮我想个更好的理由", "scores": {"S7": 3}, "tendency": "M", "reasoning": "自嘲并顺势拉他入伙→S7:3"},
            {"label": "C", "text": "面无表情地说奴婢再笑就把你一起送走", "scores": {"S7": 5}, "tendency": "H", "reasoning": "用他的语气反杀，精准打击→S7:5"}
        ],
        "reveal": "「奴婢不敢。奴婢怎敢说公子一句的不是。……你就是想找个由头，把看不上眼的送走……李君……他就是个会说话的木头人。」——朝歌之战。董奉的毒舌从不带恶意，但刀刀见血。"
    },
    {
        "id": "dongfeng_funny_02",
        "type": "funny",
        "dimension": ["S5"],
        "source_character": "董奉",
        "text": "朝歌之战中，董奉一本正经地给你出主意：「公子还记得袁氏那位吗？公子让人照着他的模样，去交州找人，殿下一定喜欢。」",
        "options": [
            {"label": "A", "text": "愣住，不知道他在说什么", "scores": {"S5": 1}, "tendency": "L", "reasoning": "反应迟钝，没跟上节奏→S5:1"},
            {"label": "B", "text": "翻个白眼说你是医师不是媒人，专心看诊", "scores": {"S5": 3}, "tendency": "M", "reasoning": "用吐槽把话题拉回正轨→S5:3"},
            {"label": "C", "text": "立刻反击说那我也给你找一个照着陈登模样的，你喜不喜欢", "scores": {"S5": 5}, "tendency": "H", "reasoning": "瞬间抓住漏洞反向进攻→S5:5"}
        ],
        "reveal": "「公子让人照着袁氏那位的样子，去交州找人，殿下一定喜欢。」——朝歌之战。董奉的损人方式是笑着递刀子，等你反应过来已经中招了。"
    },
    {
        "id": "dongfeng_funny_03",
        "type": "funny",
        "dimension": ["S4"],
        "source_character": "董奉",
        "text": "猫邦掌故中，有人转达陈登对董奉的担心，董奉的回复被别人翻译成了：「告诉这个猫陈登很担心他，让他愧疚！让他下次不要再做这种事！……这样我就可以不用告诉他我也很担心他！」",
        "options": [
            {"label": "A", "text": "点点头说确实不应该让他担心", "scores": {"S4": 1}, "tendency": "L", "reasoning": "只看表面意思，没察觉真实情感→S4:1"},
            {"label": "B", "text": "忍着笑说原来董奉也会口是心非啊", "scores": {"S4": 3}, "tendency": "M", "reasoning": "看穿了面具但不拆穿→S4:3"},
            {"label": "C", "text": "说那我转告陈登，董奉说他也很担心，一字不差地转", "scores": {"S4": 5}, "tendency": "H", "reasoning": "当面拆穿他的伪装，帮他把真心话说出来→S4:5"}
        ],
        "reveal": "「告诉他让他愧疚！……这样我就可以不用告诉他我也很担心他！」——猫邦掌故。董奉的面具是温柔本身——用关心别人的方式藏起自己的脆弱。"
    },
    {
        "id": "dongfeng_funny_04",
        "type": "funny",
        "dimension": ["S3"],
        "source_character": "董奉",
        "text": "月海夜航船中，有人想动手，董奉淡淡地说：「你把弓举过案几的瞬间，脑袋就会变成两半。」然后又加了一句：「劳力者的事，坐幕后的劳心者少管。」",
        "options": [
            {"label": "A", "text": "乖乖放下弓，听他安排", "scores": {"S3": 1}, "tendency": "L", "reasoning": "服从专业判断，不计较→S3:1"},
            {"label": "B", "text": "嘴上说偏不信，但确实收起了弓", "scores": {"S3": 3}, "tendency": "M", "reasoning": "嘴上不服但行动务实→S3:3"},
            {"label": "C", "text": "问他既然是劳力者的事那你这个医师怎么也在操心", "scores": {"S3": 5}, "tendency": "H", "reasoning": "用他自己的逻辑反问他→S3:5"}
        ],
        "reveal": "「你把弓举过案几的瞬间，脑袋就会变成两半。劳力者的事，坐幕后的劳心者少管。」——月海夜航船。董奉不擅长战斗，但他的威慑力来自极度冷静的判断。"
    },
    {
        "id": "dongfeng_angst_01",
        "type": "angst",
        "dimension": ["S6"],
        "source_character": "董奉",
        "text": "朝歌之战密探剧情中，董奉平静地说：「……家奴被打，好像也没什么奇怪的。被打死，好像也不需要理由。」停顿后：「第一次被你打的时候，忽然觉得很冷。说不出来的冷意……真的很奇怪……」",
        "options": [
            {"label": "A", "text": "不敢对上他的眼睛，只说对不起", "scores": {"S6": 1}, "tendency": "L", "reasoning": "愧疚到无法直面，道歉是最低限度的回应→S6:1"},
            {"label": "B", "text": "问他现在还冷不冷，如果是的话你可以暖他", "scores": {"S6": 3}, "tendency": "M", "reasoning": "想弥补但不直接面对伤害本身→S6:3"},
            {"label": "C", "text": "说从今以后不会再有那种冷了，你保证", "scores": {"S6": 5}, "tendency": "H", "reasoning": "做出坚定承诺，用行动划定底线→S6:5"}
        ],
        "reveal": "「第一次被你打的时候，忽然觉得很冷。说不出来的冷意……真的很奇怪……」——朝歌之战。董奉把刻骨的伤害说得轻描淡写，这才是最让人心疼的地方。"
    },
    {
        "id": "dongfeng_angst_02",
        "type": "angst",
        "dimension": ["S2"],
        "source_character": "董奉",
        "text": "七载相逢之秋，董奉面对追兵，冷静地数着距离：「二百……一百八十……一百五十……」最后关头说：「还有二十马步……等我过来——」",
        "options": [
            {"label": "A", "text": "按他的指示快跑，不回头看", "scores": {"S2": 1}, "tendency": "L", "reasoning": "信任他但不表达情感→S2:1"},
            {"label": "B", "text": "边跑边回头喊他自己也快跑", "scores": {"S2": 3}, "tendency": "M", "reasoning": "危急中仍惦记他的安危→S2:3"},
            {"label": "C", "text": "停下来说要么一起走要么一起死，不丢下他", "scores": {"S2": 5}, "tendency": "H", "reasoning": "宁可共死也不分别，情感完全表达→S2:5"}
        ],
        "reveal": "「还有二十马步……等我过来——」——七载相逢之秋。董奉数数的语气很平静，但那个破折号里全是拼命。"
    },
    {
        "id": "dongfeng_angst_03",
        "type": "angst",
        "dimension": ["S5"],
        "source_character": "董奉",
        "text": "左慈-七载相逢中，曹军追来，董奉果断安排：「我让诸葛诞带他们往西走，西边还有生路！快，带左慈上马！」",
        "options": [
            {"label": "A", "text": "听他安排，赶紧上马", "scores": {"S5": 1}, "tendency": "L", "reasoning": "执行命令，不多想→S5:1"},
            {"label": "B", "text": "拉住他问你自己呢，西边真的安全吗", "scores": {"S5": 3}, "tendency": "M", "reasoning": "关心他的安危，想确认计划→S5:3"},
            {"label": "C", "text": "拒绝上马，说除非你跟我一起走", "scores": {"S5": 5}, "tendency": "H", "reasoning": "不接受牺牲式安排，强硬表态→S5:5"}
        ],
        "reveal": "「我让诸葛诞带他们往西走，西边还有生路！快，带左慈上马！」——左慈-七载相逢。董奉安排所有人的退路，唯独没安排自己的。"
    },
    {
        "id": "dongfeng_scheme_01",
        "type": "scheme",
        "dimension": ["S1"],
        "source_character": "董奉",
        "text": "袁基-七载相逢中，董奉面对袁基的招揽，不急不慢地说：「那可不好说，孟卓当年怎么提醒你的？士族家的长公子，是你能随便撩拨了就跑的？」",
        "options": [
            {"label": "A", "text": "没听懂他在暗示什么", "scores": {"S1": 1}, "tendency": "L", "reasoning": "缺乏政治嗅觉→S1:1"},
            {"label": "B", "text": "听出他在替你敲打袁基，但假装没听懂", "scores": {"S1": 3}, "tendency": "M", "reasoning": "理解暗示但选择不介入→S1:3"},
            {"label": "C", "text": "顺势接话，把袁基逼到必须给明确承诺的地步", "scores": {"S1": 5}, "tendency": "H", "reasoning": "利用董奉创造的筹码推进局势→S1:5"}
        ],
        "reveal": "「士族家的长公子，是你能随便撩拨了就跑的？」——袁基-七载相逢。董奉用陈登的忠告当武器，替你守住底线。"
    },
    {
        "id": "dongfeng_scheme_02",
        "type": "scheme",
        "dimension": ["S9"],
        "source_character": "董奉",
        "text": "左慈-七载相逢中，董奉不带感情地分析：「你没有广陵和绣衣楼了。他最多只会庇护你，不会管这里的五万人。」他在说孙策对你的真实价值。",
        "options": [
            {"label": "A", "text": "赌一把他会帮的，毕竟我们有过交情", "scores": {"S9": 1}, "tendency": "L", "reasoning": "用感情赌权力，不理性→S9:1"},
            {"label": "B", "text": "问董奉如果他不帮，还有没有别的退路", "scores": {"S9": 3}, "tendency": "M", "reasoning": "接受现实并寻找备选方案→S9:3"},
            {"label": "C", "text": "说那就制造一个他不得不帮的局面", "scores": {"S9": 5}, "tendency": "H", "reasoning": "主动创造权力筹码，逆转被动局面→S9:5"}
        ],
        "reveal": "「你没有广陵和绣衣楼了。他最多只会庇护你，不会管这里的五万人。」——左慈-七载相逢。董奉的话像手术刀——精准、冷酷、但切掉的是幻想。"
    },
    {
        "id": "dongfeng_scheme_03",
        "type": "scheme",
        "dimension": ["S6"],
        "source_character": "董奉",
        "text": "左慈-七载相逢中，董奉冷冷地说：「违反陈登遗志，就没有资格与我们同行。我会把他们清理掉的。」",
        "options": [
            {"label": "A", "text": "觉得他说得太狠了，人都有苦衷", "scores": {"S6": 1}, "tendency": "L", "reasoning": "宽恕优先，不忍心清理→S6:1"},
            {"label": "B", "text": "问他有没有温和一点的办法，先警告一次", "scores": {"S6": 3}, "tendency": "M", "reasoning": "想找折中方案，底线有弹性→S6:3"},
            {"label": "C", "text": "说陈登的遗志就是我们的底线，该怎么处理你来定", "scores": {"S6": 5}, "tendency": "H", "reasoning": "坚定支持原则，授权执行→S6:5"}
        ],
        "reveal": "「违反陈登遗志，就没有资格与我们同行。我会把他们清理掉的。」——左慈-七载相逢。董奉的温柔只给值得的人，对背叛者他比谁都冷。"
    },
    {
        "id": "dongfeng_scheme_04",
        "type": "scheme",
        "dimension": ["S3"],
        "source_character": "董奉",
        "text": "刘辩-七载相逢中，有人临产，董奉迅速判断：「可能会早产。需要提前准备。她骨架太小，足月后可能难产。」然后开始列物资清单。",
        "options": [
            {"label": "A", "text": "慌了手脚，问怎么办怎么办", "scores": {"S3": 1}, "tendency": "L", "reasoning": "情绪化反应，无法配合→S3:1"},
            {"label": "B", "text": "深呼吸稳住，按他的清单逐项去找", "scores": {"S3": 3}, "tendency": "M", "reasoning": "配合执行，靠谱但被动→S3:3"},
            {"label": "C", "text": "一边帮他准备一边提前清出安全的产房位置，安排人手轮值", "scores": {"S3": 5}, "tendency": "H", "reasoning": "超越指令主动补位，全面准备→S3:5"}
        ],
        "reveal": "「热水，干净的布，小刀……如果有止血的药草就更好了。最重要的是，安静稳定的产房。」——刘辩-七载相逢。董奉在混乱中永远是最冷静的那个人。"
    },
    {
        "id": "dongfeng_daily_01",
        "type": "daily",
        "dimension": ["S8"],
        "source_character": "董奉",
        "text": "猫邦掌故中，董奉说：「雨季，夏天……呼……又困了，可是睡下去，很容易梦见旧事……呼……」",
        "options": [
            {"label": "A", "text": "说那你别睡了，起来喝杯茶提提神", "scores": {"S8": 1}, "tendency": "L", "reasoning": "回避他的噩梦，用行动打断→S8:1"},
            {"label": "B", "text": "坐到他旁边说那我在这里守着，梦见什么醒了都有人", "scores": {"S8": 3}, "tendency": "M", "reasoning": "用陪伴回应，不给压力→S8:3"},
            {"label": "C", "text": "说梦到什么讲出来就不可怕了，我听你说", "scores": {"S8": 5}, "tendency": "H", "reasoning": "主动引导他面对过去，深度共情→S8:5"}
        ],
        "reveal": "「睡下去，很容易梦见旧事……」——猫邦掌故。董奉怕的不是梦，是梦里那些已经回不来的人。"
    },
    {
        "id": "dongfeng_daily_02",
        "type": "daily",
        "dimension": ["S10"],
        "source_character": "董奉",
        "text": "左慈-七载相逢中，董奉自报家门：「杏林君董奉，自徐州广陵来。」又平静地说：「长沙不表态，恐怕会先一步有州内的兵祸。」",
        "options": [
            {"label": "A", "text": "说这些政治的事你不想管，只想大家平安", "scores": {"S10": 1}, "tendency": "L", "reasoning": "回避秩序问题，只想岁月静好→S10:1"},
            {"label": "B", "text": "问他长沙的态度能不能改变，需要做什么", "scores": {"S10": 3}, "tendency": "M", "reasoning": "想维持秩序但缺乏全局观→S10:3"},
            {"label": "C", "text": "说长沙不表态就是在等价而沽，先确保我们自己的退路", "scores": {"S10": 5}, "tendency": "H", "reasoning": "看穿政治逻辑并做出务实判断→S10:5"}
        ],
        "reveal": "「长沙不表态，恐怕会先一步有州内的兵祸。」——左慈-七载相逢。董奉不说废话——他只说局势，剩下的你自己判断。"
    },
    {
        "id": "dongfeng_daily_03",
        "type": "daily",
        "dimension": ["S5"],
        "source_character": "董奉",
        "text": "朝歌之战中，董奉说：「……元龙的病一直反复，我还不能回去。」身为主力医师，他把友情和职责放在个人安危前面。",
        "options": [
            {"label": "A", "text": "说那你注意身体，别把自己也累垮了", "scores": {"S5": 1}, "tendency": "L", "reasoning": "口头关心，没有实际行动→S5:1"},
            {"label": "B", "text": "帮他分担一部分伤员看护工作，让他能休息一会儿", "scores": {"S5": 3}, "tendency": "M", "reasoning": "以实际行动减轻他的负担→S5:3"},
            {"label": "C", "text": "强行让他去睡一觉，剩下的伤员你来盯着", "scores": {"S5": 5}, "tendency": "H", "reasoning": "霸道介入，不许他继续消耗自己→S5:5"}
        ],
        "reveal": "「……元龙的病一直反复，我还不能回去。」——朝歌之战。董奉留在这里不是因为走不了，是因为陈登还在生病，他放不下。"
    },
    {
        "id": "dongfeng_classic_01",
        "type": "classic",
        "dimension": ["S1"],
        "source_character": "董奉",
        "text": "七载相逢之秋中，董奉对陷入执念的人说：「人升天而去，就不在了，彻底不在了。可你若想留下他在今世，他就还会受苦。」又说：「我狠下心了。你只有自己想清楚。」",
        "options": [
            {"label": "A", "text": "说你怎么能这么狠心，人家还在悲痛中", "scores": {"S1": 1}, "tendency": "L", "reasoning": "不理解他的深层用意→S1:1"},
            {"label": "B", "text": "明白他是在用残酷的话帮人放下，但选择沉默", "scores": {"S1": 3}, "tendency": "M", "reasoning": "看懂权谋但不参与→S1:3"},
            {"label": "C", "text": "配合他，补一句执念就是枷锁，越放不下越痛", "scores": {"S1": 5}, "tendency": "H", "reasoning": "理解他的策略并配合推进→S1:5"}
        ],
        "reveal": "「我狠下心了。你只有自己想清楚。」「放下罢。放下了，人心才会好过。还记得怎么哭的人，才能不呕血。」——七载相逢之秋。董奉的狠不是无情，是知道温柔有时候救不了人。"
    },
    {
        "id": "dongfeng_classic_02",
        "type": "classic",
        "dimension": ["S10"],
        "source_character": "董奉",
        "text": "七载相逢之秋，董奉带着五万人逃亡，说：「走吧，殿下。现在出发，日落前还能赶到海西。」又低声：「……是孟卓的灵骨塔……」",
        "options": [
            {"label": "A", "text": "想停下来祭拜陈登", "scores": {"S10": 1}, "tendency": "L", "reasoning": "情感凌驾大局，想暂停行军→S10:1"},
            {"label": "B", "text": "沉默地跟着走，注意到他多看了一眼灵骨塔", "scores": {"S10": 3}, "tendency": "M", "reasoning": "克制情感，服从行军秩序→S10:3"},
            {"label": "C", "text": "说日后再回来好好祭拜，现在先带大家活下去", "scores": {"S10": 5}, "tendency": "H", "reasoning": "在情感和秩序间果断排序→S10:5"}
        ],
        "reveal": "「走吧，殿下。……是孟卓的灵骨塔……」——七载相逢之秋。董奉连经过故人灵骨塔都没有停下，因为他身后还有五万条命。"
    },
    {
        "id": "dongfeng_classic_03",
        "type": "classic",
        "dimension": ["S4"],
        "source_character": "董奉",
        "text": "七载相逢之秋，董奉说：「他们都不在了，我没有任何需要害怕的了。」又说：「……那是我最后一处封地。士燮留过话，我可以将那里当作最后的退路。」",
        "options": [
            {"label": "A", "text": "说你还有我们啊，别说得像孤家寡人", "scores": {"S4": 1}, "tendency": "L", "reasoning": "直球回应，不留余地→S4:1"},
            {"label": "B", "text": "听出他在交代后事，但没有戳破，只是说一起去看看", "scores": {"S4": 3}, "tendency": "M", "reasoning": "理解深层含义但给他留面子→S4:3"},
            {"label": "C", "text": "平静地接他的话，开始讨论那块封地的地形和补给路线", "scores": {"S4": 5}, "tendency": "H", "reasoning": "陪他把遗言说完，用务实方式守护他的体面→S4:5"}
        ],
        "reveal": "「他们都不在了，我没有任何需要害怕的了。」——七载相逢之秋。这句话不是勇敢，是一个人已经没什么可失去时的平静。"
    },
]

# ========== 周忠 ==========
zhongzhong_questions = [
    {
        "id": "zhongzhong_sweet_01",
        "type": "sweet",
        "dimension": ["S2"],
        "source_character": "周忠",
        "text": "燕歌行孙策线中，周忠接到了你的信匆忙赶来，看到你安然无恙后松了口气：「呼，接到了殿下的信，匆匆赶来，还好赶上了。」",
        "options": [
            {"label": "A", "text": "说谢谢你来，然后继续忙自己的事", "scores": {"S2": 1}, "tendency": "L", "reasoning": "轻描淡写地带过他的付出→S2:1"},
            {"label": "B", "text": "说让你担心了，路上还顺利吗", "scores": {"S2": 3}, "tendency": "M", "reasoning": "温和地回应他的关心→S2:3"},
            {"label": "C", "text": "直接拉住他的袖子说以后不许跑这么快来找我，累坏了怎么办", "scores": {"S2": 5}, "tendency": "H", "reasoning": "反客为主地关心他，情感外露→S2:5"}
        ],
        "reveal": "「呼，接到了殿下的信，匆匆赶来，还好赶上了。」——燕歌行孙策线。周忠不擅长说好听的话，但一封信就能让他放下一切赶来。"
    },
    {
        "id": "zhongzhong_sweet_02",
        "type": "sweet",
        "dimension": ["S8"],
        "source_character": "周忠",
        "text": "燕歌行孙策线中，周忠看着疲惫的你轻声说：「你累了。好好歇息吧。」然后：「……嘘，闭上眼睛。」",
        "options": [
            {"label": "A", "text": "闭上眼睛装睡，其实还醒着", "scores": {"S8": 1}, "tendency": "L", "reasoning": "接受温柔但不回应→S8:1"},
            {"label": "B", "text": "乖乖闭眼，嘴角微微翘了一下", "scores": {"S8": 3}, "tendency": "M", "reasoning": "用细微表情回应他的温柔→S8:3"},
            {"label": "C", "text": "抓住他的手不放，说那你得留下来陪我", "scores": {"S8": 5}, "tendency": "H", "reasoning": "主动索取温暖，不给退路→S8:5"}
        ],
        "reveal": "「你累了。好好歇息吧。……嘘，闭上眼睛。」——燕歌行孙策线。周忠的温柔不张扬，像老人的手——粗糙但安稳。"
    },
    {
        "id": "zhongzhong_sweet_03",
        "type": "sweet",
        "dimension": ["S7"],
        "source_character": "周忠",
        "text": "燕歌行孙策线中，周忠看到年轻的小将困得不行，笑着说：「好可爱的小弟弟，你也想好好睡一觉吗？」",
        "options": [
            {"label": "A", "text": "没接话，觉得他只是在跟别人聊天", "scores": {"S7": 1}, "tendency": "L", "reasoning": "不参与互动，旁观→S7:1"},
            {"label": "B", "text": "凑过去学着他的语气说我也好想睡觉，谁让我歇歇", "scores": {"S7": 3}, "tendency": "M", "reasoning": "蹭着他的温柔给自己找个借口撒娇→S7:3"},
            {"label": "C", "text": "直接说他叫谁小弟弟呢，论辈分他还得叫你一声", "scores": {"S7": 5}, "tendency": "H", "reasoning": "用辈分梗反将一军，不留情面→S7:5"}
        ],
        "reveal": "「好可爱的小弟弟，你也想好好睡一觉吗？」——燕歌行孙策线。周忠对年轻人总有一种爷爷式的宠溺，嘴上叫小弟弟，心里是真心疼。"
    },
    {
        "id": "zhongzhong_funny_01",
        "type": "funny",
        "dimension": ["S7"],
        "source_character": "周忠",
        "text": "朝歌之战左慈线中，周忠被左慈打服了，立刻认怂：「好了！是我输了！左慈仙人……看在先王的面子上……看在我也照顾过二位世子的份上……」",
        "options": [
            {"label": "A", "text": "假装没看到他求饶的样子", "scores": {"S7": 1}, "tendency": "L", "reasoning": "给老人留面子，不参与→S7:1"},
            {"label": "B", "text": "憋着笑说你求人的理由倒是现编了一大堆", "scores": {"S7": 3}, "tendency": "M", "reasoning": "含蓄地吐槽他的求生欲→S7:3"},
            {"label": "C", "text": "学着他的语气说看在我也给你递过茶的面子上，你先把欠我的事办了", "scores": {"S7": 5}, "tendency": "H", "reasoning": "有样学样，用他的招数反制→S7:5"}
        ],
        "reveal": "「好了！是我输了！看在先王的面子上……看在我也照顾过二位世子的份上……」——朝歌之战。周忠的求生欲极强，且理由张口就来。"
    },
    {
        "id": "zhongzhong_funny_02",
        "type": "funny",
        "dimension": ["S5"],
        "source_character": "周忠",
        "text": "燕歌行傅融线中，周忠看到诸葛亮的点心想帮忙，但被拒绝了。之后他在旁边不停念叨：「我们都走了，殿下怎么办？」——明明大家都在讨论撤退方案，他却在担心你的安危。",
        "options": [
            {"label": "A", "text": "说我没事你们先走，心里默默感动", "scores": {"S5": 1}, "tendency": "L", "reasoning": "被动接受关心，不主动回应→S5:1"},
            {"label": "B", "text": "笑着说周忠你是想走又舍不得我吧，那就别走了", "scores": {"S5": 3}, "tendency": "M", "reasoning": "用玩笑回应他的牵挂→S5:3"},
            {"label": "C", "text": "拍拍他说放心，我命大得很，你先去安全的地方等我就好", "scores": {"S5": 5}, "tendency": "H", "reasoning": "主动安抚他，用自信打消他的顾虑→S5:5"}
        ],
        "reveal": "「我们都走了，殿下怎么办？」——燕歌行傅融线。周忠在所有人都讨论撤退的时候，唯一在担心的是留下来的人。"
    },
    {
        "id": "zhongzhong_funny_03",
        "type": "funny",
        "dimension": ["S4"],
        "source_character": "周忠",
        "text": "燕歌行袁基线中，周忠假装教你怎么哄袁基：「万一被情人发现自己瞒着他做了点错事该怎么哄。」然后现场示范：「卿卿，我可都是为了你好，我们都可以为了彼此去死，怎能因此事就断绝往来呢？」",
        "options": [
            {"label": "A", "text": "认真记笔记，觉得他说得有道理", "scores": {"S4": 1}, "tendency": "L", "reasoning": "信以为真，完全没看出在演戏→S4:1"},
            {"label": "B", "text": "忍着笑说你这台词太假了，袁基听了会翻脸", "scores": {"S4": 3}, "tendency": "M", "reasoning": "配合演出但保持清醒→S4:3"},
            {"label": "C", "text": "当场拿他练手：周忠你先演袁基，我来试试你教的招好不好使", "scores": {"S4": 5}, "tendency": "H", "reasoning": "用他的游戏规则反将他拉下水→S4:5"}
        ],
        "reveal": "「卿卿，我可都是为了你好，我们都可以为了彼此去死，怎能因此事就断绝往来呢？你可真是绝情之人。」——燕歌行袁基线。周忠这台词写得太好，好到分不清是真情还是演技。"
    },
    {
        "id": "zhongzhong_funny_04",
        "type": "funny",
        "dimension": ["S3"],
        "source_character": "周忠",
        "text": "朝歌之战左慈线中，周忠被制住后突然转变态度：「仙人手下留情吧……里八华的巫也不知还能不能恢复，殿下说得有道理，不如趁此机会脱离……」上一秒还在打，下一秒就倒戈了。",
        "options": [
            {"label": "A", "text": "被他的变脸速度惊到，不知道该信哪句", "scores": {"S3": 1}, "tendency": "L", "reasoning": "困惑，无法判断真假→S3:1"},
            {"label": "B", "text": "默默观察，看他到底是真投降还是缓兵之计", "scores": {"S3": 3}, "tendency": "M", "reasoning": "冷静分析不急于下结论→S3:3"},
            {"label": "C", "text": "直接说周忠你每次倒戈都这么丝滑，这次先表个态我考虑信你", "scores": {"S3": 5}, "tendency": "H", "reasoning": "用他的历史记录当筹码讨价还价→S3:5"}
        ],
        "reveal": "「仙人手下留情吧……不如趁此机会脱离……」——朝歌之战。周忠的务实在于：打不过就加入，活着比面子重要。"
    },
    {
        "id": "zhongzhong_angst_01",
        "type": "angst",
        "dimension": ["S6"],
        "source_character": "周忠",
        "text": "燕歌行袁基线中，周忠直接点破你的把柄：「人家手中捏着两个亲生儿子呢，殿下这样大的把柄。随时都可能被她抖出来……殿下，你还是把老臣教你的话练一下吧。」",
        "options": [
            {"label": "A", "text": "说大不了摊牌，有什么好怕的", "scores": {"S6": 1}, "tendency": "L", "reasoning": "赌气式的无畏，低估风险→S6:1"},
            {"label": "B", "text": "问他如果是他，会怎么处理这个局面", "scores": {"S6": 3}, "tendency": "M", "reasoning": "虚心请教，但还没下定决心→S6:3"},
            {"label": "C", "text": "说把这把柄变成双刃剑，让对方也不敢轻举妄动", "scores": {"S6": 5}, "tendency": "H", "reasoning": "化被动为主动，建立对等威慑→S6:5"}
        ],
        "reveal": "「人家手中捏着两个亲生儿子呢，殿下这样大的把柄。随时都可能被她抖出来。」——燕歌行袁基线。周忠说最狠的话用的是最关心的语气。"
    },
    {
        "id": "zhongzhong_angst_02",
        "type": "angst",
        "dimension": ["S2"],
        "source_character": "周忠",
        "text": "燕歌行傅融线中，密道里水越涨越高。周忠的声音从前方传来：「那，我们在幽州见吗？」——像是在确认一个不确定的约定。",
        "options": [
            {"label": "A", "text": "说嗯，然后各自上路", "scores": {"S2": 1}, "tendency": "L", "reasoning": "简洁回应，压抑情感→S2:1"},
            {"label": "B", "text": "说一定要活着到，少一个人我都不答应", "scores": {"S2": 3}, "tendency": "M", "reasoning": "用要求代替告白→S2:3"},
            {"label": "C", "text": "说不行，我要亲眼看到你安全才放心，你等我", "scores": {"S2": 5}, "tendency": "H", "reasoning": "把分别变成承诺，情感完全摊开→S2:5"}
        ],
        "reveal": "「那，我们在幽州见吗？」——燕歌行傅融线。周忠用疑问句说告别，是因为他不确定自己能不能赴约。"
    },
    {
        "id": "zhongzhong_angst_03",
        "type": "angst",
        "dimension": ["S5"],
        "source_character": "周忠",
        "text": "燕歌行孙策线中，周忠手无缚鸡之力却跑来救援。孙策说：「你手无缚鸡之力，公瑾怎么会让你来救援？」周忠只是笑了笑，说：「将军终于来了……啊……」",
        "options": [
            {"label": "A", "text": "自责不该让他冒险来", "scores": {"S5": 1}, "tendency": "L", "reasoning": "内疚但无力改变→S5:1"},
            {"label": "B", "text": "帮他包扎伤口，问他路上有没有遇到危险", "scores": {"S5": 3}, "tendency": "M", "reasoning": "用照顾回应他的冒险→S5:3"},
            {"label": "C", "text": "说以后不许再这样了，要来也得带着兵马来，不许一个人冲", "scores": {"S5": 5}, "tendency": "H", "reasoning": "霸道地立规矩，不许他再拿命来赌→S5:5"}
        ],
        "reveal": "「将军终于来了……啊……」——燕歌行孙策线。周忠来的时候大概就知道自己帮不上什么忙，但他还是来了。"
    },
    {
        "id": "zhongzhong_scheme_01",
        "type": "scheme",
        "dimension": ["S1"],
        "source_character": "周忠",
        "text": "燕歌行袁基线中，周忠对你的处境了如指掌：「里八华可喜欢这种出身名门的人了，眼下正值局势飘摇之际，她在里面，可是立刻得到重用了。」他在说某个人投靠了里八华的情报。",
        "options": [
            {"label": "A", "text": "问他你说的是谁，怎么从来没跟我说过", "scores": {"S1": 1}, "tendency": "L", "reasoning": "对情报后知后觉，被动接受→S1:1"},
            {"label": "B", "text": "说那你一直在暗中关注里八华的动向", "scores": {"S1": 3}, "tendency": "M", "reasoning": "察觉到他掌握大量情报网→S1:3"},
            {"label": "C", "text": "说这个人的利用价值在哪，能不能反过来用她传假消息", "scores": {"S1": 5}, "tendency": "H", "reasoning": "立刻从情报中找到反制手段→S1:5"}
        ],
        "reveal": "「里八华可喜欢这种出身名门的人了……眼下正值局势飘摇之际，她在里面，可是立刻得到重用了。」——燕歌行袁基线。周忠的情报网络比你想象的要广得多。"
    },
    {
        "id": "zhongzhong_scheme_02",
        "type": "scheme",
        "dimension": ["S9"],
        "source_character": "周忠",
        "text": "燕歌行袁基线中，周忠拦住敌军将领：「不好意思啊，将军。我拿的是活捉的任务。」然后评价道：「真是不通情趣，上来就这么激烈啊……」",
        "options": [
            {"label": "A", "text": "觉得他说话不正经，但人确实拦住了", "scores": {"S9": 1}, "tendency": "L", "reasoning": "只看表面行为，不分析权力动机→S9:1"},
            {"label": "B", "text": "注意到他说的是「活捉」而不是「保护」，意味深长", "scores": {"S9": 3}, "tendency": "M", "reasoning": "听出用词背后的权力关系→S9:3"},
            {"label": "C", "text": "明白他是用任务为借口把保护你的行为合法化，配合他的剧本", "scores": {"S9": 5}, "tendency": "H", "reasoning": "看穿权谋布局并默契配合→S9:5"}
        ],
        "reveal": "「不好意思啊，将军。我拿的是活捉的任务。」——燕歌行袁基线。周忠把保护你包装成任务，让任何人都挑不出毛病。"
    },
    {
        "id": "zhongzhong_scheme_03",
        "type": "scheme",
        "dimension": ["S6"],
        "source_character": "周忠",
        "text": "燕歌行袁基线中，周忠问你：「殿下，如果让他知道你抓走小陈的事，你有何应对吗？」又说：「袁公子怎会和我这样的人计较呢？」",
        "options": [
            {"label": "A", "text": "说没想那么远，到时候再说", "scores": {"S6": 1}, "tendency": "L", "reasoning": "回避问题，不做底线准备→S6:1"},
            {"label": "B", "text": "说你在替我操心袁基的反应吗", "scores": {"S6": 3}, "tendency": "M", "reasoning": "察觉他在试探你的底线→S6:3"},
            {"label": "C", "text": "反问他你觉得袁基知道了会怎样，你肯定已经想好了对策", "scores": {"S6": 5}, "tendency": "H", "reasoning": "把问题推回去，逼他亮底牌→S6:5"}
        ],
        "reveal": "「殿下，如果让他知道你抓走小陈的事，你有何应对吗？」——燕歌行袁基线。周忠的问题从来不是随口问的，每个问题都是在帮你预演最坏的情况。"
    },
    {
        "id": "zhongzhong_scheme_04",
        "type": "scheme",
        "dimension": ["S3"],
        "source_character": "周忠",
        "text": "朝歌之战左慈线中，周忠被打败后迅速判断局势：「好像有马蹄声……在龙脉里？」立即警觉到新的威胁。",
        "options": [
            {"label": "A", "text": "还没反应过来，问他什么马蹄声", "scores": {"S3": 1}, "tendency": "L", "reasoning": "信息滞后，被动跟随→S3:1"},
            {"label": "B", "text": "立刻安静下来仔细听，确认方向和距离", "scores": {"S3": 3}, "tendency": "M", "reasoning": "快速切换到务实判断→S3:3"},
            {"label": "C", "text": "同时观察周围地形找掩体，问他来的人是敌是友", "scores": {"S3": 5}, "tendency": "H", "reasoning": "信息收集+环境评估同步推进→S3:5"}
        ],
        "reveal": "「好像有马蹄声……在龙脉里？」——朝歌之战。周忠的耳朵比眼睛好用，打不赢但跑得快、听得远。"
    },
    {
        "id": "zhongzhong_daily_01",
        "type": "daily",
        "dimension": ["S8"],
        "source_character": "周忠",
        "text": "燕歌行傅融线中，周忠看到故人：「好久不见，二公子。你和你姐姐都还好吗？」语气平淡，但你注意到他问的是「都还好吗」。",
        "options": [
            {"label": "A", "text": "没注意到他的目光，在忙别的事", "scores": {"S8": 1}, "tendency": "L", "reasoning": "忽略了他关心的细节→S8:1"},
            {"label": "B", "text": "轻声说周忠也很久没见到旧友了吧", "scores": {"S8": 3}, "tendency": "M", "reasoning": "注意到他的情感并温和回应→S8:3"},
            {"label": "C", "text": "说等仗打完了，带你去找他们叙旧", "scores": {"S8": 5}, "tendency": "H", "reasoning": "把他的牵挂变成具体的承诺→S8:5"}
        ],
        "reveal": "「好久不见，二公子。你和你姐姐都还好吗？」——燕歌行傅融线。周忠问的是傅融和姐姐，想到的是自己的故人们。"
    },
    {
        "id": "zhongzhong_daily_02",
        "type": "daily",
        "dimension": ["S10"],
        "source_character": "周忠",
        "text": "朝歌之战左慈线中，周忠面对左慈的强大力量，语气变得柔和：「好了！是我输了！左慈仙人……看在先王的面子上……」他用旧主的情面来求情。",
        "options": [
            {"label": "A", "text": "觉得他太没骨气了，打不过就搬出先王", "scores": {"S10": 1}, "tendency": "L", "reasoning": "不理解旧秩序的价值→S10:1"},
            {"label": "B", "text": "理解他在用仅有的筹码保护自己和身边的人", "scores": {"S10": 3}, "tendency": "M", "reasoning": "看到旧情分作为秩序维持的工具→S10:3"},
            {"label": "C", "text": "说先王当年确实对你有知遇之恩，这份情分值得被尊重", "scores": {"S10": 5}, "tendency": "H", "reasoning": "认同旧秩序中的人情价值→S10:5"}
        ],
        "reveal": "「看在先王的面子上……看在我也照顾过二位世子的份上……」——朝歌之战。周忠的世界里，旧主的恩情是最后的通行证。"
    },
    {
        "id": "zhongzhong_daily_03",
        "type": "daily",
        "dimension": ["S5"],
        "source_character": "周忠",
        "text": "燕歌行傅融线中，密道里有人提议把受伤的人丢下，周忠立刻说：「不对！把他丢下！」——等等，他说的是「不对」还是「把他丢下」？语气里明显有犹豫和矛盾。",
        "options": [
            {"label": "A", "text": "没听清，问他在说什么", "scores": {"S5": 1}, "tendency": "L", "reasoning": "没有参与决策的主动性→S5:1"},
            {"label": "B", "text": "说谁都不许丢下，带着一起走", "scores": {"S5": 3}, "tendency": "M", "reasoning": "果断做出决定，不让他纠结→S5:3"},
            {"label": "C", "text": "看穿他的矛盾，拍拍他说你的意思是不丢下对吧，那就这么定了", "scores": {"S5": 5}, "tendency": "H", "reasoning": "替他说出真心话并立刻执行→S5:5"}
        ],
        "reveal": "「不对！把他丢下！」——燕歌行傅融线。周忠在危急关头第一个反应是反对，但说出来的话却暴露了内心的挣扎。"
    },
    {
        "id": "zhongzhong_classic_01",
        "type": "classic",
        "dimension": ["S1"],
        "source_character": "周忠",
        "text": "朝歌之战左慈线中，周忠面对仙人的力量，立刻开始政治斡旋：「好了！是我输了！……不如趁此机会脱离……」同时还在帮左慈分析局势。",
        "options": [
            {"label": "A", "text": "觉得他太圆滑了，看不出真心在谁那边", "scores": {"S1": 1}, "tendency": "L", "reasoning": "对权谋不敏感，只能看到表面→S1:1"},
            {"label": "B", "text": "看出他在两头下注，但暂时不动声色", "scores": {"S1": 3}, "tendency": "M", "reasoning": "读懂棋局但不急于表态→S1:3"},
            {"label": "C", "text": "直接说周忠你又在当双面间谍了，这次站在谁那边", "scores": {"S1": 5}, "tendency": "H", "reasoning": "当面拆穿他的多面下注→S1:5"}
        ],
        "reveal": "周忠在朝歌之战中的表现堪称政治生存教科书：打不过就谈判，谈判中还不忘替所有人找退路。"
    },
    {
        "id": "zhongzhong_classic_02",
        "type": "classic",
        "dimension": ["S10"],
        "source_character": "周忠",
        "text": "燕歌行袁基线中，周忠看着白羽箭若有所思：「……白羽箭？」他在辨认箭的来历，从器物追溯秩序和阵营。",
        "options": [
            {"label": "A", "text": "问他一支箭有什么好想的", "scores": {"S10": 1}, "tendency": "L", "reasoning": "忽略物件的秩序含义→S10:1"},
            {"label": "B", "text": "意识到他在通过箭判断是哪方势力", "scores": {"S10": 3}, "tendency": "M", "reasoning": "跟上他的分析逻辑→S10:3"},
            {"label": "C", "text": "说白羽箭不是寻常军队的配置，这里面的关系不简单", "scores": {"S10": 5}, "tendency": "H", "reasoning": "从物件反推军事编制和权力关系→S10:5"}
        ],
        "reveal": "「……白羽箭？」——燕歌行袁基线。周忠从一个细节就能读出整张局势图，这是多年在权力场中磨出来的嗅觉。"
    },
    {
        "id": "zhongzhong_classic_03",
        "type": "classic",
        "dimension": ["S4"],
        "source_character": "周忠",
        "text": "朝歌之战左慈线中，面对左慈的力量展示，周忠的反应是：「啊。是吗。师父真是太感动了。」——语气平淡到听不出是真感动还是反讽。",
        "options": [
            {"label": "A", "text": "觉得他是真的被感动了", "scores": {"S4": 1}, "tendency": "L", "reasoning": "相信表面，不辨真伪→S4:1"},
            {"label": "B", "text": "拿不准他是真情还是反讽，但选择不追问", "scores": {"S4": 3}, "tendency": "M", "reasoning": "保持模糊，不打破他的面具→S4:3"},
            {"label": "C", "text": "笑着说周忠你这个感动我给六分，演技有待提高", "scores": {"S4": 5}, "tendency": "H", "reasoning": "当面给他打分，用幽默拆穿面具→S4:5"}
        ],
        "reveal": "「啊。是吗。师父真是太感动了。」——朝歌之战。周忠的面具不是冷漠，而是把所有情绪都压缩进同一个平淡的语调里。你永远猜不透他哪句话是真的。"
    },
]

def validate(questions, name):
    dims_count = {}
    types_count = {}
    for q in questions:
        t = q["type"]
        d = q["dimension"][0]
        types_count[t] = types_count.get(t, 0) + 1
        dims_count[d] = dims_count.get(d, 0) + 1
        assert len(q["options"]) == 3
        for opt in q["options"]:
            assert opt["tendency"] in ("L", "M", "H")
            assert list(opt["scores"].keys()) == [d]
            assert list(opt["scores"].values())[0] in (1, 3, 5)
            assert "reasoning" in opt
            assert '"' not in opt["text"]
            assert '"' not in q["text"]
    print(f"{name}: {len(questions)} questions")
    print(f"  Types: {types_count}")
    print(f"  Dims: {dims_count}")

validate(zhangliao_questions, "张辽")
validate(dongfeng_questions, "董奉")
validate(zhongzhong_questions, "周忠")

base = "/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions"
for name, data in [("zhangliao.json", zhangliao_questions), ("dongfeng.json", dongfeng_questions), ("zhongzhong.json", zhongzhong_questions)]:
    path = os.path.join(base, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # verify
    with open(path, "r", encoding="utf-8") as f:
        json.load(f)
    print(f"Written and verified: {path}")
