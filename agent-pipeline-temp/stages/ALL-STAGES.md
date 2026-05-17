# 全阶段指令（合并版）

> 原始文件在 stages/stage-X.md，已合并为单一文件供快速查阅。
> 协调者调度时根据阶段号定位对应章节。



---

# 阶段0：启动

## 任务
初始化项目结构，产出基本计划。规模判定在阶段1 PRD产出后进行。

## 必读文件
无（初始化阶段）

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| PROJECT-PLAN.md | 20 | 基本计划（项目目标、参与角色、初步时间线） |

## 检查项（脚本强制）
- [ ] PROJECT-PLAN.md 存在且 ≥20行
- [ ] health-dashboard.md 存在
- [ ] _index.json 合法 JSON

## 约束
- 无合同限制
- 不做规模判定（PRD 产出前无法准确判断功能数量）
- MemPalace 加载历史教训（MCP 调用）

---

# 阶段1.5：PRD 交叉评审

## 任务
各角色并发评审 PRD，从不同视角提出意见。PM 修改后，评审者复审确认。

## 必读文件
1. PRD.md

## 评审角色与维度
| 角色 | 评审视角 |
|------|---------|
| 架构师 | 技术可行性：性能隐患、技术限制、实现复杂度、逻辑 bug |
| QA | 可测试性：验收标准明确、能写测试用例、边界场景、逻辑 bug |
| 开发1 | 工作量 + 逻辑闭环：工作量合理、边界遗漏、逻辑不闭环/冲突/漏洞/逻辑 bug |
| 开发2 | 技术实现：代码结构、接口设计、技术债、逻辑 bug |

## 执行流程
1. 三个角色并发评审，产出 cross-review-pm.md
2. PM 根据意见修改 PRD.md
3. **评审者复审**：三个角色确认各自提出的问题已修复
4. 复审通过 → 推进阶段 2；仍有问题 → PM 再改（最多 2 轮）

## 产出物
| 文件 | 说明 |
|------|------|
| cross-review-pm.md | 三个角色独立评审意见 |
| re-review-pm.md | 三个角色复审确认（pipeline-check.sh 强制检查） |

## 约束
- 总轮次 ≤2（初审 + 复审算 1 轮）
- 仅 🟡中型 和 🔴大型 项目执行此阶段

---

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

---

# 阶段1.7：UI/UX 设计（PRD 确认后）

## 前置条件
- 阶段 1.6 用户已确认 PRD
- PRD.md 包含所有 REQ-xxx 功能点

## 任务
基于已确认的 PRD，进行专业化的 UI/UX 设计，产出完整设计文档和可交互 HTML 原型。

## 必读文件（按顺序）
1. PRD.md（已确认的需求文档）
2. CONTEXT.md（项目上下文）

## 加载 Skill
- `ui-ux-design`（UI/UX 设计执行 Skill，含技术特性分析框架、HTML 生成规范）

## 角色
- UI/UX 设计师（主责）

## 执行流程

### Step 1：技术特性分析
加载 `ui-ux-design` Skill，按 8 个维度分析：
1. 技术栈适配（框架/组件库选型确认）
2. 设计系统（色彩/字体/间距/圆角/阴影 Token）
3. 组件设计（原子/分子/有机体，每种 6 状态）
4. 响应式策略（断点/布局变化/触摸适配）
5. 暗黑模式（色彩反转/对比度保证）
6. 动效设计（转场/反馈/列表动画/时长规范）
7. 可访问性（对比度/键盘操作/aria/焦点管理）
8. 异常与边界（空状态/加载/错误/操作反馈）

### Step 2：UI/UX 设计文档
产出 `UI-UX-DESIGN.md`，包含：
- 设计系统 Token 定义
- 页面清单与信息架构
- 交互流程图（核心流程用状态机描述）
- 组件规格说明（含状态矩阵）
- 响应式适配方案
- 暗黑模式方案
- 动效规范
- 可访问性达标方案

### Step 3：HTML 原型生成
基于设计文档，自动生成 `docs/ui-prototype.html`：
- 单文件、内联 CSS/JS、无外部依赖
- 包含核心流程页面（2-3 个主流程）
- 组件状态展示（正常/空/加载/错误）
- 交互可点击（Tab 切换、弹窗、表单验证）
- 响应式布局（Desktop + Mobile）
- 暗黑模式切换

### Step 4：PRD 细化触发
对照 PRD 和 UI/UX 设计，识别 PRD 未明确的：
- 交互细节遗漏
- 边界情况未覆盖
- 文案规范未定义
- 异常处理路径缺失

将以上写入 `prd-refinement-notes.md`。

### Step 5：功能点标签更新
- 所有 REQ → `UI/UX-设计中`（Step 1 开始时）
- 所有 REQ → `UI/UX-设计完成`（Step 3 完成后）

### Step 6：PM 审查
PM 对照 PRD 审查 UI/UX 设计：
- 页面覆盖度：PRD 每个 REQ 是否有对应页面/流程
- 交互完整性：核心流程是否闭环
- 需求符合度：设计是否忠实于 PRD 描述
- 异常覆盖：空状态/错误状态是否完善

审查通过 → 推进阶段 1.8（PRD 反向细化）
审查不通过 → UI/UX 设计师修改（最多 2 轮）

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| UI-UX-DESIGN.md | 120 | 完整 UI/UX 设计文档（含 8 维度分析） |
| docs/ui-prototype.html | 200 | 可交互 HTML 原型 |
| prd-refinement-notes.md | 20 | PRD 细化触发说明 |
| uiux-review.md | 15 | PM 审查意见 |
| re-review-uiux.md | 10 | PM 复审确认 |

## 检查项（脚本强制）
- [ ] UI-UX-DESIGN.md 存在且 ≥120行
- [ ] docs/ui-prototype.html 存在且 ≥200行
- [ ] prd-refinement-notes.md 存在且 ≥20行
- [ ] HTML 原型包含 `<style>` 和 `<script>` 标签（非纯静态）
- [ ] HTML 原型包含响应式 meta viewport
- [ ] 设计文档覆盖 8 个技术特性维度
- [ ] 每个 REQ 有对应的设计描述
- [ ] 功能点标签已更新为 `UI/UX-设计完成`

## 约束
- 合同：🟡中风险 标准合同 最多 2 轮
- 仅 🟡中型 和 🔴大型 项目执行此阶段
- 🟢小型项目：简化为仅产出 HTML 原型（跳过完整设计文档）
- 设计决策必须基于 PRD，不能主观臆造功能
- HTML 原型是团队评审和开发参考的核心产出，必须可交互

---

# 阶段1.8：PRD 反向细化

## 前置条件
- 阶段 1.7 UI/UX 设计完成
- UI-UX-DESIGN.md 已产出
- docs/ui-prototype.html 已产出
- prd-refinement-notes.md 已产出

## 任务
根据 UI/UX 设计产出，将 PRD 从"功能描述"细化为包含交互细节、边界情况、文案规范、异常处理的完整文档。

## 必读文件（按顺序）
1. PRD.md（原始 PRD）
2. UI-UX-DESIGN.md（UI/UX 设计文档）
3. docs/ui-prototype.html（HTML 原型，重点看交互逻辑）
4. prd-refinement-notes.md（UI/UX 设计师标记的待细化项）

## 加载 Skill
- `prd-refinement`（PRD 反向细化方法论）

## 角色
- PM（主责，结合 UI/UX 产出细化 PRD）

## 执行流程

### Step 1：加载原始 PRD
读取 PRD.md，提取所有 REQ-xxx 功能点及其验收标准。

### Step 2：加载 UI/UX 设计产出
读取 UI-UX-DESIGN.md 和 prd-refinement-notes.md，识别每个 REQ 对应的设计决策和待细化项。

### Step 3：逐 REQ 四维度细化
对每个 REQ-xxx，按 4 个维度补充：

**交互细节**：
- 操作路径、交互方式、反馈时机、组件行为、键盘交互、手势操作

**边界情况**：
- 数据边界（空/超长/特殊字符）、状态边界（未登录/无权限/并发）、时序边界（快速点击/超时）、设备边界

**文案规范**：
- 页面标题、按钮文案、提示文案、占位符、空状态文案、错误文案

**异常处理**：
- 输入校验、业务规则异常、网络异常、服务端异常、权限异常

### Step 4：生成产出物
- `PRD-REFINED.md`：完整细化后的 PRD（保留原始结构 + 细化内容）
- `prd-diff.md`：变更对比（原始 → 细化），便于审查

### Step 5：功能点标签更新
- 所有 REQ → `PRD-已细化`

## 细化 PRD 格式（强制）

每个 REQ 细化后必须包含以下结构：

