import json

data = [
  # ===== sweet (5) =====
  {
    "id": "左慈_sweet_1", "type": "sweet", "dimension": ["S2", "S8"], "source_character": "左慈",
    "text": "七夕夜市，左慈替你造了一桶冰给面摊老板换凉面。他看着你吃得满头汗，替你擦了擦额角。",
    "options": [
      {"label": "A", "text": "把凉面递到他嘴边让他也尝一口", "scores": {"S2": 5, "S8": 3}, "tendency": "H"},
      {"label": "B", "text": "问他想不想去下一个摊子转转", "scores": {"S2": 3, "S8": 1}, "tendency": "M"},
      {"label": "C", "text": "安静吃面，偶尔抬头冲他笑一下", "scores": {"S2": 1, "S8": 5}, "tendency": "L"}
    ],
    "reveal": "「吾辟谷，不食炙肉，你吃吧。」辟谷不食，却替你烤肉造冰。温柔从不在嘴上。"
  },
  {
    "id": "左慈_sweet_2", "type": "sweet", "dimension": ["S5", "S4"], "source_character": "左慈",
    "text": "隐鸢阁学宫经筵上，左慈注意到你听得犯困，微微侧身挡住了夫子视线。",
    "options": [
      {"label": "A", "text": "趁机靠在他肩上闭眼小睡", "scores": {"S5": 1, "S4": 1}, "tendency": "L"},
      {"label": "B", "text": "戳戳他手背表示自己没事继续听", "scores": {"S5": 3, "S4": 3}, "tendency": "M"},
      {"label": "C", "text": "小声问他记不记得上次在这偷偷扔夫子卷轴的事", "scores": {"S5": 5, "S4": 5}, "tendency": "H"}
    ],
    "reveal": "「困了吗？枕在吾的背上，悄悄睡一会儿吧。」他永远替你打掩护。"
  },
  {
    "id": "左慈_sweet_3", "type": "sweet", "dimension": ["S8", "S6"], "source_character": "左慈",
    "text": "左慈帮你梳毛时，你发现他手在轻轻发抖——已经梳了很久一声也没吭。",
    "options": [
      {"label": "A", "text": "按住他的手说休息一会儿吧", "scores": {"S8": 5, "S6": 3}, "tendency": "H"},
      {"label": "B", "text": "假装没注意到继续享受", "scores": {"S8": 1, "S6": 1}, "tendency": "L"},
      {"label": "C", "text": "反过来拉他坐下你帮他理理头发", "scores": {"S8": 3, "S6": 5}, "tendency": "M"}
    ],
    "reveal": "「吾会很轻、很轻，让你做个好梦的。」他可以一直为你做这些小事，从不觉得累。"
  },
  {
    "id": "左慈_sweet_4", "type": "sweet", "dimension": ["S2", "S7"], "source_character": "左慈",
    "text": "七夕灯会，左慈一夜赢了六个月观星台收益，把彩头全塞给你。",
    "options": [
      {"label": "A", "text": "挑一个最好看的挂在他衣带上", "scores": {"S2": 5, "S7": 5}, "tendency": "H"},
      {"label": "B", "text": "全收下说回去分给绣衣楼的密探们", "scores": {"S2": 1, "S7": 1}, "tendency": "L"},
      {"label": "C", "text": "拉他去下一个摊位说这些不够还要赢更多", "scores": {"S2": 3, "S7": 3}, "tendency": "M"}
    ],
    "reveal": "「一夜之间赢了六个月的收益，满意了？哈……心满意足了，就去下一个地方吧。」"
  },
  {
    "id": "左慈_sweet_5", "type": "sweet", "dimension": ["S3", "S2"], "source_character": "左慈",
    "text": "左慈端来一碗麦草汤，特意吹凉递给你。他说翠叶在汤汁里浮沉像一艘小舟。",
    "options": [
      {"label": "A", "text": "接过来喝一口然后非要他也尝一口嫩叶尖", "scores": {"S3": 5, "S2": 5}, "tendency": "H"},
      {"label": "B", "text": "问他观星台收益够不够再买一车麦草", "scores": {"S3": 3, "S2": 1}, "tendency": "M"},
      {"label": "C", "text": "安静喝完把空碗递给他时碰到他的手指", "scores": {"S3": 1, "S2": 3}, "tendency": "L"}
    ],
    "reveal": "「吾在吹这碗麦草，你吃的时候冷热更适口。」辟谷之人吹的不是麦草，是陪伴。"
  },
  # ===== funny (5) =====
  {
    "id": "左慈_funny_1", "type": "funny", "dimension": ["S7", "S5"], "source_character": "左慈",
    "text": "左慈投壶连中十支射箭连中三箭红心，老板不给奖还掀桌赶人。他一脸无辜看着你。",
    "options": [
      {"label": "A", "text": "拉着他去下一摊跟新老板说他是第一次玩", "scores": {"S7": 3, "S5": 5}, "tendency": "H"},
      {"label": "B", "text": "跟老板理论说他没写不能用仙术的规则", "scores": {"S7": 5, "S5": 3}, "tendency": "M"},
      {"label": "C", "text": "忍住笑把他拖走说别把人家摊子拆了", "scores": {"S7": 1, "S5": 1}, "tendency": "L"}
    ],
    "reveal": "「不能用仙术操控箭直接进壶？可是规则上没写……啊，他临时把规则添上了。」"
  },
  {
    "id": "左慈_funny_2", "type": "funny", "dimension": ["S4", "S8"], "source_character": "左慈",
    "text": "左慈喝了一口酒当场昏倒，醒来发现已是第二天。他咳嗽一声试图装作什么都没发生。",
    "options": [
      {"label": "A", "text": "面不改色问他昨晚说梦话喊了什么", "scores": {"S4": 5, "S8": 1}, "tendency": "H"},
      {"label": "B", "text": "假装也没醒多久说刚才自己也睡着了", "scores": {"S4": 1, "S8": 3}, "tendency": "L"},
      {"label": "C", "text": "把酒杯端到他面前问他要不要再试一口", "scores": {"S4": 3, "S8": 5}, "tendency": "M"}
    ],
    "reveal": "「试一口……咚。……嗯？吾睡着了吗？」半口酒就倒，第二天：「天亮了，已经是第二天了吗。」"
  },
  {
    "id": "左慈_funny_3", "type": "funny", "dimension": ["S5", "S1"], "source_character": "左慈",
    "text": "摔跤场上左慈连猜连中，全场围过来要他帮忙下注。他转头看你，眼神像在问怎么办。",
    "options": [
      {"label": "A", "text": "拍他肩说你负责猜我负责收钱", "scores": {"S5": 5, "S1": 3}, "tendency": "H"},
      {"label": "B", "text": "挤出路人的微笑假装不认识他", "scores": {"S5": 1, "S1": 5}, "tendency": "L"},
      {"label": "C", "text": "拉着他说走走走换一家", "scores": {"S5": 3, "S1": 1}, "tendency": "M"}
    ],
    "reveal": "「想赌黑腰带的？押黄腰带的吧，他会赢。」——然后被老板撵出来：「真是个刻薄的人啊。」"
  },
  {
    "id": "左慈_funny_4", "type": "funny", "dimension": ["S3", "S7"], "source_character": "左慈",
    "text": "左慈替喷火艺人召唤祝融之火，结果来了好多人还有医师，场面失控。他悄悄看了你一眼。",
    "options": [
      {"label": "A", "text": "趁乱拉着他溜走快步混进人群", "scores": {"S3": 3, "S7": 1}, "tendency": "L"},
      {"label": "B", "text": "留下一句火是真火但人没事再走", "scores": {"S3": 5, "S7": 3}, "tendency": "M"},
      {"label": "C", "text": "憋着笑问他下次能不能只帮一半", "scores": {"S3": 1, "S7": 5}, "tendency": "H"}
    ],
    "reveal": "「吾帮他一下……祝融，召来……来了好多人，还有医师。」左慈的好心永远配着灾难级的执行。"
  },
  {
    "id": "左慈_funny_5", "type": "funny", "dimension": ["S2", "S5"], "source_character": "左慈",
    "text": "左慈在古董摊一眼看穿所有假货，摊主脸色越来越难看。他还在认真分析假松石链子的年代错误。",
    "options": [
      {"label": "A", "text": "拽着他走说那边有更好看的摊子", "scores": {"S2": 1, "S5": 1}, "tendency": "L"},
      {"label": "B", "text": "在旁边接话说先生说得对能不能便宜点", "scores": {"S2": 3, "S5": 5}, "tendency": "M"},
      {"label": "C", "text": "故意拿起一件假货大声说这个是真的吧好好看", "scores": {"S2": 5, "S5": 3}, "tendency": "H"}
    ],
    "reveal": "「吾没有生气……没事的，不用派人查封这家店。没事的。」然而那个老板已经快气炸了。"
  },
  # ===== angst (5) =====
  {
    "id": "左慈_angst_1", "type": "angst", "dimension": ["S2", "S6"], "source_character": "左慈",
    "text": "七载重逢，左慈说你不该回来。他看起来比记忆中苍老许多，却还在笑着说只是有些困倦。",
    "options": [
      {"label": "A", "text": "什么都不说就站在他身边不走", "scores": {"S2": 1, "S6": 3}, "tendency": "L"},
      {"label": "B", "text": "问他这七年每一天都是怎么过的", "scores": {"S2": 3, "S6": 5}, "tendency": "M"},
      {"label": "C", "text": "说你不是回来看他的你是来带他走的", "scores": {"S2": 5, "S6": 1}, "tendency": "H"}
    ],
    "reveal": "「为什么……那么多次……为什么……还要回来……」他说不该回来，但握着你的手始终没有松开。"
  },
  {
    "id": "左慈_angst_2", "type": "angst", "dimension": ["S4", "S2"], "source_character": "左慈",
    "text": "左慈说没遇见你的事情许多都记不清了。他让你别这样看着他，说如果再想起什么一定告诉你。",
    "options": [
      {"label": "A", "text": "点头说好不追问了", "scores": {"S4": 1, "S2": 1}, "tendency": "L"},
      {"label": "B", "text": "说没关系记得的就已经够了", "scores": {"S4": 3, "S2": 5}, "tendency": "M"},
      {"label": "C", "text": "问他是不是忘记的比记得的多得多", "scores": {"S4": 5, "S2": 3}, "tendency": "H"}
    ],
    "reveal": "「别这样看着吾，如果吾再想起什么，一定告诉你。」活了太久的人，记忆像沙子从指缝漏掉。"
  },
  {
    "id": "左慈_angst_3", "type": "angst", "dimension": ["S6", "S1"], "source_character": "左慈",
    "text": "左慈说雪球一旦从山顶滚落无法阻挡。但下一句是抱着成为下一个公敌的觉悟做你觉得正确的事吧。",
    "options": [
      {"label": "A", "text": "问他如果雪球真的滚下来他会不会挡在前面", "scores": {"S6": 5, "S1": 3}, "tendency": "H"},
      {"label": "B", "text": "沉默片刻然后说你知道了", "scores": {"S6": 1, "S1": 1}, "tendency": "L"},
      {"label": "C", "text": "说既然挡不住那就让雪球来得更大些吧", "scores": {"S6": 3, "S1": 5}, "tendency": "M"}
    ],
    "reveal": "「无论发生何事，吾都会站在你这边。」他看清了残酷真相，但选择站在你这边。"
  },
  {
    "id": "左慈_angst_4", "type": "angst", "dimension": ["S8", "S2"], "source_character": "左慈",
    "text": "左慈讲起外大父外大母临终时以为母亲回来了，他拉着他们的手一遍遍说母亲回来了。语气很平静。",
    "options": [
      {"label": "A", "text": "沉默地听着不插话", "scores": {"S8": 1, "S2": 1}, "tendency": "L"},
      {"label": "B", "text": "说他们一定知道那是他不是母亲但很欣慰", "scores": {"S8": 5, "S2": 3}, "tendency": "M"},
      {"label": "C", "text": "握住他的手说以后不会让他一个人", "scores": {"S8": 3, "S2": 5}, "tendency": "H"}
    ],
    "reveal": "「于是拉着他们的手，一遍一遍告诉他们，是啊，母亲回来了……忽然之间，许多事情结束了。」"
  },
  {
    "id": "左慈_angst_5", "type": "angst", "dimension": ["S9", "S6"], "source_character": "左慈",
    "text": "左慈说你父亲杀气疑心都重，母亲性情软弱在懊悔中郁郁而终。最后说就算相遇你也未必能和她相处多深。",
    "options": [
      {"label": "A", "text": "说有他在就不需要再想这些了", "scores": {"S9": 1, "S6": 3}, "tendency": "L"},
      {"label": "B", "text": "问他如果当年他先找到的是母亲而不是你会怎样", "scores": {"S9": 5, "S6": 1}, "tendency": "M"},
      {"label": "C", "text": "沉默很久然后说那你呢你有没有懊悔过什么", "scores": {"S9": 3, "S6": 5}, "tendency": "H"}
    ],
    "reveal": "「你的母亲……是个性子单纯的孩子。王府出事后一直在懊悔……最后郁郁而终。」他说得平静，像在讲别人的事。"
  },
  # ===== scheme (5) =====
  {
    "id": "左慈_scheme_1", "type": "scheme", "dimension": ["S1", "S9"], "source_character": "左慈",
    "text": "左慈说权力是石头，先让他们恐惧你才能让他们爱你。他问你如果是你会怎么用这块石头。",
    "options": [
      {"label": "A", "text": "说石头太沉了你更想用丝绸裹着递出去", "scores": {"S1": 1, "S9": 1}, "tendency": "L"},
      {"label": "B", "text": "说先让人恐惧确实高效但收尾要干净", "scores": {"S1": 3, "S9": 5}, "tendency": "M"},
      {"label": "C", "text": "反问他当年为什么不用石头砸回去", "scores": {"S1": 5, "S9": 3}, "tendency": "H"}
    ],
    "reveal": "「权力是石头，你把它裹上丝绸也好、染成彩色也好，它的本质都是石头。」这是左慈教广陵王的权谋课。"
  },
  {
    "id": "左慈_scheme_2", "type": "scheme", "dimension": ["S9", "S6"], "source_character": "左慈",
    "text": "犬都面临抉择：驱逐所有西凉犬是最理智的做法。左慈却说抱着成为下一个公敌的觉悟做你觉得正确的事吧。",
    "options": [
      {"label": "A", "text": "选择驱逐西凉犬先保住犬都再说", "scores": {"S9": 1, "S6": 1}, "tendency": "L"},
      {"label": "B", "text": "私下安排西凉犬秘密转移面上配合驱逐", "scores": {"S9": 5, "S6": 3}, "tendency": "M"},
      {"label": "C", "text": "公开反对驱逐哪怕成为下一个公敌", "scores": {"S9": 3, "S6": 5}, "tendency": "H"}
    ],
    "reveal": "「毫无理智，但具有道义的选择。」——他明知你会选最不理智的路，依然站在你身后。"
  },
  {
    "id": "左慈_scheme_3", "type": "scheme", "dimension": ["S1", "S10"], "source_character": "左慈",
    "text": "左慈分析各州铸钱权谋：废旧钱铸新钱把财政大权收归长安。他说要下很狠的手榨到离死只有一步再停。",
    "options": [
      {"label": "A", "text": "问他说的是汉朝的事还是现在的事", "scores": {"S1": 3, "S10": 1}, "tendency": "L"},
      {"label": "B", "text": "说这种手段一旦失控就是灭顶之灾执行的人选很重要", "scores": {"S1": 5, "S10": 5}, "tendency": "M"},
      {"label": "C", "text": "默默记下想着哪天也许用得上", "scores": {"S1": 1, "S10": 3}, "tendency": "H"}
    ],
    "reveal": "「执行起来是一套非常精密的流程，任何一个环节失控，王朝的经济都会顷刻崩塌。」"
  },
  {
    "id": "左慈_scheme_4", "type": "scheme", "dimension": ["S1", "S3"], "source_character": "左慈",
    "text": "张邈以天命为由要左慈舍弃你。左慈说天若因天命杀她吾也不在乎撕天裂地。",
    "options": [
      {"label": "A", "text": "说他的话比什么天命都管用", "scores": {"S1": 1, "S3": 3}, "tendency": "L"},
      {"label": "B", "text": "问他撕天裂地的代价是什么", "scores": {"S1": 3, "S3": 5}, "tendency": "M"},
      {"label": "C", "text": "说不用他撕天裂地你会自己走出一条路", "scores": {"S1": 5, "S3": 1}, "tendency": "H"}
    ],
    "reveal": "「只因一段虚无缥缈的天命？……天若因天命杀她，吾也不在乎撕天裂地。」他从不参与世间争斗，但为你除外。"
  },
  {
    "id": "左慈_scheme_5", "type": "scheme", "dimension": ["S9", "S1"], "source_character": "左慈",
    "text": "左慈说隐鸢阁派系复杂能继续缠斗就不必分出高下。他选择在山外多停留避免被扯去当矛和盾。",
    "options": [
      {"label": "A", "text": "支持他留在山外但问他阁里的事要不要提前布置", "scores": {"S9": 5, "S1": 3}, "tendency": "M"},
      {"label": "B", "text": "说你需要他在身边阁里的事可以放一放", "scores": {"S9": 1, "S1": 1}, "tendency": "L"},
      {"label": "C", "text": "问他隐鸢阁里到底有几派势力你想知道全貌", "scores": {"S9": 3, "S1": 5}, "tendency": "H"}
    ],
    "reveal": "「让他们继续斗吧。吾可以在山外多停留些时日。」他的不参与是选择，不是无能为力。"
  },
  # ===== daily (5) =====
  {
    "id": "左慈_daily_1", "type": "daily", "dimension": ["S3", "S8"], "source_character": "左慈",
    "text": "左慈辟谷不吃烤肉但他替你烤，还念叨肉蛋鱼虾都要多吃。你发现他翻肉串的手法比你还熟练。",
    "options": [
      {"label": "A", "text": "直接把烤好的肉串递到他嘴边让他尝一口", "scores": {"S3": 5, "S8": 5}, "tendency": "H"},
      {"label": "B", "text": "说你够了够了再烤吃不完浪费", "scores": {"S3": 3, "S8": 1}, "tendency": "M"},
      {"label": "C", "text": "默默吃偶尔抬头说一句好吃", "scores": {"S3": 1, "S8": 3}, "tendency": "L"}
    ],
    "reveal": "「没事，你慢慢吃。吾替你烤。」辟谷之人练出了最好的烤肉技术，全是为了让你多吃一点。"
  },
  {
    "id": "左慈_daily_2", "type": "daily", "dimension": ["S10", "S3"], "source_character": "左慈",
    "text": "左慈不喜欢修剪过的盆景，说矫揉造作，万物天然之美就很好。他看着被修剪成畸形的梅树沉默了很久。",
    "options": [
      {"label": "A", "text": "说梅树能活很久总有一天能恢复自由", "scores": {"S10": 5, "S3": 1}, "tendency": "M"},
      {"label": "B", "text": "说其实修剪过的也有修剪过的美", "scores": {"S10": 1, "S3": 3}, "tendency": "L"},
      {"label": "C", "text": "岔开话题拉他去看旁边的野花", "scores": {"S10": 3, "S3": 5}, "tendency": "H"}
    ],
    "reveal": "「梅树能活很久，比绝大多数人都久。只要活下去，总有一天能恢复自由。」他说的是树，也是人。"
  },
  {
    "id": "左慈_daily_3", "type": "daily", "dimension": ["S5", "S8"], "source_character": "左慈",
    "text": "左慈说你上次议事突然倒在案上瞬间睡着了，醒来时脸上压了许多红印。他问你熬夜时都在看什么。",
    "options": [
      {"label": "A", "text": "老老实实说在看公文", "scores": {"S5": 3, "S8": 1}, "tendency": "M"},
      {"label": "B", "text": "说在想他所以没睡好", "scores": {"S5": 1, "S8": 5}, "tendency": "H"},
      {"label": "C", "text": "反问他仙人不需要睡觉是不是很羡慕可以赖床的人", "scores": {"S5": 5, "S8": 3}, "tendency": "L"}
    ],
    "reveal": "「仙人没有赖床的概念吧？因为本来就不需要睡觉。」但他说该休息就休息，天不会塌的。"
  },
  {
    "id": "左慈_daily_4", "type": "daily", "dimension": ["S4", "S6"], "source_character": "左慈",
    "text": "左慈看到你书房挤满了密探，问到底睡了几个人。你说都是来保护你的。他眯了眯眼。",
    "options": [
      {"label": "A", "text": "坦然说就是大家一起开个会开晚了", "scores": {"S4": 5, "S6": 1}, "tendency": "M"},
      {"label": "B", "text": "心虚地岔开话题说师尊要不要喝茶", "scores": {"S4": 1, "S6": 3}, "tendency": "L"},
      {"label": "C", "text": "理直气