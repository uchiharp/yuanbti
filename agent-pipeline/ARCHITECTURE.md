# Agent Pipeline 脚本补全 — 技术方案

## 1. 设计原则

- **配置驱动**：脚本读 `pipeline-config.yaml` 驱动执行，不硬编码规则。改规则=改配置，不碰脚本代码
- **统一入口**：`pipeline-check.sh` 作为每阶段的主入口，其他脚本由它按阶段调度
- **幂等执行**：同一阶段重复运行结果一致，不产生副作用
- **macOS bash 3.x 兼容**：不使用关联数组、`mapfile`、`readarray` 等 bash 4+ 特性
- **最小外部依赖**：bash + grep + sed + awk + find + wc + python3（macOS自带，用于解析YAML）
- **统一输出格式**：和现有 `pipeline-check.sh` / `security-scan.sh` 保持一致

## 2. 文件清理

### 删除（已过时/已迁移）

| 文件 | 原因 |
|------|------|
| `SPLIT-PLAN.md` | 拆分计划已执行完毕 |
| `SKILL-v4.md` | v4 完整版备份，骨架化后不再需要 |
| `SKILL-v4-full.md` | 同上 |
| `templates/standards/*` | README 已声明"已迁移为独立 skill，保留为历史副本" |
| `templates/souls/*` | 同上 |
| `references/unified-code-review-standards.md` | 已被 `code-review-checklist` skill 完整覆盖 |

### 保留

| 文件 | 原因 |
|------|------|
| `SKILL.md` | 当前在用的主文件 |
| `references/iterative-contract.md` | 合同协议规范，脚本实现的依据 |
| `references/security-scan-templates.md` | Playwright 动态扫描模板，和 sh 脚本互补 |
| `scripts/pipeline-check.sh` | 在用，需增强 |
| `scripts/security-scan.sh` | 在用，不变 |

### 新增

| 文件 | 用途 |
|------|------|
| `PRD.md` | 本 PRD |
| `scripts/review-check.sh` | 评审/签收质量检查 |
| `scripts/contract-check.sh` | 合同轮次+回退次数检查 |
| `scripts/test-report-check.sh` | 测试报告格式检查 |
| `scripts/acceptance-check.sh` | 阶段9验收检查 |
| `scripts/lib.sh` | 共享函数库（输出格式、通用检查、CONTEXT.md 更新） |

## 3. 共享函数库 lib.sh

所有脚本 source 同一个 lib.sh，避免重复代码。

```bash
#!/bin/bash
# lib.sh — 脚本共享函数库
# 用法：source "$(dirname "$0")/lib.sh"

# 计数器
LIB_ERRORS=0
LIB_WARNINGS=0

# 统一输出
lib_error()   { echo "  ❌ $1"; LIB_ERRORS=$((LIB_ERRORS + 1)); }
lib_warning() { echo "  🟡 $1"; LIB_WARNINGS=$((LIB_WARNINGS + 1)); }
lib_ok()      { echo "  ✅ $1"; }

# 检查文件存在且非空，返回行数
lib_check_file() {
  local FILE="$1" MIN_LINES="$2" LABEL="$3"
  if [ ! -f "$FILE" ]; then
    lib_error "$LABEL: 文件不存在 ($FILE)"
    return 1
  fi
  if [ ! -s "$FILE" ]; then
    lib_error "$LABEL: 文件为空 ($FILE)"
    return 1
  fi
  local LINES=$(wc -l < "$FILE" | tr -d ' ')
  if [ "$LINES" -lt "$MIN_LINES" ]; then
    local DIFF=$((MIN_LINES - LINES))
    local PCT=$((DIFF * 100 / MIN_LINES))
    if [ "$PCT" -gt 20 ]; then
      lib_error "$LABEL: ${LINES}行，不足${MIN_LINES}行（差${PCT}%）"
    else
      lib_warning "$LABEL: ${LINES}行，略不足${MIN_LINES}行（差${PCT}%）"
    fi
  else
    lib_ok "$LABEL: ${LINES}行（≥${MIN_LINES}）"
  fi
  return 0
}

# 检查文件中是否包含指定模式，返回匹配数
lib_count_pattern() {
  local FILE="$1" PATTERN="$2"
  grep -cE "$PATTERN" "$FILE" 2>/dev/null || echo 0
}

# 汇总输出
lib_summary() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📊 检查结果"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ❌ 错误: $LIB_ERRORS"
  echo "  🟡 警告: $LIB_WARNINGS"
  if [ "$LIB_ERRORS" -gt 0 ]; then
    echo ""
    echo "  🔴 检查不通过！流程必须暂停。"
    return 1
  elif [ "$LIB_WARNINGS" -gt 0 ]; then
    echo ""
    echo "  🟡 有 $LIB_WARNINGS 个警告，建议修复但可继续。"
    return 0
  else
    echo ""
    echo "  ✅ 全部通过！"
    return 0
  fi
}
```

