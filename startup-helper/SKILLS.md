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

### acpx 命令速查

```bash
# 派发任务给 agent（唯一正确方式）
acpx claude --session "{project}-{agent-id}" --cwd {agent工作目录} --approve-all --format json --timeout 3600 "{prompt}"

# 并发派发（多个 agent 同时执行）
acpx claude --session "{project}-architect" --cwd /Users/sunwenyong/.openclaw/agents/architect/agent --approve-all --format json --timeout 3600 "{prompt1}" &
acpx claude --session "{project}-qa" --cwd /Users/sunwenyong/.openclaw/agents/qa/agent --approve-all --format json --timeout 3600 "{prompt2}" &
wait

# 验证产出
bash /Users/sunwenyong/.openclaw/agents/agent-pipeline/scripts/pipeline-check.sh {项目目录} {阶段号}
```

**⚠️ 禁止使用 `sessions_spawn`、`subagent` 或任何非 acpx 的调度方式。**

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
| `pm` | `agents/pm/agent` | 需求分析、PRD |
| `architect` | `agents/architect/agent` | 架构设计 |
| `backend` | `agents/backend/agent` | 后端开发 |
| `frontend` | `agents/frontend/agent` | 前端开发 |
| `qa` | `agents/qa/agent` | 测试 |
| `ux-tester` | `agents/ux-tester/agent` | UX 设计 |
| `ui-designer` | `agents/ui-designer/agent` | UI 设计 |
| `backend-reviewer` | `agents/backend-reviewer` | 代码审查 |
| `architect-reviewer` | `agents/architect-reviewer` | 架构审查 |
| `qa-reviewer` | `agents/qa-reviewer` | QA 审查 |
| `pm-reviewer` | `agents/pm-reviewer` | PRD 审查 |

## Skill 加载规则

协调者**不加载**业务 Skill（如 `tech-architecture`、`code-quality-guard`）。这些 Skill 由对应 agent 在被调度时加载。

协调者只用：`agent-pipeline`（流程定义）+ `acpx`（调度工具）+ `pipeline-check.sh`（验证脚本）
