---
name: run-tests
description: Finder App 全量测试执行器。当用户说"跑测试"、"跑所有测试"、"run tests"、"全量测试"、"E2E测试"时激活。覆盖后端单元测试、后端集成测试、前端E2E(Playwright)测试，自动处理内存限制和分批执行。
---

# Finder App 测试执行器

## 项目路径
- 后端：`/Users/sunwenyong/projects/deer-flow/output/finder-app/backend`
- 前端：`/Users/sunwenyong/projects/deer-flow/output/finder-app/uni-app`
- Java 21：`/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home`

## 测试分层

### 第一层：后端单元测试（轻量，不需要数据库）
```bash
cd /Users/sunwenyong/projects/deer-flow/output/finder-app/backend
JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home \
MAVEN_OPTS="-Xmx512m" \
mvn test -Dtest="!*IntegrationTest,!*ControllerTest,!FileUploadIntegrationTest" -B 2>&1 | tail -20
```

### 第二层：后端集成测试（中等，Spring Boot 自动启动上下文）
```bash
cd /Users/sunwenyong/projects/deer-flow/output/finder-app/backend
JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home \
MAVEN_OPTS="-Xmx768m" \
mvn test -Dtest="*IntegrationTest,*ControllerTest,FileUploadIntegrationTest" -B 2>&1 | tail -20
```

### 第三层：前端 E2E 测试（重量，必须启动前后端服务）

**前提：后端和前端服务已启动。**

```bash
# 1. 确保后端运行
curl -s http://localhost:8080/actuator/health || echo "后端未启动"

# 2. 确保前端运行
curl -s http://localhost:5173 > /dev/null || echo "前端未启动"

# 3. 跑 Playwright
cd /Users/sunwenyong/projects/deer-flow/output/finder-app/uni-app
npx playwright test 2>&1 | tail -30
```

如果服务未启动，先启动：
```bash
# 启动后端（后台）
cd /Users/sunwenyong/projects/deer-flow/output/finder-app/backend
JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home \
MAVEN_OPTS="-Xmx512m" \
nohup mvn spring-boot:run > /tmp/finder-backend.log 2>&1 &

# 启动前端（后台）
cd /Users/sunwenyong/projects/deer-flow/output/finder-app/uni-app
nohup npm run dev > /tmp/finder-frontend.log 2>&1 &
```

## 执行策略

### 默认：分批执行（推荐）
按 第一层 → 第二层 → 第三层 顺序执行。每层独立报告结果。

### 快速模式：只跑单元测试
当用户说"快速跑一下"、"只跑单元测试"时，只执行第一层。

### OOM 防护
- 始终设置 `MAVEN_OPTS="-Xmx512m"`（单元测试）或 `MAVEN_OPTS="-Xmx768m"`（集成测试）
- 如果进程被 SIGKILL，降低 Xmx 到 384m 重试
- 集成测试和 E2E 不要同时跑

## 结果汇报格式

```
## 测试结果

### 后端单元测试
- 结果：X 通过 / Y 失败 / Z 跳过
- 耗时：Ns

### 后端集成测试
- 结果：X 通过 / Y 失败
- 耗时：Ns

### 前端 E2E 测试
- 结果：X 通过 / Y 失败
- 耗时：Ns

### 失败测试明细
（列出每个失败测试的名称和错误）
```
