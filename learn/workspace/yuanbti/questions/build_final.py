import json

filepath = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/furong.json'

# 30 questions, 5 batches x 6, each dimension >= 3
# Batch allocation (adjusted for 30 questions, 5 batches):
# Batch1 sweet:    S2, S8, S2, S8, S4, S7
# Batch2 funny:    S7, S5, S3, S4, S2, S6
# Batch3 angst:    S6, S2, S4, S8, S10, S5
# Batch4 scheme:   S1, S9, S6, S3, S1, S5
# Batch5 classic:  S1, S10, S4, S9, S6, S2
# Totals: S1:3 S2:4 S3:2 S4:4 S5:3 S6:4 S7:2 S8:3 S9:2 S10:2
# S3,S7,S9,S10 need 3 each... let me redistribute

# Better plan - 5 batches ensuring min 3 per dim:
# sweet:   S2 S8 S2 S8 S4 S7
# funny:   S7 S5 S3 S4 S2 S3
# angst:   S6 S2 S10 S8 S7 S5
# scheme:  S1 S9 S6 S3 S1 S5
# classic: S1 S10 S4 S9 S10 S9
# S1:3 S2:4 S3:3 S4:3 S5:3 S6:2 S7:3 S8:3 S9:3 S10:3
# S6 only 2! Fix:
# scheme:  S1 S9 S6 S3 S1 S6  -> S6:2+2=4 but lose S5
# classic: S1 S10 S4 S9 S10 S5 -> S5:3 total
# So: sweet S2 S8 S2 S8 S4 S7, funny S7 S5 S3 S4 S2 S3, angst S6 S2 S10 S8 S7 S5, scheme S1 S9 S6 S3 S1 S6, classic S1 S10 S4 S9 S10 S5
# S1:3 S2:4 S3:3 S4:3 S5:3 S6:4 S7:3 S8:3 S9:2 S10:3
# S9 only 2. Move one: classic S1 S10 S4 S9 S9 S5 -> S9:3, S10:2... 
# Let me try: classic S1 S9 S4 S10 S9 S5
# S1:3 S2:4 S3:3 S4:3 S5:3 S6:4 S7:3 S8:3 S9:3 S10:2
# Still S10=2. One more: angst S6 S2 S10 S8 S10 S5 -> S10:3
# Final: sweet S2 S8 S2 S8 S4 S7, funny S7 S5 S3 S4 S2 S3, angst S6 S2 S10 S8 S10 S5, scheme S1 S9 S6 S3 S1 S6, classic S1 S9 S4 S10 S9 S5

