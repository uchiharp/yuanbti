# HEARTBEAT.md — 创业助手定期检查

## Agent 质量巡检（每次心跳执行）

检查各 agent 的工作质量，发现异常及时处理。

### 1. Code Review 质量检查
- 读取 `/agents/code-review/workspace/memory/review-log.md`
- 统计近期：Accept率、平均轮次、漏审率（来自QA反馈）
- 异常阈值：
  - 漏审率 ≥ 20% → 通知 code-review agent 写复盘
  - Accept率 > 90% → 提醒 PM 关注是否太松
  - Accept率 < 40% → 提醒 PM 关注是否太严
  - 连续3轮Reject > 30% → 介入协调

### 2. QA 测试质量检查
- 读取 `/agents/qa/workspace/memory/` 最近的测试报告
- 检查：P0/P1发现率、review-miss标记
- 异常：QA连续2轮没发现问题，但UX Tester发现问题 → QA可能漏测

### 3. PM 流程质量检查
- 读取 `/agents/pm/workspace/memory/` 最近的PRD
- 检查：PRD是否被下游多次打回（打回率高说明PRD质量差）

### 4. 开发交付质量检查
- 统计 Frontend/Backend 被code-review打回的频率
- 被QA打回的频率
- 异常：某个agent频繁被所有环节打回 → 可能需要调整该agent

### 5. 异常报告接收
检查各 agent 的 `memory/` 目录是否有 `escalation.md` 或类似文件
- 有 → 读取并处理（协调/通知相关agent）
- 处理完 → 归档

## 6. 任务计划清理

每次心跳执行：
```bash
# 清理超过15天的已完成/已取消的任务计划
find workspace/task-plans/ -name "*.md" -mtime +15 -delete
```

检查是否有 `🔄 进行中` 的计划但对应 Agent 已经不存在（超时/被kill）：
- 有 → 标记 `❌ 中断`，下次启动时提醒用户

## 执行频率
- Code Review质量：每次心跳检查
- 其他agent质量：每2-3次心跳轮换检查
- 异常报告：每次心跳检查
