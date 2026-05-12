# Agent Pipeline — 技术架构方案

基于 PRD.md 设计的可实现技术方案。本文档是实现的唯一依据。

---

## 1. 系统总览

```
用户需求
  │
  ▼
┌─────────────────────────────────────────────────────┐
│  Claude Code Session（协调者 agent）                   │
│  ┌───────────────────────────────────────────────┐  │
│  │ orchestrator.ts (MCP Plugin)                  │  │
│  │  ├─ pipeline_init    → 初始化项目状态           │  │
│  │  ├─ pipeline_advance → 推进到下一阶段           │  │
│  │  ├─ pipeline_gate    → 门禁检查                │  │
│  │  ├─ pipeline_status  → 查看状态                │  │
│  │  ├─ pipeline_rollback→ 回退                    │  │
│  │  ├─ pipeline_dispatch→ 解析 agent session 路由  │  │
│  │  └─ pipeline_sessions→ 管理 agent sessions      │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │ prompt-builder.ts                             │  │
│  │  ├─ 读取 SOUL.md / ROLE_TEMPLATES              │  │
│  │  ├─ 注入 skill（SKILL.md 摘要）                 │  │
│  │  ├─ 注入 agent-discipline 条款                  │  │
│  │  └─ 注入上下文（CONTEXT.md + 上游产出）          │  │
│  └───────────────────────────────────────────────┘  │
└─────────────┬───────────────────────────────────────┘
              │ 调度
              ▼
┌─────────────────────────────────────────────────────┐
│  Claude Code CLI                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ PM agent │ │ 架构 agent│ │ 开发 agent│ ...        │
│  │ glm-5.1  │ │mimo-v2.5 │ │mimo-v2.5 │            │
│  └──────────┘ └──────────┘ └──────────┘            │
│  --session-id / --resume 实现持久化 session          │
│  --model 实现模型路由                                │
└─────────────┬───────────────────────────────────────┘
              │ 产出
              ▼
┌─────────────────────────────────────────────────────┐
│  项目目录 ({project_path}/)                           │
│  ├─ .contracts/{project}/                            │
│  │   ├─ _config.json   ← 全局状态机                  │
│  │   ├─ _index.json     ← 合同索引                   │
│  │   ├─ phase-*/        ← 各阶段产出                 │
│  │   ├─ changes/        ← 变更/回退记录              │
│  │   └─ communications/ ← 沟通记录                   │
│  ├─ CONTEXT.md          ← 项目知识摘要（≤200行）      │
│  ├─ health-dashboard.md ← 健康度看板                  │
│  └─ src/                ← 项目源码                    │
└─────────────────────────────────────────────────────┘
```

---

## 2. 核心架构决策

### AD-1：配置驱动，不硬编码规则

**决策：** 所有阶段定义、门禁规则、模型路由、规模裁剪均在 `pipeline-config.json` 中声明。

**理由：** PRD 明确"改规则=改配置，不碰脚本代码"。配置文件是整个 pipeline 的 source of truth。

**现状：** `pipeline-config.json` 已存在，包含 17 个阶段定义、模型路由、回退限额。需补充：交叉评审参与者配置、上下文复用规则。

### AD-2：TypeScript Plugin + Shell 脚本分层

**决策：**
- **orchestrator.ts**（MCP Plugin）：状态机、session 路由、模型路由、门禁检查、prompt 构建
- **Shell 脚本**：文件级检查（行数、格式、内容模式匹配）

**理由：** TypeScript 处理需要 JSON 解析和状态管理的逻辑；Shell 处理简单的文件存在/行数/模式检查。两者通过 MCP tool 调用桥接。

**现状：** orchestrator.ts 已实现 init/start/gate/advance/rollback/status/recover + dispatch/sessions。Shell 脚本目录尚未创建。

### AD-3：Session 持久化已实现

**决策：** 用 Claude Code 的 `--session-id`（新建）和 `--resume`（恢复）实现 agent session 持久化。

**现状：** orchestrator.ts 的 `resolveDispatch` 方法已实现：首次创建 UUID → 后续 resume。`agent_sessions` 存储在 `PipelineState` 中。