## 4. review-check.sh

```
输入：项目目录、阶段号
输出：exit 0=通过 / exit 1=不通过
```

### 检查逻辑

```bash
#!/bin/bash
set -eo pipefail
source "$(dirname "$0")/lib.sh"

PROJECT_DIR="$1"
PHASE="$2"

# 阶段号 → 对应评审报告文件名
# 1 → PRD.md 由 PM 评审官审查
# 1.5 → cross-review-pm.md
# 2 → ARCHITECTURE.md 由架构师评审官审查
# 2.5 → cross-review-arch.md
# ...

# 核心检查：
# 1. 评审报告存在
# 2. 包含 ≥3 个检查点（匹配 🔴/🟡/🟢 或编号列表）
# 3. 包含 ≥1 个建议（🟢 或"建议"关键词）
# 4. 包含评分（X/10 或 "评分:" 模式）
# 5. 交叉评审文件：每个角色有独立段落（## 或 ### 分隔）
#    每个段落包含 ≥3 个检查点
```

### 评审报告路径映射

| 阶段 | 评审报告路径 | 说明 |
|------|------------|------|
| 1 | `phase-1-prd/review-report.md` 或 PRD.md 内嵌评审段落 | PM评审官 |
| 1.5 | `phase-1.5-prd-cross-review/cross-review-pm.md` | 交叉评审 |
| 2 | `phase-2-architecture/review-report.md` | 架构评审官 |
| 2.5 | `phase-2.5-arch-cross-review/cross-review-arch.md` | 交叉评审 |
| 4 | `phase-4-ui/review-report.md` | UI评审官 |
| 5 | `phase-5-decomposition/review-report.md` | 创业助手评审官 |
| 6.5 | `phase-6-dev/cross-review-dev.md` | 开发审查 |
| 7 | `phase-7-review/review-report.md` | QA+架构评审官 |
| 8 | `phase-8-test/review-report.md` | QA评审官 |

### 检查点计数规则

匹配以下模式计为一个检查点：
- `🔴` / `🟡` / `🟢` 开头的行
- `✅` / `❌` 开头的行
- 编号列表 `1.` `2.` `3.` 且内容≥10字符
- `- ` 开头且内容≥10字符的列表项

## 5. contract-check.sh

```
输入：项目目录
输出：exit 0=通过 / exit 1=不通过
```

### 检查逻辑

```bash
#!/bin/bash
set -eo pipefail
source "$(dirname "$0")/lib.sh"

PROJECT_DIR="$1"
CONTRACTS_DIR="$PROJECT_DIR/.contracts"

# 1. 检查 _index.json 存在
# 2. 读取 _index.json 中的 contracts 数组
#    - 检查每个 status=in-progress 的合同：轮次是否超限
#      - 🟢低风险 > 1轮 → error
#      - 🟡中风险 > 2轮 → error
#      - 🔴高风险 > 3轮 → error
#    - 超限但 status != escalated → error（应标记未标记）
# 3. 检查每个合同文件是否存在
# 4. 检查合同文件包含必要字段：
#    - 交付物路径 / 评审官 / 签收或打回结果
# 5. 扫描 changes/ 目录统计回退：
#    - 总回退次数 > 5 → error
#    - 同阶段连续回退 > 2 → error
```

