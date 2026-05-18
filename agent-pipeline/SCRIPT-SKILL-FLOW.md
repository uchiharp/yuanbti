# 脚本-Skill 穿插执行流程

> **阶段详细指令在 `stages/stage-X.md`，协调者调度时只发对应阶段文件给 agent。**
> **Skill 注册表在 `skill-registry.md`，每阶段加载哪些 Skill 必须按表执行。**

## 执行模型

```
协调者（主控，每阶段驱动）
  │
  ├── 1. 读取 stages/stage-X.md → 输出任务指令给 agent
  ├── 2. 按 skill-registry.md + stage-skills.conf 加载对应 Skill
  ├── 3. 等待 agent 完成（协调者轮询产出物）
  ├── 4. 执行 pipeline-check.sh（验证产出物合规）
  │     ├── 通过 → 推进下一阶段
  │     └── 不通过 → 输出缺失项 → 打回重做（轮次+1）
  ├── 5. 功能点标签由 agent 自动更新（feature-tags.json）
  └── 6. 调度子脚本（按阶段）
      ├── dispatch.sh（单阶段调度）
      ├── dispatch-task.sh（单任务粒度调度，阶段6）
      ├── run-stage-6.sh（阶段6 并发调度）
      ├── run-review.sh（阶段7 代码审查）
      └── run-test-review.sh（阶段7 测试审查）
```

**脚本管"做什么、做多少、做对了没"，skill 管"怎么做好"。**
**stages/ 管"每阶段具体指令"，本文档只管"阶段间关系"。**

---

## 阶段总览

| 阶段 | 名称 | 角色 | 产出物 | 最低行数 | 合同 | 功能点标签 |
|------|------|------|--------|---------|------|-----------|
| 0 | 启动 | 协调者 | PROJECT-PLAN.md | 20 | — | — |
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
| 10 | 交互式文档 | 协调者 | INTERACTIVE-DOC.html | 100 | — | — |

> **加粗行**为本次新增阶段（1.7/1.8/1.9）

---

## 阶段间流程

```
0 → 1 → 1.5(🟡/🔴) → 1.6 → 1.7(🟡/🔴) → 1.8(🟡/🔴) → 1.9(🟡/🔴)
    → 2 → 2.5 → [2.8(有高风险)] → 5 → 5.5
    → 6 → 6.3 → 6.5 → 7-test-review → 7 → 8 → 8.5 → 9 → 10
```

**新增阶段位置说明：**
- **阶段 1.7**（UI/UX 设计）：PRD 确认后、架构设计前
- **阶段 1.8**（PRD 反向细化）：UI/UX 设计完成后，细化 PRD
- **阶段 1.9**（细化 PRD 确认）：人工确认细化 PRD 后，流入架构设计

**规模裁剪：**
- 🟢 小型：跳过 1.5, 1.7, 1.8, 1.9, 2.5, 2.8, 5.5, 6.3, 6.5, 7-test-review
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

标签存储在 `pipeline/feature-tags.json`，由 agent 在每个阶段结束时自动更新（dispatch.sh prompt 中包含更新指令）。

---

## 脚本-Skill 职责分界

| 管什么 | 谁管 | 怎么管 |
|--------|------|--------|
| 阶段顺序和跳转 | 协调者 | 按 SCRIPT-SKILL-FLOW.md 流程推进 |
| 产出物名称和路径 | stage md | stages/stage-X.md 中指定 |
| 产出物最小行数 | 脚本 | pipeline-check.sh wc -l 对比阈值 |
| 评审检查点数量 | 脚本 | pipeline-check.sh grep 计数 |
| 回退次数限制 | 协调者 | 记录到 changes/，人工控制 |
| 24h时限 | 协调者 | 记录起始时间戳，对比当前时间 |
| 目录结构初始化 | 脚本 | mkdir -p 创建标准目录 |
| 安全扫描 | 脚本 | security-scan.sh 8类检查（如存在） |
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
协调者调度（手动或半自动）
│
├── dispatch.sh <项目名> <agent-id> <阶段号> <项目目录>
│   ├── 加载 stage-skills.conf → 注入 Skill
│   ├── 拼接 stage-X.md 内容 → 构建 prompt
│   └── 调用 dispatch-adapter.sh → dispatch_agent()
│
├── pipeline-check.sh <项目目录> <阶段编号> [--size small|medium|large]
│   ├── 读取 pipeline-stages.conf → 阶段产出物阈值
│   ├── check_file()（文件存在 + 行数达标）
│   ├── 各阶段专用检查函数（check_review/check_code/check_test 等）
│   └── 检查不通过 → 流程暂停
│
├── 阶段6 专用：
│   ├── run-stage-6.sh（并发调度 dev1/dev2/dev3）
│   │   ├── 解析 TASK-LIST.md → 依赖图
│   │   ├── 按依赖顺序 dispatch-task.sh
│   │   └── 进度追踪 → progress.json
│   └── dispatch-task.sh（单任务粒度，增量上下文）
│
├── 阶段7 专用：
│   ├── run-review.sh（逐任务代码审查）
│   └── run-test-review.sh（测试交叉审查）
│
└── 辅助脚本：
    ├── dispatch-adapter.sh（后端适配：claude/codex/openclaw）
    ├── session-health.sh（session 健康检查+恢复）
    ├── session-monitor.sh（session 状态面板）
    └── test-monitor.sh（测试期间错误监控）
```

---

## 回退流程

```
发现上游问题 → 协调者决定回退
  → changes/ 创建回退记录
  → 协调者检查：总回退 ≤5，连续回退 ≤2
  → 调度对应角色修正
  → 对应角色复核（1轮）
  → 从目标阶段重新走 pipeline-check.sh
  → agent 更新 feature-tags.json 回退对应 REQ 的标签
```

## 需求变更流程

```
用户提出变更 → 协调者判定类型
  🟢 小调整：当前阶段内部消化
  🟡 功能调整：PM更新PRD → 受影响角色修改 → 对应角色1轮复核 → 更新 feature-tags.json
  🔴 需求变更：回退到阶段1重走流程 → 重置 feature-tags.json
```