```markdown
### REQ-xxx: {功能名称}

{原始描述保留}

**验收标准**：
- {原始验收标准保留}

#### [UI/UX细化] 交互细节
- 操作路径：...
- 交互方式：...
- 反馈时机：...
- 组件行为：...

#### [UI/UX细化] 边界情况
- {边界场景} → {处理方式}

#### [UI/UX细化] 文案规范
- 页面标题：...
- 按钮：...
- 提示：...

#### [UI/UX细化] 异常处理
- 输入校验：... → 提示：...
- 网络异常：...
```

**新增内容必须用 `[UI/UX细化]` 标记**，不确定项用 `[待确认]` 标记。

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| PRD-REFINED.md | 300 | 细化后的完整 PRD |
| prd-diff.md | 50 | 变更对比（原始 → 细化） |

## 检查项（脚本强制）
- [ ] PRD-REFINED.md 存在且 ≥300行
- [ ] prd-diff.md 存在且 ≥50行
- [ ] 每个 REQ 包含 4 个细化维度
- [ ] 新增内容有 `[UI/UX细化]` 标记
- [ ] 不确定项有 `[待确认]` 标记
- [ ] 文案规范不出现模糊词（"确定""系统错误"等）
- [ ] 每个 REQ 至少 2 个边界情况
- [ ] 每个 REQ 至少 3 条异常处理路径
- [ ] 功能点标签已更新为 `PRD-已细化`

## 约束
- 合同：🟡中风险 标准合同 最多 2 轮
- 仅 🟡中型 和 🔴大型 项目执行此阶段
- 🟢小型项目：跳过此阶段，直接使用原始 PRD
- 细化内容必须基于 UI/UX 设计，不能脱离设计主观臆造
- 细化后的 PRD 必须经人工确认（阶段 1.9）才能流入后续

---

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

---

# 阶段1：需求分析（PM）

## 任务
和用户讨论需求，产出 PRD。

## 必读文件
无（从零开始）

## 加载 Skill
- `requirements-analysis`（需求分析方法论）

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| PRD.md | 200 | 完整产品需求文档（功能清单必须用 REQ-xxx 编号） |

## 分期策略
如果项目需求量大需要分期实现：
- **拆成多个独立 PRD 文件**：`PRD-v1.md`（本期）、`PRD-v2.md`（下期）...
- 每个 PRD 走一次完整 pipeline，本期 PRD + 架构 = **全部必须实现，不可跳过**
- 不要在一个 PRD 里标注"P2 不做"——不做就不写进本期 PRD
- 本期 PRD 的每个 REQ 都是必须交付的

## PRD 功能清单格式（强制）
功能清单章节必须用 REQ-xxx 唯一编号，每个 REQ 包含：
- 标题：`### REQ-xxx: 功能名称`
- 描述：1-3 句话说明
- 验收标准：可验证的条件列表

示例：
```markdown
### 功能清单

### REQ-001: {功能名称}
{1-3句话描述}
**验收标准**：
- {正常场景} → {预期结果}
- {异常场景A} → {预期结果}
- {异常场景B} → {预期结果}

### REQ-002: {功能名称}
{1-3句话描述}
**验收标准**：
- {正常场景} → {预期结果}
- {异常场景} → {预期结果}
```

**禁止**：功能清单不编号（如"登录功能"、"注册功能"），必须有 REQ-xxx 前缀。

## 执行流程
1. 加载 `requirements-analysis` SKILL.md
2. 和用户 Brainstorm（逐个提问，优先给选择题，给2-3个方向标注利弊）
3. 整理 PRD.md（功能清单必须用 REQ-xxx 编号）
4. PM 自审（魔鬼代言人思维）
5. 签收/打回（最多2轮）
6. **PRD 签收后，协调者进行规模判定**：统计 REQ 数量 → 对照判定标准 → 写入 PROJECT-PLAN.md + `_config.json` 的 `size` 字段

## 规模判定（PRD 产出后）
PRD 签收后，协调者根据 REQ 数量判定规模：

| 规模 | 功能数（REQ） | 子系统数 | 工期 |
|------|-------------|---------|------|
| 🔴 大型 | ≥6 | ≥3 | ≥2周 |
| 🟡 中型 | 3-5 | 1-2 | 1-2周 |
| 🟢 小型 | ≤2 | 1 | <1周 |

判定后写入 `_config.json`：`{"size": "large"}` / `"medium"` / `"small"`

## 检查项（脚本强制）
- [ ] PRD.md 存在且 ≥200行
- [ ] PRD.md 功能清单使用 REQ-xxx 编号（至少3个 REQ）
- [ ] 每个 REQ 包含验收标准
- [ ] 评审报告存在且 ≥3检查点 + ≥1建议 + 评分
- [ ] 合同状态 = signed
- [ ] communications/ 有本轮评审记录
- [ ] `_config.json` 的 `size` 字段已设置（large/medium/small）

## 约束
- 合同：🟡中风险 标准合同 最多2轮
- Brainstorm：先和用户讨论，再整理成文档
- 知识库：交付时更新 CONTEXT.md 阶段1段落，存入 MemPalace room=prd-decisions

---

# 阶段10：交互式文档生成

## 任务
基于实际代码和配置，生成面向用户的交互式 HTML 文档。

## 必读文件
1. PRD.md（产品功能定义）
2. ARCHITECTURE.md（技术架构）
3. 实际代码（src/ 目录结构、入口文件、路由、配置文件）
4. 配置文件（application.yml、.env、docker-compose.yml 等）
5. 部署脚本（Dockerfile、Makefile、CI 配置等）

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| docs/README.html | 80 | 快速启动（5分钟跑起来） |
| docs/USER-GUIDE.html | 120 | 用户操作手册（无技术术语） |
| docs/ARCHITECTURE.html | 100 | 代码架构（面向开发者） |
| docs/DEPLOYMENT.html | 80 | 部署指南（step-by-step） |
| docs/CONFIG-GUIDE.html | 60 | 配置文件使用指导 |

## 交互式 HTML 要求（强制）

### 基础结构
- 单文件、内联 CSS + JS，无外部依赖（Mermaid CDN 除外）
- 暗色主题（GitHub Dark 风格：`#0d1117` 背景）
- 响应式布局，移动端可读

### 交互行为
- **关键部分可点击** → 弹窗/模态框展示详情（API 参数、配置示例、错误排查等）
- **可点击部分必须高亮**：hover 时 `box-shadow` 发光 + `transform: translateY(-2px)`
- 模态框支持 **Escape 键** 和 **点击外部区域** 关闭
- 模态框内的 **Mermaid 图表自动重新渲染**（`mermaid.init()` on modal open）
- 长文档侧边栏有 **锚点目录**，点击跳转

### 视觉反馈
- 可交互元素有 `cursor: pointer`
- 卡片/标签 hover 时显示提示文字（如"点击查看详情"）
- 代码块有复制按钮
- 步骤列表当前步骤高亮

## 易读性要求（强制）

### 结构层
- **金字塔原则**：结论先行，细节在后
- **分层阅读**：快速参考（1页）→ 操作指南（详细步骤）→ 原理说明（为什么这样设计），三层独立可读
- **目录锚点**：每个 HTML 必须有 TOC，点击跳转

### 内容层
- **零假设知识**：不假设读者知道项目背景，第一段写"这是什么、解决什么问题"
- **术语表**：首次出现的专有名词加脚注或 tooltip
- **代码示例必须能复制粘贴直接跑**：不是伪代码，是 `copy → paste → run`
- **错误优先**：常见报错 + 解决方案放在醒目位置（不要藏在末尾）
- **What-Why-How**：每个功能先说"是什么"，再说"为什么"，最后说"怎么用"

### 格式层
- 用表格代替大段文字（对比、配置项、参数说明）
- 关键操作用 `代码块` + 高亮标注
- 步骤用有序列表，不用"首先...然后...接着..."
- 截图/示意图标注重点区域（箭头/红框）
- 每个章节不超过一屏（约30行），超过就拆子章节

### 语言层
- 中文为主，技术术语保持英文原文（说"API"不说"应用程序接口"）
- 禁用"此处省略"、"详见xxx"等跳转 — 直接把内容放出来
- 一个句子只说一件事，不用"并且、同时、另外"堆砌

## 各文档内容要求

### README.html（快速启动）
- 第一段：项目是什么 + 解决什么问题
- **5分钟快速启动**：环境要求 → 安装命令 → 启动命令 → 验证方式
- 常见问题折叠区（点击展开）
- 项目目录结构树

