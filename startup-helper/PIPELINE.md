# PIPELINE.md — 流水线调度手册

> 这是协调者的核心文件。每次收到流水线任务，先读这个文件。

## 前置文件

每次调度前必须读取：

| 文件 | 用途 |
|------|------|
| `agent-pipeline/stages/stage-X.md` | 当前阶段的具体指令 |
| `agent-pipeline/skill-registry.md` | 每阶段加载哪些 Skill |
| `agent-pipeline/SCRIPT-SKILL-FLOW.md` | 流程总览（阶段间关系） |
| `agent-pipeline/scripts/pipeline-check.sh` | 检查脚本（验证产出物） |

## 阶段 → Agent 调度表

| 阶段 | 派给谁 | Agent 目录 | 说明 |
|------|--------|-----------|------|
| 0 | 自己做 | — | 启动阶段，协调者自己评估规模 |
| 1 | PM | `pm/` | 产出 PRD |
| 1.5 | QA + 开发 + 架构师 | `qa/` + `dev1/` + `architect/` | 并发评审 PRD |
| 2 | 架构师 | `architect/` | 产出架构方案 |
| 2.5 | 开发 + QA | `dev1/` + `qa/` | 并发评审架构 |
| 2.8 | Spike agent | — | 技术验证（条件执行） |
| 3 | UX | `ux-tester/` | 产出 UX 设计 |
| 3.5 | UI | `ui-designer/` | UX→UI 交接确认 |
| 4 | UI | `ui-designer/` | 产出 UI 设计 |
| 4.5 | UX | `ux-tester/` | UI→UX 反向确认 |
| 5 | 协调者 + QA | 自己做 + `qa/` | 任务分解 + 测试计划（并发） |
| 5.5 | 开发 | `dev1/` | 确认任务分配 |
| 6 | 开发×3 + QA | `dev1/` + `dev2/` + `dev3/` + `qa/` | 编码 + E2E 测试（并发） |
| 6.3 | 开发 | `dev1/` | 代码集成 + 冒烟 |
| 6.5 | 架构师 | `architect/` | 架构审查 |
| 7 | 架构师 + QA | `architect/` + `qa/` | 代码审查 |
| 8 | QA | `qa/` | 测试验证 |
| 8.5 | PM | `pm/` | PM 验收（对照 PRD 验证测试报告） |
| 9 | 自己做 | — | 交付验收 + HTML 转换 |

## 调度方式：acpx 命令

协调者通过 `acpx` 命令行调度 agent。**不要自己执行任务，用 acpx 派发。**

### Session 规则（强制）

**每个 agent 绑定一个持久 Claude Code session，直到项目切换。**

Session 命名格式：`{project}-{agent-id}`

| Agent ID | Session 名 | 说明 |
|----------|-----------|------|
| `pm` | `{project}-pm` | PM agent |
| `architect` | `{project}-architect` | 架构师 |
| `dev1` | `{project}-dev1` | 全栈开发1 |
| `dev2` | `{project}-dev2` | 全栈开发2 |
| `dev3` | `{project}-dev3` | 全栈开发3 |
| `qa` | `{project}-qa` | QA |
| `ux-tester` | `{project}-ux` | UX 设计 |
| `ui-designer` | `{project}-ui` | UI 设计 |

### 项目开始：创建所有 Session

```bash
PROJECT="film-auth"  # 项目名

# 为每个 agent 创建命名 session
for AGENT in pm architect dev1 dev2 dev3 qa ux-tester ui-designer; do
  acpx claude sessions new --name "${PROJECT}-${AGENT}" --cwd /Users/sunwenyong/.openclaw/agents/${AGENT}/workspace
done
```

### 项目切换：关闭旧 Session，创建新 Session

