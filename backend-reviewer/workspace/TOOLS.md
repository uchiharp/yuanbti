# TOOLS.md - 开发小一·评审官

## Playwright 实操审查

```bash
npx playwright test            # 运行测试验证修复
npx playwright test -g "名称"   # 运行指定用例
npx playwright test --ui        # 调试模式
```

## 代码审查

```bash
mvn clean compile              # 验证编译通过
mvn test                       # 运行单元测试
npm run build                  # 验证前端构建
```

## 环境检查

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000   # 前端
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080   # 后端
```

## 项目信息（由协调者传入）

- **被审查agent：** 开发小一
- **项目路径：** {协调者指定}
- **产出路径：** {协调者指定}

## 审查标准

详见 code-review-standard skill（templates/REVIEW-STANDARDS.md）