### JSON 解析

macOS 无 `jq`，使用 python3（macOS 自带）：

```bash
parse_index_json() {
  python3 -c "
import json, sys
with open('$CONTRACTS_DIR/_index.json') as f:
    data = json.load(f)
for c in data.get('contracts', []):
    print(f\"{c.get('id','?')}|{c.get('status','?')}|{c.get('rounds',0)}|{c.get('risk','unknown')}\")
" 2>/dev/null
}
```

## 6. test-report-check.sh

```
输入：项目目录
输出：exit 0=通过 / exit 1=不通过
```

### 检查逻辑

```bash
#!/bin/bash
set -eo pipefail
source "$(dirname "$0")/lib.sh"

PROJECT_DIR="$1"

# 定位 test-report.md（可能在 phase-8-test/ 或项目根）
TEST_REPORT=$(find "$PROJECT_DIR" -name "test-report.md" -type f | head -1)

# 1. 文件存在且行数 ≥ 50
# 2. 截图数量 ≥ 3
#    - 查找 qa-reports/*.png, 8/screenshots/*.png, screenshots/*.png
# 3. 逐项结果 ≥ 3
#    - 匹配 ^[✅🔴🟡] 或 "✅" / "🔴" 开头的行
# 4. 包含通过率（"通过率" 或 "X/Y" 模式）
# 5. 包含问题清单（"P0" / "🔴 P0" 模式）
# 6. 包含前置条件/执行步骤/预期结果/实际结果格式
#    - 匹配 "前置条件" / "执行步骤" / "预期结果" / "实际结果" 关键词
```

## 7. acceptance-check.sh

```
输入：项目目录
输出：exit 0=通过 / exit 1=不通过
```

### 检查逻辑

```bash
#!/bin/bash
set -eo pipefail
source "$(dirname "$0")/lib.sh"

PROJECT_DIR="$1"

# 定位 ACCEPTANCE-REPORT.md
ACCEPTANCE=$(find "$PROJECT_DIR" -name "ACCEPTANCE-REPORT.md" -type f | head -1)

# 1. 文件存在
# 2. 包含7项验收 checklist（匹配 "- [ ]" 或 "- [x]" 模式 ≥ 7个）
# 3. 所有 checklist 项标记为 ✅ 或 [x]
# 4. 自动验证可脚本化的项：
#    a. 调用 contract-check.sh 确认无 escalated 合同
#    b. 调用 security-scan.sh 确认 0 严重问题
#    c. 读取 test-report.md 确认无 P0 遗留
```

## 8. 项目知识库：CONTEXT.md + MemPalace

### 8.1 CONTEXT.md 文件格式

```markdown
# {项目名} 项目上下文

## 阶段0：项目概览 | 更新于 YYYY-MM-DD
- 项目规模：🟡中型
- 参与角色：PM、架构师、开发×2、QA
- 关键约束：必须在微信小程序内运行

## 阶段1：需求 | 更新于 YYYY-MM-DD
- 目标用户：中小企业HR
- P0功能：简历解析、职位发布、候选人匹配
- 砍掉的功能：薪资测算（P1）、背调集成（P2）
- 验收标准：简历解析准确率≥95%

## 阶段2：架构 | 更新于 YYYY-MM-DD
- 技术栈：Vue3 + Spring Boot + PostgreSQL
- 核心决策：单体架构（中型项目，暂不分微服务）
- API约定：RESTful + JWT认证

...后续阶段...

## 回退/变更记录
| 时间 | 回退/变更 | 原因 | 影响的段落 | 已更新 |
|------|----------|------|-----------|-------|
```

**段落覆盖规则：**
- 每个阶段的段落用 `## 阶段N：{标题}` 唯一定位
- 执行者交付时，用 sed 替换该段落内容（从 `## 阶段N` 到下一个 `##` 之间）
- 新项目首次创建时，由协调者在阶段0写入骨架（所有阶段段落预留标题行）