### USER-GUIDE.html（用户手册）
- 按**用户操作流程**组织，不按代码模块
- 每个功能：截图/示意图 + 操作步骤 + 预期结果
- 禁用技术术语（数据库、API、服务端等）
- 常见错误提示 + 用户能理解的解决方案

### ARCHITECTURE.html（代码架构）
- 模块依赖图（Mermaid）
- 数据流图（Mermaid）
- 关键设计决策（Why，不是 What）
- 目录结构树 + 每个目录的职责说明
- 点击模块卡片 → 弹窗展示该模块的详细说明

### DEPLOYMENT.html（部署指南）
- 环境要求表（OS、依赖版本、硬件）
- step-by-step 部署命令（复制粘贴能跑）
- Docker 部署 / 裸机部署 / 云平台部署 三个分支（可点击切换）
- 健康检查命令
- 常见部署故障排查表

### CONFIG-GUIDE.html（配置指导）
- 每个配置文件独立章节
- 配置项表格：名称 | 类型 | 默认值 | 说明 | 示例
- 点击配置项 → 弹窗展示完整示例和关联配置
- 环境变量 vs 配置文件的优先级说明

## 执行流程
1. 读取实际代码目录结构（tree / find）
2. 读取所有配置文件
3. 读取 PRD.md + ARCHITECTURE.md（获取功能和设计信息）
4. 逐个生成 HTML 文档
5. 开发确认技术准确性
6. QA 验证用户手册可操作性

## 检查项（脚本强制）
- [ ] docs/README.html 存在且 ≥80行
- [ ] docs/USER-GUIDE.html 存在且 ≥120行
- [ ] docs/ARCHITECTURE.html 存在且 ≥100行
- [ ] docs/DEPLOYMENT.html 存在且 ≥80行
- [ ] docs/CONFIG-GUIDE.html 存在且 ≥60行
- [ ] 每个 HTML 包含交互式模态框（至少3个可点击元素）
- [ ] 每个 HTML 包含 Mermaid 图表（至少1个）
- [ ] 每个 HTML 包含锚点目录
- [ ] 代码示例可复制（有复制按钮或代码块格式正确）
- [ ] 无"详见xxx"等跳转式写法

## 约束
- 基于实际代码生成，不是基于设计文档抄
- 必须在阶段9验收通过后才能开始
- 文档准确性由开发确认、可操作性由 QA 验证

---

# 阶段2.5：架构交叉评审

## 任务
各角色并发评审架构方案，从不同视角提出意见。架构师修改后，评审者复审确认。

## 必读文件
1. ARCHITECTURE.md
2. PRD.md

## 评审角色与维度
| 角色 | 评审视角 |
|------|---------|
| 开发1 | 技术可行性：技术选型、接口合理性、过度设计、逻辑 bug |
| 开发2 | 技术实现：代码结构、模块划分、技术债、逻辑 bug |
| QA | 可测试性：测试覆盖、日志监控、自动化、逻辑 bug |
| PM | 需求完整性 + 逻辑闭环：PRD 覆盖、优先级、逻辑不闭环/冲突/漏洞/逻辑 bug |

## 执行流程
1. 三个角色并发评审，产出 cross-review-arch.md
2. 架构师根据意见修改 ARCHITECTURE.md
3. **评审者复审**：三个角色确认各自提出的问题已修复
4. 复审通过 → 推进阶段 2.6；仍有问题 → 架构师再改（最多 2 轮）

## 产出物
| 文件 | 说明 |
|------|------|
| cross-review-arch.md | 三个角色独立评审意见 |
| re-review-arch.md | 三个角色复审确认（pipeline-check.sh 强制检查） |

## 约束
- 总轮次 ≤2（初审 + 复审算 1 轮）

---

# 阶段 2.6：架构用户审阅

## 任务
架构师将 ARCHITECTURE.md 转成 HTML，协调者提交给用户审阅，用户确认后推进阶段 2.5。

## 角色
- 架构师：将 ARCHITECTURE.md 转成 HTML（docs/architecture-draft.html）
- 协调者：提交用户审阅、收集反馈、推进

## 执行流程
1. 架构师读取 ARCHITECTURE.md，转成 HTML 格式存入 docs/architecture-draft.html
2. 协调者通知用户审阅 HTML
3. 用户反馈后：
   - 有修改意见 → 架构师修改 ARCHITECTURE.md + HTML，重新提交
   - 用户直接改了 HTML → 架构师同步回 ARCHITECTURE.md
   - 确认通过 → 推进阶段 2.5
4. 最多 2 轮修改，超过则升级

## 产出物
| 文件 | 说明 |
|------|------|
| docs/architecture-draft.html | 架构文档 HTML 版本 |
| architecture-feedback.md | 用户反馈记录 |

## 约束
- pipeline-check.sh 强制检查 HTML 质量和用户确认
- 通过 → 推进阶段 2.5

---

# 阶段2：架构设计（架构师）

## 任务
基于已签收的 PRD（🟡/🔴项目为细化后的 PRD），产出技术架构方案。不仅要满足需求，还需主动分析架构约束、性能指标、安全策略、扩展性、技术债务处理等。

## 必读文件（按顺序）
1. PRD.md（🟡/🔴项目为细化后的 PRD-REFINED.md）
2. CONTEXT.md（项目上下文）
3. UI-UX-DESIGN.md（🟡/🔴项目，阶段1.7产出的设计文档，确认技术栈和组件选型）
4. docs/ui-prototype.html（🟡/🔴项目，阶段1.7产出的 HTML 原型，参考交互实现需求）

## 加载 Skill
- `tech-architecture`（架构设计方法论）
- `logging-exception`（日志/异常/错误处理规范）

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| ARCHITECTURE.md | 100 | 完整技术架构方案 |
| docker-compose.test.yml | — | E2E 测试环境定义（DB + 后端 + 前端 + 依赖服务） |
| 覆盖率工具配置 | — | JaCoCo/c8/coverage 配置（嵌入 pom.xml/package.json） |

## ARCHITECTURE.md 必须包含
1. 系统架构图
2. 技术选型（≥2个备选 + 选择理由 + trade-off）
3. 数据模型（实体关系 + 核心字段 + 索引策略）
4. API设计（请求/响应格式 + 错误码 + 认证方式）
5. 安全措施
6. 风险识别（≥3个风险 + 应对方案）
7. **代码架构**（分层+模块+组件+目录+扩展点+模式选型+日志异常）
8. **并发与边界设计**（见下方专项）

## 自身技术特性深度分析（强制执行）

架构方案不能只满足需求，必须主动分析以下 6 个维度：

### A. 架构约束分析
- **技术栈限制**：选型框架的版本约束、兼容性、已知 issue
- **基础设施约束**：部署环境（云/自建/混合）、资源限制、网络拓扑
- **团队约束**：团队技术栈熟悉度、维护成本、招聘难度
- **时间约束**：MVP 上线时间对架构决策的影响

### B. 性能指标设计
- **响应时间**：P50/P95/P99 目标值，关键接口 SLA
- **吞吐量**：QPS/TPS 预估值，峰值倍数
- **数据量级**：初始数据量、增长速率、分库分表阈值
- **缓存策略**：多级缓存设计、缓存命中率目标
- **性能测试方案**：压测工具、基准数据、验收标准

### C. 安全策略设计
- **认证授权**：OAuth2/JWT/Session 选型、RBAC/ABAC 模型
- **数据安全**：加密传输(TLS)、加密存储、密钥管理
- **API安全**：限流、防重放、签名验证、CORS策略
- **依赖安全**：第三方依赖扫描、漏洞响应流程
- **审计日志**：操作审计、数据变更审计、安全事件日志

### D. 扩展性设计
- **水平扩展**：无状态设计、会话管理、负载均衡策略
- **功能扩展**：插件机制、事件驱动、策略模式预留
- **数据扩展**：分库分表方案、数据迁移策略、版本兼容
- **接口版本化**：API 版本管理策略、向后兼容规则

### E. 技术债务管理
- **已知债务识别**：哪些决策是短期妥协，为什么
- **偿还计划**：每项债务的预期偿还时间和方式
- **债务量化**：对开发效率/性能/维护成本的影响评估
- **预防机制**：代码规范、架构守护测试、定期审视

### F. 可观测性设计
- **日志规范**：结构化日志、日志级别策略、日志聚合方案
- **指标监控**：应用指标（RED 方法）、基础设施指标（USE 方法）
- **链路追踪**：分布式追踪方案、Trace ID 透传
- **告警策略**：告警分级、响应流程、升级机制

