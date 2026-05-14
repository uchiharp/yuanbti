# Agent Pipeline 优化建议书 v1.0

> 基于 ClawHub 生态对比分析，识别差距与升级方向
> 日期：2026-05-14

---

## 一、现状盘点

### 1.1 已有资产

**Pipeline 框架：**
- PRD 2384 行 + 完整架构文档 + 脚本 + 模板
- 9 阶段流水线 + 3 档规模裁剪（大/中/小）
- 交叉评审机制（每个阶段有"对手"挑战质量）
- 回退额度控制
- `pipeline-check.sh` 门禁脚本

**Skill 清单（45个）：**

| 阶段 | Skill |
|------|-------|
| 需求 | `requirements-analysis`、`prd-review` |
| 架构 | `tech-architecture`、`architecture-review`、`tech-spike` |
| UX/UI | `ux-review`、`ui-review`、`finder-ui` |
| 任务 | `task-decomposition`、`task-review`、`task-verifier` |
| 开发 | `web-coder`、`web-development`、`react-dev`、`nextjs-react-typescript`、`humanize-code`、`karpathy-engineering-guidelines` |
| 代码审查 | `code-review-quality`、`code-review-checklist`、`typescript-react-reviewer`、`code-quality-guard` |
| 测试 | `qa-workflow`、`qa-review-workflow`、`run-tests` |
| 项目管理 | `project-scan`、`project-scout` |
| 工具链 | `reasoning-rag`、`db9`、`git-advanced-workflows`、`security-review`、`self-evolver`、`skill-architect`、`find-skills` |
| Pipeline | `agent-pipeline`、`agent-discipline`、`iterative-contract` |

### 1.2 自评优势

| 优势 | 说明 |
|------|------|
| 完整流水线编排 | 9 阶段 + 状态机 + 门禁脚本，ClawHub 上全是孤立 skill |
| 交叉评审机制 | 每个阶段有"对手"挑战，ClawHub 没有类似机制 |
| 规模裁剪 | 大/中/小项目走不同流程，避免杀鸡用牛刀 |
| 防假测试铁律 | `task-verifier` + `agent-discipline` + 历史教训系统 |
| 回退控制 | 有额度、有路径、有记录 |
| 经验沉淀 | MemPalace + self-evolver，做完项目自动沉淀教训 |
| 中文生态 | 大部分 ClawHub skill 是英文 |

---

## 二、ClawHub 生态对比：我们缺什么

### 2.1 缺失的能力（按严重程度排序）

#### 🔴 P0 — 完全没有

| 能力 | ClawHub 参考 | 影响 |
|------|-------------|------|
| **性能测试** | k6 生态 + 压测模式成熟 | 上线后性能问题无预警 |
| **CI/CD 集成** | `ci-cd-pipeline-builder`（3.05分） | 测试全靠手动执行 |
| **测试数据隔离** | Testcontainers 模式 | 测试用例互相污染 |
| **代码风险自动分析** | `riskforge` — 基于代码自动生成测试策略 | QA 靠经验判断风险 |

#### 🟡 P1 — 有但不够强

| 能力 | 现状 | ClawHub 参考 | 差距 |
|------|------|-------------|------|
| **E2E 测试模式** | `run-tests` 只跑命令 | `e2e-testing-patterns`（3.21分）有 Page Object、数据驱动等模式 | 缺乏测试架构指导 |
| **PRD→领域建模** | `requirements-analysis` 到 PRD 就停了 | `prd-to-ddd-design`（1.98分）能直接产出 DDD 模型、ER 图 | 需求→设计有断层 |
| **设计系统自动化** | `finder-ui` 只做评审 | `ui-design-system`（4.25分）能自动生成设计 token | 不生成规范代码 |
| **竞品分析** | 无 | `competitor-teardown`（0.60分）有系统化框架 | 无竞品意识 |
| **头脑风暴结构化** | PRD 里提了 brainstorm 但无独立 skill | `brainstorming` 有结构化创意流程 | 创意发散不够系统 |

#### 🟢 P2 — 锦上添花

| 能力 | 说明 |
|------|------|
| **Git Worktree 隔离** | `using-git-worktrees` — 并行开发时分支隔离 |
| **编码会话共享** | `codecast` — 流式共享编码过程 |
| **测试覆盖分析** | `riskforge` 内含覆盖率分析能力 |

### 2.2 差距可视化