### 8.2 段落更新脚本实现

```bash
# lib.sh 新增函数

# 更新 CONTEXT.md 中指定阶段的段落
# 用法：lib_update_context <项目目录> <阶段号> <阶段标题> <内容文件>
lib_update_context() {
  local PROJECT_DIR="$1" PHASE="$2" TITLE="$3" CONTENT_FILE="$4"
  local CTX="$PROJECT_DIR/CONTEXT.md"

  # 如果文件不存在，创建骨架
  if [ ! -f "$CTX" ]; then
    cat > "$CTX" << 'SKEL'
# 项目上下文

## 阶段0：项目概览 | 更新于

## 阶段1：需求 | 更新于

## 阶段2：架构 | 更新于

## 阶段2.8：技术Spike | 更新于

## 阶段3：UX设计 | 更新于

## 阶段4：UI设计 | 更新于

## 阶段5：任务分解 | 更新于

## 阶段6：开发 | 更新于

## 阶段8：测试 | 更新于

## 回退/变更记录
| 时间 | 回退/变更 | 原因 | 影响的段落 | 已更新 |
|------|----------|------|-----------|-------|
SKEL
  fi

  # 用 sed 替换指定阶段段落
  # 匹配 "## 阶段N" 到下一个 "##" 之间的内容
  local DATE=$(date '+%Y-%m-%d')
  local HEADER="## 阶段${PHASE}：${TITLE} | 更新于 ${DATE}"

  # macOS sed: 用换行符分割替换内容
  local NEW_CONTENT="${HEADER}"$'\n'"$(cat "$CONTENT_FILE")"

  # 使用 awk 替换（比 sed 更可靠处理多段落）
  awk -v phase="阶段${PHASE}" -v content="$NEW_CONTENT" '
    /^## 阶段[0-9]/ && $0 ~ phase { found=1; print content; next }
    /^## / && found { found=0 }
    !found { print }
  ' "$CTX" > "$CTX.tmp" && mv "$CTX.tmp" "$CTX"
}
```

### 8.3 pipeline-check.sh 知识库检查

```bash
check_knowledge() {
  echo ""
  echo "📚 检查项目知识库"

  local CTX="$PROJECT_DIR/CONTEXT.md"

  # 强制检查1：CONTEXT.md 存在
  if [ ! -f "$CTX" ]; then
    lib_error "CONTEXT.md 不存在（协调者应在阶段0创建）"
    return
  fi
  lib_ok "CONTEXT.md 存在"

  # 强制检查2：包含当前阶段段落
  if ! grep -q "## 阶段${PHASE}" "$CTX"; then
    lib_error "CONTEXT.md 未包含阶段${PHASE}段落"
  else
    lib_ok "CONTEXT.md 包含阶段${PHASE}段落"
  fi

  # 强制检查3：总行数 ≤200
  local LINES=$(wc -l < "$CTX" | tr -d ' ')
  if [ "$LINES" -gt 200 ]; then
    lib_error "CONTEXT.md ${LINES}行，超过200行限制"
  else
    lib_ok "CONTEXT.md ${LINES}行（≤200）"
  fi

  # 回退一致性检查：changes/ 目录有新记录时，对应段落必须已更新
  local CHANGES_DIR="$PROJECT_DIR/changes"
  if [ -d "$CHANGES_DIR" ]; then
    local CHANGES_DIR="$PROJECT_DIR/changes"
    local LATEST_CHANGE=$(find "$CHANGES_DIR" -name "*.md" -type f -newer "$CTX" 2>/dev/null | head -1)
    if [ -n "$LATEST_CHANGE" ]; then
      # 有比 CONTEXT.md 更新的 change 记录，检查是否已更新对应段落
      local AFFECTED_PHASE=$(grep -oE '阶段[0-9.]+', "$LATEST_CHANGE" 2>/dev/null | head -1 | tr -d ',')
      if [ -n "$AFFECTED_PHASE" ]; then
        # 检查该段落更新时间是否晚于 change 记录
        local PHASE_HEADER=$(grep -n "## ${AFFECTED_PHASE}" "$CTX" | head -1 | cut -d: -f1)
        if [ -n "$PHASE_HEADER" ]; then
          # 简化检查：段落中的日期是否晚于 change 记录日期
          local PHASE_DATE=$(sed -n "${PHASE_HEADER}p" "$CTX" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
          local CHANGE_DATE=$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$LATEST_CHANGE" | head -1)
          if [ "$PHASE_DATE" '<' "$CHANGE_DATE" ] 2>/dev/null; then
            lib_error "回退后知识库未更新：${AFFECTED_PHASE}段落日期(${PHASE_DATE})早于回退记录(${CHANGE_DATE})"
          fi
        fi
      fi
    fi
  fi

  # 可选检查：MemPalace（依赖 MCP，失败只 warning）
  # 此项检查由协调者通过 MCP 工具在 agent 层面执行
  # 脚本层面无法直接调用 MCP，因此只在健康度看板中标记
  lib_warning "MemPalace 知识库存入需协调者通过 MCP 验证（脚本无法自动检查）"
}
```