## 执行流程
1. 加载 `tech-architecture` + `logging-exception` SKILL.md
2. 读 PRD.md（🟡/🔴项目还需读 UI-UX-DESIGN.md 和 ui-prototype.html）
3. 和用户讨论技术选型（Brainstorm）
4. **执行 6 维度技术特性分析**（不是简单翻译需求）
5. 产出 ARCHITECTURE.md
6. 标注高风险技术点（触发阶段2.8条件）
7. 架构师自审（最多2轮）

## 检查项（脚本强制）
- [ ] ARCHITECTURE.md ≥100行
- [ ] docker-compose.test.yml 存在（E2E 测试环境定义）
- [ ] 覆盖率工具已配置（pom.xml 含 JaCoCo / package.json 含 c8）
- [ ] 覆盖率阈值设为 95%（低于则构建失败）
- [ ] 评审报告 ≥3检查点 + ≥1建议 + 评分
- [ ] 合同轮次 ≤2
- [ ] 如含"高风险"/"Spike"标记 → 触发阶段2.8
- [ ] ARCHITECTURE.md 包含 6 维度技术特性分析
- [ ] ARCHITECTURE.md 包含全部 11 项工程健壮性设计

## docker-compose.test.yml 要求
架构师必须在阶段2产出测试环境定义文件，确保后续阶段（开发自测、E2E、冒烟）都能一键启动完整环境：

```yaml
# docker-compose.test.yml 示例
version: "3.8"
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: test123
      MYSQL_DATABASE: app_test
    ports: ["3306:3306"]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    ports: ["8080:8080"]
    depends_on:
      mysql: { condition: service_healthy }
      redis: { condition: service_started }
    environment:
      SPRING_PROFILES_ACTIVE: test

  frontend:
    build: ./frontend
    ports: ["5173:80"]
    depends_on: [backend]
```

**要求**：
- 所有服务用 healthcheck 确认就绪（不是 sleep 等待）
- 后端依赖 DB 就绪后才启动（`condition: service_healthy`）
- 端口映射明确，和 E2E 脚本中的 baseURL 一致
- 阶段6/8/9 统一使用此文件启动环境

## 覆盖率工具配置要求
架构师必须在阶段2配置好覆盖率工具，嵌入项目构建配置中。**阈值 95%，低于则 `mvn test` / `npm test` 直接失败。**

### Java（JaCoCo，嵌入 pom.xml）
```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
    <execution>
      <id>check</id>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>BUNDLE</element>
            <limits>
              <limit>
                <counter>LINE</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.95</minimum>
              </limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

### Node.js（c8，嵌入 package.json）
```json
{
  "scripts": {
    "test": "c8 --lines 95 --branches 95 jest"
  },
  "c8": {
    "reporter": ["text", "html"],
    "report-dir": "coverage"
  }
}
```

### Python（pytest-cov，嵌入 pyproject.toml）
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=html --cov-fail-under=95"
```

**效果**：`mvn test` / `npm test` / `pytest` 时自动收集覆盖率，低于 95% 直接失败。开发者本地就能看到哪些行没覆盖。

## 工程健壮性设计（必须在 ARCHITECTURE.md 中体现）

架构师必须在 ARCHITECTURE.md 中明确设计以下 11 项内容。**详细规范见 `engineering-robustness` SKILL.md（dispatch.sh 自动加载）。**

1. 前端防抖/节流 — 列出所有需防抖/节流的接口和组件
2. 分布式锁/并发控制 — 每个实体标注乐观锁字段或说明无并发风险
3. 边界条件清单 — 逐接口列出边界条件处理策略
4. 超时设计 — 列出所有外部调用及超时配置
5. 缓存策略 — 每个缓存的 key 设计、TTL、失效策略
6. 限流 — 维度 + 阈值 + 超限响应
7. 文件上传安全 — 类型/大小/路径/权限
8. 连接池配置 — 所有连接池参数
9. 优雅降级 — 每个非核心依赖的降级方案
10. 数据脱敏 — 所有敏感字段及脱敏规则
11. 幂等性设计 — 每个写接口的幂等方案

### 检查项
- [ ] ARCHITECTURE.md 包含全部 11 项工程健壮性设计

## 约束
- 合同：🟡中风险 标准合同 最多2轮
- 必须读取 PRD（不能靠记忆或概括）
- 🟡/🔴项目必须参考 UI/UX 设计文档和 HTML 原型
- 技术选型必须列出对比（≥2个备选）
- 数据模型必须定义字段（不能只写表名）
- 风险识别至少3个
- 6 维度技术特性分析不能遗漏
- 知识库：更新 CONTEXT.md 阶段2段落，存入 MemPalace room=arch-decisions

---

# 阶段5.5：任务分解确认

## 任务
各开发确认分配的任务合理性。

## 必读文件
1. TASK-LIST.md
2. ARCHITECTURE.md

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| confirm-tasks.md | 20 | 每个开发者的确认段落 |
| api-schema.md | 30 | 接口契约（API 路径、请求/响应格式、错误码） |

## 执行流程
1. 协调者并发调度各开发 agent
2. 各开发确认任务合理性 → 1轮复核
3. 各开发根据任务分工，定义自己负责的 API 接口（路径、请求体、响应体、错误码）
4. 汇总产出 api-schema.md（统一接口文档）
5. QA 基于 api-schema.md 写 E2E 测试（阶段6并行时使用）

## 检查项（脚本强制）
- [ ] confirm-tasks.md 存在且 ≥20行
- [ ] 包含每个开发者的确认段落
- [ ] api-schema.md 存在且 ≥30行
- [ ] api-schema.md 包含 API 路径定义（至少3个接口）
- [ ] 追溯完整性：PRD 的每个 REQ 都有任务覆盖（pipeline-check.sh 自动检查）
- [ ] 追溯完整性：PRD 的每个 REQ 都有测试用例覆盖（pipeline-check.sh 自动检查）

## 约束
- 无合同限制
- 此阶段通过后，QA-TEST-STRATEGY.md 应归档到 docs/
- 如果发现 REQ 未被任务或测试覆盖，必须补充后才能通过

---

# 阶段5：任务分解 + QA 测试计划

## 任务
协调者产出开发任务清单，QA 同步产出测试计划（并发）。

## 必读文件
1. PRD.md
2. ARCHITECTURE.md
3. UX-DESIGN.md / UI-DESIGN.md
4. CONTEXT.md

## 加载 Skill
| 角色 | Skill |
|------|-------|
| 协调者 | `task-decomposition` |
| QA | `qa-workflow` |

## 产出物
| 文件 | 最低行数 | 角色 | 说明 |
|------|---------|------|------|
| TASK-LIST.md | 50 | 协调者 | 开发任务清单（含批次/依赖/开发者分配/需求关联） |
| test-plan.md | 30 | QA | 测试计划（每个用例关联 REQ-xxx） |

## TASK-LIST.md 格式（强制）
每个任务必须包含 `**需求**` 字段，关联 PRD 中的 REQ-xxx 编号：

```markdown
### T-001: {任务标题}
**批次**: P0
**依赖**: 无
**开发者**: dev1
**并发组**: g1
**需求**: REQ-001

{任务描述}

### T-002: {任务标题}
**批次**: P0
**依赖**: 无
**开发者**: dev2
**并发组**: g1
**需求**: REQ-002

{任务描述}

### T-003: {任务标题}
**批次**: P1
**依赖**: T-001
**开发者**: dev3
**并发组**: g2
**需求**: REQ-003

{任务描述}
```

**开发者字段规范**：
- 必须指定具体 agent-id：`dev1`、`dev2`、`dev3`
- 不允许写"后端"、"前端"等泛称（脚本无法识别）
- 复杂任务可以标注多个：`dev1, dev2`（由协调者拆分或指定主责）
- 协调者应尽量均衡分配：3个开发者的任务数差异 ≤2

**禁止**：任务不标注 `**需求**` 字段，或标注的 REQ 在 PRD 中不存在。

## test-plan.md 格式（强制）
每个测试用例必须包含 `**覆盖**`、`**来源**` 字段：

```markdown
### TC-001: {场景描述}
**覆盖**: REQ-xxx
**来源**: PRD验收标准"{原文摘录}"
**步骤**: {操作步骤}
**预期**: {预期结果}
```

- `**覆盖**`：关联的 REQ-xxx
- `**来源**`：PRD 中对应验收标准的原文摘录（证明从 PRD 推导，不是凭空编的）

**每个 REQ 的 TC 推导规则：** 每条验收标准 → 至少 1 个正向 TC + 1 个逆向 TC，再补边界/接口 TC。

**禁止**：不标注 `**覆盖**` 或 `**来源**` 字段。

