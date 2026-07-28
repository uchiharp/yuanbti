# 架构师 Pipeline 使用指南

在 Claude Code 中驱动架构师 Pipeline 的完整提示词集。

## 快速开始

```bash
# 前提：需求阶段已完成（requirements_done）
# 1. 初始化项目（只跑一次）
./pipeline-architecture.sh --project my-project --dir /path/to/project

# 2. 查看断点状态
./pipeline-architecture.sh --project my-project --dir /path/to/project --status

# 3. 跳过已有步骤继续
./pipeline-architecture.sh --project my-project --dir /path/to/project --skip-arch-design
```

## 提示词规则

### 核心原则

1. **每个阶段一个提示词**，不要一次发多个阶段的指令
2. **提示词里的路径必须和 `--dir` 一致**，否则产出文件找不到
3. **脚本暂停时才用提示词**，脚本自动跑的步骤（评分）不需要
4. **完成后重新运行脚本**，不要手动继续下一步

### 使用模式

| 模式 | 何时用 | 怎么做 |
|------|--------|--------|
| **交互模式** | 默认 | 脚本暂停 → 复制提示词给 Claude → 完成 → 重跑脚本 |
| **自动模式** | CI/批量 | 设置 `DISPATCH_CMD` + `--yes`，脚本自动调度 AI |
| **断点续跑** | 中断后 | 直接重跑同命令，已完成的步骤自动跳过 |

---

## Step 1: 架构设计 提示词

脚本运行后会在终端输出提示词，也可直接用以下模板：

```
你是架构师，基于已确认的 PRD 产出技术架构方案。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}
规模：{size}
产出文件：{PROJECT_DIR}/ARCHITECTURE.md

## PRD 内容
{PRD.md 的内容}

## 阶段指令
{stages/01-arch-design.md 的内容}

## 技术架构 Skill
{skills/tech-architecture.md 的内容}

## 工程健壮性 Skill
{skills/engineering-robustness.md 的内容}

## 日志异常 Skill
{skills/logging-exception.md 的内容}

## 架构模板
{templates/architecture-comprehensive.md 或 architecture-minimal.md 的内容}

## 产出路径
所有产出文件写入：{PROJECT_DIR}/

## 完成后
产出 ARCHITECTURE.md + docker-compose.test.yml 后通知用户确认。

## 约束
- 不要问用户"要继续吗"，直接执行
- 必须读取 PRD（不能靠记忆或概括）
- 技术选型必须列出对比（≥2个备选）
- 数据模型必须定义字段
- 风险识别至少3个
- 6维度技术特性分析不能遗漏
- 11项工程健壮性设计不能遗漏
```

**执行方式**：直接在 Claude Code 会话中发送，Claude 会产出架构方案。确认后重跑脚本。

---

## Step 2: 架构质量评分

**无需提示词**。脚本自动调用 `arch_score_inline` 执行评分，直接输出结果。

---

## Step 3: 架构交叉评审 提示词

评分通过后，脚本暂停时使用：

```
你同时扮演四个角色对架构方案进行交叉评审。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}

## ARCHITECTURE 内容
{ARCHITECTURE.md 的内容}

## PRD 内容
{PRD.md 的内容}

## 质量评分
{score}/{max_score}（{grade}）

## 评审规则
{references/arch-adversarial-review.md 的内容}

## 产出
将评审报告写入：{PROJECT_DIR}/cross-review-arch.md

## 约束
- 严格按输出格式写评审报告
- 阻断项 = 0 时，结论为"评审通过"
- 阻断项 > 0 时，结论为"评审未通过"
- 不要修改 ARCHITECTURE.md，只发现问题
```

---

## Step 4: 用户审阅 提示词

```
将 ARCHITECTURE.md 转成 HTML 格式，保存到 docs/architecture-draft.html。
HTML 要求：保留标题层级、表格正常渲染、代码块语法高亮、浏览器可独立打开。
```

---

## Step 5: 技术 Spike 提示词

当架构中有高风险标记时触发：

```
读取 ARCHITECTURE.md 中的高风险技术点，执行 Spike 验证。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}

## ARCHITECTURE 内容
{ARCHITECTURE.md 中的风险相关章节}

## Spike 模板
{references/spike-template.md 的内容}

## 产出
将 Spike 报告写入：{PROJECT_DIR}/SPIKE-REPORT.md

## 约束
- 时间上限 4 小时
- 只验证关键技术点，不做完整实现
- 结论必须明确：✅/🟡/❌
```

---

## 完整流程示例

以项目 `task-app` 为例：

```bash
# Step 0: 确保需求阶段已完成
./pipeline-requirements.sh --project task-app --dir ~/projects/task-app --status

# Step 1: 启动架构 Pipeline
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
# → 脚本暂停，输出架构设计提示词

# Step 2: 把架构设计提示词发给 Claude Code
# → Claude 写出 ~/projects/task-app/ARCHITECTURE.md + docker-compose.test.yml

# Step 3: 重跑脚本（自动跳过架构设计）
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
# → 自动评分，然后暂停输出交叉评审提示词

# Step 4: 把交叉评审提示词发给 Claude Code
# → Claude 写出 ~/projects/task-app/cross-review-arch.md

# Step 5: 重跑脚本（自动跳过已完成步骤）
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
# → 用户审阅 → Spike（如有高风险）→ 入库

# 随时查看状态
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app --status
```

## 断点续跑

Pipeline 任何步骤中断后，直接重跑同命令：

```bash
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
```

脚本会：
1. 检查 DB 中每个步骤的状态
2. 已完成的步骤显示 ⏩ 跳过
3. 从断点步骤继续执行
4. `--status` 只看不动，不执行任何步骤

## 常用场景

| 场景 | 命令 |
|------|------|
| 已有架构方案，跳过设计 | `--skip-arch-design` |
| 强制指定规模 | `--size large` |
| CI 自动模式 | `--yes` |
| 只看断点不执行 | `--status` |
| 修改架构后重评 | 正常重跑（会自动重跑评分+评审） |

## 文件结构

```
project-dir/
├── pipeline.db              # 状态数据库（与需求阶段共用）
├── PRD.md                   # 需求阶段产出
├── ARCHITECTURE.md          # 架构设计产出
├── docker-compose.test.yml  # 测试环境定义
├── cross-review-arch.md     # 交叉评审产出
├── architecture-feedback.md # 用户反馈记录
├── SPIKE-REPORT.md          # Spike 报告（如有）
└── docs/
    └── architecture-draft.html  # HTML 版本
```

## 自动调度模式

设置 `DISPATCH_CMD` 环境变量，脚本会自动调用 AI 而不暂停：

```bash
# Claude Code CLI
DISPATCH_CMD='claude --print' ./pipeline-architecture.sh --project task-app --dir ~/projects/task-app --yes

# 自定义调度
DISPATCH_CMD='my-ai-client --input' ./pipeline-architecture.sh --project task-app --dir ~/projects/task-app --yes
```
