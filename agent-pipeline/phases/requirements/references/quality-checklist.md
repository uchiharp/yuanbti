# PRD 质量评分检查清单

## 评分规则

总分 60 分，12 项检查。

### 必检项（8项，共 40 分）

| # | 检查项 | 满分 | 扣分规则 |
|---|--------|------|---------|
| 1 | Executive Summary 存在且 50-200 词 | 5 | 缺失 0 分，过短/过长 3 分 |
| 2 | Problem Statement 含 User Impact | 5 | 缺失 0 分 |
| 3 | Problem Statement 含 Business Impact | 5 | 缺失 0 分 |
| 4 | Goals 有量化指标（SMART） | 5 | 有表格 5 分，有目标无表格 2 分 |
| 5 | System Overview 完整（模块+数据流+旅程） | 5 | 每少一个子章节 -2，全有 5 分 |
| 6 | User Stories 有验收标准（每故事≥3条） | 5 | ≥3 条 5 分，每少 1 条 -1 |
| 7 | REQ 编号存在且连续 | 5 | 连续 5 分，不连续 3 分 |
| 8 | REQ 模块归属覆盖率（≥80%） | 5 | ≥80% 5 分，≥50% 3 分，≥30% 1 分 |

### 质量项（2项，共 10 分）

| # | 检查项 | 满分 | 扣分规则 |
|---|--------|------|---------|
| 9 | 验收标准可测试（无模糊语言） | 5 | 模糊词每处 -1，最多 -5 |
| 10 | Out of Scope 已定义 | 5 | 缺失 0 分 |

### 加分项（2项，共 10 分）

| # | 检查项 | 满分 | 加分规则 |
|---|--------|------|---------|
| 11 | 非功能需求有量化目标 | 5 | 量化 5 分，有但模糊 2 分 |
| 12 | 每个 REQ 有 Task Breakdown Hints | 5 | ≥50% 覆盖 5 分，≥30% 2 分 |

## 评级标准

| 评级 | 分数范围 | 含义 |
|------|---------|------|
| EXCELLENT | ≥54 | 高质量 PRD，可直接进入设计 |
| GOOD | 45-53 | 质量良好，小修后可用 |
| ACCEPTABLE | 36-44 | 可接受，但建议补充关键章节 |
| NEEDS_WORK | <36 | 质量不达标，必须修改后重评 |

## 模糊词黑名单

以下词语出现在验收标准中会被扣分：
```
fast, secure, user-friendly, scalable, efficient, robust,
performant, reliable, easy, simple, quick, better, improved,
enhanced, optimized, flexible
```

**替代写法**：
- "fast" → "P95 响应时间 < 200ms"
- "secure" → "使用 RS256 签名，Token 有效期 8h"
- "scalable" → "支持 1000 QPS，水平扩展无需代码改动"
- "user-friendly" → "新用户 3 次点击内完成注册"
