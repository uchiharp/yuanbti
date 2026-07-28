---
name: architecture-pipeline-design-patterns
description: 架构师 Pipeline 特有的设计模式补充，对通用 Pipeline 设计模式的架构师特定扩展
metadata:
  type: reference
---

# 架构师 Pipeline 设计模式补充

本文档是通用 Pipeline 设计模式（见 requirements-pipeline/DESIGN-PATTERNS.md）的架构师特定补充。

---

## 1. 六步流程编排

**与需求 Pipeline 的区别：**

| 特性 | 需求 Pipeline | 架构 Pipeline |
|------|-------------|-------------|
| 步骤数 | 5 步 | 6 步 |
| 自动步骤 | 评分 | 评分 |
| 条件步骤 | 无 | Spike（高风险时触发） |
| 前置依赖 | 无 | requirements_done |
| phase 字段 | `requirements` | `architecture` |

**流程：**
```
arch-design → arch-quality-score → arch-review → arch-user-review → tech-spike(条件) → arch-finalize
```

---

## 2. 条件触发（Conditional Trigger）

**问题：** Spike 步骤不是每次都执行，只在架构中有高风险标记时触发。

**设计：**
- `run_tech_spike()` 函数开头检查 ARCHITECTURE.md 中是否有高风险标记
- 有 → 执行 Spike 验证
- 无 → 标记 skipped，直接跳过
- 检测关键词：`高风险`、`🔴`、`Spike`、`需验证`

```
local risk_markers=$(grep -ciE '高风险|🔴|Spike|需验证' "$arch_file" || echo 0)
if [ "$risk_markers" -eq 0 ]; then
  echo "⏩ 无高风险标记，跳过 Spike"
  db_phase_log ... "skipped"
  return 0
fi
```

**复用要点：** 任何 Pipeline 都可以有条件步骤，用关键词检测 + skipped 状态。

---

## 3. 多产出物校验

**问题：** 架构设计步骤产出多个文件（ARCHITECTURE.md + docker-compose.test.yml + 覆盖率配置），校验逻辑比需求 Pipeline 复杂。

**设计：**
- 主产出物（ARCHITECTURE.md）：行数 ≥100 + 结构校验
- 辅助产出物（docker-compose.test.yml）：存在性校验
- 嵌入产出物（覆盖率配置）：关键词检测

```
validate_artifact "$arch_file" "ARCHITECTURE.md" 100
# docker-compose 可选但推荐
# 覆盖率配置通过 arch_score_inline 自动检测
```

---

## 4. 评分维度差异

**需求 Pipeline 评分：** 12 项 × 5 分 = 60 分
- 聚焦 PRD 质量：摘要、问题、目标、REQ 编号...

**架构 Pipeline 评分：** 12 项 × 5 分 = 60 分
- 聚焦架构质量：架构图、技术选型、数据模型、API、安全、风险、6维度、健壮性...

**共同模式：**
- 评分函数纯 bash，不依赖外部工具
- 评分结果存入 `phase_log.detail`（JSON 格式）
- 评级阈值统一：EXCELLENT≥54, GOOD≥45, ACCEPTABLE≥36, NEEDS_WORK<36

---

## 5. 评审角色扩展

**需求 Pipeline 评审：** 3 角色（RD + 架构师 + QA）
**架构 Pipeline 评审：** 4 角色（开发1 + 开发2 + QA + PM）

**设计要点：**
- 角色定义在 `references/arch-adversarial-review.md`
- 评审 prompt 统一组装，不分角色拆分
- 阻断项检测逻辑相同

---

## 6. 前置依赖链

**架构 Pipeline 的完整依赖链：**
```
requirements_done → arch-design → arch-quality-score → arch-review → arch-user-review → tech-spike(条件) → arch-finalize → development
```

**前置检查：**
- `init_project()` 检查 `current_phase = requirements_done`
- `run_arch_design()` 检查 features 表有 `PRD-已确认` 的 REQ
- 后续步骤各自检查前置步骤完成状态

---

## 7. 入库逻辑差异

**需求 Pipeline 入库：**
- 更新 projects.current_phase = requirements_done
- 注册 features（REQ 列表）
- 注册 artifacts（PRD.md）

**架构 Pipeline 入库：**
- 更新 projects.current_phase = architecture_done
- 更新 features 状态 → 技术方案-已确认
- 注册 artifacts（ARCHITECTURE.md + docker-compose.test.yml）
