# 脚本-Skill 穿插执行流程

> **阶段详细指令在 `stages/stage-X.md`，协调者调度时只发对应阶段文件给 agent。**
> **Skill 注册表在 `skill-registry.md`，每阶段加载哪些 Skill 必须按表执行。**

## 执行模型

```
pipeline-run.sh（主控脚本，每阶段驱动）
  │
  ├── 1. 读取 stages/stage-X.md → 输出任务指令给 agent
  ├── 2. 按 skill-registry.md 加载对应 Skill
  ├── 3. 等待 agent 完成（协调者轮询产出物）
  ├── 4. 执行 pipeline-check.sh（验证产出物合规）
  │     ├── 通过 → 推进下一阶段
  │     └── 不通过 → 输出缺失项 → 打回重做（轮次+1）
  ├── 5. 执行 feature-tags.sh（更新功能点标签状态）
  └── 6. 调度子脚本（按阶段）
      ├── review-check.sh（阶段6.5/7）
      ├── contract-check.sh（阶段7/9）
      ├── test-report-check.sh（阶段8）
      └── acceptance-check.sh（阶段9）
```

**脚本管"做什么、做多少、做对了没"，skill 管"怎么做好"。**
**stages/ 管"每阶段具体指令"，本文档只管"阶段间关系"。**

---

## 阶段总览

| 阶段 | 名称 | 角色 | 产出物 | 最低行数 | 合同 | 功能点标签 |
|------|------|------|--------|---------|------|-----------|
| 0 | 启动 | 协调者 | PROJECT-PLAN.md | 30 | — | — |
| 1 | 需求分析 | PM | PRD.md | 200 | 🟡 2轮 | PRD-待确认 |
| 1.5 | PRD交叉评审 | 各角色 | cross-review-pm.md | 50 | — | — |
| 1.6 | PRD用户审阅 | PM+用户 | prd-feedback.md | 10 | — | PRD-已确认 |
| **1.7** | **UI/UX设计** | **UI/UX设计师** | **UI-UX-DESIGN.md + ui-prototype.html** | **120+200** | **🟡 2轮** | **UI/UX-设计完成** |
| **1.8** | **PRD反向细化** | **PM** | **PRD-REFINED.md + prd-diff.md** | **300+50** | **🟡 2轮** | **PRD-已细化** |
| **1.9** | **细化PRD确认** | **PM+用户** | **prd-refinement-feedback.md** | **10** | **—** | **PRD-细化确认** |
| 2 | 架构设计 | 架构师 | ARCHITECTURE.md | 100 | 🟡 2轮 | 技术方案-待确认 |
| 2.5 | 架构交叉评审 | 各角色 | cross-review-arch.md | 40 | — | 技术方案-已确认 |
| 2.6 | 架构用户确认 | 用户 | architecture-feedback.md | 10 | — | — |
| 2.8 | 技术Spike | Spike | SPIKE-REPORT.md | 30 | 4h | — |
| 3 | UX设计 | UX | UX-DESIGN.md | 80 | 🟡 2轮 | — |
| 3.5 | UX→UI交接 | UI | cross-review-ux-to-ui.md | 20 | — | — |
| 4 | UI设计 | UI | UI-DESIGN.md | 80 | 🟡 2轮 | — |
| 4.5 | UI→UX确认 | UX | cross-review-ui-to-ux.md | 20 | — | — |
| 5 | 任务分解 | 协调者+QA | TASK-LIST.md + test-plan.md | 50+30 | 🟡 2轮 | — |
| 5.5 | 分解确认 | 开发 | confirm-tasks.md | 20 | — | — |
| 6 | 开发执行 | 开发+QA | 代码 + 测试脚本 | — | 🔴 3轮 | 开发-进行中/完成 |
| 6.3 | 代码集成 | 开发 | 集成后代码 + 冒烟结果 | — | — | — |
| 6.5 | 架构审查 | 架构师 | cross-review-dev.md | 60 | — | — |
| 7 | 代码审查 | 架构师+QA | review-report.md + 截图 | — | 🔴 3轮 | — |
| 7-test-review | 测试交叉审查 | QA | test-review-report.md | — | — | — |
| 8 | 测试验证 | QA | test-report.md + 截图 | 50 | 🔴 3轮 | 测试-通过/失败 |
| 8.5 | PM验收 | PM | pm-acceptance.md | 30 | 🟡 2轮 | 验收-通过 |
| 9 | 交付验收 | 协调者 | ACCEPTANCE-REPORT.md + 交付文档 | 50 | — | 交付-完成 |

