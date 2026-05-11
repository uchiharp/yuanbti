# 阶段5：任务分解 + QA 测试计划

## 任务
创业助手产出开发任务清单，QA 同步产出测试计划（并发）。

## 必读文件
1. PRD.md
2. ARCHITECTURE.md
3. UX-DESIGN.md / UI-DESIGN.md
4. CONTEXT.md

## 加载 Skill
| 角色 | Skill |
|------|-------|
| 创业助手 | `task-decomposition` |
| QA | `qa-workflow` |

## 产出物
| 文件 | 最低行数 | 角色 | 说明 |
|------|---------|------|------|
| TASK-LIST.md | 50 | 创业助手 | 开发任务清单（含批次/依赖/开发者分配） |
| test-plan.md | 30 | QA | 测试计划 |

## 执行流程
1. 协调者并发调度创业助手 + QA
2. 创业助手：加载 `task-decomposition`，和用户讨论拆分方式 → 产出 TASK-LIST.md
3. QA：加载 `qa-workflow`，产出 test-plan.md
4. 各自评审官审查 → 签收/打回（最多2轮）

## 检查项（脚本强制）
- [ ] TASK-LIST.md ≥50行
- [ ] test-plan.md ≥30行
- [ ] 两个评审报告 ≥3检查点 + 评分
- [ ] 合同轮次 ≤2
- [ ] TASK-LIST.md 包含批次/依赖/开发者分配信息

## 约束
- 合同：🟡中风险 标准合同 最多2轮
- Brainstorm：和用户讨论拆分方式、优先级、依赖
- 知识库：更新 CONTEXT.md 阶段5段落，存入 MemPalace room=task-breakdown
