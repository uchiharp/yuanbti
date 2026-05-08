# Agent 开发流水线 — 产品需求文档 (PRD)

## 核心理念

**不是让一个agent做完所有事，而是让一群专业agent各司其职、互相评审、迭代交付。**

每个环节都有"对手"来挑战产出质量。从PRD到代码，从设计到测试，每一步交付都经过专业评审官的严格审查。规则必须有脚本强制执行，没有脚本保障的规则 = 建议而非约束。

---

## 项目规模裁剪

不同规模项目走不同流程长度，避免"杀鸡用牛刀"。

### 规模判定标准（阶段0由协调者判定）

| 规模 | 判定条件 | 示例 |
|------|---------|------|
| 🔴 大型 | 功能≥10、涉及≥3个子系统、预估工期≥2周 | 电商系统、社交App |
| 🟡 中型 | 功能5-9、1-2个子系统、工期1-2周 | 后台管理、小程序 |
| 🟢 小型 | 功能≤4、单子系统、工期<1周 | 工具页、H5活动页 |

**"功能"定义：** 独立用户可交互的功能模块，每个有明确的用户故事和验收标准。如"用户登录"、"商品搜索"、"订单支付"各算1个功能。
**"子系统"定义：** 独立部署的服务或数据存储，如API服务、前端应用、数据库、消息队列。前端+后端=2个子系统，+数据库=3个。

### 规模差异表

**脚本感知：** `pipeline-check.sh` 接受第三个可选参数 `SIZE`（`small`/`medium`/`large`，默认 `medium`）。🟢小型跳过的阶段，脚本直接跳过检查（exit 0）。规模值存储在 `_config.json` 的 `size` 字段中，脚本优先从配置读取。

### 规模重判定

任何阶段可触发规模重评：协调者重新判定 → 如果升级（🟢→🟡），暂停当前阶段→按顺序补做跳过的阶段（使用对应规模的完整评审）→补做完成后回到暂停点继续→对齐方式：补做阶段如果发现需要修订上游产出，按回退流程处理（消耗回退额度）；补做阶段如果无需修订（下游与补做产出一致），评审官签收即可，不影响下游。"一致"的判定标准：补做阶段评审官检查下游产出是否覆盖了补做阶段新增的检查点/约束，若未覆盖则判定为"不一致"。如果降级（🟡→🟢），跳过的阶段不再补做。重判定计入变更记录（`changes/` 下记录）。

| 阶段 | 🔴 大型 | 🟡 中型 | 🟢 小型 |
|------|---------|---------|---------|
| 0. 启动 | 完整规划 | 完整规划 | 简化规划 |
| 1. PM→PRD | ✅ | ✅ | ✅ |
| 1.5. PRD交叉评审 | ✅ 全角色并发 | ✅ 架构+QA | ⏭️ 跳过 |
| 2. 架构设计 | ✅ | ✅ | ✅ |
| 2.5. 架构交叉评审 | ✅ | ✅ | ⏭️ 跳过 |
| 2.8. 技术Spike | ✅ 按需 | ✅ 按需 | ⏭️ 跳过 |
| 3. UX设计 | ✅ | ✅ | ⏭️ 跳过 |
| 3.5. UX→UI交接 | ✅ | ⏭️ 跳过 | ⏭️ 跳过 |
| 4. UI设计 | ✅ | ✅ | 🟢 PM兼任 |
| 4.5. UI→UX反向 | ✅ | ⏭️ 跳过 | ⏭️ 跳过 |
| 5. 任务分解 | ✅ | ✅ | ✅（简化版）|
| 5.5. 分解确认 | ✅ | ✅ | 🟢 开发可行性快检（5-10min）|
| 6. 开发执行 | 3Agent并发 | 2Agent并发 | 1Agent |
| 6.3. 代码集成 | ✅ | ✅ | 🟢 轻量冒烟（开发自验）|
| 6.5. 开发审查 | 3reviewer并发 | 2reviewer并发 | 1reviewer |
| 7. 代码审查 | QA评审官+架构评审官 | QA评审官+架构评审官 | 🟢 QA评审官（兼任架构合规检查）|
| 8. 测试验证 | L1+L2+L3 | L1+L2 | L1 |
| 9. 验收 | 完整报告 | 完整报告 | 简化报告 |

---

## Brainstorm 融合原则

**适用阶段表中列出的阶段，应先用 Brainstorm 的对话式讨论方式与用户确认，最后再整理成文档。**

### 适用阶段

| 阶段 | Brainstorm 讨论什么 | 产出文档 |
|------|-------------------|---------|
| 阶段1（PRD设计） | 用户是谁、解决什么痛点、功能边界、验收标准、和竞品的差异化 | PRD.md |
| 阶段2（架构设计） | 技术选型、架构风格、数据模型、API设计、非功能需求 | ARCHITECTURE.md |
| 阶段5（任务分解） | 任务拆分方式、优先级排序、依赖关系、每任务的验收标准 | TASK-LIST.md + test-plan.md |

**阶段5 Brainstorm 执行者：** 由创业助手（startup-helper）主导与用户的讨论，QA并行参与测试策略讨论。创业助手具备项目管理和任务拆解能力，PM不需要重复参与此阶段。

### Brainstorm 讨论规则

1. **了解现状** — 先读项目文件、CONTEXT.md、历史教训
2. **逐个提问** — 每次只问一个问题，优先给选择题
3. **提出方案** — 给出 2-3 个方向，标注利弊和推荐
4. **分段确认** — 按模块一段一段讲，每段等用户确认再继续
5. **整理文档** — 讨论完毕后整理成正式文档提交 git

**Brainstorm 不替代评审** — 讨论确保文档内容正确，评审确保文档质量达标。两者先后关系，互补不重叠。

**Brainstorm 与自主执行的关系：** 标记 `brainstorm: true` 的阶段是自主执行的例外——协调者必须先与用户进行 Brainstorm 讨论，讨论完毕后执行者再自主产出文档。Brainstorm 阶段的执行流程：协调者与用户讨论 → 整理讨论要点 → 调度执行者产出文档 → 评审官审查。

**Brainstorm 可验证性：** `brainstorm: true` 的阶段必须产出 `brainstorm-log.md`（与产出物同目录），记录每个提问和用户回答摘要。`pipeline-check.sh` 对 `brainstorm: true` 阶段检查 `brainstorm-log.md` 存在且包含≥3个问答对（`## Q1` / `## A1` 格式）。

---

## 完整流程图

```
用户需求
  │
  ▼
┌──────────────────────────────────────────────┐
│ 阶段0：启动（协调者）                          │
│ · 接收用户需求                                │
│ · 评估项目范围、复杂度、规模（🔴/🟡/🟢）       │
│ · 确定需要哪些角色参与                          │
│ · 初始化健康度看板 + CONTEXT.md                 │
│ · 加载历史教训（MemPalace）                    │
│ · 产出项目计划 → 自动开始阶段1                  │
│ · 计划同步展示给用户（用户可随时打断）            │
└──────────────────┬───────────────────────────┘
                   │ 自动进入
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段1：需求分析（PM）                          │
│ · 梳理用户需求 → 产出 PRD                      │
│ · PRD → PM·评审官审查（最多2轮迭代）→ 签收      │
│ · 更新 CONTEXT.md 阶段1段落                    │
└──────────────────┬───────────────────────────┘
                   │ 评审官签收
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段1.5：PRD交叉评审（全体角色）[24h时限]       │
│ · 架构师、QA、开发、UI、UX 并发评审PRD          │
│ · 各角色独立输出评审意见                        │
│ · 汇总意见 → PM修订 → PM·评审官复核            │
└──────────────────┬───────────────────────────┘
                   │ PRD最终签收
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段2：架构设计（架构师）                      │
│ · 基于 PRD → 产出技术架构方案                  │
│ · 标注高风险技术点 → 触发Spike（阶段2.8）       │
│ · 架构 → 架构师·评审官审查（最多2轮）→ 签收     │
│ · 更新 CONTEXT.md 阶段2段落                    │
└──────────────────┬───────────────────────────┘
                   │ 评审官签收
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段2.5：架构交叉评审（开发+QA）[24h时限]       │
│ · 开发+QA独立输出评审意见                      │
│ · 汇总 → 架构师修订 → 评审官复核               │
│                                                │
│ 阶段2.8：技术Spike（按需）≤4h【与2.5并发】     │
│ · 独立Agent验证技术可行性                      │
│ · ✅成功→继续 🟡部分成功→协调者决定 ❌失败→回退  │
│                                                │
│ 【2.5+2.8均完成后才进入阶段3】                  │
└──────────────────┬───────────────────────────┘
                   │ 架构签收 + Spike通过
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段3：UX设计 → 阶段3.5 UX→UI交接评审          │
│ 阶段4：UI设计 → 阶段4.5 UI→UX反向确认          │
│ · 各自经评审官审查（最多2轮）→ 签收             │
│ · 更新 CONTEXT.md 阶段3/4段落                  │
└──────────────────┬───────────────────────────┘
                   │ UI最终签收
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段5：任务分解（创业助手 + QA并行）            │
│ · 创业助手 → 开发任务清单                       │
│ · QA → 测试计划（test-plan.md）                │
│ · 各自经评审官审查 → 签收                       │
│ · 更新 CONTEXT.md 阶段5段落                    │
│                                                │
│ 阶段5.5：分解确认（开发并发确认）               │
└──────────────────┬───────────────────────────┘
                   │ 分解最终签收
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段6：开发执行（开发并发 + QA同步写测试）       │
│ · 按依赖关系分批调度，无依赖任务并发             │
│ · QA同步写L2集成+L3 E2E测试骨架                 │
│ · 更新 CONTEXT.md 阶段6段落                    │
│                                                │
│ 阶段6.3：代码集成 + 冒烟验证                    │
│ 阶段6.5：开发审查（各reviewer并行）             │
└──────────────────┬───────────────────────────┘
                   │ 开发审查完成
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段7：代码审查（QA评审官 + 架构评审官并发）     │
│ · review-check.sh 检查评审质量                  │
│ · 最多3轮迭代                                  │
└──────────────────┬───────────────────────────┘
                   │ 签收
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段8：测试验证（QA）— L1→L2→L3              │
│ · test-report-check.sh 检查报告格式             │
│ · 最多3轮迭代                                  │
│ · 更新 CONTEXT.md 阶段8段落                    │
└──────────────────┬───────────────────────────┘
                   │ 测试通过
                   ▼
┌──────────────────────────────────────────────┐
│ 阶段9：交付验收（协调者）                       │
│ · acceptance-check.sh 自动验证7项验收标准       │
│ · 端到端用户旅程走查                           │
│ · 沉淀经验教训到 MemPalace                     │
│ · 更新 CONTEXT.md 阶段9段落                    │
└──────────────────────────────────────────────┘
```

---

## 阶段依赖与并发关系

```
时间线 →

阶段0 启动
  │
  └─────→ 阶段1 PM写PRD
            │
            ├──→ [PM评审官审查] → 签收
            │
            └──→ 阶段1.5 PRD交叉评审（并发，24h时限）
                   ├─ 架构师评审
                   ├─ QA评审
                   ├─ 开发评审
                   └─ UI/UX评审
                   → [PM修订] → [PM评审官复核] → 签收
                   │
                   └──→ 阶段2 架构师设计
                          │
                          ├──→ [架构师评审官审查] → 签收
                          │
                          ├──→ 阶段2.5 架构交叉评审（并发，24h时限）
                          │      ├─ 开发评审
                          │      └─ QA评审
                          │      → [架构师修订] → [架构师评审官复核]
                          │
                          ├──→ 阶段2.8 技术Spike（按需，≤4h）
                          │
                          ├──→ 阶段3 UX设计
                          │      [UX评审官审查] → 签收
                          │      → 阶段3.5 UI交接评审 → [UX修订+复核]
                          │
                          └──→ 阶段4 UI设计
                                 [UI评审官审查] → 签收
                                 → 阶段4.5 UX反向确认 → [UI修订+复核]
                                 │
                                 ▼
                      阶段5 创业助手分解任务 + QA拆测试计划（并行）
                                 │
                       [创业助手评审官审查] → 签收
                                 │
                      阶段5.5 分解确认（开发并发）
                                 │
                       [开发确认结果自动进入阶段6]
                                 │
                                 ▼
                      阶段6 开发并发 + QA同步写测试脚本
                                 │
                      阶段6.3 代码集成
                                 │
                      阶段6.5 开发审查（并发）
                                 │
                      阶段7 评审审查（并发）
                                 │
                      阶段8 QA测试（L1→L2→L3）
                                 │
                                 ▼
                      阶段9 验收汇总
```

**关键并发点：**
- 阶段3（UX）和阶段2（架构）的后半段可以并发
- 阶段4（UI）依赖阶段3（UX）签收
- 阶段6 的多个开发Agent可以并发
- 阶段6.5 的多个reviewer可以并发审查
- 阶段7 的多个评审官可以并发审查

---

## 各阶段角色与评审官对照表