### AD-4：交叉评审替代独立评审官

**决策：** 删除所有 `*-reviewer` 专用 agent，改由相关角色交叉评审。

**影响：**
- pipeline-config.json 中 `review.roles` 字段仍引用 reviewer ID → 需清理
- 交叉评审的参与者由阶段定义中的 `cross_review_roles` 字段指定
- 各 agent 均可使用 `code-review-checklist`、`code-review-standard`、`iterative-contract` 通用 skill

**现状：** 5 个 SKILL.md 已清理 reviewer 引用。pipeline-config.json 的 phases 中仍残留 reviewer 引用。

### AD-5：模型异构性

**决策：** 交叉评审参与者必须使用不同模型，避免共享盲点。

**路由表：**
| 角色 | 模型 |
|------|------|
| architect, qa, dev2 | mimo-v2.5-pro |
| pm, dev1, dev3, ux-tester, ui-designer | glm5.1 | |

**现状：** `model_routing` 已在 pipeline-config.json 和 orchestrator.ts 中实现。

---

## 3. 数据模型

### 3.1 PipelineState（运行时状态）

```typescript
// 存储位置：.contracts/{project}/_config.json
// 分两层：TypeScript 运行时字段（orchestrator.ts 直接操作）+ 持久化扩展字段（_config.json 独有）
interface PipelineState {
  // ---- TypeScript 运行时字段 ----
  version: string;
  project_name: string;
  project_path: string;
  scale: Scale;                    // "large" | "medium" | "small"
  initialized_at: string;
  current_phase: string | null;    // "0", "1", "1.5", "2", ...
  phases: Record<string, PhaseState>;
  rollback_log: RollbackEntry[];
  gate_history: GateHistoryEntry[];
  active_sequence: string[];       // 当前规模下的活跃阶段序列
  skipped_phases: string[];        // 当前规模跳过的阶段
  rollback_count: RollbackCount;
  agent_sessions: Record<string, AgentSessionEntry>;

  // ---- 持久化扩展字段（_config.json 独有，orchestrator 读写） ----
  paused_at?: string;              // 暂停时间（用户打断/升级等待）
  rollback_in_progress?: boolean;  // 回退执行中标记（防并发回退）
  active_agents?: string[];        // 当前活跃的 agent ID 列表
  escalations?: EscalationEntry[]; // 升级记录
  first_escalation_at?: string;    // 首次升级时间（用于超时判定）
  prd_version?: number;            // PRD 版本号（变更时递增）
  config_checksum?: string;        // _config.json 内容 SHA256（防篡改）
}

interface EscalationEntry {
  from_agent: string;
  to: "user" | "coordinator";
  reason: string;
  phase: string;
  timestamp: string;
  resolved: boolean;
}
```

### 3.2 合同索引（.contracts/{project}/_index.json）

```json
{
  "schema_version": "2.0",
  "lastUpdated": "2026-05-10T14:30:00+08:00",
  "checksum": "sha256:...",
  "contracts": [
    {
      "id": "phase-1-prd",
      "task": "PRD 编写",
      "status": "signed",          // in-progress | revision-requested | signed | escalated | closed | reopened | paused
      "risk": "medium",            // low | medium | high
      "rounds": 2,
      "finalScore": 7.8,
      "agents": ["pm", "architect", "qa"],
      "contracts": ["c01.md", "c02.md"],
      "transitions": [
        { "from": "in-progress", "to": "revision-requested", "at": "2026-05-10T14:10:00+08:00", "by": "architect" },
        { "from": "revision-requested", "to": "in-progress", "at": "2026-05-10T14:15:00+08:00", "by": "pm" },
        { "from": "in-progress", "to": "signed", "at": "2026-05-10T14:25:00+08:00", "by": "architect" }
      ],
      "createdAt": "...",
      "completedAt": "..."
    }
  ],
  "stats": {
    "total": 1,
    "completed": 1,
    "inProgress": 0,
    "averageRounds": 2,
    "averageScore": 7.8
  }
}
```

**状态流转矩阵（7 种状态）：**

