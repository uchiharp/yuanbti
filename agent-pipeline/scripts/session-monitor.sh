#!/bin/bash
# session-monitor.sh — 流水线 Session 监控面板
# 用法:
#   ./session-monitor.sh                    # 查看所有 session
#   ./session-monitor.sh <项目名>           # 查看项目 session 状态
#   ./session-monitor.sh <项目名> init      # 创建项目所有 agent session
#   ./session-monitor.sh <项目名> close     # 关闭项目所有 agent session
#   ./session-monitor.sh <项目名> close-all # 关闭并删除项目所有 session

set -eo pipefail

PROJECT="${1:-}"
ACTION="${2:-status}"
AGENTS_ROOT="${AGENTS_ROOT:-/Users/sunwenyong/.openclaw/agents}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📡 Pipeline Session Monitor"
echo "   $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 所有已知 agent
AGENTS=(
  "pm"
  "architect"
  "dev1"
  "dev2"
  "dev3"
  "qa"
  "ux-tester"
  "ui-designer"
)

# Agent 目录映射
get_agent_cwd() {
  case "$1" in
    pm) echo "$AGENTS_ROOT/pm/workspace" ;;
    architect) echo "$AGENTS_ROOT/architect/workspace" ;;
    dev1) echo "$AGENTS_ROOT/dev1/workspace" ;;
    dev2) echo "$AGENTS_ROOT/dev2/workspace" ;;
    dev3) echo "$AGENTS_ROOT/dev3/workspace" ;;
    qa) echo "$AGENTS_ROOT/qa/workspace" ;;
    ux-tester) echo "$AGENTS_ROOT/ux-tester/workspace" ;;
    ui-designer) echo "$AGENTS_ROOT/ui-designer/workspace" ;;
    *) echo "" ;;
  esac
}

# ─── init: 创建项目所有 session ───
if [ "$ACTION" = "init" ] && [ -n "$PROJECT" ]; then
  echo ""
  echo "🚀 创建项目 [$PROJECT] 的所有 Agent Session"
  echo "─────────────────────────────────────────"
  CREATED=0
  SKIPPED=0
  FAILED=0

  for AGENT in "${AGENTS[@]}"; do
    SESSION_NAME="${PROJECT}-${AGENT}"
    AGENT_CWD=$(get_agent_cwd "$AGENT")

    if [ -z "$AGENT_CWD" ]; then
      echo "  ⚠️  $AGENT — 未知 agent，跳过"
      SKIPPED=$((SKIPPED + 1))
      continue
    fi

    # 检查是否已存在
    EXISTS=$(acpx claude sessions show "$SESSION_NAME" 2>&1 || true)
    if ! echo "$EXISTS" | grep -qi "not found\|no session\|error"; then
      echo "  ⏭️  $AGENT — session 已存在: $SESSION_NAME"
      SKIPPED=$((SKIPPED + 1))
      continue
    fi

    # 创建 session
    RESULT=$(acpx claude --session "$SESSION_NAME" --cwd "$AGENT_CWD" sessions new 2>&1 || true)
    if echo "$RESULT" | grep -qi "created\|success\|new session"; then
      echo "  ✅ $AGENT — session 创建成功: $SESSION_NAME"
      CREATED=$((CREATED + 1))
    else
      echo "  ❌ $AGENT — 创建失败: $RESULT"
      FAILED=$((FAILED + 1))
    fi
  done

  echo ""
  echo "📊 结果: 创建 $CREATED | 跳过 $SKIPPED | 失败 $FAILED"
  exit 0
fi

# ─── close: 关闭项目所有 session ───
if [ "$ACTION" = "close" ] && [ -n "$PROJECT" ]; then
  echo ""
  echo "🔒 关闭项目 [$PROJECT] 的所有 Agent Session"
  echo "─────────────────────────────────────────"
  CLOSED=0
  NOT_FOUND=0

  for AGENT in "${AGENTS[@]}"; do
    SESSION_NAME="${PROJECT}-${AGENT}"
    RESULT=$(acpx claude --session "$SESSION_NAME" sessions close 2>&1 || true)
    if echo "$RESULT" | grep -qi "closed\|success"; then
      echo "  ✅ $AGENT — session 已关闭: $SESSION_NAME"
      CLOSED=$((CLOSED + 1))
    else
      echo "  ⏭️  $AGENT — session 不存在或已关闭"
      NOT_FOUND=$((NOT_FOUND + 1))
    fi
  done

  echo ""
  echo "📊 结果: 关闭 $CLOSED | 未找到 $NOT_FOUND"
  exit 0