| 阶段 | 执行者 | 评审官 | 思维模式 | 最大迭代 |
|------|--------|--------|---------|---------|
| 0. 启动 | 协调者 | — | — | 0（自动启动）|
| 1. 需求分析 | PM | PM·评审官 | 魔鬼代言人 | 2 |
| 1.5. PRD交叉评审 | 架构师/QA/开发/UI/UX | — | 各自专业视角 | 1（仅评审）|
| 2. 架构设计 | 架构师 | 架构师·评审官 | 架构审计师 | 2 |
| 2.5. 架构交叉评审 | 开发/QA | — | 各自专业视角 | 1（仅评审）|
| 2.8. 技术Spike | 架构师/开发 | — | — | 1（≤4h）|
| 3. UX设计 | UX测试 | UX·评审官 | 人类学家 | 2 |
| 3.5. UX→UI交接评审 | UI设计师 | — | 视觉可行性视角 | 1（仅评审）|
| 4. UI设计 | UI设计师 | UI·评审官 | 美学刺客 | 2 |
| 4.5. UI→UX反向确认 | UX测试 | — | 交互完整性视角 | 1（仅确认）|
| 5. 任务分解 | 创业助手+QA | 创业助手·评审官+QA·评审官 | 冷血投资人+测试艺术家 | 2 |
| 5.5. 分解确认 | 开发×3 | — | 实现者视角 | 1（仅确认）|
| 6. 开发执行 | 开发小一/二/三 | — | — | — |
| 6.3. 代码集成 | dev3 | — | — | — |
| 6.5. 开发审查 | 小一/二/三reviewer | — | 全面审查视角 | 1（仅评审）|
| 7. 代码审查 | QA评审官+架构评审官 | 协调者 | QA视角+架构视角 | 3 |
| 8. 测试验证 | QA | QA·评审官 | 测试艺术家 | 3 |
| 9. 验收汇总 | 协调者 | — | — | — |

---

## 角色配置表（Agent ID）

| 角色 | Agent ID | 备注 |
|------|----------|------|
| 协调者 | main | 全流程调度 |
| PM | pm | 需求分析 |
| PM评审官 | pm-reviewer | PM对手 |
| 架构师 | architect | 技术方案（🟢小型由PM兼任，以 `pm` session 执行，加载 `tech-architecture` skill）|
| 架构师评审官 | architect-reviewer | 架构对手 |
| UX测试 | ux-tester | 交互设计（🔴专用）|
| UX评审官 | ux-tester-reviewer | UX对手 |
| UI设计师 | ui-designer | 视觉设计（🟢小型由PM兼任，以 `pm` session 执行）|
| UI评审官 | ui-designer-reviewer | UI对手 |
| 创业助手 | startup-helper | 任务分解 + 冒烟验证（阶段6.3后）。名称沿袭系统角色体系，实际职能为项目任务拆解与可行性验证 |
| 创业助手评审官 | startup-helper-reviewer | 创业助手对手 |
| 开发小一 | backend | 全栈（主力） |
| 开发小二 | frontend | 全栈（副手） |
| 开发小三 | dev3 | 全栈（三号位） |
| 小一reviewer | backend-reviewer | 代码审查 |
| 小二reviewer | frontend-reviewer | 代码审查 |
| 小三reviewer | dev3-reviewer | 代码审查 |
| QA | qa | 测试规划（阶段5）+ 测试编写（阶段6）+ 测试验证（阶段7/8）|
| QA评审官 | qa-reviewer | 代码审查 |

**🟢小型项目角色子集：** 协调者、PM（兼任architect+ui-designer）、PM评审官（兼任architect-reviewer）、开发小一（backend）、小一reviewer（backend-reviewer）、QA、QA评审官。其余角色不激活、不调度。

**🟢小型双重角色补偿控制：** PM兼任architect和ui-designer时，PM评审官也兼任对应评审官——这打破了"对手"原则。补偿措施：(1) 协调者对PM兼任的阶段（2/4）强制执行抽查（5.5规则），不可跳过；(2) 阶段2 PM兼任architect时加载 `tech-architecture` skill，阶段4 PM兼任ui-designer时不加载额外skill（以PM通用能力执行）。

**协调者通信规则：**
1. 优先 `sessions_send` — 向已存在的固化 agent session 发消息
2. 备选 `sessions_spawn` — 创建新的子 agent 执行任务
3. 优先使用固化 agent — 通过 `sessions_send` 发给 agent ID（如 `pm`、`architect`、`qa`）
4. **失败处理：** `sessions_send` 失败 → 重试1次（间隔10s）→ 仍失败则 `sessions_spawn` 创建新session → spawn也失败 → escalated 用户"agent不可用"，协调者暂停该项目调度

**执行纪律：** 协调者派任务时必须附加对应角色的纪律条款（详见 `agent-discipline` skill）。

**协调者调度逻辑保障：** 协调者是整个系统最复杂的部分（状态机驱动+并发调度+异常恢复），其核心调度逻辑不能完全依赖 LLM 推理。实现方式：(1) 将核心调度逻辑抽取为 `scripts/orchestrator.sh`，协调者 agent 调用该脚本的子命令（`next-phase`、`rollback`、`handle-timeout`、`check-deadlock`）驱动流程；(2) 脚本读取 `pipeline-config.yaml` + `_config.json` + `_index.json`，输出下一步操作指令（JSON格式）；(3) 协调者执行脚本输出的指令，不自行决策阶段跳转、回退触发、超时处理；(4) 协调者的判断力只用于：规模判定、Brainstorm讨论、根因分析等脚本无法处理的部分。

---

## 各阶段详细说明

### 阶段0：启动（协调者）

**产出：** `.contracts/{project}/phase-0-startup/PROJECT-PLAN.md` + `.contracts/{project}/CONTEXT.md`

**执行内容：**
- 理解用户需求，自主判定项目规模和参与角色
- 初始化健康度看板（`health-dashboard.md`）
- 创建 `CONTEXT.md` 骨架，写入项目基本信息
- 加载 MemPalace 历史教训（`wing=agent-pipeline room=project-lessons`），追加到 PROJECT-PLAN.md
- 将历史教训摘要写入 CONTEXT.md 阶段0段落
- 产出项目计划并展示给用户，**不等确认，自动进入阶段1**

---

### 阶段1：需求分析（PM）

**产出：** `.contracts/{project}/phase-1-prd/PRD.md`
**加载 skill：** `requirements-analysis`（如可用）
**知识库：** 交付时更新 CONTEXT.md 阶段1段落 + 存入 MemPalace `prd-decisions`

**简要说明：** PM 梳理用户需求，产出包含背景、用户故事、功能清单（must-have/nice-to-have）、优先级排序、验收标准的 PRD。经 PM·评审官审查（魔鬼代言人，最多2轮迭代）后签收。

---

### 阶段1.5：PRD交叉评审（全体角色并发）

**产出：** `.contracts/{project}/phase-1.5-prd-cross-review/cross-review-pm.md`

**简要说明：** 架构师、QA、开发、UI、UX 并发评审 PRD，各角色从专业角度独立输出评审意见。汇总意见 → PM修订 → PM·评审官快速复核（1轮 = 修订+复核算1个完整轮次）。24h时限，最终签收。

---

### 阶段2：架构设计（架构师）

**产出：** `.contracts/{project}/phase-2-architecture/ARCHITECTURE.md`
**加载 skill：** `tech-architecture`（如可用）
**知识库：** 交付时更新 CONTEXT.md 阶段2段落 + 存入 MemPalace `arch-decisions`

**简要说明：** 架构师基于 PRD 产出技术架构方案（技术选型、系统架构、数据模型、API设计、安全措施），标注高风险技术点触发 Spike。经架构师·评审官审查（最多2轮迭代）后签收。

---

### 阶段2.5：架构交叉评审（开发+QA）

**产出：** `.contracts/{project}/phase-2.5-arch-cross-review/cross-review-arch.md`

**简要说明：** 开发+QA独立输出评审意见。汇总 → 架构师修订 → 架构师·评审官快速复核（1轮）。24h时限。

---

### 阶段2.8：技术Spike（按需触发）

**产出：** `.contracts/{project}/phase-2.8-spike/SPIKE-REPORT.md`
**加载 skill：** `tech-spike`（如可用）
**知识库：** 交付时更新 CONTEXT.md 阶段2.8段落 + 存入 MemPalace `spike-reports`

**简要说明：** 独立Agent花≤4h验证技术可行性，产出结论（可行/不可行/需调整）+ 代码原型。成功则继续，失败则回退阶段2。🟡部分成功时：(a) 调整方案→修订ARCHITECTURE.md→架构师评审官1轮复核→继续；(b) 简化需求→回退阶段1更新PRD→按回退流程走。**同一技术点Spike最多2次，第2次仍失败则必须换方案或降级需求，Spike循环回退计入回退额度。每个项目最多触发3个不同技术点的Spike，总Spike时间≤12h。Spike触发的回退到阶段2，其直接下游（2.5）也必须重做。Spike触发的回退无论影响多少子阶段，仅消耗1次回退额度。**

---

### 阶段3：UX设计（UX测试）

**产出：** `.contracts/{project}/phase-3-ux/UX-DESIGN.md`
**知识库：** 交付时更新 CONTEXT.md 阶段3段落（MemPalace不存，完整文档在文件里）

**简要说明：** 基于 PRD+架构产出 UX 方案（用户流程图、信息架构、交互规范、核心场景走查）。经 UX·评审官审查（最多2轮迭代）后签收。

### 阶段3.5：UX→UI设计交接评审

**产出：** `.contracts/{project}/phase-3.5-ux-to-ui/cross-review-ux-to-ui.md`

### 阶段4：UI设计（UI设计师）

**产出：** `.contracts/{project}/phase-4-ui/UI-DESIGN.md`
**知识库：** 交付时更新 CONTEXT.md 阶段4段落

### 阶段4.5：UI→UX反向确认

**产出：** `.contracts/{project}/phase-4.5-ui-to-ux/cross-review-ui-to-ux.md`

---

### 阶段5：任务分解（创业助手 + QA并行）

**产出：** `.contracts/{project}/phase-5-decomposition/TASK-LIST.md` + `phase-5-decomposition/test-plan.md`
**加载 skill：** `task-decomposition`（如可用）
**知识库：** 交付时更新 CONTEXT.md 阶段5段落 + 存入 MemPalace `task-breakdown`

### 阶段5.5：分解确认（开发Agent）

**产出：** `.contracts/{project}/phase-5.5-decomposition-confirm/confirm-tasks.md`

**简要说明：** 开发并发确认任务可行性。如果开发拒绝某任务，反馈回创业助手修订（计入阶段5的1轮迭代，非回退）。修订仍被拒绝则升级到用户决策。

---

### 阶段6：开发执行（开发Agent并发 + QA同步写测试）

**产出：**
- 代码文件：`.contracts/{project}/phase-6-dev/`
- 测试脚本：`.contracts/{project}/phase-6-dev/tests/`（L2集成 + L3 E2E测试骨架，L1由开发写）
**合同类型：** 🔴高风险完整合同
**知识库：** 各开发交付时更新 CONTEXT.md 阶段6段落 + 存入 MemPalace `dev-notes`

**QA测试脚本要求：**
- QA在阶段6编写L2集成测试骨架（mock接口）+ L3 E2E测试骨架（关键用户旅程），L1单元测试由开发编写
- QA启动时机：开发提交第一批可编译代码后QA开始同步工作。QA可先基于ARCHITECTURE.md+test-plan.md写测试骨架（mock接口），开发提交代码后逐步替换为真实调用
- L2/L3测试比例遵循测试金字塔：L2约2倍于L3数量

**环境就绪检查（阶段6.3前必须满足）：**
- `package.json`/`pom.xml`/`requirements.txt` 存在
- 依赖可安装（`npm install` / `mvn resolve` 不报错）
- `.env.example` 存在（实际 `.env` 不纳入版本控制）
- 数据库 migration 脚本存在且可执行
- 若检查失败 → 开发修复，不计入回退额度

**数据库迁移管理：** 阶段6 DoD 增加"migration脚本存在且可执行"。每个migration必须包含对应的rollback脚本。补偿事务中，开发负责提供migration rollback脚本。

### 阶段6.3：代码集成 + 冒烟验证

**产出：** `.contracts/{project}/phase-6.3-integration/integration-report.md`
**执行者：** dev3（集成）+ 创业助手（冒烟验证）

**冒烟验证（硬性要求）：** 逐项执行，每项输出：验证项名称、执行步骤、预期结果、实际结果、✅/❌。冒烟不通过禁止进入6.5。冒烟失败→开发修复→重做6.3冒烟→通过后进6.5。冒烟连续失败3次→触发回退。**回退目标判定：** 协调者分析失败模式——编译/依赖/基础设施问题→回退阶段2；功能缺失或实现错误→回退阶段5。分析记录在回退记录中。冒烟修复总时限≤2h（从首次冒烟开始计时），超时仍不通过则 escalated 用户决策，不继续重试。

### 阶段6.5：开发审查（各reviewer并行）

