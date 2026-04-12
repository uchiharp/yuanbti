# TOOLS.md - QA·评审官

## Playwright 实操审查

```bash
npx playwright test            # 运行测试验证
npx playwright test -g "名称"   # 运行指定用例
npx playwright test --ui        # 调试模式
```

## 环境检查

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000   # 前端
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080   # 后端
```

## 项目信息（由协调者传入）

- **被审查agent：** QA
- **项目路径：** {协调者指定}
- **产出路径：** {协调者指定}

## 审查标准

详见 qa-review-workflow skill（templates/REVIEW-STANDARDS.md）
