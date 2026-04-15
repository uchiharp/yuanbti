#!/usr/bin/env python3
"""生成batch4d的14道剧情题"""
import json, os

OUT = "/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions"

questions = [
    # 1. 袁绍 - S9权力 H(4)
    {
        "id": "q_yuanshao_1",
        "dimension": "S9",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "袁绍",
        "source_story": "邺城·颜良文丑出征",
        "route_hint": None,
        "city_hint": "邺城",
        "text": "邺城议事堂上，战事一触即发，袁绍起身环顾众将，拔刀割指滴入鸡血碗中——「人选就此决定！取鸡血酒来，为三位勇士送行！」他转头看向颜良与文丑，目光灼灼。若你是袁绍，在众人面前以歃血为盟的方式号令三军，你内心的真实想法是——",
        "options": [
            {"label": "A", "text": "颜良文丑勇冠三军，有他们在，此战必胜无疑。", "scores": {"S9": 2}, "tendency": "L"},
            {"label": "B", "text": "以血酒凝聚军心，让他们为我效死，此战不可不胜。", "scores": {"S9": 3}, "tendency": "M"},
            {"label": "C", "text": "将士们需要看到我的决断，这杯酒喝下去，退路便断了。", "scores": {"S9": 4}, "tendency": "H"}
        ],
        "reveal": "袁绍以歃血为盟激励将士出征，既是对部下的信任，也是以仪式感巩固自身在河北的号令之权。"
    },
    # 2. 曹操 - S7锋芒 H(4)
    {
        "id": "q_caocao_1",
        "dimension": "S7",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "曹操",
        "source_story": "许县·论吕布",
        "route_hint": None,
        "city_hint": "许县",
        "text": "许县军帐中，曹操放下军报，目光沉沉——「吕布是猛虎，徘徊在侧，迟早露出獠牙。」帐中诸将沉默不语。他转而看向众人，语气不变：「我不找，袁氏也会来找。他藏不住的。」若你是曹操，面对如吕布这般难以驯服的猛将，你的策略是——",
        "options": [
            {"label": "A", "text": "先稳住他，待时机成熟再一举铲除，不可打草惊蛇。", "scores": {"S7": 2}, "tendency": "L"},
            {"label": "B", "text": "既然迟早要翻脸，不如主动出击，打他个措手不及。", "scores": {"S7": 3.5}, "tendency": "H"},
            {"label": "C", "text": "放长线钓大鱼，让他去替我咬别人，最后再收拾残局。", "scores": {"S7": 3}, "tendency": "M"}
        ],
        "reveal": "曹操对吕布的判断精准而冷酷——不急于动手，也不放任不管，而是以猎人的耐心等待最佳时机。"
    },
    # 3. 孙坚 - S5行动 M(3) （数据库无台词，基于游戏剧情）
    {
        "id": "q_sunjian_1",
        "dimension": "S5",
        "cross_dimension": None,
        "type": "story_anon",
        "source_character": None,
        "source_story": None,
        "route_hint": ["长沙线"],
        "city_hint": "长沙",
        "text": "江东猛虎身经百战，入洛阳宫时于枯井中得传国玉玺。一老臣跪阻于前：「此乃天子信物，将军若私藏，恐为天下所不容！」四周无人，怀中玉玺温热。你——",
        "options": [
            {"label": "A", "text": "收起玉玺，但对外绝不声张，先保命要紧。", "scores": {"S5": 2}, "tendency": "L"},
            {"label": "B", "text": "坦然收下——天命所归，不取白不取。", "scores": {"S5": 3.5}, "tendency": "H"},
            {"label": "C", "text": "犹豫片刻，决定先带回去再从长计议。", "scores": {"S5": 3}, "tendency": "M"}
        ],
        "reveal": "这个场景来自孙坚的洛阳剧情——传国玉玺是天下权柄的象征，取与不取，皆为豪赌。"
    },
    # 4. 刘协 - S9权力 M(3)
    {
        "id": "q_liuxie_1",
        "dimension": "S9",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "刘协",
        "source_story": "许县·天子召见广陵王",
        "route_hint": None,
        "city_hint": "许县",
        "text": "刘协端坐于案后，目光直视来人——「广陵王既然来了，为何不来见朕。」语气平静却不容回避。他顿了顿：「你是绣衣校尉，直属于天子的人。」若你是这位年轻的天子，面对被曹操架空的朝廷，你会如何对待绣衣楼——",
        "options": [
            {"label": "A", "text": "绣衣楼是朕仅存的倚仗，必须牢牢攥在手中。", "scores": {"S9": 4}, "tendency": "H"},
            {"label": "B", "text": "虽无力直接号令，但以天子之名笼络人心，徐图恢复。", "scores": {"S9": 3}, "tendency": "M"},
            {"label": "C", "text": "曹操在旁虎视，不如装作不在意，暗中联络即可。", "scores": {"S9": 2}, "tendency": "L"}
        ],
        "reveal": "刘协虽为天子，实为傀儡，但他从未放弃对权力的渴望——以绣衣楼为暗线，试图在夹缝中重掌天下。"
    },
    # 5. 郭汜 - S2情感 H(4)
    {
        "id": "q_guosi_1",
        "dimension": "S2",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "郭汜",
        "source_story": "长安·寻回居米",
        "route_hint": ["西凉线"],
        "city_hint": "长安",
        "text": "郭汜一路狂奔，找到被曹操带走的孩子，紧紧抱在怀里——「……居米……叔叔一直……一直都对你好的……」声音沙哑，手臂发抖。孩子在他怀中渐渐安静下来。若你是郭汜，在乱世中对这个孩子如此牵挂，你心底最害怕的是什么——",
        "options": [
            {"label": "A", "text": "怕这孩子有朝一日知道了真相，不再认我这个叔叔。", "scores": {"S2": 3}, "tendency": "M"},
            {"label": "B", "text": "怕自己哪天战死沙场，再没人护着她。", "scores": {"S2": 4}, "tendency": "H"},
            {"label": "C", "text": "怕别人拿这孩子来要挟我，所以绝不能让人知道她的存在。", "scores": {"S2": 2}, "tendency": "L"}
        ],
        "reveal": "郭汜对居米的感情是西凉铁汉最柔软的一面——在杀伐乱世中，这个孩子是他唯一想拼命护住的人。"
    },
    # 6. 李傕 - S1权谋 H(4)
    {
        "id": "q_liqu_1",
        "dimension": "S1",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "李傕",
        "source_story": "长安·逼宫废帝",
        "route_hint": ["西凉线"],
        "city_hint": "长安",
        "text": "李傕带兵闯入朝堂，对太后冷冷道——「董太师希望太后辨明事理，在这份废帝诏书上盖玺。」太后颤声不肯，他淡淡补了一句：「杨太尉最近病休在弘农，董太师很是担心，特派我来慰问。」言下之意不言自明。若你是李傕，以胁迫为手段逼人就范时，你会——",
        "options": [
            {"label": "A", "text": "直接亮刀兵，不废话，逼她签字画押。", "scores": {"S1": 2}, "tendency": "L"},
            {"label": "B", "text": "先礼后兵，软硬兼施，让她自己明白形势。", "scores": {"S1": 4}, "tendency": "H"},
            {"label": "C", "text": "拿她身边的人开刀，杀鸡儆猴。", "scores": {"S1": 3}, "tendency": "M"}
        ],
        "reveal": "李傕的权谋在于以「关心」之名行胁迫之实——他深谙人性的软肋，不靠暴力，靠的是让对手自己害怕。"
    },
    # 7. 伏寿♀ - S2情感 H(4)
    {
        "id": "q_fushou_1",
        "dimension": "S2",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "伏寿",
        "source_story": "许县·阿春重伤",
        "route_hint": None,
        "city_hint": "许县",
        "text": "伏寿跪在地上，双手紧紧握住阿春冰冷的手——「不会的！阿春你不会死的，你不会死的！」她的眼泪砸在阿春脸上，声音哽咽到几乎破碎。阿春的手渐渐失去温度，她却死死不放。若你是伏寿，看着在意之人命悬一线，你会——",
        "options": [
            {"label": "A", "text": "强忍悲痛，赶紧去请大夫，哭解决不了任何事。", "scores": {"S2": 2}, "tendency": "L"},
            {"label": "B", "text": "什么也做不了，只想握着她的手，陪她到最后。", "scores": {"S2": 4}, "tendency": "H"},
            {"label": "C", "text": "一边呼唤她的名字不让她睡过去，一边让人去找大夫。", "scores": {"S2": 3}, "tendency": "M"}
        ],
        "reveal": "伏寿在阿春重伤时的崩溃，是她平日端庄面具下最真实的一面——她可以忍痛，却无法忍受失去。"
    },
    # 8. 刘表 - S10秩序 M(3) （数据库无台词，基于游戏剧情）
    {
        "id": "q_liubiao_1",
        "dimension": "S10",
        "cross_dimension": None,
        "type": "story_anon",
        "source_character": None,
        "source_story": None,
        "route_hint": ["长沙线"],
        "city_hint": "长沙",
        "text": "荆州牧坐镇襄阳多年，北有曹操虎视，东有孙坚窥伺。帐下谋士献策：一则趁曹操北征乌桓之际出兵中原，二则加固城防以守为上，三则遣使联络各方以待时变。荆州的存亡，系于你的一念之间——",
        "options": [
            {"label": "A", "text": "乱世之中，守好荆州一方水土，让百姓免遭战祸便是大功。", "scores": {"S10": 4}, "tendency": "H"},
            {"label": "B", "text": "坐守必亡，不如趁虚而动，即便冒险也要搏一搏。", "scores": {"S10": 2}, "tendency": "L"},
            {"label": "C", "text": "先观望局势，联络各方形成联盟，再择机而动。", "scores": {"S10": 3}, "tendency": "M"}
        ],
        "reveal": "这个场景来自刘表的荆州局势——他一生以「保境安民」为策，虽被讥为坐守，却让荆州在乱世中维持了数十年太平。"
    },
    # 9. 刘备 - S6底线 H(4)
    {
        "id": "q_liubei_1",
        "dimension": "S6",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "刘备",
        "source_story": "徐州·广陵王之局",
        "route_hint": None,
        "city_hint": "下邳",
        "text": "刘备站在城头，望着烽火连天的徐州，声音平静却坚定——「只要能保住尽可能多的人，我刘备什么都愿意做，什么罪名都愿意担下。」他转头看向身边的人：「我的仁道，就是保全尽可能多的百姓。」若你是刘备，面对「牺牲自己换取数十万百姓」的选择，你会——",
        "options": [
            {"label": "A", "text": "先保全自身实力，只有活着才能救更多人。", "scores": {"S6": 2}, "tendency": "L"},
            {"label": "B", "text": "如果自己的死能换百姓平安，那就死吧。", "scores": {"S6": 4}, "tendency": "H"},
            {"label": "C", "text": "试着找第三条路，不到万不得已不愿牺牲任何人。", "scores": {"S6": 3}, "tendency": "M"}
        ],
        "reveal": "刘备的仁道不是口号——在代号鸢的徐州线中，他真的愿意以自身为筹码换取百姓的生存。"
    },
    # 10. 吴夫人♀ - S8温柔 H(4)
    {
        "id": "q_wufuren_1",
        "dimension": "S8",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "吴夫人",
        "source_story": "寿春·家中日常",
        "route_hint": None,
        "city_hint": "寿春",
        "text": "吴夫人笑着拉过身边人的手，语气温柔——「对对对，听伯符的，千万别拘束。这是今年的桂花新酿，快尝尝。」转头又念叨：「管事，快去纺室问问，她什么时候回来？」若你是吴夫人，在乱世之中操持一大家子，你最希望给孩子们什么——",
        "options": [
            {"label": "A", "text": "安稳的生活就够了，外面的纷争让他们去操心。", "scores": {"S8": 3}, "tendency": "M"},
            {"label": "B", "text": "让每个孩子都感受到，这个家永远有人在等他们回来。", "scores": {"S8": 4}, "tendency": "H"},
            {"label": "C", "text": "教他们武艺和权术，乱世里心软是要吃亏的。", "scores": {"S8": 2}, "tendency": "L"}
        ],
        "reveal": "吴夫人是孙策孙权背后的温暖依靠——她不是不知道世道险恶，只是选择以温柔对抗乱世。"
    },
    # 11. 袁术 - S9权力 H(4)
    {
        "id": "q_yuanshu_1",
        "dimension": "S9",
        "cross_dimension": None,
        "type": "story_known",
        "source_character": "袁术",
        "source_story": "寿春·袁绍遇险",
        "route_hint": None,
        "city_hint": "寿春",
        "text": "袁术得知长兄被人带走，怒不可遏——「把囚车打开！长兄要是有事，我活剐了你们！」他猛地拔剑，目光凶狠。稍后压住怒意：「那些长老现下在何处？我要带着董奉，当面去和他们对质！」若你是袁术，面对宗族长老对长兄的不公，你会——",
        "options": [
            {"label": "A", "text": "先弄清楚前因后果，贸然动武只会让事情更糟。", "scores": {"S9": 2}, "tendency": "L"},
            {"label": "B", "text": "带人去对质，但不动手，以理服人。", "scores": {"S9": 3}, "tendency": "M"},
            {"label": "C", "text": "直接带兵闯入，用武力让所有人知道袁家不是好惹的。", "scores": {"S9": 4}, "tendency": "H"}
        ],
        "reveal": "袁术的行事风格是「先动手再说」——他对权力的理解就是用绝对的力量让所有人闭嘴。"
    },
    # 12. 公孙瓒 - S7锋芒 L(2) （数据库无台词，基于游戏剧情）
    {
        "id": "q_gongsunzan_1",
        "dimension": "S7",
        "cross_dimension": None,
        "type": "story_anon",
        "source_character": None,
        "source_story": None,
        "route_hint": ["幽州线"],
        "city_hint": "幽州",
        "text": "白马将军驻守幽州边塞多年，与乌桓骑兵反复交锋。朝中有人上书弹劾他拥兵自重、杀良冒功。传旨使者来到军营，宣读罢免诏书。将士们怒目而视，只等一声令下。你——",
        "options": [
            {"label": "A", "text": "接旨谢恩，交出兵权，回京自证清白。", "scores": {"S7": 1}, "tendency": "L"},
            {"label": "B", "text": "当场翻脸，把使者赶出去，与朝廷决裂。", "scores": {"S7": 4}, "tendency": "H"},
            {"label": "C", "text": "表面接旨，暗中联络旧部，伺机东山再起。", "scores": {"S7": 2.5}, "tendency": "M"}
        ],
        "reveal": "这个场景来自公孙瓒的幽州线——白马将军的性格刚烈直率，但锋芒太露往往招致杀身之祸。"
    },
    # 13. 陈昭 - S4面具 M(3) （数据库无台词，基于游戏剧情）
    {
        "id": "q_chenzhao_1",
        "dimension": "S4",
        "cross_dimension": None,
        "type": "story_anon",
        "source_character": None,
        "source_story": None,
        "route_hint": None,
        "city_hint": "广陵",
        "text": "绣衣楼中，你接到一道密令——去接近一位手握重兵的诸侯，获取他的军力部署。对方为人多疑，对陌生人极不信任。你需要在短时间内取得他的好感。你会——",
        "options": [
            {"label": "A", "text": "以真实身份接近，坦诚相待，用诚意打动他。", "scores": {"S4": 1}, "tendency": "L"},
            {"label": "B", "text": "伪装成落魄书生，以才华引起他的注意和怜惜。", "scores": {"S4": 3.5}, "tendency": "H"},
            {"label": "C", "text": "以商人身份混入，不刻意表现，等他主动注意到你。", "scores": {"S4": 2.5}, "tendency": "M"}
        ],
        "reveal": "陈昭是绣衣楼中最擅长伪装的密探之一——在代号鸢的世界中，面具不仅是保护色，更是武器。"
    },
    # 14. 春梦 - S2情感 H(4) （数据库无台词，基于游戏剧情）
    {
        "id": "q_chunmeng_1",
        "dimension": "S2",
        "cross_dimension": None,
        "type": "story_anon",
        "source_character": None,
        "source_story": None,
        "route_hint": None,
        "city_hint": "广陵",
        "text": "你做了一个很长很长的梦。梦里有人在叫你的名字，声音温柔又遥远。醒来时枕边微湿，窗外的月光照着空荡荡的房间。你想起梦中那个人，心中涌起一阵说不清的情绪——",
        "options": [
            {"label": "A", "text": "不过是个梦罢了，翻个身继续睡。", "scores": {"S2": 1}, "tendency": "L"},
            {"label": "B", "text": "起身写下梦中情景，怕天亮就忘了。", "scores": {"S2": 3}, "tendency": "M"},
            {"label": "C", "text": "睁眼望着天花板，任由那股情绪漫过全身，久久不愿起身。", "scores": {"S2": 4}, "tendency": "H"}
        ],
        "reveal": "春梦如其名——在代号鸢中，她游走于梦境与现实的边界，对情感的感知比任何人都敏锐。"
    }
]

# 写入各角色文件
char_map = {
    "yuanshao": [questions[0]], "caocao": [questions[1]], "sunjian": [questions[2]],
    "liuxie": [questions[3]], "guosi": [questions[4]], "liqu": [questions[5]],
    "fushou": [questions[6]], "liubiao": [questions[7]], "liubei": [questions[8]],
    "wufuren": [questions[9]], "yuanshu": [questions[10]], "gongsunzan": [questions[11]],
    "chenzhao": [questions[12]], "chunmeng": [questions[13]]
}

os.makedirs(OUT, exist_ok=True)
for fname, qs in char_map.items():
    fpath = os.path.join(OUT, f"{fname}.json")
    existing = []
    if os.path.exists(fpath):
        with open(fpath) as f:
            existing = json.load(f)
    existing.extend(qs)
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"✅ {fname}.json: {len(existing)} questions")

print("\nDone! 14 questions generated.")