**产出：** `.contracts/{project}/phase-6.5-dev-review/cross-review-dev.md`
**加载 skill：** `code-review-checklist`（如可用）
**脚本检查：** `review-check.sh` 验证评审质量
**审查后修复验证：** 6.5 reviewer发现问题 → 开发修复 → 同一reviewer快速验证修复（不计入新轮次，≤30min）→ 验证通过进阶段7，验证不通过则打回开发重修。**修复验证循环上限3次**，3次仍不通过则升级到协调者决策：换开发者 / 降级为已知缺陷 / 升级到用户。

---

### 阶段7：代码审查（QA评审官 + 架构评审官）

**产出：** `.contracts/{project}/phase-7-review/review-report.md` + `phase-7-review/screenshots/`
**加载 skill：** `code-review-checklist` + `qa-workflow` + `humanize-code`
**脚本检查：** `review-check.sh` 验证评审质量
**最多3轮迭代**

---

### 阶段8：测试验证（QA）

**产出：** `.contracts/{project}/phase-8-test/test-report.md` + `phase-8-test/qa-reports/*.png`
**加载 skill：** `qa-workflow`（如可用）
**脚本检查：** `test-report-check.sh` 验证报告格式
**知识库：** 交付时更新 CONTEXT.md 阶段8段落 + 存入 MemPalace `test-results`

**QA测试报告硬性格式（每项必须）：**
```
=== [功能模块] ===
✅/🔴 [测试项名称]
- 前置条件：[环境/数据准备]
- 执行步骤：[具体操作]
- 预期结果：[应该发生什么]
- 实际结果：[实际发生了什么]

---
通过率: X/Y
问题清单:
- 🔴 P0: [描述] [截图名]
- 🟡 P1: [描述]
- 🔵 P2: [描述]
```
**报告<50行或截图<3张或无逐项结果 → 自动打回。**

---

### 阶段9：交付验收（协调者）

**产出：** `.contracts/{project}/phase-9-acceptance/ACCEPTANCE-REPORT.md`
**脚本检查：** `acceptance-check.sh` 自动验证7项验收标准
**知识库：** 更新 CONTEXT.md 阶段9段落 + 存入 MemPalace `project-lessons`

**项目交付验收标准（必须全部满足）：**
- [ ] 所有阶段审查通过（无escalated合同）
- [ ] 安全扫描 0 严重问题
- [ ] P0/P1 功能测试维度覆盖率 100%（对比test-plan）
- [ ] 测试报告中无未解决的 P0 遗留问题
- [ ] 端到端核心用户旅程全部走通
- [ ] 性能基准达标（API<200ms / 首屏<2s / 100并发）
- [ ] 展示最终成果给用户

**知识库清理：** Git提交所有产出 → 归档到 `_archive/` → MemPalace 保留 project-lessons（永久）

---

## 通用交付规则（所有阶段必须遵守）

每个执行者提交阶段产出物时，必须向用户交付以下信息：

```markdown
📋 阶段交付 | 阶段{N} | {角色名}
━━━━━━━━━━━━━━━━━━━

👥 沟通对象：
  - {角色A}：{沟通了什么，精简描述}
  - 评审官 {评审官名}：{审查结果，评分}

📁 产出文件：
  - {文件名} → {完整绝对路径}

📚 知识库：
  - CONTEXT.md：✅已更新 / ❌未更新
  - MemPalace：✅已存入 / ⏭️跳过

📊 本阶段结果：
  - 状态：签收/打回
  - 评分：{X}/10
  - 问题数：🔴{N} | 🟡{N} | 🟢{N}

下一步：{动作}
━━━━━━━━━━━━━━━━━━━
```

**禁止：** 不写沟通对象就提交 / 只写"已沟通" / 文件路径写错 / 跳过知识库更新不说明原因

**脚本强制覆盖说明：** 核心原则"没有脚本保障的规则=建议"中，以下规则因需要判断力或依赖外部系统，暂无脚本强制，标记为"软规则"：(1) Brainstorm讨论质量（需人类判断，但brainstorm-log.md存在性可验证）；(2) Self-Reflection段落内容质量（第2轮起review-check.sh验证段落存在且≥50字，但不验证内容质量）；(3) 补偿事务执行结果（compensation状态可验证）；(4) 断路器同因判定（root_cause_category可验证）；(5) 通信重试逻辑（协调者自律）。脚本可验证"是否执行了该步骤"但不验证"执行质量"。

**产出物安全消毒：** `pipeline-check.sh` 增加 `check_sanitize()`：扫描 Markdown 产出物中的 `javascript:` 协议链接、`<script>` 标签、外部图片链接（非白名单域名）。产出物路径字段验证：必须是 `.contracts/` 下的相对路径，禁止包含 `..` 或绝对路径。

**元数据完整性校验：** 关键状态变更（`in-progress→signed`、回退计数增加）时，`contract-check.sh` 交叉验证：变更是否有对应的评审签收记录或回退记录。`_index.json` 和 `_config.json` 增加顶层 `checksum` 字段（SHA256），脚本启动时校验，不匹配则 warning。

---

## Skill 引用容错规则

| Skill | 不存在时的回退 |
|-------|--------------|
| requirements-analysis | 按阶段1简要说明直接执行（产出PRD.md） |
| tech-architecture | 按阶段2简要说明直接执行（产出ARCHITECTURE.md） |
| tech-spike | 按阶段2.8简要说明直接执行（4h验证，产出SPIKE-REPORT.md） |
| task-decomposition | 按阶段5简要说明直接执行（产出TASK-LIST.md + test-plan.md） |
| qa-workflow | 按阶段8简化流程执行（编译→API冒烟→E2E）|
| code-review-checklist | 使用流水线内置审查维度表（代码质量+安全+健壮性+去AI味）|
| code-quality-guard | 仅做基础编译验证（`mvn compile` / `tsc --noEmit`）|
| run-tests | 手动执行 `mvn test` + `npx playwright test` |
| humanize-code | 跳过去AI味检查，仅做代码质量和安全审查 |
| iterative-contract | 使用简化合同格式（3行） |
| agent-discipline | 使用 default.md 通用条款 |

**原则：skill 是锦上添花，不是硬依赖。流水线在任何 skill 缺失的情况下都必须能继续执行。**

---

## 机制一：回退规则

流水线不是单向前进的。任何阶段发现上游问题，必须立即回退。

### 回退触发条件

| 发现问题的阶段 | 回退目标 | 典型场景 |
|---------------|---------|----------|
| 阶段2.8 Spike | 阶段2 架构 | Spike失败，需调整架构方案 |
| 阶段2.8 Spike | 阶段1 PRD | Spike部分成功，需简化需求 |
| 阶段6 开发 | 阶段2 架构 | 架构设计导致无法实现某个PRD功能 |
| 阶段6 开发 | 阶段1 PRD | 发现PRD遗漏了关键业务逻辑 |
| 阶段7 审查 | 阶段4 UI | 实际UI和设计稿差异大 |
| 阶段8 测试 | 阶段5 分解 | 测试发现任务清单遗漏了边界场景 |
| 阶段8 测试 | 阶段2 架构 | 性能测试发现架构瓶颈 |
| 阶段9 验收 | 任意 | 端到端走查发现任何阶段的问题（回退到阶段1/2需用户确认，附token/时间成本估算） |

### 回退流程

```
发现问题 → 严重度评估 → 🔴阻断（立即回退）/ 🟡重要（本批次后回退）/ 🟢建议（记录备查）
回退到对应阶段 → 附带问题描述 + 影响范围标注 → 上游修正 → 评审官复核（1轮）→ 从回退阶段重新走流程
→ 更新 CONTEXT.md 受影响段落 + MemPalace 存入新版本
```

### 回退影响范围

回退触发者必须标注影响范围：
- **影响直接下游** → 目标阶段+直接下游重做，其余保留（最小粒度，任何上游变更至少影响直接下游）。“直接下游”= 阶段依赖图中直接依赖目标阶段产出的所有阶段（如阶段1的直接下游=1.5和2，阶段2的直接下游=2.5/2.8/3/4）
- **影响下游** → 目标阶段+下游受影响阶段重做，其余保留
- **全量重走** → 从目标阶段开始全部重走

评审官在1轮复核时确认影响范围是否合理。受影响阶段合同状态转为 `reopened`，不受影响阶段 `signed` 状态保留。

### 回退后中间产物处理

回退目标之后的所有阶段产出物标记为 `stale`（在 `_index.json` 中更新状态），不清除旧文件。**两阶段清理：** (1) 回退触发时：标记 `stale`，文件保留供参考；(2) 阶段重执行时：执行者开工前，协调者将 `stale` 文件移到 `_rollback-backup/phase-N-timestamp/`，创建空目录。agent 开工前必须检查文件状态，`stale` 文件不可作为输入依据。

### 回退次数限制

| 回退类型 | 最大额度 | 超限处理 |
|---------|---------|---------|
| 阶段间回退 | 总额度≤5次 | 第5次回退允许执行完成后 warning 触发复盘；第6次回退请求 exit 1 阻断 |
| 同阶段连续回退 | ≤2次 | 第3次升级到协调者+用户决策 |

**回退额度耗尽后的复盘：**
- 复盘产出：回退原因分析、是否系统性问题、建议方案
- 用户选项：终止项目 / 重置额度继续（附带改进措施）/ 降级规模（🔴→🟡或🟡→🟢）继续

每次回退在 `.contracts/{project}/changes/` 下以 `rollback-` 前缀记录。`contract-check.sh` 自动统计回退次数，超限 exit 1。

---

## 机制二：端到端用户旅程验证

阶段9验收必须包含完整用户旅程走查。各模块各自通过测试 ≠ 系统整体OK。

**走查维度：**
1. 模块衔接 — 页面跳转正常？状态未丢失？
2. 数据一致性 — 前端展示和后端一致？
3. 权限边界 — 不同角色权限隔离生效？
4. 错误处理链路 — 任一环节出错有有意义提示？
5. 业务闭环 — 核心流程从头走到底是否通？
6. 对比PRD — P0/P1功能实现状态无遗漏
7. 对比测试报告 — 标记的问题是否真修复

**结果判定：** 全部走通✅ / 🔴问题修复后重查 / 🟡记录已知问题可交付

---

## 机制三：需求变更管理

| 变更类型 | 影响 | 处理方式 |
|---------|------|---------|
| 🟢 小调整 | 不影响已有设计/代码 | 当前阶段内部消化 |
| 🟡 功能调整 | 影响部分设计 | 快速变更：PM更新PRD → 受影响角色修改 → 评审官复核（1轮）→ 继续 |
| 🔴 需求变更 | 改变PRD核心 | 回退变更：协调者+用户讨论 → 回退阶段1重走流程 |

**额度规则：** 🟡功能调整不计入阶段间回退额度（5次），但单独计入功能调整额度（≤3次）。🟢小调整不计入任何额度。🔴需求变更计入阶段间回退额度。`changes/` 下用前缀区分：`rollback-`（回退）、`change-`（功能调整）、`minor-`（小调整）。

每次变更在 `.contracts/{project}/changes/` 下记录。变更后必须更新 CONTEXT.md 受影响段落 + MemPalace 存入新版本。

---

## 机制四：Agent 间沟通汇报

**所有 agent 之间的每一次沟通都必须记录并汇报给用户。**

存储在 `.contracts/{project}/communications/` 下，每条记录包含：时间、发送方、接收方、类型（签收/打回/评审/回退）、合同编号、阶段、沟通内容、期望响应。

**汇报规则：** 用户看到的是原始沟通记录，不是协调者的总结。协调者不可信，只信任原文。每个节点完成后，协调者必须发送总结 + 沟通记录原文。

**脚本检查：** `pipeline-check.sh` 检查 communications/ 目录，验证每条记录包含发送方/接收方/类型字段。

---

## 机制五：防偷懒强制约束

**LLM 会偷懒。必须用强制机制确保每步真实执行。**

### 5.1 文件检查点

协调者进入下一阶段前必须执行 `pipeline-check.sh`。不执行 = 严重违规。

**脚本覆盖：**
- 各阶段产出文件存在 + 行数达标（含补全的3/4/5.5/6.5/7阶段）
- 沟通记录内容完整性（发送方/接收方/类型）
- 健康度看板更新检查（最后修改时间在时间窗口内）

### 5.2 签收必须附带内容（禁止空签收）

签收报告必须包含：至少3个具体检查过的点、至少1个🟢建议、各维度评分。

**脚本检查：** `review-check.sh` 验证评审报告包含≥3检查点 + ≥1建议 + 评分

### 5.3 交叉评审独立输出

每个角色必须单独输出评审意见，至少3个检查点。全部通过也要写具体检查过的点。

**脚本检查：** `review-check.sh` 验证 cross-review-*.md 中每个角色有独立段落且包含≥3检查点

### 5.4 并发执行的真实性

协调者优先 `sessions_send` 同时发出，或 `sessions_spawn` 在同一调用中启动。绝对禁止顺序等待再发下一条。

**脚本间接验证：** 并发角色的产出文件（mtime）应在同一时间窗口内（2分钟）。`communications/` 中并发角色评审意见发出时间差应<30秒。此为协调者自律规则，脚本仅做间接验证，不作为阻断条件。

### 5.5 协调者随机抽查

