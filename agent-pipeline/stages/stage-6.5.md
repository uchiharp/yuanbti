# 阶段6.5：开发审查（互审）

## 任务
各开发互相审查代码。

## 必读文件（强制）
1. docs/ARCHITECTURE.md（架构合规基准）
2. 被审查者的代码文件

## 加载 Skill
- `code-review-checklist`（审查维度清单）

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| cross-review-dev.md | 60 | 每个 reviewer 独立段落 ≥20行，每段 ≥3检查点 |

## 审查重点
- 代码是否符合架构方案中的分层、模块、模式选型
- 日志异常是否符合 `logging-exception` 规范
- SOLID 原则
- 设计模式使用

## 执行流程
1. 各 reviewer 加载 `code-review-checklist`
2. 先读 ARCHITECTURE.md，再读被审查代码
3. 对比代码 vs 架构文档
4. 产出评审意见 → 开发修改 → 确认

## 检查项（脚本强制）
- [ ] cross-review-dev.md 存在
- [ ] 每个 reviewer 有独立段落
- [ ] 每段 ≥3检查点
- [ ] 审查报告引用了架构相关内容

## 约束
- 1轮修复后仍不通过 → 升级到阶段7
