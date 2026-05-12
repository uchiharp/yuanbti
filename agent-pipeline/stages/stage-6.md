# 阶段6：开发执行

## 任务
协调者按任务清单逐个 dispatch 开发 agent，每个任务一次 acpx 调用。QA 同步写 E2E 测试脚本。

## 必读文件（协调者）
1. docs/ARCHITECTURE.md
2. TASK-LIST.md
3. api-schema.md（阶段5.5产出）

## 加载 Skill
| 角色 | Skill |
|------|-------|
| 开发 | `code-quality-guard`, `logging-exception` |
| QA（并行） | `qa-workflow` |

## 执行流程

协调者只需调一行命令，脚本自动完成所有调度：

```bash
bash /Users/sunwenyong/.openclaw/agents/agent-pipeline/scripts/run-stage-6.sh {项目名} {项目目录}
```

脚本自动：
1. 解析 TASK-LIST.md，提取所有任务和依赖关系
2. 创建 6/progress.json 追踪完成状态
3. 按依赖顺序逐个 dispatch（依赖完成才 dispatch 下一个）
4. 每个任务失败自动重试 1 次
5. 输出最终执行报告

### 进度追踪

6/progress.json 格式：
```json
{
  "completed": ["T-001", "T-002"],
  "failed": ["T-003"]
}
```

脚本自动维护，支持中断后继续执行（跳过已完成任务）。

## 产出物
| 文件 | 说明 |
|------|------|
| 6/ 代码文件 | 按任务清单逐任务产出 |
| 6/progress.json | 任务完成进度 |
| 6/task-reports/{task_id}.md | 每个任务的产出摘要（含完成内容、文件清单、验收标准确认） |
| 6/dev-log.md | 开发日志（每个任务追加） |
| tests/ 测试脚本 | QA 同步产出 Playwright E2E |

## 测试要求（开发写）
- 单元测试 → `tests/unit/{task_id}/`（每个任务独立目录）
- 基础集成测试 → `tests/integration/`
- mock 比例 ≤ 50%，核心业务逻辑禁止 mock
- 每个 test case 至少 1 个有效断言
- 写完立刻跑测试，不通过当场修
- 单元测试由 dispatch-task.sh 自动执行验证

## QA E2E 测试（阶段6并行）
QA 在开发执行的同时编写 E2E 测试脚本：
- E2E 测试 → `tests/e2e/`
- 工具：Playwright（首次使用前运行 `check-test-tools.sh` 检查安装）
- QA 写完 E2E 脚本后，进入阶段7-test-review 做交叉审查

## 前置方案审查（强制）
开发过程中如果发现前面阶段的方案有问题、有 bug、有遗漏：
1. **能自行判断的** → 直接补全修复，不要等
2. **无法判断如何处理的** → 立即中断，询问用户
3. **修改了实现逻辑的** → 通知对应文档的负责人，按实际实现逻辑重新修改文档（ARCHITECTURE.md / api-schema.md / TASK-LIST.md 等）

## 检查项（脚本强制）
- [ ] 6/ 目录存在且含代码文件
- [ ] tests/ 目录存在且含测试文件
- [ ] progress.json 存在且 completed 非空
- [ ] 代码遵循分层架构（Controller 不直接引用 Repository）
- [ ] 每个 P0 任务验收标准逐条通过

## 约束
- 单任务超时：2小时（dispatch-task.sh 内置）
- 单任务最大轮次：50轮
- 失败重试：1次
- 重试仍失败 → 中断，询问用户
- ❌ 禁止只看任务描述就直接写代码
- ❌ 禁止在此阶段写 E2E 测试（QA 负责）