> **加粗行**为本次新增阶段（1.7/1.8/1.9）

---

## 阶段间流程

```
0 → 1 → 1.5(🟡/🔴) → 1.6 → 1.7(🟡/🔴) → 1.8(🟡/🔴) → 1.9(🟡/🔴)
    → 2 → 2.5 → [2.8(有高风险)] → 3 → 3.5 → 4 → 4.5 → 5 → 5.5
    → 6 → 6.3 → 6.5 → 7-test-review → 7 → 8 → 8.5 → 9 → 10
```

**新增阶段位置说明：**
- **阶段 1.7**（UI/UX 设计）：PRD 确认后、架构设计前
- **阶段 1.8**（PRD 反向细化）：UI/UX 设计完成后，细化 PRD
- **阶段 1.9**（细化 PRD 确认）：人工确认细化 PRD 后，流入架构设计

**规模裁剪：**
- 🟢 小型：跳过 1.5, 1.7, 1.8, 1.9, 2.5, 3.5, 4.5, 5.5, 6.3, 6.5
- 🟡 中型：跳过 2.8（除非有高风险标记），**执行 1.7, 1.8, 1.9**
- 🔴 大型：全阶段执行

**回退规则：**
- 任何阶段发现上游问题 → 记录到 changes/ → 回退到目标阶段
- 总回退 ≤5次，同阶段连续回退 ≤2次
- 超限 → 暂停项目，需用户复盘

---

## 功能点标签流转

每个 REQ-xxx 功能点在 Pipeline 中自动打标：

```
PRD-待确认 → PRD-已确认 → UI/UX-设计中 → UI/UX-设计完成
    → PRD-已细化 → PRD-细化确认 → 技术方案-待确认 → 技术方案-已确认
    → 开发-进行中 → 开发-完成 → 测试-通过 → 验收-通过 → 交付-完成
```

标签存储在 `pipeline/feature-tags.json`，由 `feature-tags.sh` 自动维护。

---

## 脚本-Skill 职责分界

| 管什么 | 谁管 | 怎么管 |
|--------|------|--------|
| 阶段顺序和跳转 | 脚本 | pipeline-run.sh case 语句 + 规模裁剪表 |
| 产出物名称和路径 | 脚本 | stages/stage-X.md 中指定 |
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
| docs/ 归档 | 脚本 | pipeline-check.sh 检查文件存在性 |
| 交付文档齐全 | 脚本 | pipeline-check.sh 检查4文档+行数+关键词 |
| 分层架构合规 | 脚本 | pipeline-check.sh 检查 Controller 不引用 Repository |
| 架构审查引用 | 脚本 | pipeline-check.sh 检查审查报告引用架构文档 |
| **功能点标签状态** | **脚本** | **feature-tags.sh 自动打标 + 一致性检查** |
| **怎么做好 UI/UX 设计** | **Skill** | **ui-ux-design 设计方法论** |
| **怎么细化 PRD** | **Skill** | **prd-refinement 反向细化方法论** |
| **怎么管理功能点标签** | **Skill** | **feature-tagging 标签系统** |
| **怎么写好PRD** | Skill | requirements-analysis 方法论 |
| **怎么做好架构设计** | Skill | tech-architecture 方法论 |
| **怎么验证技术可行性** | Skill | tech-spike 方法论 |
| **怎么拆好任务** | Skill | task-decomposition 方法论 |
| **怎么写好测试** | Skill | qa-workflow 方法论 |
| **怎么审查代码** | Skill | code-review-checklist 维度清单 |
| **怎么保证编码质量** | Skill | code-quality-guard 规范 |
| **怎么去AI味** | Skill | humanize-code 检查方法 |
| **日志/异常/错误处理** | Skill | logging-exception 架构规范 |
| **怎么和用户讨论** | Skill | Brainstorm 讨论规则 |
| **审查怎么挑毛病** | SKILL.md | 思维模式定义（魔鬼代言人等） |
| **规模判定** | 协调者 | 需要判断力，脚本只读取判定结果 |
| **MemPalace 存取** | 协调者 | 需要 MCP 工具，脚本无法直接调用 |

