# 阶段6：开发执行

## 任务
协调者按任务清单逐个 dispatch 开发 agent，每个任务一次调度。QA 同步写 E2E 测试脚本。

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
- 集成测试 → `tests/integration/`
- **集成测试禁止 mock 数据库/Redis/MQ**，必须连接 `docker-compose.test.yml` 启动的真实服务
- mock 仅允许用于外部第三方 API（支付、短信等不可控服务）
- 每个 test case 至少 1 个有效断言
- 写完立刻跑测试，不通过当场修
- 单元测试由 dispatch-task.sh 自动执行验证

## 工程健壮性实现要求（开发必须遵守）

**详细规范见 `engineering-robustness` SKILL.md（dispatch.sh 自动加载）。** 以下为检查清单：

### 检查项
- [ ] 所有提交按钮有防重复提交保护
- [ ] 搜索/滚动等高频操作有 debounce/throttle
- [ ] 写操作有并发控制（乐观锁/分布式锁/幂等）
- [ ] 每个 API 有边界条件测试（空值/空集合/溢出/并发冲突）
- [ ] 金额字段使用 BigDecimal（非 double/float）
- [ ] 日期处理有时区一致性
- [ ] 所有外部调用有显式超时配置
- [ ] 缓存有穿透/雪崩/击穿防护
- [ ] 公开 API 有限流配置
- [ ] 文件上传有类型/大小/路径校验
- [ ] 连接池已显式配置（不依赖默认值）
- [ ] 非核心依赖有降级/fallback
- [ ] 敏感字段有脱敏处理
- [ ] 写接口支持幂等

## 覆盖率自测（每个任务完成后必须）
开发完成每个任务后，必须验证覆盖率：

```bash
# 1. 启动测试环境
cd {项目目录} && docker-compose -f docker-compose.test.yml up -d
# 等待就绪...

# 2. 跑全部测试（单元 + 集成），JaCoCo/c8 自动收集覆盖率
cd {项目目录}/6 && mvn test  # 或 npm test

# 3. 检查覆盖率报告
# Java: target/site/jacoco/index.html
# Node: coverage/index.html

# 4. 清理
docker-compose -f docker-compose.test.yml down
```

**覆盖率阈值 95%**（阶段2架构师配置）。`mvn test` / `npm test` 低于 95% 直接失败，不允许提交。

## 测试日志监控（每次跑测试必须）

跑测试时必须捕获完整输出（stdout + stderr），失败时保留日志供排查：

```bash
# 单元测试日志
cd {项目目录}/6 && mvn test 2>&1 | tee logs/unit/T-{task_id}.log

# 集成测试日志
cd {项目目录}/6 && mvn verify 2>&1 | tee logs/integration/T-{task_id}.log
```

**要求：**
- 测试通过：日志保留，标记 `PASS`
- 测试失败：日志保留，标记 `FAIL`，**开发必须先看日志再修代码**，不要盲改
- 日志必须包含：失败用例名、错误堆栈、断言差异（expected vs actual）
- 日志目录：`logs/unit/`、`logs/integration/`、`logs/e2e/`（gitignore）

**禁止：**
- ❌ 测试失败后不看日志就改代码
- ❌ 只看"测试通过/失败"的汇总行，不看具体失败用例
- ❌ 日志输出到 /dev/null

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
- [ ] tests/integration/ 存在且有测试文件（集成测试）
- [ ] progress.json 存在且 completed 非空
- [ ] 代码遵循分层架构（Controller 不直接引用 Repository）
- [ ] 覆盖率 ≥95%（JaCoCo/c8 报告存在且达标）
- [ ] 集成测试连接真实 DB（非 mock）

## 约束
- 单任务超时：2小时（dispatch-task.sh 内置）
- 单任务最大轮次：50轮
- 失败重试：1次
- 重试仍失败 → 中断，询问用户
- ❌ 禁止只看任务描述就直接写代码
- ❌ 禁止在此阶段写 E2E 测试（QA 负责）