| 当前状态 | 可转到 | 触发条件 |
|---------|--------|---------|
| in-progress | revision-requested | 评审者打回 |
| in-progress | signed | 评审者签收 |
| in-progress | escalated | 超时/轮次超限 |
| in-progress | paused | 用户打断 |
| revision-requested | in-progress | 修订后重提 |
| signed | reopened | 回退触发 |
| escalated | closed | 用户决策完成 |
| paused | in-progress | 用户恢复 |
| reopened | in-progress | 重新执行 |

### 3.3 阶段定义（pipeline-config.json phases[]）

```jsonc
{
  "id": "1.5",
  "name": "PRD交叉评审",
  "mandatory": true,
  "scales": ["large", "medium", "small"],
  "artifacts": [
    { "name": "cross-review-pm.md", "min_lines": 50, "required": true }
  ],
  "review": {
    "min_roles": { "large": 4, "medium": 3, "small": 2 },
    "min_count": { "large": 4, "medium": 3, "small": 2 }
  },
  // 新增字段（需补充到配置 schema）
  "cross_review_roles": ["architect", "qa", "dev1", "ux-tester"],
  "executor": { "type": "acp", "role": "pm" },
  "timeout_minutes": 60,
  "skill": "prd-review"
}
```

---

## 4. 组件设计

### 4.1 orchestrator.ts — 状态机 + 调度核心

**已有功能：**
- `handleInit` — 初始化项目状态
- `handleStart` — 标记阶段开始
- `handleGate` — 门禁检查（文件存在/行数/审查数）
- `handleAdvance` — 推进到下一阶段（含 session 路由 + 模型解析）
- `handleRollback` — 回退（记录日志、标记 stale）
- `handleStatus` — 查看当前状态
- `handleRecover` — 从异常恢复
- `resolveDispatch` — 解析 agent session 路由（--session-id / --resume）
- `listSessions` — 列出所有 agent sessions
- `resetSession` — 重置某个 agent 的 session

**需新增/增强：**

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 交叉评审调度 | 并发派发评审任务给多个角色，收集评审结果 | P0 |
| 上下文注入 | prompt-builder 注入 CONTEXT.md + 上游产出 + 评审上下文 | P0 |
| 合同状态机 | 管理 in-progress → signed/revision-requested/escalated 流转 | P1 |
| 知识库更新 | 阶段完成后触发 CONTEXT.md 段落更新 | P1 |
| Brainstorm 检查 | 验证 brainstorm-log.md 存在且包含 ≥3 个问答对 | P1 |

### 4.2 Shell 脚本层

```
{project_path}/scripts/        ← 项目级脚本（从 agent-pipeline/scripts/ 复制）
├── lib.sh                     ← 共享函数库
├── pipeline-check.sh          ← 主入口（配置驱动，从 pipeline-config.json 读取阶段规则）
├── review-check.sh            ← 评审质量检查
├── contract-check.sh          ← 合同轮次+回退次数+stale 文件检查
├── test-report-check.sh       ← 测试报告格式检查
├── acceptance-check.sh        ← 阶段9验收检查
└── security-scan.sh           ← 安全扫描（已有）
```

**lib.sh 核心函数：**
- `lib_error / lib_warning / lib_ok` — 统一输出
- `lib_check_file` — 文件存在+行数检查
- `lib_count_pattern` — 模式匹配计数
- `lib_summary` — 汇总输出
- `lib_update_context` — 更新 CONTEXT.md 中指定阶段段落
- `get_phase_config` — 从 pipeline-config.json 读取阶段配置（python3 解析 JSON）
- `check_sanitize` — 扫描产出物中的 `javascript:` 链接、`<script>` 标签、路径遍历

