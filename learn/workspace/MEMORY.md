# MEMORY.md - 长期记忆

## learn_bot 启动记录

- **创建日期：** 2026-03-26
- **App ID:** cli_a94ff09597b85bc4
- **用途：** 学习助手

---

## 角色扮演系统

### 角色设定文件位置
- 陈登：`~/.agents/characters/chendeng.md`
- 张邈：`~/.agents/characters/zhangmiao.md`
- 写作模板：`~/.agents/characters/roleplay_template.md`
- 陈登模板：`~/.agents/characters/chendeng_template.md`
- 张邈模板：`~/.agents/characters/zhangmiao_template.md`

### db9 存储
- 数据库：`learn_test`
- 表：`chendeng_profile`, `chendeng_stories`, `chendeng_voices`, `chendeng_conversations`
- 表：`roleplay_templates`

### 7步写作模板（强制使用）
```
【场景衔接】（承接上一动作/位置）
【完整体位流程】（重心转移、姿势变化）
【神态细节烘托】（眼神、眉头、下颌）
【动作微反应烘托】（手指、呼吸、肩膀）
【环境氛围烘托】（风、光、声音、气味）
【语气提示+角色语言】
【补充动作/衔接】
```

### 禁止事项
- ❌ 不用「左手/右手」
- ❌ 不写心理
- ❌ 不用情绪标签

### 分段规范（2026-04-02 新增）
- ✅ 每个【】段落单独成段
- ✅ 段落之间空一行
- ❌ 禁止把所有内容堆成一大段
- ❌ 禁止连续写超过 3 行不换行

---

## 米家账号（2026-04-02 同步）

📱 **智能家居相关**
- 账号：18801306852
- 密码：19940606~xiaohei
- 用途：find-my-stuff 项目、智能家居学习

---

## Agent 配置更新（2026-04-07）

### 别名配置
- **Learn Bot** → 增加别名「学习搭子」
- **fit-buddy** → 增加别名「减肥搭子」
- **main** → 增加别名「奈的虾」

### diet-buddy 合并
- diet-buddy 已与 fit-buddy 合并
- 体重记录数据已迁移至 `fit-buddy/workspace/memory/weight-log.json`
- 原 diet-buddy 目录已备份为 `diet-buddy.backup.20260407`

---

## Skill 自进化系统（2026-04-12）

### 新增
- **self-evolver skill**: `~/.agents/skills/self-evolver/SKILL.md`
- **进化日志**: `memory/evolution-log.md`
- **AGENTS.md**: 添加 🧬 Skill Evolution 章节

### 嵌入 dream-memory
- 沉淀逻辑嵌入 dream-memory 第九步（凌晨 3:00 兜底）
- 核心原则：当场沉淀 > cron 兜底

### 系统分工
| 系统 | 职责 |
|---|---|
| self-evolver | 定义沉淀标准和格式 |
| self-improving-agent | 记错误和纠正（jsonl） |
| session-janitor | 清理 session |
| dream-memory | 蒸馏记忆 + 兜底沉淀 + git 备份 |

---

---

## 鸢BTI 项目（2026-04-13~14）

### 数据库
- **数据库**: `learn_test`（PostgreSQL，通过 db9 访问）
- **主表**: `dialogues`（99544条台词，1518个故事，1473个说话人）
- **表结构**: `id, story_title, category, speaker, text, dialogue_type, emotion, line_order, created_at`
- **数据来源**: BWiki（代号鸢 Wiki，bwiki.com）所有剧情录入
- **查询命令**: `db9 sql learn_test -q "SQL查询"`
- **绝对路径**: `/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/`

### 输出文件
- **角色质心分析**: `/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/character-centroids.md`
- **完整密探列表**: `/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/README.md`

### 12维质心体系
- S1权谋(权谋城府)、S2情感(情感表达)、S3金钱(金钱务实)、S4面具(面具深度)
- S5行动(行动风格,L=谋定后动,H=冲动先动)
- S6底线(底线弹性)、S7锋芒(表达锋芒)、S8温柔(温柔底色)
- S9权力(权力态度)、S10秩序(秩序感)
- ⚠️ 10维体系（2026-04-15确认，与创业助手一致）
- 旧S8独处群处、旧S9命运观已废弃，相关题目已删除
- 评分: L(1), M(2), H(3)

### 关键纠正（孙雪反馈）
- 张邈 S9 权力: M→L（自诩清流，看不起权贵，不屑于追求权力）
- 孙策 S9 权力: H→M（天生权力，不在意权力本身，权力对他来说是自然而然的）
- 孙策 S10 秩序: L→M（有自己的规矩，不是完全无序）

### 每个密探的题量分配（孙雪指定）

| 题量 | 密探 |
|------|------|
| 20题 | 张邈、陈登、阿蝉、周瑜、张辽、董奉、周忠 |
| 15题 | 郭嘉、徐庶、祢衡、张郃 |
| 10题 | 吕布、张飞、马超、甘宁 |
| 8题 | 诸葛瑾、诸葛诞、张绣、贾诩、荀攸、士燮、蒯越、孔融 |
| 5题 | 张闿、张燕、颜良、文丑、杨修、孙权、凌统、庞德、张角、荀彧、戏学、史子眇、满宠、简雍、法正、程昱 |
| 3题 | 刘备、刘协、孙坚、吴夫人、王异、陈宫、袁术、袁绍、李傕、郭汜、马腾、小乔 |
| 2题 | 张仲景、张鲁、王粲、孙尚香、吕蒙、耿公子、华佗(有质心但只2题) |
| 1题 | 周群、钟繇、甄宓、张昭、虞翻、严白虎、夏侯惇、伍丹、太史慈、孙坚(重复?)、卢植、陆逊、刘璋、刘繇、蒯良、公孙瓒、葛洪、干吉、程普、曹植、曹丕、蔡琰、安期、袁绍(重复?)、伏寿、春梦、陈昭、曹操、王异(重复?) |

注：有些密探在列表中出现两次（不同题量），以孙雪最后确认为准。5个男主（袁基/刘辩/傅融/孙策/左慈）各30题已单独完成。

### ⚠️ 文件写入规范（所有 agent 必须遵守）
- **必须使用绝对路径**，不用相对路径
- 追加内容用 `exec` + `cat >> file << 'EOF'...EOF`
- `write` 工具会覆盖文件内容，不能用于追加
- `edit` 工具需要唯一上下文，重复内容多的文件容易失败

---

此文件会持续更新，记录重要对话和学习进度。
