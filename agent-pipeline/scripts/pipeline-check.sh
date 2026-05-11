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
    1.5) echo "cross-review-pm.md:50" ;;
    2) echo "ARCHITECTURE.md:100" ;;
    2.5) echo "cross-review-arch.md:40" ;;
    3) echo "UX-DESIGN.md:80" ;;
    3.5) echo "cross-review-ux-to-ui.md:20" ;;
    4) echo "UI-DESIGN.md:80" ;;
    4.5) echo "cross-review-ui-to-ux.md:20" ;;
    5) echo "TASK-LIST.md:50" ;;
    # test-plan.md 由 QA 产出，单独检查
    # TEST-PLAN.md 在 TASK-LIST.md 同目录，最小30行
    5.5) echo "confirm-tasks.md:20" ;;
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

  # 检查QA测试脚本（阶段6 QA同步产出）
  local TESTS_DIR="$PROJECT_DIR/tests"
  if [ -d "$TESTS_DIR" ]; then
    local TEST_FILES=$(find "$TESTS_DIR" -name "*.spec.*" -o -name "*.test.*" | wc -l | tr -d ' ')
    echo "  E2E测试文件数: $TEST_FILES"
    if [ "$TEST_FILES" -eq 0 ]; then
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

check_review() {
  echo ""
  echo "📊 检查审查报告"

  local REVIEW_FILE="$PROJECT_DIR/7/review-report.md"
  local SCREENSHOTS_DIR="$PROJECT_DIR/7/screenshots"

  if [ ! -f "$REVIEW_FILE" ] || [ ! -s "$REVIEW_FILE" ]; then
    echo "  ❌ 审查报告不存在或为空"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ 审查报告存在"
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
  case "$PHASE" in 2.5|2.8|3|3.5|4|4.5|5|5.5|6|6.3|6.5|7|8|9)
    if [ ! -f "$DOCS_DIR/CODE-MAP.md" ]; then
      echo "  ❌ docs/CODE-MAP.md 不存在（阶段2开始前应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/CODE-MAP.md"
    fi
  esac

  # ARCHITECTURE.md（阶段2.8起）
  case "$PHASE" in 2.8|3|3.5|4|4.5|5|5.5|6|6.3|6.5|7|8|9)
    if [ ! -f "$DOCS_DIR/ARCHITECTURE.md" ]; then
      echo "  ❌ docs/ARCHITECTURE.md 不存在（阶段2签收后应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/ARCHITECTURE.md"
    fi
  esac

  # QA-TEST-STRATEGY.md（阶段5.5起）
  case "$PHASE" in 5.5|6|6.3|6.5|7|8|9)
    if [ ! -f "$DOCS_DIR/QA-TEST-STRATEGY.md" ]; then
      echo "  ❌ docs/QA-TEST-STRATEGY.md 不存在（阶段5签收后应归档）"
      ERRORS=$((ERRORS + 1))
    else
      echo "  ✅ docs/QA-TEST-STRATEGY.md"
    fi
  esac

  # dev-log.md（阶段7起）
  case "$PHASE" in 7|8|9)
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
    echo "     架构评审官必须先读 docs/ARCHITECTURE.md，再对比代码审查"
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

# 主逻辑：根据阶段号执行对应检查
case "$PHASE" in
  6)
    check_code
    check_layered_architecture
    check_input_references "6" "$PROJECT_DIR/6" "ARCHITECTURE" "CODE-MAP" "TASK-LIST"
    ;;
  7)
    check_review
    check_architecture_reference
    check_input_references "7" "$PROJECT_DIR/7/review-report.md" "ARCHITECTURE"
    ;;
  8)
    check_test
    ;;
  9)
    PHASE_SPEC=$(get_phase_file "$PHASE")
    if [ -n "$PHASE_SPEC" ]; then
      FILE_NAME=$(echo "$PHASE_SPEC" | cut -d: -f1)
      MIN_L=$(echo "$PHASE_SPEC" | cut -d: -f2)
      check_file "$FILE_NAME" "$MIN_L"
    fi
    check_deliverable_docs
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
