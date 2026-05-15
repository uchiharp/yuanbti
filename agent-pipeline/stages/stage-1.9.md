# 阶段1.9：细化 PRD 人工确认

## 前置条件
- 阶段 1.8 PRD 反向细化完成
- PRD-REFINED.md 已产出
- prd-diff.md 已产出

## 任务
协调者将细化的 PRD 和变更对比提交给用户审阅，用户确认后替换原始 PRD，流入后续技术方案阶段。

## 角色
- PM（准备 HTML 版本）
- 协调者（提交用户审阅、收集反馈、推进）
- 用户（最终确认）

## 执行流程

### Step 1：PM 准备审阅材料
PM 产出以下材料供用户审阅：
- `docs/prd-refined-draft.html`：细化 PRD 的 HTML 版本（便于阅读）
- 将 `prd-diff.md` 标记为"新增/修改/待确认"三色高亮

### Step 2：协调者提交用户审阅
将 HTML 版本和 diff 提交给用户：
- 用户重点关注 `[待确认]` 标记的不确定项
- 用户审阅 4 个细化维度是否合理
- 用户确认文案规范是否符合产品调性

### Step 3：用户反馈处理
- **用户确认通过** → PM 将 `PRD-REFINED.md` 替换原始 `PRD.md`，推进阶段 2
- **有修改意见** → PM 修改细化内容 + HTML，重新提交（最多 2 轮）
- **用户直接改了 HTML** → PM 同步回 `PRD-REFINED.md`

### Step 4：功能点标签更新
- 用户确认后，所有 REQ → `PRD-细化确认`

### Step 5：归档
- 原始 PRD 备份为 `docs/PRD-original-backup.md`
- 最终 PRD.md 即为细化后的版本

## 产出物
| 文件 | 说明 |
|------|------|
| PRD.md | 替换为细化后的 PRD（后续流程使用此版本） |
| docs/prd-refined-draft.html | 细化 PRD HTML 版本 |
| docs/PRD-original-backup.md | 原始 PRD 备份 |
| prd-refinement-feedback.md | 用户反馈记录 |

## 检查项（脚本强制）
- [ ] PRD.md 已替换为细化版本（内容 ≥ PRD-REFINED.md 行数）
- [ ] docs/PRD-original-backup.md 存在（原始备份）
- [ ] prd-refinement-feedback.md 存在且包含用户确认记录
- [ ] 所有 `[待确认]` 项已处理（无残留）
- [ ] 功能点标签已更新为 `PRD-细化确认`

## 约束
- 最多 2 轮修改
- 超过 2 轮 → 升级用户决策
- 细化后的 PRD 是后续所有阶段的基准文档
- 仅 🟡中型 和 🔴大型 项目执行此阶段
- 🟢小型项目：跳过，阶段 1.6 用户确认后直接进入阶段 2
