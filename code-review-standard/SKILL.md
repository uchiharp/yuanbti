# code-review-standard — 统一代码审查标准

## 是什么

为任何执行代码审查的角色提供统一的审查标准、安全扫描模板和 Playwright 审查工作流。开发互审、架构师审查、QA 审查均可使用，确保审查质量一致。

**本 skill 无任何外部依赖，可独立使用。**

## 触发条件

- 任何角色执行代码审查（开发互审、架构师审查、QA审查等）
- 安全扫描
- Playwright E2E 测试审查

## 使用场景

- 流水线中交叉代码审查
- 安全审计
- E2E 测试脚本审查

## 执行流程

```
1. 确定审查类型（代码审查/安全扫描/Playwright审查）
2. 读取对应模板：
   - 代码审查 → templates/REVIEW-STANDARDS.md
   - 安全扫描 → templates/SECURITY-SCAN.md
   - Playwright审查 → templates/PLAYWRIGHT-WORKFLOW.md
3. 按模板执行审查
4. 输出审查报告（评分 + 问题清单）
```

## 文件说明

| 文件 | 内容 | 行数 |
|------|------|------|
| `templates/REVIEW-STANDARDS.md` | 统一代码审查标准 | 382行 |
| `templates/SECURITY-SCAN.md` | 安全扫描模板 | 392行 |
| `templates/PLAYWRIGHT-WORKFLOW.md` | Playwright E2E 审查工作流 | 256行 |

## 质量门槛

- 总评 ≥ 7.0 才可签收
- 🔴 阻断问题必须为 0
- 安全扫描中发现的 🔴 问题必须在打回中明确标注

## 原则

**这份标准是你的最低要求，不是全部要求。你必须自由发挥，关注标准之外的任何问题。**
