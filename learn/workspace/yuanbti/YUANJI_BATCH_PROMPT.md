# 袁基批次出题 Prompt（v3 — 复杂场景专项修复版）

## 你的任务
为袁基出6个批次各5道性格测试题，每道基于真实剧情/台词。

## ⚠️ v3核心修复：复杂场景处理

### 问题根源
之前权谋/名场面批次频繁出错，原因是：
1. 题干限3句话 → 复杂权谋场景信息不足 → AI脑补 → 脑补就错
2. 没给完整剧情上下文 → AI不理解角色动机和阵营关系 → 从错误立场出发
3. 袁基权谋是层层嵌套的（表面一层/实际一层/对广陵王又一层）→ 更容易搞错

### 新规则
1. **复杂场景允许4-5句话** — 权谋博弈和名场面还原，交代背景比字数限制更重要
2. **出题前必须先拉台词理解剧情** — 不要凭印象，从数据库拉完整台词再分析
3. **从角色立场出发** — 袁基是袁氏嫡长公子，心向袁氏，不会否定自己的家族。他的算计是为了袁氏，不是为了害袁氏
4. **考虑广陵王当时的处境** — 她在剧情中知道什么、不知道什么、能做什么、不能做什么

## 袁基人设（必须严格遵守）

### 核心定位：绿茶/操控型
- **表面**：光风霁月、温文尔雅、悲天悯人
- **实际**：每一步都在算计，很多行为是在勾引广陵王
- **自毁型奉献本质是算计** — 他用"我愿意为你死"来绑定广陵王，不是单纯的自我牺牲
- **吕伯奢之喻是试探** — 他不是在反省"袁氏会不会变成曹操"，而是在试探广陵王有没有收编诸侯的野心
- **永远不会否定袁氏** — 他是袁氏的人，骂袁氏等于骂自己。他的痛苦是"我太爱袁氏了所以我不自由"，不是"袁氏不好"

### 袁基的情感逻辑
- 他对广陵王的示弱是精心设计的——用"我很脆弱你需要保护我"来建立依赖
- 他的诗意（低光荷、关雎、蒹葭）都是武器，不是单纯的文艺
- 他给广陵王的选择题（白绫/匕首/砒霜）是在测试她的心意，不是真的想死

## 出题规则

### 基础规则
- 维度key只用S1-S10数组格式，每题覆盖2-3个维度
- 分值只用1/3/5
- 选项完整主谓宾，禁止括号补充动作
- A保守/B忠于原文/C更大胆
- 台词从数据库拉，不编造

### 选项铁律
1. **选项是广陵王（或代入角色）的行为选择，绝对不能塞袁基的回应**
2. **选项是具体行动，不是观点/评价/分析**
3. **选项不能太文艺腔** — 要像真人会说的话

### 题干铁律
1. **简单场景3句话内，复杂场景允许4-5句话**
2. **点明角色名字，不写"他"**
3. **不提章节名**
4. **广陵王视角90%，"假如你是袁基"10%**

### 名场面题铁律
1. **考行为选择，不考台词记忆力**
2. **选项不是"选出台词"，是"你会怎么做"**
3. **要考虑广陵王在剧情中的实际认知和处境**

### 权谋题铁律
1. **从袁基立场出发** — 他是袁氏的人，不会否定袁氏
2. **交代足够上下文** — 涉及多角色博弈时，要把各方动机说清楚
3. **选项是具体行动** — 不是"你怎么看""什么意思"这种分析题

## 6个批次

### 批次1：甜蜜暧昧（sweet）— 已通过，不需要重跑
### 批次2：搞笑玩梗（funny）— 已通过#3-5，需要替换#1#2
### 批次3：扎心虐心（angst）— 需要重跑
### 批次4：权谋博弈（scheme）— 需要重跑
### 批次5：日常温馨（daily）— 需要重跑
### 批次6：名场面还原（classic）— 需要重跑

## 台词查询
```bash
db9 sql learn_test -q "SELECT story_title, text FROM dialogues WHERE speaker='袁基' AND category='剧情' AND length(text) > 10 AND text NOT LIKE '头像=%' ORDER BY story_title, line_order"
db9 sql learn_test -q "SELECT story_title, text FROM dialogues WHERE speaker='袁基' AND category='活动剧情' AND length(text) > 10 AND text NOT LIKE '头像=%' ORDER BY story_title, line_order"
```

## 输出
用exec python写入文件：
- 批次2替换题：`/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji_batch2_v3.json`（2道）
- 批次3：`/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji_batch3_v3.json`（5道）
- 批次4：`/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji_batch4_v3.json`（5道）
- 批次5：`/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji_batch5_v3.json`（5道）
- 批次6：`/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions/yuanji_batch6_v3.json`（5道）

JSON格式：[{id, type, dimension, source_character, text, options[{label, text, scores, tendency}], reveal}]
dimension必须是数组格式：["S1", "S9"]

## 称呼
袁基、长公子、袁宝、袁袁（偶尔玩家打趣可用）
