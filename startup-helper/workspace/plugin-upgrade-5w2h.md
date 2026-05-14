# Plugin 升级方案 — 5W2H 分析

> 基于 openclaw-pipeline 当前架构的深度分析
> 日期：2026-05-14

---

## 一、What — 做什么

### 1.1 当前架构

openclaw-pipeline 已经是一个 Plugin（`openclaw.plugin.json` type: "tool"），注册了 7 个 MCP 工具：

| 工具 | 作用 | 自动化程度 |
|------|------|-----------|
| `pipeline_init` | 初始化项目状态 | 被动——需协调者调用 |
| `pipeline_start_phase` | 启动指定阶段 | 被动——需协调者调用 |
| `pipeline_check_gate` | 运行门禁检查 | 被动——需协调者调用 |
| `pipeline_advance` | 推进阶段（含门禁+prompt生成） | 被动——需协调者调用 |
| `pipeline_rollback` | 回退阶段 | 被动——需协调者调用 |
| `pipeline_status` | 查询状态 | 被动——需协调者调用 |
| `pipeline_recover` | 恢复失败阶段 | 被动——需协调者调用 |

**核心问题：7 个工具全部是被动调用，协调者 Agent 必须记住在正确时机调用正确工具。**

### 1.2 要升级什么

把"协调者脑子里的调度逻辑"变成"Plugin 自动执行的行为"：

| 升级项 | 当前 | 目标 |
|--------|------|------|
| 门禁触发 | 协调者手动调用 `pipeline_check_gate` | 阶段完成时自动触发 |
| 阶段推进 | 协调者手动调用 `pipeline_advance` | 门禁通过后自动推进 |
| Agent 调度 | 协调者手动 spawn Agent | Plugin 根据 executor 字段自动 spawn |
| 超时处理 | 无 | Plugin watchdog 自动检测并处理 |
| 产出归档 | Agent 自觉放到 `.contracts/` | Plugin 自动归档 + 校验目录结构 |
| Agent 间通信 | 文件系统间接通信 | Plugin 事件总线 |

### 1.3 不做什么

- **不改现有 7 个工具的接口**——保持向后兼容
- **不替换 GateChecker / StateManager / PromptBuilder**——这些模块逻辑正确，只改调用方式
- **不做 UI 面板**——当前不需要可视化
- **不引入新的外部依赖**（Redis / 消息队列等）——用文件系统 + 内存实现

---

## 二、Why — 为什么做

### 2.1 当前痛点（按严重程度排序）

| 痛点 | 频率 | 后果 | 严重程度 |
|------|------|------|---------|
| 协调者忘记跑门禁就推进 | 每个项目 | 质量失控，未完成的阶段被跳过 | 🔴 致命 |
| 协调者忘记 spawn 正确角色的 Agent | 每个阶段 | 开发阶段 spawn 了 QA Agent，产出不匹配 | 🔴 致命 |
| Agent 卡死无超时 | 偶尔 | 整个 pipeline 停滞，无自动恢复 | 🟡 严重 |
| 产出物放错目录 | 经常 | 下个阶段读不到前置产出 | 🟡 严重 |
| Agent 间通信靠文件轮询 | 持续 | 延迟大，协调者需要反复读目录 | 🟢 不便 |

### 2.2 不做的风险

如果不升级，pipeline 的可靠性完全依赖协调者 Agent 的"记忆"和"纪律"。Agent 换模型、换 prompt、上下文压缩后，调度逻辑随时可能丢失。

---

## 三、Who — 谁做谁用

### 3.1 开发者

本人（用户）+ Claude Code agent。

### 3.2 使用者

| 角色 | 使用方式 | 受影响 |
|------|---------|--------|
| 协调者 Agent | 调用 Plugin 工具 + 接收自动事件 | 最直接受益——减少手动调度 |
| PM Agent | 被自动 spawn，接收任务 prompt | 间接受益——prompt 自动注入技术栈 |
| 开发 Agent | 被自动 spawn，接收任务 prompt | 同上 |
| QA Agent | 被自动 spawn，接收任务 prompt | 同上 |
| 用户 | 通过协调者间接使用 | 受益——pipeline 更可靠 |

