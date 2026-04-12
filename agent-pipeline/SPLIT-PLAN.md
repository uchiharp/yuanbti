# Agent-Pipeline v4 拆分计划

## 拆分原则

1. **骨架最小化** — agent-pipeline 只保留编排逻辑和跨阶段规则
2. **细则独立化** — 每个阶段的方法论拆成小 skill
3. **可独立使用** — 小 skill 不依赖 pipeline 上下文，任何 agent 都可加载
4. **单一信息源** — 骨架引用小 skill，不复制内容

---

## 拆分结果总览

```
agent-pipeline（骨架 · ~400行）
  │  保留：流程图、角色配置、通信规则、回退/容错/防偷懒
  │  保留：阶段3/4/6/7/9 的简要编排说明（无细则）
  │
  ├─ references/（目录内参考文件，不变）
  │
  ├─ requirements-analysis skill（阶段1细则 · ~150行）
  ├─ tech-architecture skill（阶段2细则 · ~150行）
  ├─ tech-spike skill（阶段2.8细则 · ~100行）
  ├─ task-decomposition skill（阶段5细则 · ~200行）
  │
  └─ 已有 skill（不拆，引用即可）
     ├─ code-review-checklist（阶段6.5细则）
     ├─ qa-workflow（阶段8细则）
     ├─ code-quality-guard（编码检查）
     └─ humanize-code（去AI味）
```

---

## 一、agent-pipeline 骨架（~400行）

**保留的内容：**

| 章节 | 行数(估) | 原因 |
|------|---------|------|
| YAML front matter + 核心理念 + v4特性 | ~30 | 全局标识 |
| 项目规模裁剪（大/中/小判定表） | ~40 | 编排决策 |
| 完整流程图（ASCII概览） | ~200 | 核心编排逻辑 |
| 阶段依赖与并发关系 | ~30 | 编排规则 |
| 角色配置表（含Agent ID） | ~30 | 编排决策 |
| 协调者通信规则 | ~20 | 编排规则 |
| Skill引用容错规则 | ~20 | 跨阶段规则 |
| 回退规则（机制一） | ~50 | 跨阶段规则 |
| 需求变更管理（机制三） | ~60 | 跨阶段规则 |
| Agent间沟通汇报（机制四） | ~80 | 跨阶段规则 |
| 防偷懒强制约束（机制五） | ~80 | 跨阶段规则 |
| 参考文件引用 | ~15 | skill索引 |

**简化/删除的内容：**

| 章节 | 处理方式 |
|------|---------|
| 阶段0详细说明 | 保留简要版（~15行），角色配置表已含Agent ID |
| 阶段1详细说明 | → 拆到 `requirements-analysis` skill |
| 阶段2详细说明 | → 拆到 `tech-architecture` skill |
| 阶段2.8详细说明 | → 拆到 `tech-spike` skill |
| 阶段3/4详细说明 | 保留简要编排版（~10行），UX/UI细则不拆（独立场景少） |
| 阶段5详细说明 | → 拆到 `task-decomposition` skill |
| 阶段6/6.3/6.5详细说明 | 保留简要编排版，细则引用 code-review-checklist |
| 阶段7详细说明 | 保留简要编排版（~10行） |
| 阶段8详细说明 | 保留简要编排版，细则引用 qa-workflow |
| 阶段9详细说明 | 保留简要编排版（~15行），含交付验收标准 |
| 端到端用户旅程验证（机制二） | 保留（跨阶段规则） |
| CI/CD集成附录 | 保留（可选附录） |
| 合同存储与规则 | 保留（跨阶段规则） |

**骨架中的阶段描述示例（简化后）：**

```markdown
### 阶段1：需求分析（PM）
**执行者：** PM agent
**产出：** `.contracts/{project}/PRD.md`
**加载 skill：** `requirements-analysis`（如可用）
**验收标准：** 见 requirements-analysis skill 中的验收清单
```

---

## 二、新拆分的小 skill（4个）

### 1. requirements-analysis skill（~150行）

**路径：** `~/.agents/skills/requirements-analysis/SKILL.md`

**内容（从 v4 阶段1提取）：**
- PRD.md 完整模板（背景与目标、用户故事、功能清单、非功能需求、不做什么）
- PRD 交叉评审流程（1.5）的产出格式
- 验收标准清单（用户故事覆盖、优先级标注、术语表等）

**独立使用场景：**
- 用户说"帮我分析这个需求"、"写个PRD"
- 任何 agent 需要结构化分析需求时

**触发词：** 需求分析、写PRD、分析需求、需求拆解

**YAML front matter：**
```yaml
---
name: requirements-analysis
type: methodology
trigger: user-request
description: 结构化需求分析方法论。从背景分析到PRD产出的完整流程，含用户故事模板、功能清单格式、非功能需求检查、验收标准清单。触发词：需求分析、写PRD、分析需求。
priority: high
auto-load: true
---
```

### 2. tech-architecture skill（~150行）

**路径：** `~/.agents/skills/tech-architecture/SKILL.md`

**内容（从 v4 阶段2提取）：**
- ARCHITECTURE.md 完整模板（系统架构图、技术选型、数据模型、API设计、扩展性分析、安全措施、高风险技术点）
- 架构交叉评审流程（2.5）的产出格式
- 验收标准清单（技术选型理由、接口定义完整性、风险识别等）