当一个阶段"全部通过"时，随机选择评审官要求详细说明检查内容。同一项目连续2个阶段无异议，强制第3个阶段抽查。抽查记录存入 `.contracts/{project}/spot-checks/`。

**抽查结果处理：**
- (a) 通过 → 记录在案，继续
- (b) 轻微问题 → 评审官补查修复检查项
- (c) 严重空签收 → 打回该阶段产出物，由协调者指定替代评审官（从角色配置表中其他评审官选）复核该评审官本项目所有评审结果；复核不通过→该阶段合同转 `reopened`→重新走评审

**脚本验证：** 连续2阶段无异议后，脚本检查 `spot-checks/` 目录是否有对应记录。此为协调者自律规则，脚本仅做记录存在性验证。

### 5.6 产出物最小要求

| 产出物 | 最小要求 |
|--------|---------|
| PRD | ≥200行 |
| 架构设计 | ≥100行 |
| UX/UI设计 | ≥80行 |
| 任务清单 | ≥50行 |
| 评审报告 | ≥30行 |
| 交叉评审 | 每角色≥20行 |
| 测试报告 | ≥50行 |
| 测试计划 | ≥30行 |
| 集成报告 | ≥30行 |
| 分解确认 | ≥20行 |
| Spike报告 | ≥30行 |

差额≤20%警告，差额>20%打回。`pipeline-check.sh` 自动检查。**注意：** 行数为最低门槛，若产出物包含 `required_sections`（YAML配置），脚本优先检查必要章节是否存在，行数作为补充验证。Markdown空行不计入有效行数。

### 5.6.1 代码目录检查规则

`type: "code_directory"` / `type: "test_directory"` 的产出物**不检查行数**，只检查：
1. 目录存在
2. 包含 `required_extensions` 中至少1种扩展名的文件，且文件数≥3
3. 排除目录：`node_modules/`、`vendor/`、`.git/`、`dist/`、`build/`、`__pycache__/`
4. 统计命令：`find {path} -type f \( -name "*.ts" -o -name "*.java" \) ! -path "*/node_modules/*" ! -path "*/.git/*" | wc -l`

### 5.6.2 交叉评审文件解析规则

`require_role_sections: true` 的交叉评审文件，脚本按以下规则解析：
1. **角色段落**：以 `### {role_name}` 开头的二级标题为角色段落起始，到下一个 `### ` 或文件结束为该角色段落
2. **检查点**：角色段落内以 `- ` 或 `* ` 开头的列表项计为检查点（空行和纯文字不计）
3. 脚本命令：`grep -cE '^### '` 计数角色段落数，每段落内 `grep -cE '^\s*[-*] '` 计数检查点
4. **角色名来源**：从 YAML 的 `participating_roles` 字段读取，脚本动态匹配

### 5.6.3 签收报告检查点格式

评审签收报告（非交叉评审）中的"检查点"：以 `- ` 或 `* ` 开头的列表项，包含具体描述（>10字符）。"建议"：包含"建议"或"🟢"关键词的列表项。"评分"：包含 `/10` 格式的行。

### 5.6.4 脚本错误信息标准

所有脚本错误输出必须包含：(1) 检查项名称；(2) 期望值；(3) 实际值；(4) 配置来源（YAML字段路径）。脚本支持 `--verbose` 模式，输出每步中间状态。

### 5.7 用户随时介入与暂停/恢复

流水线默认全程自主执行，不等待用户确认。用户可随时打断。

**暂停/恢复机制：**
- 用户说"暂停"→ 协调者将当前阶段号、合同状态、活跃agent列表写入 `_config.json` 的 `paused_at` 字段 → 协调者停止调度
- 用户说"继续"→ 协调者读取 `paused_at` → 从断点恢复执行
- 协调者session断开恢复：重启后读取 `_config.json` 中的 `current_phase` + `paused_at` → 从断点继续

**其他用户指令：**
- "看看进展"→ 协调者从 `_config.json` + `health-dashboard.md` + `communications/` 汇总输出
- "跳过XX阶段"→ 用户确认跳过原因 → 下游阶段合同标注"上游跳过" → 协调者评估下游是否仍可执行
- "重做"→ 先暂停活跃agent（写入 `paused_at`）→ 等待活跃agent停止（最多5min超时，超时则force kill）→ 执行回退
- "有问题"→ 协调者暂停并等待用户指示

**单阶段重试：** 用户可对任何已完成的阶段要求重做（不等同于回退，不消耗回退额度）：用户说"重做阶段N"→ 该阶段合同转 `reopened` → 重新调度执行者 → 评审官审查 → 签收后检查下游是否需要同步更新。

**单阶段检查点继续：** 阶段6开发/阶段8测试等多步骤阶段中断后，协调者可在断点继续而非从头重做：中断前已完成的子任务产出保留，只重做中断时的子任务。

---

## 机制六：项目知识库（CONTEXT.md + MemPalace）

### 问题

流水线里每阶段的 agent 都需要项目上下文，但当前靠各自读文件，容易漏读、重复读、读到过时版本。回退和需求变更后，已存的知识可能过期。

### 双层知识库

| 层 | 存储 | 用途 | 容量 |
|---|------|------|------|
| 摘要层 | `CONTEXT.md`（项目目录内） | 每个 agent 开工前必读，≤200行（约4000 tokens） | 小，全量加载 |
| 深度层 | MemPalace（`wing={project-name}`） | 遇到具体问题时按需检索 | 大，按 room 检索 |

### CONTEXT.md 结构

按阶段分段，每段覆盖更新（不是追加）：

```markdown
# {项目名} 项目上下文

## 阶段0：项目概览 | 更新于 YYYY-MM-DD
项目规模、参与角色、关键约束

## 阶段1：需求 | 更新于 YYYY-MM-DD
核心决策、MVP范围、验收标准

## 阶段2：架构 | 更新于 YYYY-MM-DD
技术栈、核心决策、API约定

...后续阶段（每段≤15行）...
```

回退/变更记录独立存放在 `.contracts/{project}/change-log.md`，不占用 CONTEXT.md 行数。

**规则：**
- 每个阶段有固定段落，执行者交付时覆盖自己的段落（不是追加新段落）
- 主阶段（0/1/2/3/4/5/6/7/8/9）各占一段，子阶段（1.5/2.5/2.8/3.5/4.5/5.5/6.3/6.5）的变更合并到父阶段段落中，不单独占段
- 回退/变更时，触发者负责更新受影响段落 + 在回退记录表中登记
- 每段落≤15行，总文件≤200行（10段 × 15行 = 150行，留50行给标题和空行）
- 回退/变更记录表从 CONTEXT.md 移出，单独存为 `.contracts/{project}/change-log.md`（不占CONTEXT行数）
- 协调者在阶段0创建初始版本

### MemPalace 深度知识

| 阶段 | room 名 | 存入内容 |
|------|---------|---------|
| 0 | `project-overview` | 完整项目计划 |
| 1 | `prd-decisions` | 功能优先级取舍理由、砍掉的需求及原因 |
| 2 | `arch-decisions` | 技术选型对比、为什么选A不选B、性能预算 |
| 2.8 | `spike-reports` | 代码原型、性能数据、限制条件 |
| 5 | `task-breakdown` | 完整任务清单、预估工时、依赖图 |
| 6 | `dev-notes` | 踩坑记录、接口变更、临时方案及原因 |
| 8 | `test-results` | 性能数据、边界case、未修复问题 |
| 9 | `project-lessons` | 回退原因、迭代超限原因、改进建议 |

**版本机制：**
- 存入时带 `version` + `updated_at` + `supersedes` 元数据（指向被取代的旧版本）
- 回退/变更时存入新版本，`supersedes` 指向旧版本，形成版本链 v3→v2→v1
- 回退场景新增 `rollback_to` 字段：指向内容恢复的目标版本（如 v3.rollback_to = v1），与 `supersedes`（v3.supersedes = v2）配合使用，区分"新内容"和"回退到旧内容"
- 检索时只返回最新版本
- 旧版本不删除，可用于回溯分析

**谁存、什么时候存：**
- 阶段执行者自己存（干活的人最清楚自己做了什么决策）
- 交付产出时同时存入，不事后整理
- 回退/变更时：触发者负责更新受影响段落 + 存入新版本

### 脚本强制检查

`pipeline-check.sh` 新增 `check_knowledge()`：

**强制检查（exit 1）：**
- CONTEXT.md 存在
- CONTEXT.md 包含当前阶段标题（`## 阶段N`）
- CONTEXT.md 总行数 ≤200

**回退一致性检查（exit 1）：**
- changes/ 目录有回退记录时
- CONTEXT.md 中受影响段落的更新时间晚于回退记录时间
- 如果不晚 → error（知识库未更新，知识可能过时）

**可选检查（warning only）：**
- MemPalace 中对应 room 是否存在（依赖 MCP，失败不断阻断）

---

## 机制七：跨项目经验复用（MemPalace）

### 阶段9：沉淀教训

项目交付后，协调者从本项目提取教训存入 MemPalace `wing=agent-pipeline room=project-lessons`。

**自动提取规则：** 扫描 `changes/`（回退记录）和 `communications/`（打回记录），凡是发生过回退或≥2轮迭代的阶段，必须提取一条教训。

### 阶段0：加载历史教训

协调者启动新项目时，用 `mempalace_search` 检索历史教训，写入 PROJECT-PLAN.md 的「历史教训」章节，并摘要写入 CONTEXT.md 阶段0段落。

---

## 迭代合同核心规则

**协调者红线：以下规则不可跳过、不可绕过、不可降低等级。**

| 风险等级 | 合同类型 | 最大轮次 | 适用场景 |
|---------|---------|---------|---------|
| 🔴 高风险 | 完整合同（30行） | 3轮 | 安全相关、核心流程、数据一致性 |
| 🟡 中风险 | 标准合同（10行） | 2轮 | 新功能、UI交互、业务逻辑 |
| 🟢 低风险 | 简化合同（3行） | 1轮 | 文案修改、样式调整、文档更新 |

**不确定风险等级时，按高等级执行。**

**轮次说明：** 角色对照表中的"最大迭代"= 该阶段合同的默认最大轮次。阶段6标注 `quality-only` 仅指代码质量风险，不触发合同轮次（开发交付由阶段6.5 reviewer审查）。`quality-only` 不属于三级风险体系，脚本遇到此标记时跳过合同轮次检查。

**`quality-only` 阶段合同规则：** `contract_risk: "quality-only"` + `max_rounds: 0` + `reviewer: null` 的阶段不创建合同。阶段完成由协调者判定：当所有执行者agent报告任务完成（对照 TASK-LIST.md）→ 协调者标记 `phase_progress` 为 `completed`。后续阶段（如6.5）的审查结果独立追踪，不回溯影响阶段6的完成状态。

**合同状态：** `in-progress` / `revision-requested` / `signed` / `escalated` / `closed` / `reopened` / `paused`

**状态转换：**
```
in-progress ──签收──→ signed
in-progress ──打回──→ revision-requested
revision-requested ──修改重提──→ in-progress（轮次+1）
in-progress ──轮次超限──→ escalated
escalated ──用户接受继续──→ signed
escalated ──用户终止/回退──→ closed
signed ──回退场景──→ reopened（等同 in-progress，可追溯）
closed ──流水线重新进入该阶段──→ in-progress（创建新合同，轮次重置）
in-progress ──agent被抢占──→ paused
revision-requested ──agent被抢占──→ paused
paused ──agent恢复──→ in-progress
paused ──用户终止──→ closed
```

**合法转换矩阵（脚本硬编码校验，非法转换 exit 1）：**
| from \ to | in-progress | revision-requested | signed | escalated | closed | reopened | paused |
|-----------|------------|-------------------|--------|-----------|--------|----------|--------|
| in-progress | - | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| revision-requested | ✅ | - | ❌ | ❌ | ❌ | ❌ | ✅ |
| signed | ❌ | ❌ | - | ❌ | ❌ | ✅ | ❌ |
| escalated | ❌ | ❌ | ✅ | - | ✅ | ❌ | ❌ |
| closed | ✅ | ❌ | ❌ | ❌ | - | ❌ | ❌ |
| reopened | ✅ | ❌ | ❌ | ❌ | ❌ | - | ❌ |
| paused | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | - |

**状态转换记录：** `_index.json` 每个合同对象增加 `transitions: [{from, to, at, by}]` 数组，`contract-check.sh` 校验每次转换的合法性。

**`_index.json` / `_config.json` 完整 Schema：** 见 `references/metadata-schema.md`（需创建，包含全部字段定义和示例）。

**轮次超限处理：** 达到最大轮次仍未签收 → 标记为 `escalated` → 协调者汇报用户决定。**禁止协调者自行决定跳过未签收的阶段。** escalated 合同的具体超时和默认处理见"Human-in-the-Loop 关键决策点"表，不在此处定义单一默认值。

**`closed` 语义：** 合同终止，该阶段工作不通过。流水线回退到该合同的上一阶段，触发新一轮合同。如无上游可回退，则项目终止并归档。

**脚本检查：** `contract-check.sh` 读取 `_index.json`，检查轮次超限未标记 escalated 的合同 + 校验合同文件存在且包含必要字段。

