# Pipeline 流程总览（合并版）

> 合并自 SCRIPT-SKILL-FLOW.md + skill-registry.md + PIPELINE-V2-OPTIMIZATION.md

---

## 一、Pipeline V2 优化说明


# Agent Pipeline v2 增强方案

> 优化日期：2026-05-17
> 状态：已实施

## 变更概述

将旧的阶段3 UX / 3.5 UX→UI交接 / 4 UI / 4.5 UI→UX反向 替换为新的 1.7/1.8/1.9 流程，实现 UI/UX 设计前置到 PRD 确认后、PRD 反向细化闭环。

## 旧流程 → 新流程

| 旧阶段 | 问题 | 新阶段 | 改进 |
|--------|------|--------|------|
| 3. UX设计 | 在架构设计后才做UX，容易返工 | 1.7 UI/UX设计 | PRD确认后立即设计，避免架构返工 |
| 3.5 UX→UI交接 | UX/UI割裂，交接成本高 | 合并到1.7 | 一体化设计，单agent完成 |
| 4. UI设计 | 延迟到架构后，交互需求不明确 | 合并到1.7 | 设计前置，驱动架构 |
| 4.5 UI→UX反向 | 仅确认，无细化 | 1.8 PRD反向细化 | 4维度细化，产出强化版PRD |
| — | 无用户确认节点 | 1.9 细化PRD确认 | 人工确认细化后的PRD |

## 新流程时序

```
阶段1 PM→PRD
  → 阶段1.5 PRD交叉评审
    → 阶段1.6 PRD用户审阅
      → 阶段1.7 UI/UX设计（8维度技术特性分析 + HTML原型）
        → 阶段1.8 PRD反向细化（交互细节/边界/文案/异常）
          → 阶段1.9 细化PRD人工确认
            → 阶段2 架构设计（基于细化PRD）
```

## 功能点标签状态机

```
PRD-待确认 → PRD-已确认 → UI/UX-设计中 → UI/UX-设计完成
    → PRD-已细化 → PRD-细化确认 → 技术方案-待确认 → 技术方案-已确认
    → 开发-进行中 → 开发-完成 → 测试-通过 → 验收-通过 → 交付-完成
```

## 新增 Skill 清单

| Skill | 路径 | 用途 |
|-------|------|------|
| ui-ux-design | skills/ui-ux-design/SKILL.md | UI/UX设计执行规范，含8维度分析框架 |
| prd-refinement | skills/prd-refinement/SKILL.md | PRD反向细化方法论 |
| feature-tagging | skills/feature-tagging/SKILL.md | 功能点标签系统规范 |
| interactive-html | skills/interactive-html/SKILL.md | HTML原型生成规范 |
| engineering-robustness | skills/engineering-robustness/SKILL.md | 工程健壮性检查 |

## 新增 Stage 清单

| Stage | 路径 |
|-------|------|
| 1.6 PRD用户审阅 | stages/stage-1.6.md |
| 1.7 UI/UX设计 | stages/stage-1.7.md |
| 1.8 PRD反向细化 | stages/stage-1.8.md |
| 1.9 细化PRD确认 | stages/stage-1.9.md |

## 修改文件清单

| 文件 | 变更 |
|------|------|
| PRD.md | 规模表/流程图/角色表/阶段定义/产出路径/DoD/YAML配置 全部替换3/3.5/4/4.5为1.6/1.7/1.8/1.9 |
| ARCHITECTURE.md | 模型路由/交叉评审角色 清理旧ux-tester/ui-designer引用 |
| scripts/dispatch.sh | 添加1.7/1.8/1.9阶段名称/NEXT_CMD/角色映射/ui-ux-designer角色/标签更新指令 |
| config/pipeline-stages.conf | 删除3/3.5/4/4.5产出配置，1.7/1.8/1.9已有 |
| config/stage-skills.conf | 删除3/3.5/4/4.5 skill映射，1.7/1.8/1.9已有 |

## 已删除的旧阶段文件（保留但不再调度）

- stages/stage-3.md（UX设计）
- stages/stage-3.5.md（UX→UI交接）
- stages/stage-4.md（UI设计）
- stages/stage-4.5.md（UI→UX反向）

这些文件保留作为参考，但 dispatch.sh 不再调度它们。


---

## 二、脚本-Skill 穿插执行流程


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


---

## 三、Skill 注册表


# Skill 注册表 — 每阶段加载哪些 Skill

协调者调度 agent 时，必须按此表加载对应 Skill。**不在表中的阶段不需要加载 Skill。**

## 注册表

