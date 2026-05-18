#!/bin/bash
# pipeline-check.sh — 开发流水线防偷懒检查脚本
# 用法：./pipeline-check.sh <项目目录> <阶段编号>
# 协调者无法绕过此脚本，检查不通过 = 流程暂停
# 兼容 macOS bash 3.x

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PROJECT_DIR="$1"
PHASE="$2"

if [ -z "$PROJECT_DIR" ] || [ -z "$PHASE" ]; then
  echo "用法: $0 <项目目录> <阶段编号> [--size small|medium|large]"
  echo "示例: $0 .contracts/my-app 1 --size small"
  exit 1
fi

# 解析 --size 参数（支持 --size small / --size=small 两种格式）
SIZE=""
if [ "$3" = "--size" ] && [ -n "$4" ]; then
  SIZE="$4"
elif [ "${3#--size=}" != "$3" ]; then
  SIZE="${3#--size=}"
fi

ERRORS=0
WARNINGS=0

# ─── 加载共享配置 ───
CONF_FILE="$PIPELINE_ROOT/config/pipeline-stages.conf"
load_conf() {
  local key="$1"
  local default="${2:-}"
  if [ -f "$CONF_FILE" ]; then
    grep "^${key}=" "$CONF_FILE" 2>/dev/null | head -1 | cut -d= -f2- || echo "$default"
  else
    echo "$default"
  fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 流水线检查 | 阶段 $PHASE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 获取阶段对应的文件名和最小行数（从配置文件读取）
get_phase_file() {
  load_conf "PHASE_${1}_FILE" ""
}

# 统计有效行数（排除空行）
count_lines() {
  local file="$1"
  grep -cve '^\s*$' "$file" 2>/dev/null || echo 0
}

# 从配置读取角色列表（逗号分隔 → 数组）
load_roles() {
  local key="$1"
  local csv=$(load_conf "$key" "")
  if [ -n "$csv" ]; then
    echo "$csv" | tr ',' '\n'
  fi
}

# 规模系数（--size 参数影响行数门槛）
get_size_multiplier() {
  case "$SIZE" in
    small)  echo "50" ;;   # 小项目门槛减半
    medium) echo "75" ;;   # 中项目门槛 75%
    large)  echo "100" ;;  # 大项目原样
    *)      echo "100" ;;
  esac
}

# 检查单个文件
check_file() {
  local FILE="$1"
  local MIN_LINES="$2"
  local FULL_PATH="$PROJECT_DIR/pipeline/$PHASE/$FILE"

  echo ""
  echo "📄 检查文件: $FILE"

  if [ ! -f "$FULL_PATH" ]; then
    echo "  ❌ 文件不存在: $FULL_PATH"
    ERRORS=$((ERRORS + 1))
    return
  fi

  if [ ! -s "$FULL_PATH" ]; then
    echo "  ❌ 文件为空: $FULL_PATH"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 应用规模系数
  local MULTIPLIER=$(get_size_multiplier)
  MIN_LINES=$((MIN_LINES * MULTIPLIER / 100))
  [ "$MIN_LINES" -lt 1 ] && MIN_LINES=1

  LINES=$(count_lines "$FULL_PATH")
  echo "  ✅ 文件存在"
  echo "  📏 有效行数: $LINES (最低要求: $MIN_LINES)"

  if [ "$LINES" -lt "$MIN_LINES" ]; then
    DIFF=$((MIN_LINES - LINES))
    if [ "$MIN_LINES" -gt 0 ]; then
      PERCENT=$((DIFF * 100 / MIN_LINES))
    else
      PERCENT=100
    fi
    if [ "$PERCENT" -gt 20 ]; then
      echo "  ❌ 行数严重不足（差${PERCENT}%，缺${DIFF}行）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  🟡 行数轻微不足（差${PERCENT}%，缺${DIFF}行）"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  ✅ 行数达标"
  fi
}

# 阶段6-8：特殊检查
check_code() {
  echo ""
  echo "📁 检查代码产出"

  local CODE_DIR="$PROJECT_DIR"
  if [ ! -d "$CODE_DIR" ]; then
    echo "  ❌ 项目目录不存在: $CODE_DIR"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local CODE_FILES=$(find "$CODE_DIR" -not -path "*/pipeline/*" -not -path "*/node_modules/*" -not -path "*/.git/*" \( -name "*.ts" -o -name "*.java" -o -name "*.vue" -o -name "*.js" -o -name "*.py" -o -name "*.sql" -o -name "*.xml" \) -type f 2>/dev/null | wc -l | tr -d ' ')

  echo "  代码文件数: $CODE_FILES"

  if [ "$CODE_FILES" -eq 0 ]; then
    echo "  ❌ 没有找到任何代码文件"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 找到代码文件"
  fi

  # 检查进度文件（逐任务调度产出）
  local PROGRESS_FILE="$PROJECT_DIR/pipeline/6/progress.json"
  if [ -f "$PROGRESS_FILE" ]; then
    local COMPLETED=$(python3 -c "import json; d=json.load(open('$PROGRESS_FILE')); print(sum(1 for v in d.values() if isinstance(v,dict) and v.get('status')=='completed' and v.get('agent')!='skipped'))" 2>/dev/null || echo 0)
    local FAILED=$(python3 -c "import json; d=json.load(open('$PROGRESS_FILE')); print(sum(1 for v in d.values() if isinstance(v,dict) and v.get('status')=='failed'))" 2>/dev/null || echo 0)
    echo "  ✅ progress.json 存在（完成: $COMPLETED, 失败: $FAILED）"
    if [ "$COMPLETED" -eq 0 ]; then
      echo "  ❌ 没有已完成的任务"
      ERRORS=$((ERRORS + 1))
    fi
    if [ "$FAILED" -gt 0 ]; then
      echo "  🟡 有 $FAILED 个任务失败"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  🟡 progress.json 不存在（可能非逐任务调度模式）"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 检查任务产出摘要（逐任务调度产出）
  local TASK_REPORTS_DIR="$PROJECT_DIR/pipeline/6/task-reports"
  if [ -d "$TASK_REPORTS_DIR" ]; then
    local REPORT_COUNT=$(find "$TASK_REPORTS_DIR" -name "T-*.md" -type f | wc -l | tr -d ' ')
    echo "  📋 task-reports/ 产出摘要数: $REPORT_COUNT"
    if [ "$REPORT_COUNT" -eq 0 ]; then
      echo "  ❌ task-reports/ 目录存在但没有产出摘要（每个完成的任务应有 {task_id}.md）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 找到任务产出摘要"
    fi
  else
    echo "  ❌ task-reports/ 目录不存在（dispatch-task.sh 应创建此目录）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查开发写的单元测试（逐任务）
  local UNIT_TESTS_DIR="$PROJECT_DIR/tests/unit"
  if [ -d "$UNIT_TESTS_DIR" ]; then
    local UNIT_TEST_DIRS=$(find "$UNIT_TESTS_DIR" -mindepth 1 -maxdepth 1 -type d -name "T-*" | wc -l | tr -d ' ')
    echo "  📋 tests/unit/ 任务测试目录数: $UNIT_TEST_DIRS"
    if [ "$UNIT_TEST_DIRS" -eq 0 ]; then
      echo "  ❌ tests/unit/ 目录存在但没有 T-*/ 子目录（每个任务应有独立测试目录）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 找到任务级单元测试目录"
    fi
  else
    echo "  ❌ tests/unit/ 目录不存在（开发应在阶段6产出单元测试）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查QA写的E2E测试脚本（阶段6 QA同步产出）
  local E2E_DIR="$PROJECT_DIR/tests/e2e"
  if [ -d "$E2E_DIR" ]; then
    local E2E_FILES=$(find "$E2E_DIR" -name "*.spec.*" -o -name "*.test.*" | wc -l | tr -d ' ')
    echo "  E2E测试文件数: $E2E_FILES"
    if [ "$E2E_FILES" -eq 0 ]; then
      echo "  ❌ tests/e2e/ 目录存在但没有测试文件"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 找到E2E测试文件"
    fi
  else
    echo "  ❌ tests/e2e/ 目录不存在（QA应在阶段6同步产出Playwright测试脚本）"
    ERRORS=$((ERRORS + 1))
  fi
}

# 通用复审检查（各阶段共用）
check_re_review() {
  local FILE="$1"
  local DOC_NAME="$2"
  shift 2
  local ROLES=("$@")

  echo ""
  echo "🔄 检查复审 ($DOC_NAME)"

  if [ ! -f "$FILE" ] || [ ! -s "$FILE" ]; then
    echo "  ❌ $FILE 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$FILE" | tr -d ' ')
  echo "  ✅ 文件存在 (${LINES}行)"
  if [ "$LINES" -lt 10 ]; then
    echo "  ❌ 行数不足（${LINES}行，最低10行）"
    ERRORS=$((ERRORS + 1))
  fi

  for role in "${ROLES[@]}"; do
    if grep -qE "^##.*${role}" "$FILE" 2>/dev/null; then
      echo "  ✅ ${role} 复审段落存在"
    else
      echo "  ❌ 缺少 ${role} 复审段落"
      ERRORS=$((ERRORS + 1))
    fi
  done

  if grep -qE '通过|确认|已修复|LGTM' "$FILE" 2>/dev/null; then
    echo "  ✅ 包含确认通过"
  else
    echo "  ❌ 缺少确认通过"
    ERRORS=$((ERRORS + 1))
  fi
}

# PRD 交叉评审检查（阶段 1.5）
check_cross_review_pm() {
  echo ""
  echo "📊 检查 PRD 交叉评审"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/1.5/cross-review-pm.md"

  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ cross-review-pm.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$REVIEW_FILE" | tr -d ' ')
  echo "  ✅ 文件存在 (${LINES}行)"
  if [ "$LINES" -lt 50 ]; then
    echo "  ❌ 行数不足（${LINES}行，最低50行）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查角色段落（从配置读取）
  while IFS= read -r role; do
    [ -z "$role" ] && continue
    if grep -qE "^##.*${role}" "$REVIEW_FILE" 2>/dev/null; then
      echo "  ✅ ${role} 评审段落存在"
      local SECTION=$(awk "/^##.*${role}/,/^##/" "$REVIEW_FILE" 2>/dev/null)
      local CHECKS=$(echo "$SECTION" | grep -cE '^\s*[0-9]+\.|^-\s*\*\*|检查点|问题|建议' 2>/dev/null || echo 0)
      if [ "$CHECKS" -lt 3 ]; then
        echo "  ❌ ${role} 检查点少于3个（发现 ${CHECKS} 个）"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ ${role} 检查点达标 (${CHECKS}个)"
      fi
    else
      echo "  ❌ 缺少 ${role} 评审段落"
      ERRORS=$((ERRORS + 1))
    fi
  done <<< "$(load_roles "REVIEW_1.5_ROLES")"
}

# 架构交叉评审检查（阶段 2.5）
check_cross_review_arch() {
  echo ""
  echo "📊 检查架构交叉评审"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/2.5/cross-review-arch.md"

  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ cross-review-arch.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$REVIEW_FILE" | tr -d ' ')
  echo "  ✅ 文件存在 (${LINES}行)"
  if [ "$LINES" -lt 40 ]; then
    echo "  ❌ 行数不足（${LINES}行，最低40行）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查角色段落（从配置读取）
  while IFS= read -r role; do
    [ -z "$role" ] && continue
    if grep -qE "^##.*${role}" "$REVIEW_FILE" 2>/dev/null; then
      echo "  ✅ ${role} 评审段落存在"
      local SECTION=$(awk "/^##.*${role}/,/^##/" "$REVIEW_FILE" 2>/dev/null)
      local CHECKS=$(echo "$SECTION" | grep -cE '^\s*[0-9]+\.|^-\s*\*\*|检查点|问题|建议' 2>/dev/null || echo 0)
      if [ "$CHECKS" -lt 3 ]; then
        echo "  ❌ ${role} 检查点少于3个（发现 ${CHECKS} 个）"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ ${role} 检查点达标 (${CHECKS}个)"
      fi
    else
      echo "  ❌ 缺少 ${role} 评审段落"
      ERRORS=$((ERRORS + 1))
    fi
  done <<< "$(load_roles "REVIEW_2.5_ROLES")"
}

