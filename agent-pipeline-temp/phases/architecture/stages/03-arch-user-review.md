# Stage 3: 架构用户审阅

## 任务

将 ARCHITECTURE.md 转成 HTML，提交给用户审阅，用户确认后推进下一阶段（如有高风险标记则先推进 tech-spike）。

## 执行流程

1. 读取 ARCHITECTURE.md，转成 HTML 格式存入 docs/architecture-draft.html
2. 通知用户审阅 HTML
3. 用户反馈后：
   - 有修改意见 → 修改 ARCHITECTURE.md + HTML，重新提交
   - 用户直接改了 HTML → 同步回 ARCHITECTURE.md
   - 确认通过 → 推进下一阶段（如有高风险标记则先推进 tech-spike）
4. 最多 2 轮修改，超过则升级

## 产出物

| 文件 | 说明 |
|------|------|
| docs/architecture-draft.html | 架构文档 HTML 版本 |
| architecture-feedback.md | 用户反馈记录 |

## HTML 转换要求

- 保留所有标题层级
- 表格正常渲染
- 代码块语法高亮
- 可在浏览器中独立打开
- 移动端可读

## 约束

- 通过 → 推进下一阶段（如有高风险标记则先推进 tech-spike）
- 最多 2 轮修改