### 8.4 MemPalace 版本机制

存入时带 YAML 元数据：

```markdown
---
version: 2
updated_at: 2026-05-10
replaces: version-1
trigger: 阶段6回退→阶段2，JWT改OAuth
---

# 架构决策（v2）

认证方案：OAuth2.0 + PKCE
...
```

检索时协调者过滤最新版本：
```
mempalace_search(wing="finder-app", room="arch-decisions")
→ 返回所有版本，协调者取 version 最大且 replaces 链完整的记录
```

**废弃规则：**

| 事件 | 触发者 | 知识库操作 |
|------|--------|-----------|
| 回退到阶段N | 协调者 | CONTEXT.md 更新阶段N段落 + MemPalace 存入新版本 |
| 需求变更 | 变更发起者 | CONTEXT.md 更新受影响段落 + MemPalace 存入新版本 |
| 迭代修复 | 修复者 | CONTEXT.md 更新阶段6段落 + MemPalace 更新 dev-notes room |

### 8.5 各阶段知识库存入规则

| 阶段 | CONTEXT.md 段落（≤30行） | MemPalace room | 存入者 |
|------|--------------------------|----------------|--------|
| 0 | 项目规模、角色、约束 | `project-overview` | 协调者 |
| 1 | 目标用户、MVP功能、验收标准 | `prd-decisions` | PM |
| 2 | 技术栈、架构决策、API约定 | `arch-decisions` | 架构师 |
| 2.8 | Spike结论 | `spike-reports` | 架构师/开发 |
| 3 | 用户流程要点、交互规范摘要 | 无（UX完整文档在文件里） | UX测试 |
| 4 | 设计系统要点、组件规范摘要 | 无 | UI设计师 |
| 5 | 任务批次、分工 | `task-breakdown` | 创业助手 |
| 6 | 各开发者负责内容、代码入口 | `dev-notes` | 各开发 |
| 8 | 覆盖率、已知问题 | `test-results` | QA |
| 9 | 交付状态、遗留问题、教训 | `project-lessons` | 协调者 |

**阶段3/4不存 MemPalace**：UX/UI 设计文档本身就在项目目录文件里，不需要重复存。CONTEXT.md 只写摘要要点。

---

## 9. pipeline-check.sh 增强

在现有脚本基础上新增：

### 9.1 补全缺失阶段的行数检查

```bash
# 新增到 get_phase_file()
3) echo "UX-DESIGN.md:80" ;;
3.5) echo "cross-review-ux-to-ui.md:20" ;;
4) echo "UI-DESIGN.md:80" ;;
4.5) echo "cross-review-ui-to-ux.md:20" ;;
5.5) echo "confirm-tasks.md:20" ;;
6.5) echo "cross-review-dev.md:30" ;;
7) echo "review-report.md:30" ;;
```

### 9.2 沟通记录内容检查

