# 架构师 Pipeline 使用指南

在 Claude Code 中驱动架构师 Pipeline 的完整提示词集。

## 快速开始

```bash
# 前提：需求阶段已完成（current_phase = requirements_done）
# 查看项目状态
sqlite3 ~/projects/my-project/pipeline.db "SELECT current_phase FROM projects WHERE name='my-project';"

# 1. 启动架构师 pipeline
./pipeline-architecture.sh --project my-project --dir /path/to/project

# 2. 查看断点状态
./pipeline-architecture.sh --project my-project --dir /path/to/project --status

# 3. 跳过已有步骤继续
./pipeline-architecture.sh --project my-project --dir /path/to/project --skip-arch-design
```

## 前置条件

| 条件 | 检查方式 |
|------|---------|
| 需求阶段已完成 | `SELECT current_phase FROM projects` = `requirements_done` |
| PRD.md 存在且非空 | 文件系统检查 |
| pipeline.db 存在 | 文件系统检查 |

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

## Step 1: arch-design — 架构设计 提示词

脚本运行后会在终端输出提示词，也可直接用以下模板：

```
你是架构师，执行架构设计阶段。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}
规模：{SIZE}
产出文件：{PROJECT_DIR}/ARCHITECTURE.md, {PROJECT_DIR}/docker-compose.test.yml

## 必读文件
1. {PROJECT_DIR}/PRD.md
2. {stages/01-arch-design.md 的内容}

## 加载 Skill
- skills/tech-architecture.md
- skills/engineering-robustness.md
- skills/logging-exception.md

## 产出路径
所有产出文件写入：{PROJECT_DIR}/

## 完成后
产出 ARCHITECTURE.md 和 docker-compose.test.yml 后通知用户确认。

## 约束
- 不要问用户"要继续吗"，直接执行
- 技术选型必须列出对比（≥2个备选）
- 数据模型必须定义字段（不能只写表名）
- 风险识别至少3个
- 6 维度技术特性分析不能遗漏
- 11 项工程健壮性设计不能遗漏
- ARCHITECTURE.md ≥100行
- docker-compose.test.yml 必须产出
```

**执行方式**：直接在 Claude Code 会话中发送。完成后重跑脚本。

---

## Step 2: arch-quality-score — 架构质量评分

**无需提示词**。脚本自动调用 `arch_score_inline` 执行评分，直接输出结果。

---

## Step 3: arch-review — 架构交叉评审 提示词

评分通过后，脚本暂停时使用：

```
你同时扮演四个角色对架构方案进行交叉评审。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}

## 架构文档
{PROJECT_DIR}/ARCHITECTURE.md 的内容

## PRD
{PROJECT_DIR}/PRD.md 的内容

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

**执行方式**：发送后 Claude 直接产出 cross-review-arch.md，检查结果后重跑脚本。

---

## Step 4: arch-user-review — 架构用户审阅 提示词

```
你是架构师，将 ARCHITECTURE.md 转成 HTML 供用户审阅。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}

## 架构文档
{PROJECT_DIR}/ARCHITECTURE.md 的内容

## 产出
将 HTML 版本写入：{PROJECT_DIR}/docs/architecture-draft.html

## 约束
- 单文件、内联 CSS、无外部依赖
- 暗色主题（GitHub Dark 风格）
- 表格/标题/代码块样式清晰
- 响应式布局，移动端可读
- 包含锚点目录
```

**执行方式**：发送后 Claude 产出 HTML。协调者通知用户审阅，用户确认后重跑脚本。

---

## Step 5: tech-spike — 技术 Spike（条件触发）

**仅当 ARCHITECTURE.md 包含高风险标记时触发**。

```
你执行技术 Spike 验证。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}

## 架构文档
{PROJECT_DIR}/ARCHITECTURE.md 的内容

## Spike 指令
{stages/04-tech-spike.md 的内容}

## Spike 模板
{templates/spike-report.md 的内容}

## 产出
将 Spike 报告写入：{PROJECT_DIR}/SPIKE-REPORT.md

