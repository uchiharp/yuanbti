import json, os

BASE = os.path.dirname(__file__) + '/questions'

def load(path):
    with open(path) as f: return json.load(f)

def save(path, data):
    with open(path, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)

def next_id(data, prefix):
    n = max(int(q['id'].split('_')[-1]) for q in data if q['id'].startswith('q_'+prefix))
    return f'q_{prefix}_{n+1}'

# dimension rotation to spread coverage
dims = ['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10']
def pick_dim(data, offset=0):
    used = [q['dimension'] for q in data]
    # pick least used
    from collections import Counter
    c = Counter(used)
    for d in dims:
        if c[d] == min(c.values()):
            return d
    return dims[offset % len(dims)]

def make_opts(scores_list, tendency_list, texts):
    labels = 'ABC'
    return [{"label": l, "text": t, "scores": {"S1": s}, "tendency": ten} 
            for l,t,s,ten in zip(labels, texts, scores_list, tendency_list)]

questions = {
'liubian.json': [
  # value x2
  {"dim_offset": 0, "type": "value", "texts": [
    "「保护一个人最好的方式，就是让她以为你不在。」——你对这种想法怎么看？",
    "「我不想当别人的棋子，哪怕这盘棋是为我而下的。」——你更认同哪种态度？",
    "「有些事说出来反而会让对方为难，不如自己扛着。」——你觉得呢？"
  ], "scores": [2,3,4], "tendencies": ["L","M","H"], "reveal": "保护与被保护之间，藏着对等关系的理解。"},
  {"dim_offset": 3, "type": "value", "texts": [
    "「我什么都不怕，就怕你担心。」——这句话背后是什么？",
    "「我已经在黑暗里待了太久，再也没资格靠近光了。」——你怎么看？",
    "「失去的东西，就让它失去好了。至少我还活着。」——你更认同哪个？"
  ], "scores": [2,3.5,4], "tendencies": ["M","H","L"], "reveal": "在自我否定和坦然接受之间，衡量的是与过去的和解程度。"},
  # daily x2
  {"dim_offset": 1, "type": "daily", "texts": [
    "深夜值守绣衣楼，你发现楼内密探的值班记录被人篡改了。你会——",
    "广陵王临时加派了任务，但你和另一位密探已经约好一起吃饭。你——",
    "你负责的情报在传递途中泄露了，虽然不是你的错，但上面要追责。你——"
  ], "scores": [2,3,4], "tendencies": ["L","M","H"], "reveal": "日常中的选择反映你处理压力和责任的方式。"},
  {"dim_offset": 4, "type": "daily", "texts": [
    "绣衣楼新来了一批年轻密探，都抢着跟高阶密探搭档出任务。你——",
    "你的搭档在一次任务中受伤，短期内无法行动。你——",
    "广陵王让你去监视一个老朋友，你发现他似乎在密谋对绣衣楼不利。你——"
  ], "scores": [2,3.5,4], "tendencies": ["L","M","H"], "reveal": "公私之间的选择，考验的是你把谁放在第一位。"},
  # extreme x1
  {"dim_offset": 5, "type": "extreme", "texts": [
    "「我宁愿你恨我，也不愿你为我死。」",
    "「如果你真的为我好，就让我陪在你身边，不管前面是什么。」"
  ], "scores": [2,5], "tendencies": ["L","H"], "reveal": "一边是推开，一边是靠近。都是爱，方向相反。"},
],
'furong.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「兵法讲究的不是赢，而是不输。」——你怎么理解？",
    "「宁可千日不用，不可一日不备。」——你更认同哪种态度？",
    "「天时不如地利，地利不如人和。」——在你心中，最重要的是？"
  ], "scores": [2,3,4], "tendencies": ["M","H","L"], "reveal": "三种态度分别对应：保守策略、极致准备、关系优先。"},
  {"dim_offset": 2, "type": "value", "texts": [
    "「在战场上犹豫一秒，就会多死一个人。」——所以你认为？",
    "「计划赶不上变化，所以要在变化来临之前就准备好变化。」——你的看法？",
    "「有时候退一步不是怕输，而是为了赢。」——你更认同哪个？"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "果断、周密、策略——三种领导力的侧面。"},
  {"dim_offset": 1, "type": "daily", "texts": [
    "广陵王让你制定一份攻城方案，但情报有缺，只能推断。你——",
    "你带的一支密探小队在执行任务时遭遇伏击，损失了两名队员。撤退后你——",
    "绣衣楼内部有人质疑你的用兵风格太保守，认为应该更激进。你——"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "战场上的每一个决策都关乎性命，压力下才能看清一个人的底色。"},
  {"dim_offset": 3, "type": "daily", "texts": [
    "你接到命令要摧毁一个敌方据点，但据点里还有平民。你——",
    "有密探在任务中违抗你的命令，但他这样做救了全队。你——",
    "广陵王让你暗中调查一位同僚，你发现他其实并无不忠。你——"
  ], "scores": [2,3,4], "tendencies": ["L","M","H"], "reveal": "规则与灵活之间的平衡，体现你对自己信念的坚持程度。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「胜利就是一切，哪怕要踏着同伴的尸体走过去。」",
    "「输了就是输了，没什么好说的。但下次我不会再输。」"
  ], "scores": [5,3], "tendencies": ["H","L"], "reveal": "胜利至上还是过程导向——这道题测的是你对结果的态度。"},
],
'yuanji.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「与其改变世界，不如让世界以为你已经改变了。」——你觉得？",
    "「真正聪明的人，不是让所有人服你，而是让所有人觉得你无害。」——你认同吗？",
    "「微笑是最好的武器，因为没人会防备一个笑着的杀手。」——你怎么看？"
  ], "scores": [3.5,2,4], "tendencies": ["H","M","L"], "reveal": "三种态度对应：操控表象、示弱生存、笑里藏刀。"},
  {"dim_offset": 2, "type": "value", "texts": [
    "「我不喜欢争，但不喜欢的东西总会来找我。」——所以？",
    "「世人都说我是君子，君子就该忍。但忍到什么时候呢？」——你的看法？",
    "「有些善意比恶意更可怕，因为它让你无法拒绝。」——你更认同哪个？"
  ], "scores": [2,4,3.5], "tendencies": ["L","H","M"], "reveal": "被动应对、忍无可忍、洞察陷阱——面对善意的伪装，你更警惕哪一种？"},
  {"dim_offset": 1, "type": "daily", "texts": [
    "广陵王让你在世家宴会上打探消息。席间有人用隐晦的话试探你的身份。你——",
    "你收到一封匿名信，里面是绣衣楼内部的人事安排，信息极其详细。你——",
    "一位世家公子当众送你贵重礼物，背后显然有目的。你——"
  ], "scores": [2,4,3], "tendencies": ["L","H","M"], "reveal": "社交场合的应对，体现你对表面功夫的驾驭能力。"},
  # extreme x2
  {"dim_offset": 3, "type": "extreme", "texts": [
    "「这世上没有永远的敌人，只有永远的利益。」",
    "「有些人的善意，比刀子还毒。」"
  ], "scores": [3,4.5], "tendencies": ["M","H"], "reveal": "利益至上还是警惕善意——袁基的世界里，笑容下面永远是棋局。"},
  {"dim_offset": 5, "type": "extreme", "texts": [
    "「我不想算计任何人，但如果我不算计，别人就会算计我。」",
    "「如果你想保护一个人，就永远不要让她看到你的真面目。」"
  ], "scores": [2,5], "tendencies": ["L","H"], "reveal": "被动自保还是主动伪装——两条路都通向孤独。"},
],
'sunce.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「命是天给的，但路是自己走的。」——你怎么看？",
    "「打不过就跑有什么丢人的？活着才有机会翻盘。」——你更认同？",
    "「如果注定要输，我也要输得漂亮。」——你的看法？"
  ], "scores": [3,2,4], "tendencies": ["M","L","H"], "reveal": "顺应命运、务实生存、体面抗争——三种面对困境的姿态。"},
  {"dim_offset": 2, "type": "value", "texts": [
    "「兄弟不是说出来的，是打出来的。」——你觉得？",
    "「谁说我只会蛮干？我只是懒得跟你们绕弯子。」——你的看法？",
    "「开心的时候就要大笑，难过的时候也别硬撑。」——你认同吗？"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "行动验证、坦率表达、真实情感——孙策式直爽的三个维度。"},
  {"dim_offset": 1, "type": "daily", "texts": [
    "你在校场练武时，有个密探嘲笑你'只会动武不会动脑'。你——",
    "广陵王派你和一位文人密探搭档执行任务，两人理念完全不合。你——",
    "你带队突袭敌营大获全胜，但战利品分配上引起了争执。你——"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "直来直去还是能屈能伸，反映你对外界评价的敏感度。"},
  {"dim_offset": 3, "type": "daily", "texts": [
    "绣衣楼举行比武大会，你被分到了实力最强的那一组。你——",
    "你得知一位朋友在背后说你坏话，但你还没核实。你——",
    "广陵王让你去安抚一群因为战败而士气低落的密探。你——"
  ], "scores": [2,3.5,4], "tendencies": ["L","M","H"], "reveal": "面对竞争和冲突，你是迎难而上还是另有策略？"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「就算全世界都不信我，我也要相信自己选的路。」",
    "「如果连自己都保护不了，谈什么保护别人？」"
  ], "scores": [4,2], "tendencies": ["H","L"], "reveal": "信念至上还是能力优先——两种英雄主义。"},
],
'zuoci.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「万物皆有裂痕，那是光照进来的地方。」——你怎么理解？",
    "「得道多助，失道寡助。」——在你看来，「道」是什么？",
    "「天命所归？不过是强者的借口罢了。」——你的看法？"
  ], "scores": [3,4,2], "tendencies": ["M","H","L"], "reveal": "接受缺陷、相信正义、质疑权威——三种面对世界的方式。"},
  {"dim_offset": 2, "type": "value", "texts": [
    "「人生如梦，何必太执着？」——但如果是你珍视的东西呢？",
    "「有些事不是做不到，而是你还没找到正确的方法。」——你认同吗？",
    "「放下不是放弃，而是换一种方式拿起。」——你觉得呢？"
  ], "scores": [2,3.5,4], "tendencies": ["L","M","H"], "reveal": "超脱、钻研、转化——面对困境的三种哲学。"},
  {"dim_offset": 1, "type": "daily", "texts": [
    "你在绣衣楼藏书阁发现一本被列为禁书的典籍，内容涉及天文异象。你——",
    "一位密探请你帮忙卜卦，问的是出任务的吉凶。你——",
    "广陵王要你用术数预测一场战役的胜算。你——"
  ], "scores": [2,3,4], "tendencies": ["L","M","H"], "reveal": "知识、善意、责任——面对超出常理的请求，你如何抉择。"},
  {"dim_offset": 3, "type": "daily", "texts": [
    "有人传言你是妖人，因为你准确预测了一场天灾。你——",
    "你在集市上看到一个孩子正在被欺负，周围无人帮忙。你——",
    "绣衣楼要举办一次驱邪仪式，但你认为根本没有什么邪祟。你——"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "被误解时的反应，体现你对外界眼光的在意程度。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「如果天命注定要失败，我也要逆天而行。」",
    "「有些真相知道了反而会让人更痛苦，不如不知道。」"
  ], "scores": [4,2], "tendencies": ["H","L"], "reveal": "抗争宿命还是接受无知——左慈的选择，从来都不是表面上那么简单。"},
],
'zhangmiao.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「自由不是想做什么就做什么，而是可以选择不做什么。」——你怎么看？",
    "「人活一世，总得有点自己真正想要的东西。」——你更认同？",
    "「潇洒不是不在乎，而是在乎了也不表现出来。」——你的看法？"
  ], "scores": [3,2,4], "tendencies": ["M","L","H"], "reveal": "约束中的自由、真实欲望、隐忍的潇洒——三种活法。"},
  {"dim_offset": 2, "type": "daily", "texts": [
    "你在绣衣楼的酒宴上被灌了很多酒，有人趁机套你的话。你——",
    "你负责押送一批重要物资，途中遇到暴雨和山洪，路被断了。你——",
    "一位密探私下找你借钱，说是家里有急事。你——"
  ], "scores": [2,3.5,4], "tendencies": ["L","M","H"], "reveal": "应变、坚持、善意——日常中的每个选择都在塑造你的为人。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「我这辈子没后悔过任何事，因为每一步都是我自己的选择。」",
    "「人嘛，活得开心最重要，其他的都无所谓。」"
  ], "scores": [4,2], "tendencies": ["H","L"], "reveal": "自主担当还是随遇而安——张邈式洒脱的两种解读。"},
],
'achan.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「忠诚不是服从，而是即使被命令离开，也会默默守护。」——你怎么看？",
    "「沉默不代表无话可说，有时候只是不想伤害对方。」——你认同吗？",
    "「我不需要被理解，只需要被信任。」——你的看法？"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "无声的守护、克制的表达、坚定的信任——阿蝉式的温柔。"},
  {"dim_offset": 2, "type": "daily", "texts": [
    "你独自巡逻时发现绣衣楼的围墙被人动了手脚。你——",
    "广陵王让你保护一位身份特殊的访客，但你发现此人与你的过去有关。你——",
    "你在厨房做宵夜时，听到隔壁密探在议论你的出身。你——"
  ], "scores": [3,2,4], "tendencies": ["M","L","H"], "reveal": "职责优先、情感纠葛、隐忍克制——阿蝉的日常充满了这样的瞬间。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「我活着就是为了守护一个人，除此之外，别无所求。」",
    "「就算全世界都抛弃了她，我也会站在她身后。」"
  ], "scores": [2,5], "tendencies": ["L","H"], "reveal": "守护的定义可以很轻，也可以重到用一生去践行。"},
],
'chendeng.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「读书是为了明理，不是为了显摆。」——你怎么看？",
    "「真正的聪明人懂得藏拙，只有蠢人才会处处表现。」——你认同吗？",
    "「知识本身没有用，用对了地方才有用。」——你的看法？"
  ], "scores": [3,4,2], "tendencies": ["M","H","L"], "reveal": "求知、藏锋、实用——三种对待智慧的态度。"},
  {"dim_offset": 2, "type": "daily", "texts": [
    "你在绣衣楼的书房整理情报时，发现一份文件记载了你不该知道的事情。你——",
    "广陵王让你去谈判一个棘手的同盟关系，对方是个出了名难缠的人。你——",
    "一位年轻密探向你请教如何提高情报分析能力。你——"
  ], "scores": [2,3.5,4], "tendencies": ["L","M","H"], "reveal": "守密、策略、传承——文人密探的三种日常考验。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「与其用刀剑解决问题，不如用一句话让对手自己放下武器。」",
    "「有些人不值得你费心思，但为了大局，你必须费心思。」"
  ], "scores": [2,4], "tendencies": ["L","H"], "reveal": "理想主义还是现实主义——陈登的答案从来都是后者。"},
],
'guojia.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「人活着的乐趣，就在于想做什么就做什么。」——你怎么看？",
    "「无聊是最大的敌人，比任何对手都可怕。」——你认同吗？",
    "「天才和疯子只差一步，而我刚好站在那条线上。」——你的看法？"
  ], "scores": [3,2,4], "tendencies": ["M","L","H"], "reveal": "自由、刺激、极限——郭嘉的人生信条从不走寻常路。"},
  {"dim_offset": 2, "type": "daily", "texts": [
    "你在绣衣楼执行任务时，发现了一个可以用来要挟上层的把柄。你——",
    "广陵王布置了一个你觉得毫无意义的任务。你——",
    "你和另一位密探同时发现了关键情报，但他抢先一步上报了。你——"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "权力游戏中的选择，暴露你最真实的行事风格。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「规则是给普通人定的，聪明人负责利用规则。」",
    "「我这辈子只做自己觉得有趣的事，其他的都无所谓。」"
  ], "scores": [4,2.5], "tendencies": ["H","L"], "reveal": "掌控规则还是享受自由——郭嘉选择了两条路都走。"},
],
'zhouyu.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「大局为重，不是不考虑个人，而是个人的得失在大局面前微不足道。」——你怎么看？",
    "「优雅不是天生的，是在无数次狼狈之后练出来的。」——你认同吗？",
    "「有些人注定要承担更多，不是因为能力，而是因为责任。」——你的看法？"
  ], "scores": [3.5,2,4], "tendencies": ["H","L","M"], "reveal": "责任、修炼、担当——周瑜式的从容背后是无数次的咬牙。"},
  {"dim_offset": 2, "type": "daily", "texts": [
    "你负责统筹一场多方参与的密探行动，其中两个小队因为过去的恩怨拒绝配合。你——",
    "广陵王让你在一众密探中选拔一位新任队长。你——",
    "你在执行任务时受了伤，但伤口不重，任务还没结束。你——"
  ], "scores": [2,3.5,4], "tendencies": ["L","M","H"], "reveal": "协调、识人、坚韧——统帅的日常，考验的是格局和定力。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「你可以恨我，但不能恨我做的决定，因为那是唯一正确的选择。」",
    "「我不是不在乎，而是不能在乎。一在乎，就会做错。」"
  ], "scores": [3,5], "tendencies": ["M","H"], "reveal": "理性到极致就是残忍——但周瑜从不认为这是残忍。"},
],
'lvbu.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「强者不需要理由，弱者才需要借口。」——你怎么看？",
    "「战斗不是为了证明什么，而是因为这是唯一会做的事。」——你认同吗？",
    "「所谓的忠诚，不过是你找到了一个值得效忠的人。」——你的看法？"
  ], "scores": [3.5,4,2], "tendencies": ["H","H","L"], "reveal": "力量本能、战斗宿命、忠诚定义——吕布的三重人格。"},
  {"dim_offset": 2, "type": "value", "texts": [
    "「他们说我三姓家奴，可谁又给过我一个不用背叛的理由？」——你怎么看？",
    "「我不需要被理解，只需要被需要。」——你认同吗？",
    "「天下人笑我又如何？天下人又有几个敢站在我面前？」——你的看法？"
  ], "scores": [2,4,3.5], "tendencies": ["L","H","M"], "reveal": "被误解的委屈、存在的价值、不屈的骄傲——吕布的孤独很少有人能懂。"},
  {"dim_offset": 1, "type": "daily", "texts": [
    "绣衣楼举行武力比试，对手故意挑衅你。你——",
    "你接到一个潜入任务，但场地太小，你的武器施展不开。你——",
    "一位年轻密探害怕出任务，找你诉苦。你——"
  ], "scores": [4,2,3], "tendencies": ["H","L","M"], "reveal": "武力、适应、意外温柔——吕布的反差在日常中展现。"},
  {"dim_offset": 3, "type": "extreme", "texts": [
    "「我就是我，不需要任何人来定义我是谁。」",
    "「如果能找到一个值得我用命去守护的人，我就心满意足了。」"
  ], "scores": [3,5], "tendencies": ["M","H"], "reveal": "自我还是他者——吕布的答案可能比你想象的更柔软。"},
],
'zhouzhong.json': [
  {"dim_offset": 0, "type": "value", "texts": [
    "「我这种人，能在别人眼里留下一点影子就算不错了。」——你怎么看这种自嘲？",
    "「比起被人记住，我更害怕被人看穿。」——你觉得呢？",
    "「笨拙也是一种才华，至少说明你是认真的。」——你认同吗？"
  ], "scores": [2,4,3], "tendencies": ["L","H","M"], "reveal": "自我贬低背后往往藏着意想不到的清醒——周忠从不只是'没用'而已。"},
  {"dim_offset": 2, "type": "daily", "texts": [
    "绣衣楼分配任务，所有人都被派了重要的活，只有你被安排去看守仓库。你——",
    "你在整理旧档案时发现了一份被遗漏的重要情报。你——",
    "广陵王在众人面前随口夸了你一句，但你不确定是真心还是客套。你——"
  ], "scores": [2,3.5,4], "tendencies": ["L","M","H"], "reveal": "被忽视时的反应，最能看出一个人是安于现状还是暗中蓄力。"},
  {"dim_offset": 4, "type": "extreme", "texts": [
    "「我宁愿做一个被人遗忘的影子，也不要做一只被关在笼子里的鸟。」",
    "「不聪明没关系，只要能在关键时刻，站在对的位置上就够了。」"
  ], "scores": [3,4.5], "tendencies": ["M","H"], "reveal": "周忠式的人生哲学：看似认命，实则暗藏锋芒——你品，你细品。"},
],
}