```
              我们的 Pipeline
    ┌─────────────────────────────────────┐
    │                                      │
    │  需求 ──→ 架构 ──→ UX/UI ──→ 任务   │
    │    │                    │         │  │
    │    ✅                    ✅        ✅  │
    │                                      │
    │  开发 ──→ 代码审查 ──→ 测试 ──→ 验收  │
    │    │        │          │        │    │
    │    ✅        ✅      ⚠️ 弱     ✅    │
    │                                      │
    │  ❌ 性能测试                          │
    │  ❌ CI/CD                             │
    │  ❌ 风险自动分析                       │
    │  ❌ 领域建模                          │
    │  ❌ 竞品分析                          │
    │                                      │
    └─────────────────────────────────────┘
```

---

## 三、Skill vs Plugin：架构升级方向

### 3.1 核心区别

| 能力 | Skill（知识） | Plugin（能力） |
|------|-------------|--------------|
| 读写文件 | ❌ 只能在 chat 里建议 | ✅ 能直接操作文件系统 |
| 注册新命令 | ❌ 不能 | ✅ `/my-command` |
| 提供 MCP 工具 | ❌ 不能 | ✅ 能给 Agent 新工具 |
| 持久化状态 | ❌ 每次对话重新来 | ✅ 能维护数据库/文件状态 |
| 监听事件 | ❌ 不能 | ✅ 能监听消息、Git hook、定时器 |
| 跨 Session 通信 | ❌ 不能 | ✅ 能在 Agent 间传递消息 |
| 门禁脚本自动执行 | ❌ 只能建议跑 | ✅ 能自动跑并拦截 |
| UI 面板 | ❌ 不能 | ✅ 能渲染自定义界面 |
| 状态机管理 | ❌ 靠文件系统模拟 | ✅ 内存级状态机 |

### 3.2 Pipeline 中需要 Plugin 的环节

| 环节 | 当前实现 | 问题 | Plugin 能做什么 |
|------|---------|------|----------------|
| 阶段切换 | 协调者手动调用 `pipeline-check.sh` | 依赖人，容易漏 | 自动在阶段切换时跑门禁，失败则拦截 |
| 交叉评审 | 协调者手动 spawn 多个 session | 调度逻辑在 agent 脑子里 | 自动 spawn + 汇总 + 超时控制 |
| 回退额度 | 文件计数 | 不精确，可能被覆盖 | 内存级状态机，精确计数 |
| 产出物归档 | Agent 自觉放到 `changes/` | 容易放错位置或忘记 | 自动归档 + 校验目录结构 |
| Agent 间消息 | 靠文件系统间接通信 | 延迟大，不可靠 | 事件总线，实时消息传递 |
| 进度追踪 | 读 `_config.json` | 每个 agent 都要读一遍 | 中央状态 + 订阅通知 |
| 超时控制 | 无 | agent 可能卡死 | 自动超时 + 降级处理 |

### 3.3 升级路径

```
当前架构（Skill 驱动）：

  协调者 Agent（读 PRD + SKILL.md）
       │
       ├── 手动 spawn PM Agent
       ├── 手动 spawn 架构 Agent
       ├── 手动跑 pipeline-check.sh
       ├── 手动汇总评审结果
       └── 手动管理状态机

目标架构（Plugin 驱动）：

  Pipeline Plugin（MCP 工具）
       │
       ├── pipeline_init()     → 初始化状态机
       ├── pipeline_advance()  → 自动跑门禁 → 通过则推进
       ├── pipeline_dispatch() → 自动 spawn 对应 Agent
       ├── pipeline_gate()     → 自动检查产出物
       ├── pipeline_rollback() → 自动回退 + 额度扣减
       └── pipeline_sessions() → 自动管理 Agent 生命周期
       │
       └── 协调者 Agent 只做"判断"和"沟通"
           不做"调度"和"检查"
```

---

## 四、建议安装的 ClawHub Skill

### 4.1 立刻安装（补缺口）

| # | Skill | 用途 | 评分 | 命令 |
|---|--------|------|------|------|
| 1 | `prd-to-ddd-design` | PRD → DDD 领域建模 | 1.98 | `clawhub install prd-to-ddd-design` |
| 2 | `e2e-testing-patterns` | E2E 测试架构模式 | 3.21 | `clawhub install e2e-testing-patterns` |
| 3 | `riskforge` | 代码风险分析 + 自动测试策略 | — | `clawhub install riskforge` |

### 4.2 短期安装（增强）

| # | Skill | 用途 | 评分 |
|---|--------|------|------|
| 4 | `ui-design-system` | 设计系统自动化 | 4.25 |
| 5 | `fullstack-developer` | 全栈开发增强 | 4.24 |
| 6 | `duck-code-review-hardened` | 加固版代码审查 | 3.43 |
| 7 | `cn-project-management` | 中文项目管理 | 3.05 |

### 4.3 长期考虑

