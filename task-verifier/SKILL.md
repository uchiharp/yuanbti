---
name: task-verifier
description: 任务执行验证系统。检查 Agent 任务是否真实执行、是否有落地文档、是否留痕。
---

## 元数据
- **type:** workflow
- **triggers:** agent-need
- **requires:** exec, read
- **auto-load:** false
- **priority:** medium

---

# Task Verifier - 任务执行验证

## 核心原则
**没有证据 = 没有执行**

## 各 Agent 证据要求

### PM Agent
| 证据类型 | 检查项 | 验证方式 |
|---------|--------|---------|
| PRD 文档 | 文件存在 | `ls <workspace>/docs/PRD-*.md` |
| 验收标准 | 内容具体 | grep "Given-When-Then" |
| 可追溯 | git 提交记录 | `git log --oneline -5` |

### Architect Agent
| 证据类型 | 检查项 | 验证方式 |
|---------|--------|---------|
| API 设计 | 文件存在 | `ls <workspace>/docs/API-*.md` |
| 字段对照表 | 表格完整 | grep "\|" 检查表格行数 |
| 类型定义 | TypeScript interface | grep "interface" |

### Frontend Agent
| 证据类型 | 检查项 | 验证方式 |
|---------|--------|---------|
| 代码文件 | 文件存在且非空 | `find . -name "*.vue" -size +0` |
| 编译产物 | build 输出 | `ls dist/` |
| 执行记录 | exec 调用记录 | 检查 sessions_history |

### Backend Agent
| 证据类型 | 检查项 | 验证方式 |
|---------|--------|---------|
| 代码文件 | Java 文件存在 | `find . -name "*.java" -size +0` |
| 编译通过 | mvn compile 输出 | 检查 exec 记录 |
| API 可调用 | curl 测试记录 | 检查 exec 记录 |

### Code Review Agent
| 证据类型 | 检查项 | 验证方式 |
|---------|--------|---------|
| 审查报告 | 文件存在 | `ls <workspace>/reviews/` |
| 问题清单 | 具体项列表 | grep -c "P0\|P1\|P2" |
| 对比记录 | 前后代码对比 | `git diff` 输出 |

### QA Agent
| 证据类型 | 检查项 | 验证方式 |
|---------|--------|---------|
| 测试报告 | 文件存在 | `ls <workspace>/qa-reports/` |
| 截图证据 | 图片文件 | `find . -name "*.png"` |
| API 调用记录 | curl 输出 | 检查 exec 记录 |

### UX Tester Agent
| 证据类型 | 检查项 | 验证方式 |
|---------|--------|---------|
| 体验报告 | 文件存在 | `ls <workspace>/ux-reports/` |
| 截图证据 | 图片文件 | `find . -name "ux-*.png"` |
| 操作记录 | 点击/输入流程 | 报告中的操作步骤 |

## 验证流程

```
Agent 提交"任务完成"
    ↓
Task Verifier 检查：
    1. 要求的输出文件是否存在？
    2. 文件内容是否符合规范？
    3. 是否有 exec 执行记录？
    4. 是否有截图/日志等证据？
    ↓
验证结果：
    ✅ 通过 → 继续下一步
    ❌ 失败 → 打回 Agent，要求补充证据
```

## 证据检查脚本示例

### 检查文件存在且非空
```bash
#!/bin/bash
file=$1
if [ -f "$file" ] && [ -s "$file" ]; then
    echo "✅ $file exists and not empty"
    wc -l "$file"
else
    echo "❌ $file missing or empty"
    exit 1
fi
```

### 检查 exec 执行记录
```bash
# 通过 sessions_history 检查是否有 exec 调用
# 或通过检查命令输出文件
```

### 检查代码规范
```bash
# 检查是否包含关键内容
grep -E "(function|class|const|let)" "$file"
```

## 报告格式

### 验证通过
```markdown
## 任务验证报告 ✅

Agent: <name>
Task: <description>
Status: PASSED

### 证据清单
- [x] 文件1: <path> (XX lines)
- [x] 文件2: <path> (XX lines)
- [x] 执行记录: <command>
- [x] 截图: <path>

结论: 任务真实执行，证据完整
```

### 验证失败
```markdown
## 任务验证报告 ❌

Agent: <name>
Task: <description>
Status: FAILED

### 缺失证据
- [ ] 文件缺失: <expected path>
- [ ] 内容不足: <file> (only X lines, expected >Y)
- [ ] 无执行记录: <command> not found in history

要求: 请补充以上证据后重新提交
```
