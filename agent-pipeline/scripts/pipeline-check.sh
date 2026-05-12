#!/bin/bash
# pipeline-check.sh — 开发流水线防偷懒检查脚本
# 用法：./pipeline-check.sh <项目目录> <阶段编号>
# 协调者无法绕过此脚本，检查不通过 = 流程暂停
# 兼容 macOS bash 3.x

set -eo pipefail

PROJECT_DIR="$1"
PHASE="$2"

if [ -z "$PROJECT_DIR" ] || [ -z "$PHASE" ]; then
  echo "用法: $0 <项目目录> <阶段编号>"
  echo "示例: $0 .contracts/my-app 1"
  exit 1
fi

ERRORS=0
WARNINGS=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 流水线检查 | 阶段 $PHASE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 获取阶段对应的文件名和最小行数
get_phase_file() {
  case "$1" in
    0) echo "PROJECT-PLAN.md:30" ;;
    1) echo "PRD.md:200" ;;
    1.6) echo "prd-feedback.md:10" ;;
    1.5) echo "cross-review-pm.md:50" ;;
    2) echo "ARCHITECTURE.md:100" ;;
    2.5) echo "cross-review-arch.md:40" ;;
    2.6) echo "architecture-feedback.md:10" ;;
    3) echo "UX-DESIGN.md:80" ;;
    3.5) echo "cross-review-ux-to-ui.md:20" ;;
    4) echo "UI-DESIGN.md:80" ;;
    4.5) echo "cross-review-ui-to-ux.md:20" ;;
    5) echo "TASK-LIST.md:50" ;;
    # test-plan.md 由 QA 产出，单独检查
    # TEST-PLAN.md 在 TASK-LIST.md 同目录，最小30行
    5.5) echo "confirm-tasks.md:20" ;;
    8.5) echo "pm-acceptance.md:30" ;;
    9) echo "ACCEPTANCE-REPORT.md:50" ;;
    # health-dashboard.md 由协调者维护，单独检查
    *) echo "" ;;
  esac
}

# 检查单个文件
check_file() {
  local FILE="$1"
  local MIN_LINES="$2"
  local FULL_PATH="$PROJECT_DIR/$PHASE/$FILE"

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

  LINES=$(wc -l < "$FULL_PATH" | tr -d ' ')
  echo "  ✅ 文件存在"
  echo "  📏 行数: $LINES (最低要求: $MIN_LINES)"

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

  local CODE_DIR="$PROJECT_DIR/6"
  if [ ! -d "$CODE_DIR" ]; then
    echo "  ❌ 阶段6目录不存在: $CODE_DIR"
    ERRORS=$((ERRORS + 1))
    return
  fi

  local CODE_FILES=$(find "$CODE_DIR" \( -name "*.ts" -o -name "*.java" -o -name "*.vue" -o -name "*.js" -o -name "*.py" -o -name "*.sql" -o -name "*.xml" \) -type f 2>/dev/null | wc -l | tr -d ' ')

  echo "  代码文件数: $CODE_FILES"

  if [ "$CODE_FILES" -eq 0 ]; then
    echo "  ❌ 没有找到任何代码文件"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 找到代码文件"
  fi

  # 检查进度文件（逐任务调度产出）
  local PROGRESS_FILE="$PROJECT_DIR/6/progress.json"
  if [ -f "$PROGRESS_FILE" ]; then
    local COMPLETED=$(python3 -c "import json; d=json.load(open('$PROGRESS_FILE')); print(sum(1 for v in d.values() if isinstance(v,dict) and v.get('status')=='completed'))" 2>/dev/null || echo 0)
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
  local TASK_REPORTS_DIR="$PROJECT_DIR/6/task-reports"
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

  local REVIEW_FILE="$PROJECT_DIR/1.5/cross-review-pm.md"

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

  # 检查四个角色的段落
  local ROLES=("架构师" "QA" "开发1" "开发2")
  for role in "${ROLES[@]}"; do
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
  done
}

# 架构交叉评审检查（阶段 2.5）
check_cross_review_arch() {
  echo ""
  echo "📊 检查架构交叉评审"

  local REVIEW_FILE="$PROJECT_DIR/2.5/cross-review-arch.md"

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

  # 检查四个角色的段落
  local ROLES=("开发1" "开发2" "QA" "PM")
  for role in "${ROLES[@]}"; do
    if grep -qE "^##.*${role}" "$REVIEW_FILE" 2>/dev/null; then
      echo "  ✅ ${role} 评审段落存在"
      # 检查该段落的检查点数量（## 到下一个 ## 之间）
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
  done
}

