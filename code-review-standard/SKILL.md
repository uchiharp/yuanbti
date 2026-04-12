# code-review-standard — 统一代码审查标准

## 是什么

为 reviewer agent 提供统一的代码审查标准、安全扫描模板和 Playwright 审查工作流。所有 reviewer 共用同一套标准，确保审查质量一致。

**本 skill 无任何外部依赖，可独立使用。**

## 触发条件

- reviewer agent 执行代码审查
- 安全扫描
- Playwright E2E 测试审查

## 使用场景

- 流水线中 reviewer 审查代码交付
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