```bash
# 关闭旧项目的所有 session
acpx claude sessions list | grep "old-project-" | xargs -I{} acpx claude --session {} sessions close

# 创建新项目的 session
for AGENT in pm architect dev1 dev2 dev3 qa ux-tester ui-designer; do
  acpx claude sessions new --name "new-project-${AGENT}" --cwd /Users/sunwenyong/.openclaw/agents/${AGENT}/workspace
done
```

### 基本调度格式

```bash
acpx claude --session "{project}-{agent-id}" --cwd {agent工作目录} --approve-all --format json --timeout 3600 "{任务prompt}"
```

### 调度示例

```bash
# 阶段1：派给 PM（使用持久 session）
acpx claude --session "film-auth-pm" \
  --cwd /Users/sunwenyong/.openclaw/agents/pm/agent \
  --approve-all --format json --timeout 3600 \
  "你是PM，执行阶段1：需求分析。
   必读文件：/path/to/PRD.md
   加载 Skill：requirements-analysis（读取 /path/to/SKILL.md）
   任务：和用户讨论需求，产出PRD.md ≥200行。
   产出路径：/path/to/project/1/PRD.md"

# 阶段2：派给架构师（复用同一 session，保留阶段1的上下文）
acpx claude --session "film-auth-architect" \
  --cwd /Users/sunwenyong/.openclaw/agents/architect/agent \
  --approve-all --format json --timeout 3600 \
  "你是架构师，执行阶段2：架构设计。
   必读文件：/path/to/PRD.md
   加载 Skill：tech-architecture, logging-exception
   任务：基于PRD产出ARCHITECTURE.md ≥100行。
   产出路径：/path/to/project/2/ARCHITECTURE.md"

# 阶段6：派给开发（复用 session，保留之前的代码上下文）
acpx claude --session "film-auth-dev1" \
  --cwd /Users/sunwenyong/.openclaw/agents/dev1/workspace \
  --approve-all --format json --timeout 3600 \
  "你是开发，执行阶段6：开发执行。
   必读文件：docs/ARCHITECTURE.md, docs/CODE-MAP.md, TASK-LIST.md
   加载 Skill：code-quality-guard, logging-exception
   任务：按任务清单开发代码。
   产出路径：/path/to/project/6/"
```

### 并发调度

多个 agent 可以同时派发（不同 session 互不干扰）：

```bash
# 阶段5：协调者（任务分解）+ QA（测试计划）并发
# 协调者自己做任务分解，同时派 QA 写测试计划
acpx claude --session "film-auth-qa" ... "测试计划..." &
# 协调者自己执行 task-decomposition Skill...
acpx claude --session "film-auth-qa" ... "测试计划..." &
wait  # 等待两个都完成
```

### 调度后验证

agent 完成后，运行检查脚本：

```bash
bash /path/to/agent-pipeline/scripts/pipeline-check.sh {项目目录} {阶段号}
```

### 任务 Prompt 模板

```
你是 {角色}，执行阶段 {X}：{名称}。不要问"要继续吗"，收到任务直接执行。

## 启动自检（先做）
1. 读取 SOUL.md — 确认你的角色和性格
2. 读取 AGENTS.md — 确认你的工作规范和约束

## 必读文件（按顺序）
1. {文件1}
2. {文件2}

## 加载 Skill
- {skill1} — 读取 /Users/sunwenyong/.openclaw/agents/{skill1}/SKILL.md
- {skill2} — 读取 /Users/sunwenyong/.openclaw/agents/{skill2}/SKILL.md

## 任务
{从 stages/stage-X.md 复制任务描述}

## 产出物
- {文件名} — 最低 {N} 行

## 约束
- 合同：{风险等级} 最多 {N} 轮
- {其他约束}

## 决策规则（遇到选择时按此执行）

### 技术决策
- 技术选型不确定 → 选团队最熟悉的，不选最新最火的
- 方案有多个 → 选最简单的，不过度设计
- 框架版本不确定 → 选最新 LTS 稳定版
- 数据库选型 → 默认 PostgreSQL，已有 MySQL 就用 MySQL

### 产品决策
- 功能优先级不确定 → P0（核心流程）> P1（重要）> P2（优化）
- 需求不明确 → 先做最小可用版本，不要猜测用户意图
- 交互方式有争议 → 选用户最熟悉的（业界通用模式）

### 架构决策
- 分层不确定 → Controller → Service → Repository 三层
- 模块划分不确定 → 按业务域划分（用户、权限、项目）
- 设计模式不确定 → 简单 CRUD 不用模式，复杂场景才用

### 需要用户确认时
写入 `{project}/questions.md`，格式：
```markdown
## 待确认问题
1. {问题描述}
   - 选项A：{说明}（推荐）
   - 选项B：{说明}