**pipeline-check.sh 配置驱动调度（非硬编码）：**
```bash
# 从 pipeline-config.json 读取当前阶段的 artifacts 和 gate_rules
# macOS 无 jq，用 python3 解析
get_phase_config() {
  python3 -c "
import json, sys
with open('$CONFIG_FILE') as f:
    cfg = json.load(f)
for p in cfg['phases']:
    if p['id'] == '$PHASE':
        for a in p.get('artifacts', []):
            print(f\"artifact|{a['name']}|{a['min_lines']}|{a['required']}\")
        for r in p.get('gate_rules', []):
            print(f\"rule|{r}\")
        break
"
}

# 主循环：遍历配置中的 artifacts 做文件检查
while IFS='|' read -r TYPE ARG1 ARG2 ARG3; do
  case "$TYPE" in
    artifact) lib_check_file "$PROJECT_DIR/$ARG1" "$ARG2" "$ARG1" ;;
    rule)     eval_gate_rule "$ARG1" ;;  # 解析 "file_exists:X" / "file_lines:X:N" / "review_count:N" 等
  esac
done < <(get_phase_config)

# 按需调用子脚本（配置中无硬编码，由 gate_rules 触发）
check_knowledge
check_sanitize
```

### 4.3 prompt-builder.ts — 提示词构建

**已有功能：**
- 读取 SOUL.md（agent 身份定义）
- 读取 SKILL.md（技能说明，截取前 N 节）
- ROLE_TEMPLATES fallback（SOUL.md 不存在时）
- agent-discipline 条款注入

**需增强：**

| 功能 | 说明 | 优先级 |
|------|------|--------|
| CONTEXT.md 注入 | 读取项目 CONTEXT.md，注入当前阶段相关段落 | P0 |
| 上游产出摘要注入 | 注入当前阶段依赖的上游产出摘要 | P0 |
| 评审上下文注入 | 交叉评审阶段注入被评审物 + 相关评审 skill | P0 |
| 纪律条款注入 | 从 agent-discipline skill 读取对应角色条款 | P0 |
| Anti-Rationalization 注入 | 注入反借口规则表（PRD 652-665 行） | P1 |
| Brainstorm 检查 | brainstorm 阶段验证 brainstorm-log.md 存在且 ≥3 个 QA 对 | P1 |

**CONTEXT.md 段落选择逻辑：**
```
输入：当前 phase_id（如 "6" 或 "6.3"）
规则：
  1. 子阶段合并到父阶段段落（"6.3" → 读 "## 阶段6" 段落）
  2. 跨阶段引用（如阶段6需要阶段2的架构决策）→ 从 phase definition 的 dependencies 字段推导
  3. 注入格式：截取匹配段落，超过 50 行时截取首尾各 25 行 + 中间 "...省略 N 行..."
```

**prompt 结构：**
```
[1. SOUL.md / ROLE_TEMPLATES]     ← 身份定义
[2. SKILL.md 摘要]                 ← 技能说明（≤4K chars）
[3. agent-discipline 条款]         ← 执行纪律
[4. Anti-Rationalization 规则]     ← 反借口表（仅执行阶段注入）
[5. CONTEXT.md 相关段落]            ← 项目上下文（按段落选择逻辑）
[6. 上游产出摘要]                   ← 当前阶段的输入
[7. 阶段任务说明]                   ← 从 phase definition 生成
```

### 4.4 合同状态机（7 种状态）

```
                    ┌──────────────┐
         ┌─────────│  in-progress │─────────┐
         │         └──────┬───────┘         │
         │                │                 │
         │    ┌───────────┼───────────┐     │
         │    ▼           ▼           ▼     │
         │ ┌────────┐ ┌──────────┐ ┌───────┤
         │ │ signed │ │ revision-│ │escal- │
         │ │ (签收) │ │ requested│ │ated   │
         │ └────┬───┘ │ (打回)   │ │(升级) │
         │      │     └─────┬────┘ └───┬───┘
         │      │           │          │
         │      │     修订后重提     用户决策
         │      │           │          │
         │      │           ▼          ▼
         │      │     ┌──────────┐ ┌────────┐
         │      │     │in-progress│ │ closed │
         │      │     └──────────┘ └────────┘
         │      │
   回退触发│      │
         │      ▼
         │ ┌──────────┐      用户打断
         │ │ reopened ├───────────→ ┌────────┐
         │ └────┬─────┘            │ paused │
         │      │                  └───┬────┘
         └──────┤                      │
                │                用户恢复│
                ▼                      │
          ┌──────────────┐             │
          │  in-progress │←────────────┘
          └──────────────┘
```

**完整状态流转矩阵：**

