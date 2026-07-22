# 架构师 Pipeline 特有设计模式

> 从架构师 Pipeline 抽象出的、与需求 Pipeline 不同的设计逻辑。
> 通用设计模式（断点续跑、前置条件、产出物校验等）参见 `~/tools/requirements-pipeline/DESIGN-PATTERNS.md`。

---

## 1. 共用数据库、Phase 隔离

**问题**：架构师 Pipeline 和需求 Pipeline 共用同一个 pipeline.db，如何避免数据冲突？

**设计**：
- `phase_log` 表的 `phase` 字段区分：`requirements` / `architecture` / `design`（兼容旧数据）
- 每个 Pipeline 只查自己 phase 的记录
- `features` 表是共享的，需求组写入，架构组读取并更新状态
- `artifacts` 表按 phase 区分：`requirements` 产出 PRD.md，`architecture` 产出 ARCHITECTURE.md

**复用要点**：
- 所有 `get_step_status()` 查询都带 `phase='architecture'` 条件
- `db_phase_log()` 调用时传入 `phase='architecture'`

---

## 2. 前置条件链（Phase 级）

**问题**：架构师 Pipeline 的前置条件不是单个文件，而是整个需求阶段的完成状态。

**设计**：
- `check_requirements_done()` 检查 `projects.current_phase = requirements_done`
- 需求组完成后设置 `current_phase = requirements_done`
- 架构组完成后设置 `current_phase = design_done`
- 每个 Pipeline 启动时检查前置 Phase

```
requirements_done → design_done → (后续阶段)
```

**复用要点**：
- 每个 Phase Pipeline 都有 `check_xxx_done()` 前置检查
- `current_phase` 是阶段级的状态机

---

## 3. 内联评分（无 AI）

**问题**：质量评分步骤不需要 AI 执行，应该由脚本自动完成。

**设计**：
- `arch_score_inline()` 函数在 `arch-parser.sh` 中实现
- 用 `grep` + 关键词检测替代 AI 理解
- 检测覆盖度（6维度、11项健壮性）通过关键词匹配
- 评分结果 JSON 存入 `phase_log.detail`

**复用要点**：
- 评分函数是纯 bash，不需要 AI 调用
- 评分结果用于后续步骤的门控（NEEDS_WORK 跳过评审）

---

## 4. 条件步骤（Tech Spike）

**问题**：Tech Spike 不是每次都执行，只在架构有高风险标记时触发。

**设计**：
- `check_high_risk()` 检测 ARCHITECTURE.md 中的高风险关键词
- 检测词：`HIGH-RISK`、`SPIKE`、`高风险`、`需验证`、`技术不确定性`
- 无高风险标记 → `tech-spike` 步骤自动标记为 `skipped`
- 有高风险标记 → 正常执行 Spike

```
arch-user-review → check_high_risk() → [有] → tech-spike
                                       → [无] → skip → arch-finalize
```

**复用要点**：
- 条件步骤的 `require_step_done` 逻辑：skipped 也视为"完成"
- 条件判断在步骤开头，不在主流程

---

## 5. 产出物级联清理

**问题**：重跑某步骤时，下游产出物需要清理，但清理粒度因步骤而异。

**设计**：
- `cleanup_downstream(from_step)` 按步骤递增清理
- 架构设计重跑 → 清理 ARCHITECTURE.md + docker-compose + artifacts
- 评分重跑 → 清理评审报告
- 评审重跑 → 清理 HTML + 反馈
- 用户审阅重跑 → 清理 Spike 报告

```
arch-design → ALL (arch + dc + artifacts + review + html + spike)
arch-quality-score → review + html + spike
arch-review → html + spike
arch-user-review → spike
```

**复用要点**：
- 清理在步骤执行前调用
- `rm -f` 幂等，不怕文件不存在

---

## 6. HTML 转换中间产物

**问题**：用户审阅需要 HTML 格式，但源文件是 Markdown。

**设计**：
- `arch-user-review` 步骤产出 `docs/architecture-draft.html`
- HTML 是中间产物，源文件始终是 ARCHITECTURE.md
- 用户反馈必须同步回 ARCHITECTURE.md
- HTML 不作为最终交付物

**复用要点**：
- `docs/` 目录存放中间产物
- 产出物校验检查 HTML 存在性，不检查内容质量

---

## 7. Spike 结论路由

**问题**：Spike 结论不只有"通过"，还有"不通过"和"有条件通过"，需要不同的后续流程。

**设计**：
- Spike 报告必须包含明确结论
- 全部通过 → 推进
- 部分不通过 → 回退架构设计（用户确认）
- 全部不通过 → 回退架构设计（用户确认）
- 有条件通过 → 记录条件，推进

**复用要点**：
- 脚本检测 `不通过` 关键词，提示用户确认
- 用户可选择"带风险继续"

---

## 8. 功能点标签流转

**问题**：架构完成后，features 表中的功能点状态需要更新。

**设计**：
- 需求组完成后：`status = PRD-已确认`
- 架构组完成后：`status = ARCH-已设计`
- 标签更新在 `arch-finalize` 步骤中批量执行
- 同时写入 `feature_history` 表

```
PRD-已确认 → ARCH-已设计 → (后续标签)
```

**复用要点**：
- `db_feature_set_status()` 同时更新 features 和 feature_history
- 批量更新用 `grep PRD` 提取 REQ 列表后循环

---

## 9. 规模自适应模板

**问题**：不同规模的项目需要不同详细程度的架构方案。

**设计**：
- 规模从 DB 读取（需求组已判定）或从 PRD 推断
- 大型/中型 → `architecture-comprehensive.md` 模板
- 小型 → `architecture-minimal.md` 模板
- 评分标准不变（60分制），但小型项目某些章节可简化

**复用要点**：
- `determine_size()` 函数优先读 DB，其次推断，最后默认 medium
- 模板选择在 prompt 组装时决定

---

## 10. 多 Skill 联合加载

**问题**：架构设计需要同时加载多个 Skill（tech-architecture + engineering-robustness + logging-exception）。

**设计**：
- prompt 组装时拼接多个 Skill 文件内容
- Skill 内容直接嵌入 prompt，不依赖运行时加载
- 每个 Skill 文件独立，可单独更新

**复用要点**：
- `[ -f "$skill_file" ] && skill_content=$(cat "$skill_file")`
- Skill 内容按优先级排列在 prompt 中
