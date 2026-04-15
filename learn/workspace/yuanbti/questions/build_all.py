import json

filepath = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/furong.json'
with open(filepath, 'r') as f:
    data = json.load(f)

# Add batches 2-5
new_questions = [
  # === Batch 2: funny ===
  {
    "id": "furong_funny_01", "type": "funny", "dimension": ["S7"], "source_character": "傅融",
    "text": "傅融在学宫恶作剧环节犹豫半天，最终只把木案「稍稍往旁边挪歪了一点点」。你看着他如临大敌的样子。",
    "options": [
      {"label": "A", "text": "帮他把木案挪正，说算了别恶作剧了", "scores": {"S7": 1}, "tendency": "L", "reasoning": "按部就班不敢越界→S7:1"},
      {"label": "B", "text": "自己也挪歪一个花瓶，说这叫双人配合恶作剧", "scores": {"S7": 3}, "tendency": "M", "reasoning": "小范围配合，不冒大险→S7:3"},
      {"label": "C", "text": "直接把整排木案都挪歪，拉着他一起跑路", "scores": {"S7": 5}, "tendency": "H", "reasoning": "大胆升级恶作剧规模→S7:5"}
    ],
    "reveal": "「要把房间弄乱吗……虽然是猫族天性，但是……但是……就……把这个木案，稍稍的……往旁边挪歪一点点吧……」"
  },
  {
    "id": "furong_funny_02", "type": "funny", "dimension": ["S5"], "source_character": "傅融",
    "text": "傅融看到七夕射箭摊位，开始疯狂计算套餐性价比。你说你射箭很准，他半信半疑地又买了一次箭。",
    "options": [
      {"label": "A", "text": "老老实实说不太有把握，别浪费钱了", "scores": {"S5": 1}, "tendency": "L", "reasoning": "保守退缩，不做尝试→S5:1"},
      {"label": "B", "text": "说试试看吧，射不准就当玩了", "scores": {"S5": 3}, "tendency": "M", "reasoning": "愿意尝试但降低预期→S5:3"},
      {"label": "C", "text": "直接拉开弓连射三箭，用实力让他闭嘴", "scores": {"S5": 5}, "tendency": "H", "reasoning": "果敢行动，用结果说话→S5:5"}
    ],
    "reveal": "「……真的有把握吗？你有把握的话，我就再去买一次箭？……七环、十环、十环……不错嘛，算准箭角了？你看，老板要哭了。」"
  },
  {
    "id": "furong_funny_03", "type": "funny", "dimension": ["S3"], "source_character": "傅融",
    "text": "傅融发现糕点铺的全糖和无糖一个价，当场觉得不合理要找老板理论。你拉住他。",
    "options": [
      {"label": "A", "text": "随他去吧，让老板感受一下傅校尉的物价管理", "scores": {"S3": 1}, "tendency": "L", "reasoning": "放任不管，不做干预→S3:1"},
      {"label": "B", "text": "给他买个别的口味转移注意力", "scores": {"S3": 3}, "tendency": "M", "reasoning": "变通处理，用替代方案化解→S3:3"},
      {"label": "C", "text": "拉着他一起分析成本结构，帮他写一份物价报告", "scores": {"S3": 5}, "tendency": "H", "reasoning": "系统性地解决问题→S3:5"}
    ],
    "reveal": "「明明一样的钱，为什么全糖和无糖一个价？至少扣掉糖的差价啊。」——傅校尉的物价正义感，让全广陵的商贩闻风丧胆。"
  },
  {
    "id": "furong_funny_04", "type": "funny", "dimension": ["S4"], "source_character": "傅融",
    "text": "听经课上傅融自带了算盘认真做笔记，结果不知不觉开始清起了账。你发现他在桌案下偷偷打算盘。",
    "options": [
      {"label": "A", "text": "轻轻碰他一下示意他认真听课", "scores": {"S4": 1}, "tendency": "L", "reasoning": "维持规矩不破坏形象→S4:1"},
      {"label": "B", "text": "偷偷把自己那页经书推过去盖住他的算盘", "scores": {"S4": 3}, "tendency": "M", "reasoning": "用小动作帮他掩饰→S4:3"},
      {"label": "C", "text": "凑过去和他一起算，反正这课也没在听", "scores": {"S4": 5}, "tendency": "H", "reasoning": "公然放弃伪装，直接加入→S4:5"}
    ],
    "reveal": "「我带了算盘……为什么要带算盘？因为今天是算经课，来前我看过课表的。三下五去二、七上二去五进一……喵？不知不觉怎么清起账来了……」"
  },
  {
    "id": "furong_funny_05", "type": "funny", "dimension": ["S2"], "source_character": "傅融",
    "text": "七夕夜市看到竹筒饭摊位，傅融眼睛发亮说以后不当密探要去摆摊，还规划了亲子套餐、情侣套餐。你看着满眼是商机算盘的他。",
    "options": [
      {"label": "A", "text": "说别想了好好当密探吧，摆摊不稳定", "scores": {"S2": 1}, "tendency": "L", "reasoning": "用现实打断对方的畅想→S2:1"},
      {"label": "B", "text": "说那我当你的第一个客人，先赊账", "scores": {"S2": 3}, "tendency": "M", "reasoning": "配合畅想但保持调侃距离→S2:3"},
      {"label": "C", "text": "说我帮你算账，咱们以后一起摆摊过日子", "scores": {"S2": 5}, "tendency": "H", "reasoning": "把对方的小梦想变成共同的未来→S2:5"}
    ],
    "reveal": "「如果以后不当密探，我也推一台木车，夜市摆摊卖竹筒饭。竹筒饭携带方便，便宜，香味浓……到时候可以出亲子套餐、饮料套餐、情侣套餐……」"
  },
  {
    "id": "furong_funny_06", "type": "funny", "dimension": ["S6"], "source_character": "傅融",
    "text": "傅融在七夕角抵场连赢两把，果断收手说不赌了。旁边有人嘲讽他胆小不敢继续下注。",
    "options": [
      {"label": "A", "text": "拉着傅融离开，不值得和这种人纠缠", "scores": {"S6": 1}, "tendency": "L", "reasoning": "回避冲突，退让为安→S6:1"},
      {"label": "B", "text": "替他回一句：见好就收才是本事，你行你上", "scores": {"S6": 3}, "tendency": "M", "reasoning": "适度还击但不过激→S6:3"},
      {"label": "C", "text": "拿出全部筹码押下一把，赢了加倍怼回去", "scores": {"S6": 5}, "tendency": "H", "reasoning": "正面硬刚用实力回应挑衅→S6:5"}
    ],
    "reveal": "「啊……又赢了！见好就收，我不赌了。」——傅融的赌博哲学：赢够了就跑，绝不贪心。"
  },
  # === Batch 3: angst ===
  {
    "id": "furong_angst_01", "type": "angst", "dimension": ["S6"], "source_character": "傅融",
    "text": "傅融说如果需要牺牲一只猫去拯救天下，他拒绝。「凭什么一只猫就要为了天下猫牺牲。」他看向你。",
    "options": [
      {"label": "A", "text": "沉默不语，觉得他说得有道理但不敢附和", "scores": {"S6": 1}, "tendency": "L", "reasoning": "回避立场表态，不触碰核心价值→S6:1"},
      {"label": "B", "text": "说如果非要选，你希望他活下去", "scores": {"S6": 3}, "tendency": "M", "reasoning": "表达个人立场但不涉及宏大命题→S6:3"},
      {"label": "C", "text": "握住他的手说不会让任何人牺牲，包括他", "scores": {"S6": 5}, "tendency": "H", "reasoning": "坚定许下保护承诺，对抗命运论→S6:5"}
    ],
    "reveal": "「我拒绝。很奇怪吗？凭什么一只猫就要为了天下猫牺牲。……到那一天，我们能站一边，变成两只活下去的猫吗？」"
  },
  {
    "id": "furong_angst_02", "type": "angst", "dimension": ["S2"], "source_character": "傅融",
    "text": "离别前傅融说「没关系啊，你会来看我的」，然后又改口说「我不是一定要你来看我」。你听出了他话里的不安。",
    "options": [
      {"label": "A", "text": "说嗯会的，然后低下头不让他看到表情", "scores": {"S2": 1}, "tendency": "L", "reasoning": "给出承诺但回避深层情感交流→S2:1"},
      {"label": "B", "text": "用力点头，说一定会的，你别想太多", "scores": {"S2": 3}, "tendency": "M", "reasoning": "用肯定回应他的不安但不深入→S2:3"},
      {"label": "C", "text": "抱住他说不准说这种话，我哪儿都不让你去", "scores": {"S2": 5}, "tendency": "H", "reasoning": "用行动否定分离可能，全情投入→S2:5"}
    ],
    "reveal": "「没关系啊，你会来看我的。……啊，我不是一定要你来看我……总之……你会想起来的时候来看看我的……会的，对吧？」"
  },
  {
    "id": "furong_angst_03", "type": "angst", "dimension": ["S4"], "source_character": "傅融",
    "text": "傅融受了伤被你发现了，他说是刚才走路不小心磕的。但你看到伤口分明是刀伤。",
    "options": [
      {"label": "A", "text": "接受他的说法，帮他要些药膏来", "scores": {"S4": 1}, "tendency": "L", "reasoning": "接受面具解释，不追问→S4:1"},
      {"label": "B", "text": "不拆穿但默默帮他处理伤口，比平时更仔细", "scores": {"S4": 3}, "tendency": "M", "reasoning": "不戳破谎言但用行动表达在意→S4:3"},
      {"label": "C", "text": "直接撸起他袖子说骗谁呢，老实交代怎么受的伤", "scores": {"S4": 5}, "tendency": "H", "reasoning": "正面拆穿伪装，要求坦诚→S4:5"}
    ],
    "reveal": "「哼……怕你在外面出什么事，影响行动进度。」——他把担心包装成工作汇报，傅校尉的体贴永远带着绩效考核的味道。"
  },
  {
    "id": "furong_angst_04", "type": "angst", "dimension": ["S8"], "source_character": "傅融",
    "text": "深夜傅融一个人在院子里给飞云重新画被踩坏的灯笼花，嘴里念叨着「多可爱啊你看，给它穿个红棉袄」。你站在远处看着。",
    "options": [
      {"label": "A", "text": "默默回屋，让他一个人待着", "scores": {"S8": 1}, "tendency": "L", "reasoning": "给予空间但不给予陪伴→S8:1"},
      {"label": "B", "text": "悄悄走过去递杯热水，不说话陪在旁边", "scores": {"S8": 3}, "tendency": "M", "reasoning": "无声陪伴，不强求交流→S8:3"},
      {"label": "C", "text": "蹲下来接过画笔说一起画，红棉袄太丑了换你画", "scores": {"S8": 5}, "tendency": "H", "reasoning": "主动分担他的脆弱时刻→S8:5"}
    ],
    "reveal": "「看看还能不能补救……把那团红的改画成红衣小人?不不不更恐怖了……多可爱啊你看，给它穿个红棉袄……实在不行重新画一张吧……不要哭了。」"
  },
  {
    "id": "furong_angst_05", "type": "angst", "dimension": ["S7"], "source_character": "傅融",
    "text": "傅融在犬都之战后，面对房屋被毁、房贷还在的现实，当着你的面崩溃了。「雒阳的房贷和首付啊啊——」",
    "options": [
      {"label": "A", "text": "说会帮他想想办法，先冷静一下", "scores": {"S7": 1}, "tendency": "L", "reasoning": "理性安抚但回避情绪共振→S7:1"},
      {"label": "B", "text": "说实在不行以后一起还，反正你也没钱", "scores": {"S7": 3}, "tendency": "M", "reasoning": "用自嘲化解沉重，适度回应→S7:3"},
      {"label": "C", "text": "跟着他一起喊，房贷算什么咱俩从头赚回来", "scores": {"S7": 5}, "tendency": "H", "reasoning": "完全共振对方情绪并给出战斗宣言→S7:5"}
    ],
    "reveal": "「根本没法冷静——雒阳的……雒阳的……雒阳的房贷和首付啊啊——」——天塌了，但最让他崩溃的永远是房贷。"
  },
  {
    "id": "furong_angst_06", "type": "angst", "dimension": ["S5"], "source_character": "傅融",
    "text": "傅融在行动前说「你别来迟了，误了时辰，没人等你」。语气平淡但你知道他在担心你那一路的安全。",
    "options": [
      {"label": "A", "text": "嗯了一声，各自出发", "scores": {"S5": 1}, "tendency": "L", "reasoning": "接受安排不表露情感→S5:1"},
      {"label": "B", "text": "回头看了他一眼，说我尽量", "scores": {"S5": 3}, "tendency": "M", "reasoning": "给出回应但不做承诺→S5:3"},
      {"label": "C", "text": "在他肩膀上按了一下说一定准时，你也是", "scores": {"S5": 5}, "tendency": "H", "reasoning": "用肢体语言确认彼此的约定→S5:5"}
    ],
    "reveal": "「……别来迟了，误了时辰，没人等你。」——翻译：你一定要平安回来，我在这里等你。"
  },
  # === Batch 4: scheme ===
  {
    "id": "furong_scheme_01", "type": "scheme", "dimension": ["S1"], "source_character": "傅融",
    "text": "傅融查出刺杀名单上各方势力齐聚，唯独缺了王允。他冷静地分析局势，等你的决定。",
    "options": [
      {"label": "A", "text": "按原计划继续，不因一人缺席改变部署", "scores": {"S1": 1}, "tendency": "L", "reasoning": "忽视异常信号，不深入研判→S1:1"},
      {"label": "B", "text": "让他暗中调查王允的动向，其余照旧", "scores": {"S1": 3}, "tendency": "M", "reasoning": "适度反应，分出精力排查→S1:3"},
      {"label": "C", "text": "暂停行动，重新评估所有人包括王允在内的立场", "scores": {"S1": 5}, "tendency": "H", "reasoning": "全面推翻重来，深度权谋思考→S1:5"}
    ],
    "reveal": "「汉臣周贾、名士蔡邕、汉臣杨勋……西凉军牛辅……王允不在上面。文臣武将、甚至西凉军内部的人都在，偏偏王允不在。」"
  },
  {
    "id": "furong_scheme_02", "type": "scheme", "dimension": ["S9"], "source_character": "傅融",
    "text": "傅融在郿坞行动前说不能赌西凉军哗变，已经私自改了撤退计划。你发现他没有事先请示就做了这个决定。",
    "options": [
      {"label": "A", "text": "既然已经安排好了就按他的来吧", "scores": {"S9": 1}, "tendency": "L", "reasoning": "默认服从下属安排→S9:1"},
      {"label": "B", "text": "让他详细汇报新计划，确认后再执行", "scores": {"S9": 3}, "tendency": "M", "reasoning": "审查但不否定，保持主导权→S9:3"},
      {"label": "C", "text": "说下次这种改动必须先报备，但这次计划确实更稳妥", "scores": {"S9": 5}, "tendency": "H", "reasoning": "既认可判断又重申权力边界→S9:5"}
    ],
    "reveal": "「不能赌。你在拿她和你自己赌。要有一个戒严情况下最稳妥的撤退路线。我改了计划，已经安排好了。」"
  },
  {
    "id": "furong_scheme_03", "type": "scheme", "dimension": ["S6"], "source_character": "傅融",
    "text": "傅融质问那个差点出卖你们的香玉：「说认真的，怎么处理她？杀？」他看向你，等你做决定。",
    "options": [
      {"label": "A", "text": "说放了她吧，她也是被人利用的", "scores": {"S6": 1}, "tendency": "L", "reasoning": "宽大处理，不忍下重手→S6:1"},
      {"label": "B", "text": "说先关押起来审问幕后主使再定", "scores": {"S6": 3}, "tendency": "M", "reasoning": "折中处理，先查清再判→S6:3"},
      {"label": "C", "text": "沉默片刻说按规矩来，叛徒的代价她清楚", "scores": {"S6": 5}, "tendency": "H", "reasoning": "严格执行纪律，不因情感动摇→S6:5"}
    ],
    "reveal": "「说认真的，怎么处理她？杀？……这块香玉，刚才可是差点卖了我们。」——他在问你，也在观察你的底线在哪里。"
  },
  {
    "id": "furong_scheme_04", "type": "scheme", "dimension": ["S3"], "source_character": "傅融",
    "text": "傅融从成本角度分析中止犬神宴不划算，建议利用现有资源转攻为守。你看着他冷静得近乎冷酷的表情。",
    "options": [
      {"label": "A", "text": "觉得这样太功利了，应该更多考虑民众的感受", "scores": {"S3": 1}, "tendency": "L", "reasoning": "感性优先，排斥功利计算→S3:1"},
      {"label": "B", "text": "说有道理，但也问问其他人的意见", "scores": {"S3": 3}, "tendency": "M", "reasoning": "接受务实建议但引入民意平衡→S3:3"},
      {"label": "C", "text": "直接让他列一份详细的资源调配方案", "scores": {"S3": 5}, "tendency": "H", "reasoning": "完全拥抱务实路线，要求可执行方案→S3:5"}
    ],
    "reveal": "「从成本核算的角度来说中止犬神宴更改备战目标根本不划算。」——傅融的世界里，一切都是账本。"
  },
  {
    "id": "furong_scheme_05", "type": "scheme", "dimension": ["S1"], "source_character": "傅融",
    "text": "傅融发现有人在长安街头认出了你们，立刻拿出司徒府的木牒伪装身份。他低声让你配合演戏。",
    "options": [
      {"label": "A", "text": "紧张地站在他后面，让他一个人应付", "scores": {"S1": 1}, "tendency": "L", "reasoning": "慌乱退缩，缺乏应变→S1:1"},
      {"label": "B", "text": "接过木牒看一眼，顺着他编的故事接话", "scores": {"S1": 3}, "tendency": "M", "reasoning": "配合演戏但被动跟随→S1:3"},
      {"label": "C", "text": "主动上前和对方攀谈，用更多细节夯实假身份", "scores": {"S1": 5}, "tendency": "H", "reasoning": "主动加码伪装，掌控局面→S1:5"}
    ],
    "reveal": "「我们是司徒王允府上的人，出来采买，这是司徒府的木牒。」——傅校尉的临场应变能力，是在无数次生死关头磨出来的。"
  },
  {
    "id": "furong_scheme_06", "type": "scheme", "dimension": ["S5"], "source_character": "傅融",
    "text": "傅融说分头行动两处同时放火，但要把更危险的那条路留给自己。他已经在想哪条路你走更安全。",
    "options": [
      {"label": "A", "text": "说都听他的安排，他比较熟悉地形", "scores": {"S5": 1}, "tendency": "L", "reasoning": "服从分配，不做争取→S5:1"},
      {"label": "B", "text": "提出自己走更远但更安全的那条路让他放心", "scores": {"S5": 3}, "tendency": "M", "reasoning": "妥协折中，各退一步→S5:3"},
      {"label": "C", "text": "说危险的路一起去，分什么你我", "scores": {"S5": 5}, "tendency": "H", "reasoning": "拒绝分开，坚持并肩行动→S5:5"}
    ],
    "reveal": "「分头行动，两处同时起火。……那里有甲兵巡逻，你将大致地形告知我，我去。……要是那里的守军太多，不要强闯，立刻抽身而退。」"
  },
  # === Batch 5: daily ===
  {
    "id": "furong_daily_01", "type": "daily", "dimension": ["S8"], "source_character": "傅融",
    "text": "傅融做了点心端给你，你随口说了一句比饭店卖的还好吃。第二天他在厨房研究了一个时辰的糕点秘方。",
    "options": [
      {"label": "A", "text": "说挺好吃的，谢谢", "scores": {"S8": 1}, "tendency": "L", "reasoning": "礼貌回应但不给予额外鼓励→S8:1"},
      {"label": "B", "text": "夸他厨艺进步了，问他下次做什么", "scores": {"S8": 3}, "tendency": "M", "reasoning": "肯定他的付出并给予期待→S8:3"},
      {"label": "C", "text": "把糕点吃完说要当他的永久试菜员", "scores": {"S8": 5}, "tendency": "H", "reasoning": "用行动+承诺给予最大肯定→S8:5"}
    ],
    "reveal": "「啊……我看到了！她在红糖里加了紫苏！秘方原来是这样……我要记下来。」——你随口一句夸奖，他能在厨房琢磨三天。"
  },
  {
    "id": "furong_daily_02", "type": "daily", "dimension": ["S3"], "source_character": "傅融",
    "text": "傅融边逛夜市边心算物价涨幅，说要让雀部出个报告。你看着他认真的侧脸。",
    "options": [
      {"label": "A", "text": "等着他说完，反正他算账时拦不住", "scores": {"S3": 1}, "tendency": "L", "reasoning": "被动等待，不参与他的务实世界→S3:1"},
      {"label": "B", "text": "说回去帮他一起整理数据", "scores": {"S3": 3}, "tendency": "M", "reasoning": "愿意配合他的务实节奏→S3:3"},
      {"label": "C", "text": "说物价涨了那我们的工资也该涨了，让他一起算", "scores": {"S3": 5}, "tendency": "H", "reasoning": "主动融入他的思维模式并推动→S3:5"}
    ],
    "reveal": "「阴凉井水、果脯、蔗糖……商品还跟去年一样，物价是不是涨了？我算下涨幅，让雀部出个报告……」"
  },
  {
    "id": "furong_daily_03", "type": "daily", "dimension": ["S10"], "source_character": "傅融",
    "text": "傅融在夜市吃自助餐时规划全楼年夜饭方案：喜欢聊天的聊天，不善言辞的埋头吃肉，强制社交就是团建地狱。",
    "options": [
      {"label": "A", "text": "说随便吧，大家爱怎么来怎么来", "scores": {"S10": 1}, "tendency": "L", "reasoning": "不做规划，放任自流→S10:1"},
      {"label": "B", "text": "说按他说的安排，再加几个小游戏活跃气氛", "scores": {"S10": 3}, "tendency": "M", "reasoning": "在规划基础上适度补充→S10:3"},
      {"label": "C", "text": "让他出一份完整的年夜饭方案，菜单、座位、流程全列好", "scores": {"S10": 5}, "tendency": "H", "reasoning": "要求完整的系统化规划→S10:5"}
    ],
    "reveal": "「楼里的年夜饭要不要来这？喜欢聊天的聊天，不善言辞的埋头吃肉，不然强制社交，团建即地狱啊。」"
  },
  {
    "id": "furong_daily_04", "type": "daily", "dimension": ["S5"], "source_character": "傅融",
    "text": "傅融说想跑快一点，这里是无限速区。你看着他的背影，他回头等你跟上。",
    "options": [
      {"label": "A", "text": "说跑太快了，慢一点吧", "scores": {"S5": 1}, "tendency": "L", "reasoning": "选择舒适节奏，不追赶→S5:1"},
      {"label": "B", "text": "加速跟上去，保持在他身边", "scores": {"S5": 3}, "tendency": "M", "reasoning": "配合对方的节奏但不超越→S5:3"},
      {"label": "C", "text": "猛地冲到他前面，回头冲他笑", "scores": {"S5": 5}, "tendency": "H", "reasoning": "主动提速，制造追逐的乐趣→S5:5"}
    ],
    "reveal": "「想跑快一点吗？这里是无限速区哦。……慢悠悠……慢悠悠喵……这可是约会版拉练，和工作版拉练应该有区分才对。」"
  },
  {
    "id": "furong_daily_05", "type": "daily", "dimension": ["S7"], "source_character": "傅融",
    "text": "傅融在酒肆约会，端起酒杯前说了半天「身为下属要保持清醒」「喝酒误事」，最后被你劝了一口就红了脸。",
    "options": [
      {"label": "A", "text": "说不喝就不喝吧，给他叫壶热茶", "scores": {"S7": 1}, "tendency": "L", "reasoning": "尊重表面拒绝，不推进→S7:1"},
      {"label": "B", "text": "说就一口，陪他喝", "scores": {"S7": 3}, "tendency": "M", "reasoning": "温和引导，小步推进→S7:3"},
      {"label": "C", "text": "直接碰杯说今天不当下属了，放松一下", "scores": {"S7": 5}, "tendency": "H", "reasoning": "打破身份框架，拉他一起越界→S7:5"}
    ],
    "reveal": "「身为你的下属，要时刻保证头脑清醒，喝酒很容易误事的。……好、好吧，既然你这么推荐，喝一口……甜滋滋的，还不错。」"
  },
  {
    "id": "furong_daily_06", "type": "daily", "dimension": ["S9"], "source_character": "傅融",
    "text": "傅融说「图钱呗，出来上班不图钱图什么」，又说「谢谢老板，不用体谅我，多给点钱比较实际」。你看着他半开玩笑的样子。",
    "options": [
      {"label": "A", "text": "笑着说好的，下个月涨工资", "scores": {"S9": 1}, "tendency": "L", "reasoning": "用玩笑带过权力关系→S9:1"},
      {"label": "B", "text": "说那你先把这个月的绩效报告交上来", "scores": {"S9": 3}, "tendency": "M", "reasoning": "用工作逻辑回应工作诉求→S9:3"},
      {"label": "C", "text": "说真话，你觉得绣衣楼给你的够不够", "scores": {"S9": 5}, "tendency": "H", "reasoning": "直面权力关系中的价值交换→S9:5"}
    ],
    "reveal": "「图……图钱呗。出来上班，不图钱图什么。谢谢老板。不用这样体谅我，多给点钱比较实际。」——他在用玩笑试探你对他价值的认可。"
  },
  # === Batch 6: classic ===
  {
    "id": "furong_classic_01", "type": "classic", "dimension": ["S1"], "source_character": "傅融",
    "text": "傅融说「这世道，哪条道都是黑的，有什么差别」。你在决定绣衣楼是否要脱离朝廷。",
    "options": [
      {"label": "A", "text": "说听他的意见，他说哪条路就走哪条", "scores": {"S1": 1}, "tendency": "L", "reasoning": "放弃自主判断，完全依赖他人→S1:1"},
      {"label": "B", "text": "说正因为都是黑的，才要选一条自己能走的", "scores": {"S1": 3}, "tendency": "M", "reasoning": "在虚无中寻找有限自主→S1:3"},
      {"label": "C", "text": "说那不如自己开一条路，不管黑不黑", "scores": {"S1": 5}, "tendency": "H", "reasoning": "挑战现有格局，自主定义规则→S1:5"}
    ],
    "reveal": "「这世道，哪条道都是黑的。有什么差别。……你已经决定，不让绣衣楼重归朝廷了？说得好像这乱世在正确的路上一样。」"
  },
  {
    "id": "furong_classic_02", "type": "classic", "dimension": ["S10"], "source_character": "傅融",
    "text": "傅融说「当了那么久的绣衣校尉，也该明白，不是什么案子都能有结果的」。你看着眼前被拆毁的道观废墟。",
    "options": [
      {"label": "A", "text": "说算了，确实查不下去了", "scores": {"S10": 1}, "tendency": "L", "reasoning": "接受无序现实，放弃秩序追求→S10:1"},
      {"label": "B", "text": "说先把能查的查了，剩下的以后再说", "scores": {"S10": 3}, "tendency": "M", "reasoning": "在混乱中维持部分秩序→S10:3"},
      {"label": "C", "text": "说查，只要有一丝线索就不放弃", "scores": {"S10": 5}, "tendency": "H", "reasoning": "坚持追求完整秩序不妥协→S10:5"}
    ],
    "reveal": "「当了那么久的绣衣校尉，也该明白，不是什么案子都能有结果的。在这乱世，没有结果的，远比有结果的多。」"
  },
  {
    "id": "furong_classic_03", "type": "classic", "dimension": ["S4"], "source_character": "傅融",
    "text": "傅融说「和你有些亲近，也不是想让你对我格外的好。你怎么对他们，就一样对我」。你听着他刻意拉平关系的话。",
    "options": [
      {"label": "A", "text": "说好，一视同仁", "scores": {"S4": 1}, "tendency": "L", "reasoning": "接受他的面具设定，维持表面→S4:1"},
      {"label": "B", "text": "说行吧，但特殊的照顾不收回去", "scores": {"S4": 3}, "tendency": "M", "reasoning": "不完全接受面具，留有余地→S4:3"},
      {"label": "C", "text": "说不行，你就是不一样的，别装了", "scores": {"S4": 5}, "tendency": "H", "reasoning": "拒绝接受他的伪装，直击真心→S4:5"}
    ],
    "reveal": "「……不用，我和他们一样就好。和你有些亲近，也不是想让你……对我格外的好。你怎么对他们，就一样对我。」"
  },
  {
    "id": "furong_classic_04", "type": "classic", "dimension": ["S9"], "source_character": "傅融",
    "text": "傅融说「我还有八十五年房贷，不能丢了饭碗」，用这句话说服自己接下危险任务。你看着他认命的苦笑。",
    "options": [
      {"label": "A", "text": "说那就别去了，房贷的事再想办法", "scores": {"S9": 1}, "tendency": "L", "reasoning": "否定权力结构中的依附关系→S9:1"},
      {"label": "B", "text": "说那就多要点任务津贴，不能白干", "scores": {"S9": 3}, "tendency": "M", "reasoning": "在权力框架内争取利益→S9:3"},
      {"label": "C", "text": "说你去哪我去哪，饭碗一起端", "scores": {"S9": 5}, "tendency": "H", "reasoning": "重新定义权力关系为伙伴关系→S9:5"}
    ],
    "reveal": "「我要是说不愿意，被开除了怎么办？我还有八十五年房贷，不能丢了饭碗。」——最真实的打工人心声。"
  },
  {
    "id": "furong_classic_05", "type": "classic", "dimension": ["S6"], "source_character": "傅融",
    "text": "傅融看到动物表演时沉默了很久，说「总觉得很可怜，但戏班的人也以此为生，乱世中先让人有口饭吃」。他起身走开了。",
    "options": [
      {"label": "A", "text": "跟着他走，换个话题聊", "scores": {"S6": 1}, "tendency": "L", "reasoning": "回避矛盾，不表态→S6:1"},
      {"label": "B", "text": "说以后我们可以做点什么帮帮他们", "scores": {"S6": 3}, "tendency": "M", "reasoning": "表达善意但承诺模糊→S6:3"},
      {"label": "C", "text": "拉他去找班主聊聊，看能不能改善条件", "scores": {"S6": 5}, "tendency": "H", "reasoning": "立即行动，直面两难→S6:5"}
    ],
    "reveal": "「……总觉得很可怜。但是戏班的人也以此为生，乱世中，肯定是先让人有口饭吃。……我们不要教飞云坐下、握手了吧？小狗开心最重要。」"
  },
  {
    "id": "furong_classic_06", "type": "classic", "dimension": ["S2"], "source_character": "傅融",
    "text": "流星划过天际，傅融对着流星许了一个愿望，被你问到时许了什么时，他说「没什么……大概是心诚则灵吧」。",
    "options": [
      {"label": "A", "text": "嗯了一声不再追问", "scores": {"S2": 1}, "tendency": "L", "reasoning": "尊重隐私但关闭情感通道→S2:1"},
      {"label": "B", "text": "说你的愿望里有我吗，半开玩笑半认真", "scores": {"S2": 3}, "tendency": "M", "reasoning": "试探性接近但不强求答案→S2:3"},
      {"label": "C", "text": "靠过来说不许偷偷许愿，要一起许才行", "scores": {"S2": 5}, "tendency": "H", "reasoning": "主动消除距离，共享仪式感→S2:5"}
    ],
    "reveal": "「等等等等我能再换个愿望吗？！！回来啊流星——……没、没什么……大概是……心诚则灵吧。」——他第一次许的愿望大概是和你有关的，但来不及了；第二次嘛，大概是暴富。"
  }
]

data.extend(new_questions)
with open(filepath, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Verify
print(f'Total questions: {len(data)}')
dims = {}
for q in data:
    d = q['dimension'][0]
    dims[d] = dims.get(d, 0) + 1
print('Dimension counts:', dict(sorted(dims.items())))