| 当前状态 | 可转到 | 触发条件 |
|---------|--------|---------|
| in-progress | revision-requested | 评审者打回 |
| in-progress | signed | 评审者签收 |
| in-progress | escalated | 超时/轮次超限 |
| in-progress | paused | 用户打断 |
| revision-requested | in-progress | 修订后重提 |
| signed | reopened | 回退触发 |
| escalated | closed | 用户决策完成 |
| paused | in-progress | 用户恢复 |
| reopened | in-progress | 重新执行 |

**轮次限制：**
- 🟢低风险：最多 1 轮
- 🟡中风险：最多 2 轮
- 🔴高风险：最多 3 轮

**非法转转拒绝：** 任何不在上表中的转转，contract-check.sh 报错并拒绝。

### 4.5 Stale 文件生命周期管理

**问题：** 回退后，下游阶段产出物可能已过时，但不能直接删除（可能需要恢复）。

**生命周期：**
```
回退触发
  │
  ├─ 发现者写 changes/rollback-{id}.md（含根因、影响范围、目标阶段）
  ├─ orchestrator 标记受影响阶段的产出为 stale（_index.json status=reopened）
  │
  ▼
阶段重执行
  │
  ├─ 执行者开工前检查：读 _index.json，找 status=reopened 的产出
  ├─ 将 stale 文件移到 _rollback-backup/phase-N-{timestamp}/
  ├─ 创建空目录，开始重执行
  │
  ▼
重执行成功 → 正常推进
重执行失败 → 从 _rollback-backup/ 恢复最近备份 → 状态恢复为 rolled-back → 升级用户
```

**实现：** orchestrator.ts 的 `handleRollback` 方法扩展：
1. 计算影响范围（直接下游 / 全量重走）
2. 标记受影响阶段产出为 stale
3. 创建 `_rollback-backup/phase-N-{timestamp}/` 目录
4. 记录到 rollback_log

### 4.6 变更管理（3 级）

| 变更类型 | 前缀 | 计入额度 | 处理方式 |
|---------|------|---------|---------|
| 🟢 小调整 | `minor-` | 不计入 | 当前阶段内部消化 |
| 🟡 功能调整 | `change-` | 单独计（≤3次） | PM 更新 PRD → 受影响角色修改 → 交叉评审 1 轮 |
| 🔴 需求变更 | `rollback-` | 计入回退额度 | 回退阶段 1 重走流程 |

**实现：** `changes/` 目录下按前缀区分文件。contract-check.sh 统计各类型额度。

### 4.7 调度决策日志

**必须记录的 5 个决策点：**

| 决策点 | 决策者 | 记录位置 |
|--------|--------|---------|
| 规模判定（🟢/🟡/🔴） | 协调者 | changes/decision-log.md |
| 回退目标选择 | 发现者 | changes/rollback-{id}.md |
| 冒烟失败回退目标 | 创业助手 | changes/rollback-{id}.md |
| 🟡部分成功处理 | 协调者 | changes/decision-log.md |
| 并发冲突裁决 | 架构师 | changes/decision-log.md |

**格式：** `[时间] [阶段] [决策者] [决策内容] [理由]`

**实现：** contract-check.sh 验证每个决策点是否有对应日志条目。

### 4.8 知识库：CONTEXT.md

**格式：** 每阶段一个 `## 阶段N：{标题}` 段落，总行数 ≤200。

**更新时机：** 每个阶段执行者交付时，更新自己的段落。

**更新方式：** `lib_update_context` 函数用 awk 替换指定段落。

**回退一致性：** 回退后，受影响阶段的 CONTEXT.md 段落必须同步更新。`check_knowledge` 函数检查时间戳一致性。

---

## 5. 上下文复用机制

PRD 核心原则：**"评审即上下文建设，分配即上下文复用，派发只补变更"。**

### 5.1 交叉评审 → 上下文建设

阶段 1.5（PRD 交叉评审）中，架构师/QA/开发各自审阅 PRD 并产出评审意见。这些评审意见就是各角色对需求的理解。

### 5.2 任务分配 → 上下文复用

