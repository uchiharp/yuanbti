# 功能点标签系统 Skill

> 本 Skill 定义全流程功能点打标规范，贯穿 Pipeline 所有阶段。

---

## 1. 标签体系

### 1.1 标签状态定义

| 标签 | 含义 | 阶段 | 打标方式 |
|------|------|------|---------|
| `PRD-待确认` | PRD 已编写，等待用户确认 | 1 | 自动 |
| `PRD-已确认` | 用户已确认 PRD | 1.6 | 人工确认 |
| `UI/UX-设计中` | UI/UX 设计进行中 | 1.7 | 自动 |
| `UI/UX-设计完成` | UI/UX 设计完成，含 HTML 原型 | 1.7 | 自动 |
| `PRD-已细化` | PRD 已根据 UI/UX 反向细化 | 1.8 | 自动 |
| `PRD-细化确认` | 细化 PRD 经人工确认 | 1.9 | 人工确认 |
| `技术方案-待确认` | 架构方案已产出，待确认 | 2 | 自动 |
| `技术方案-已确认` | 架构方案经评审确认 | 2.5/2.6 | 人工确认 |
| `开发-进行中` | 任务开发中 | 6 | 自动 |
| `开发-完成` | 开发任务完成 | 6 | 自动 |
| `测试-通过` | 测试验证通过 | 8 | 自动 |
| `测试-失败` | 测试未通过，需返工 | 8 | 自动 |
| `验收-通过` | PM 验收通过 | 8.5 | 人工确认 |
| `交付-完成` | 全流程交付完成 | 9 | 自动 |

### 1.2 标签状态机

```
PRD-待确认 → PRD-已确认 → UI/UX-设计中 → UI/UX-设计完成
    → PRD-已细化 → PRD-细化确认 → 技术方案-待确认 → 技术方案-已确认
    → 开发-进行中 → 开发-完成 → 测试-通过 → 验收-通过 → 交付-完成
                                          ↘ 测试-失败 → 开发-进行中（回退）
```

合法转换规则：
- 只能按顺序前进，不能跳跃
- 回退仅限：`测试-失败` → `开发-进行中`
- `人工确认`类标签必须等待人工操作

---

## 2. 存储格式

### 2.1 功能点标签文件
存储路径：`pipeline/feature-tags.json`

```json
{
  "version": "1.0",
  "project": "{项目名}",
  "last_updated": "2025-05-15T10:30:00Z",
  "features": {
    "REQ-001": {
      "title": "用户登录",
      "status": "PRD-已确认",
      "history": [
        {"status": "PRD-待确认", "timestamp": "2025-05-15T09:00:00Z", "operator": "auto", "phase": "1"},
        {"status": "PRD-已确认", "timestamp": "2025-05-15T10:30:00Z", "operator": "manual", "phase": "1.6", "confirmed_by": "user"}
      ]
    },
    "REQ-002": {
      "title": "数据导出",
      "status": "开发-进行中",
      "history": [
        {"status": "PRD-待确认", "timestamp": "...", "operator": "auto", "phase": "1"},
        {"status": "PRD-已确认", "timestamp": "...", "operator": "manual", "phase": "1.6", "confirmed_by": "user"},
        {"status": "UI/UX-设计中", "timestamp": "...", "operator": "auto", "phase": "1.7"},
        {"status": "UI/UX-设计完成", "timestamp": "...", "operator": "auto", "phase": "1.7"},
        {"status": "PRD-已细化", "timestamp": "...", "operator": "auto", "phase": "1.8"},
        {"status": "PRD-细化确认", "timestamp": "...", "operator": "manual", "phase": "1.9", "confirmed_by": "user"},
        {"status": "技术方案-待确认", "timestamp": "...", "operator": "auto", "phase": "2"},
        {"status": "技术方案-已确认", "timestamp": "...", "operator": "manual", "phase": "2.5"},
        {"status": "开发-进行中", "timestamp": "...", "operator": "auto", "phase": "6"}
      ]
    }
  },
  "pipeline_status": {
    "current_phase": "6",
    "phase_tags": {
      "0": "completed",
      "1": "completed",
      "1.6": "completed",
      "1.7": "completed",
      "1.8": "completed",
      "1.9": "completed",
      "2": "completed",
      "2.5": "completed",
      "5": "completed",
      "5.5": "completed",
      "6": "in_progress"
    }
  }
}
```

