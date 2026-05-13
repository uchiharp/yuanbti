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
| 架构师 | 分层合规、模块隔离、模式使用、日志异常规范、**工程健壮性设计落地**、逻辑 bug |
| QA | 业务逻辑、**健壮性（边界/并发/异常路径）**、去AI味、测试审查报告验证、逻辑 bug |
| PM | PRD 需求覆盖、功能完整性、优先级合理性、逻辑 bug |
| 开发2 | 代码质量：命名规范、重复代码、技术债、逻辑 bug |

## 工程健壮性审查清单（所有审查者共用）

**详细审查要点见 `engineering-robustness` SKILL.md（dispatch.sh 自动加载）。** 以下为检查清单：

- [ ] 前端防抖/节流：提交按钮 disabled、搜索 debounce、滚动 throttle、定时器清理
- [ ] 并发控制：乐观锁/分布式锁/幂等、无 TOCTOU 竞态
- [ ] 边界条件：空值校验、空集合、分页修正、字符串/数值/日期边界
- [ ] 超时配置：所有外部调用有显式超时、无 timeout=0
- [ ] 缓存：穿透/雪崩/击穿防护、Cache Aside 策略
- [ ] 限流：公开 API 有限流、超限 429、前端友好提示
- [ ] 文件上传：content-type + magic bytes、UUID 文件名、路径不可控
- [ ] 连接池：DB/Redis/HTTP 连接池显式配置
- [ ] 优雅降级：fallback 存在、重试有上限、死信队列
- [ ] 数据脱敏：日志/API/DB/前端敏感字段处理
- [ ] 幂等：创建有唯一约束、更新有乐观锁、回调有状态机

## 执行流程

### 第一步：安全扫描（架构师负责，最先执行）

代码审查前先跑安全扫描，发现问题优先修复：

```bash
bash agent-pipeline/scripts/security-scan.sh {项目目录}/6
```

**处理规则：**
- 🔴 严重问题（硬编码密钥、SQL注入、XSS、路径穿越）→ 必须修复，不通过不允许进阶段8
- 🟡 警告（CORS 通配符、日志敏感信息）→ 评估风险，可降级为后续修复
- 修复后重跑，直到 0 严重问题

**产出**：将扫描结果追加到 review-report.md 的架构师段落。

### 第二步：逐任务审查（自动化）
每个审查者调用 run-review.sh，自动对每个已完成任务做代码审查：

```bash
bash agent-pipeline/scripts/run-review.sh {项目名} {reviewer-id} {项目目录}
# reviewer-id: architect, qa, pm, dev2
```

脚本自动：
1. 读取 pipeline/6/progress.json 获取所有已完成任务
2. 逐个任务读取 pipeline/6/task-reports/{task_id}.md + 对应代码
3. 对照验收标准逐条检查
4. 产出 pipeline/7/task-reviews/{task_id}.md
5. 做跨任务集成审查
6. 汇总 7/review-report.md

### 第三步：开发修改
开发根据审查意见修改代码。每个审查者的问题逐条修复。

### 第四步：审查者复审（第2轮）
三个角色确认各自提出的问题已修复，产出 re-review-code.md。

复审检查项：
- 架构师：之前提出的问题是否已修复，是否引入新问题
- QA：单元测试/集成测试是否已补充，E2E 测试是否已调整
- PM：需求覆盖是否完整，功能是否符合 PRD

### 第五步：推进
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
