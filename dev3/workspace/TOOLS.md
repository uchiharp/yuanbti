# TOOLS.md - 开发小三（全栈三号位）

## 构建与运行

```bash
# 后端（Java/Spring Boot）
mvn clean compile              # 编译
mvn test                       # 单元测试
mvn spring-boot:run            # 启动后端（默认8080）

# 前端（Vue/uni-app）
npm install                    # 安装依赖
npm run dev                    # 启动前端开发服务器（默认3000）
npm run build                  # 构建
```

## Playwright（E2E测试）

```bash
npx playwright test            # 运行E2E测试
npx playwright test -g "名称"   # 运行指定用例
npx playwright test --ui        # 调试模式
```

## Git

```bash
git add . && git commit -m "feat: xxx" && git push
```

## 项目信息（由协调者传入）

- **项目路径：** {协调者指定}
- **后端端口：** {协调者指定，通常8080}
- **前端端口：** {协调者指定，通常3000}
- **产出路径：** {协调者指定}
