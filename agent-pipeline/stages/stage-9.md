# 阶段9：交付验收（协调者）

## 任务
端到端验收，产出验收报告和交付文档。

## 必读文件
所有阶段产出物

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| ACCEPTANCE-REPORT.md | 50 | 验收报告（7项 checklist 全部 ✅） |
| docs/user-manual.md | 100 | 用户使用手册 |
| docs/api-docs.md | — | API 接口文档 |
| docs/rpc-api-docs.md | — | RPC 接口文档 |
| docs/integration-guide.md | — | 接入指南（必须含步骤说明） |

## 交付文档写作规则
- **必须在阶段7签收后才能写**（基于最终代码）
- 写完后开发确认准确性 + QA 验证可操作性
- 时限：4小时

## 检查项（脚本强制）
- [ ] ACCEPTANCE-REPORT.md 存在
- [ ] 7项验收 checklist 全部 ✅ 或 [x]
- [ ] 无 escalated 合同
- [ ] 安全扫描 0 严重问题
- [ ] 测试报告无 P0 遗留
- [ ] docs/ 归档完整（5个过程文档均存在）
- [ ] 交付文档齐全：
  - user-manual.md ≥100行
  - api-docs.md 存在
  - rpc-api-docs.md 存在
  - integration-guide.md 含步骤说明

## 约束
- 通过 → 输出"项目交付完成"
- 不通过 → 输出缺失项，协调者修复后重检
- 知识库：更新 CONTEXT.md 阶段9段落，存入 MemPalace room=project-lessons
