# 阶段7：代码审查（架构师 + QA + PM）

## 前置条件
测试交叉审查（stage-7-test-review）必须通过。未通过则不能进入本阶段。

## 任务
架构师做架构合规验证，QA 做业务+健壮性验证，PM 做需求覆盖验证。开发修改后，审查者复审确认。

## 必读文件

### 架构师
1. dev/ 代码
2. （ARCHITECTURE.md 由你在阶段2产出，同 session 上下文已知，无需重读）

### QA
1. dev/ 代码
2. 7/test-reviews/ 测试审查报告（stage-7-test-review 产出）

### PM
1. dev/ 代码
2. PRD.md（验证需求覆盖）

## 加载 Skill
| 角色 | Skill |
|------|-------|
| 架构师 | `code-review-checklist`, `logging-exception` |
| QA | `qa-workflow`, `humanize-code`, `logging-exception` |
| PM | — |

## 各角色审查维度
| 角色 | 审查视角 |
|------|---------|
| 架构师 | 分层合规、模块隔离、模式使用、日志异常规范、逻辑 bug |
| QA | 业务逻辑、健壮性、去AI味、测试审查报告验证、逻辑 bug |
| PM | PRD 需求覆盖、功能完整性、优先级合理性、逻辑 bug |
| 开发2 | 代码质量：命名规范、重复代码、技术债、逻辑 bug |

## 执行流程

### 第一步：逐任务审查（自动化）
每个审查者调用 run-review.sh，自动对每个已完成任务做代码审查：

```bash
bash agent-pipeline/scripts/run-review.sh {项目名} {reviewer-id} {项目目录}
# reviewer-id: architect, qa, pm, dev2
```

脚本自动：
1. 读取 6/progress.json 获取所有已完成任务
2. 逐个任务读取 6/task-reports/{task_id}.md + 对应代码
3. 对照验收标准逐条检查
4. 产出 7/task-reviews/{task_id}.md
5. 做跨任务集成审查
6. 汇总 7/review-report.md

### 第二步：开发修改
开发根据审查意见修改代码。每个审查者的问题逐条修复。

### 第三步：审查者复审（第2轮）
三个角色确认各自提出的问题已修复，产出 re-review-code.md。

复审检查项：
- 架构师：之前提出的问题是否已修复，是否引入新问题
- QA：单元测试/集成测试是否已补充，E2E 测试是否已调整
- PM：需求覆盖是否完整，功能是否符合 PRD

### 第四步：推进
- 复审通过 → 推进阶段 8
- 仍有问题 → 开发再改（第3轮，最多 3 轮）
- 超过 3 轮 → 升级用户决策

## 产出物
| 文件 | 说明 |
|------|------|
| review-report.md | 架构师、QA、PM 各有独立段落，每段 ≥3检查点 + ≥1建议 + 评分 |
| re-review-code.md | 三个角色复审确认 |
| screenshots/ | Playwright 截图 ≥1张 |

## 约束
- 总轮次 ≤3（初审 + 复审算 1 轮）
- 超限 → escalated → 协调者汇报用户
- 通过 → 推进阶段 8