详细格式见 `references/iterative-contract.md`。

---

## 异步交叉评审机制

### 24h时限规则
- Agent评审参与方：1h窗口期（超时视为无异议）
- 人类评审参与方（如有）：24h窗口期（超时视为无异议）
- 🟢小型项目跳过的阶段，其时限规则也同步跳过
- 时限在 `pipeline-config.yaml` 的 `deadline_hours` 字段配置（默认24h人类/1h agent）

---

## 项目健康度看板

- **用途：** 可视化项目状态，及时发现风险
- **维护者：** 协调者（更新触发：阶段完成 / 阶段里程碑 / 回退或升级事件 / 阶段执行超过30min时每30min更新）
- **存放位置：** `.contracts/{project}/health-dashboard.md`
- **看板格式：** 进度概览、风险追踪（活跃风险+回退额度）、回退记录、整体健康度评分
- **脚本检查：** `pipeline-check.sh` 检查最后更新时间在时间窗口内

---

## 合同存储与目录结构

```
.contracts/
├── _index.json
├── _config.json
├── {project-name}/
│   ├── CONTEXT.md                    ← 项目知识库摘要
│   ├── pipeline.log                  ← 结构化流水线日志
│   ├── health-dashboard.md
│   ├── phase-0-startup/
│   ├── phase-1-prd/
│   ├── phase-1.5-prd-cross-review/
│   ├── phase-2-architecture/
│   ├── phase-2.5-arch-cross-review/
│   ├── phase-2.8-spike/
│   ├── phase-3-ux/
│   ├── phase-3.5-ux-to-ui/
│   ├── phase-4-ui/
│   ├── phase-4.5-ui-to-ux/
│   ├── phase-5-decomposition/
│   ├── phase-5.5-decomposition-confirm/
│   ├── phase-6-dev/
│   ├── phase-6.3-integration/
│   ├── phase-6.5-dev-review/
│   ├── phase-7-review/
│   ├── phase-8-test/
│   ├── phase-9-acceptance/
│   ├── changes/                      ← 回退/变更记录
│   ├── communications/              ← 沟通记录
│   ├── spot-checks/                  ← 抽查记录
│   ├── _rollback-backup/             ← 回退前备份
│   ├── mempalace-backup/             ← MCP本地备份
│   └── pending-writes/               ← MCP待重试写入
└── _archive/
    └── {project-name}/              ← 归档（含所有产出物）
```

### 各阶段产出物绝对路径

`{base}` = 项目根目录，`{p}` = 项目名称。

| 阶段 | 产出物 | 绝对路径 |
|------|--------|---------|
| 0 | 项目计划 | `{base}/.contracts/{p}/phase-0-startup/PROJECT-PLAN.md` |
| 0 | 项目上下文 | `{base}/.contracts/{p}/CONTEXT.md` |
| 0 | 健康度看板 | `{base}/.contracts/{p}/health-dashboard.md` |
| 1 | PRD | `{base}/.contracts/{p}/phase-1-prd/PRD.md` |
| 1.5 | PRD交叉评审 | `{base}/.contracts/{p}/phase-1.5-prd-cross-review/cross-review-pm.md` |
| 2 | 架构设计 | `{base}/.contracts/{p}/phase-2-architecture/ARCHITECTURE.md` |
| 2.5 | 架构交叉评审 | `{base}/.contracts/{p}/phase-2.5-arch-cross-review/cross-review-arch.md` |
| 2.8 | Spike报告 | `{base}/.contracts/{p}/phase-2.8-spike/SPIKE-REPORT.md` |
| 3 | UX设计 | `{base}/.contracts/{p}/phase-3-ux/UX-DESIGN.md` |
| 3.5 | UX→UI交接 | `{base}/.contracts/{p}/phase-3.5-ux-to-ui/cross-review-ux-to-ui.md` |
| 4 | UI设计 | `{base}/.contracts/{p}/phase-4-ui/UI-DESIGN.md` |
| 4.5 | UI→UX反向 | `{base}/.contracts/{p}/phase-4.5-ui-to-ux/cross-review-ui-to-ux.md` |
| 5 | 任务清单 | `{base}/.contracts/{p}/phase-5-decomposition/TASK-LIST.md` |
| 5 | 测试计划 | `{base}/.contracts/{p}/phase-5-decomposition/test-plan.md` |
| 5.5 | 分解确认 | `{base}/.contracts/{p}/phase-5.5-decomposition-confirm/confirm-tasks.md` |
| 6 | 代码文件 | `{base}/.contracts/{p}/phase-6-dev/` |
| 6 | 测试脚本 | `{base}/.contracts/{p}/phase-6-dev/tests/` |
| 6.3 | 集成报告 | `{base}/.contracts/{p}/phase-6.3-integration/integration-report.md` |
| 6.5 | 开发审查 | `{base}/.contracts/{p}/phase-6.5-dev-review/cross-review-dev.md` |
| 7 | 代码审查报告 | `{base}/.contracts/{p}/phase-7-review/review-report.md` |
| 7 | 审查截图 | `{base}/.contracts/{p}/phase-7-review/screenshots/` |
| 8 | 测试报告 | `{base}/.contracts/{p}/phase-8-test/test-report.md` |
| 8 | QA截图 | `{base}/.contracts/{p}/phase-8-test/qa-reports/` |
| 9 | 验收报告 | `{base}/.contracts/{p}/phase-9-acceptance/ACCEPTANCE-REPORT.md` |
| 全局 | 变更记录 | `{base}/.contracts/{p}/changes/` |
| 全局 | 沟通记录 | `{base}/.contracts/{p}/communications/` |
| 全局 | 抽查记录 | `{base}/.contracts/{p}/spot-checks/` |
| 全局 | 变更日志 | `{base}/.contracts/{p}/change-log.md` |
| 全局 | MCP备份 | `{base}/.contracts/{p}/mempalace-backup/` |
| 全局 | 回退备份 | `{base}/.contracts/{p}/_rollback-backup/` |

---

## 脚本清单与依赖关系

```
pipeline-check.sh（主入口，每阶段调用）
  ├── 直接检查：文件存在 + 行数 + 沟通记录 + 健康度看板 + 知识库(CONTEXT.md)
  ├── 阶段6.5/7 → 调用 review-check.sh
  ├── 阶段8 → 调用 test-report-check.sh
  └── 阶段9 → 调用 acceptance-check.sh
                  ├── 调用 contract-check.sh
                  └── 调用 security-scan.sh
```

| 脚本 | 对应规则 | 功能 |
|------|---------|------|
| `pipeline-check.sh` | 5.1+5.6 | 产出文件存在+行数（含2.8/6.3/6.5）+沟通记录内容格式+健康度+知识库+规模感知 |
| `review-check.sh` | 5.2+5.3 | 评审报告≥3检查点+≥1建议+评分+交叉评审独立段落 |
| `contract-check.sh` | 合同+回退 | 轮次超限检查+回退次数统计（区分rollback-/change-/minor-前缀）+索引一致性+合同必要字段+合同状态机校验 |
| `test-report-check.sh` | 阶段8 | 报告≥50行+截图≥3+逐项结果+通过率+问题清单 |
| `acceptance-check.sh` | 阶段9 | 7项验收checklist+调用contract-check+security-scan |
| `security-scan.sh` | 安全 | 10类安全扫描（硬编码密钥/SQL注入/XSS/反序列化/日志泄露/CORS/路径遍历/JWT弱密钥/访问控制缺失/安全日志缺失）|

---

## CI/CD集成（可选）

仅当项目使用 GitHub/GitLab CI 时启用，本地开发项目可跳过。阶段6.3后自动触发CI，阶段9通过后可自动部署。

---

## 脚本-Skill 职责分界

**脚本管"做什么、做多少、做对了没"，skill 管"怎么做好"。**

| 管什么 | 谁管 | 怎么管 |
|--------|------|--------|
| 阶段顺序和跳转 | 脚本 | pipeline-check.sh case 语句 + 规模裁剪表 |
| 产出物名称和路径 | 脚本 | 每阶段检查项中指定 |
| 产出物最小行数 | 脚本 | wc -l 对比阈值 |
| 评审检查点数量 | 脚本 | review-check.sh grep 计数 |
| 合同轮次限制 | 脚本 | contract-check.sh 读 _index.json |
| 回退次数限制 | 脚本 | contract-check.sh 统计 changes/ |
| 24h时限 | 脚本 | 记录起始时间戳，对比当前时间 |
| 知识库更新验证 | 脚本 | check_knowledge() 检查段落存在+日期+行数 |
| 目录结构初始化 | 脚本 | mkdir -p 创建标准目录 |
| 安全扫描 | 脚本 | security-scan.sh 8类检查 |
| 测试报告格式 | 脚本 | test-report-check.sh 6项检查 |
| 验收7项标准 | 脚本 | acceptance-check.sh 自动验证 |
| 沟通记录完整性 | 脚本 | grep 发送方/接收方/类型 |
| 健康度看板更新 | 脚本 | stat 检查最后修改时间 |
| 怎么写好PRD | Skill | requirements-analysis 方法论 |
| 怎么做好架构设计 | Skill | tech-architecture 方法论 |
| 怎么验证技术可行性 | Skill | tech-spike 方法论 |
| 怎么拆好任务 | Skill | task-decomposition 方法论 |
| 怎么写好测试 | Skill | qa-workflow 方法论 |
| 怎么审查代码 | Skill | code-review-checklist 维度清单 |
| 怎么保证编码质量 | Skill | code-quality-guard 规范 |
| 怎么去AI味 | Skill | humanize-code 检查方法 |
| 怎么和用户讨论 | SKILL.md | Brainstorm 讨论规则 |
| 评审官怎么挑毛病 | SKILL.md | 思维模式定义（魔鬼代言人等）|
| 规模判定 | 协调者 | 需要判断力，脚本只读取判定结果 |
| MemPalace 存取 | 协调者 | 需要 MCP 工具，脚本无法直接调用 |
| 流程编排和调度 | SKILL.md | 协调者读 skill 知道该做什么、调谁 |

---

## 文件清单

**权威源原则：PRD 是唯一的产品需求权威，`pipeline-config.yaml` 是 PRD 的可执行子集，SKILL.md 和脚本必须与 PRD 保持一致。SKILL.md 中与 PRD 重复的内容以 PRD 为准。**

**关键交接文件模板：** 以下文件对下游agent解析至关重要，必须按 `templates/` 目录下的模板产出，关键字段用固定格式标题/表格，下游agent可可靠解析：(1) `TASK-LIST.md` — 开发者分配必须用 `| 开发者 | {agent_id} |` 表格格式；(2) `ARCHITECTURE.md` — API设计必须有 `### API Endpoints` 章节，数据模型必须有 `### Data Models` 章节；(3) `test-plan.md` — P0功能列表必须用 `- [ ] {功能名}` 格式；(4) `PRD.md` — 功能清单必须有 `### 功能清单` 章节。

---

## 流水线配置即代码（Pipeline as Code）

PRD 中的结构性规则（产出物路径、行数阈值、合同轮次、规模跳过、必填章节、时限等）提取到 `pipeline-config.yaml`，脚本读配置驱动执行，而非硬编码 case 语句。**改规则 = 改配置，不碰脚本代码。**

### 配置文件位置

`.openclaw/agents/agent-pipeline/pipeline-config.yaml`

### 配置结构