**独立使用场景：**
- 用户说"设计一下架构"、"技术选型"、"系统设计"
- 任何 agent 需要做技术方案设计时

**触发词：** 架构设计、技术方案、技术选型、系统设计

**YAML front matter：**
```yaml
---
name: tech-architecture
type: methodology
trigger: user-request
description: 技术架构设计方法论。从系统架构图到技术选型的完整流程，含数据模型模板、API设计规范、安全措施检查、风险评估。触发词：架构设计、技术方案、技术选型。
priority: high
auto-load: true
---
```

### 3. tech-spike skill（~100行）

**路径：** `~/.agents/skills/tech-spike/SKILL.md`

**内容（从 v4 阶段2.8提取）：**
- Spike 执行流程（4h时限、时间盒控制）
- SPIKE-REPORT.md 模板
- 三路决策机制（成功/部分成功/失败）
- 部分成功的量化定义

**独立使用场景：**
- 用户说"这个技术可行吗"、"验证一下"、"做个原型试试"
- 任何 agent 遇到不确定的技术方案需要验证时

**触发词：** 技术验证、Spike、验证可行性、技术原型

**YAML front matter：**
```yaml
---
name: tech-spike
type: methodology
trigger: user-request
description: 技术可行性验证方法论。4h时间盒控制，含Spike报告模板、三路决策机制（成功/部分成功/失败）。触发词：技术验证、Spike、验证可行性。
priority: medium
auto-load: false
---
```

### 4. task-decomposition skill（~200行）

**路径：** `~/.agents/skills/task-decomposition/SKILL.md`

**内容（从 v4 阶段5提取）：**
- tasks.md 完整模板（依据文档、批次规划、任务描述格式）
- test-plan.md 完整模板（测试维度清单、优先级、验收标准）
- 冒烟验证流程（创业助手执行P0冒烟的标准流程）
- 验收标准清单（任务粒度、依赖关系、验收条件）

**独立使用场景：**
- 用户说"拆任务"、"把这个需求拆成开发任务"
- 任何 agent 需要做任务规划时

**触发词：** 任务分解、拆任务、任务规划、拆测试计划

**YAML front matter：**
```yaml
---
name: task-decomposition
type: methodology
trigger: user-request
description: 任务分解与测试规划方法论。从开发任务拆解到测试计划编写的完整流程，含批次规划、依赖管理、冒烟验证、QA测试维度拆解。触发词：任务分解、拆任务、任务规划。
priority: high
auto-load: true
---
```

---

## 三、已有 skill（不拆，引用即可）

| skill | 覆盖的 pipeline 阶段 | 引用方式 |
|-------|---------------------|---------|
| code-review-checklist | 阶段6.5 开发审查 | `加载 skill：code-review-checklist` |
| qa-workflow | 阶段8 测试验证 | `加载 skill：qa-workflow` |
| code-quality-guard | 阶段6 编码时 | `加载 skill：code-quality-guard` |
| humanize-code | 阶段6.5 去AI味 | `加载 skill：humanize-code` |
| run-tests | 阶段8 测试执行 | `加载 skill：run-tests` |

---

## 四、拆分后的 Token 节省

| 角色 | 拆分前（加载完整v4） | 拆分后 |
|------|---------------------|--------|
| 协调者 | ~1966行 | ~400行（骨架） |
| PM | ~1966行 | ~400行（骨架）+ ~150行（requirements-analysis）= ~550行 |
| 架构师 | ~1966行 | ~400行 + ~150行（tech-architecture）= ~550行 |
| 开发者 | ~1966行 | ~400行 + ~115行（code-quality-guard）= ~515行 |
| reviewer | ~1966行 | ~400行 + ~130行（code-review-checklist）= ~530行 |
| QA | ~1966行 | ~400行 + ~311行（qa-workflow）= ~711行 |
| 创业助手 | ~1966行 | ~400行 + ~200行（task-decomposition）= ~600行 |

**平均节省：~65% token**

---

## 五、执行计划

### Step 1：创建4个新 skill
1. 创建 `~/.agents/skills/requirements-analysis/SKILL.md`
2. 创建 `~/.agents/skills/tech-architecture/SKILL.md`
3. 创建 `~/.agents/skills/tech-spike/SKILL.md`
4. 创建 `~/.agents/skills/task-decomposition/SKILL.md`

### Step 2：精简 agent-pipeline 骨架
1. 备份 v4 → `SKILL-v4-full.md`
2. 删除已拆分阶段的详细说明
3. 每个阶段替换为简要编排说明 + skill 引用
4. 保留跨阶段规则不变

### Step 3：更新各 agent 的 skills 配置
每个 agent 的 agent.json 中添加对应的小 skill：
| agent | 新增 skill |
|-------|-----------|
| pm | requirements-analysis |
| architect | tech-architecture, tech-spike |
| startup-helper | task-decomposition |
| backend/frontend/dev3 | code-quality-guard（已有） |
| backend-reviewer/frontend-reviewer/dev3-reviewer | code-review-checklist（已有） |
| qa | qa-workflow, task-decomposition（读取test-plan用） |

### Step 4：验证
1. 检查所有 skill 文件存在且 YAML 格式正确
2. 检查骨架中所有引用路径指向实际文件
3. 模拟小型项目流程（5个阶段）确认骨架足够
4. 独立测试每个小 skill（非pipeline场景）
