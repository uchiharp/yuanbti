# 阶段7：代码审查（QA评审官 + 架构评审官）

## 任务
QA 评审官做业务+健壮性验证，架构评审官做架构合规验证。

## 必读文件（审查前必须先读，强制）
1. docs/ARCHITECTURE.md（架构合规基准）
2. dev/ 代码
3. tests/ 测试脚本

## 加载 Skill
| 角色 | Skill |
|------|-------|
| QA评审官 | `qa-workflow`, `humanize-code`, `logging-exception` |
| 架构评审官 | `code-review-checklist`, `logging-exception` |

## 产出物
| 文件 | 说明 |
|------|------|
| review-report.md | 两个评审官各有独立段落，每段 ≥3检查点 + ≥1建议 + 评分 |
| screenshots/ | Playwright 截图 ≥1张 |

## 执行流程

### QA评审官
1. 加载 `qa-workflow` + `humanize-code` + `logging-exception`
2. Playwright 实操验证
3. 业务逻辑验证 + 健壮性测试 + 去AI味检查 + 日志异常规范检查

### 架构评审官
1. **先读 docs/ARCHITECTURE.md**（这是审查基准）
2. 加载 `code-review-checklist` + `logging-exception`
3. **对比代码 vs 架构文档**：
   - 分层是否合规（Controller→Service→Repository）
   - 模块是否按方案隔离
   - 模式是否按方案使用
   - 日志异常是否符合规范
4. 可读性 + 可维护性 + 去AI味

## 检查项（脚本强制）
- [ ] review-report.md 存在
- [ ] 两个评审官各有独立段落
- [ ] 每段 ≥3检查点 + ≥1建议 + 评分
- [ ] screenshots/ 存在且含截图 ≥1
- [ ] 审查报告引用了架构相关内容（架构/分层/Controller/Service/Repository/模块/模式）
- [ ] 合同轮次 ≤3
- [ ] 回退总额度 ≤5

## 约束
- 合同：🔴高风险 完整合同 最多3轮
- 打回 → 开发修改 → 重新检查（最多3轮）
- 超限 → escalated → 协调者汇报用户
- 通过 → 推进阶段8