check_review() {
  echo ""
  echo "📊 检查审查报告"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/7/review-report.md"
  local SCREENSHOTS_DIR="$PROJECT_DIR/pipeline/7/screenshots"
  local TASK_REVIEWS_DIR="$PROJECT_DIR/pipeline/7/task-reviews"

  # 检查逐任务审查产出
  if [ -d "$TASK_REVIEWS_DIR" ]; then
    local REVIEW_COUNT=$(find "$TASK_REVIEWS_DIR" -name "T-*.md" -type f | wc -l | tr -d ' ')
    echo "  📋 task-reviews/ 逐任务审查数: $REVIEW_COUNT"
    if [ "$REVIEW_COUNT" -eq 0 ]; then
      echo "  ❌ task-reviews/ 目录存在但没有审查文件（run-review.sh 应产出 {task_id}.md）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 找到逐任务审查文件"
    fi
  else
    echo "  ❌ task-reviews/ 目录不存在（run-review.sh 应创建此目录）"
    ERRORS=$((ERRORS + 1))
  fi

  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ 审查报告不存在或为空"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 审查报告存在"

    # 检查四个角色的段落
    local ROLES=("架构师" "QA" "PM" "开发2")
    for role in "${ROLES[@]}"; do
      if grep -qE "^##.*${role}" "$REVIEW_FILE" 2>/dev/null; then
        echo "  ✅ ${role} 审查段落存在"
      else
        echo "  ❌ 缺少 ${role} 审查段落"
        ERRORS=$((ERRORS + 1))
      fi
    done

    local CHECK_POINTS=$(grep -cE '^\s*[0-9]+\.|^-\s*\*\*#|检查了|检查点' "$REVIEW_FILE" 2>/dev/null || echo 0)
    echo "  🔍 发现检查点: $CHECK_POINTS"
    if [ "$CHECK_POINTS" -lt 3 ]; then
      echo "  ❌ 检查点少于3个，疑似空签收"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 检查点数量达标"
    fi
  fi

  if [ -d "$SCREENSHOTS_DIR" ]; then
    local SCREENSHOT_COUNT=$(find "$SCREENSHOTS_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | wc -l | tr -d ' ')
    echo "  📸 截图数量: $SCREENSHOT_COUNT"
    if [ "$SCREENSHOT_COUNT" -eq 0 ]; then
      echo "  🟡 没有截图，Playwright可能未实际执行"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  🟡 screenshots/ 目录不存在"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# PM 测试用例评审检查（阶段 8）
check_test_case_review() {
  echo ""
  echo "📋 检查 PM 测试用例评审"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/8/test-case-review.md"

  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ test-case-review.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$REVIEW_FILE" | tr -d ' ')
  echo "  ✅ 文件存在 (${LINES}行)"
  if [ "$LINES" -lt 10 ]; then
    echo "  ❌ 行数不足（${LINES}行，最低10行）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查是否引用了 PRD
  if grep -qi 'PRD' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 引用了 PRD"
  else
    echo "  ❌ 未引用 PRD（PM 评审必须对照 PRD）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查是否有覆盖度评估
  if grep -qE '覆盖|遗漏|缺失|未测试' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 包含覆盖度评估"
  else
    echo "  🟡 缺少覆盖度评估"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# UX 审查检查（阶段 3）
check_ux_review() {
  echo ""
  echo "📋 检查 UX 审查"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/3/ux-review.md"

  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ ux-review.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$REVIEW_FILE" | tr -d ' ')
  echo "  ✅ 文件存在 (${LINES}行)"
  if [ "$LINES" -lt 10 ]; then
    echo "  ❌ 行数不足（${LINES}行，最低10行）"
    ERRORS=$((ERRORS + 1))
  fi

  if grep -qi 'PRD' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 引用了 PRD"
  else
    echo "  ❌ 未引用 PRD"
    ERRORS=$((ERRORS + 1))
  fi

  if grep -qE '通过|不通过' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 包含明确判定"
  else
    echo "  ❌ 缺少明确判定"
    ERRORS=$((ERRORS + 1))
  fi
}

# UI 审查检查（阶段 4）
check_ui_review() {
  echo ""
  echo "📋 检查 UI 审查"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/4/ui-review.md"

  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ ui-review.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$REVIEW_FILE" | tr -d ' ')
  echo "  ✅ 文件存在 (${LINES}行)"
  if [ "$LINES" -lt 10 ]; then
    echo "  ❌ 行数不足（${LINES}行，最低10行）"
    ERRORS=$((ERRORS + 1))
  fi

  local ROLES=("PM" "开发")
  for role in "${ROLES[@]}"; do
    if grep -qE "^##.*${role}" "$REVIEW_FILE" 2>/dev/null; then
      echo "  ✅ ${role} 审查段落存在"
    else
      echo "  ❌ 缺少 ${role} 审查段落"
      ERRORS=$((ERRORS + 1))
    fi
  done

  if grep -qE '通过|不通过' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 包含明确判定"
  else
    echo "  ❌ 缺少明确判定"
    ERRORS=$((ERRORS + 1))
  fi
}

check_test() {
  echo ""
  echo "🧪 检查测试报告"

  local TEST_FILE="$PROJECT_DIR/pipeline/8/test-report.md"

  if [ ! -f "$TEST_FILE" ] || [ ! -s "$TEST_FILE" ]; then
    echo "  ❌ 测试报告不存在或为空"
    ERRORS=$((ERRORS + 1))
  else
    local LINES=$(wc -l < "$TEST_FILE" | tr -d ' ')
    echo "  ✅ 测试报告存在 (${LINES}行)"
    if [ "$LINES" -lt 20 ]; then
      echo "  ❌ 测试报告过短"
      ERRORS=$((ERRORS + 1))
    fi

    # 检查是否包含 REQ 覆盖情况
    local REQ_MENTIONS=$(grep -cE 'REQ-[0-9]+' "$TEST_FILE" 2>/dev/null || echo 0)
    if [ "$REQ_MENTIONS" -gt 0 ]; then
      echo "  ✅ 测试报告提及了 $REQ_MENTIONS 处 REQ-xxx"
    else
      echo "  ❌ 测试报告未提及任何 REQ-xxx（必须有 REQ 追溯矩阵）"
      ERRORS=$((ERRORS + 1))
    fi

    # 检查是否有 TC → REQ 追溯矩阵
    if grep -qE 'TC-[0-9]+.*REQ-[0-9]+|追溯矩阵|追溯|traceability' "$TEST_FILE" 2>/dev/null; then
      echo "  ✅ 测试报告包含 TC → REQ 追溯"
    else
      echo "  ❌ 测试报告缺少 TC → REQ 追溯矩阵（每个 TC-xxx 应对应 REQ-xxx）"
      ERRORS=$((ERRORS + 1))
    fi
  fi

  # 检查错误监控报告
  local ERROR_REPORT="$PROJECT_DIR/pipeline/8/error-monitor/error-report.md"
  if [ -f "$ERROR_REPORT" ]; then
    echo "  ✅ 错误监控报告存在"
    local ERROR_COUNT=$(grep -cE '🔴|ERROR|Exception' "$ERROR_REPORT" 2>/dev/null || echo 0)
    if [ "$ERROR_COUNT" -gt 0 ]; then
      echo "  🟡 错误监控报告中有 $ERROR_COUNT 处错误记录，需排查"
      WARNINGS=$((WARNINGS + 1))
    else
      echo "  ✅ 错误监控报告无未排查错误"
    fi
  else
    echo "  ❌ 错误监控报告不存在（test-monitor.sh 应在测试执行前启动）"
    ERRORS=$((ERRORS + 1))
  fi

  # E2E 执行验证（关键：防止"写了没跑"）
  local E2E_DIR="$PROJECT_DIR/tests/e2e"
  if [ -d "$E2E_DIR" ]; then
    local E2E_FILES=$(find "$E2E_DIR" -name "*.spec.*" -o -name "*.test.*" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$E2E_FILES" -gt 0 ]; then
      # 有 E2E 脚本 → 检查是否真的执行了
      local QA_REPORTS="$PROJECT_DIR/pipeline/8/qa-reports"
      local E2E_SCREENSHOTS=0
      if [ -d "$QA_REPORTS" ]; then
        E2E_SCREENSHOTS=$(find "$QA_REPORTS" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
      fi

      if [ "$E2E_SCREENSHOTS" -eq 0 ]; then
        echo "  ❌ 有 $E2E_FILES 个 E2E 脚本，但 qa-reports/ 无截图 — E2E 可能未执行"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ E2E 截图 $E2E_SCREENSHOTS 张（证明已执行）"
      fi

      # 检查 test-report.md 是否提及 E2E 结果
      if grep -qiE 'e2e|playwright|端到端' "$TEST_FILE" 2>/dev/null; then
        echo "  ✅ 测试报告包含 E2E 执行结果"
      else
        echo "  🟡 测试报告未提及 E2E 结果（建议补充 E2E 执行情况）"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  fi
}

# 检查 docs/ 归档（各阶段签收后检查对应文档是否存在）
check_docs_archive() {
  echo ""
  echo "📚 检查 docs/ 归档"

  local DOCS_DIR="$PROJECT_DIR/docs"
  if [ ! -d "$DOCS_DIR" ]; then
    echo "  ❌ docs/ 目录不存在"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 根据当前阶段检查已签收阶段的归档文档（bash 3.x 兼容）
  # 阶段2起：PRD.md
  # 阶段2.5起：+ CODE-MAP.md
  # 阶段2.8起：+ ARCHITECTURE.md
  # 阶段5.5起：+ QA-TEST-STRATEGY.md
  # 阶段7起：+ dev-log.md

  # PRD.md（阶段2起）
  if [ "$PHASE" != "0" ] && [ "$PHASE" != "1" ] && [ "$PHASE" != "1.5" ]; then
    if [ ! -f "$DOCS_DIR/PRD.md" ]; then
      echo "  ❌ docs/PRD.md 不存在（阶段1签收后应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/PRD.md"
    fi
  fi

  # CODE-MAP.md（阶段2.5起）
  case "$PHASE" in 2.5|2.8|5|5.5|6|6.3|6.5|7|8|8.5|9)
    if [ ! -f "$DOCS_DIR/CODE-MAP.md" ]; then
      echo "  ❌ docs/CODE-MAP.md 不存在（阶段2开始前应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/CODE-MAP.md"
    fi
  esac

  # ARCHITECTURE.md（阶段2.8起）
  case "$PHASE" in 2.8|5|5.5|6|6.3|6.5|7|8|8.5|9)
    if [ ! -f "$DOCS_DIR/ARCHITECTURE.md" ]; then
      echo "  ❌ docs/ARCHITECTURE.md 不存在（阶段2签收后应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/ARCHITECTURE.md"
    fi
  esac

  # QA-TEST-STRATEGY.md（阶段5.5起）
  case "$PHASE" in 5.5|6|6.3|6.5|7|8|8.5|9)
    if [ ! -f "$DOCS_DIR/QA-TEST-STRATEGY.md" ]; then
      echo "  ❌ docs/QA-TEST-STRATEGY.md 不存在（阶段5签收后应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/QA-TEST-STRATEGY.md"
    fi
  esac

  # dev-log.md（阶段7起）
  case "$PHASE" in 7|8|8.5|9)
    if [ ! -f "$DOCS_DIR/dev-log.md" ]; then
      echo "  ❌ docs/dev-log.md 不存在（阶段6-7完成后应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/dev-log.md"
    fi
  esac
}

# 检查交付文档（阶段9专用）
check_deliverable_docs() {
  echo ""
  echo "📦 检查交付文档"

  local DOCS_DIR="$PROJECT_DIR/docs"
  local DELIVERABLE_ERRORS=0

  # 4个交付文档必须存在
  local REQUIRED_DOCS=("user-manual.md" "api-docs.md" "rpc-api-docs.md" "integration-guide.md")
  for doc in "${REQUIRED_DOCS[@]}"; do
    if [ ! -f "$DOCS_DIR/$doc" ]; then
      echo "  ❌ docs/$doc 不存在"
      DELIVERABLE_ERRORS=$((DELIVERABLE_ERRORS + 1))
    else
      echo "  ✅ docs/$doc"
    fi
  done

  # 用户使用手册最低100行
  if [ -f "$DOCS_DIR/user-manual.md" ]; then
    local MANUAL_LINES=$(wc -l < "$DOCS_DIR/user-manual.md" | tr -d ' ')
    if [ "$MANUAL_LINES" -lt 100 ]; then
      echo "  ❌ user-manual.md 仅 ${MANUAL_LINES} 行（最低100行）"
      DELIVERABLE_ERRORS=$((DELIVERABLE_ERRORS + 1))
    else
      echo "  ✅ user-manual.md ${MANUAL_LINES} 行"
    fi
  fi

  # 接入指南必须包含步骤说明
  if [ -f "$DOCS_DIR/integration-guide.md" ]; then
    if ! grep -qE '步骤|step|Step' "$DOCS_DIR/integration-guide.md" 2>/dev/null; then
      echo "  ❌ integration-guide.md 缺少步骤说明（未找到'步骤'或'step'）"
      DELIVERABLE_ERRORS=$((DELIVERABLE_ERRORS + 1))
    else
      echo "  ✅ integration-guide.md 包含步骤说明"
    fi
  fi

  ERRORS=$((ERRORS + DELIVERABLE_ERRORS))
}

# 需求追溯检查（阶段5/5.5/8）
check_traceability() {
  local CHECK_STAGE="$1"

  echo ""
  echo "🔗 检查需求追溯完整性（阶段 $CHECK_STAGE）"

  local PRD_FILE="$PROJECT_DIR/docs/PRD.md"
  if [ ! -f "$PRD_FILE" ]; then
    # 尝试阶段1产出
    PRD_FILE="$PROJECT_DIR/pipeline/1/PRD.md"
  fi

  if [ ! -f "$PRD_FILE" ]; then
    echo "  ❌ PRD.md 不存在（docs/ 或 1/ 目录）"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 提取 PRD 中的 REQ-xxx
  local PRD_REQS=$(grep -oE 'REQ-[0-9]+' "$PRD_FILE" 2>/dev/null | sort -u)
  local PRD_REQ_COUNT=$(echo "$PRD_REQS" | grep -c 'REQ-' 2>/dev/null || echo 0)

  if [ "$PRD_REQ_COUNT" -eq 0 ]; then
    echo "  ❌ PRD.md 中未找到 REQ-xxx 编号（功能清单必须用 REQ-xxx 编号）"
    ERRORS=$((ERRORS + 1))
    return
  fi

  echo "  📋 PRD 中的 REQ 数量: $PRD_REQ_COUNT"

  # 阶段5：检查 TASK-LIST.md 的需求覆盖
  if [ "$CHECK_STAGE" = "5" ] || [ "$CHECK_STAGE" = "5.5" ] || [ "$CHECK_STAGE" = "8" ]; then
    local TASK_FILE="$PROJECT_DIR/pipeline/5/TASK-LIST.md"
    if [ -f "$TASK_FILE" ]; then
      local TASK_REQS=$(grep -oE 'REQ-[0-9]+' "$TASK_FILE" 2>/dev/null | sort -u)
      local TASK_REQ_COUNT=$(echo "$TASK_REQS" | grep -c 'REQ-' 2>/dev/null || echo 0)

      echo "  📋 任务覆盖的 REQ 数量: $TASK_REQ_COUNT"

      # 找出未被任务覆盖的 REQ
      local UNCOVERED_TASK_REQS=$(comm -23 <(echo "$PRD_REQS") <(echo "$TASK_REQS") 2>/dev/null)
      if [ -n "$UNCOVERED_TASK_REQS" ]; then
        echo "  ❌ 以下 REQ 未被任何任务覆盖:"
        echo "$UNCOVERED_TASK_REQS" | while read -r req; do
          [ -n "$req" ] && echo "     - $req"
        done
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ 所有 REQ 都有任务覆盖"
      fi
    else
      echo "  ⚠️ TASK-LIST.md 不存在，跳过任务覆盖检查"
    fi
  fi

  # 阶段5.5/8：检查 test-plan.md 的测试覆盖
  if [ "$CHECK_STAGE" = "5.5" ] || [ "$CHECK_STAGE" = "8" ]; then
    local TESTPLAN_FILE="$PROJECT_DIR/pipeline/5/test-plan.md"
    if [ -f "$TESTPLAN_FILE" ]; then
      local TEST_REQS=$(grep -oE 'REQ-[0-9]+' "$TESTPLAN_FILE" 2>/dev/null | sort -u)
      local TEST_REQ_COUNT=$(echo "$TEST_REQS" | grep -c 'REQ-' 2>/dev/null || echo 0)

      echo "  📋 测试覆盖的 REQ 数量: $TEST_REQ_COUNT"

      # 找出未被测试覆盖的 REQ
      local UNCOVERED_TEST_REQS=$(comm -23 <(echo "$PRD_REQS") <(echo "$TEST_REQS") 2>/dev/null)
      if [ -n "$UNCOVERED_TEST_REQS" ]; then
        echo "  ❌ 以下 REQ 未被测试用例覆盖:"
        echo "$UNCOVERED_TEST_REQS" | while read -r req; do
          [ -n "$req" ] && echo "     - $req"
        done
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ 所有 REQ 都有测试用例覆盖"
      fi
    else
      echo "  ⚠️ test-plan.md 不存在，跳过测试覆盖检查"
    fi
  fi

  # 阶段8：检查测试报告是否逐 REQ 报告
  if [ "$CHECK_STAGE" = "8" ]; then
    local TEST_REPORT="$PROJECT_DIR/pipeline/8/test-report.md"
    if [ -f "$TEST_REPORT" ]; then
      local REPORT_REQS=$(grep -oE 'REQ-[0-9]+' "$TEST_REPORT" 2>/dev/null | sort -u)
      local REPORT_REQ_COUNT=$(echo "$REPORT_REQS" | grep -c 'REQ-' 2>/dev/null || echo 0)

      echo "  📋 测试报告提及的 REQ 数量: $REPORT_REQ_COUNT"

      if [ "$REPORT_REQ_COUNT" -lt "$PRD_REQ_COUNT" ]; then
        local MISSING_REPORT_REQS=$(comm -23 <(echo "$PRD_REQS") <(echo "$REPORT_REQS") 2>/dev/null)
        if [ -n "$MISSING_REPORT_REQS" ]; then
          echo "  🟡 测试报告未提及以下 REQ:"
          echo "$MISSING_REPORT_REQS" | while read -r req; do
            [ -n "$req" ] && echo "     - $req"
          done
          WARNINGS=$((WARNINGS + 1))
        fi
      else
        echo "  ✅ 测试报告覆盖了所有 REQ"
      fi
    fi
  fi
}

# 技术方案实现检查（阶段7/8）
check_architecture_implementation() {
  echo ""
  echo "🏗️ 检查技术方案实现情况"

  local ARCH_FILE="$PROJECT_DIR/docs/ARCHITECTURE.md"
  if [ ! -f "$ARCH_FILE" ]; then
    ARCH_FILE="$PROJECT_DIR/pipeline/2/ARCHITECTURE.md"
  fi

  if [ ! -f "$ARCH_FILE" ]; then
    echo "  ⚠️ ARCHITECTURE.md 不存在，跳过"
    return
  fi

  # 提取架构中的关键设计点（模块、接口、模式）
  local ARCH_SECTIONS=$(grep -cE '^##' "$ARCH_FILE" 2>/dev/null || echo 0)
  echo "  📋 架构文档章节数: $ARCH_SECTIONS"

  # 检查代码中是否实现了架构提到的关键模块
  local CODE_DIR="$PROJECT_DIR"
  if [ ! -d "$CODE_DIR" ]; then
    echo "  ⚠️ 项目目录不存在，跳过"
    return
  fi

  # 提取架构中提到的类名/模块名（驼峰命名）
  local ARCH_NAMES=$(grep -oE '[A-Z][a-z]+([A-Z][a-z]+)+[A-Za-z]*' "$ARCH_FILE" 2>/dev/null | sort -u | head -20)
  local MISSING_IMPL=0

  if [ -n "$ARCH_NAMES" ]; then
    while IFS= read -r name; do
      [ -z "$name" ] && continue
      # 在代码中搜索该类名
      if ! grep -r "$name" "$CODE_DIR" --exclude-dir=pipeline --exclude-dir=node_modules --exclude-dir=.git --include="*.java" --include="*.ts" --include="*.py" --include="*.vue" -l 2>/dev/null | head -1 > /dev/null; then
        echo "  🟡 架构中提到的 '$name' 在代码中未找到实现"
        MISSING_IMPL=$((MISSING_IMPL + 1))
      fi
    done <<< "$ARCH_NAMES"
  fi

  if [ "$MISSING_IMPL" -gt 0 ]; then
    echo "  🟡 有 $MISSING_IMPL 个架构设计点未在代码中找到对应实现"
    WARNINGS=$((WARNINGS + 1))
  else
    echo "  ✅ 架构设计点在代码中都有对应实现"
  fi
}

# 通用检查：沟通记录
check_communications() {
  echo ""
  echo "💬 检查沟通记录"

  local COMM_DIR="$PROJECT_DIR/communications"
  if [ -d "$COMM_DIR" ]; then
    local COMM_COUNT=$(find "$COMM_DIR" -name "comm-*.md" -type f | wc -l | tr -d ' ')
    echo "  沟通记录数: $COMM_COUNT"

    if [ "$COMM_COUNT" -eq 0 ]; then
      echo "  🟡 没有沟通记录"
      WARNINGS=$((WARNINGS + 1))
    else
      echo "  ✅ 沟通记录存在"
    fi
  else
    echo "  🟡 communications/ 目录不存在"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# 测试交叉审查检查（阶段7-test-review）
check_test_review() {
  echo ""
  echo "🧪 检查测试交叉审查"

  local TEST_REVIEW_DIR="$PROJECT_DIR/pipeline/7/test-reviews"
  local TEST_REVIEW_FILE="$PROJECT_DIR/pipeline/7/test-review.md"

  # 检查 test-reviews 目录
  if [ ! -d "$TEST_REVIEW_DIR" ]; then
    echo "  ❌ test-reviews/ 目录不存在（run-test-review.sh 应创建此目录）"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 检查单元测试验收报告数量
  local UNIT_REVIEW_COUNT=$(find "$TEST_REVIEW_DIR" -name "unit-*.md" -type f | wc -l | tr -d ' ')
  echo "  📋 单元测试验收报告数: $UNIT_REVIEW_COUNT"
  if [ "$UNIT_REVIEW_COUNT" -eq 0 ]; then
    echo "  ❌ 没有单元测试验收报告"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 找到单元测试验收报告"
  fi

  # 检查集成测试验收
  if [ -f "$TEST_REVIEW_DIR/integration-review.md" ]; then
    echo "  ✅ 集成测试验收报告存在"
  else
    echo "  🟡 集成测试验收报告不存在（可能无集成测试）"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 检查 E2E 自查
  if [ -f "$TEST_REVIEW_DIR/e2e-self-review.md" ]; then
    echo "  ✅ E2E 自查报告存在"
  else
    echo "  🟡 E2E 自查报告不存在（可能无 E2E 测试）"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 检查 E2E 开发确认
  if [ -f "$TEST_REVIEW_DIR/e2e-dev-confirm.md" ]; then
    echo "  ✅ E2E 开发确认报告存在"
  else
    echo "  🟡 E2E 开发确认报告不存在（可能无 E2E 测试）"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 检查汇总报告
  if [ ! -f "$TEST_REVIEW_FILE" ] || [ ! -s "$TEST_REVIEW_FILE" ]; then
    echo "  ❌ test-review.md 汇总报告不存在或为空"
    ERRORS=$((ERRORS + 1))
  else
    local LINES=$(wc -l < "$TEST_REVIEW_FILE" | tr -d ' ')
    echo "  ✅ test-review.md 汇总报告存在 (${LINES}行)"
    if [ "$LINES" -lt 30 ]; then
      echo "  ❌ test-review.md 行数不足（${LINES}行，最低30行）"
      ERRORS=$((ERRORS + 1))
    fi
  fi

  # 检查是否有不通过的结论
  if [ -f "$TEST_REVIEW_FILE" ]; then
    if grep -qE '不通过|需补充|需修改|不合格' "$TEST_REVIEW_FILE" 2>/dev/null; then
      echo "  🟡 测试审查有不通过项，需修复后复审"
      WARNINGS=$((WARNINGS + 1))
    fi
  fi
}

# 架构审查必须引用架构文档（阶段7）
check_architecture_reference() {
  echo ""
  echo "🏗️ 检查架构引用（阶段7）"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/7/review-report.md"
  if [ ! -f "$REVIEW_FILE" ]; then
    echo "  ⚠️ 审查报告不存在，跳过架构引用检查"
    return
  fi

  # 检查审查报告是否提到了架构相关内容
  if grep -qE '架构|分层|Controller|Service|Repository|模块|模式|ARCHITECTURE|设计模式|DDD|聚合|策略|观察者' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 审查报告引用了架构相关内容"
  else
    echo "  ❌ 审查报告未引用架构文档内容（未找到架构相关关键词）"
    echo "     架构师应基于阶段2产出的 ARCHITECTURE.md 对比代码审查（同 session 上下文已知）"
    ERRORS=$((ERRORS + 1))
  fi
}

# 覆盖率检查（阶段6/8）— 分层校验
check_coverage() {
  echo ""
  echo "📊 检查测试覆盖率（阈值 95%）— 分层校验"

  local UNIT_REPORT="$PROJECT_DIR/coverage/unit/index.html"
  local INT_REPORT="$PROJECT_DIR/coverage/integration/index.html"
  local PASS=true
  local FOUND_ANY=false

  # ── 单元测试覆盖率 ──
  if [ -f "$UNIT_REPORT" ]; then
    FOUND_ANY=true
    local UNIT_COV=$(grep -oP '(?:Lines|Total).*?(\d+)%' "$UNIT_REPORT" 2>/dev/null | grep -oP '\d+' | head -1)
    if [ -z "$UNIT_COV" ]; then
      # fallback: 尝试其他常见 HTML 格式
      UNIT_COV=$(grep -oE '[0-9]+%' "$UNIT_REPORT" 2>/dev/null | head -1 | tr -d '%')
    fi
    if [ -n "$UNIT_COV" ] && [ "$UNIT_COV" -ge 95 ]; then
      echo "  ✅ 单元测试覆盖率: ${UNIT_COV}%"
    elif [ -n "$UNIT_COV" ]; then
      echo "  ❌ 单元测试覆盖率: ${UNIT_COV}%（低于 95%）"
      PASS=false
      ERRORS=$((ERRORS + 1))
    else
      echo "  🟡 单元测试覆盖率报告存在但无法解析"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  ❌ 未找到单元测试覆盖率报告 (coverage/unit/index.html)"
    echo "     阶段2架构师应已配置覆盖率工具，输出到统一路径"
    PASS=false
  fi

  # ── 集成测试覆盖率 ──
  if [ -f "$INT_REPORT" ]; then
    FOUND_ANY=true
    local INT_COV=$(grep -oP '(?:Lines|Total).*?(\d+)%' "$INT_REPORT" 2>/dev/null | grep -oP '\d+' | head -1)
    if [ -z "$INT_COV" ]; then
      INT_COV=$(grep -oE '[0-9]+%' "$INT_REPORT" 2>/dev/null | head -1 | tr -d '%')
    fi
    if [ -n "$INT_COV" ] && [ "$INT_COV" -ge 95 ]; then
      echo "  ✅ 集成测试覆盖率: ${INT_COV}%"
    elif [ -n "$INT_COV" ]; then
      echo "  ❌ 集成测试覆盖率: ${INT_COV}%（低于 95%）"
      PASS=false
      ERRORS=$((ERRORS + 1))
    else
      echo "  🟡 集成测试覆盖率报告存在但无法解析"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  ❌ 未找到集成测试覆盖率报告 (coverage/integration/index.html)"
    echo "     阶段2架构师应已配置覆盖率工具，输出到统一路径"
    PASS=false
  fi

  if [ "$FOUND_ANY" = false ]; then
    ERRORS=$((ERRORS + 1))
  fi

  # ── 兼容旧路径：如存在 target/site/jacoco 但无统一路径，提示迁移 ──
  local LEGACY_JACOCO="$PROJECT_DIR/target/site/jacoco/index.html"
  if [ -f "$LEGACY_JACOCO" ] && [ ! -f "$UNIT_REPORT" ]; then
    echo "  ⚠️ 发现旧路径 JaCoCo 报告 (target/site/jacoco/)，请按统一路径约定迁移"
    echo "     mkdir -p coverage/unit coverage/integration"
    echo "     ln -sf $PWD/target/site/jacoco-ut coverage/unit"
    echo "     ln -sf $PWD/target/site/jacoco-it coverage/integration"
    WARNINGS=$((WARNINGS + 1))
  fi

  # ── 集成测试 mock 检查 ──
  local INT_DIR="$PROJECT_DIR/tests/integration"
  if [ -d "$INT_DIR" ]; then
    local MOCK_COUNT=$(grep -rl "mock\|Mock\|@Mock\|jest.mock\|unittest.mock" "$INT_DIR" 2>/dev/null | wc -l | tr -d ' ')
    local TOTAL_INT=$(find "$INT_DIR" -name "*.test.*" -o -name "*Test.*" -o -name "test_*" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$TOTAL_INT" -gt 0 ]; then
      if [ "$MOCK_COUNT" -gt 0 ]; then
        echo "  🟡 集成测试中 $MOCK_COUNT 个文件使用了 mock（应连接真实 DB）"
        WARNINGS=$((WARNINGS + 1))
      else
        echo "  ✅ 集成测试未使用 mock"
      fi
    fi
  fi
}

# TC 追溯校验（阶段6/7/8）
# 扫描测试代码中的 TC-xxx 标注，对比 test-plan.md 中的 TC 列表
check_tc_traceability() {
  echo ""
  echo "🔗 检查 TC 追溯（测试代码 → test-plan.md）"

  local TEST_PLAN="$PROJECT_DIR/test-plan.md"
  if [ ! -f "$TEST_PLAN" ]; then
    echo "  ⚠️ test-plan.md 不存在，跳过 TC 追溯检查"
    return
  fi

  # 提取 test-plan.md 中的所有 TC-xxx
  local PLAN_TCS=$(grep -oE 'TC-[0-9]+' "$TEST_PLAN" 2>/dev/null | sort -u)
  if [ -z "$PLAN_TCS" ]; then
    echo "  ⚠️ test-plan.md 中未找到 TC-xxx 编号"
    WARNINGS=$((WARNINGS + 1))
    return
  fi

  local PLAN_TC_COUNT=$(echo "$PLAN_TCS" | wc -l | tr -d ' ')
  echo "  📋 test-plan.md 中定义了 ${PLAN_TC_COUNT} 个 TC"

  # 扫描测试代码中的 TC-xxx 标注
  local TESTS_DIR="$PROJECT_DIR/tests"
  if [ ! -d "$TESTS_DIR" ]; then
    echo "  ❌ tests/ 目录不存在"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 支持 Java (@DisplayName, 注释), JS/TS (注释, describe/it), Python (注释, docstring)
  local CODE_TCS=$(grep -roE 'TC-[0-9]+' "$TESTS_DIR" 2>/dev/null | sed 's/.*:\(TC-[0-9]*\).*/\1/' | sort -u)
  local CODE_TC_COUNT=$(echo "$CODE_TCS" | grep -c 'TC-' 2>/dev/null || echo 0)
  echo "  📝 测试代码中标注了 ${CODE_TC_COUNT} 个 TC"

  # 找出 test-plan 中有但测试代码中没标注的 TC
  local MISSING_TCS=""
  for tc in $PLAN_TCS; do
    if ! echo "$CODE_TCS" | grep -q "$tc"; then
      MISSING_TCS="$MISSING_TCS $tc"
    fi
  done

  if [ -z "$MISSING_TCS" ]; then
    echo "  ✅ test-plan.md 中所有 TC 均在测试代码中有标注"
  else
    local MISSING_COUNT=$(echo "$MISSING_TCS" | wc -w | tr -d ' ')
    echo "  ❌ ${MISSING_COUNT} 个 TC 在测试代码中未标注:$(echo $MISSING_TCS | tr '\n' ' ')"
    echo "     开发必须在测试方法名或注释中标注 TC-xxx（如 @DisplayName(\"TC-001: ...\") 或 // TC-001）"
    ERRORS=$((ERRORS + 1))
  fi

  # 找出测试代码中有但 test-plan 中没有的 TC（可能是遗漏或拼写错误）
  local EXTRA_TCS=""
  for tc in $CODE_TCS; do
    if ! echo "$PLAN_TCS" | grep -q "$tc"; then
      EXTRA_TCS="$EXTRA_TCS $tc"
    fi
  done

  if [ -n "$EXTRA_TCS" ]; then
    local EXTRA_COUNT=$(echo "$EXTRA_TCS" | wc -w | tr -d ' ')
    echo "  🟡 ${EXTRA_COUNT} 个 TC 仅在测试代码中存在，test-plan.md 未定义:$(echo $EXTRA_TCS | tr '\n' ' ')"
    echo "     请确认这些 TC 是否需要补充到 test-plan.md"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# 开发产出分层架构检查（阶段6）
check_layered_architecture() {
  echo ""
  echo "🏗️ 检查分层架构（阶段6）"

  local CODE_DIR="$PROJECT_DIR"
  if [ ! -d "$CODE_DIR" ]; then
    echo "  ⚠️ 项目目录不存在，跳过分层检查"
    return
  fi

  local VIOLATIONS=0

  # Controller 是否直接 import Repository/Mapper
  local CONTROLLER_FILES=$(find "$CODE_DIR" -not -path "*/pipeline/*" -not -path "*/node_modules/*" -name "*Controller*" -type f 2>/dev/null)
  if [ -n "$CONTROLLER_FILES" ]; then
    local REPO_IMPORTS=$(echo "$CONTROLLER_FILES" | xargs grep -l "import.*Repository\|import.*Mapper" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$REPO_IMPORTS" -gt 0 ]; then
      echo "  ❌ Controller 直接引用 Repository/Mapper（违反分层架构）"
      VIOLATIONS=$((VIOLATIONS + 1))
    else
      echo "  ✅ Controller 未直接引用 Repository"
    fi
  fi

  # Service 是否 import HttpServletRequest
  local SERVICE_FILES=$(find "$CODE_DIR" -not -path "*/pipeline/*" -not -path "*/node_modules/*" -name "*Service*" -type f 2>/dev/null)
  if [ -n "$SERVICE_FILES" ]; then
    local HTTP_IMPORTS=$(echo "$SERVICE_FILES" | xargs grep -l "import.*HttpServletRequest\|import.*HttpServletResponse" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$HTTP_IMPORTS" -gt 0 ]; then
      echo "  ❌ Service 依赖了 HttpServletRequest（框架对象不应穿透到 Service 层）"
      VIOLATIONS=$((VIOLATIONS + 1))
    else
      echo "  ✅ Service 未依赖 HttpServletRequest"
    fi
  fi

  ERRORS=$((ERRORS + VIOLATIONS))
}

# 必读文件引用检查
check_input_references() {
  local PHASE="$1"
  local OUTPUT_FILE="$2"
  shift 2

  echo ""
  echo "📚 检查必读文件引用（阶段$PHASE）"

  if [ ! -f "$OUTPUT_FILE" ]; then
    echo "  ⚠️ 产出文件不存在，跳过引用检查"
    return
  fi

  for req_file in "$@"; do
    local basename_noext=$(basename "$req_file" .md)
    if grep -qi "$basename_noext" "$OUTPUT_FILE" 2>/dev/null; then
      echo "  ✅ 引用了 $req_file"
    else
      echo "  🟡 产出未引用必读文件: $req_file"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
}

# PM验收专用检查（阶段8.5）
check_pm_acceptance() {
  echo ""
  echo "📋 检查 PM 验收报告"

  local ACCEPTANCE_FILE="$PROJECT_DIR/pipeline/8.5/pm-acceptance.md"
  if [ ! -f "$ACCEPTANCE_FILE" ] || [ ! -s "$ACCEPTANCE_FILE" ]; then
    echo "  ❌ pm-acceptance.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 检查包含"结论"关键词
  if grep -q '结论' "$ACCEPTANCE_FILE" 2>/dev/null; then
    echo "  ✅ 包含结论段落"
  else
    echo "  ❌ 缺少结论段落（未找到'结论'关键词）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查引用了 PRD
  if grep -qi 'PRD' "$ACCEPTANCE_FILE" 2>/dev/null; then
    echo "  ✅ 引用了 PRD"
  else
    echo "  ❌ 未引用 PRD（PM 验收必须对照 PRD）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查有明确判定
  if grep -qE '通过|不通过' "$ACCEPTANCE_FILE" 2>/dev/null; then
    echo "  ✅ 包含明确判定"
  else
    echo "  ❌ 缺少明确判定（未找到'通过'或'不通过'）"
    ERRORS=$((ERRORS + 1))
  fi
}

# 检查接口文档（阶段5.5）
check_api_schema() {
  echo ""
  echo "📋 检查接口文档"

  local API_FILE="$PROJECT_DIR/pipeline/5.5/api-schema.md"
  if [ ! -f "$API_FILE" ] || [ ! -s "$API_FILE" ]; then
    echo "  ❌ api-schema.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$API_FILE" | tr -d ' ')
  echo "  ✅ api-schema.md 存在 (${LINES}行)"
  if [ "$LINES" -lt 30 ]; then
    echo "  ❌ api-schema.md 过短（${LINES}行，最低30行）"
    ERRORS=$((ERRORS + 1))
  fi

  # 检查包含 API 路径定义
  local API_PATHS=$(grep -cE 'GET |POST |PUT |DELETE |PATCH |/api/|/v[0-9]/' "$API_FILE" 2>/dev/null || echo 0)
  echo "  🔍 发现 API 路径: $API_PATHS"
  if [ "$API_PATHS" -lt 3 ]; then
    echo "  ❌ API 路径定义少于3个"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ API 路径数量达标"
  fi
}

# 检查 HTML 交付文档（阶段9）
check_html_docs() {
  echo ""
  echo "🌐 检查 HTML 交付文档"

  local DOCS_DIR="$PROJECT_DIR/docs"
  local REQUIRED_HTML=("acceptance-report.html" "prd.html" "architecture.html")
  local HTML_ERRORS=0

  for html in "${REQUIRED_HTML[@]}"; do
    if [ ! -f "$DOCS_DIR/$html" ]; then
      echo "  ❌ docs/$html 不存在"
      HTML_ERRORS=$((HTML_ERRORS + 1))
    else
      echo "  ✅ docs/$html"
    fi
  done

  ERRORS=$((ERRORS + HTML_ERRORS))
}

# 检查 HTML 审阅文档（阶段 1.6 / 2.6）
check_html_draft() {
  local HTML_FILE="$1"
  local FEEDBACK_FILE="$2"
  local DOC_NAME="$3"

  echo ""
  echo "🌐 检查 HTML 审阅文档 ($DOC_NAME)"

  # 1. HTML 文件存在且非空
  if [ ! -f "$HTML_FILE" ] || [ ! -s "$HTML_FILE" ]; then
    echo "  ❌ $HTML_FILE 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi
  echo "  ✅ HTML 文件存在"

  # 2. 内联 CSS（不能有外部样式表引用）
  if grep -qE '<link.*rel="stylesheet"|@import' "$HTML_FILE" 2>/dev/null; then
    echo "  ❌ HTML 引用了外部样式表（必须内联 CSS）"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ CSS 已内联"
  fi

  # 3. 结构检查：必须有标题标签
  if ! grep -qE '<h[1-3]' "$HTML_FILE" 2>/dev/null; then
    echo "  🟡 HTML 缺少标题标签（h1-h3），结构不清晰"
    WARNINGS=$((WARNINGS + 1))
  else
    echo "  ✅ 包含标题结构"
  fi

  # 4. 结构检查：必须有表格
  if ! grep -qE '<table' "$HTML_FILE" 2>/dev/null; then
    echo "  🟡 HTML 缺少表格，建议用表格展示结构化信息"
    WARNINGS=$((WARNINGS + 1))
  else
    echo "  ✅ 包含表格"
  fi

  # 5. 反馈文件存在
  if [ ! -f "$FEEDBACK_FILE" ] || [ ! -s "$FEEDBACK_FILE" ]; then
    echo "  ❌ $FEEDBACK_FILE 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi
  echo "  ✅ 反馈文件存在"

  # 6. 反馈文件包含用户确认
  if grep -qE '确认|通过|同意|approved|LGTM' "$FEEDBACK_FILE" 2>/dev/null; then
    echo "  ✅ 包含用户确认"
  else
    echo "  ❌ 反馈文件未包含用户确认（需有'确认'/'通过'/'同意'）"
    ERRORS=$((ERRORS + 1))
  fi
}

# ─── 阶段0：项目初始化检查 ───
check_project_init() {
  echo ""
  echo "🚀 检查项目初始化"

  # health-dashboard.md
  local HD_FILE="$PROJECT_DIR/pipeline/0/health-dashboard.md"
  if [ -f "$HD_FILE" ] && [ -s "$HD_FILE" ]; then
    echo "  ✅ health-dashboard.md 存在"
  else
    echo "  ❌ health-dashboard.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
  fi

  # _index.json 合法 JSON
  local INDEX_FILE="$PROJECT_DIR/pipeline/0/_index.json"
  if [ -f "$INDEX_FILE" ]; then
    if python3 -c "import json; json.load(open('$INDEX_FILE'))" 2>/dev/null; then
      echo "  ✅ _index.json 合法 JSON"
    else
      echo "  ❌ _index.json 不是合法 JSON"
      ERRORS=$((ERRORS + 1))
    fi
  else
    echo "  ❌ _index.json 不存在"
    ERRORS=$((ERRORS + 1))
  fi
}

# ─── 阶段1：PRD 深度检查 ───
check_prd_quality() {
  echo ""
  echo "📝 检查 PRD 质量"

  local PRD_FILE="$PROJECT_DIR/pipeline/1/PRD.md"
  if [ ! -f "$PRD_FILE" ]; then
    return
  fi

  # REQ 数量 ≥3
  local REQ_COUNT=$(grep -cE '### REQ-[0-9]+' "$PRD_FILE" 2>/dev/null || echo 0)
  if [ "$REQ_COUNT" -lt 3 ]; then
    echo "  ❌ REQ 数量不足（$REQ_COUNT 个，最低 3 个）"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ REQ 数量: $REQ_COUNT"
  fi

  # 每个 REQ 包含验收标准
  local REQ_WITHOUT_AC=0
  while IFS= read -r req_line; do
    local req_id=$(echo "$req_line" | grep -oE 'REQ-[0-9]+')
    [ -z "$req_id" ] && continue
    # 检查该 REQ 到下一个 REQ 之间是否有验收标准
    local req_block=$(awk "/### $req_id/{found=1;next} /### REQ-/{found=0} found" "$PRD_FILE")
    if ! echo "$req_block" | grep -qE '验收标准|验收条件|Acceptance'; then
      echo "  🟡 $req_id 缺少验收标准"
      REQ_WITHOUT_AC=$((REQ_WITHOUT_AC + 1))
    fi
  done < <(grep -E '### REQ-[0-9]+' "$PRD_FILE" 2>/dev/null)
  if [ "$REQ_WITHOUT_AC" -gt 0 ]; then
    echo "  🟡 $REQ_WITHOUT_AC 个 REQ 缺少验收标准"
    WARNINGS=$((WARNINGS + 1))
  else
    echo "  ✅ 每个 REQ 都有验收标准"
  fi

  # _config.json size 字段
  local CONFIG_FILE="$PROJECT_DIR/_config.json"
  if [ -f "$CONFIG_FILE" ]; then
    local SIZE=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('size',''))" 2>/dev/null)
    case "$SIZE" in
      large|medium|small)
        echo "  ✅ _config.json size = $SIZE"
        ;;
      *)
        echo "  ❌ _config.json size 字段缺失或无效（应为 large/medium/small）"
        ERRORS=$((ERRORS + 1))
        ;;
    esac
  else
    echo "  ❌ _config.json 不存在（阶段1 PRD 签收后应创建）"
    ERRORS=$((ERRORS + 1))
  fi
}

# ─── 阶段2：架构产出物检查 ───
check_architecture_outputs() {
  echo ""
  echo "🏗️ 检查架构产出物"

  # docker-compose.test.yml
  local DC_FILE="$PROJECT_DIR/docker-compose.test.yml"
  if [ -f "$DC_FILE" ] && [ -s "$DC_FILE" ]; then
    echo "  ✅ docker-compose.test.yml 存在"
    # 检查是否有 healthcheck
    if grep -q "healthcheck" "$DC_FILE" 2>/dev/null; then
      echo "  ✅ 包含 healthcheck 配置"
    else
      echo "  🟡 docker-compose.test.yml 缺少 healthcheck（建议添加）"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  ❌ docker-compose.test.yml 不存在（架构师应产出测试环境定义）"
    ERRORS=$((ERRORS + 1))
  fi

  # 覆盖率工具配置
  local POM_FILE="$PROJECT_DIR/pom.xml"
  local PACKAGE_FILE="$PROJECT_DIR/package.json"
  local PYPROJECT_FILE="$PROJECT_DIR/pyproject.toml"
  local COVERAGE_FOUND=false

  if [ -f "$POM_FILE" ]; then
    if grep -q "jacoco" "$POM_FILE" 2>/dev/null; then
      echo "  ✅ pom.xml 包含 JaCoCo 配置"
      COVERAGE_FOUND=true
      # 检查阈值是否为 95%
      if grep -q "0.95" "$POM_FILE" 2>/dev/null; then
        echo "  ✅ JaCoCo 阈值 ≥ 95%"
      else
        echo "  🟡 JaCoCo 阈值未设为 95%（请确认）"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  fi
  if [ -f "$PACKAGE_FILE" ]; then
    if grep -qE "c8|nyc|coverage" "$PACKAGE_FILE" 2>/dev/null; then
      echo "  ✅ package.json 包含覆盖率工具配置"
      COVERAGE_FOUND=true
    fi
  fi
  if [ -f "$PYPROJECT_FILE" ]; then
    if grep -q "cov" "$PYPROJECT_FILE" 2>/dev/null; then
      echo "  ✅ pyproject.toml 包含 pytest-cov 配置"
      COVERAGE_FOUND=true
    fi
  fi
  if [ "$COVERAGE_FOUND" = false ]; then
    echo "  ❌ 未找到覆盖率工具配置（JaCoCo/c8/pytest-cov）"
    ERRORS=$((ERRORS + 1))
  fi

  # ARCHITECTURE.md 结构要求
  local ARCH_FILE="$PROJECT_DIR/pipeline/2/ARCHITECTURE.md"
  if [ -f "$ARCH_FILE" ]; then
    # 风险识别 ≥3
    local RISK_COUNT=$(grep -ciE '风险|Risk|⚠️' "$ARCH_FILE" 2>/dev/null || echo 0)
    if [ "$RISK_COUNT" -lt 3 ]; then
      echo "  🟡 ARCHITECTURE.md 风险识别偏少（$RISK_COUNT 处，建议 ≥3）"
      WARNINGS=$((WARNINGS + 1))
    else
      echo "  ✅ 风险识别: $RISK_COUNT 处"
    fi
  fi
}

# ─── 阶段5：任务分解深度检查 ───
check_task_list_quality() {
  echo ""
  echo "📋 检查任务分解质量"

  local TASK_FILE="$PROJECT_DIR/pipeline/5/TASK-LIST.md"
  local TEST_PLAN="$PROJECT_DIR/pipeline/5/test-plan.md"

  # test-plan.md 存在且 ≥30 行
  if [ -f "$TEST_PLAN" ] && [ -s "$TEST_PLAN" ]; then
    local TP_LINES=$(wc -l < "$TEST_PLAN" | tr -d ' ')
    if [ "$TP_LINES" -lt 30 ]; then
      echo "  ❌ test-plan.md 过短（${TP_LINES}行，最低30行）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ test-plan.md 存在（${TP_LINES}行）"
    fi
  else
    echo "  ❌ test-plan.md 不存在或为空（QA 应在阶段5同步产出）"
    ERRORS=$((ERRORS + 1))
  fi

  [ ! -f "$TASK_FILE" ] && return

  # 每个任务必须有 **需求** 字段
  local TASK_COUNT=$(grep -cE '### T-[0-9]+' "$TASK_FILE" 2>/dev/null || echo 0)
  local TASKS_WITH_REQ=$(grep -cE '\*\*需求\*\*:' "$TASK_FILE" 2>/dev/null || echo 0)
  if [ "$TASK_COUNT" -gt 0 ]; then
    if [ "$TASKS_WITH_REQ" -lt "$TASK_COUNT" ]; then
      echo "  ❌ $TASK_COUNT 个任务中只有 $TASKS_WITH_REQ 个有 **需求** 字段（每个任务必须关联 REQ-xxx）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 每个任务都有 **需求** 字段"
    fi
  fi

  # 每个任务必须有 **并发组** 字段
  local TASKS_WITH_GROUP=$(grep -cE '\*\*并发组\*\*:' "$TASK_FILE" 2>/dev/null || echo 0)
  if [ "$TASK_COUNT" -gt 0 ] && [ "$TASKS_WITH_GROUP" -lt "$TASK_COUNT" ]; then
    echo "  🟡 $TASK_COUNT 个任务中只有 $TASKS_WITH_GROUP 个有 **并发组** 字段"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 开发者任务均衡（差异 ≤2）
  local DEV1=$(grep -c "\*\*开发者\*\*:\s*dev1" "$TASK_FILE" 2>/dev/null || echo 0)
  local DEV2=$(grep -c "\*\*开发者\*\*:\s*dev2" "$TASK_FILE" 2>/dev/null || echo 0)
  local DEV3=$(grep -c "\*\*开发者\*\*:\s*dev3" "$TASK_FILE" 2>/dev/null || echo 0)
  local MAX=$DEV1; local MIN=$DEV1
  [ "$DEV2" -gt "$MAX" ] && MAX=$DEV2; [ "$DEV3" -gt "$MAX" ] && MAX=$DEV3
  [ "$DEV2" -lt "$MIN" ] && MIN=$DEV2; [ "$DEV3" -lt "$MIN" ] && MIN=$DEV3
  local DIFF=$((MAX - MIN))
  if [ "$DIFF" -gt 2 ]; then
    echo "  ❌ 开发者任务分配不均衡（dev1=$DEV1, dev2=$DEV2, dev3=$DEV3, 差异=$DIFF, 应≤2）"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 开发者任务均衡（dev1=$DEV1, dev2=$DEV2, dev3=$DEV3）"
  fi

  # 禁止优先级字段
  if grep -qE '\*\*优先级\*\*|P0|P1|P2' "$TASK_FILE" 2>/dev/null; then
    echo "  🟡 TASK-LIST.md 包含优先级字段（不做的一律不拆，不应有优先级）"
    WARNINGS=$((WARNINGS + 1))
  fi

  # test-plan.md 每个用例有 **覆盖** 字段
  if [ -f "$TEST_PLAN" ]; then
    local TC_COUNT=$(grep -cE '### TC-' "$TEST_PLAN" 2>/dev/null || echo 0)
    local TC_WITH_COVER=$(grep -cE '\*\*覆盖\*\*:' "$TEST_PLAN" 2>/dev/null || echo 0)
    if [ "$TC_COUNT" -gt 0 ]; then
      if [ "$TC_WITH_COVER" -lt "$TC_COUNT" ]; then
        echo "  ❌ $TC_COUNT 个用例中只有 $TC_WITH_COVER 个有 **覆盖** 字段（每个用例必须关联 REQ-xxx）"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ 每个测试用例都有 **覆盖** 字段"
      fi
    fi
  fi
}

# ─── 阶段6.3：代码集成检查 ───
check_code_integration() {
  echo ""
  echo "🔗 检查代码集成"

  local INT_DIR="$PROJECT_DIR/pipeline/6.3"
  if [ ! -d "$INT_DIR" ]; then
    echo "  ❌ 6.3/ 目录不存在"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # 集成后代码存在
  local MERGE_REPORT="$INT_DIR/merge-report.md"
  if [ -f "$MERGE_REPORT" ] && [ -s "$MERGE_REPORT" ]; then
    echo "  ✅ merge-report.md 存在"
  else
    echo "  ❌ merge-report.md 不存在（代码集成报告）"
    ERRORS=$((ERRORS + 1))
  fi

  # 冒烟测试
  local SMOKE_REPORT="$INT_DIR/smoke-test.md"
  if [ -f "$SMOKE_REPORT" ] && [ -s "$SMOKE_REPORT" ]; then
    echo "  ✅ smoke-test.md 存在"
    if grep -qiE '通过|pass|✅' "$SMOKE_REPORT" 2>/dev/null; then
      echo "  ✅ 冒烟测试通过"
    else
      echo "  🟡 冒烟测试报告未明确标注通过"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  ❌ smoke-test.md 不存在（集成后必须冒烟测试）"
    ERRORS=$((ERRORS + 1))
  fi
}

# ─── 阶段6.5：开发审查检查 ───
check_dev_review() {
  echo ""
  echo "🔍 检查开发审查（阶段6.5）"

  local REVIEW_FILE="$PROJECT_DIR/pipeline/6.5/cross-review-dev.md"
  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ cross-review-dev.md 不存在或为空"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local LINES=$(wc -l < "$REVIEW_FILE" | tr -d ' ')
  echo "  ✅ cross-review-dev.md 存在 (${LINES}行)"

  # 架构师有独立段落
  if grep -qE '架构师|Architect' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 包含架构师审查段落"
  else
    echo "  ❌ 缺少架构师审查段落"
    ERRORS=$((ERRORS + 1))
  fi

  # 每段 ≥3 检查点
  local CHECKPOINT_COUNT=$(grep -cE '检查|check|验证|确认|问题|建议|✅|❌|🟡' "$REVIEW_FILE" 2>/dev/null || echo 0)
  if [ "$CHECKPOINT_COUNT" -lt 3 ]; then
    echo "  ❌ 检查点不足（$CHECKPOINT_COUNT 个，最低 3 个）"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 检查点: $CHECKPOINT_COUNT 个"
  fi

  # 引用架构相关内容
  if grep -qiE '架构|ARCHITECTURE|分层|模块|接口|设计' "$REVIEW_FILE" 2>/dev/null; then
    echo "  ✅ 引用了架构相关内容"
  else
    echo "  🟡 未引用架构相关内容（建议关联架构设计）"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# ─── 阶段7：安全扫描检查 ───
check_security_scan() {
  echo ""
  echo "🔒 检查安全扫描"

  # 检查 review-report.md 中是否包含安全扫描结果
  local REVIEW_FILE="$PROJECT_DIR/pipeline/7/review-report.md"
  if [ -f "$REVIEW_FILE" ]; then
    if grep -qiE '安全扫描|security.scan|严重问题.*0|无安全问题' "$REVIEW_FILE" 2>/dev/null; then
      echo "  ✅ review-report.md 包含安全扫描结果"
      # 检查是否有严重问题
      if grep -qiE '严重问题.*[1-9]|🔴.*问题|SQL注入|XSS|硬编码.*密钥|路径穿越' "$REVIEW_FILE" 2>/dev/null; then
        echo "  ❌ 发现严重安全问题未修复"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ 无严重安全问题"
      fi
    else
      echo "  🟡 review-report.md 未包含安全扫描结果（架构师应先跑 security-scan.sh）"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  🟡 review-report.md 不存在，跳过安全扫描检查"
  fi

  # 检查 security-scan.sh 是否可执行
  local SCAN_SCRIPT="$PIPELINE_ROOT/scripts/security-scan.sh"
  if [ -f "$SCAN_SCRIPT" ]; then
    echo "  ✅ security-scan.sh 脚本存在"
  else
    echo "  ❌ security-scan.sh 脚本不存在"
    ERRORS=$((ERRORS + 1))
  fi
}

# ─── 阶段8：E2E 深度检查 ───
check_e2e_execution() {
  echo ""
  echo "🎭 检查 E2E 测试执行"

  local QA_REPORTS="$PROJECT_DIR/pipeline/8/qa-reports"
  local E2E_DIR="$PROJECT_DIR/tests/e2e"

  # 有 E2E 脚本才检查
  if [ ! -d "$E2E_DIR" ]; then
    echo "  🟡 tests/e2e/ 目录不存在（无 E2E 测试）"
    WARNINGS=$((WARNINGS + 1))
    return
  fi
  local E2E_FILES=$(find "$E2E_DIR" -name "*.spec.*" -o -name "*.test.*" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$E2E_FILES" -eq 0 ]; then
    echo "  🟡 tests/e2e/ 无测试文件"
    return
  fi
  echo "  📊 E2E 测试文件: $E2E_FILES 个"

  # 截图 ≥3 张
  local SCREENSHOT_COUNT=0
  if [ -d "$QA_REPORTS" ]; then
    SCREENSHOT_COUNT=$(find "$QA_REPORTS" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
  fi
  if [ "$SCREENSHOT_COUNT" -lt 3 ]; then
    echo "  ❌ E2E 截图不足（$SCREENSHOT_COUNT 张，最低 3 张）— E2E 可能未完整执行"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ E2E 截图: $SCREENSHOT_COUNT 张"
  fi

  # 截图时间戳晚于 test-report.md
  local TEST_REPORT="$PROJECT_DIR/pipeline/8/test-report.md"
  if [ -f "$TEST_REPORT" ] && [ -d "$QA_REPORTS" ]; then
    local NEWER_COUNT=$(find "$QA_REPORTS" -name "*.png" -newer "$TEST_REPORT" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$NEWER_COUNT" -gt 0 ]; then
      echo "  ✅ 截图时间戳晚于 test-report.md（证明是本次执行）"
    else
      echo "  🟡 截图时间戳不晚于 test-report.md（可能是旧截图）"
      WARNINGS=$((WARNINGS + 1))
    fi
  fi

  # test-report.md 提及 E2E 结果
  if [ -f "$TEST_REPORT" ]; then
    if grep -qiE 'e2e|playwright|端到端' "$TEST_REPORT" 2>/dev/null; then
      echo "  ✅ 测试报告包含 E2E 执行结果"
    else
      echo "  ❌ 测试报告未提及 E2E 结果"
      ERRORS=$((ERRORS + 1))
    fi
  fi

  # 集成测试连接真实 DB（阶段8 也要检查）
  local INT_DIR="$PROJECT_DIR/tests/integration"
  if [ -d "$INT_DIR" ]; then
    local MOCK_COUNT=$(grep -rl "mock\|Mock\|@Mock\|jest.mock\|unittest.mock" "$INT_DIR" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$MOCK_COUNT" -gt 0 ]; then
      echo "  ❌ 集成测试中 $MOCK_COUNT 个文件使用了 mock（必须连接真实 DB）"
      ERRORS=$((ERRORS + 1))
    fi
  fi
}

# ─── 阶段9：交付验收深度检查 ───
check_acceptance_quality() {
  echo ""
  echo "🎯 检查交付验收质量"

  local REPORT="$PROJECT_DIR/pipeline/9/ACCEPTANCE-REPORT.md"
  if [ ! -f "$REPORT" ]; then
    return
  fi

  # 7项 checklist 全部勾选
  local CHECK_ITEMS=$(grep -cE '\[x\]|\[X\]|✅' "$REPORT" 2>/dev/null || echo 0)
  if [ "$CHECK_ITEMS" -lt 7 ]; then
    echo "  ❌ 验收 checklist 勾选不足（$CHECK_ITEMS 项，应全部 7 项）"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 验收 checklist: $CHECK_ITEMS 项已勾选"
  fi

  # 安全扫描
  local SEC_SCAN="$PROJECT_DIR/pipeline/9/security-scan.md"
  if [ -f "$SEC_SCAN" ] && [ -s "$SEC_SCAN" ]; then
    if grep -qiE '严重|critical|高危' "$SEC_SCAN" 2>/dev/null; then
      echo "  ❌ 安全扫描发现严重问题"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 安全扫描无严重问题"
    fi
  else
    echo "  🟡 security-scan.md 不存在（建议执行安全扫描）"
    WARNINGS=$((WARNINGS + 1))
  fi

  # 测试报告无 P0 遗留
  local TEST_REPORT="$PROJECT_DIR/pipeline/8/test-report.md"
  if [ -f "$TEST_REPORT" ]; then
    if grep -qiE 'P0.*未修复|P0.*失败|P0.*遗留' "$TEST_REPORT" 2>/dev/null; then
      echo "  ❌ 测试报告有 P0 遗留问题"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ 测试报告无 P0 遗留"
    fi
  fi

  # docs/ 归档完整（5 个过程文档）
  local DOCS_DIR="$PROJECT_DIR/docs"
  local REQUIRED_DOCS=("PRD.md" "CODE-MAP.md" "ARCHITECTURE.md" "QA-TEST-STRATEGY.md" "dev-log.md")
  local MISSING_DOCS=0
  for doc in "${REQUIRED_DOCS[@]}"; do
    if [ ! -f "$DOCS_DIR/$doc" ]; then
      echo "  🟡 docs/$doc 不存在"
      MISSING_DOCS=$((MISSING_DOCS + 1))
    fi
  done
  if [ "$MISSING_DOCS" -eq 0 ]; then
    echo "  ✅ docs/ 归档完整（5 个过程文档）"
  else
    echo "  🟡 docs/ 缺少 $MISSING_DOCS 个过程文档"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# ─── 阶段10：交互式文档检查 ───
check_interactive_docs() {
  echo ""
  echo "📚 检查交互式文档（阶段10）"

  local DOCS_DIR="$PROJECT_DIR/docs"
  local REQUIRED_HTML=(
    "README.html:80"
    "USER-GUIDE.html:120"
    "ARCHITECTURE.html:100"
    "DEPLOYMENT.html:80"
    "CONFIG-GUIDE.html:60"
  )
  local HTML_ERRORS=0

  for entry in "${REQUIRED_HTML[@]}"; do
    local FNAME=$(echo "$entry" | cut -d: -f1)
    local MIN_LINES=$(echo "$entry" | cut -d: -f2)
    local FPATH="$DOCS_DIR/$FNAME"

    if [ ! -f "$FPATH" ] || [ ! -s "$FPATH" ]; then
      echo "  ❌ docs/$FNAME 不存在"
      HTML_ERRORS=$((HTML_ERRORS + 1))
      continue
    fi

    local LINES=$(wc -l < "$FPATH" | tr -d ' ')
    if [ "$LINES" -lt "$MIN_LINES" ]; then
      echo "  ❌ docs/$FNAME 过短（${LINES}行，最低${MIN_LINES}行）"
      HTML_ERRORS=$((HTML_ERRORS + 1))
    else
      echo "  ✅ docs/$FNAME (${LINES}行)"
    fi

    # 包含交互式模态框
    local MODAL_COUNT=$(grep -c "modal-overlay\|modal" "$FPATH" 2>/dev/null || echo 0)
    if [ "$MODAL_COUNT" -lt 3 ]; then
      echo "  🟡 docs/$FNAME 交互式模态框不足（$MODAL_COUNT 个，建议 ≥3）"
      WARNINGS=$((WARNINGS + 1))
    fi

    # 包含 Mermaid 图表
    if ! grep -q "mermaid" "$FPATH" 2>/dev/null; then
      echo "  🟡 docs/$FNAME 缺少 Mermaid 图表"
      WARNINGS=$((WARNINGS + 1))
    fi

    # 包含锚点目录
    if ! grep -qE 'toc|目录|nav' "$FPATH" 2>/dev/null; then
      echo "  🟡 docs/$FNAME 缺少锚点目录"
      WARNINGS=$((WARNINGS + 1))
    fi

    # 禁止"详见xxx"跳转
    if grep -qE '详见|参见|见下方|见上文' "$FPATH" 2>/dev/null; then
      echo "  🟡 docs/$FNAME 包含跳转式写法（应直接放内容）"
      WARNINGS=$((WARNINGS + 1))
    fi
  done

  ERRORS=$((ERRORS + HTML_ERRORS))
}

# ─── 阶段7：测试审查前置检查 ───
check_test_review_prerequisite() {
  echo ""
  echo "🔒 检查测试审查前置条件"

  local TEST_REVIEW="$PROJECT_DIR/pipeline/7-test-review/test-review.md"
  if [ -f "$TEST_REVIEW" ] && [ -s "$TEST_REVIEW" ]; then
    echo "  ✅ test-review.md 存在（阶段7-test-review 已完成）"
  else
    echo "  ❌ test-review.md 不存在（必须先完成测试审查才能进入阶段7）"
    ERRORS=$((ERRORS + 1))
  fi
}


# ─── 新增阶段检查函数 ───

# 检查 UI/UX 设计产出（阶段1.7）
check_uiux_design() {
  echo ""
  echo "🎨 检查 UI/UX 设计产出"

  local DESIGN_FILE="$PROJECT_DIR/pipeline/1.7/UI-UX-DESIGN.md"
  if [ -f "$DESIGN_FILE" ]; then
    # 检查 8 个技术特性维度覆盖
    local DIMENSIONS=("技术栈适配" "设计系统" "组件设计" "响应式" "暗黑模式" "动效" "可访问性" "异常")
    for dim in "${DIMENSIONS[@]}"; do
      if grep -q "$dim" "$DESIGN_FILE" 2>/dev/null; then
        echo "  ✅ 技术特性维度已覆盖: $dim"
      else
        echo "  🟡 技术特性维度未明确提及: $dim"
        WARNINGS=$((WARNINGS + 1))
      fi
    done
  else
    echo "  🟡 UI-UX-DESIGN.md 不在 pipeline/1.7/ 目录（可能在 docs/）"
  fi
}

# 检查 HTML 原型交互性（阶段1.7）
check_html_prototype() {
  echo ""
  echo "🌐 检查 HTML 原型"

  local PROTO_FILE="$PROJECT_DIR/docs/ui-prototype.html"
  if [ ! -f "$PROTO_FILE" ]; then
    PROTO_FILE="$PROJECT_DIR/pipeline/1.7/ui-prototype.html"
  fi

  if [ -f "$PROTO_FILE" ]; then
    echo "  ✅ HTML 原型文件存在"

    # 检查非纯静态（有 script 标签）
    if grep -q '<script>' "$PROTO_FILE" 2>/dev/null || grep -q '<script ' "$PROTO_FILE" 2>/dev/null; then
      echo "  ✅ HTML 包含交互脚本"
    else
      echo "  ❌ HTML 为纯静态，缺少 <script> 交互"
      ERRORS=$((ERRORS + 1))
    fi

    # 检查响应式
    if grep -q 'viewport' "$PROTO_FILE" 2>/dev/null; then
      echo "  ✅ HTML 包含响应式 viewport"
    else
      echo "  ❌ HTML 缺少 viewport meta 标签"
      ERRORS=$((ERRORS + 1))
    fi

    # 检查 style 标签
    if grep -q '<style>' "$PROTO_FILE" 2>/dev/null || grep -q '<style ' "$PROTO_FILE" 2>/dev/null; then
      echo "  ✅ HTML 包含内联样式"
    else
      echo "  ❌ HTML 缺少内联样式"
      ERRORS=$((ERRORS + 1))
    fi
  else
    echo "  ❌ HTML 原型文件不存在"
    ERRORS=$((ERRORS + 1))
  fi
}

# 检查 PRD 反向细化质量（阶段1.8）
check_prd_refinement() {
  echo ""
  echo "📝 检查 PRD 反向细化质量"

  local REFINED_FILE="$PROJECT_DIR/pipeline/1.8/PRD-REFINED.md"
  if [ ! -f "$REFINED_FILE" ]; then
    REFINED_FILE="$PROJECT_DIR/PRD-REFINED.md"
  fi

  if [ -f "$REFINED_FILE" ]; then
    # 检查 4 个细化维度
    local DIMENSIONS=("交互细节" "边界情况" "文案规范" "异常处理")
    for dim in "${DIMENSIONS[@]}"; do
      if grep -q "\[UI/UX细化\].*$dim\|$dim" "$REFINED_FILE" 2>/dev/null; then
        echo "  ✅ 细化维度已覆盖: $dim"
      else
        echo "  ❌ 细化维度缺失: $dim"
        ERRORS=$((ERRORS + 1))
      fi
    done

    # 检查 [UI/UX细化] 标记
    local REFINEMENT_COUNT=$(grep -c '\[UI/UX细化\]' "$REFINED_FILE" 2>/dev/null || echo 0)
    if [ "$REFINEMENT_COUNT" -gt 0 ]; then
      echo "  ✅ 发现 $REFINEMENT_COUNT 处 [UI/UX细化] 标记"
    else
      echo "  ❌ 未发现 [UI/UX细化] 标记（细化内容未标记）"
      ERRORS=$((ERRORS + 1))
    fi

    # 检查 [待确认] 残留（阶段1.9应处理完毕）
    local PENDING_COUNT=$(grep -c '\[待确认\]' "$REFINED_FILE" 2>/dev/null || echo 0)
    if [ "$PENDING_COUNT" -gt 0 ]; then
      echo "  🟡 发现 $PENDING_COUNT 处 [待确认] 残留（需人工确认）"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo "  🟡 PRD-REFINED.md 不存在（可能在非中型/大型项目）"
  fi
}

# 检查功能点标签一致性
check_feature_tags() {
  echo ""
  echo "🏷️ 检查功能点标签"

  local TAGS_FILE="$PROJECT_DIR/pipeline/feature-tags.json"
  if [ -f "$TAGS_FILE" ]; then
    echo "  ✅ feature-tags.json 存在"

    # 检查 JSON 合法性
    if python3 -c "import json; json.load(open('$TAGS_FILE'))" 2>/dev/null; then
      echo "  ✅ JSON 格式合法"

      # 统计各状态数量
      local TOTAL=$(python3 -c "import json; d=json.load(open('$TAGS_FILE')); print(len(d.get('features',{})))" 2>/dev/null || echo 0)
      echo "  📊 功能点总数: $TOTAL"
    else
      echo "  ❌ JSON 格式不合法"
      ERRORS=$((ERRORS + 1))
    fi
  else
    echo "  🟡 feature-tags.json 不存在（首次运行阶段1.7后会自动创建）"
  fi
}

# 主逻辑：根据阶段号执行对应检查
case "$PHASE" in
  0)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_project_init
    ;;
  1)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    # 检查 PRD 是否使用 REQ-xxx 编号
    PRD_FILE="$PROJECT_DIR/pipeline/1/PRD.md"
    if [ -f "$PRD_FILE" ]; then
      REQ_COUNT=$(grep -cE 'REQ-[0-9]+' "$PRD_FILE" 2>/dev/null || echo 0)
      if [ "$REQ_COUNT" -eq 0 ]; then
        echo "  ❌ PRD.md 中未找到 REQ-xxx 编号（功能清单必须用 REQ-xxx 编号）"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ PRD.md 包含 $REQ_COUNT 处 REQ-xxx 编号"
      fi
    fi
    check_prd_quality
    ;;
  1.5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_cross_review_pm
    check_re_review "$PROJECT_DIR/pipeline/1.5/re-review-pm.md" "PRD复审" $(load_roles "REREVIEW_PM_ROLES" | tr '\n' ' ')
    ;;
  1.6)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_html_draft "$PROJECT_DIR/docs/prd-draft.html" "$PROJECT_DIR/pipeline/1.6/prd-feedback.md" "PRD"
    ;;
  1.7)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    # HTML 原型额外检查
    PROTO_SPEC=$(load_conf "PHASE_1.75_FILE" "")
    if [ -n "$PROTO_SPEC" ]; then
      PROTO_FILE_NAME=$(echo "$PROTO_SPEC" | cut -d: -f1)
      PROTO_MIN_L=$(echo "$PROTO_SPEC" | cut -d: -f2)
      # HTML 原型在 docs/ 目录
      OLD_PROJECT_DIR="$PROJECT_DIR"
      PROTO_PATH="$PROJECT_DIR/docs/$PROTO_FILE_NAME"
      if [ -f "$PROTO_PATH" ]; then
        LINES_PROTO=$(count_lines "$PROTO_PATH")
        echo "  📏 HTML原型有效行数: $LINES_PROTO (最低要求: $PROTO_MIN_L)"
        if [ "$LINES_PROTO" -lt "$PROTO_MIN_L" ]; then
          echo "  ❌ HTML原型行数不足"
          ERRORS=$((ERRORS + 1))
        else
          echo "  ✅ HTML原型行数达标"
        fi
      else
        echo "  ❌ HTML原型不存在: $PROTO_PATH"
        ERRORS=$((ERRORS + 1))
      fi
    fi
    check_uiux_design
    check_html_prototype
    check_feature_tags
    ;;
  1.8)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    # prd-diff.md 额外检查
    DIFF_FILE="$PROJECT_DIR/pipeline/1.8/prd-diff.md"
    if [ ! -f "$DIFF_FILE" ]; then
      DIFF_FILE="$PROJECT_DIR/prd-diff.md"
    fi
    if [ -f "$DIFF_FILE" ]; then
      echo "  ✅ prd-diff.md 存在"
    else
      echo "  ❌ prd-diff.md 不存在"
      ERRORS=$((ERRORS + 1))
    fi
    check_prd_refinement
    check_feature_tags
    ;;
  1.9)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    # 检查原始 PRD 备份
    BACKUP_FILE="$PROJECT_DIR/docs/PRD-original-backup.md"
    if [ -f "$BACKUP_FILE" ]; then
      echo "  ✅ 原始 PRD 备份存在"
    else
      echo "  🟡 原始 PRD 备份不存在（建议保留）"
      WARNINGS=$((WARNINGS + 1))
    fi
    # 检查 [待确认] 残留
    FINAL_PRD="$PROJECT_DIR/PRD.md"
    if [ -f "$FINAL_PRD" ]; then
      PENDING=$(grep -c '\[待确认\]' "$FINAL_PRD" 2>/dev/null || echo 0)
      if [ "$PENDING" -gt 0 ]; then
        echo "  ❌ 最终 PRD 仍有 $PENDING 处 [待确认] 残留"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ 最终 PRD 无 [待确认] 残留"
      fi
    fi
    check_feature_tags
    ;;
  2)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_architecture_outputs
    check_feature_tags
    ;;
  2.5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_cross_review_arch
    check_re_review "$PROJECT_DIR/pipeline/2.5/re-review-arch.md" "架构复审" $(load_roles "REREVIEW_ARCH_ROLES" | tr '\n' ' ')
    ;;
  2.6)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_html_draft "$PROJECT_DIR/docs/architecture-draft.html" "$PROJECT_DIR/pipeline/2.6/architecture-feedback.md" "架构"
    ;;
  2.8)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    # 检查 SPIKE-REPORT.md 存在且有结论
    SPIKE_REPORT="$PROJECT_DIR/pipeline/2.8/SPIKE-REPORT.md"
    if [ -f "$SPIKE_REPORT" ]; then
      SPIKE_LINES=$(count_lines "$SPIKE_REPORT")
      if [ "$SPIKE_LINES" -lt 10 ]; then
        echo "  ❌ SPIKE-REPORT.md 内容不足（$SPIKE_LINES 行）"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ SPIKE-REPORT.md 存在（$SPIKE_LINES 行）"
      fi
      # 检查是否有明确结论
      if grep -qiE '结论|通过|不通过|有条件' "$SPIKE_REPORT" 2>/dev/null; then
        echo "  ✅ SPIKE-REPORT.md 包含明确结论"
      else
        echo "  ❌ SPIKE-REPORT.md 缺少明确结论"
        ERRORS=$((ERRORS + 1))
      fi
    else
      echo "  ❌ SPIKE-REPORT.md 不存在: $SPIKE_REPORT"
      ERRORS=$((ERRORS + 1))
    fi
    ;;
  5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_traceability "5"
    check_task_list_quality
    # 检查 TASK-LIST.md 中的开发者字段使用合法 agent-id
    TASK_FILE="$PROJECT_DIR/pipeline/5/TASK-LIST.md"
    if [ -f "$TASK_FILE" ]; then
      echo ""
      echo "👤 检查任务分配（agent-id 合法性）"
      DEV_VALUES=$(grep -oE '\*\*开发者\*\*:\s*\S+' "$TASK_FILE" 2>/dev/null | sed 's/\*\*开发者\*\*:\s*//' | sort -u)
      INVALID_DEVS=""
      while IFS= read -r dv; do
        [ -z "$dv" ] && continue
        case "$dv" in
          dev1|dev2|dev3) ;;
          *) INVALID_DEVS="$INVALID_DEVS $dv" ;;
        esac
      done <<< "$DEV_VALUES"
      if [ -n "$INVALID_DEVS" ]; then
        echo "  ❌ 发现非法开发者标识:$INVALID_DEVS（应使用 dev1/dev2/dev3）"
        ERRORS=$((ERRORS + 1))
      else
        echo "  ✅ 开发者字段全部使用合法 agent-id"
      fi
    fi
    ;;
  5.5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_api_schema
    check_traceability "5.5"
    ;;
  6)
    check_code
    check_layered_architecture
    check_coverage
    check_tc_traceability
    check_input_references "6" "$PROJECT_DIR" "ARCHITECTURE" "CODE-MAP" "TASK-LIST"
    check_feature_tags
    # 集成测试目录检查
    INT_DIR="$PROJECT_DIR/tests/integration"
    if [ -d "$INT_DIR" ]; then
      INT_FILES=$(find "$INT_DIR" -name "*.test.*" -o -name "*Test.*" -o -name "test_*" 2>/dev/null | wc -l | tr -d ' ')
      if [ "$INT_FILES" -gt 0 ]; then
        echo "  ✅ tests/integration/ 存在（$INT_FILES 个测试文件）"
      else
        echo "  ❌ tests/integration/ 存在但无测试文件"
        ERRORS=$((ERRORS + 1))
      fi
    else
      echo "  ❌ tests/integration/ 不存在（必须有集成测试）"
      ERRORS=$((ERRORS + 1))
    fi
    ;;
  6.3)
    check_code_integration
    ;;
  6.5)
    check_dev_review
    ;;
  7)
    check_test_review_prerequisite
    check_security_scan
    check_review
    check_architecture_reference
    check_architecture_implementation
    check_input_references "7" "$PROJECT_DIR/pipeline/7/review-report.md" "ARCHITECTURE"
    check_re_review "$PROJECT_DIR/pipeline/7/re-review-code.md" "代码复审" $(load_roles "REREVIEW_CODE_ROLES" | tr '\n' ' ')
    ;;
  7-test-review)
    check_test_review
    check_tc_traceability
    ;;
  8)
    check_test
    check_coverage
    check_tc_traceability
    check_e2e_execution
    check_test_case_review
    check_traceability "8"
    check_feature_tags
    check_architecture_implementation
    if [ -f "$PROJECT_DIR/pipeline/8/tool-check.log" ]; then
      echo "  ✅ 测试工具检查日志存在"
    else
      echo "  🟡 测试工具检查日志不存在（建议运行 check-test-tools.sh）"
      WARNINGS=$((WARNINGS + 1))
    fi
    ;;
  8.5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_pm_acceptance
    ;;
  9)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_feature_tags
    check_deliverable_docs
    check_html_docs
    check_acceptance_quality
    ;;
  10)
    check_interactive_docs
    ;;
  *)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    else
      echo ""
      echo "⚠️ 阶段 $PHASE 没有定义检查规则，跳过文件检查。"
    fi
    ;;
esac

# 阶段2起检查 docs/ 归档
if [ "$PHASE" != "0" ] && [ "$PHASE" != "1" ] && [ "$PHASE" != "1.5" ]; then
  check_docs_archive
fi

# 每个阶段都检查沟通记录
check_communications

# 汇总结果
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 检查结果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ❌ 错误: $ERRORS"
echo "  🟡 警告: $WARNINGS"

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "  🔴 检查不通过！流程必须暂停。"
  echo "  协调者必须修复以上 $ERRORS 个错误后才能继续。"
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo ""
  echo "  🟡 有 $WARNINGS 个警告，建议修复但可继续。"
  exit 0
else
  echo ""
  echo "  ✅ 全部通过！可以进入下一阶段。"
  exit 0
fi