```
通知协调者，协调者转发给用户。等用户回答后再继续。

## 完成后
产出文件写入 {project_path}/{phase}/ 目录。
完成后通知协调者。
```

## 检查脚本调用

每阶段 agent 完成后，运行：

```bash
bash agent-pipeline/scripts/pipeline-check.sh <项目目录> <阶段号>
```

### 结果处理

| exit code | 含义 | 动作 |
|-----------|------|------|
| 0（无警告） | 全部通过 | 推进下一阶段 |
| 0（有警告） | 通过但有建议 | 推进，记录警告 |
| 1 | 不通过 | 把错误列表发给 agent，要求补全 |

### 轮次控制

| 合同等级 | 最大轮次 | 超限动作 |
|---------|---------|---------|
| 🟡 中风险 | 2 轮 | 升级给用户 |
| 🔴 高风险 | 3 轮 | 升级给用户 |

## 阶段间依赖

```
0 → 1 → 1.5(🟡/🔴) → 2 → 2.5 → [2.8] → 3 → 3.5 → 4 → 4.5 → 5 → 5.5 → 6 → 6.3 → 6.5 → 7 → 8 → 9
```

### 可并发的阶段

- 1.5：架构师 + QA + 开发（并发评审）
- 2.5：开发 + QA（并发评审）
- 5：协调者（任务分解）+ QA（测试计划）
- 6：开发（编码）+ QA（E2E测试）
- 7：架构师 + QA（并发审查）

### 可跳过的阶段（🟢 小型项目）

1.5, 2.5, 3.5, 4.5, 5.5, 6.3, 6.5

## 回退流程

```
发现问题 → 记录到 changes/ → 决定回退目标
  → 检查回退次数（总≤5，连续≤2）
  → 调度对应 agent 修正
  → 修正完成后重新检查
  → 超限 → 暂停，升级给用户
```

## docs/ 归档检查

阶段 2 起，每阶段检查 `docs/` 目录是否有已签收阶段的归档文档：

| 从哪个阶段起检查 | 检查文件 |
|-----------------|---------|
| 阶段 2 | docs/PRD.md |
| 阶段 2.5 | docs/CODE-MAP.md |
| 阶段 2.8 | docs/ARCHITECTURE.md |
| 阶段 5.5 | docs/QA-TEST-STRATEGY.md |
| 阶段 7 | docs/dev-log.md |

## 交付文档（阶段 9）

| 文件 | 最低行数 | 说明 |
|------|---------|------|
| docs/user-manual.md | 100 | 用户使用手册 |
| docs/api-docs.md | — | API 接口文档 |
| docs/rpc-api-docs.md | — | RPC 接口文档 |
| docs/integration-guide.md | — | 接入指南（必须含步骤说明） |

## 常见问题

**Q: agent 不读必读文件怎么办？**
A: pipeline-check.sh 有 `check_input_references` 检查，不通过就打回。

**Q: agent 自己做了所有事不派发怎么办？**
A: 你是协调者，不是执行者。读 PIPELINE.md，按调度表派发。

**Q: 脚本报错但 agent 说完成了怎么办？**
A: 信任脚本，不信任 agent。脚本说不通过就是不通过。