| 阶段 | 角色 | 必加载 Skill | 可选 Skill |
|------|------|-------------|-----------|
| 0 | 协调者 | — | — |
| 1 | PM | `requirements-analysis` | — |
| 1.6 | PM | — | — |
| 1.5 | QA + 开发 + 架构师 | — | — |
| **1.7** | **UI/UX 设计师** | **`ui-ux-design`, `feature-tagging`** | **—** |
| **1.8** | **PM** | **`prd-refinement`, `feature-tagging`** | **—** |
| **1.9** | **协调者** | **`feature-tagging`** | **—** |
| 2 | 架构师 | `tech-architecture`, `logging-exception` | — |
| 2.5 | 开发 + QA + PM | `architecture-review` | — |
| 2.6 | 架构师 | — | — |
| 2.8 | Spike agent | `tech-spike` | — |
| 3 | UX 设计师 | — | — |
| 3 | PM | — | — |
| 3.5 | UI 设计师 | — | — |
| 4 | UI 设计师 | — | — |
| 4 | PM + 开发 | — | — |
| 4.5 | UX | — | — |
| 5 | 协调者 | `task-decomposition` | — |
| 5 | QA | `qa-workflow` | — |
| 5.5 | 开发 | — | — |
| 6 | 开发 | `code-quality-guard`, `logging-exception` | `humanize-code` |
| 6 | QA（并行） | `qa-workflow` | — |
| 6.5 | 架构师 | `code-review-checklist` | — |
| 7 | 架构师 | `code-review-checklist`, `logging-exception` | — |
| 7 | QA | `qa-workflow`, `humanize-code`, `logging-exception` | — |
| 7 | PM | — | — |
| 8 | QA | `qa-workflow` | — |
| 8 | PM | — | — |
| 8.5 | PM | — | — |
| 9 | 协调者 | — | — |

> **加粗行**为本次新增阶段

## Skill 用途速查

| Skill | 用途 | 使用阶段 |
|-------|------|---------|
| `requirements-analysis` | 需求分析方法论 | 1 |
| **`ui-ux-design`** | **UI/UX 设计方法论（技术特性分析 + HTML 原型生成）** | **1.7** |
| **`prd-refinement`** | **PRD 反向细化（交互/边界/文案/异常）** | **1.8** |
| **`feature-tagging`** | **功能点标签系统（全流程打标）** | **1.7, 1.8, 1.9, 6, 8, 8.5, 9** |
| `tech-architecture` | 架构设计方法论（含设计模式、DDD、日志异常架构） | 2 |
| `architecture-review` | 架构审查（12维度打分红黄绿 + AI味检测） | 2.5 |
| `tech-spike` | 技术可行性验证 | 2.8 |
| `task-decomposition` | 任务拆分方法论 | 5 |
| `qa-workflow` | 测试计划/执行/调试 | 5, 6, 7, 8 |
| `code-quality-guard` | 编码质量检查（含命名/格式/注释/Git规范） | 6 |
| `code-review-checklist` | 代码审查维度（含SOLID、设计模式检查） | 6.5, 7 |
| `humanize-code` | 去AI味检查 | 7 |
| `logging-exception` | 日志/异常/错误处理架构 | 2, 6, 7 |
| `engineering-robustness` | 工程健壮性规范 | 2, 6, 6.3, 7 |
| `interactive-html` | 交互式 HTML 文档生成 | 10 |

## 强制规则

1. **必须按表加载** — 不能跳过必加载 Skill
2. **不能自创 Skill** — 不在表中的 Skill 不能代替必加载的
3. **Skill 加载后必须读 SKILL.md** — 不是"知道有这个 Skill"就行，要实际读取内容
4. **必读文件必须先读** — 每个阶段文件的「必读文件」比 Skill 更优先
5. **`feature-tagging` 贯穿全流程** — 在所有标签变更节点必须加载并执行

## 检查点缺口（待实现）

以下检查点在 Skill 中定义但 Pipeline 尚未强制执行：

| # | 检查点 | 来源 Skill | 缺口位置 | 建议动作 |
|---|--------|-----------|---------|---------|
| 1 | 接口契约锁定 | `task-decomposition` | Stage 5 无子步骤 | Stage 5 开始前先锁接口契约，签字后再拆任务 |
| 2 | REQ 可追溯矩阵 | `qa-workflow` | Stage 8 无检查 | Stage 8 硬门：矩阵缺失或有未测 REQ 则拒绝 |
| 3 | 错误码一致性 | `logging-exception` | Stage 7 无验证 | Stage 7 用 grep 检查架构文档错误码是否出现在代码中 |
| 4 | Spike 部分成功回退 | `tech-spike` | 只有成功/失败路由 | 部分成功 → 条件回退 Stage 2 做针对性架构调整 |
| 5 | 设计模式表检查 | `tech-architecture` | Stage 2.5 无验证 | Stage 2.5 检查架构师是否产出了设计模式选型表 |
