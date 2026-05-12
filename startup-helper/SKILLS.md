# SKILLS.md — 协调者技能

## 流水线调度（核心技能）

| 技能 | 用途 | 触发场景 |
|------|------|----------|
| **agent-pipeline** | 流水线全流程定义 | 收到"开始开发"/"做项目"任务时 |
| **acpx** | 调度其他 agent | 每个阶段需要派发任务时 |
| **pipeline-check.sh** | 验证产出物 | 每阶段 agent 完成后 |

### 调度流程

```
读 stages/stage-X.md → 组装 prompt → acpx 派发 → 等完成 → pipeline-check.sh → 通过/打回
```

### 调度命令速查

```bash
# 创建命名 session
acpx claude sessions new --name "{project}-{agent-id}" --cwd {agent/workspace目录}

# 派发任务
acpx claude --session "{project}-{agent-id}" --cwd {agent/workspace目录} --approve-all --format json --timeout 3600 "{任务prompt}"

# 并发派发（用 & 和 wait）
acpx claude --session "{project}-dev1" --cwd /Users/sunwenyong/.openclaw/agents/dev1/workspace --approve-all --format json --timeout 3600 "{任务}" &
acpx claude --session "{project}-dev2" --cwd /Users/sunwenyong/.openclaw/agents/dev2/workspace --approve-all --format json --timeout 3600 "{任务}" &
wait

# 验证产出
bash /Users/sunwenyong/.openclaw/agents/agent-pipeline/scripts/pipeline-check.sh {项目目录} {阶段号}
```

## 创业辅导（非流水线时）

| 技能 | 用途 | 触发场景 |
|------|------|----------|
| **task-decomposition** | 任务拆分 | 阶段5任务分解 |
| **web_search** | 网络搜索 | 市场调研、竞品分析 |

## 飞书集成

| 技能 | 用途 |
|------|------|
| **feishu-doc** | 飞书文档读写 |
| **feishu-drive** | 飞书云盘管理 |
| **feishu-wiki** | 飞书知识库 |
| **feishu-media** | 下载飞书消息中的图片/视频/文件 |

飞书 App ID: `cli_a944cc3f77b89bd2`

## 可调度的 Agent 列表

| Agent ID | 目录 | 用途 |
|----------|------|------|
| `pm` | `agents/pm/workspace` | 需求分析、PRD |
| `architect` | `agents/architect/workspace` | 架构设计 |
| `dev1` | `agents/dev1/workspace` | 全栈开发1 |
| `dev2` | `agents/dev2/workspace` | 全栈开发2 |
| `dev3` | `agents/dev3/workspace` | 全栈开发3 |
| `qa` | `agents/qa/workspace` | 测试 |
| `ux-tester` | `agents/ux-tester/workspace` | UX 设计 |
| `ui-designer` | `agents/ui-designer/workspace` | UI 设计 |

## Skill 加载规则

协调者**不加载**业务 Skill（如 `tech-architecture`、`code-quality-guard`）。这些 Skill 由对应 agent 在被调度时加载。

协调者只用：`agent-pipeline`（流程定义）+ `acpx`（调度工具）+ `pipeline-check.sh`（验证脚本）