### 2.2 Pipeline 阶段标签

| 标签 | 含义 |
|------|------|
| `pending` | 阶段未开始 |
| `in_progress` | 阶段进行中 |
| `completed` | 阶段已完成 |
| `blocked` | 阶段被阻塞 |
| `skipped` | 阶段被跳过（规模裁剪） |

---

## 3. 自动打标规则

### 3.1 阶段完成时自动打标

| 阶段完成 | 自动操作 |
|---------|---------|
| 阶段 1 完成 | 所有 REQ → `PRD-待确认` |
| 阶段 1.6 完成 | 用户确认的 REQ → `PRD-已确认` |
| 阶段 1.7 开始 | 所有 REQ → `UI/UX-设计中` |
| 阶段 1.7 完成 | 所有 REQ → `UI/UX-设计完成` |
| 阶段 1.8 完成 | 所有 REQ → `PRD-已细化` |
| 阶段 1.9 完成 | 用户确认后 → `PRD-细化确认` |
| 阶段 2 完成 | 所有 REQ → `技术方案-待确认` |
| 阶段 2.5/2.6 完成 | 所有 REQ → `技术方案-已确认` |
| 阶段 6 任务开始 | 对应 REQ → `开发-进行中` |
| 阶段 6 任务完成 | 对应 REQ → `开发-完成` |
| 阶段 8 测试通过 | 对应 REQ → `测试-通过` |
| 阶段 8 测试失败 | 对应 REQ → `测试-失败` |
| 阶段 8.5 完成 | 对应 REQ → `验收-通过` |
| 阶段 9 完成 | 所有 REQ → `交付-完成` |

### 3.2 人工确认打标

需要人工确认的标签，协调者必须暂停并通知用户：
- `PRD-已确认`：阶段 1.6 用户审阅后
- `PRD-细化确认`：阶段 1.9 细化 PRD 审阅后
- `技术方案-已确认`：阶段 2.5/2.6 评审后
- `验收-通过`：阶段 8.5 PM 验收后

---

## 4. 进度看板

每次标签变更时，自动生成进度摘要（追加到 `pipeline/feature-tags-summary.md`）：

```markdown
# 功能点进度看板
> 最后更新：2025-05-15 10:30:00

| REQ | 功能 | 当前状态 | 阶段 |
|-----|------|---------|------|
| REQ-001 | 用户登录 | PRD-已确认 | 1.6 ✅ |
| REQ-002 | 数据导出 | 开发-进行中 | 6 🔄 |
| REQ-003 | 权限管理 | 测试-通过 | 8 ✅ |

**统计**：
- 总功能点：3
- 已完成：1（33%）
- 进行中：1（33%）
- 待开发：1（33%）
```

---

## 5. 脚本集成

### 5.1 标签操作脚本
```bash
# 初始化标签（阶段1完成后调用）
bash scripts/feature-tags.sh init <项目目录>

# 更新标签（每阶段完成后调用）
bash scripts/feature-tags.sh update <项目目录> <阶段> <新状态>

# 人工确认（等待用户操作）
bash scripts/feature-tags.sh confirm <项目目录> <REQ编号>

# 生成进度看板
bash scripts/feature-tags.sh summary <项目目录>

# 检查所有标签是否一致
bash scripts/feature-tags.sh check <项目目录>
```

### 5.2 pipeline-check.sh 集成
在阶段检查时增加标签一致性验证：
- 阶段 N 的检查逻辑中，验证所有 REQ 的标签 ≥ 该阶段对应的标签状态
- 不一致则报 🟡 警告
