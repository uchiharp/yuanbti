# 阶段6：开发执行

## 任务
协调者按任务清单逐个 dispatch 开发 agent，每个任务一次调度。QA 同步写 E2E 测试脚本。

**开发不能简单机械地翻译 PRD**，必须遵循技术栈最佳实践，将任务拆分成独立小流程逐步执行。

## 必读文件（协调者）
1. docs/ARCHITECTURE.md
2. TASK-LIST.md
3. api-schema.md（阶段5.5产出）
4. PRD.md（🟡/🔴项目为细化后的 PRD，含交互细节/边界/异常处理）
5. UI-UX-DESIGN.md（🟡/🔴项目，阶段1.7产出）
6. docs/ui-prototype.html（🟡/🔴项目，阶段1.7产出的 HTML 原型参考）

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

## 技术栈最佳实践（开发必须遵循）

开发不是简单翻译 PRD，必须在每个任务中主动应用以下最佳实践：

### A. 状态管理最佳实践
- **全局状态**：仅跨组件/跨页面共享的状态放入全局 store
- **本地状态**：组件私有状态用 useState/useReducer，不污染全局
- **服务端状态**：API 数据用 TanStack Query / SWR 管理，不做手动缓存
- **表单状态**：复杂表单用 dedicated form library（react-hook-form / vee-validate）
- **URL 状态**：筛选/分页/Tab 状态同步到 URL，支持书签和前进后退

### B. 错误边界与异常处理
- **React Error Boundary**：每个关键路由/组件包裹 ErrorBoundary
- **API 错误**：统一拦截器处理 401/403/500，业务错误用 Toast 提示
- **异步错误**：Promise 链必须有 catch 或 try-catch
- **网络错误**：Axios/Fetch 超时配置 + 重试策略 + 离线检测
- **渲染错误**：Suspense fallback + ErrorBoundary 兜底

### C. 性能优化
- **渲染优化**：React.memo/useMemo/useCallback 按需使用，避免过度优化
- **代码分割**：路由级 lazy loading，大组件动态 import
- **列表虚拟化**：超过 100 项的列表用 virtual scroll
- **图片优化**：懒加载、WebP/AVIF、响应式 srcset、占位骨架屏
- **Bundle 优化**：Tree shaking、按需引入、分析 bundle size

### D. 代码规范
- **TypeScript strict mode**：noImplicitAny、strictNullChecks 全开
- **命名规范**：组件 PascalCase、函数/变量 camelCase、常量 UPPER_SNAKE
- **文件组织**：一个文件一个组件/类、按功能分目录、index 统一导出
- **注释规范**：JSDoc 公共接口、TODO 标记技术债、避免冗余注释
- **Git 规范**：Conventional Commits、原子提交、有意义的 message

### E. 安全编码
- **输入校验**：前端校验 + 后端校验双重保障
- **XSS 防护**：不使用 dangerouslySetInnerHTML，输出编码
- **CSRF 防护**：Token 机制、SameSite Cookie
- **敏感数据**：Token 不存 localStorage（用 httpOnly Cookie）、密码不明文

### F. 任务逐步执行策略

每个任务不是一次性完成所有代码，而是拆分成独立的小流程逐步执行：

1. **接口定义**：先定义 API 接口/类型，确保契约一致
2. **数据层**：实现数据获取/存储逻辑（Repository/Service 层）
3. **业务逻辑层**：实现核心业务逻辑（UseCase/Handler 层）
4. **UI 层**：实现页面和组件
5. **状态管理**：接入全局状态管理
6. **异常处理**：添加错误边界和异常提示
7. **单元测试**：为每层编写单元测试
8. **集成验证**：连接前后端验证完整流程

每步完成后运行测试确认正确，再进入下一步。

## 进度追踪

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
- [ ] TypeScript strict mode 已开启（如适用）
- [ ] ErrorBoundary 已配置（如适用）
- [ ] API 统一错误拦截器已配置

## 约束
- 单任务超时：2小时（dispatch-task.sh 内置）
- 单任务最大轮次：50轮
- 失败重试：1次
- 重试仍失败 → 中断，询问用户
- ❌ 禁止只看任务描述就直接写代码
- ❌ 禁止在此阶段写 E2E 测试（QA 负责）
- ❌ 禁止一次性写完所有代码（必须逐步执行）