## 约束
- Spike 时间上限 4 小时
- 只验证关键技术点，不做完整实现
- 验证代码不合并到主分支
- 每个风险点必须有明确结论（通过/不通过/有条件通过）
```

---

## Step 6: arch-finalize — 架构阶段完成

**无需提示词**。脚本自动完成：
- 更新项目状态为 `design_done`
- 注册产出物到 artifacts 表
- 更新功能点标签为 `ARCH-已设计`

---

## 完整流程示例

以项目 `my-app` 为例：

```bash
# Step 0: 确认需求阶段已完成
sqlite3 ~/projects/my-app/pipeline.db "SELECT current_phase FROM projects;"

# Step 1: 启动 Pipeline
./pipeline-architecture.sh --project my-app --dir ~/projects/my-app
# → 脚本暂停，输出架构设计提示词

# Step 2: 把架构设计提示词发给 Claude Code
# → Claude 写出 ~/projects/my-app/ARCHITECTURE.md 和 docker-compose.test.yml

# Step 3: 重跑脚本（自动跳过架构设计）
./pipeline-architecture.sh --project my-app --dir ~/projects/my-app
# → 自动评分，然后暂停输出交叉评审提示词

# Step 4: 把交叉评审提示词发给 Claude Code
# → Claude 写出 ~/projects/my-app/cross-review-arch.md

# Step 5: 重跑脚本（自动跳过已完成步骤）
./pipeline-architecture.sh --project my-app --dir ~/projects/my-app
# → 暂停输出用户审阅提示词

# Step 6: 用户审阅完成后重跑
./pipeline-architecture.sh --project my-app --dir ~/projects/my-app
# → 如有高风险标记，暂停输出 Spike 提示词；否则直接完成

# 随时查看状态
./pipeline-architecture.sh --project my-app --dir ~/projects/my-app --status
```

## 断点续跑

Pipeline 任何步骤中断后，直接重跑同命令：

```bash
./pipeline-architecture.sh --project my-app --dir ~/projects/my-app
```

脚本会：
1. 检查 DB 中每个步骤的状态
2. 已完成的步骤显示 ⏩ 跳过
3. 从断点步骤继续执行
4. `--status` 只看不动，不执行任何步骤

## 常用场景

| 场景 | 命令 |
|------|------|
| 已有 ARCHITECTURE.md，跳过设计 | `--skip-arch-design` |
| 强制指定规模 | `--size large` |
| CI 自动模式 | `--yes` |
| 只看断点不执行 | `--status` |
| 修改架构后重评 | 正常重跑（会自动重跑评分+评审） |

## 文件结构

```
project-dir/
├── pipeline.db                    # 状态数据库（共享）
├── ARCHITECTURE.md                # Step 1 产出
├── docker-compose.test.yml        # Step 1 产出
├── cross-review-arch.md           # Step 3 产出
├── docs/architecture-draft.html   # Step 4 产出
├── architecture-feedback.md       # Step 4 用户反馈
├── SPIKE-REPORT.md                # Step 5 产出（条件）
└── docs/                          # 其他文档
```

## 自动调度模式

设置 `DISPATCH_CMD` 环境变量，脚本会自动调用 AI 而不暂停：

```bash
# Claude Code CLI
DISPATCH_CMD='claude --print' ./pipeline-architecture.sh --project my-app --dir ~/projects/my-app --yes

# 自定义调度
DISPATCH_CMD='my-ai-client --input' ./pipeline-architecture.sh --project my-app --dir ~/projects/my-app --yes
```

## 与需求 Pipeline 的衔接

```
需求 Pipeline 完成（requirements_done）
  → 架构 Pipeline 启动
    → 读取 features 表中的 REQ-xxx
    → 基于 PRD.md 设计架构
    → 完成后状态变为 design_done
      → 下一步：任务分解 Pipeline
```

## 高风险标记触发 Spike

架构设计中如果出现以下标记，脚本会自动触发 tech-spike 步骤：

```markdown
<!-- HIGH-RISK: 技术选型不确定，需要验证 -->
<!-- SPIKE: 需要验证第三方API兼容性 -->
<!-- RISK: 高并发场景性能未验证 -->
```

或者在"风险识别"章节中包含 `高风险` / `Spike` / `需验证` 等关键词。