```bash
check_communications() {
  # 现有：只检查目录是否存在
  # 新增：检查 comm-*.md 文件内容
  local COMM_DIR="$PROJECT_DIR/communications"
  # 遍历 comm-*.md，检查是否包含：
  # - "发送方" 或 "from:" 模式
  # - "接收方" 或 "to:" 模式
  # - 类型标记（签收/打回/评审/回退）
}
```

### 9.3 健康度看板更新检查

```bash
check_health_dashboard() {
  local HD="$PROJECT_DIR/health-dashboard.md"
  if [ ! -f "$HD" ]; then
    lib_error "health-dashboard.md 不存在"
    return
  fi
  # 检查最后修改时间是否在最近 N 分钟内
  # macOS: stat -f %m 获取修改时间戳
  local MTIME=$(stat -f %m "$HD" 2>/dev/null || echo 0)
  local NOW=$(date +%s)
  local AGE=$(( NOW - MTIME ))
  # 假设阶段间隔不超过 2 小时
  if [ "$AGE" -gt 7200 ]; then
    lib_warning "health-dashboard.md 超过2小时未更新"
  fi
}
```

### 9.4 按阶段调用子脚本

```bash
# 在主逻辑的 case 语句中新增
6.5|7)
  check_file "review-report.md" "$MIN_L"
  "$(dirname "$0")/review-check.sh" "$PROJECT_DIR" "$PHASE"
  ;;
8)
  check_file "test-report.md" "$MIN_L"
  "$(dirname "$0")/test-report-check.sh" "$PROJECT_DIR"
  ;;
9)
  check_file "ACCEPTANCE-REPORT.md" "$MIN_L"
  "$(dirname "$0")/acceptance-check.sh" "$PROJECT_DIR"
  ;;
```

### 9.5 每阶段调用知识库检查

```bash
# 在每个阶段的检查末尾，加入知识库检查
check_knowledge

# 阶段0额外：检查 CONTEXT.md 骨架是否创建
# 阶段9额外：检查 MemPalace project-lessons 是否存入
```

## 10. 实现顺序

| 步骤 | 内容 | 依赖 |
|------|------|------|
| 1 | 创建 `scripts/lib.sh` 共享函数库（含 CONTEXT.md 更新函数） | 无 |
| 2 | 重构 `scripts/pipeline-check.sh`，source lib.sh + 补全行数检查 + 知识库检查 | 步骤1 |
| 3 | 创建 `scripts/review-check.sh` | 步骤1 |
| 4 | 创建 `scripts/contract-check.sh` | 步骤1 |
| 5 | 创建 `scripts/test-report-check.sh` | 步骤1 |
| 6 | 创建 `scripts/acceptance-check.sh` | 步骤1+4+security-scan.sh |
| 7 | 在 pipeline-check.sh 中集成子脚本调用 + 知识库检查 | 步骤2-6 |
| 8 | 删除过时文件 | 无 |
| 9 | 更新 SKILL.md 引用 + 各阶段交付规则增加 CONTEXT.md 更新义务 | 步骤7 |

## 11. 测试方案

每个脚本创建对应的测试目录结构：

```bash
# tests/
# ├── test-lib.sh              — lib.sh 单元测试（含 lib_update_context）
# ├── test-review-check.sh     — 构造合法/非法评审报告
# ├── test-contract-check.sh   — 构造合法/超限合同
# ├── test-test-report.sh      — 构造合格/不合格测试报告
# ├── test-acceptance.sh       — 构造通过/未通过验收
# ├── test-knowledge.sh        — 构造合法/过时/缺失 CONTEXT.md
# └── fixtures/                — 测试用例文件
#     ├── valid-review.md
#     ├── empty-review.md
#     ├── valid-contract-index.json
#     ├── valid-context.md     — 包含所有阶段段落的合法 CONTEXT.md
#     ├── stale-context.md     — 回退后未更新的过时 CONTEXT.md
#     └── ...
```

运行：`bash tests/test-all.sh`，全部 exit 0 即通过。
