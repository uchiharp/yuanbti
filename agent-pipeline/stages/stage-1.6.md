# 阶段 1.6：PRD 用户审阅

## 任务
PM 将 PRD 转成 HTML，协调者提交给用户审阅，用户确认后推进阶段 1.5。

## 角色
- PM：将 PRD.md 转成 HTML（docs/prd-draft.html）
- 协调者：提交用户审阅、收集反馈、推进

## 执行流程
1. PM 读取 PRD.md，转成 HTML 格式存入 docs/prd-draft.html
2. 协调者通知用户审阅 HTML
3. 用户反馈后：
   - 有修改意见 → PM 修改 PRD.md + HTML，重新提交
   - 用户直接改了 HTML → PM 同步回 PRD.md
   - 确认通过 → 推进阶段 1.5
4. 最多 2 轮修改，超过则升级

## 产出物
| 文件 | 说明 |
|------|------|
| docs/prd-draft.html | PRD HTML 版本 |
| prd-feedback.md | 用户反馈记录 |

## 约束
- pipeline-check.sh 强制检查 HTML 质量和用户确认
- 通过 → 推进阶段 1.5
