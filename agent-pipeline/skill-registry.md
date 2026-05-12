# Skill 注册表 — 每阶段加载哪些 Skill

协调者调度 agent 时，必须按此表加载对应 Skill。**不在表中的阶段不需要加载 Skill。**

## 注册表

| 阶段 | 角色 | 必加载 Skill | 可选 Skill |
|------|------|-------------|-----------|
| 0 | 协调者 | — | — |
| 1 | PM | `requirements-analysis` | — |
| 1.6 | PM | — | — |
| 1.5 | QA + 开发 + 架构师 | — | — |
| 2 | 架构师 | `tech-architecture`, `logging-exception` | — |
| 2.5 | 开发 + QA + PM | — | — |
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
| 6 | 开发 | `code-quality-guard`, `logging-exception` | — |
| 6 | QA（并行） | `qa-workflow` | — |
| 6.5 | 架构师 | `code-review-checklist` | — |
| 7 | 架构师 | `code-review-checklist`, `logging-exception` | — |
| 7 | QA | `qa-workflow`, `humanize-code`, `logging-exception` | — |
| 7 | PM | — | — |
| 8 | QA | `qa-workflow` | — |
| 8 | PM | — | — |
| 8.5 | PM | — | — |
| 9 | 协调者 | — | — |

## Skill 用途速查

| Skill | 用途 | 使用阶段 |
|-------|------|---------|
| `requirements-analysis` | 需求分析方法论 | 1 |
| `tech-architecture` | 架构设计方法论（含设计模式、DDD、日志异常架构） | 2 |
| `tech-spike` | 技术可行性验证 | 2.8 |
| `task-decomposition` | 任务拆分方法论 | 5 |
| `qa-workflow` | 测试计划/执行/调试 | 5, 6, 7, 8 |
| `code-quality-guard` | 编码质量检查（含命名/格式/注释/Git规范） | 6 |
| `code-review-checklist` | 代码审查维度（含SOLID、设计模式检查） | 6.5, 7 |
| `humanize-code` | 去AI味检查 | 7 |
| `logging-exception` | 日志/异常/错误处理架构 | 2, 6, 7 |

## 强制规则

1. **必须按表加载** — 不能跳过必加载 Skill
2. **不能自创 Skill** — 不在表中的 Skill 不能代替必加载的
3. **Skill 加载后必须读 SKILL.md** — 不是"知道有这个 Skill"就行，要实际读取内容
4. **必读文件必须先读** — 每个阶段文件的「必读文件」比 Skill 更优先