---

## 四、When — 什么时候做

### 4.1 优先级排序依据

```
影响面 × 发生频率 = 优先级
```

| 步骤 | 影响面 | 频率 | 优先级 |
|------|--------|------|--------|
| 门禁自动触发 | 全阶段 | 每阶段必做 | P0 |
| Agent 自动调度 | 全阶段 | 每阶段必做 | P0 |
| 超时 watchdog | 单阶段 | 偶尔 | P1 |
| 产出自动归档 | 全阶段 | 经常出错 | P1 |
| 事件总线 | Agent间 | 持续不便 | P2 |

### 4.2 时间规划

| 步骤 | 预计工时 | 前置依赖 | 验收标准 |
|------|---------|---------|---------|
| Step 1：门禁+推进自动化 | 3-4 天 | 无 | 阶段完成时门禁自动执行，失败自动阻断 |
| Step 2：Agent 调度+超时 | 3-4 天 | Step 1 | 根据 executor 字段自动 spawn，超时自动处理 |
| Step 3：产出归档 | 1-2 天 | Step 2 | 产出物自动归档到 .contracts/ 正确目录 |
| Step 4：事件总线 | 2-3 天 | Step 2 | Agent 间实时通信，替代文件轮询 |

总工时：9-13 天。

---

## 五、Where — 在哪里做

### 5.1 代码变更范围

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `src/index.ts` | 重构 | 当前 7 个工具是 inline 实现，需重构为委托 Orchestrator 类 |
| `src/orchestrator.ts` | 扩展 | 加入自动门禁、自动调度、watchdog、归档逻辑 |
| `src/types.ts` | 扩展 | 加入事件类型、调度参数类型 |
| `src/dispatcher.ts` | 新增 | Agent 调度模块 |
| `src/watchdog.ts` | 新增 | 超时监控模块 |
| `src/event-bus.ts` | 新增 | Agent 间事件总线 |
| `src/archiver.ts` | 新增 | 产出物自动归档模块 |

### 5.2 不改的文件

| 文件 | 原因 |
|------|------|
| `src/gate-checker.ts` | 逻辑正确，只被调用 |
| `src/prompt-builder.ts` | 同上 |
| `src/state-manager.ts` | 同上 |
| `src/phase-resolver.ts` | 同上 |
| `pipeline-config.json` | 只加字段，不改现有结构 |

---

## 六、How — 怎么做

### 6.1 Step 1：门禁+推进自动化

**问题：** 协调者必须手动调用 `pipeline_advance` 才能推进，经常忘记先跑门禁。

**方案：** 在 `pipeline_advance` 内部，门禁检查已经是第一步骤。关键是让门禁失败时**阻断推进**并**通知协调者**，而不是返回一个 JSON 让协调者自己判断。

**具体改动：**

```
当前流程：
  协调者 → pipeline_advance()
         → 内部跑门禁
         → 返回 JSON（status: "fail"）
  协调者需要读 JSON → 判断失败 → 决定下一步

升级后流程：
  协调者 → pipeline_advance()
         → 内部跑门禁
         → 失败：自动设置 phase.status = "failed"
                 自动写入失败原因到 .contracts/
                 返回结构化错误（含 recovery_hint）
         → 通过：自动设置 phase.status = "completed"
                 自动启动下一阶段
                 自动构建下一阶段 prompt
                 返回下一阶段信息 + prompt
```

**代码改动：**

1. `index.ts`：`pipeline_advance` 的 execute handler 委托给 `Orchestrator.handleAdvance`
2. `orchestrator.ts`：`handleAdvance` 扩展逻辑：
   - 门禁失败 → 写 `gate-fail-report.md` 到 `.contracts/` → 返回 `PipelineError` 含 recovery_hint
   - 门禁通过 → 自动 `pipeline_start_phase` 下一阶段 → 调用 `buildCustomizedPrompt` → 返回 prompt
