# 阶段5.5：任务分解确认

## 任务
各开发确认分配的任务合理性。

## 必读文件
1. TASK-LIST.md
2. ARCHITECTURE.md

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| confirm-tasks.md | 20 | 每个开发者的确认段落 |
| api-schema.md | 30 | 接口契约（API 路径、请求/响应格式、错误码） |

## 执行流程
1. 协调者并发调度各开发 agent
2. 各开发确认任务合理性 → 1轮复核
3. 各开发根据任务分工，定义自己负责的 API 接口（路径、请求体、响应体、错误码）
4. 汇总产出 api-schema.md（统一接口文档）
5. QA 基于 api-schema.md 写 E2E 测试（阶段6并行时使用）

## 检查项（脚本强制）
- [ ] confirm-tasks.md 存在且 ≥20行
- [ ] 包含每个开发者的确认段落
- [ ] api-schema.md 存在且 ≥30行
- [ ] api-schema.md 包含 API 路径定义（至少3个接口）

## 约束
- 无合同限制
- 此阶段通过后，QA-TEST-STRATEGY.md 应归档到 docs/