```yaml
# pipeline-config.yaml — 流水线定义，脚本读它驱动执行
version: "1.0"

stages:
  - id: "0"
    name: "启动"
    executor: "coordinator"
    reviewer: null
    contract_risk: null
    max_rounds: 0
    outputs:
      - path: "phase-0-startup/PROJECT-PLAN.md"
        min_lines: 30
      - path: "CONTEXT.md"
        min_lines: 10
        root_level: true          # 不在 phase-N 子目录下
      - path: "health-dashboard.md"
        min_lines: 5
        root_level: true
    skill: null
    knowledge:
      context_phase: 0
      mempalace_room: "project-overview"
    size_skip: []
    timeout_minutes: 10

  - id: "1"
    name: "需求分析"
    executor: "pm"
    reviewer: "pm-reviewer"
    reviewer_mindset: "魔鬼代言人"
    contract_risk: "medium"
    max_rounds: 2
    outputs:
      - path: "phase-1-prd/PRD.md"
        min_lines: 200
        required_sections: ["用户故事", "验收标准", "功能清单"]
    skill: "requirements-analysis"
    brainstorm: true
    knowledge:
      context_phase: 1
      mempalace_room: "prd-decisions"
    size_skip: []
    timeout_minutes: 30

  - id: "1.5"
    name: "PRD交叉评审"
    executor: "multi-role"       # 架构师/QA/开发/UI/UX 并发
    reviewer: "pm-reviewer"      # 复核
    contract_risk: "low"
    max_rounds: 1
    outputs:
      - path: "phase-1.5-prd-cross-review/cross-review-pm.md"
        min_lines: 50
        require_role_sections: true
        min_checkpoints_per_role: 3
        participating_roles: ["architect", "qa", "backend", "ui-designer", "ux-tester"]
    size_skip: ["small"]
    deadline_hours: 24
    timeout_minutes: 30

  - id: "2"
    name: "架构设计"
    executor: "architect"
    reviewer: "architect-reviewer"
    reviewer_mindset: "架构审计师"
    contract_risk: "medium"
    max_rounds: 2
    outputs:
      - path: "phase-2-architecture/ARCHITECTURE.md"
        min_lines: 100
        required_sections: ["技术选型", "数据模型", "API设计", "安全措施"]
        spike_trigger_keywords: ["高风险", "Spike", "待验证"]
    skill: "tech-architecture"
    brainstorm: true
    knowledge:
      context_phase: 2
      mempalace_room: "arch-decisions"
    size_skip: []
    timeout_minutes: 30
    small_executor_override: "pm"  # 🟢小型由PM兼任

  - id: "2.5"
    name: "架构交叉评审"
    executor: "multi-role"
    reviewer: "architect-reviewer"
    contract_risk: "low"
    max_rounds: 1
    outputs:
      - path: "phase-2.5-arch-cross-review/cross-review-arch.md"
        min_lines: 40
        require_role_sections: true
        min_checkpoints_per_role: 3
        participating_roles: ["backend", "qa"]
    size_skip: ["small"]
    deadline_hours: 24
    timeout_minutes: 30

  - id: "2.8"
    name: "技术Spike"
    executor: "architect"         # 或开发
    reviewer: null
    contract_risk: null
    max_rounds: 1
    outputs:
      - path: "phase-2.8-spike/SPIKE-REPORT.md"
        min_lines: 30
        required_keywords: ["可行", "不可行", "需调整"]
    skill: "tech-spike"
    knowledge:
      context_phase: "2.8"
      mempalace_room: "spike-reports"
    size_skip: ["small"]
    timeout_minutes: 240          # 4h硬限制
    spike_max_retries: 2          # 同一技术点最多2次

  - id: "3"
    name: "UX设计"
    executor: "ux-tester"
    reviewer: "ux-tester-reviewer"
    reviewer_mindset: "人类学家"
    contract_risk: "medium"
    max_rounds: 2
    outputs:
      - path: "phase-3-ux/UX-DESIGN.md"
        min_lines: 80
    knowledge:
      context_phase: 3
      mempalace_room: null        # 完整文档在文件里，不存MemPalace
    size_skip: ["small"]
    timeout_minutes: 30

  - id: "3.5"
    name: "UX→UI交接"
    executor: "ui-designer"
    reviewer: null
    contract_risk: "low"
    max_rounds: 1
    outputs:
      - path: "phase-3.5-ux-to-ui/cross-review-ux-to-ui.md"
        min_lines: 20
    size_skip: ["small", "medium"]
    timeout_minutes: 15

  - id: "4"
    name: "UI设计"
    executor: "ui-designer"
    reviewer: "ui-designer-reviewer"
    reviewer_mindset: "美学刺客"
    contract_risk: "medium"
    max_rounds: 2
    outputs:
      - path: "phase-4-ui/UI-DESIGN.md"
        min_lines: 80
    knowledge:
      context_phase: 4
      mempalace_room: null
    size_skip: []
    timeout_minutes: 30
    small_executor_override: "pm"  # 🟢小型由PM兼任

  - id: "4.5"
    name: "UI→UX反向"
    executor: "ux-tester"
    reviewer: null
    contract_risk: "low"
    max_rounds: 1
    outputs:
      - path: "phase-4.5-ui-to-ux/cross-review-ui-to-ux.md"
        min_lines: 20
    size_skip: ["small", "medium"]
    timeout_minutes: 15

  - id: "5"
    name: "任务分解"
    executor: "startup-helper"
    executor_parallel: "qa"       # QA并行产出测试计划
    reviewer: "startup-helper-reviewer"
    reviewer_parallel: "qa-reviewer"
    reviewer_mindset: "冷血投资人"
    contract_risk: "medium"
    max_rounds: 2
    outputs:
      - path: "phase-5-decomposition/TASK-LIST.md"
        min_lines: 50
        required_sections: ["批次", "依赖", "开发者"]
      - path: "phase-5-decomposition/test-plan.md"
        min_lines: 30
    skill: "task-decomposition"
    brainstorm: true
    knowledge:
      context_phase: 5
      mempalace_room: "task-breakdown"
    size_skip: []
    timeout_minutes: 30

  - id: "5.5"
    name: "分解确认"
    executor: "multi-developer"   # 开发×3 并发确认
    reviewer: null                # 开发确认无需独立评审官，确认结果由阶段6开发实践验证
    contract_risk: "low"
    max_rounds: 1
    outputs:
      - path: "phase-5.5-decomposition-confirm/confirm-tasks.md"
        min_lines: 20
        required_developer_sections: true
    size_skip: ["small"]
    timeout_minutes: 15

  - id: "6"
    name: "开发执行"
    executor: "developers"        # 多开发并发
    reviewer: null
    contract_risk: "quality-only"  # 代码质量风险，不触发合同轮次
    max_rounds: 0                 # 无评审官，6.5审查
    outputs:
      - path: "phase-6-dev/"
        type: "code_directory"
        required_extensions: [".ts", ".java", ".vue", ".js", ".py"]
      - path: "phase-6-dev/tests/"
        type: "test_directory"
        required_extensions: [".spec.ts", ".test.ts"]
    skill: "code-quality-guard"
    knowledge:
      context_phase: 6
      mempalace_room: "dev-notes"
    size_skip: []
    timeout_minutes: 240
    developer_count:
      large: 3
      medium: 2
      small: 1

  - id: "6.3"
    name: "代码集成"
    executor: "dev3"
    reviewer: null
    contract_risk: null
    max_rounds: 0
    outputs:
      - path: "phase-6.3-integration/integration-report.md"
        min_lines: 30
        required_smoke_results: true   # 必须有✅/❌逐项结果
    size_skip: ["small"]
    timeout_minutes: 60
    smoke_max_retries: 3

  - id: "6.5"
    name: "开发审查"
    executor: "reviewers"         # 各reviewer并行
    reviewer: null
    contract_risk: null
    max_rounds: 1
    outputs:
      - path: "phase-6.5-dev-review/cross-review-dev.md"
        min_lines: 30
        require_role_sections: true
        min_checkpoints_per_role: 3
    skill: "code-review-checklist"
    check_script: "review-check.sh"
    size_skip: []
    timeout_minutes: 60

  - id: "7"
    name: "代码审查"
    executor: "qa-reviewer+architect-reviewer"  # 评审官执行审查
    reviewer: "coordinator"                      # 协调者复核审查质量
    reviewer_mindset: "QA视角+架构视角"
    contract_risk: "high"
    max_rounds: 3
    outputs:
      - path: "phase-7-review/review-report.md"
        min_lines: 30
        min_screenshots: 1
      - path: "phase-7-review/screenshots/"
        type: "directory"
    skill: "code-review-checklist+qa-workflow+humanize-code"
    check_script: "review-check.sh"
    size_skip: []
    timeout_minutes: 60
    small_reviewer_override: "qa-reviewer"  # 🟢小型QA评审官兼任

  - id: "8"
    name: "测试验证"
    executor: "qa"
    reviewer: "qa-reviewer"
    reviewer_mindset: "测试艺术家"
    contract_risk: "high"
    max_rounds: 3
    outputs:
      - path: "phase-8-test/test-report.md"
        min_lines: 50
        required_sections: ["前置条件", "执行步骤", "预期结果", "实际结果"]
        required_keywords: ["通过率", "P0"]
      - path: "phase-8-test/qa-reports/"
        type: "directory"
        min_files: 3
        file_extensions: [".png", ".jpg"]
    skill: "qa-workflow"
    check_script: "test-report-check.sh"
    knowledge:
      context_phase: 8
      mempalace_room: "test-results"
    size_skip: []
    timeout_minutes: 120
    test_levels:
      large: ["L1", "L2", "L3"]
      medium: ["L1", "L2"]
      small: ["L1"]

  - id: "9"
    name: "交付验收"
    executor: "coordinator"
    reviewer: null
    contract_risk: null
    max_rounds: 0
    outputs:
      - path: "phase-9-acceptance/ACCEPTANCE-REPORT.md"
        min_lines: 30
        required_checklist_items: 7
    check_script: "acceptance-check.sh"
    knowledge:
      context_phase: 9
      mempalace_room: "project-lessons"
    size_skip: []
    timeout_minutes: 30

# 全局配置
global:
  context_max_lines: 200
  context_max_per_phase: 15
  context_max_tokens: 4000      # 近似值，line数为主控
  rollback_max_total: 5
  rollback_max_consecutive: 2
  change_max_functional: 3       # 🟡功能调整额度
  escalation_timeout_hours: 24
  escalation_max_wall_hours: 72  # 升级终止墙
  spot_check_after_consecutive_passes: 2
  flaky_test_max_retries: 1
  flaky_test_max_flags: 3
  max_concurrent_api_calls: 3   # 并发API请求上限
  rate_limit_backoff_seconds: 30
  spike_max_points_per_project: 3  # 项目最多Spike技术点数
  spike_max_total_hours: 12       # 项目Spike总时间上限
  smoke_retry_max_hours: 2        # 冒烟修复总时限
  agent_wait_timeout_minutes: 60  # 等待agent资源超时
  agent_kill_cleanup: true         # kill后清理残留

# Token 预算分配（估算）
token_budget:
  large: 400000
  medium: 250000
  small: 100000
  per_stage:
    "0": 5000
    "1": 20000
    "1.5": 15000
    "2": 20000
    "2.5": 10000
    "2.8": 10000
    "3": 15000
    "3.5": 3000
    "4": 15000
    "4.5": 3000
    "5": 15000
    "5.5": 5000
    "6": 50000
    "6.3": 8000
    "6.5": 15000
    "7": 15000
    "8": 20000
    "9": 5000
  # per_stage合计: ~241K (medium)，预留~9K给回退/变更

# 版本信息
config_version: "1.0"

# DoD 清单（脚本按此逐项检查）
# script_verifiable: true = 脚本可自动验证; false = 需评审官签收时确认
definition_of_done:
  "1":
    - item: "覆盖所有用户故事"
      script_verifiable: false
    - item: "每个功能有验收标准"
      script_verifiable: false
    - item: "优先级标注"
      script_verifiable: true
    - item: "评审官签收"
      script_verifiable: true
    - item: "CONTEXT.md已更新"
      script_verifiable: true
  "2":
    - item: "技术选型有对比理由"
      script_verifiable: false
    - item: "API设计完整"
      script_verifiable: false
    - item: "数据模型完整"
      script_verifiable: false
    - item: "安全措施列出"
      script_verifiable: true
    - item: "高风险点标注"
      script_verifiable: true
    - item: "评审官签收"
      script_verifiable: true
    - item: "CONTEXT.md已更新"
      script_verifiable: true
  "5":
    - item: "每个任务有明确输入输出"
      script_verifiable: false
    - item: "依赖关系无环"
      script_verifiable: true
    - item: "每个任务有验收标准"
      script_verifiable: false
    - item: "P0任务100%覆盖"
      script_verifiable: false
    - item: "评审官签收"
      script_verifiable: true
  "6":
    - item: "代码编译通过"
      script_verifiable: true
    - item: "单元测试通过"
      script_verifiable: true
    - item: "lint无error"
      script_verifiable: true
    - item: "安全扫描0严重问题"
      script_verifiable: true
    - item: "migration脚本存在且可执行"
      script_verifiable: true
    - item: "reviewer审查完成"
      script_verifiable: true
  "8":
    - item: "test-plan中P0测试100%执行"
      script_verifiable: true
    - item: "P0功能通过率100%"
      script_verifiable: true
    - item: "无未解决P0缺陷"
      script_verifiable: true
    - item: "报告格式合规"
      script_verifiable: true
  "9":
    - item: "7项验收标准全部✅"
      script_verifiable: true
    - item: "端到端旅程走通"
      script_verifiable: false
    - item: "经验教训已沉淀"
      script_verifiable: true
```

### 脚本读取配置

```bash
# pipeline-check.sh 读取配置驱动检查
CONFIG_FILE="$(dirname "$0")/../pipeline-config.yaml"

# 环境依赖检测
check_env() {
  if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install: brew install python3" >&2; exit 1
  fi
  if ! python3 -c "import yaml" 2>/dev/null; then
    echo "ERROR: pyyaml not found. Install: pip3 install pyyaml" >&2; exit 1
  fi
}
check_env

# 解析阶段配置（macOS 无 jq，用 python3）
get_stage_config() {
  python3 -c "
import yaml, json, sys
with open('$CONFIG_FILE') as f:
    data = yaml.safe_load(f)
stage = [s for s in data['stages'] if s['id'] == '$1']
if stage:
    print(json.dumps(stage[0]))
else:
    print('{}')
"
}

# 示例：检查阶段1
STAGE=$(get_stage_config "1")
MIN_LINES=$(echo "$STAGE" | python3 -c "import json,sys; print(json.load(sys.stdin)['outputs'][0]['min_lines'])")
OUTPUT_PATH=$(echo "$STAGE" | python3 -c "import json,sys; print(json.load(sys.stdin)['outputs'][0]['path'])")
```

