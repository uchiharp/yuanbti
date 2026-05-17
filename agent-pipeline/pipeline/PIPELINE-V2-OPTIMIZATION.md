# Agent Pipeline v2 增强方案

> 优化日期：2026-05-17
> 状态：已实施

## 变更概述

将旧的阶段3 UX / 3.5 UX→UI交接 / 4 UI / 4.5 UI→UX反向 替换为新的 1.7/1.8/1.9 流程，实现 UI/UX 设计前置到 PRD 确认后、PRD 反向细化闭环。

## 旧流程 → 新流程

| 旧阶段 | 问题 | 新阶段 | 改进 |
|--------|------|--------|------|
| 3. UX设计 | 在架构设计后才做UX，容易返工 | 1.7 UI/UX设计 | PRD确认后立即设计，避免架构返工 |
| 3.5 UX→UI交接 | UX/UI割裂，交接成本高 | 合并到1.7 | 一体化设计，单agent完成 |
| 4. UI设计 | 延迟到架构后，交互需求不明确 | 合并到1.7 | 设计前置，驱动架构 |
| 4.5 UI→UX反向 | 仅确认，无细化 | 1.8 PRD反向细化 | 4维度细化，产出强化版PRD |
| — | 无用户确认节点 | 1.9 细化PRD确认 | 人工确认细化后的PRD |

## 新流程时序

```
阶段1 PM→PRD
  → 阶段1.5 PRD交叉评审
    → 阶段1.6 PRD用户审阅
      → 阶段1.7 UI/UX设计（8维度技术特性分析 + HTML原型）
        → 阶段1.8 PRD反向细化（交互细节/边界/文案/异常）
          → 阶段1.9 细化PRD人工确认
            → 阶段2 架构设计（基于细化PRD）
```

## 功能点标签状态机

```
PRD-待确认 → PRD-已确认 → UI/UX-设计中 → UI/UX-设计完成
    → PRD-已细化 → PRD-细化确认 → 技术方案-待确认 → 技术方案-已确认
    → 开发-进行中 → 开发-完成 → 测试-通过 → 验收-通过 → 交付-完成
```

## 新增 Skill 清单

| Skill | 路径 | 用途 |
|-------|------|------|
| ui-ux-design | skills/ui-ux-design/SKILL.md | UI/UX设计执行规范，含8维度分析框架 |
| prd-refinement | skills/prd-refinement/SKILL.md | PRD反向细化方法论 |
| feature-tagging | skills/feature-tagging/SKILL.md | 功能点标签系统规范 |
| interactive-html | skills/interactive-html/SKILL.md | HTML原型生成规范 |
| engineering-robustness | skills/engineering-robustness/SKILL.md | 工程健壮性检查 |

## 新增 Stage 清单

| Stage | 路径 |
|-------|------|
| 1.6 PRD用户审阅 | stages/stage-1.6.md |
| 1.7 UI/UX设计 | stages/stage-1.7.md |
| 1.8 PRD反向细化 | stages/stage-1.8.md |
| 1.9 细化PRD确认 | stages/stage-1.9.md |

## 修改文件清单

| 文件 | 变更 |
|------|------|
| PRD.md | 规模表/流程图/角色表/阶段定义/产出路径/DoD/YAML配置 全部替换3/3.5/4/4.5为1.6/1.7/1.8/1.9 |
| ARCHITECTURE.md | 模型路由/交叉评审角色 清理旧ux-tester/ui-designer引用 |
| scripts/dispatch.sh | 添加1.7/1.8/1.9阶段名称/NEXT_CMD/角色映射/ui-ux-designer角色/标签更新指令 |
| config/pipeline-stages.conf | 删除3/3.5/4/4.5产出配置，1.7/1.8/1.9已有 |
| config/stage-skills.conf | 删除3/3.5/4/4.5 skill映射，1.7/1.8/1.9已有 |

## 已删除的旧阶段文件（保留但不再调度）

- stages/stage-3.md（UX设计）
- stages/stage-3.5.md（UX→UI交接）
- stages/stage-4.md（UI设计）
- stages/stage-4.5.md（UI→UX反向）

这些文件保留作为参考，但 dispatch.sh 不再调度它们。