## 执行流程
1. 协调者并发调度自己（任务分解）+ QA（测试计划）
2. 协调者：加载 `task-decomposition`，和用户讨论拆分方式 → 产出 TASK-LIST.md
3. **TASK-LIST.md 产出后必须给用户确认**（并发组划分、任务粒度、依赖关系），用户确认后才进入阶段5.5
4. QA：加载 `qa-workflow`，产出 test-plan.md
5. 各自审查 → 签收/打回（最多2轮）

## 检查项（脚本强制）
- [ ] TASK-LIST.md ≥50行
- [ ] test-plan.md ≥30行
- [ ] 两个评审报告 ≥3检查点 + 评分
- [ ] 合同轮次 ≤2
- [ ] TASK-LIST.md 包含依赖/开发者/并发组信息
- [ ] 并发组划分合理：同组任务修改的文件不重叠
- [ ] 无优先级字段（不做的一律不拆）
- [ ] TASK-LIST.md 每个任务有 `**需求**` 字段（REQ-xxx）
- [ ] TASK-LIST.md 每个任务的 `**开发者**` 使用 dev1/dev2/dev3（不允许泛称）
- [ ] 三个开发者任务分配均衡（差异 ≤2）
- [ ] PRD 的每个 REQ 至少被一个任务覆盖
- [ ] test-plan.md 每个用例有 `**覆盖**` 字段（REQ-xxx）
- [ ] PRD 的每个 REQ 至少被一个测试用例覆盖

## 约束
- 合同：🟡中风险 标准合同 最多2轮
- Brainstorm：和用户讨论拆分方式、优先级、依赖
- 知识库：更新 CONTEXT.md 阶段5段落，存入 MemPalace room=task-breakdown

---

# 阶段6.3：代码集成

## 任务
将多个开发者的代码集成到一起，运行冒烟测试确认基本功能可用。

## 执行者
- **集成**：dev3
- **冒烟验证**：协调者

## 必读文件
1. dev/ 代码（各开发产出）
2. ARCHITECTURE.md（架构方案）
3. TASK-LIST.md（任务清单）

## 加载 Skill
无

## 产出物
| 文件 | 说明 |
|------|------|
| 集成后代码 | 合并到统一目录 |
| 冒烟测试结果 | 基本功能验证通过 |

## 执行流程
1. dev3 读取各开发者的代码产出
2. 检查代码冲突、接口不一致、命名冲突
3. 合并代码到统一目录
4. 协调者运行冒烟测试（基本功能能跑通）
5. 记录集成问题及修复结果

## 冒烟验证规则（协调者负责）
- 逐项执行，每项输出：验证项名称、执行步骤、预期结果、实际结果、✅/❌
- 冒烟不通过禁止进入6.5
- 冒烟失败 → 开发修复 → 重做冒烟 → 通过后进6.5
- 首次失败后最多重试3次（总计4次尝试）
- 第4次仍失败 → 协调者自判回退目标（编译/依赖/基础设施→阶段2；功能缺失/实现错误→阶段5），写回退记录
- 冒烟修复总时限≤2h（从首次冒烟开始计时），超时 escalated 用户决策

## 检查项（脚本强制）
- [ ] 集成后代码存在
- [ ] 冒烟测试通过

## 约束
- 集成失败 → 记录问题，调度对应开发修改 → 重新集成（最多2轮）
- 超限 → 升级给用户
- 通过后推进阶段6.5（架构审查）

---

# 阶段6.5：开发审查（架构师审查）

## 任务
架构师审查开发代码的架构合规性。

## 必读文件（强制）
1. 被审查者的代码文件
2. （ARCHITECTURE.md 由你在阶段2产出，同 session 上下文已知，无需重读。如上下文被压缩则重新读取）

## 加载 Skill
- `code-review-checklist`（审查维度清单）

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| cross-review-dev.md | 60 | 架构师独立审查段落 ≥20行，≥3检查点 |

## 审查重点
- 代码是否符合架构方案中的分层、模块、模式选型
- 日志异常是否符合 `logging-exception` 规范
- SOLID 原则
- 设计模式使用

## 执行流程
1. 架构师加载 `code-review-checklist`
2. 先读 ARCHITECTURE.md，再读被审查代码
3. 对比代码 vs 架构文档
4. 产出评审意见 → 开发修改 → 确认

## 检查项（脚本强制）
- [ ] cross-review-dev.md 存在
- [ ] 架构师有独立审查段落
- [ ] 每段 ≥3检查点
- [ ] 审查报告引用了架构相关内容

## 约束
- 1轮修复后仍不通过 → 升级到阶段7

---

# 阶段6：开发执行

## 任务
协调者按任务清单逐个 dispatch 开发 agent，每个任务一次调度。QA 同步写 E2E 测试脚本。

**开发不能简单机械地翻译 PRD**，必须遵循技术栈最佳实践，将任务拆分成独立小流程逐步执行。

## 必读文件（协调者）
1. docs/ARCHITECTURE.md
2. TASK-LIST.md
3. api-schema.md（阶段5.5产出）
4. PRD.md（🟡/🔴项目为细化后的 PRD，含交互细节/边界/异常处理）
5. UI-UX-DESIGN.md（🟡/🔴项目，阶段1.7产出）
6. docs/ui-prototype.html（🟡/🔴项目，阶段1.7产出的 HTML 原型参考）

## 加载 Skill
| 角色 | Skill |
|------|-------|
| 开发 | `code-quality-guard`, `logging-exception` |
| QA（并行） | `qa-workflow` |

## 执行流程

协调者只需调一行命令，脚本自动完成所有调度：

```bash
bash /Users/sunwenyong/.openclaw/agents/agent-pipeline/scripts/run-stage-6.sh {项目名} {项目目录}
```

脚本自动：
1. 解析 TASK-LIST.md，提取所有任务和依赖关系
2. 创建 6/progress.json 追踪完成状态
3. 按依赖顺序逐个 dispatch（依赖完成才 dispatch 下一个）
4. 每个任务失败自动重试 1 次
5. 输出最终执行报告

## 技术栈最佳实践（开发必须遵循）

开发不是简单翻译 PRD，必须在每个任务中主动应用以下最佳实践：

### A. 状态管理最佳实践
- **全局状态**：仅跨组件/跨页面共享的状态放入全局 store
- **本地状态**：组件私有状态用 useState/useReducer，不污染全局
- **服务端状态**：API 数据用 TanStack Query / SWR 管理，不做手动缓存
- **表单状态**：复杂表单用 dedicated form library（react-hook-form / vee-validate）
- **URL 状态**：筛选/分页/Tab 状态同步到 URL，支持书签和前进后退

### B. 错误边界与异常处理
- **React Error Boundary**：每个关键路由/组件包裹 ErrorBoundary
- **API 错误**：统一拦截器处理 401/403/500，业务错误用 Toast 提示
- **异步错误**：Promise 链必须有 catch 或 try-catch
- **网络错误**：Axios/Fetch 超时配置 + 重试策略 + 离线检测
- **渲染错误**：Suspense fallback + ErrorBoundary 兜底

### C. 性能优化
- **渲染优化**：React.memo/useMemo/useCallback 按需使用，避免过度优化
- **代码分割**：路由级 lazy loading，大组件动态 import
- **列表虚拟化**：超过 100 项的列表用 virtual scroll
- **图片优化**：懒加载、WebP/AVIF、响应式 srcset、占位骨架屏
- **Bundle 优化**：Tree shaking、按需引入、分析 bundle size

### D. 代码规范
- **TypeScript strict mode**：noImplicitAny、strictNullChecks 全开
- **命名规范**：组件 PascalCase、函数/变量 camelCase、常量 UPPER_SNAKE
- **文件组织**：一个文件一个组件/类、按功能分目录、index 统一导出
- **注释规范**：JSDoc 公共接口、TODO 标记技术债、避免冗余注释
- **Git 规范**：Conventional Commits、原子提交、有意义的 message

### E. 安全编码
- **输入校验**：前端校验 + 后端校验双重保障
- **XSS 防护**：不使用 dangerouslySetInnerHTML，输出编码
- **CSRF 防护**：Token 机制、SameSite Cookie
- **敏感数据**：Token 不存 localStorage（用 httpOnly Cookie）、密码不明文

### F. 任务逐步执行策略

每个任务不是一次性完成所有代码，而是拆分成独立的小流程逐步执行：

1. **接口定义**：先定义 API 接口/类型，确保契约一致
2. **数据层**：实现数据获取/存储逻辑（Repository/Service 层）
3. **业务逻辑层**：实现核心业务逻辑（UseCase/Handler 层）
4. **UI 层**：实现页面和组件
5. **状态管理**：接入全局状态管理
6. **异常处理**：添加错误边界和异常提示
7. **单元测试**：为每层编写单元测试
8. **集成验证**：连接前后端验证完整流程

每步完成后运行测试确认正确，再进入下一步。

