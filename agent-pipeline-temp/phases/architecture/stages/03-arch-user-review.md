# 架构用户审阅阶段指令

你是架构师，将 ARCHITECTURE.md 转成 HTML 供用户审阅。不要问"要继续吗"，收到任务直接执行。

## 前置条件
- ARCHITECTURE.md 已存在且交叉评审通过

## 必读文件
1. ARCHITECTURE.md

## 产出物
| 文件 | 说明 |
|------|------|
| docs/architecture-draft.html | 架构文档 HTML 版本 |
| architecture-feedback.md | 用户反馈记录（如有） |

## 执行流程

1. 读取 ARCHITECTURE.md
2. 转成 HTML 格式存入 docs/architecture-draft.html
3. 通知用户审阅 HTML
4. 用户反馈后：
   - 有修改意见 → 架构师修改 ARCHITECTURE.md + HTML，重新提交
   - 用户直接改了 HTML → 架构师同步回 ARCHITECTURE.md
   - 确认通过 → 推进（如架构有高风险标记则先进入 tech-spike）
5. 最多 2 轮修改，超过则升级

## HTML 转换要求

- **单文件**：所有 CSS 内联，无外部依赖（Mermaid CDN 除外）
- **暗色主题**：GitHub Dark 风格（#0d1117 背景，#c9d1d9 文字）
- **响应式**：移动端可读
- **目录**：包含锚点目录，点击可跳转
- **表格**：表格样式清晰，支持水平滚动
- **代码块**：语法高亮（可用 Prism.js CDN 或内联高亮）
- **图表**：Mermaid 图表可渲染
- **可交互**：关键部分可点击展开/折叠

## 用户反馈处理

### 收集反馈
- 用户在 HTML 中直接标注修改意见
- 用户口头反馈，协调者记录到 architecture-feedback.md

### 修改流程
1. 架构师读取 feedback
2. 修改 ARCHITECTURE.md（源文件）
3. 重新生成 HTML
4. 重新提交用户审阅

## 约束
- 最多 2 轮修改，超过则升级到协调者
- 修改必须同步到 ARCHITECTURE.md（源文件），不能只改 HTML
- 用户确认后才能推进下一阶段

## 完成标志

用户确认架构方案后，推进到 tech-spike（如有高风险标记）或 arch-finalize。
