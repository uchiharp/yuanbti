# 阶段2：架构设计（架构师）

## 任务
基于已签收的 PRD，产出技术架构方案。

## 必读文件（按顺序）
1. PRD.md（已签收的需求文档）
2. CONTEXT.md（项目上下文）

## 加载 Skill
- `tech-architecture`（架构设计方法论）
- `logging-exception`（日志/异常/错误处理规范）

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| ARCHITECTURE.md | 100 | 完整技术架构方案 |
| docker-compose.test.yml | — | E2E 测试环境定义（DB + 后端 + 前端 + 依赖服务） |
| 覆盖率工具配置 | — | JaCoCo/c8/coverage 配置（嵌入 pom.xml/package.json） |

## ARCHITECTURE.md 必须包含
1. 系统架构图
2. 技术选型（≥2个备选 + 选择理由 + trade-off）
3. 数据模型（实体关系 + 核心字段 + 索引策略）
4. API设计（请求/响应格式 + 错误码 + 认证方式）
5. 安全措施
6. 风险识别（≥3个风险 + 应对方案）
7. **代码架构**（分层+模块+组件+目录+扩展点+模式选型+日志异常）
8. **并发与边界设计**（见下方专项）

## 执行流程
1. 加载 `tech-architecture` + `logging-exception` SKILL.md
2. 读 PRD.md
3. 和用户讨论技术选型（Brainstorm）
4. 产出 ARCHITECTURE.md
5. 标注高风险技术点（触发阶段2.8条件）
6. 架构师自审（最多2轮）

## 检查项（脚本强制）
- [ ] ARCHITECTURE.md ≥100行
- [ ] docker-compose.test.yml 存在（E2E 测试环境定义）
- [ ] 覆盖率工具已配置（pom.xml 含 JaCoCo / package.json 含 c8）
- [ ] 覆盖率阈值设为 95%（低于则构建失败）
- [ ] 评审报告 ≥3检查点 + ≥1建议 + 评分
- [ ] 合同轮次 ≤2
- [ ] 如含"高风险"/"Spike"标记 → 触发阶段2.8

## docker-compose.test.yml 要求
架构师必须在阶段2产出测试环境定义文件，确保后续阶段（开发自测、E2E、冒烟）都能一键启动完整环境：

```yaml
# docker-compose.test.yml 示例
version: "3.8"
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: test123
      MYSQL_DATABASE: app_test
    ports: ["3306:3306"]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    ports: ["8080:8080"]
    depends_on:
      mysql: { condition: service_healthy }
      redis: { condition: service_started }
    environment:
      SPRING_PROFILES_ACTIVE: test

  frontend:
    build: ./frontend
    ports: ["5173:80"]
    depends_on: [backend]
```

**要求**：
- 所有服务用 healthcheck 确认就绪（不是 sleep 等待）
- 后端依赖 DB 就绪后才启动（`condition: service_healthy`）
- 端口映射明确，和 E2E 脚本中的 baseURL 一致
- 阶段6/8/9 统一使用此文件启动环境

## 覆盖率工具配置要求
架构师必须在阶段2配置好覆盖率工具，嵌入项目构建配置中。**阈值 95%，低于则 `mvn test` / `npm test` 直接失败。**

### Java（JaCoCo，嵌入 pom.xml）
```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
    <execution>
      <id>check</id>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>BUNDLE</element>
            <limits>
              <limit>
                <counter>LINE</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.95</minimum>
              </limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

### Node.js（c8，嵌入 package.json）
```json
{
  "scripts": {
    "test": "c8 --lines 95 --branches 95 jest"
  },
  "c8": {
    "reporter": ["text", "html"],
    "report-dir": "coverage"
  }
}
```

### Python（pytest-cov，嵌入 pyproject.toml）
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=html --cov-fail-under=95"
```

**效果**：`mvn test` / `npm test` / `pytest` 时自动收集覆盖率，低于 95% 直接失败。开发者本地就能看到哪些行没覆盖。

## 工程健壮性设计（必须在 ARCHITECTURE.md 中体现）

架构师必须在 ARCHITECTURE.md 中明确设计以下 11 项内容。**详细规范见 `engineering-robustness` SKILL.md（dispatch.sh 自动加载）。**

1. 前端防抖/节流 — 列出所有需防抖/节流的接口和组件
2. 分布式锁/并发控制 — 每个实体标注乐观锁字段或说明无并发风险
3. 边界条件清单 — 逐接口列出边界条件处理策略
4. 超时设计 — 列出所有外部调用及超时配置
5. 缓存策略 — 每个缓存的 key 设计、TTL、失效策略
6. 限流 — 维度 + 阈值 + 超限响应
7. 文件上传安全 — 类型/大小/路径/权限
8. 连接池配置 — 所有连接池参数
9. 优雅降级 — 每个非核心依赖的降级方案
10. 数据脱敏 — 所有敏感字段及脱敏规则
11. 幂等性设计 — 每个写接口的幂等方案

### 检查项
- [ ] ARCHITECTURE.md 包含全部 11 项工程健壮性设计

## 约束
- 合同：🟡中风险 标准合同 最多2轮
- 必须读取 PRD（不能靠记忆或概括）
- 技术选型必须列出对比（≥2个备选）
- 数据模型必须定义字段（不能只写表名）
- 风险识别至少3个
- 知识库：更新 CONTEXT.md 阶段2段落，存入 MemPalace room=arch-decisions