## 进度追踪

6/progress.json 格式：
```json
{
  "completed": ["T-001", "T-002"],
  "failed": ["T-003"]
}
```

脚本自动维护，支持中断后继续执行（跳过已完成任务）。

## 产出物
| 文件 | 说明 |
|------|------|
| 6/ 代码文件 | 按任务清单逐任务产出 |
| 6/progress.json | 任务完成进度 |
| 6/task-reports/{task_id}.md | 每个任务的产出摘要（含完成内容、文件清单、验收标准确认） |
| 6/dev-log.md | 开发日志（每个任务追加） |
| tests/ 测试脚本 | QA 同步产出 Playwright E2E |

## 测试要求（开发写）
- 单元测试 → `tests/unit/{task_id}/`（每个任务独立目录）
- 集成测试 → `tests/integration/`
- **集成测试禁止 mock 数据库/Redis/MQ**，必须连接 `docker-compose.test.yml` 启动的真实服务
- mock 仅允许用于外部第三方 API（支付、短信等不可控服务）
- 每个 test case 至少 1 个有效断言
- 写完立刻跑测试，不通过当场修
- 单元测试由 dispatch-task.sh 自动执行验证

## 工程健壮性实现要求（开发必须遵守）

**详细规范见 `engineering-robustness` SKILL.md（dispatch.sh 自动加载）。** 以下为检查清单：

### 检查项
- [ ] 所有提交按钮有防重复提交保护
- [ ] 搜索/滚动等高频操作有 debounce/throttle
- [ ] 写操作有并发控制（乐观锁/分布式锁/幂等）
- [ ] 每个 API 有边界条件测试（空值/空集合/溢出/并发冲突）
- [ ] 金额字段使用 BigDecimal（非 double/float）
- [ ] 日期处理有时区一致性
- [ ] 所有外部调用有显式超时配置
- [ ] 缓存有穿透/雪崩/击穿防护
- [ ] 公开 API 有限流配置
- [ ] 文件上传有类型/大小/路径校验
- [ ] 连接池已显式配置（不依赖默认值）
- [ ] 非核心依赖有降级/fallback
- [ ] 敏感字段有脱敏处理
- [ ] 写接口支持幂等

## 覆盖率自测（每个任务完成后必须）
开发完成每个任务后，必须验证覆盖率：

```bash
# 1. 启动测试环境
cd {项目目录} && docker-compose -f docker-compose.test.yml up -d
# 等待就绪...

# 2. 跑全部测试（单元 + 集成），JaCoCo/c8 自动收集覆盖率
cd {项目目录}/6 && mvn test  # 或 npm test

# 3. 检查覆盖率报告
# Java: target/site/jacoco/index.html
# Node: coverage/index.html

# 4. 清理
docker-compose -f docker-compose.test.yml down
```

**覆盖率阈值 95%**（阶段2架构师配置）。`mvn test` / `npm test` 低于 95% 直接失败，不允许提交。

## 测试日志监控（每次跑测试必须）

跑测试时必须捕获完整输出（stdout + stderr），失败时保留日志供排查：

```bash
# 单元测试日志
cd {项目目录}/6 && mvn test 2>&1 | tee logs/unit/T-{task_id}.log

# 集成测试日志
cd {项目目录}/6 && mvn verify 2>&1 | tee logs/integration/T-{task_id}.log
```

**要求：**
- 测试通过：日志保留，标记 `PASS`
- 测试失败：日志保留，标记 `FAIL`，**开发必须先看日志再修代码**，不要盲改
- 日志必须包含：失败用例名、错误堆栈、断言差异（expected vs actual）
- 日志目录：`logs/unit/`、`logs/integration/`、`logs/e2e/`（gitignore）

**禁止：**
- ❌ 测试失败后不看日志就改代码
- ❌ 只看"测试通过/失败"的汇总行，不看具体失败用例
- ❌ 日志输出到 /dev/null

## QA E2E 测试（阶段6并行）
QA 在开发执行的同时编写 E2E 测试脚本：
- E2E 测试 → `tests/e2e/`
- 工具：Playwright（首次使用前运行 `check-test-tools.sh` 检查安装）
- QA 写完 E2E 脚本后，进入阶段7-test-review 做交叉审查

## 前置方案审查（强制）
开发过程中如果发现前面阶段的方案有问题、有 bug、有遗漏：
1. **能自行判断的** → 直接补全修复，不要等
2. **无法判断如何处理的** → 立即中断，询问用户
3. **修改了实现逻辑的** → 通知对应文档的负责人，按实际实现逻辑重新修改文档（ARCHITECTURE.md / api-schema.md / TASK-LIST.md 等）

## 检查项（脚本强制）
- [ ] 6/ 目录存在且含代码文件
- [ ] tests/ 目录存在且含测试文件
- [ ] tests/integration/ 存在且有测试文件（集成测试）
- [ ] progress.json 存在且 completed 非空
- [ ] 代码遵循分层架构（Controller 不直接引用 Repository）
- [ ] 覆盖率 ≥95%（JaCoCo/c8 报告存在且达标）
- [ ] 集成测试连接真实 DB（非 mock）
- [ ] TypeScript strict mode 已开启（如适用）
- [ ] ErrorBoundary 已配置（如适用）
- [ ] API 统一错误拦截器已配置

## 约束
- 单任务超时：2小时（dispatch-task.sh 内置）
- 单任务最大轮次：50轮
- 失败重试：1次
- 重试仍失败 → 中断，询问用户
- ❌ 禁止只看任务描述就直接写代码
- ❌ 禁止在此阶段写 E2E 测试（QA 负责）
- ❌ 禁止一次性写完所有代码（必须逐步执行）

---

# 阶段7-test-review：测试交叉审查

## 概述
开发完成阶段6后，进入测试交叉审查。QA 验收开发的测试，开发确认 QA 的 E2E 测试。

## 流程总览

```
Step 1: QA 验收单元测试（逐任务）
  │
  ├─ 通过 → Step 2
  ├─ 不通过 → 开发补充测试 → QA 复审（第2轮）
  └─ 仍不通过 → 升级用户
  │
Step 2: QA 验收集成测试
  │
  ├─ 通过 → Step 3
  ├─ 不通过 → 开发补充测试 → QA 复审（第2轮）
  └─ 仍不通过 → 升级用户
  │
Step 3: QA E2E 测试自查
  │
  ├─ 通过 → Step 4
  ├─ 不通过 → QA 自行修改 → 自查（第2轮）
  └─ 仍不通过 → 升级用户
  │
Step 4: 开发确认 E2E 测试脚本
  │
  ├─ 通过 → 产出 test-review.md，进入阶段7代码审查
  ├─ 不一致 → QA 修改脚本 → 开发复审（第2轮）
  └─ 仍不一致 → 升级用户
```

## 审查标准

### 单元测试验收（QA 审查）

| 检查项        | 通过标准                       | 不通过处理            |
| ---------- | -------------------------- | ---------------- |
| **test-plan 追溯** | 测试用例覆盖 test-plan.md 中对应 REQ 的 TC-xxx，测试注释标注 TC-xxx | 开发补充缺失的 TC 对应测试 |
| 验收标准覆盖     | 每个验收标准有 ≥1 个测试用例           | 开发补充缺失的测试        |
| mock 比例    | ≤ 50%                      | 开发减少 mock，改用真实依赖 |
| 核心逻辑禁 mock | 业务逻辑未被 mock                | 开发改用真实调用         |
| **独立运行**       | 每个测试自包含：自己创建数据、自己清理、无顺序依赖 | 开发改为独立 fixture   |
| **数据隔离**       | 测试数据用 UUID/时间戳唯一化，不硬编码共享数据 | 开发改用唯一标识        |
| 有效断言       | 每个 test case 有 ≥1 个 assert | 开发补充断言           |
| 异常覆盖       | 关键异常路径有测试                  | 开发补充异常测试         |

**评分标准：**
- 8-10：优秀，直接通过
- 7：合格，通过但有 minor 建议
- 5-6：需补充，列出缺失项，开发补充后复审
- <5：不合格，打回重写

### 集成测试验收（QA 审查）

| 检查项 | 通过标准 | 不通过处理 |
|--------|---------|-----------|
| 接口调用链 | Controller → Service → Repository 全链路 | 开发补充调用链测试 |
| 异常路径 | 参数错误/权限不足/资源不存在 | 开发补充异常测试 |
| 数据库交互 | 事务、回滚有测试 | 开发补充事务测试 |
| 独立运行 | 不依赖外部服务 | 开发 mock 外部依赖 |

### E2E 测试自查（QA 自查）

