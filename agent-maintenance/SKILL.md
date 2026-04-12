# agent-maintenance — Agent 配置维护体系

## 是什么

Agent 和 Skill 配置的维护方法论、健康检查工具和创建模板。确保 agent 体系不会随时间膨胀退化。

**本 skill 无任何外部依赖，可独立使用。**

## 核心原则

### 1. 单一职责
- 一个 skill 只解决一个问题
- SOUL.md 只定义人格，不混入操作流程
- AGENTS.md 只定义职责和规则，不存放可复用内容

### 2. 解耦独立
- skill 之间不互相引用
- 可复用内容提取为独立 skill
- agent 不直接读取其他 agent 的文件

### 3. 按需加载
- 通用内容通过 agent.json 的 skills 字段注册
- 项目特定内容由协调者传入（TOOLS.md 占位符 `{协调者指定}`）
- 不把项目产出留在 workspace 根目录

### 4. 量化兜底
- 产出物行数不足 → 自动打回
- 审查报告无具体引用 → 视为敷衍
- 配置文件超阈值 → 健康检查报警

### 5. 版本管理
- 每次批量修改后 git commit
- 改之前先 branch（重大改动）
- 可回滚

## 文件结构规范

### Agent workspace 核心文件（仅这些会被注入上下文）
```
workspace/
├── AGENTS.md      ← 职责和规则（<200行）
├── SOUL.md        ← 人格定义（<80行）
├── TOOLS.md       ← 工具配置（填入实际命令）
├── USER.md        ← 用户信息（必须包含称呼和角色）
├── IDENTITY.md    ← 身份信息
├── HEARTBEAT.md   ← 心跳任务
└── memory/        ← 记忆（不自动注入）
```

### 文件职责边界

| 文件 | 放什么 | 不放什么 |
|------|--------|---------|
| SOUL.md | 人格、思维方式、口头禅、禁止事项 | 操作流程、检查清单、评分标准 |
| AGENTS.md | 职责、规则、执行纪律（引用） | 大段模板、可复用标准 |
| TOOLS.md | 命令、路径、环境配置 | 通用方法论 |
| USER.md | 用户称呼、角色说明 | 项目特定信息 |

### 文件大小阈值

| 文件 | 阈值 | 超出处理 |
|------|------|---------|
| SOUL.md | 80行 | 操作流程移到skill |
| AGENTS.md | 200行 | 可复用内容提取为skill |
| TOOLS.md | 无上限 | — |

## Skill 设计规范

### SKILL.md 必须包含
1. **是什么** — 一句话说明
2. **触发条件** — 什么时候用
3. **使用场景** — 流水线内/外的具体场景
4. **执行流程** — 具体步骤
5. **约束规则** — 必须遵守的规则
6. **无外部依赖声明** — 确保独立可用

### SKILL.md 行数
- 核心描述 < 100行
- 大内容（评分标准、模板）放 `templates/` 子目录

### 文件结构
```
my-skill/
├── SKILL.md           ← 使用说明（<100行）
└── templates/          ← 详细内容
    └── STANDARDS.md   ← 标准/模板
```

## 使用方法

### 健康检查（定期执行）
```bash
bash scripts/agent-health-check.sh
```

检查项：
1. 文件大小是否超阈值
2. TOOLS.md/USER.md 是否为空模板
3. 是否有重复文件（应使用skill）
4. workspace 是否有垃圾文件
5. skill 加载量是否过多（>10）
6. reviewer 是否用了强模型

### 创建新 Agent
```bash
bash scripts/create-pipeline-agent.sh <agent-id> <显示名> <角色类型> [模型]
```

角色类型：pm / architect / developer / reviewer / ui / ux / qa / startup-helper

自动生成：agent.json + 6个核心文件 + 按角色注册skill

### 提取可复用内容为 Skill
当多个 agent 共享相同内容时：
1. 创建 `~/.agents/skills/{skill-name}/`
2. 写 SKILL.md（使用说明）
3. 可复用内容放 `templates/`
4. 在 agent.json 中注册 skill
5. 从各 agent workspace 删除重复文件
6. 在 AGENTS.md 中加引用指向 skill

## 文件结构

```
agent-maintenance/
├── SKILL.md                              ← 本文件
└── scripts/
    ├── agent-health-check.sh            ← 健康检查脚本
    └── create-pipeline-agent.sh          ← Agent创建模板
```