for fname, qs in questions.items():
    path = f'{BASE}/{fname}'
    data = load(path)
    prefix = fname.replace('.json','')
    for i, q in enumerate(qs):
        nid = next_id(data, prefix)
        dim = dims[(q['dim_offset'] + i) % len(dims)]
        opt = {"label": "A", "text": q['texts'][0], "scores": {"S1": q['scores'][0]}, "tendency": q['tendencies'][0]}
        opt2 = {"label": "B", "text": q['texts'][1], "scores": {"S1": q['scores'][1]}, "tendency": q['tendencies'][1]}
        if len(q['texts']) == 3:
            opt3 = {"label": "C", "text": q['texts'][2], "scores": {"S1": q['scores'][2]}, "tendency": q['tendencies'][2]}
            opts = [opt, opt2, opt3]
        else:
            opts = [opt, opt2]
        new_q = {
            "id": nid,
            "dimension": dim,
            "cross_dimension": None,
            "type": q['type'],
            "source_character": None,
            "source_story": None,
            "route_hint": None,
            "city_hint": None,
            "text": q['texts'][0].split('——')[0].split('「')[0].split('？')[0].strip() if q['type']=='extreme' else q['texts'][0].split('——')[0].strip(),
            "options": opts,
            "reveal": q.get('reveal', None)
        }
        # Fix text for value/daily: use full first option text as question
        if q['type'] in ('value', 'daily'):
            new_q['text'] = q['texts'][0].split('——')[0].strip()
        elif q['type'] == 'extreme':
            new_q['text'] = "以下两句话，你更认同哪句？"
        data.append(new_q)
    save(path, data)
    print(f'{fname}: added {len(qs)} questions, total now {len(data)}')