### 配置与 PRD 的关系

| 位置 | 内容 | 角色 |
|------|------|------|
| PRD.md | 完整规则+理由+示例 | 权威文档，人读 |
| pipeline-config.yaml | 结构性规则的可执行子集 | 脚本输入，机器读 |
| SKILL.md | 编排逻辑+创作方法论 | agent 读 |

**同步规则：** PRD 改了结构性规则 → 必须同步改 YAML → 脚本自动跟随。YAML 和 PRD 冲突时以 PRD 为准，但脚本只能执行 YAML 中的规则。

**`pipeline-config.yaml` 是阶段定义的 single source of truth。** 脚本从 YAML 读取所有阶段信息（产出路径、行数阈值、规模跳过、角色），不再硬编码 case 语句。新增阶段只需：改 YAML + 写阶段详细说明（PRD中）。YAML 配置启动时校验：每个 stage 必须有 id/name/executor/outputs 字段，`size_skip` 值必须在 `["small","medium","large"]` 中，`required_sections` 的 key 在 `pipeline-check.sh` 中用固定英文 key 匹配（中文 displayName 仅用于展示）。

**`_index.json` 和 `_config.json` 完整 Schema：** 定义在 `references/metadata-schema.md`（需创建），包含全部字段、类型、默认值、示例。脚本启动时 `--validate-metadata` 校验JSON语法+必要字段。字段命名统一：合同完成状态用 `signed`（非 `completed`），与合同状态机一致。

### 保留

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 流水线骨架（编排逻辑 + skill 引用） |
| `PRD.md` | 本文件（完整产品需求） |
| `ARCHITECTURE.md` | 技术方案 |
| `SCRIPT-SKILL-FLOW.md` | 脚本-Skill 穿插执行流程 |
| `references/iterative-contract.md` | 合同协议规范 |
| `references/security-scan-templates.md` | Playwright 动态扫描模板 |
| `scripts/pipeline-check.sh` | 流程检查（需增强） |
| `scripts/security-scan.sh` | 安全扫描 |

### 新增

| 文件 | 用途 |
|------|------|
| `scripts/lib.sh` | 共享函数库 |
| `scripts/review-check.sh` | 评审质量检查 |
| `scripts/contract-check.sh` | 合同+回退检查 |
| `scripts/test-report-check.sh` | 测试报告格式检查 |
| `scripts/acceptance-check.sh` | 阶段9验收检查 |
| `pipeline-config.yaml` | 流水线配置（可执行规则） |
| `references/metadata-schema.md` | _index.json 和 _config.json 完整 JSON Schema |
| `scripts/orchestrator.sh` | 协调者调度逻辑（状态机驱动，输出下一步指令）|
| `templates/` | 关键交接文件 Markdown 模板（PRD/TASK-LIST/test-plan/ARCHITECTURE）|

### 已删除

| 文件 | 原因 |
|------|------|
| `SPLIT-PLAN.md` | 拆分计划已执行完毕 |
| `SKILL-v4.md` / `SKILL-v4-full.md` | v4备份，不再需要 |
| `templates/standards/*` | 已迁到独立 skill |
| `templates/souls/*` | 已迁到独立 skill |
| `references/unified-code-review-standards.md` | 已被 code-review-checklist 覆盖 |

---

## 机制八：错误处理与异常恢复

### Agent 超时

| 阶段类型 | 最大执行时限 | 超时处理 |
|---------|------------|---------|
| 文档产出（1/2/3/4/5） | 30min | 协调者kill → 清理残留 → 重试（最多2次）→ 仍失败则 escalated |
| 开发执行（6） | 4h | 同上，单次时限更长 |
| 评审/审查（6.5/7） | 1h | 同上 |
| 测试验证（8） | 2h | 同上 |
| Spike（2.8） | 4h（硬限制） | 超时视为失败 |

**Kill后清理协议：** 协调者kill agent后，重试前必须执行：(1) 将部分产出移到 `_rollback-backup/phase-N-kill-{timestamp}/`（移动操作事务化：先复制到backup，成功后删除原文件，backup失败则不删除）；(2) 验证 CONTEXT.md 完整性（有效markdown，无截断——检查文件是否以完整段落结尾，不以换行+`|`等不完整markdown结束）；(3) 清理被kill agent的session残留消息；(4) `pipeline-check.sh --validate` 检查产出文件完整性（Markdown文件不以截断段落结尾，JSON文件可完整解析）。

**回退时并发阶段的处理规则：** 回退触发时，若目标阶段存在正在执行的并发阶段（如回退到阶段2时2.5正在执行）：(1) 协调者立即暂停并发阶段（`paused`）；(2) 已完成的并发阶段产出标记 `stale`；(3) 目标阶段重做完成后，并发阶段按需重做。脚本检查 `phase_progress` 时必须验证并发阶段状态一致性。

### 产出损坏检测

脚本检查产出文件：非空 + 可解析（JSON无语法错误、Markdown有标题结构 `##`）。损坏则要求执行者重提，不计入轮次。

**元数据文件保护：** `_index.json` 和 `_config.json` 写入时采用原子写入（先写临时文件，再 rename）。`pipeline-check.sh --validate-metadata` 校验JSON语法和必要字段。维护最近3个版本在 `_rollback-backup/metadata/` 中，损坏时从备份恢复。

**全部备份损坏的恢复策略：** `pipeline-check.sh --rebuild-index` 模式从文件系统状态重建 `_index.json`：扫描各阶段目录产出物是否存在 → 推断阶段状态（有产出物=completed，无=not-started）→ 从 `changes/` 统计回退次数 → 重建合同记录（状态默认为 `signed`，需要人工确认）→ 写入 `_config.json` 的 `rebuilt_at` 时间戳标记。四数据源交叉验证：`pipeline-check.sh --full-audit` 比对 `_index.json` 合同状态 vs 文件系统产出物 vs `CONTEXT.md` 段落时间 vs `_config.json` current_phase，不一致时以文件系统为事实源重建。

### 协调者 Session 断开

`_config.json` 记录 `current_phase` + `current_contracts`（活跃合同列表）+ `active_agents`（活跃agent列表）+ `rollback_in_progress`（是否有进行中的回退）+ `coordinator_heartbeat`（最后心跳时间，每5min更新）。协调者重启后读取该字段，从断点继续。

**防数据丢失措施：** (1) 协调者每次派发任务后、等待agent响应前，必须先更新 `_config.json` 的 `active_agents`；(2) agent返回结果同时写入 `agent-logs/{agent-id}.log`，协调者恢复后扫描本地日志重建丢失的通信；(3) 恢复时检查 `coordinator_heartbeat` 间隔，若>10min则判定为异常断开，触发完整性检查。

**回退中断恢复：** 协调者在回退开始前写入 `changes/rollback-{id}-plan.md`（列出所有状态变更步骤），`_config.json` 增加 `rollback_in_progress: true`。重启后若发现回退未完成，读取 plan 继续执行或回滚本次回退操作。

### MCP 工具降级

MemPalace 不可用时：存入操作写入本地备份 `.contracts/{project}/mempalace-backup/{room}.json`，同时写入待重试队列 `.contracts/{project}/pending-writes/`，协调者后续重试。检索操作优先 MCP，失败则读本地备份。

**跨项目知识降级：** 本地备份仅含本项目历史写入，不含其他项目的跨项目教训。MCP 不可用时，协调者在阶段0日志中标注"跨项目教训不可用"，项目仅依赖本项目知识和 PRD 中的通用规则。MCP 恢复后，协调者自动从 `pending-writes/` 重试未成功的写入。

**静默失败检测：** `pipeline-check.sh` 可选检查：`pending-writes/` 目录积压>10条 warning。`pending-writes/` 重试最多5次，超限标记 `failed` 并通知用户。

### 脚本异常

脚本执行失败（非 exit 1 而是 segfault 等）：记录日志 → 警告用户 → 允许协调者手动标记阶段完成（附理由）。`pipeline-check.sh --skip-checks` 降级模式仅 warning 不阻断，**但必须写入审计记录**：`changes/skip-checks-{timestamp}.md`，包含跳过原因、哪些检查被跳过、谁授权、预期影响。

---

## 机制九：多项目并发与资源调度

### Agent Session 隔离

同一 agent ID（如 `pm`）同一时间只服务一个项目。项目排队机制：`_config.json` 全局增加 `project_queue`，协调者串行化或受控并发执行。**并发限制：** 最多3个项目同时活跃，每个agent等待队列最多3个项目，超出则拒绝新项目并提示"系统容量已满"。队列优先级：用户设置的项目优先级优先，同优先级FIFO。

### 资源争抢

当项目A和项目B同时需要 `pm` agent：先到先得，后到的项目协调者在 `health-dashboard.md` 中标记"等待pm资源"。用户可设置项目优先级，高优先级项目可抢占低优先级项目的 agent。

**抢占协议：** 高优先级项目抢占时 → 被抢占agent完成当前原子工作单元（最长5min等待，如写完当前文件、完成当前评审轮）→ 被抢占项目合同转 `paused` → 释放agent → 高优先级项目获得agent。若5min内agent无法完成检查点，协调者force kill，阶段标记为 `interrupted`。恢复时从最后检查点重做（协调者通过 `phase_progress` 追踪阶段内子任务完成情况）。
**等待超时：** 单个agent等待时间≤1h，超时则该项目暂停并通知用户。
**死锁检测：** 协调者每30min检查是否存在循环等待（A等B的pm，B等A的qa），发现则按优先级强制释放低优先级项目的agent。

### 并发安全

`_index.json` 并发更新由协调者串行化：agent 通过消息通知协调者更新状态，协调者集中管理所有写入，避免并发冲突。`version` 字段仅用于协调者重启恢复时检测断点期间的未提交变更。

### 项目生命周期

项目 = 唯一名称 + 目录路径，名称在 `_config.json` 全局注册，不可重复。生命周期状态：`active`（执行中）→ `paused`（暂停）→ `completed`（阶段9通过）→ `archived`（归档）。归档时：agent session 释放、产出物移到 `_archive/{project-name}/`、当前版本 `pipeline-config.yaml` 快照一并保存、MemPalace project-lessons 永久保留。恢复归档项目时自动使用归档时的配置版本。

**项目隔离：** agent 只能读写自己项目的 `.contracts/{project-name}/` 子目录，禁止跨项目访问。MemPalace 写入使用项目级 `wing={project-name}`，全局 `wing=agent-pipeline` 仅限追加（存教训），不可修改或删除。

---

## 机制十：可观测性

### 进度追踪

**结构化日志格式：** 所有流水线事件写入 `.contracts/{project}/pipeline.log`，JSON格式：`{"ts":"ISO8601","project":"name","phase":"N","agent":"id","event":"type","severity":"info|warn|error","msg":"text","meta":{}}`。每个agent在执行前先写入本地日志 `.contracts/{project}/agent-logs/{agent-id}.log`，完成后通知协调者合并到主日志。agent崩溃时协调者从本地日志恢复最后状态。

`_config.json` 增加 `phase_progress` 字段，记录每个阶段状态：

```
阶段状态: not-started | in-progress | waiting-review | revision | completed | skipped | rolled-back | waiting-user | waiting-resource | paused
转换:
  not-started → in-progress（协调者调度）
  in-progress → waiting-review（执行者提交）
  waiting-review → completed（评审签收）
  waiting-review → revision（评审打回）
  waiting-review → waiting-user（合同escalated，等用户决策）
  waiting-user → waiting-review（用户接受继续）
  waiting-user → rolled-back（用户选择回退/终止）
  revision → in-progress（修改重提）
  completed → rolled-back（回退场景）
  not-started → skipped（小型项目跳过）
  skipped → not-started（规模升级重评，需要补做）
  rolled-back → not-started（准备重做）
  in-progress → waiting-resource（agent被其他项目占用）
  waiting-resource → in-progress（agent可用）
  任意状态 → paused（用户暂停）
  paused → in-progress（用户继续，从断点恢复）
```

协调者调度逻辑基于状态机，脚本也可校验状态转换合法性。

### 健康度看板展示

协调者每完成一个阶段后向用户输出看板摘要（格式化进度条+风险列表+回退额度消耗）。用户问"进展如何"时，协调者从 `_config.json` + `health-dashboard.md` + `communications/` 汇总输出。

### 异常告警

关键事件协调者必须立即通知用户（不等阶段完成）：合同 escalated、回退额度耗尽、agent 超时、脚本失败、安全扫描严重问题。

### 历史趋势

记录每个阶段的实际耗时 vs 预估耗时（`_config.json` 的 `phase_durations` 字段），用于后续项目的时间预估。

---

## 机制十一：性能与成本控制

### Token 消耗基准（估算）