阶段 6 分配开发任务时：
- 审查过 PRD 的开发 → 优先分配其审查过的模块
- 审查过架构的 QA → 优先分配相关测试任务
- 不需要重新注入完整 PRD/架构，只需注入"你审查过的 X 模块分配给你，补充变更：Y"

### 5.3 实现方式

在 `pipeline-config.json` 的阶段定义中增加 `context_reuse` 字段：

```jsonc
{
  "id": "6",
  "name": "开发执行",
  "context_reuse": {
    "from_phase": "1.5",           // 从哪个阶段复用上下文
    "match_by": "review_role",     // 按角色匹配
    "inject": "review_summary"     // 注入评审摘要而非完整产出
  }
}
```

prompt-builder 读取此配置，在构建 prompt 时自动注入对应评审摘要。

---

## 6. 交叉评审调度流程

以阶段 1.5（PRD 交叉评审）为例：

```
协调者                        多个评审 agent
  │                              │
  ├─ pipeline_advance(1.5)       │
  │  → 解析 cross_review_roles   │
  │  → 为每个角色 resolveDispatch │
  │  → 生成 prompt（含 PRD 摘要） │
  │                              │
  ├──→ dispatch to architect ────┤
  ├──→ dispatch to qa ───────────┤
  ├──→ dispatch to dev1 ─────────┤
  ├──→ dispatch to ux-tester ────┤
  │                              │
  │   （并发评审，各自产出意见）    │
  │                              │
  │←── architect 评审意见 ────────┤
  │←── qa 评审意见 ───────────────┤
  │←── dev1 评审意见 ─────────────┤
  │←── ux-tester 评审意见 ────────┤
  │                              │
  ├─ 汇总评审意见                 │
  ├─ dispatch to pm（修订）       │
  │←── pm 修订后 PRD             │
  ├─ pipeline_gate(1.5)          │
  │  → 检查 cross-review-pm.md   │
  │  → 检查评审角色数 ≥ 阈值      │
  │→ pass → advance to 2         │
```

**并发控制：** 同一阶段最多 3 个 agent 并发。超过 3 个评审角色时分批派发。

---

## 7. 实现计划（MVP 14 步）

| # | 任务 | 依赖 | 产出 |
|---|------|------|------|
| M1 | 清理 pipeline-config.json 残留 reviewer 引用 | 无 | 配置文件更新 |
| M2 | 新增 `cross_review_roles` / `context_reuse` 字段到 PhaseDefinition 类型 | M1 | types.ts, schema.ts |
| M2b | 扩展 _index.json schema（transitions、7 种状态、checksum） | M1 | types.ts, state-manager.ts |
| M3 | 实现交叉评审调度逻辑（handleAdvance 并发派发） | M2 | orchestrator.ts |
| M4 | prompt-builder 增加 CONTEXT.md 注入（含段落选择逻辑） | 无 | prompt-builder.ts |
| M5 | prompt-builder 增加上游产出摘要注入 | M4 | prompt-builder.ts |
| M6 | prompt-builder 增加 agent-discipline 条款 + anti-rationalization 注入 | 无 | prompt-builder.ts |
| M7 | 创建 scripts/lib.sh 共享函数库（含 get_phase_config、check_sanitize） | 无 | lib.sh |
| M7b | 实现 stale 文件生命周期管理（_rollback-backup/ 目录结构） | M7 | orchestrator.ts |
| M8 | 创建 scripts/pipeline-check.sh 主入口（配置驱动） | M7 | pipeline-check.sh |
| M9 | 创建 scripts/review-check.sh 评审检查 | M7 | review-check.sh |
| M10 | 创建 scripts/contract-check.sh 合同检查（含 transitions 校验） | M7+M2b | contract-check.sh |
| M11 | 创建 scripts/test-report-check.sh 测试报告检查 | M7 | test-report-check.sh |
| M12 | 创建 scripts/acceptance-check.sh 验收检查 | M7+M10 | acceptance-check.sh |
| M13 | 合同状态机实现（7 种状态完整流转） | M2+M2b | orchestrator.ts |
| M14 | 上下文复用机制（context_reuse 配置 + prompt-builder 读取） | M4+M5 | prompt-builder.ts |
| M15 | Brainstorm 检查（brainstorm-log.md ≥3 QA 对） | M8 | gate-checker.ts |