| # | Skill | 用途 |
|---|--------|------|
| 8 | `ci-cd-pipeline-builder` | CI/CD 流水线生成 |
| 9 | `competitor-teardown` | 竞品分析框架 |
| 10 | `brainstorming` | 结构化头脑风暴 |

---

## 五、自研 Skill 建议（ClawHub 上没有的）

### 5.1 需要自研的 Skill

| Skill | 说明 | 为什么 ClawHub 没有 |
|-------|------|-------------------|
| **test-data-isolation** | 测试数据隔离策略（Testcontainers + 快照 + UUID 唯一标识） | 太项目特化 |
| **pipeline-smoke-protocol** | 冒烟验证标准化协议（防止"假装测试"） | 我们的独特经验 |
| **contract-verification** | 前后端接口契约自动验证 | 通用但没人做 |
| **performance-budget** | 性能预算设定 + 告警 | 新兴概念 |
| **test-idempotency-check** | 测试幂等性检查器 | 我们的痛点 |

### 5.2 建议升级为 Plugin 的模块

| 模块 | 当前形态 | 目标形态 |
|------|---------|---------|
| Pipeline 状态机 | `pipeline-check.sh` + `_config.json` | MCP Plugin `pipeline_advance()` |
| 交叉评审调度 | 协调者手动 spawn | MCP Plugin `pipeline_dispatch()` |
| 回退额度管理 | 文件计数 | Plugin 内存状态 |
| 产出物归档 | Agent 自觉 | Plugin 自动归档 |
| Agent 超时控制 | 无 | Plugin watchdog |

---

## 六、实施路线图

### Phase 1：补 Skill（1-2天）

```
安装 3 个缺口 Skill
    │
    ├── prd-to-ddd-design → 补上需求→设计断层
    ├── e2e-testing-patterns → 补上测试架构指导
    └── riskforge → 补上风险自动分析
    │
    └── 验证：在下一个项目中实际使用
```

### Phase 2：自研 Skill（3-5天）

```
开发 5 个自研 Skill
    │
    ├── test-data-isolation → 解决测试数据污染
    ├── pipeline-smoke-protocol → 标准化冒烟验证
    ├── contract-verification → 自动验接口契约
    ├── performance-budget → 性能预算
    └── test-idempotency-check → 测试幂等检查
    │
    └── 验证：在 film-auth 项目中试点
```

### Phase 3：Plugin 升级（1-2周）

```
将 Pipeline 核心逻辑升级为 Plugin
    │
    ├── Step 1: 状态机 Plugin（替换 _config.json）
    │     pipeline_init / advance / status / rollback
    │
    ├── Step 2: 调度 Plugin（替换手动 spawn）
    │     pipeline_dispatch / sessions
    │
    ├── Step 3: 门禁 Plugin（替换 pipeline-check.sh）
    │     pipeline_gate（自动检查 + 拦截）
    │
    └── Step 4: 通信 Plugin（替换文件系统间接通信）
          事件总线 + 订阅通知
    │
    └── 验证：完整项目跑一遍 9 阶段流程
```

### Phase 4：生态打通（持续）

```
Pipeline Plugin + ClawHub Skill 生态打通
    │
    ├── Plugin 自动推荐所需 Skill
    ├── Pipeline 模板可发布到 ClawHub
    └── 其他团队可复用我们的 Pipeline
```

---

## 七、预期收益

| 维度 | 优化前 | 优化后 |
|------|--------|--------|
| 测试覆盖 | 只有单元+E2E，无性能/边界/错误场景 | 五层测试体系（单元/集成/E2E/性能/错误） |
| 流水线可靠性 | 依赖协调者手动调度 | Plugin 自动化调度 + 门禁拦截 |
| 需求→设计 | PRD 到架构有断层 | DDD 领域建模补上 |
| 测试数据 | 互相污染 | Testcontainers + UUID 隔离 |
| 风险识别 | QA 靠经验 | 代码自动分析风险 → 生成测试策略 |
| 可复现性 | Pipeline 只在我们这能用 | Plugin + Skill 模板可发布到 ClawHub |

---

## 八、风险与注意事项

| 风险 | 应对 |
|------|------|
| Plugin 开发门槛高 | 先用 Skill 模拟 Plugin 行为，验证逻辑后再升级 |
| ClawHub Skill 质量参差不齐 | 安装前 `clawhub inspect` 看内容，不盲目装 |
| 自研 Skill 维护成本 | 只做通用的，项目特化的不做成 Skill |
| Plugin 升级影响现有流程 | 渐进式：先并行运行（Plugin + 脚本），验证通过后切换 |
| Agent 间通信改造 | 先用文件系统 + 轮询验证逻辑，再换成事件总线 |