| 检查项 | 通过标准 | 不通过处理 |
|--------|---------|-----------|
| **test-plan 追溯** | E2E 测试覆盖 test-plan.md 中的 TC-xxx，测试名/注释标注 TC-xxx | QA 补充缺失的 TC 对应测试 |
| P0 流程覆盖 | 所有 P0 功能有 E2E 测试 | QA 补充缺失场景 |
| **PRD 驱动** | 测试场景从 PRD 验收标准推导，不是只看页面写 | QA 补充 PRD 驱动的测试场景 |
| 异常路径 | 关键异常有测试 | QA 补充异常场景 |
| 选择器稳定性 | 避免 brittle selectors | QA 改用 data-testid |
| 等待策略 | 无硬编码 sleep | QA 改用 waitFor |
| **测试数据独立** | 每个测试自包含：自己创建数据、自己清理、无顺序依赖 | QA 改为独立 fixture |
| **随机顺序可执行** | `--random-order` 下全部通过 | QA 修复依赖关系 |
| **前端错误监听** | 注册 console.error/pageerror/network 监听 | QA 补充错误监听代码 |

### E2E 测试开发确认

| 检查项 | 通过标准 | 不通过处理 |
|--------|---------|-----------|
| 路由一致 | 测试中的路由与实际路由匹配 | QA 修改路由 |
| 字段一致 | 表单字段名与实际一致 | QA 修改字段名 |
| 接口一致 | API 路径与实际一致 | QA 修改接口路径 |
| 预期结果 | 预期返回与实际一致 | QA 修改预期 |
| 功能已实现 | 测试覆盖的功能已实现 | 标记待实现，跳过该测试 |

## 审查轮次规则

- **最多 2 轮**：初审 + 1 次复审
- **第 1 轮不通过** → 对应角色修改 → 进入第 2 轮
- **第 2 轮仍不通过** → 升级用户决策
- **轮次计数**：每步独立计数（单元测试 2 轮、集成测试 2 轮、E2E 自查 2 轮、E2E 确认 2 轮）

## 产出物

| 文件 | 说明 | 最低行数 |
|------|------|---------|
| test-review.md | 汇总报告（含各步骤审查结果） | 30 |
| unit-{task_id}.md | 逐任务单元测试验收 | — |
| integration-review.md | 集成测试验收 | — |
| e2e-self-review.md | E2E 自查报告 | — |
| e2e-dev-confirm.md | E2E 开发确认报告 | — |

## 执行命令

```bash
# 一键执行测试交叉审查
bash agent-pipeline/scripts/run-test-review.sh {项目名} {项目目录}
```

## 约束
- 测试审查通过后才进入阶段7代码审查
- 审查不通过 → 对应角色修改 → 复审 → 仍不通过 → 升级用户
- 每步审查结果必须写入文件，不能只口头说"通过"

---

# 阶段7：代码审查（架构师 + QA + PM）

## 前置条件
测试交叉审查（stage-7-test-review）必须通过。未通过则不能进入本阶段。

## 任务
架构师做架构合规验证，QA 做业务+健壮性验证，PM 做需求覆盖验证。开发修改后，审查者复审确认。

## 必读文件

### 架构师
1. dev/ 代码
2. （ARCHITECTURE.md 由你在阶段2产出，同 session 上下文已知，无需重读）

### QA
1. dev/ 代码
2. 7/test-reviews/ 测试审查报告（stage-7-test-review 产出）

### PM
1. dev/ 代码
2. PRD.md（验证需求覆盖）

## 加载 Skill
| 角色 | Skill |
|------|-------|
| 架构师 | `code-review-checklist`, `logging-exception` |
| QA | `qa-workflow`, `humanize-code`, `logging-exception` |
| PM | — |

## 各角色审查维度
| 角色 | 审查视角 |
|------|---------|
| 架构师 | 分层合规、模块隔离、模式使用、日志异常规范、**工程健壮性设计落地**、逻辑 bug |
| QA | 业务逻辑、**健壮性（边界/并发/异常路径）**、去AI味、测试审查报告验证、逻辑 bug |
| PM | PRD 需求覆盖、功能完整性、优先级合理性、逻辑 bug |
| 开发2 | 代码质量：命名规范、重复代码、技术债、逻辑 bug |

## 工程健壮性审查清单（所有审查者共用）

**详细审查要点见 `engineering-robustness` SKILL.md（dispatch.sh 自动加载）。** 以下为检查清单：

- [ ] 前端防抖/节流：提交按钮 disabled、搜索 debounce、滚动 throttle、定时器清理
- [ ] 并发控制：乐观锁/分布式锁/幂等、无 TOCTOU 竞态
- [ ] 边界条件：空值校验、空集合、分页修正、字符串/数值/日期边界
- [ ] 超时配置：所有外部调用有显式超时、无 timeout=0
- [ ] 缓存：穿透/雪崩/击穿防护、Cache Aside 策略
- [ ] 限流：公开 API 有限流、超限 429、前端友好提示
- [ ] 文件上传：content-type + magic bytes、UUID 文件名、路径不可控
- [ ] 连接池：DB/Redis/HTTP 连接池显式配置
- [ ] 优雅降级：fallback 存在、重试有上限、死信队列
- [ ] 数据脱敏：日志/API/DB/前端敏感字段处理
- [ ] 幂等：创建有唯一约束、更新有乐观锁、回调有状态机

## 执行流程

### 第一步：安全扫描（架构师负责，最先执行）

代码审查前先跑安全扫描，发现问题优先修复：

```bash
bash agent-pipeline/scripts/security-scan.sh {项目目录}/6
```

**处理规则：**
- 🔴 严重问题（硬编码密钥、SQL注入、XSS、路径穿越）→ 必须修复，不通过不允许进阶段8
- 🟡 警告（CORS 通配符、日志敏感信息）→ 评估风险，可降级为后续修复
- 修复后重跑，直到 0 严重问题

**产出**：将扫描结果追加到 review-report.md 的架构师段落。

### 第二步：逐任务审查（自动化）
每个审查者调用 run-review.sh，自动对每个已完成任务做代码审查：

```bash
bash agent-pipeline/scripts/run-review.sh {项目名} {reviewer-id} {项目目录}
# reviewer-id: architect, qa, pm, dev2
```

脚本自动：
1. 读取 pipeline/6/progress.json 获取所有已完成任务
2. 逐个任务读取 pipeline/6/task-reports/{task_id}.md + 对应代码
3. 对照验收标准逐条检查
4. 产出 pipeline/7/task-reviews/{task_id}.md
5. 做跨任务集成审查
6. 汇总 7/review-report.md

### 第三步：开发修改
开发根据审查意见修改代码。每个审查者的问题逐条修复。

### 第四步：审查者复审（第2轮）
三个角色确认各自提出的问题已修复，产出 re-review-code.md。

复审检查项：
- 架构师：之前提出的问题是否已修复，是否引入新问题
- QA：单元测试/集成测试是否已补充，E2E 测试是否已调整
- PM：需求覆盖是否完整，功能是否符合 PRD

### 第五步：推进
- 复审通过 → 推进阶段 8
- 仍有问题 → 开发再改（第3轮，最多 3 轮）
- 超过 3 轮 → 升级用户决策

## 产出物
| 文件 | 说明 |
|------|------|
| review-report.md | 架构师、QA、PM 各有独立段落，每段 ≥3检查点 + ≥1建议 + 评分 |
| re-review-code.md | 三个角色复审确认 |
| screenshots/ | Playwright 截图 ≥1张 |

## 约束
- 总轮次 ≤3（初审 + 复审算 1 轮）
- 超限 → escalated → 协调者汇报用户
- 通过 → 推进阶段 8

---

# 阶段8.5：PM 验收

## 任务
PM 对照 PRD 逐条验证测试报告，确认需求被正确实现。

## 必读文件
1. PRD.md（需求基准）
2. test-report.md（阶段8产出）
3. review-report.md（阶段7产出）

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| pm-acceptance.md | 30 | PM 验收报告 |

## 产出物规范

pm-acceptance.md 必须包含以下结构：

```markdown
# PM 验收报告

## 需求逐项对照
| # | PRD 需求项 | 测试覆盖 | 结果 |
|---|-----------|---------|------|
| 1 | {需求描述} | test-report.md 第X节 | ✅/🔴 |

## 遗留问题
- {问题清单，无则写"无"}

## 结论
- [ ] 通过 / [ ] 不通过
- 不通过原因：{具体说明}
```

## 执行流程
1. 读取 PRD.md，提取所有需求项
2. 读取 test-report.md，逐条对照测试覆盖情况
3. 读取 review-report.md，确认代码审查无阻塞问题
4. 产出 pm-acceptance.md
5. 给出明确结论：通过 / 不通过