---

## 脚本调用链

```
pipeline-run.sh <项目目录> <阶段号>
│
├── lib.sh（共享函数库，所有脚本 source）
│
├── 阶段0-1.6：直接检查（文件+行数+知识库+沟通记录）
│
├── 阶段1.7：UI/UX 设计检查
│   ├── check_file（UI-UX-DESIGN.md ≥120行）
│   ├── check_file（docs/ui-prototype.html ≥200行）
│   ├── check_html_interactive（HTML 非纯静态）
│   └── feature-tags.sh update（标签 → UI/UX-设计完成）
│
├── 阶段1.8：PRD 反向细化检查
│   ├── check_file（PRD-REFINED.md ≥300行）
│   ├── check_file（prd-diff.md ≥50行）
│   ├── check_prd_refinement_quality（4维度覆盖检查）
│   └── feature-tags.sh update（标签 → PRD-已细化）
│
├── 阶段1.9：细化 PRD 确认检查
│   ├── check_file（prd-refinement-feedback.md）
│   ├── check_no_pending_items（无残留 [待确认]）
│   └── feature-tags.sh confirm（标签 → PRD-细化确认）
│
├── 阶段2-5.5：同原有逻辑
│
├── 阶段6：
│   ├── check_code（代码文件+测试文件存在）
│   ├── check_layered_architecture（分层架构合规）
│   ├── check_input_references（必读文件引用）
│   └── feature-tags.sh update（按任务更新 开发-进行中/完成）
│
├── 阶段6.5/7：
│   ├── review-check.sh（评审报告格式）
│   ├── check_architecture_reference（架构引用检查）
│   └── check_input_references（必读文件引用）
│
├── 阶段7/9：
│   └── contract-check.sh（合同+回退次数）
│
├── 阶段8：
│   ├── test-report-check.sh（测试报告格式）
│   └── feature-tags.sh update（按 REQ 更新 测试-通过/失败）
│
├── 阶段8.5：
│   └── feature-tags.sh confirm（标签 → 验收-通过）
│
├── 阶段9：
│   ├── acceptance-check.sh + pipeline-check.sh（交付文档）
│   └── feature-tags.sh update（标签 → 交付-完成）
│
└── 每阶段：
    ├── check_knowledge()（CONTEXT.md 更新）
    ├── check_docs_archive()（阶段2起，docs/ 归档）
    └── feature-tags.sh summary（生成进度看板）
```

---

## 回退流程

```
发现上游问题 → 协调者决定回退
  → changes/ 创建回退记录
  → 脚本检查：总回退 ≤5，连续回退 ≤2
  → 调度对应角色修正
  → 对应角色复核（1轮）
  → 从目标阶段重新走检查
  → feature-tags.sh 回退对应 REQ 的标签
```

## 需求变更流程

```
用户提出变更 → 协调者判定类型
  🟢 小调整：当前阶段内部消化
  🟡 功能调整：PM更新PRD → 受影响角色修改 → 对应角色1轮复核 → 更新标签
  🔴 需求变更：回退到阶段1重走流程 → 重置标签
```