check_review() {
  echo ""
  echo "📊 检查审查报告"

  local REVIEW_FILE="$PROJECT_DIR/7/review-report.md"
  local SCREENSHOTS_DIR="$PROJECT_DIR/7/screenshots"
  local TASK_REVIEWS_DIR="$PROJECT_DIR/7/task-reviews"

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

  local REVIEW_FILE="$PROJECT_DIR/8/test-case-review.md"

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

  local REVIEW_FILE="$PROJECT_DIR/3/ux-review.md"

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

  local REVIEW_FILE="$PROJECT_DIR/4/ui-review.md"

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

  local TEST_FILE="$PROJECT_DIR/8/test-report.md"

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
  case "$PHASE" in 2.5|2.8|3|3.5|4|4.5|5|5.5|6|6.3|6.5|7|8|8.5|9)
    if [ ! -f "$DOCS_DIR/CODE-MAP.md" ]; then
      echo "  ❌ docs/CODE-MAP.md 不存在（阶段2开始前应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/CODE-MAP.md"
    fi
  esac

  # ARCHITECTURE.md（阶段2.8起）
  case "$PHASE" in 2.8|3|3.5|4|4.5|5|5.5|6|6.3|6.5|7|8|8.5|9)
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

  local TEST_REVIEW_DIR="$PROJECT_DIR/7/test-reviews"
  local TEST_REVIEW_FILE="$PROJECT_DIR/7/test-review.md"

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

  local REVIEW_FILE="$PROJECT_DIR/7/review-report.md"
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

# 开发产出分层架构检查（阶段6）
check_layered_architecture() {
  echo ""
  echo "🏗️ 检查分层架构（阶段6）"

  local CODE_DIR="$PROJECT_DIR/6"
  if [ ! -d "$CODE_DIR" ]; then
    echo "  ⚠️ 代码目录不存在，跳过分层检查"
    return
  fi

  local VIOLATIONS=0

  # Controller 是否直接 import Repository/Mapper
  local CONTROLLER_FILES=$(find "$CODE_DIR" -name "*Controller*" -type f 2>/dev/null)
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
  local SERVICE_FILES=$(find "$CODE_DIR" -name "*Service*" -type f 2>/dev/null)
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

  local ACCEPTANCE_FILE="$PROJECT_DIR/8.5/pm-acceptance.md"
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

  local API_FILE="$PROJECT_DIR/5.5/api-schema.md"
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

# 主逻辑：根据阶段号执行对应检查
case "$PHASE" in
  6)
    check_code
    check_layered_architecture
    check_input_references "6" "$PROJECT_DIR/6" "ARCHITECTURE" "CODE-MAP" "TASK-LIST"
    ;;
  5.5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_api_schema
    ;;
  1.5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_cross_review_pm
    check_re_review "$PROJECT_DIR/1.5/re-review-pm.md" "PRD复审" "架构师" "QA" "开发1" "开发2"
    ;;
  2.5)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_cross_review_arch
    check_re_review "$PROJECT_DIR/2.5/re-review-arch.md" "架构复审" "开发1" "开发2" "QA" "PM"
    ;;
  3)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_ux_review
    check_re_review "$PROJECT_DIR/3/re-review-ux.md" "UX复审" "PM"
    ;;
  4)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_ui_review
    check_re_review "$PROJECT_DIR/4/re-review-ui.md" "UI复审" "PM" "开发"
    ;;
  7)
    check_review
    check_architecture_reference
    check_input_references "7" "$PROJECT_DIR/7/review-report.md" "ARCHITECTURE"
    check_re_review "$PROJECT_DIR/7/re-review-code.md" "代码复审" "架构师" "QA" "PM" "开发2"
    ;;
  7-test-review)
    check_test_review
    ;;
  1.6)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_html_draft "$PROJECT_DIR/docs/prd-draft.html" "$PROJECT_DIR/1.6/prd-feedback.md" "PRD"
    ;;
  2.6)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_html_draft "$PROJECT_DIR/docs/architecture-draft.html" "$PROJECT_DIR/2.6/architecture-feedback.md" "架构"
    ;;
  8)
    check_test
    check_test_case_review
    # 检查测试工具是否已检查
    if [ -f "$PROJECT_DIR/8/tool-check.log" ]; then
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
    check_deliverable_docs
    check_html_docs
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