## 检查项（脚本强制）
- [ ] pm-acceptance.md 存在且非空
- [ ] ≥30行
- [ ] 包含"结论"关键词（确认有结论段落）
- [ ] 包含"PRD"关键词（确认引用了需求文档）
- [ ] 包含"通过"或"不通过"关键词（确认有明确判定）

## 约束
- 不通过 → 记录问题到 changes/，回退到对应阶段修复（最多2轮）
- 超限 → 升级给用户
- 通过 → 推进阶段9（交付验收）

---

# 阶段8：测试执行（QA + PM）

## 前置条件
- 测试交叉审查（stage-7-test-review）已通过
- 代码审查（stage-7）已通过

## 任务
QA 执行所有测试脚本，PM 验证测试覆盖 PRD 需求。

**测试用例必须基于细化后的 PRD 和 UI 原型编写**，覆盖交互流程和异常场景。

## 必读文件
1. tests/unit/ 开发写的单元测试（阶段6产出，阶段7 QA已验收）
2. tests/integration/ 开发写的集成测试（阶段6产出，阶段7 QA已验收）
3. tests/e2e/ QA 写的 E2E 测试（阶段6产出，阶段7已确认）
4. test-plan.md（阶段5产出）
5. PRD.md（🟡/🔴项目为细化后的 PRD，含交互细节/边界/异常处理描述）
6. PRD-REFINED.md（🟡/🔴项目，阶段1.8产出的细化 PRD，测试用例需覆盖细化内容）
7. UI-UX-DESIGN.md（🟡/🔴项目，阶段1.7产出，测试交互行为需与设计一致）
8. docs/ui-prototype.html（🟡/🔴项目，阶段1.7产出的 HTML 原型，验证 UI 行为）

## 加载 Skill
- `qa-workflow`

## 前置工具检查

```bash
# 检查测试工具是否已安装（缺失才安装）
bash agent-pipeline/scripts/check-test-tools.sh {项目目录}
```

## 产出物
| 文件 | 说明 |
|------|------|
| test-report.md | 测试报告（含逐项结果、通过率、问题清单、REQ 追溯矩阵） |
| qa-reports/*.png | 测试截图 ≥3张 |
| test-case-review.md | PM 测试用例评审意见 |
| error-monitor/error-report.md | 错误监控报告（前后端隐含错误） |

## 执行流程

### Step 0: 工具检查
```bash
bash agent-pipeline/scripts/check-test-tools.sh {项目目录}
```

### Step 1: 测试用例对照（基于细化 PRD 和 UI 原型）

QA 必须基于以下基准验证测试覆盖：

**细化 PRD（🟡/🔴项目）**：
- 交互细节测试：验证每个 REQ 的操作路径、交互方式、反馈时机
- 边界情况测试：验证每个 REQ 标注的边界场景
- 文案规范测试：验证页面标题、按钮、提示文案符合规范
- 异常处理测试：验证输入校验、网络异常、权限异常等路径

**UI 原型（🟡/🔴项目）**：
- 交互一致性：实际 UI 行为与 HTML 原型一致
- 组件状态：正常/空/加载/错误状态切换正确
- 响应式：至少验证 Desktop + Mobile 两种布局

**🟢小型项目**：基于原始 PRD 验收标准测试即可。

### Step 2: 测试执行
按 test-plan.md 顺序执行：
1. 单元测试 → `mvn test` / `npm test`
2. 集成测试 → `mvn verify` / `npm run test:integration`
3. E2E 测试 → `npx playwright test`
4. 记录每个测试结果

### Step 3: REQ 追溯矩阵
生成测试报告时，必须包含 REQ 追溯矩阵：

```markdown
## REQ 追溯矩阵
| REQ | 功能 | TC 数 | 通过 | 失败 | 覆盖率 |
|-----|------|-------|------|------|--------|
| REQ-001 | 用户登录 | 5 | 5 | 0 | 100% |
| REQ-002 | 数据导出 | 8 | 7 | 1 | 87.5% |
```

### Step 4: 功能点标签更新
- 测试通过的 REQ → `测试-通过`
- 测试失败的 REQ → `测试-失败`（回退到开发-进行中）

### Step 5: PM 测试用例评审
PM 对照 PRD 验证：
- 每个 REQ 至少有 1 个正向 TC + 1 个逆向 TC
- 边界场景已覆盖（🟡/🔴项目参考细化 PRD 的边界情况章节）
- 异常路径已覆盖（🟡/🔴项目参考细化 PRD 的异常处理章节）
- 交互行为与 UI 设计一致（🟡/🔴项目）

## 检查项（脚本强制）
- [ ] test-report.md 存在且 ≥50行
- [ ] qa-reports/ 存在且含截图 ≥3张
- [ ] REQ 追溯矩阵完整（每个 REQ 至少 1 个 TC）
- [ ] 每个 REQ 至少 1 正向 + 1 逆向 TC
- [ ] 覆盖率 ≥95%
- [ ] 集成测试连接真实 DB
- [ ] 功能点标签已更新

## 约束
- 合同：🔴高风险 最多3轮
- 测试失败 → 开发修复 → QA 回归验证
- 修复后仅重跑失败用例（非全量重跑）
- 单次回归超时：1小时

---

# 阶段9：交付验收（协调者）

## 任务
端到端验收，产出验收报告和交付文档。

## 必读文件
所有阶段产出物

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| ACCEPTANCE-REPORT.md | 50 | 验收报告（7项 checklist 全部 ✅） |
| docs/user-manual.md | 100 | 用户使用手册 |
| docs/api-docs.md | — | API 接口文档 |
| docs/rpc-api-docs.md | — | RPC 接口文档 |
| docs/integration-guide.md | — | 接入指南（必须含步骤说明） |
| docs/*.html | — | 关键文档的 HTML 版本（结构清晰、便于阅读） |

## 交付文档写作规则
- **必须在阶段7签收后才能写**（基于最终代码）
- 写完后开发确认准确性 + QA 验证可操作性
- 时限：4小时

## HTML 转换（必须）
将以下文档转成 HTML 版本，存入 `docs/` 目录：
- ACCEPTANCE-REPORT.md → docs/acceptance-report.html
- PRD.md → docs/prd.html
- ARCHITECTURE.md → docs/architecture.html
- docs/user-manual.md → docs/user-manual.html
- docs/api-docs.md → docs/api-docs.html

**HTML 要求：**
- 单文件、内联 CSS、无外部依赖
- 表格/标题/代码块/标签样式清晰
- 参考 `agent-pipeline/PIPELINE-GUIDE.html` 的样式风格

## 协调者冒烟验证（交付前必须）

在产出验收报告前，协调者必须亲自跑以下命令确认系统可用：

```bash
# 1. 使用阶段2产出的 docker-compose.test.yml 启动完整环境
cd {项目目录}
docker-compose -f docker-compose.test.yml up -d
# 等待服务就绪（healthcheck 自动判断）
sleep 10

# 2. 健康检查
curl -sf http://localhost:8080/actuator/health || echo "❌ 健康检查失败"

# 3. 核心接口冒烟（至少3个接口）
curl -s http://localhost:8080/api/xxx | head -5
curl -s http://localhost:8080/api/yyy | head -5
curl -s http://localhost:8080/api/zzz | head -5

# 4. 安全扫描（确认阶段7修复后无遗留）
bash agent-pipeline/scripts/security-scan.sh {项目目录}

# 5. 检查测试报告真实性（截图时间戳）
find {项目目录}/pipeline/8/qa-reports -name "*.png" -mtime -1 | wc -l

# 6. 清理
docker-compose -f docker-compose.test.yml down
```

**冒烟失败处理：**
- 编译失败 → 回退阶段6，发给开发
- 启动失败 → 检查日志，发给开发修复
- 接口失败 → 发给对应开发修复
- 超过2轮冒烟仍失败 → 升级给用户

## 检查项（脚本强制）
- [ ] ACCEPTANCE-REPORT.md 存在
- [ ] 7项验收 checklist 全部 ✅ 或 [x]
- [ ] 无 escalated 合同
- [ ] 安全扫描 0 严重问题
- [ ] 测试报告无 P0 遗留
- [ ] docs/ 归档完整（5个过程文档均存在）
- [ ] 交付文档齐全：
  - user-manual.md ≥100行
  - api-docs.md 存在
  - rpc-api-docs.md 存在
  - integration-guide.md 含步骤说明

## 约束
- 通过 → 输出"项目交付完成"
- 不通过 → 输出缺失项，协调者修复后重检
- 知识库：更新 CONTEXT.md 阶段9段落，存入 MemPalace room=project-lessons