data = [
  # ===== Batch 1: sweet =====
  {
    "id": "furong_sweet_01", "type": "sweet", "dimension": ["S2"], "source_character": "傅融",
    "text": "七夕夜市，傅融买了一碗娇耳端到你面前，特意加了豉油。你咬开发现里面有五铢钱，傅融紧张地凑过来问你有没有硌到牙。",
    "options": [
      {"label": "A", "text": "把钱吐出来放兜里，假装没事继续吃", "scores": {"S2": 1}, "tendency": "L", "reasoning": "回避情感互动，独自消化→S2:1"},
      {"label": "B", "text": "举着钱笑着说许愿一夜暴富，偷偷看他反应", "scores": {"S2": 3}, "tendency": "M", "reasoning": "用玩笑间接回应他的关心→S2:3"},
      {"label": "C", "text": "直接把那枚钱放到他手心里，说这是咱俩的许愿钱", "scores": {"S2": 5}, "tendency": "H", "reasoning": "主动制造亲密的共同记忆→S2:5"}
    ],
    "reveal": "「对娇耳里的五铢钱许愿很灵验？那就……一夜暴富，拜托了。」——傅融嘴上说是许愿暴富，实际上紧张地要去找老板理论食品安全。"
  },
  {
    "id": "furong_sweet_02", "type": "sweet", "dimension": ["S8"], "source_character": "傅融",
    "text": "傅融在花摊前盯着紫菖蒲看了很久，嘴上说水边到处能挖不用花钱买，但你注意到他一直在回头看那盆花。",
    "options": [
      {"label": "A", "text": "拉着他去下一个摊位，说还有别的想看的", "scores": {"S8": 1}, "tendency": "L", "reasoning": "忽视对方的隐秘期待→S8:1"},
      {"label": "B", "text": "趁他不注意偷偷买下来，之后找机会放在他桌上", "scores": {"S8": 3}, "tendency": "M", "reasoning": "默默照顾但不过度表达→S8:3"},
      {"label": "C", "text": "直接塞到他怀里说送你的，别再说什么划不划算", "scores": {"S8": 5}, "tendency": "H", "reasoning": "大方给足被珍视的感觉→S8:5"}
    ],
    "reveal": "「但水边到处都能挖，为什么要花钱买？算了，不浪费钱了……嗯？你替我买了？……谢谢。」——他永远嘴硬，但收到花的那一刻声音都软了。"
  },
  {
    "id": "furong_sweet_03", "type": "sweet", "dimension": ["S2"], "source_character": "傅融",
    "text": "约会时傅融假装不经意地采了一朵野花，被你发现后慌张地说是顺手摘的。",
    "options": [
      {"label": "A", "text": "点头说哦挺好的，低头继续走路", "scores": {"S2": 1}, "tendency": "L", "reasoning": "对示好视而不见，关闭情感通道→S2:1"},
      {"label": "B", "text": "笑嘻嘻地说他嘴硬，接过来别在衣领上", "scores": {"S2": 3}, "tendency": "M", "reasoning": "俏皮回应但没点破那层心意→S2:3"},
      {"label": "C", "text": "凑过去帮他整理花枝，说这朵和他一样好看", "scores": {"S2": 5}, "tendency": "H", "reasoning": "正面接住他的心意并回以赞美→S2:5"}
    ],
    "reveal": "「假装要追蝴蝶、假装追上树梢、假装这朵精心挑选的花是不小心挂在身上的……好像说漏嘴了喵！但、但是……花的确是想……送给你的。」"
  },
  {
    "id": "furong_sweet_04", "type": "sweet", "dimension": ["S8"], "source_character": "傅融",
    "text": "傅融发现你一直在看隔壁桌的菜，但嘴上说吃不下了不能浪费，故意把话题岔开。",
    "options": [
      {"label": "A", "text": "算了，确实吃不下，继续聊天", "scores": {"S8": 1}, "tendency": "L", "reasoning": "顺从表面话语，不深究对方需求→S8:1"},
      {"label": "B", "text": "偷偷又去拿了一份放在两人中间，说帮你尝尝", "scores": {"S8": 3}, "tendency": "M", "reasoning": "委婉体贴，不戳破对方的小纠结→S8:3"},
      {"label": "C", "text": "直接起身端一整盘回来，说想吃什么就吃什么不用省", "scores": {"S8": 5}, "tendency": "H", "reasoning": "果断满足对方需求，不让他自我压抑→S8:5"}
    ],
    "reveal": "「隔壁桌的牛内脏看上去不错……不行不行，有点吃不下了，不能浪费食物。」——他嘴上在计算性价比，其实一直在注意你想吃什么。"
  },
  {
    "id": "furong_sweet_05", "type": "sweet", "dimension": ["S4"], "source_character": "傅融",
    "text": "约会时傅融不小心说漏嘴「要是每天都能约会就好了」，立刻改口说「我是说要是每天都不用公务就好了」。",
    "options": [
      {"label": "A", "text": "点点头说确实公务太忙了，理解他的辛苦", "scores": {"S4": 1}, "tendency": "L", "reasoning": "接受表面解释，不触及真实情绪层→S4:1"},
      {"label": "B", "text": "眯起眼睛笑着追问：所以到底是想约会还是不想上班？", "scores": {"S4": 3}, "tendency": "M", "reasoning": "半开玩笑地试探面具背后的真心→S4:3"},
      {"label": "C", "text": "凑到他耳边说我也想每天和你约会，看他脸红成什么样", "scores": {"S4": 5}, "tendency": "H", "reasoning": "直接拆穿伪装并坦诚回应→S4:5"}
    ],
    "reveal": "「郊外的天地好广阔，要是每天都能约会就……喵，我是说，要是每天都不用公务就好了。」——傅校尉的口误翻译：我每天都想见你。"
  },
  {
    "id": "furong_sweet_06", "type": "sweet", "dimension": ["S7"], "source_character": "傅融",
    "text": "夜市套圈摊上，傅融凭当年流落桥洞练出的技术连中好几个，摊主快哭了。",
    "options": [
      {"label": "A", "text": "默默帮他拿奖品，觉得差不多就行了", "scores": {"S7": 1}, "tendency": "L", "reasoning": "低调配合，不张扬→S7:1"},
      {"label": "B", "text": "拍手叫好，大声嚷嚷让周围人都来看看傅校尉的手艺", "scores": {"S7": 3}, "tendency": "M", "reasoning": "给对方鼓劲但分寸适中→S7:3"},
      {"label": "C", "text": "拉着他再去别的摊位大杀四方，今晚所有摊主都要认识傅融", "scores": {"S7": 5}, "tendency": "H", "reasoning": "高调放大对方的闪光时刻→S7:5"}
    ],
    "reveal": "「我来。当年被黑心房东扣完三个月押金流落桥洞下的时候，我苦练套圈，去摊子上套点心！中了！中了！中了！」"
  },
  # ===== Batch 2: funny =====
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
    "text": "听经课上傅融自带了算盘，结果不知不觉开始清起了账。你发现他在桌案下偷偷打算盘。",
    "options": [
      {"label": "A", "text": "轻轻碰他一下示意他认真听课", "scores": {"S4": 1}, "tendency": "L", "reasoning": "维持规矩不破坏形象→S4:1"},
      {"label": "B", "text": "偷偷把自己那页经书推过去盖住他的算盘", "scores": {"S4": 3}, "tendency": "M", "reasoning": "用小动作帮他掩饰→S4:3"},
      {"label": "C", "text": "凑过去和他一起算，反正这课也没在听", "scores": {"S4": 5}, "tendency": "H", "reasoning": "公然放弃伪装，直接加入→S4:5"}
    ],
    "reveal": "「我带了算盘……为什么要带算盘？因为今天是算经课，来前我看过课表的。三下五去二、七上二去五进一……喵？不知不觉怎么清起账来了……」"
  },
  {
    "id": "furong_funny_05", "type": "funny", "dimension": ["S2"], "source_character": "傅融",
    "text": "七夕夜市看到竹筒饭摊位，傅融眼睛发亮说以后不当密探要去摆摊，还规划了亲子套餐、情侣套餐。",
    "options": [
      {"label": "A", "text": "说别想了好好当密探吧，摆摊不稳定", "scores": {"S2": 1}, "tendency": "L", "reasoning": "用现实打断对方的畅想→S2:1"},
      {"label": "B", "text": "说那我当你的第一个客人，先赊账", "scores": {"S2": 3}, "tendency": "M", "reasoning": "配合畅想但保持调侃距离→S2:3"},
      {"label": "C", "text": "说我帮你算账，咱们以后一起摆摊过日子", "scores": {"S2": 5}, "tendency": "H", "reasoning": "把对方的小梦想变成共同的未来→S2:5"}
    ],
    "reveal": "「如果以后不当密探，我也推一台木车，夜市摆摊卖竹筒饭。竹筒饭携带方便，便宜，香味浓……到时候可以出亲子套餐、饮料套餐、情侣套餐……」"
  },
  {
    "id": "furong_funny_06", "type": "funny", "dimension": ["S3"], "source_character": "傅融",
    "text": "傅融赢了棋局后算了一下奖金，说给大家下班后聚餐。你看着他笑眯眯数白金币的样子。",
    "options": [
      {"label": "A", "text": "说你自己留着吧，赢的凭什么分", "scores": {"S3": 1}, "tendency": "L", "reasoning": "拒绝务实分配，强调个人利益→S3:1"},
      {"label": "B", "text": "说好啊，问他打算去哪家店吃", "scores": {"S3": 3}, "tendency": "M", "reasoning": "接受务实方案，自然配合→S3:3"},
      {"label": "C", "text": "说帮他列个预算表，确保每分钱都花在刀刃上", "scores": {"S3": 5}, "tendency": "H", "reasoning": "主动深度参与务实规划→S3:5"}
    ],
    "reveal": "「……差点不分输赢，险胜。我赢的这些白金币……给大家下班后聚餐怎么样？」——赢了钱第一反应是团队聚餐，傅校尉的管理魂永不熄灭。"
  },
  # ===== Batch 3: angst =====
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
    "id": "furong_angst_03", "type": "angst", "dimension": ["S10"], "source_character": "傅融",
    "text": "傅融说「放在原地，就会觉得他们还可能会回来。一直这样想，心里会生出魔障的」。他在劝你放下留下的东西。",
    "options": [
      {"label": "A", "text": "说那就放着吧，总比后悔好", "scores": {"S10": 1}, "tendency": "L", "reasoning": "接受无序混沌，不追求收尾→S10:1"},
      {"label": "B", "text": "说收拾一部分，留一两件做纪念", "scores": {"S10": 3}, "tendency": "M", "reasoning": "在秩序与情感之间折中→S10:3"},
      {"label": "C", "text": "说他说得对，全部收拾好，该放下的放下", "scores": {"S10": 5}, "tendency": "H", "reasoning": "果断建立秩序，彻底了断→S10:5"}
    ],
    "reveal": "「放在原地，就会觉得，他们还可能会回来。一直这样想，心里会生出魔障的。」"
  },
  {
    "id": "furong_angst_04", "type": "angst", "dimension": ["S8"], "source_character": "傅融",
    "text": "深夜傅融一个人在院子里给飞云重新画被踩坏的灯笼花，嘴里念叨着「多可爱啊你看，给它穿个红棉袄」。",
    "options": [
      {"label": "A", "text": "默默回屋，让他一个人待着", "scores": {"S8": 1}, "tendency": "L", "reasoning": "给予空间但不给予陪伴→S8:1"},
      {"label": "B", "text": "悄悄走过去递杯热水，不说话陪在旁边", "scores": {"S8": 3}, "tendency": "M", "reasoning": "无声陪伴，不强求交流→S8:3"},
      {"label": "C", "text": "蹲下来接过画笔说一起画，红棉袄太丑了换你画", "scores": {"S8": 5}, "tendency": "H", "reasoning": "主动分担他的脆弱时刻→S8:5"}
    ],
    "reveal": "「看看还能不能补救……把那团红的改画成红衣小人?不不不更恐怖了……多可爱啊你看，给它穿个红棉袄……实在不行重新画一张吧……不要哭了。」"
  },
  {
    "id": "furong_angst_05", "type": "angst", "dimension": ["S10"], "source_character": "傅融",
    "text": "傅融说「能相聚就有分开，就好像赚钱就会花钱」。你听着他用理财比喻离别，语气平静得让人心疼。",
    "options": [
      {"label": "A", "text": "说别用钱打比方了，不是一回事", "scores": {"S10": 1}, "tendency": "L", "reasoning": "拒绝用秩序框架处理情感→S10:1"},
      {"label": "B", "text": "说那至少把钱花在值得的地方", "scores": {"S10": 3}, "tendency": "M", "reasoning": "顺着他的秩序逻辑接话→S10:3"},
      {"label": "C", "text": "说那就一直赚一直花，别停", "scores": {"S10": 5}, "tendency": "H", "reasoning": "用他的逻辑推翻他的结论→S10:5"}
    ],
    "reveal": "「能相聚就有分开，就好像赚钱就会花钱。……很担心的话，以后去北方看他们吧？广陵这边房价贵，也就是说北方便宜……」"
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
  # ===== Batch 4: scheme =====
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
    "text": "傅融在郿坞行动前私自改了撤退计划，说不能赌西凉军哗变。你发现他没有事先请示就做了这个决定。",
    "options": [
      {"label": "A", "text": "既然已经安排好了就按他的来吧", "scores": {"S9": 1}, "tendency": "L", "reasoning": "默认服从下属安排→S9:1"},
      {"label": "B", "text": "让他详细汇报新计划，确认后再执行", "scores": {"S9": 3}, "tendency": "M", "reasoning": "审查但不否定，保持主导权→S9:3"},
      {"label": "C", "text": "说下次这种改动必须先报备，但这次确实更稳妥", "scores": {"S9": 5}, "tendency": "H", "reasoning": "既认可判断又重申权力边界→S9:5"}
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
    "id": "furong_scheme_06", "type": "scheme", "dimension": ["S6"], "source_character": "傅融",
    "text": "傅融说分头行动两处同时放火，但要把更危险的那条路留给自己。他已经在想哪条路你走更安全。",
    "options": [
      {"label": "A", "text": "说都听他的安排，他比较熟悉地形", "scores": {"S6": 1}, "tendency": "L", "reasoning": "服从分配，不做争取→S6:1"},
      {"label": "B", "text": "提出自己走更远但更安全的那条路让他放心", "scores": {"S6": 3}, "tendency": "M", "reasoning": "妥协折中，各退一步→S6:3"},
      {"label": "C", "text": "说危险的路一起去，分什么你我", "scores": {"S6": 5}, "tendency": "H", "reasoning": "拒绝分开，坚持并肩行动→S6:5"}
    ],
    "reveal": "「分头行动，两处同时起火。……那里有甲兵巡逻，你将大致地形告知我，我去。……要是那里的守军太多，不要强闯，立刻抽身而退。」"
  },
  # ===== Batch 5: classic =====
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
    "id": "furong_classic_02", "type": "classic", "dimension": ["S9"], "source_character": "傅融",
    "text": "傅融说「我还有八十五年房贷，不能丢了饭碗」，用这句话说服自己接下危险任务。你看着他认命的苦笑。",
    "options": [
      {"label": "A", "text": "说那就别去了，房贷的事再想办法", "scores": {"S9": 1}, "tendency": "L", "reasoning": "否定权力结构中的依附关系→S9:1"},
      {"label": "B", "text": "说那就多要点任务津贴，不能白干", "scores": {"S9": 3}, "tendency": "M", "reasoning": "在权力框架内争取利益→S9:3"},
      {"label": "C", "text": "说你去哪我去哪，饭碗一起端", "scores": {"S9": 5}, "tendency": "H", "reasoning": "重新定义权力关系为伙伴关系→S9:5"}
    ],
    "reveal": "「我要是说不愿意，被开除了怎么办？我还有八十五年房贷，不能丢了饭碗。」——最真实的打工人心声。"
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
    "id": "furong_classic_04", "type": "classic", "dimension": ["S10"], "source_character": "傅融",
    "text": "傅融说「当了那么久的绣衣校尉，也该明白，不是什么案子都能有结果的」。你看着眼前被拆毁的道观废墟。",
    "options": [
      {"label": "A", "text": "说算了，确实查不下去了", "scores": {"S10": 1}, "tendency": "L", "reasoning": "接受无序现实，放弃秩序追求→S10:1"},
      {"label": "B", "text": "说先把能查的查了，剩下的以后再说", "scores": {"S10": 3}, "tendency": "M", "reasoning": "在混乱中维持部分秩序→S10:3"},
      {"label": "C", "text": "说查，只要有一丝线索就不放弃", "scores": {"S10": 5}, "tendency": "H", "reasoning": "坚持追求完整秩序不妥协→S10:5"}
    ],
    "reveal": "「当了那么久的绣衣校尉，也该明白，不是什么案子都能有结果的。在这乱世，没有结果的，远比有结果的多。」"
  },
  {
    "id": "furong_classic_05", "type": "classic", "dimension": ["S9"], "source_character": "傅融",
    "text": "傅融说「图钱呗，出来上班不图钱图什么」，又说「谢谢老板，不用体谅我，多给点钱比较实际」。",
    "options": [
      {"label": "A", "text": "笑着说好的，下个月涨工资", "scores": {"S9": 1}, "tendency": "L", "reasoning": "用玩笑带过权力关系→S9:1"},
      {"label": "B", "text": "说那你先把这个月的绩效报告交上来", "scores": {"S9": 3}, "tendency": "M", "reasoning": "用工作逻辑回应工作诉求→S9:3"},
      {"label": "C", "text": "说真话，你觉得绣衣楼给你的够不够", "scores": {"S9": 5}, "tendency": "H", "reasoning": "直面权力关系中的价值交换→S9:5"}
    ],
    "reveal": "「图……图钱呗。出来上班，不图钱图什么。谢谢老板。不用这样体谅我，多给点钱比较实际。」——他在用玩笑试探你对他价值的认可。"
  },
  {
    "id": "furong_classic_06", "type": "classic", "dimension": ["S5"], "source_character": "傅融",
    "text": "流星划过天际，傅融对着流星许了愿，被你问到时许了什么时，他说「没什么……大概是心诚则灵吧」。",
    "options": [
      {"label": "A", "text": "嗯了一声不再追问", "scores": {"S5": 1}, "tendency": "L", "reasoning": "被动接受，不主动推进→S5:1"},
      {"label": "B", "text": "说你的愿望里有我吗，半开玩笑半认真", "scores": {"S5": 3}, "tendency": "M", "reasoning": "试探性接近但不强求答案→S5:3"},
      {"label": "C", "text": "靠过来说不许偷偷许愿，要一起许才行", "scores": {"S5": 5}, "tendency": "H", "reasoning": "主动消除距离，共享仪式感→S5:5"}
    ],
    "reveal": "「等等等等我能再换个愿望吗？！！回来啊流星——……没、没什么……大概是……心诚则灵吧。」——他第一次许的愿望大概是和你有关的，但来不及了；第二次嘛，大概是暴富。"
  }
]

with open(filepath, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

dims = {}
for q in data:
    d = q['dimension'][0]
    dims[d] = dims.get(d, 0) + 1
print(f'Total: {len(data)}')
print('Dimensions:', dict(sorted(dims.items())))
print('All >= 3:', all(v >= 3 for v in dims.values()))