| 阶段 | 估算 token | 说明 |
|------|-----------|------|
| 0. 启动 | ~5K | 读需求+规划 |
| 1. PRD | ~20K | Brainstorm+写PRD+评审 |
| 1.5 交叉评审 | ~15K | 多角色并发评审 |
| 2. 架构 | ~20K | Brainstorm+写架构+评审 |
| 2.5 交叉评审 | ~10K | 开发+QA评审 |
| 3/4 UX/UI | ~30K | 设计+评审×2 |
| 5. 任务分解 | ~15K | 分解+评审 |
| 6. 开发 | ~50K+ | 按代码量变化大 |
| 6.5/7 审查 | ~30K | 多reviewer并发 |
| 8. 测试 | ~20K | 执行+报告 |
| 9. 验收 | ~5K | 走查+汇总 |
| **中型合计** | **~240K** | 不含回退重做（预留~10K给回退/变更） |

### 预算控制

用户可设置项目总 token 预算（`_config.json` 的 `token_budget` 字段）。超限时流水线暂停并提醒用户。每阶段预算分配：大型 ~400K、中型 ~250K、小型 ~100K。

**Token 计量：** 协调者在每个agent任务完成后，要求agent自报本次消耗token数（输入+输出），写入 `_config.json` 的 `phase_tokens` 字段。此为估算值，不保证精确，但足以做预算控制。**异常检测：** agent自报0 token则标记warning；协调者追踪每小时消耗速率，预测预算耗尽时间。阶段开始前检查剩余预算 vs 预估需求，剩余<20%时警告，耗尽时暂停。**长阶段（timeout_minutes≥60）在执行中点做一次预算检查。** 回退token消耗：预留项目总预算的20%作为回退储备（总预算*20%预扣，非回退阶段最多可用总预算*80%），非回退阶段消耗超过80%时警告用户。**Token耗尽处理：** 当前子任务完成后暂停（非立即中断），子任务完成判定=agent完成当前sessions_send任务并返回结果。

### 成本优化

- CONTEXT.md 控制上下文长度（≤200行）
- Brainstorm 讨论控制单次输入长度
- 评审时只传 diff 而非全量（阶段6.5/7）
- 并发 agent 对 API 速率限制的影响：3个开发并发=3倍速率消耗，需配置速率限制策略
- **速率限制配置：** `pipeline-config.yaml` global 增加 `max_concurrent_api_calls: 3`（默认），`rate_limit_backoff_seconds: 30`（429响应后退避），协调者维护请求队列，超过并发上限的请求排队等待

---

## 机制十二：版本兼容与演进

### PRD 版本

PRD.md 顶部增加 `version: X.Y` 和 `updated_at` 字段。

### 项目锁定版本

`_config.json` 增加 `prd_version` + `config_yaml_version` 字段，项目启动时锁定当前 PRD 版本和 YAML 配置版本，执行期间不受新版本影响。`pipeline-config.yaml` 增加 `prd_min_version` 字段，脚本启动时校验 `config_yaml_version` 与 YAML 的 `config_version` 一致 + `prd_min_version` ≤ `prd_version`，不一致则 exit 1 列出不匹配项。正在执行的项目可选升级（需用户确认）或继续使用锁定版本。

### 版本升级迁移

PRD 变更分为两类：(1) **结构性变更**（新增阶段、产出路径变化、合同格式变化）→ 执行中项目不可升级，需完成当前阶段后重启项目或继续使用锁定版本；(2) **流程性变更**（评审标准调整、DoD 修改、阈值微调）→ 执行中项目可立即采用，无需重启。脚本通过 `config_version` 的 major.minor 区分：major 变化为结构性，minor 为流程性。

### 合同格式版本

`_index.json` 增加 `schema_version`，脚本检查 `schema_version` 决定校验逻辑。

### 脚本版本

每个脚本文件增加 `VERSION` 常量（与 `pipeline-config.yaml` 的 `config_version` 共享 major 版本），`pipeline-check.sh` 启动时校验子脚本 major 版本一致。major 版本不一致则 exit 1，minor 版本不一致则 warning。

---

## 质量门：每阶段 Definition of Done

行数是最低门槛，但不等于质量。每阶段必须满足 DoD 清单，`pipeline-check.sh` 按 DoD 逐项检查：

| 阶段 | DoD（全部满足才算完成） |
|------|----------------------|
| 1. PRD | 覆盖所有用户故事 / 每个功能有验收标准 / 优先级标注 / 评审官签收 / CONTEXT.md已更新 |
| 2. 架构 | 技术选型有对比理由 / API设计完整 / 数据模型完整 / 安全措施列出 / 高风险点标注 / 评审官签收 / CONTEXT.md已更新 |
| 5. 任务分解 | 每个任务有明确输入输出 / 依赖关系无环 / 每个任务有验收标准 / P0任务100%覆盖 / 评审官签收 |
| 6. 开发 | 代码编译通过 / 单元测试通过 / lint无error / 安全扫描0严重问题 / reviewer审查完成 |
| 8. 测试 | test-plan中P0测试100%执行 / P0功能通过率100% / 无未解决P0缺陷 / 报告格式合规 |
| 9. 验收 | 7项验收标准全部✅ / 端到端旅程走通 / 经验教训已沉淀 |

---

## 测试层级（L1/L2/L3）

测试金字塔原则：底层多、顶层少，快速反馈优先。

| 层级 | 类型 | 谁写 | 数量占比 | 运行时间 | 覆盖目标 |
|------|------|------|---------|---------|---------|
| L1 | 单元测试 | 开发 | ~70% | <1min | 核心逻辑、工具函数、数据处理 |
| L2 | 集成测试 | 开发+QA | ~20% | <5min | 模块交互、API调用、数据流 |
| L3 | E2E测试 | QA | ~10% | <15min | 关键用户旅程、跨模块端到端 |

**QA 职责调整：** L3 E2E + L2 集成测试编写 + 审查开发写的 L1 单元测试覆盖率。

### Flaky Test 处理

- 测试失败后自动重跑1次，两次都失败才标记为真失败
- 重跑通过则标记为 `flaky`，记录在 test-report.md 问题清单中（不影响通过判定）
- 同一测试被标记 `flaky` ≥3次 → 自动降级为 `skip`，标注为 P1 技术债
- QA 评审官在阶段8审查时确认 flaky 标记合理性

---

## Shift-Left QA

QA 在阶段1.5和2.5即前置参与，而非等到阶段5：

| 交叉评审阶段 | QA 新增评审维度 |
|------------|---------------|
| 1.5 PRD交叉评审 | **可测性评审**：每个P0功能是否有明确验收标准？是否可自动化测试？测试数据如何准备？ |
| 2.5 架构交叉评审 | **测试基础设施评估**：架构是否支持测试隔离？mock能力？测试数据管理？**安全设计评审**：是否有RBAC/ABAC设计？权限边界定义？ |

---

## 安全扫描假阳性处理

安全扫描结果中每条问题可由 QA 评审官标记为 `confirmed` 或 `false-positive`（需附理由）。`false-positive` 标记需架构评审官复核。🟢小型项目无独立架构评审官，`false-positive` 由协调者复核（避免QA评审官自我审核）。验收标准改为"0 confirmed 严重问题"而非"0严重问题"。

---

## Human-in-the-Loop 关键决策点

以下决策点**必须等待用户确认**，协调者不可自行决定：

| 决策点 | 触发条件 | 用户选项 | 默认超时处理 |
|--------|---------|---------|------------|
| 合同 escalated | 轮次超限 | 继续签约 / 回退 / 终止 | 24h后默认回退，每6h提醒 |
| 回退额度耗尽 | 累计5次回退 | 终止 / 重置额度 / 降级 | 24h后默认终止 |
| Spike失败 | 同一技术点2次失败 | 换方案 / 降需求 / 终止 | 12h后默认换方案 |
| 安全扫描严重问题 | 0容忍不通过 | 修复 / 标记误报 / 终止 | 无超时，必须处理 |
| 项目规模重判定 | 任何阶段触发 | 确认新规模 / 维持原判定 | 6h后默认确认 |

**升级终止墙：** 任何升级决策点累计等待72h用户未响应 → 自动执行该决策点的默认处理（不终止整个项目）。72h为项目级累计值，从首次升级时间戳开始计算（`_config.json` 的 `first_escalation_at` 字段记录），覆盖所有升级决策点的总等待时间。已响应的决策点不受影响。`_config.json` 中 `escalations` 数组记录每个决策点的 `escalated_at`/`resolved_at`。若所有决策点均超时未响应且累计>72h → 项目自动终止并归档。

非清单中的决策点，协调者可自主决定，不等用户。

---

## 评审迭代 Self-Reflection

评审从第2轮开始，双方必须增加反思段落，避免低效循环：

- **评审官**：增加"上一轮反思"段落——上轮提出的问题是否已解决？是否有新问题？自己的上轮评审是否过度严苛？
- **执行者**：增加"变更摘要"段落——相对上一版的具体改动、为什么这些改动能解决上轮问题、是否引入新风险

---

## 回退幂等性与补偿事务

### 阶段交付幂等性

重做某阶段前，先清理该阶段产出目录（移到 `.contracts/{project}/_rollback-backup/phase-N-timestamp/`），再创建空目录。重执行等价于首次执行，保证幂等。

### 断路器：连续同因回退熔断

连续2次回退的根因相同 → 第3次同因回退直接触发熔断：跳过回退目标阶段，升级到协调者+用户决策（等价于回退额度耗尽的复盘流程）。

**同因判定结构化：** 回退记录 `changes/rollback-*.md` 中必须包含 `root_cause_category` 字段，从预定义枚举中选：`architecture-mismatch`、`prd-omission`、`tech-feasibility`、`performance`、`implementation-error`。`contract-check.sh` 按 `root_cause_category` 统计连续同因次数，达到2次 warning，3次强制熔断（exit 1）。

### 补偿事务

回退触发者必须列出"需要回滚的副作用"清单（git分支、数据库变更、部署产物等）。协调者执行补偿动作（git revert、数据库回滚脚本、环境清理）。补偿失败则：(1) 回滚前已创建当前状态快照在 `_rollback-backup/`；(2) 协调者生成手动回滚操作指引给用户；(3) 用户可选择"强制标记已补偿"（确认已知不一致）或"终止项目"。在 `changes/rollback-*.md` 中增加"compensation"段落记录补偿操作及结果，状态为 `completed/partial/failed`。

**补偿事务脚本验证：** `pipeline-check.sh` 在回退后、下游阶段开始前，检查最近一条回退记录的 `compensation` 段落状态：`completed` → 继续；`partial` → 允许用户"强制标记已补偿"后继续（写入审计记录）；`failed` 或缺失 → exit 1 阻断，防止回退后状态不一致继续执行。

---

## 流水线系统自身测试策略

流水线是一个复杂的状态机+多agent协调系统，必须有独立的测试策略。

### 单元测试（覆盖脚本和状态机逻辑）

| 测试对象 | 覆盖内容 | 测试数据 |
|---------|---------|---------|
| contract-check.sh | 每个合同状态转换（含非法转换exit 1）、轮次超限、回退计数、root_cause_category统计 | `tests/fixtures/index-*.json` 各种状态组合 |
| pipeline-check.sh | 每阶段DoD检查、行数阈值、required_sections、代码目录检查、产出物消毒 | `tests/fixtures/phase-*/` 合规/不合规产出物样本 |
| review-check.sh | 检查点计数（列表项格式）、角色段落数、评分格式 | `tests/fixtures/review-*.md` |
| security-scan.sh | 10类扫描的true positive/false positive样本 | `tests/fixtures/insecure-code/` |
| acceptance-check.sh | 7项验收标准各种组合 | `tests/fixtures/acceptance-*.json` |

### 集成测试（覆盖多组件协作）

| 场景 | 测试内容 |
|------|---------|
| 合同生命周期 | 创建→提交→打回→修改→签收→reopened→closed |
| 回退流程 | 触发→影响范围标注→stale标记→重执行→恢复 |
| MCP降级 | MemPalace不可用→本地备份→重试→恢复 |
| 多项目并发 | 抢占→paused→恢复→继续执行→死锁检测 |
| 补偿事务 | 补偿成功→completed→继续；补偿失败→failed→阻断 |

### E2E测试（模拟完整流水线）

| 场景 | 规模 | 特殊路径 |
|------|------|---------|
| small 项目完整流程 | small | 最少阶段，轻量冒烟 |
| medium 项目含回退 | medium | 触发1次回退，验证stale+重执行 |
| large 项目完整流程 | large | Spike+交叉评审+3开发并发 |
| 用户干预 | medium | 暂停→恢复→单阶段重试→跳过 |

### Mock策略

**必须mock（外部依赖）：** LLM API调用（sessions_send/spawn响应）、MemPalace MCP工具、时间函数（测试时限和72h终止墙）

**不能mock（核心逻辑）：** 脚本检查逻辑、合同状态机转换、文件系统操作（可用临时目录）

**可选mock：** agent产出内容（用预定义Markdown文件，各种合规/不合规样本）

### 测试数据构造

- `tests/fixtures/`：每阶段合规/不合规产出物样本、各种状态的_index.json样本、各种规模的_config.json样本
- `tests/helpers/setup-project.sh`：接受参数（规模、当前阶段、回退次数、escalated状态），自动构造对应状态的测试项目
- `tests/helpers/mock-agent-response.sh`：返回指定阶段的预定义agent响应
