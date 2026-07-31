# 阶段3: 架构用户审阅（arch-user-review）

## 任务
架构师将 ARCHITECTURE.md 转成 HTML，提交给用户审阅。用户确认后推进（如有高风险标记则先执行 tech-spike）。

## 前置条件
- `arch-review` 步骤已完成（交叉评审通过）
- ARCHITECTURE.md 已根据评审意见修订

## 角色
- **架构师**：将 ARCHITECTURE.md 转成 HTML（architecture-draft.html）
- **协调者**：提交用户审阅、收集反馈、推进

## 执行流程

1. 架构师读取 ARCHITECTURE.md，转成 HTML 格式
2. HTML 保存到 `$PROJECT_DIR/architecture-draft.html`
3. 协调者通知用户审阅 HTML
4. 用户反馈后：
   - **有修改意见** → 架构师修改 ARCHITECTURE.md + HTML，重新提交
   - **用户直接改了 HTML** → 架构师同步回 ARCHITECTURE.md
   - **确认通过** → 推进（如有高风险标记则先 tech-spike）
5. 最多 2 轮修改，超过则升级

## HTML 转换要求

### 基本要求
- 响应式设计，支持桌面和移动端
- 暗色主题优先（技术文档常用）
- 代码块语法高亮
- 目录导航（可折叠侧边栏或顶部锚点）
- 图表使用 Mermaid.js 渲染（架构图、ER图、流程图）

### 内容映射
- ARCHITECTURE.md 一级标题 → HTML 页面标题
- ARCHITECTURE.md 二级标题 → 章节标题 + 目录项
- 表格 → HTML 表格（带排序/筛选可选）
- 代码块 → 语法高亮
- Mermaid 代码块 → 渲染为 SVG 图表

### 交互功能
- 点击目录项跳转到对应章节
- 搜索功能（Ctrl+F 增强）
- 打印友好（@media print 样式）

## 产出物
| 文件 | 说明 |
|------|------|
| architecture-draft.html | 架构文档 HTML 版本 |
| architecture-feedback.md | 用户反馈记录（如有修改） |

## 检查项（脚本强制）
- [ ] architecture-draft.html 存在且非空
- [ ] HTML 文件可正常打开（非空、有基本结构）
- [ ] 用户确认记录存在（feedback 或确认标记）

## 约束
- HTML 必须包含 ARCHITECTURE.md 的全部内容（不遗漏章节）
- 用户最多 2 轮修改
- 确认通过后才能进入下一步（tech-spike 或 finalize）
