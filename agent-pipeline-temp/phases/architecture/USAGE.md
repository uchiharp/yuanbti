# 架构组 Pipeline 使用指南

在 Claude Code 中驱动架构组 Pipeline 的完整提示词集。

## 快速开始

```bash
# 前置条件：需求阶段已完成（requirements_done）
# 1. 查看断点状态
./pipeline-architecture.sh --project my-project --dir /path/to/project --status

# 2. 启动架构流水线
./pipeline-architecture.sh --project my-project --dir /path/to/project

# 3. 断点续跑（中断后直接重跑同命令）
./pipeline-architecture.sh --project my-project --dir /path/to/project
```

## 提示词规则

### 核心原则

1. **每个步骤一个提示词**，不要一次发多个步骤的指令
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
产出文件：
- {PROJECT_DIR}/ARCHITECTURE.md（≥100行）
- {PROJECT_DIR}/docker-compose.test.yml

## PRD 内容
{PRD.md 的内容}

## 阶段指令
{stages/01-arch-design.md 的内容}

## 架构模板
{templates/architecture-comprehensive.md 或 architecture-minimal.md 的内容}

## 工程健壮性规范（11项，必须覆盖）
{skills/engineering-robustness.md 的内容}

## 日志/异常规范
{skills/logging-exception.md 的内容}

## 约束
- 不要问用户"要继续吗"，直接执行
- 严格按照模板填写 ARCHITECTURE.md
- 必须包含 6 维度技术特性分析
- 必须包含 11 项工程健壮性设计
- 技术选型必须列出 ≥2 个备选方案对比
- 数据模型必须定义字段
- 风险识别至少 3 个
- 覆盖 PRD 中的所有 REQ
- ARCHITECTURE.md ≥100 行
- 标注高风险技术点
```

---

## Step 2: 质量评分

**无需提示词**。脚本自动调用 `arch_score_inline` 执行评分，直接输出结果。

---

## Step 3: 交叉评审 提示词

评分通过后，脚本暂停时使用：

```
你同时扮演四个角色对架构方案进行交叉评审。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}

## 架构方案
{ARCHITECTURE.md 的内容}

## PRD 内容
{PRD.md 的内容}

## 质量评分
{score}/{max_score}（{grade}）

## 评审规则
{references/arch-adversarial-review.md 的内容}

## 产出
将评审报告写入：{PROJECT_DIR}/cross-review-arch.md

## 四个评审角色
1. RD（开发视角）：技术可行性
2. 架构师视角：架构一致性
3. QA 视角：可测试性
4. PM 视角：需求完整性

## 约束
- 每个角色必须有独立评审段落和评分
- 阻断项 = 0 时，结论为"评审通过"
- 阻断项 > 0 时，结论为"评审未通过"
- 不要修改 ARCHITECTURE.md，只发现问题
```

---

## Step 4: 用户审阅 提示词

评审通过后，脚本暂停时使用：

```
将以下架构文档转换为 HTML。不要问"要继续吗"，收到任务直接执行。

## 架构文档内容
{ARCHITECTURE.md 的内容}

## HTML 要求
1. 响应式设计，支持桌面和移动端
2. 暗色主题（技术文档风格）
3. 代码块语法高亮
4. 左侧目录导航
5. 表格样式美观
6. 内联 CSS/JS（独立可打开）

## 产出
将 HTML 文件保存到：{PROJECT_DIR}/architecture-draft.html
```

---

## Step 5: 技术 Spike 提示词（条件触发）

只有 ARCHITECTURE.md 中有高风险标记时才触发：

```
你是 Spike Agent，对架构方案中的高风险技术点进行快速原型验证。不要问"要继续吗"，收到任务直接执行。

## 项目
项目名：{PROJECT}
项目目录：{PROJECT_DIR}
产出文件：{PROJECT_DIR}/SPIKE-REPORT.md

## 架构方案
{ARCHITECTURE.md 的内容}

## Spike 方法论
{skills/tech-spike.md 的内容}

## 约束
- 时间盒限制：单个 Spike ≤ 2h，总时间 ≤ 4h
- 只验证关键技术点，不做完整实现
- 每个 Spike 必须有明确结论
- 产出 SPIKE-REPORT.md
```

---

## 完整流程示例

```bash
# 前提：requirements pipeline 已完成

# Step 1: 启动架构 Pipeline
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
# → 脚本暂停，输出架构设计提示词

# Step 2: 把架构设计提示词发给 Claude Code
# → Claude 写出 ARCHITECTURE.md + docker-compose.test.yml

# Step 3: 重跑脚本（自动跳过已完成步骤）
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
# → 自动评分，然后暂停输出交叉评审提示词

# Step 4: 把交叉评审提示词发给 Claude Code
# → Claude 写出 cross-review-arch.md

# Step 5: 重跑脚本
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
# → 暂停输出用户审阅提示词

# Step 6: 重跑脚本（用户确认后）
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app
# → 条件触发 Spike → 入库

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

## 指定步骤运行

使用 `--step` 参数只执行某个步骤：

```bash
# 只执行架构设计
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app --step arch-design

# 只执行质量评分
./pipeline-architecture.sh --project task-app --dir ~/projects/task-app --step arch-quality-score
```

## 常用场景

| 场景 | 命令 |
|------|------|
| 强制指定规模 | `--size large` |
| CI 自动模式 | `--yes` |
| 只看断点不执行 | `--status` |
| 只跑某个步骤 | `--step arch-design` |
| 修改架构后重评 | 正常重跑（会自动重跑评分+评审） |

## 文件结构

```
project-dir/
├── pipeline.db                 # 状态数据库（与需求组共用）
├── PRD.md                      # 需求文档（需求组产出）
├── ARCHITECTURE.md             # Step 1 产出
├── docker-compose.test.yml     # Step 1 产出
├── cross-review-arch.md        # Step 3 产出
├── architecture-draft.html     # Step 4 产出
└── SPIKE-REPORT.md             # Step 5 产出（条件触发）
```

## 自动调度模式

设置 `DISPATCH_CMD` 环境变量，脚本会自动调用 AI 而不暂停：

```bash
# Claude Code CLI
DISPATCH_CMD='claude --print' ./pipeline-architecture.sh --project task-app --dir ~/projects/task-app --yes

# 自定义调度
DISPATCH_CMD='my-ai-client --input' ./pipeline-architecture.sh --project task-app --dir ~/projects/task-app --yes
```

## 架构组与需求组的关系

```
requirements pipeline → requirements_done → architecture pipeline → architecture_done
       ↓                                            ↓
  PRD.md (12 REQ)                          ARCHITECTURE.md
                                            features: PRD-已确认 → 技术方案-已确认
```

两个 pipeline 共用 `pipeline.db`，通过 `phase` 字段和 `current_phase` 区分阶段。