**执行顺序：**
- 第一批（无依赖）：M1, M4, M6, M7
- 第二批（依赖第一批）：M2, M2b, M5, M7b, M8-M12
- 第三批（依赖第二批）：M3, M13, M14, M15

---

## 8. 关键接口

### 8.1 orchestrator.sh 输出格式（协调者调用）

```json
{
  "action": "dispatch",
  "phase": "1.5",
  "agents": [
    {
      "agent_id": "architect",
      "mode": "new",
      "model": "mimo-v2.5",
      "claude_session_id": "uuid-1",
      "cli_args": ["--session-id", "uuid-1", "-n", "pipeline:architect", "--model", "mimo-v2.5"]
    },
    {
      "agent_id": "qa",
      "mode": "resume",
      "model": "glm-5.1",
      "claude_session_id": "uuid-2",
      "cli_args": ["--resume", "uuid-2", "--model", "glm-5.1"]
    }
  ],
  "timeout_minutes": 60,
  "collect_strategy": "wait_all"
}
```

### 8.2 门禁检查结果

```json
{
  "status": "pass",
  "checks": [
    { "type": "file_exists", "artifact": "PRD.md", "result": "pass", "detail": "文件存在" },
    { "type": "file_lines", "artifact": "PRD.md", "result": "pass", "detail": "250行 ≥ 200行" },
    { "type": "review_count", "result": "warn", "detail": "3/4 评审角色完成" }
  ],
  "warnings": ["评审角色数不足：期望4，实际3"],
  "failures": []
}
```

### 8.3 合同签收/打回

```markdown
📋 合同 #c01 | architect → pm | 🟡中风险
━━━━━━━━━━━━━━━━━━━
交付：PRD.md
路径：.contracts/finder-app/phase-1-prd/PRD.md
验证：≥200行，包含假设清单、功能清单、验收标准
━━━━━━━━━━━━━━━━━━━
状态：✅ 签收 | 评分: 7.5 | 🟡1项: 假设清单缺少降级方案
```

---

## 9. 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| Claude Code session 过期 | agent 丢失上下文 | orchestrator 检测 session 无效时自动创建新 session |
| 并发 agent 文件冲突 | 代码合并失败 | 阶段 5 任务分解强制文件级独立 |
| 交叉评审超时 | 流水线阻塞 | 24h 时限 + 超时自动 escalation |
| CONTEXT.md 超 200 行 | token 浪费 | check_knowledge 强制检查行数 |
| 模型不可用 | 调度失败 | model_routing fallback 到默认模型 |

---

## 10. 与现有代码的映射

| 本文档组件 | 现有代码 | 状态 |
|-----------|---------|------|
| orchestrator.ts 状态机 | src/orchestrator.ts | ✅ 已实现（init/start/gate/advance/rollback/status/recover） |
| session 路由 | src/orchestrator.ts resolveDispatch | ✅ 已实现 |
| 模型路由 | pipeline-config.json model_routing | ✅ 已实现 |
| prompt-builder | src/prompt-builder.ts | 🟡 已有基础，需增强上下文注入 |
| gate-checker | src/gate-checker.ts | ✅ 已实现 |
| phase-resolver | src/phase-resolver.ts | ✅ 已实现 |
| state-manager | src/state-manager.ts | ✅ 已实现 |
| schema 校验 | src/schema.ts | ✅ 已实现（M2/M2b 需扩展） |
| 错误处理 | src/errors.ts + src/fs-port.ts | ✅ 已实现 |
| Shell 脚本层 | 不存在 | ❌ 待创建 |
| 合同状态机（7 种状态） | 不存在 | ❌ 待实现 |
| 交叉评审调度 | 不存在 | ❌ 待实现 |
| 上下文复用 | 不存在 | ❌ 待实现 |
| Stale 文件管理 | 不存在 | ❌ 待实现 |
| 变更管理（3 级） | 不存在 | ❌ 待实现 |
| 决策日志 | 不存在 | ❌ 待实现 |
