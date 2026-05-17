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
