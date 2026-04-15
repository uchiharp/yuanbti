# 任务执行验证系统（小灵检测）

## 核心原则

> **没有证据 = 没有执行**

每个 Agent 完成任务后，必须留下可追溯的证据。小灵（Task Verifier）负责验证这些证据。

---

## 验证层级

```
用户请求
    ↓
创业助手分配任务给 Agent
    ↓
Agent 执行并提交"完成"
    ↓
【第一层】小灵验证：文件是否存在？
    ├── ❌ 不存在 → 立即打回
    └── ✅ 存在 → 继续
    ↓
【第二层】创业助手验证：功能是否可用？
    ├── ❌ 不可用 → 打回开发
    └── ✅ 可用 → 继续
    ↓
【第三层】Code Review/QA/UX 验证
    ↓
交付
```

---

## 各 Agent 证据标准

| Agent | 必须产出 | 检查方式 | 最低标准 |
|-------|---------|---------|---------|
| **PM** | `docs/PRD-*.md` | 文件存在 + wc -l | >50 行，含 Given-When-Then |
| **Architect** | `docs/API-*.md` | 文件存在 + grep 表格 | >30 行，含字段对照表 |
| **Frontend** | `src/**/*.{vue,ts}` | find 命令 | ≥2 文件，>10 行/文件 |
| **Backend** | `src/**/*.java` | find 命令 | ≥2 文件，>20 行/文件 |
| **Code Review** | `reviews/*.md` | 文件存在 + grep P0/P1/P2 | >20 行 |
| **QA** | `qa-reports/*.md` + `*.png` | ls 命令 | 报告>30行，≥3 张截图 |
| **UX Tester** | `ux-reports/*.md` + `*.png` | ls 命令 | 报告>30行，≥3 张截图 |

---

## 验证失败处理

### 第一次失败
```markdown
【任务验证失败】
Agent: xxx
问题: 未找到文件 docs/PRD-2026-04-09.md
要求: 请补充产出文件后重新提交
```

### 重复失败（标记）
- 记录到 `memory/agent-reliability.md`
- 连续 3 次验证失败 → 升级给孙雪

---

## 为什么需要这个系统

### 之前的问题
- Agent 说"写好了" → 实际没写文件
- Agent 说"测试通过" → 实际没测试
- Agent 说"审查完成" → 实际没写报告

### 解决方案
**强制留痕 + 自动验证**
- 每个 Agent 必须写文件
- 小灵自动检查文件存在性和内容
- 没有文件 = 任务不算完成

---

## 验证工具

### 命令行验证
```bash
# 检查文件存在
ls ~/.openclaw/agents/pm/workspace/docs/PRD-*.md

# 检查文件大小
wc -l <file>

# 检查关键内容
grep -c "Given-When-Then" <file>
find . -name "*.vue" -size +0 | wc -l
```

### 自动验证脚本
```bash
#!/bin/bash
# agent-verify.sh

AGENT=$1
WORKSPACE="~/.openclaw/agents/$AGENT/workspace"

case $AGENT in
  pm)
    ls $WORKSPACE/docs/PRD-*.md && \
    wc -l $WORKSPACE/docs/PRD-*.md | tail -1
    ;;
  frontend)
    find $WORKSPACE/src -name "*.vue" -size +0 | wc -l
    ;;
  qa)
    ls $WORKSPACE/qa-reports/*.md && \
    ls $WORKSPACE/qa-reports/*.png
    ;;
esac
```

---

## 文件位置汇总

| Agent | 产出目录 | 验证命令 |
|-------|---------|---------|
| pm | `~/.openclaw/agents/pm/workspace/docs/` | `ls docs/PRD-*.md` |
| architect | `~/.openclaw/agents/architect/workspace/docs/` | `ls docs/API-*.md` |
| frontend | `~/.openclaw/agents/frontend/workspace/src/` | `find src -name "*.vue"` |
| backend | `~/.openclaw/agents/backend/workspace/src/` | `find src -name "*.java"` |
| code-review | `~/.openclaw/agents/code-review/workspace/reviews/` | `ls reviews/*.md` |
| qa | `~/.openclaw/agents/qa/workspace/qa-reports/` | `ls qa-reports/` |
| ux-tester | `~/.openclaw/agents/ux-tester/workspace/ux-reports/` | `ls ux-reports/` |

---

## 更新记录

- **2026-04-09**: 建立任务执行验证系统
- **所有 Agent AGENTS.md 已更新**: 加入【必须留痕】章节
- **创业助手流程已更新**: 加入【小灵验证】步骤
