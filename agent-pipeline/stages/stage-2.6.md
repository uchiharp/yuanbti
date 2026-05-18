# 阶段 2.6：架构用户审阅

## 任务
架构师将 ARCHITECTURE.md 转成 HTML，协调者提交给用户审阅，用户确认后推进阶段 5（如架构有高风险标记则先推进阶段 2.8）。

## 角色
- 架构师：将 ARCHITECTURE.md 转成 HTML（docs/architecture-draft.html）
- 协调者：提交用户审阅、收集反馈、推进

## 执行流程
1. 架构师读取 ARCHITECTURE.md，转成 HTML 格式存入 docs/architecture-draft.html
2. 协调者通知用户审阅 HTML
3. 用户反馈后：
   - 有修改意见 → 架构师修改 ARCHITECTURE.md + HTML，重新提交
   - 用户直接改了 HTML → 架构师同步回 ARCHITECTURE.md
   - 确认通过 → 推进阶段 5（如架构有高风险标记则先推进阶段 2.8）
4. 最多 2 轮修改，超过则升级

## 产出物
| 文件 | 说明 |
|------|------|
| docs/architecture-draft.html | 架构文档 HTML 版本 |
| architecture-feedback.md | 用户反馈记录 |

## 约束
- pipeline-check.sh 强制检查 HTML 质量和用户确认
- 通过 → 推进阶段 5（如架构有高风险标记则先推进阶段 2.8）