3. 新增 `pipeline_auto_advance` 工具：协调者只需在阶段产出完成后调用一次，自动完成 门禁→推进→启动下一阶段→生成 prompt 的全链路

### 6.2 Step 2：Agent 调度+超时

**问题：** 协调者需要自己判断"这个阶段该 spawn 什么角色的 Agent"，而且没有超时机制。

**方案：** pipeline-config.json 已经有 `executor` 字段（developer/qa/architect/pm），Plugin 自动根据这个字段 spawn 对应 Agent。

**具体改动：**

1. 新增 `dispatcher.ts`：

```typescript
interface DispatchRequest {
  phaseId: string;
  executor: string;  // "developer" | "qa" | "architect" | "pm" | "coordinator"
  prompt: string;
  projectPath: string;
  timeoutMinutes: number;
}

interface DispatchResult {
  agentId: string;
  status: "running" | "completed" | "timed_out" | "failed";
  outputFiles: string[];
  durationMs: number;
}
```

2. `Orchestrator.handleAdvance` 成功后，自动调用 `dispatcher.dispatch()` spawn 下一阶段的 Agent
3. 新增 `watchdog.ts`：定期检查 `state.phases[phaseId].started_at` + `timeout_minutes`，超时自动设置 `timed_out` 状态
4. `pipeline-config.json` 中每个阶段的 `executor` 字段作为调度依据

**调度策略：**

```
Phase 0.5-0.8: executor = "pm"       → spawn PM Agent
Phase 1:       executor = "pm"       → spawn PM Agent
Phase 1.5:     executor = "coordinator" → spawn 多个 review Agent
Phase 2:       executor = "architect" → spawn Architect Agent
Phase 2.5:     executor = "coordinator" → spawn 多个 review Agent
Phase 3-4.5:   executor = "pm/architect" → 根据 scale 决定
Phase 5-5.5:   executor = "architect" → spawn Architect Agent
Phase 6:       executor = "developer" → spawn Developer Agent
Phase 6.3:     executor = "developer" → spawn Developer Agent（冒烟）
Phase 6.5-7:   executor = "coordinator" → spawn review Agent
Phase 8:       executor = "developer" → spawn Developer Agent
Phase 8.3:     executor = "qa"        → spawn QA Agent
Phase 8.6:     executor = "qa"        → spawn QA Agent
Phase 9:       executor = "coordinator" → 用户确认
```

### 6.3 Step 3：产出自动归档

**问题：** Agent 有时把文件放到项目根目录而不是 `.contracts/phase-{id}/` 下。

**方案：** `pipeline_advance` 成功后，自动扫描项目目录中的产出物，移动到正确的 `.contracts/` 子目录。

**具体改动：**

1. 新增 `archiver.ts`：

```typescript
interface ArchiveRule {
  pattern: string;      // 产出物文件名或 glob
  targetDir: string;    // 目标目录（如 .contracts/{project}/phase-{id}-{name}/）
  required: boolean;    // 是否必须存在
}

async function archiveArtifacts(
  projectPath: string,
  phaseId: string,
  phaseName: string,
  artifacts: ArtifactRule[],
): Promise<{ archived: string[]; missing: string[] }>
```

2. 在 `Orchestrator.handleAdvance` 中，门禁通过后、标记 completed 之前，调用 `archiveArtifacts`
3. 归档失败（缺少 required 产出物）→ 门禁失败，不推进

### 6.4 Step 4：事件总线

**问题：** Agent 间通信靠文件系统（写文件 → 另一个 Agent 轮询读文件），延迟大、不可靠。

**方案：** Plugin 内置一个简单的内存事件总线，Agent 通过 `pipeline_subscribe` 和 `pipeline_emit` 工具通信。

**具体改动：**

1. 新增 `event-bus.ts`：

