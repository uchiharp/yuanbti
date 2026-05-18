# {项目名} — 产品需求文档

## 1. Executive Summary
{2-3 句：核心问题 + 解决方案 + 预期影响}

## 2. Problem Statement
### Current Situation
{现状描述}

### User Impact
{谁受影响、具体痛点、严重程度+证据}

### Business Impact
{量化成本、机会成本、战略重要性}

## 3. Goals & Success Metrics
| 目标 | Metric | Baseline | Target | Timeframe |
|------|--------|----------|--------|-----------|
| {目标1} | {度量} | {基线} | {目标值} | {时间} |

## 4. System Overview
### 模块关系图
{模块A} ↔ {模块B} ↔ {模块C}

### 核心数据流
{起点} → {处理} → {终点}

### 用户旅程地图
{角色A}: {步骤1} → {步骤2} → {步骤3}
{角色B}: {步骤1} → {步骤2} → {步骤3}

## 5. User Stories
- As a [role], I want [feature], so that [benefit]
  - Acceptance Criteria:
    - {正常场景} → {预期结果}
    - {异常场景} → {预期结果}
    - {边界场景} → {预期结果}
- As a [role], I want [feature], so that [benefit]
  - Acceptance Criteria:
    - ...

## 6. 功能需求（REQ-xxx 编号，强制）

### REQ-001: {功能名称}
**优先级**: P0/P1/P2
**描述**: {1-3 句话}
**验收标准**:
- {正常场景} → {预期结果}
- {异常场景} → {预期结果}
**模块**: {所属模块名，对应 System Overview 中的模块}
**关联故事**: {对应用户故事简述}
**UI/UX**（中型+才有）:
- 交互流程：{步骤}
- 状态：{空/加载/成功/失败}
- 组件：{组件名列表}
**Task Breakdown Hints**:
- 实现 [组件/功能]: Small (2-4h)
- 添加 [功能]: Medium (4-8h)
**Dependencies**: None / REQ-xxx

### REQ-002: {功能名称}
{同上格式}

## 7. 非功能需求
| 类型 | 指标 | 目标值 |
|------|------|--------|
| 性能 | {P95响应时间/QPS} | {量化值} |
| 安全 | {认证/加密/审计} | {具体要求} |
| 可用性 | {SLA/RTO/RPO} | {量化值} |
| 可扩展性 | {数据量/并发} | {量化值} |

## 8. 技术考量
- 系统架构概览
- 技术栈偏好/强制要求
- 外部依赖
- 迁移策略（如有）

## 9. 实施路线图
| Phase | 包含 REQ | 验证检查点 | 工时估算 |
|-------|---------|-----------|---------|

## 10. Out of Scope
明确列出不在本期范围内的功能及原因。

## 11. Open Questions & Risks
| 问题/风险 | Owner | 影响 | 截止日期 |
|-----------|-------|------|---------|

## 12. Validation Checkpoints
每个 Phase 的验收标准。

## 13. Appendix: Task Breakdown
- 可并行的任务组
- 关键路径
- Risk Buffer (+20%)
