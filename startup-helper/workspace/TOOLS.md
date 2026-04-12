# TOOLS.md - 创业助手

## 构建验证

```bash
mvn clean compile              # 验证后端编译
mvn test                       # 运行后端单元测试
npm run build                  # 验证前端构建
```

## Playwright（冒烟验证）

```bash
npx playwright test            # 运行E2E测试
npx playwright test -g "名称"   # 运行指定用例
```

## 环境检查

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000   # 前端
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080   # 后端
```

## Git

```bash
git add . && git commit -m "feat: xxx" && git push
```

## 项目信息（由协调者传入）

- **项目路径：** {协调者指定}
- **产出路径：** {协调者指定}