```typescript
interface PipelineEvent {
  type: "phase_completed" | "phase_failed" | "review_submitted" | "gate_passed" | "gate_failed" | "agent_timeout";
  phaseId: string;
  data: Record<string, unknown>;
  timestamp: string;
}

type EventHandler = (event: PipelineEvent) => void | Promise<void>;

class EventBus {
  subscribe(eventType: string, handler: EventHandler): void;
  emit(event: PipelineEvent): Promise<void>;
  getHistory(eventType?: string): PipelineEvent[];
}
```

2. 新增 2 个 MCP 工具：
   - `pipeline_subscribe`：注册事件监听（如 QA Agent 订阅 `phase_completed:8`）
   - `pipeline_emit`：发送事件（如 Developer Agent 完成后发送 `phase_completed:8`）

3. 事件自动触发：`Orchestrator.handleAdvance` 成功后自动 emit `phase_completed`，失败后自动 emit `phase_failed`

---

## 七、How Much — 代价多少

### 7.1 工时估算

| 步骤 | 新增代码量 | 修改代码量 | 工时 |
|------|-----------|-----------|------|
| Step 1：门禁自动化 | ~200 行 | ~150 行（index.ts + orchestrator.ts） | 3-4 天 |
| Step 2：调度+超时 | ~400 行 | ~100 行（orchestrator.ts） | 3-4 天 |
| Step 3：产出归档 | ~150 行 | ~50 行（orchestrator.ts） | 1-2 天 |
| Step 4：事件总线 | ~250 行 | ~100 行（index.ts + orchestrator.ts） | 2-3 天 |
| 测试 | ~300 行 | — | 2 天 |
| **合计** | **~1300 行** | **~400 行** | **11-15 天** |

### 7.2 风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| index.ts 和 orchestrator.ts 合并时引入 bug | 中 | 高 | 先写测试覆盖现有行为，再重构 |
| Agent spawn 机制依赖 OpenClaw Plugin SDK 能力 | 中 | 高 | 先验证 SDK 是否支持 programmatic spawn |
| 事件总线内存泄漏 | 低 | 中 | 事件历史限 100 条，自动过期 |
| 重构期间 pipeline 不可用 | 中 | 高 | 新旧代码并行，feature flag 切换 |

### 7.3 先决条件验证清单

在开始编码之前，必须先验证：

- [ ] OpenClaw Plugin SDK 是否支持 programmatic agent spawn
- [ ] Plugin 是否能在工具执行中调用其他工具（如 `pipeline_advance` 内部调 `pipeline_start_phase`）
- [ ] Plugin 是否能注册后台任务（watchdog 定时检查）
- [ ] index.ts 和 orchestrator.ts 合并后，现有 7 个工具的接口是否完全兼容

如果上述任何一项不满足，需要调整方案或先扩展 SDK 能力。

---

## 八、实施顺序流程

```
Step 0: 验证先决条件（1天）
  ├── SDK 能力验证
  ├── 现有测试覆盖确认
  └── feature flag 机制设计
       │
Step 1: 门禁+推进自动化（3-4天）
  ├── 1.1 合并 index.ts → orchestrator.ts
  ├── 1.2 handleAdvance 扩展（自动归档失败原因）
  ├── 1.3 新增 pipeline_auto_advance 工具
  └── 1.4 测试：全阶段自动推进
       │
Step 2: Agent 调度+超时（3-4天）
  ├── 2.1 dispatcher.ts 实现
  ├── 2.2 executor → Agent 映射
  ├── 2.3 watchdog.ts 实现
  └── 2.4 测试：自动 spawn + 超时处理
       │
Step 3: 产出自动归档（1-2天）
  ├── 3.1 archiver.ts 实现
  ├── 3.2 集成到 handleAdvance
  └── 3.3 测试：产出物自动归档
       │
Step 4: 事件总线（2-3天）
  ├── 4.1 event-bus.ts 实现
  ├── 4.2 pipeline_subscribe / pipeline_emit 工具
  ├── 4.3 自动事件触发集成
  └── 4.4 测试：Agent 间事件通信
       │
Step 5: 集成测试+切换（2天）
  ├── 全流程跑通（init → ... → 交付验收）
  ├── 新旧并行运行验证
  └── feature flag 切换到新架构
```
