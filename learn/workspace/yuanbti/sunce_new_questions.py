import json

new_questions = [
  {
    "id": "sunce_scheme_1",
    "type": "scheme",
    "dimension": ["S1"],
    "source_character": "孙策",
    "text": "孙策告诉你袁术逼他来杀你取玉玺，但他不想动手。他说「我明天就跟他翻脸，我保证」。",
    "options": [
      {"label": "A", "text": "信他，直接把自己安危交到他手上", "scores": {"S1": 1}, "tendency": "L", "reasoning": "毫无保留地信任，不做任何后手准备→S1:1"},
      {"label": "B", "text": "说信他，但暗中让陈登准备好城防", "scores": {"S1": 3}, "tendency": "M", "reasoning": "表面信任但留退路，谨慎但不伤感情→S1:3"},
      {"label": "C", "text": "笑着问他「翻脸之后你打算怎么办」，把他的退路也一起算清楚", "scores": {"S1": 5}, "tendency": "H", "reasoning": "主动替他规划全局，把感情和利益统筹考量→S1:5"}
    ],
    "reveal": "「我明天就跟他翻脸！我保证！」——明知得罪袁氏的代价，仍然选择站在你这边"
  },
  {
    "id": "sunce_scheme_2",
    "type": "scheme",
    "dimension": ["S1"],
    "source_character": "孙策",
    "text": "孙策分析天下局势：「袁氏想拥立刘虞为天子，下邳就是鸿门宴，弄不好会血流成河」。他让你不要去下邳。",
    "options": [
      {"label": "A", "text": "听他的，不去下邳", "scores": {"S1": 1}, "tendency": "L", "reasoning": "直接采纳建议，不自己判断局势→S1:1"},
      {"label": "B", "text": "表面答应，但派人暗中调查下邳的真实情况", "scores": {"S1": 3}, "tendency": "M", "reasoning": "不完全依赖单一信息源，自行验证→S1:3"},
      {"label": "C", "text": "反过来利用这个局——既然袁氏要演鸿门宴，不如将计就计反杀", "scores": {"S1": 5}, "tendency": "H", "reasoning": "把危机当棋子，以攻代守反转局势→S1:5"}
    ],
    "reveal": "「下邳就是鸿门宴。弄不好，会血流成河。他们得到刘虞，首当其冲的就是你」——他看穿了整盘棋"
  },
  {
    "id": "sunce_classic_1",
    "type": "classic",
    "dimension": ["S1"],
    "source_character": "孙策",
    "text": "初见孙策，他直说「我上司要杀你，知道袁氏的袁术吧？就是他」。然后大方承认「杀你，顺便打个广陵玩玩」。",
    "options": [
      {"label": "A", "text": "被他气笑了，问他到底想怎样", "scores": {"S1": 1}, "tendency": "L", "reasoning": "情绪化应对，不分析对方真实意图→S1:1"},
      {"label": "B", "text": "观察他的表情和语气，判断他说的是真心话还是试探", "scores": {"S1": 3}, "tendency": "M", "reasoning": "冷静观察对方行为背后的动机→S1:3"},
      {"label": "C", "text": "顺着他的话说「那你动手吧」，赌他不敢真杀", "scores": {"S1": 5}, "tendency": "H", "reasoning": "以攻为守，反向博弈逼对方亮底牌→S1:5"}
    ],
    "reveal": "「打个赌？杀了你，我一样能从广陵正门口出去」——初次见面就敢赌命的江东小霸王"
  },
  {
    "id": "sunce_classic_2",
    "type": "classic",
    "dimension": ["S2"],
    "source_character": "孙策",
    "text": "孙策在西王母庙里说「我有话想同你说，你听了不许笑」。他说「你若是王母座下玄女，我便是猛虎，为你护法」。",
    "options": [
      {"label": "A", "text": "忍住笑，假装没听清让他再说一遍", "scores": {"S2": 1}, "tendency": "L", "reasoning": "用逃避回避他的真情告白→S2:1"},
      {"label": "B", "text": "笑着说「猛虎护法，那我是不是该收你当坐骑」", "scores": {"S2": 3}, "tendency": "M", "reasoning": "用玩笑化解紧张，间接回应→S2:3"},
      {"label": "C", "text": "认真地看着他说「那我也只皈依你」", "scores": {"S2": 5}, "tendency": "H", "reasoning": "同等重量的告白直接回击，不躲不闪→S2:5"}
    ],
    "reveal": "「你若是王母座下玄女，我便是猛虎，为你护法。什么神仙来了，江东孙策都不皈依……我只皈依你」"
  },
  {
    "id": "sunce_angst_1",
    "type": "angst",
    "dimension": ["S2"],
    "source_character": "孙策",
    "text": "孙策说「下次受伤了，别管大伤小伤，都告诉我。我会来你身边的，无论有什么阻碍，我都会来」。",
    "options": [
      {"label": "A", "text": "说「好」，但受了伤还是自己扛着不说", "scores": {"S2": 1}, "tendency": "L", "reasoning": "口头答应但行动上拒绝让对方分担→S2:1"},
      {"label": "B", "text": "笑着说「那我天天受伤，你天天来？」", "scores": {"S2": 3}, "tendency": "M", "reasoning": "用玩笑包装真心话，试探他的认真程度→S2:3"},
      {"label": "C", "text": "握住他的手说「你也一样，不许瞒我」", "scores": {"S2": 5}, "tendency": "H", "reasoning": "直接回应并要求对等的坦诚→S2:5"}
    ],
    "reveal": "「我会来你身边的。无论有什么阻碍，我都会来。因为我对你……嘿嘿，你懂的」"
  },
  {
    "id": "sunce_daily_1",
    "type": "daily",
    "dimension": ["S3"],
    "source_character": "孙策",
    "text": "孙策说「带你去看春日扬州。我知道你去过很多地方，但我保证，江东是世上最好的去处」。",
    "options": [
      {"label": "A", "text": "说「好啊」但心里觉得哪都差不多", "scores": {"S3": 1}, "tendency": "L", "reasoning": "敷衍答应不认真考虑实际安排→S3:1"},
      {"label": "B", "text": "问他江东和广陵有什么不一样的地方", "scores": {"S3": 3}, "tendency": "M", "reasoning": "理性对比再决定，务实但不主动→S3:3"},
      {"label": "C", "text": "直接问「什么时候出发？我需要准备什么？」", "scores": {"S3": 5}, "tendency": "H", "reasoning": "快速进入执行模式，落实到具体行动→S3:5"}
    ],
    "reveal": "「想待多久都可以，待一辈子都可以！……没事，反正我总在江东等你的」"
  },
  {
    "id": "sunce_scheme_3",
    "type": "scheme",
    "dimension": ["S3"],
    "source_character": "孙策",
    "text": "孙策盯着广陵地图分析：「上有幽州侧有袁曹，下路江水横断，右路只能投海。你总窝在这，我不放心」。他提议送你一片江东的地。",
    "options": [
      {"label": "A", "text": "觉得他管太多，婉拒他的提议", "scores": {"S3": 1}, "tendency": "L", "reasoning": "拒绝务实的军事建议，凭感性做判断→S3:1"},
      {"label": "B", "text": "承认他说得有道理，但想先守住广陵试试", "scores": {"S3": 3}, "tendency": "M", "reasoning": "理性听取但选择折中方案→S3:3"},
      {"label": "C", "text": "和他一起研究地图，把两个据点的补给线和退路都算清楚", "scores": {"S3": 5}, "tendency": "H", "reasoning": "主动进行军事可行性分析，量化利弊→S3:5"}
    ],
    "reveal": "「啧啧，广陵郡这地形啊……上有幽州侧有袁曹，你总窝在这，我不放心」——嘴上大大咧咧，地图看得比谁都仔细"
  },
  {
    "id": "sunce_funny_1",
    "type": "funny",
    "dimension": ["S4"],
    "source_character": "孙策",
    "text": "孙策连输十七把五子棋，急得说「下棋好难啊呜呜！我们去下个地方吧」。但你注意到他偷偷把棋子摆回去想重来。",
    "options": [
      {"label": "A", "text": "假装没看见，由着他转移话题", "scores": {"S4": 1}, "tendency": "L", "reasoning": "给对方面子但不参与互动→S4:1"},
      {"label": "B", "text": "把棋子摆正说「输了就是输了，不许赖」", "scores": {"S4": 3}, "tendency": "M", "reasoning": "直接戳穿但带调侃语气→S4:3"},
      {"label": "C", "text": "偷偷也把自己的棋子挪回去几颗，让他赢一把", "scores": {"S4": 5}, "tendency": "H", "reasoning": "完全进入他的游戏规则，配合演戏→S4:5"}
    ],
    "reveal": "「不是我吹啊，我可是号称江东五子棋小霸……啊，我输了……又输了……连输十七把了」"
  },
  {
    "id": "sunce_angst_2",
    "type": "angst",
    "dimension": ["S4"],
    "source_character": "孙策",
    "text": "孙策半夜磨镜子，说「其实挺有意思……算了说实话吧，挺没劲的」。他嘴上赶你走，但你转身时他又说「啥？你想留下看？」",
    "options": [
      {"label": "A", "text": "听他的话去客房休息", "scores": {"S4": 1}, "tendency": "L", "reasoning": "只听字面意思，不解读真实心意→S4:1"},
      {"label": "B", "text": "停住脚步回头看他一眼，等他再说一遍", "scores": {"S4": 3}, "tendency": "M", "reasoning": "察觉到口是心非但让他自己主动→S4:3"},
      {"label": "C", "text": "直接坐过去说「你就是想让我留下吧」", "scores": {"S4": 5}, "tendency": "H", "reasoning": "当场拆穿他的傲娇，主动拉近距离→S4:5"}
    ],
    "reveal": "「夜深了，快让人带你去客房歇息……啥？你想留下看？嘿……来来来！坐过来！」"
  },
  {
    "id": "sunce_daily_2",
    "type": "daily",
    "dimension": ["S4"],
    "source_character": "孙策",
    "text": "孙策嘴上说「我第一次和女孩子走太慢没有气势，我走快点不能等你了」，走了两步就放慢了。",
    "options": [
      {"label": "A", "text": "跟上他的步子，不拆穿", "scores": {"S4": 1}, "tendency": "L", "reasoning": "配合他的嘴硬，不去戳破→S4:1"},
      {"label": "B", "text": "故意走更慢，看他会不会回头", "scores": {"S4": 3}, "tendency": "M", "reasoning": "小小地测试一下他的真实态度→S4:3"},
      {"label": "C", "text": "挽住他胳膊说「那一起走不就好了」", "scores": {"S4": 5}, "tendency": "H", "reasoning": "直接用行动破解他的口是心非→S4:5"}
    ],
    "reveal": "「我第一次和女孩子一起走……嘿嘿……等你的等你的，我走慢点」"
  },
  {
    "id": "sunce_funny_2",
    "type": "funny",
    "dimension": ["S5"],
    "source_character": "孙策",
    "text": "看摔跤比赛时孙策跃跃欲试，说「那个花腰带的人看起来强，我都想亲自上阵比试了」。你让他去他就真的跑去报名了。",
    "options": [
      {"label": "A", "text": "拦住他「你冷静点，我们还有别的摊位没逛」", "scores": {"S5": 1}, "tendency": "L", "reasoning": "用理性压制冲动，优先完成计划→S5:1"},
      {"label": "B", "text": "说「去吧去吧」，然后在场边给他加油", "scores": {"S5": 3}, "tendency": "M", "reasoning": "支持但保持旁观者姿态→S5:3"},
      {"label": "C", "text": "跟着一起去报名「我也来！」", "scores": {"S5": 5}, "tendency": "H", "reasoning": "同等行动力直接加入，不讲废话→S5:5"}
    ],
    "reveal": "「你让我亲自上？上就上，等我去那边报名！」——说风就是雨的行动派"
  },
  {
    "id": "sunce_daily_3",
    "type": "daily",
    "dimension": ["S5"],
    "source_character": "孙策",
    "text": "孙策在夜市钓鱼钓不到，直接拍金块在桌上说「老板这金块给你！我徒手抓！」",
    "options": [
      {"label": "A", "text": "拉住他说「别闹了，鱼我请你吃」", "scores": {"S5": 1}, "tendency": "L", "reasoning": "阻止他的疯狂举动，走正常途径解决→S5:1"},
      {"label": "B", "text": "在旁边看热闹，随时准备捞他", "scores": {"S5": 3}, "tendency": "M", "reasoning": "不阻止但保持旁观，适度放任→S5:3"},
      {"label": "C", "text": "撸袖子「我帮你一起抓！」", "scores": {"S5": 5}, "tendency": "H", "reasoning": "直接跟他一起疯，行动力满格→S5:5"}
    ],
    "reveal": "「老子就不信今天抓不到鱼！老板，这金块给你！我徒手抓！」"
  },
  {
    "id": "sunce_classic_3",
    "type": "classic",
    "dimension": ["S5"],
    "source_character": "孙策",
    "text": "孙策说「那待会儿我们一起跳下去？我托着你，你就像乘在一朵云上，呼的一下就下凡啦」。",
    "options": [
      {"label": "A", "text": "摇头说「太高了，我不敢」", "scores": {"S5": 1}, "tendency": "L", "reasoning": "被恐惧支配不敢行动→S5:1"},
      {"label": "B", "text": "犹豫一下说「你真接得住我？」", "scores": {"S5": 3}, "tendency": "M", "reasoning": "想试但需要确认安全才敢动→S5:3"},
      {"label": "C", "text": "直接跳了", "scores": {"S5": 5}, "tendency": "H", "reasoning": "信任到不犹豫，说跳就跳→S5:5"}
    ],
    "reveal": "「我托着你，不管从多高的地方落下去，都不会让你伤到一点的」——他说的就是承诺"
  },
  {
    "id": "sunce_angst_3",
    "type": "angst",
    "dimension": ["S6"],
    "source_character": "孙策",
    "text": "孙策知道你受伤后带兵清剿残军，说「他们伤了你，就一个都别想跑」。天没亮他就进山把人收拾干净了。",
    "options": [
      {"label": "A", "text": "训他「你不用为我冒这个险」", "scores": {"S6": 1}, "tendency": "L", "reasoning": "压抑对方的保护欲，把底线设得很低→S6:1"},
      {"label": "B", "text": "心疼他跑了一夜没睡，但心里觉得他做得没错", "scores": {"S6": 3}, "tendency": "M", "reasoning": "理解但不完全认同他的极端方式→S6:3"},
      {"label": "C", "text": "一句话不说，给他热一碗粥端过去", "scores": {"S6": 5}, "tendency": "H", "reasoning": "默认他的行为合理，用行动支持→S6:5"}
    ],
    "reveal": "「趁着破晓，我带兵进了林子，把里头的残军给收拾干净了。他们伤了你，就一个都别想跑」"
  },
  {
    "id": "sunce_classic_4",
    "type": "classic",
    "dimension": ["S6"],
    "source_character": "孙策",
    "text": "孙策从回忆里说起父母：「他们在军队经过吴郡的途中成婚，万事从简，只沿途栽了一棵海棠当作信物。后来三军回吴，战事所过之处一片废墟，只有海棠依旧」。",
    "options": [
      {"label": "A", "text": "说「战争就是这样，没什么好感慨的」", "scores": {"S6": 1}, "tendency": "L", "reasoning": "对感情和记忆的分量无感，底线松→S6:1"},
      {"label": "B", "text": "静静听完，说「那棵海棠很厉害」", "scores": {"S6": 3}, "tendency": "M", "reasoning": "尊重他的记忆但没有深入共鸣→S6:3"},
      {"label": "C", "text": "说「以后我也给你种一棵，比海棠活得还久」", "scores": {"S6": 5}, "tendency": "H", "reasoning": "用同等重量的承诺回应他的深情→S6:5"}
    ],
    "reveal": "「后来三军回吴，战事所过之处一片废墟，只有海棠依旧」——他记住了那棵树，就像记住所有重要的东西"
  },
  {
    "id": "sunce_scheme_4",
    "type": "scheme",
    "dimension": ["S6"],
    "source_character": "孙策",
    "text": "孙策说「权力对我来说太可怕了，比毒药还会腐蚀人心。所以我想打下天下，对权力倒是没什么兴趣」。",
    "options": [
      {"label": "A", "text": "半信半疑，打天下的人怎么可能对权力没兴趣", "scores": {"S6": 1}, "tendency": "L", "reasoning": "怀疑他的动机，不信任他说的底线→S6:1"},
      {"label": "B", "text": "觉得有道理，但想看看他以后会不会变", "scores": {"S6": 3}, "tendency": "M", "reasoning": "理解但保留判断，让时间验证→S6:3"},
      {"label": "C", "text": "信他，因为他连这种话都敢说出口", "scores": {"S6": 5}, "tendency": "H", "reasoning": "完全信任他的底线，不怀疑不试探→S6:5"}
    ],
    "reveal": "「绝大多数人心里想的是自己想要天下和权力吧。不过，权力对我来说太可怕了」——乱世里最清醒的理想主义"
  },
  {
    "id": "sunce_funny_3",
    "type": "funny",
    "dimension": ["S7"],
    "source_character": "孙策",
    "text": "孙策把鲁班锁研究半天搞不定，最后直接劈开了说「大力出奇迹！」。然后问九连环是不是也能大力出奇迹。",
    "options": [
      {"label": "A", "text": "默默把他劈碎的鲁班锁收起来，叹口气", "scores": {"S7": 1}, "tendency": "L", "reasoning": "无奈但不反驳，回避冲突→S7:1"},
      {"label": "B", "text": "笑着说「你跟这锁有仇啊？」", "scores": {"S7": 3}, "tendency": "M", "reasoning": "用玩笑回应暴力美学，适度表达态度→S7:3"},
      {"label": "C", "text": "把九连环也递给他「来，再劈一个」", "scores": {"S7": 5}, "tendency": "H", "reasoning": "全力配合他的狂野风格，火上浇油→S7:5"}
    ],
    "reveal": "「大力出奇迹！喝！——看，直接一劈二就好了。还有个九连环？要不还是大力出奇迹？」"
  },
  {
    "id": "sunce_classic_5",
    "type": "classic",
    "dimension": ["S7"],
    "source_character": "孙策",
    "text": "一群人围观你和孙策走在一起，他大声说「一群八卦，有什么好看的，没见过郎才女貌啊？你走近点，给他们开开眼！」",
    "options": [
      {"label": "A", "text": "往他身后躲一躲，不想被看", "scores": {"S7": 1}, "tendency": "L", "reasoning": "回避关注，不想成为焦点→S7:1"},
      {"label": "B", "text": "笑一笑走过去，不刻意靠近也不躲", "scores": {"S7": 3}, "tendency": "M", "reasoning": "自然应对但不主动制造场面→S7:3"},
      {"label": "C", "text": "直接挽住他胳膊，对着人群笑", "scores": {"S7": 5}, "tendency": "H", "reasoning": "比他更嚣张，大方展示→S7:5"}
    ],
    "reveal": "「一群八卦，有什么好看的，没见过郎才女貌啊？走走走，别看他们了，看我」"
  },
  {
    "id": "sunce_daily_4",
    "type": "daily",
    "dimension": ["S8"],
    "source_character": "孙策",
    "text": "孙策吃饭特别快，但这次说「我吃完啦你慢慢吃，我等别人吃完等习惯啦，你不用急」。然后又跑去买新出炉的饭包。",
    "options": [
      {"label": "A", "text": "加快速度吃完", "scores": {"S8": 1}, "tendency": "L", "reasoning": "不领受对方的体贴，反而配合对方节奏→S8:1"},
      {"label": "B", "text": "说「不急，你买的那个分我一半」", "scores": {"S8": 3}, "tendency": "M", "reasoning": "接受他的等待，用分享回应关心→S8:3"},
      {"label": "C", "text": "放下筷子看着他「你等我的时候在干什么？有没有无聊？」", "scores": {"S8": 5}, "tendency": "H", "reasoning": "主动关心他等人的感受，体贴入微→S8:5"}
    ],
    "reveal": "「我吃饭太快了，等别人吃完等习惯啦，你不用急。……等等，那个新出炉的饭包一定也很好吃！」"
  },
  {
    "id": "sunce_angst_4",
    "type": "angst",
    "dimension": ["S8"],
    "source_character": "孙策",
    "text": "雪地里孙策问「你冷不冷？冷的话我们再挨紧一些」。然后安静地说「这样可真暖和……都不想分开了」。",
    "options": [
      {"label": "A", "text": "说「不冷」就继续看雪", "scores": {"S8": 1}, "tendency": "L", "reasoning": "否认感受，拒绝亲密→S8:1"},
      {"label": "B", "text": "把围巾解下来一半搭在他肩上", "scores": {"S8": 3}, "tendency": "M", "reasoning": "用小动作表达关心，温柔但含蓄→S8:3"},
      {"label": "C", "text": "靠在他肩上说「那就不分开」", "scores": {"S8": 5}, "tendency": "H", "reasoning": "直接回应他的温柔，用肢体语言确认→S8:5"}
    ],
    "reveal": "「你冷不冷？冷的话，我们再挨紧一些。这样可真暖和……都不想分开了」"
  },
  {
    "id": "sunce_classic_6",
    "type": "classic",
    "dimension": ["S9"],
    "source_character": "孙策",
    "text": "孙策说「那我帮你把广陵攻下来，你若真随我回去，你停留在哪，我就让哪改名广陵」。他把玉玺的事当笑话处理。",
    "options": [
      {"label": "A", "text": "觉得他在吹牛，笑笑就好", "scores": {"S9": 1}, "tendency": "L", "reasoning": "不在意权力交换，当耳边风→S9:1"},
      {"label": "B", "text": "认真想了一下说「那我要挑个风水好的地方」", "scores": {"S9": 3}, "tendency": "M", "reasoning": "把权力承诺当有趣的交易，半认真半玩→S9:3"},
      {"label": "C", "text": "说「那我也要给江东改个名字」", "scores": {"S9": 5}, "tendency": "H", "reasoning": "对等交换权力象征，在权力关系中要求平等→S9:5"}
    ],
    "reveal": "「你若真随我回去，你停留在哪，我就让哪改名广陵。那我还真的想攻城略地，把这广陵……攻下来」"
  },
  {
    "id": "sunce_scheme_5",
    "type": "scheme",
    "dimension": ["S9"],
    "source_character": "孙策",
    "text": "绒绒版世界线里，孙策说「先称霸天下，再去实现那个什么村」。被问起权力时他说「权力比毒药还可怕」。",
    "options": [
      {"label": "A", "text": "觉得他在自我矛盾，称霸却不要权力？", "scores": {"S9": 1}, "tendency": "L", "reasoning": "质疑他的权力观，认为他在自欺→S9:1"},
      {"label": "B", "text": "理解他的意思——打天下是为了守护而非统治", "scores": {"S9": 3}, "tendency": "M", "reasoning": "理解权力作为工具而非目的的逻辑→S9:3"},
      {"label": "C", "text": "说「那我帮你守着，免得权力反噬你」", "scores": {"S9": 5}, "tendency": "H", "reasoning": "主动参与权力制衡，成为他的安全阀→S9:5"}
    ],
    "reveal": "「我想打下天下，对权力倒是没什么兴趣……就算我打下了天下，最终也是想天下太平的汪！」"
  },
  {
    "id": "sunce_daily_5",
    "type": "daily",
    "dimension": ["S10"],
    "source_character": "孙策",
    "text": "七夕夜市上，你和孙策把靶子射断了，老板看过来。孙策小声说「我们溜吧？」",
    "options": [
      {"label": "A", "text": "拉着他就跑", "scores": {"S10": 1}, "tendency": "L", "reasoning": "无规则意识，跟着一起逃→S10:1"},
      {"label": "B", "text": "留几枚钱在摊位上当赔偿，然后再跑", "scores": {"S10": 3}, "tendency": "M", "reasoning": "闯祸了但补一点，边跑边补救→S10:3"},
      {"label": "C", "text": "留下来跟老板道歉赔偿", "scores": {"S10": 5}, "tendency": "H", "reasoning": "面对后果不逃避，守规则→S10:5"}
    ],
    "reveal": "「啊……我们使的力太大了……靶子裂开了……老板看过来了，我们……我们溜吧？」"
  },
  {
    "id": "sunce_funny_4",
    "type": "funny",
    "dimension": ["S10"],
    "source_character": "孙策",
    "text": "孙策发现娇耳店的老板作弊——把五铢钱饺子藏起来只给赏钱多的桌。他当场喊「掀桌！」",
    "options": [
      {"label": "A", "text": "跟着喊「掀桌！」", "scores": {"S10": 1}, "tendency": "L", "reasoning": "看到不公直接暴力解决，不顾规则→S10:1"},
      {"label": "B", "text": "拉住他说「别掀，让老板把饺子拿出来就行」", "scores": {"S10": 3}, "tendency": "M", "reasoning": "纠正不公但用协商方式→S10:3"},
      {"label": "C", "text": "冷静地说「老板，退钱，不然报官」", "scores": {"S10": 5}, "tendency": "H", "reasoning": "用规则和制度手段处理，不走极端→S10:5"}
    ],
    "reveal": "「啊！我刚才瞥见了，他把五铢钱饺子藏起来了，哪桌赏钱多给哪桌，太狡猾了！掀桌！」"
  }
]

from collections import Counter
dims = Counter()
for q in new_questions:
    for d in q['dimension']:
        dims[d] += 1
print(f"New: {dict(dims)}, Total new: {len(new_questions)}")

with open('questions/sunce.json') as f:
    existing = json.load(f)

all_dims = Counter()
for q in existing:
    for d in q['dimension']:
        all_dims[d] += 1
for q in new_questions:
    for d in q['dimension']:
        all_dims[d] += 1
print(f"Total after merge: {len(existing) + len(new_questions)}")
print(f"All dims: {dict(all_dims)}")

existing.extend(new_questions)
with open('questions/sunce.json', 'w') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)
print("Done!")