fi

# ─── close-all: 关闭并删除项目所有 session ───
if [ "$ACTION" = "close-all" ] && [ -n "$PROJECT" ]; then
  echo ""
  echo "🗑️  删除项目 [$PROJECT] 的所有 Agent Session"
  echo "─────────────────────────────────────────"
  DELETED=0
  NOT_FOUND=0

  for AGENT in "${AGENTS[@]}"; do
    SESSION_NAME="${PROJECT}-${AGENT}"
    # 关闭 session
    RESULT=$(acpx claude --session "$SESSION_NAME" sessions close 2>&1 || true)
    if echo "$RESULT" | grep -qi "closed\|success\|deleted"; then
      echo "  🗑️  $AGENT — session 已删除: $SESSION_NAME"
      DELETED=$((DELETED + 1))
    else
      echo "  ⏭️  $AGENT — session 不存在"
      NOT_FOUND=$((NOT_FOUND + 1))
    fi
  done

  echo ""
  echo "📊 结果: 删除 $DELETED | 未找到 $NOT_FOUND"
  exit 0
fi

# ─── status: 显示 session 状态（默认）───

# 1. 列出所有 Claude session
echo ""
echo "📋 所有 Claude Sessions:"
echo "─────────────────────────────────────────"
ALL_SESSIONS=$(acpx claude sessions list 2>&1 || true)
if [ "$ALL_SESSIONS" = "No sessions" ] || [ -z "$ALL_SESSIONS" ]; then
  echo "  (无活跃 session)"
else
  echo "$ALL_SESSIONS"
fi

# 2. 如果指定了项目，检查每个 agent 的 session 状态
if [ -n "$PROJECT" ]; then
  echo ""
  echo "🔍 项目 [$PROJECT] 的 Agent Session:"
  echo "─────────────────────────────────────────"
  printf "  %-25s %-15s %-10s %s\n" "AGENT" "SESSION" "STATUS" "PID"
  echo "  ───────────────────── ─────────────── ────────── ──────────"

  for AGENT in "${AGENTS[@]}"; do
    SESSION_NAME="${PROJECT}-${AGENT}"
    STATUS="❌ 未创建"
    PID="—"

    # 检查 session 是否存在
    SESSION_INFO=$(acpx claude sessions show "$SESSION_NAME" 2>&1 || true)

    if echo "$SESSION_INFO" | grep -qi "not found\|no session\|error"; then
      STATUS="❌ 未创建"
    else
      # 检查进程状态
      PROC_STATUS=$(acpx claude status -s "$SESSION_NAME" 2>&1 || true)
      if echo "$PROC_STATUS" | grep -qi "running\|active\|alive"; then
        STATUS="🟢 运行中"
        PID=$(echo "$PROC_STATUS" | grep -oE 'pid[=:]?\s*[0-9]+' | grep -oE '[0-9]+' || echo "—")
      elif echo "$PROC_STATUS" | grep -qi "idle\|waiting\|standby"; then
        STATUS="🟡 空闲"
      elif echo "$PROC_STATUS" | grep -qi "stopped\|closed\|dead"; then
        STATUS="🔴 已停止"
      else
        STATUS="⚪ 已创建"
      fi
    fi

    printf "  %-25s %-15s %-10s %s\n" "$AGENT" "$SESSION_NAME" "$STATUS" "$PID"
  done
fi

# 3. 系统级 session 概览
echo ""
echo "📊 概览:"
echo "─────────────────────────────────────────"

TOTAL=$(echo "$ALL_SESSIONS" | grep -c . 2>/dev/null || echo 0)
if [ "$ALL_SESSIONS" = "No sessions" ] || [ -z "$ALL_SESSIONS" ]; then
  TOTAL=0
fi

echo "  活跃 session 总数: $TOTAL"

if [ -n "$PROJECT" ]; then
  PROJECT_SESSIONS=$(echo "$ALL_SESSIONS" | grep -c "$PROJECT" 2>/dev/null || echo 0)
  echo "  项目 [$PROJECT] session: $PROJECT_SESSIONS / ${#AGENTS[@]}"
fi

# 4. 快捷命令提示
echo ""
echo "💡 快捷命令:"
echo "─────────────────────────────────────────"
echo "  创建项目 session:  $0 <项目名> init"
echo "  关闭项目 session:  $0 <项目名> close"
echo "  查看 session 历史:  acpx claude sessions history <session-name>"
echo ""
