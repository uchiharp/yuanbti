# 阶段2：架构设计（架构师）

## 任务
基于已签收的 PRD（🟡/🔴项目为细化后的 PRD），产出技术架构方案。不仅要满足需求，还需主动分析架构约束、性能指标、安全策略、扩展性、技术债务处理等。

## 必读文件（按顺序）
1. PRD.md（🟡/🔴项目为细化后的 PRD-REFINED.md）
2. CONTEXT.md（项目上下文）
3. UI-UX-DESIGN.md（🟡/🔴项目，阶段1.7产出的设计文档，确认技术栈和组件选型）
4. docs/ui-prototype.html（🟡/🔴项目，阶段1.7产出的 HTML 原型，参考交互实现需求）

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

## 自身技术特性深度分析（强制执行）

架构方案不能只满足需求，必须主动分析以下 6 个维度：

### A. 架构约束分析
- **技术栈限制**：选型框架的版本约束、兼容性、已知 issue
- **基础设施约束**：部署环境（云/自建/混合）、资源限制、网络拓扑
- **团队约束**：团队技术栈熟悉度、维护成本、招聘难度
- **时间约束**：MVP 上线时间对架构决策的影响

### B. 性能指标设计
- **响应时间**：P50/P95/P99 目标值，关键接口 SLA
- **吞吐量**：QPS/TPS 预估值，峰值倍数
- **数据量级**：初始数据量、增长速率、分库分表阈值
- **缓存策略**：多级缓存设计、缓存命中率目标
- **性能测试方案**：压测工具、基准数据、验收标准

### C. 安全策略设计
- **认证授权**：OAuth2/JWT/Session 选型、RBAC/ABAC 模型
- **数据安全**：加密传输(TLS)、加密存储、密钥管理
- **API安全**：限流、防重放、签名验证、CORS策略
- **依赖安全**：第三方依赖扫描、漏洞响应流程
- **审计日志**：操作审计、数据变更审计、安全事件日志

### D. 扩展性设计
- **水平扩展**：无状态设计、会话管理、负载均衡策略
- **功能扩展**：插件机制、事件驱动、策略模式预留
- **数据扩展**：分库分表方案、数据迁移策略、版本兼容
- **接口版本化**：API 版本管理策略、向后兼容规则

### E. 技术债务管理
- **已知债务识别**：哪些决策是短期妥协，为什么
- **偿还计划**：每项债务的预期偿还时间和方式
- **债务量化**：对开发效率/性能/维护成本的影响评估
- **预防机制**：代码规范、架构守护测试、定期审视

### F. 可观测性设计
- **日志规范**：结构化日志、日志级别策略、日志聚合方案
- **指标监控**：应用指标（RED 方法）、基础设施指标（USE 方法）
- **链路追踪**：分布式追踪方案、Trace ID 透传
- **告警策略**：告警分级、响应流程、升级机制

## 执行流程
1. 加载 `tech-architecture` + `logging-exception` SKILL.md
2. 读 PRD.md（🟡/🔴项目还需读 UI-UX-DESIGN.md 和 ui-prototype.html）
3. 和用户讨论技术选型（Brainstorm）
4. **执行 6 维度技术特性分析**（不是简单翻译需求）
5. 产出 ARCHITECTURE.md
6. 标注高风险技术点（触发阶段2.8条件）
7. 架构师自审（最多2轮）

## 检查项（脚本强制）
- [ ] ARCHITECTURE.md ≥100行
- [ ] docker-compose.test.yml 存在（E2E 测试环境定义）
- [ ] 覆盖率工具已配置（pom.xml 含 JaCoCo / package.json 含 c8 / pyproject.toml 含 pytest-cov / Makefile 含 go test / cargo tarpaulin）
- [ ] 覆盖率阈值设为 95%（低于则构建失败）
- [ ] 覆盖率报告输出到统一路径（coverage/unit/ + coverage/integration/）
- [ ] 单元测试和集成测试覆盖率分开收集（ut/it 独立报告）
- [ ] 评审报告 ≥3检查点 + ≥1建议 + 评分
- [ ] 合同轮次 ≤2
- [ ] 如含"高风险"/"Spike"标记 → 触发阶段2.8
- [ ] ARCHITECTURE.md 包含 6 维度技术特性分析
- [ ] ARCHITECTURE.md 包含全部 11 项工程健壮性设计

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

### 统一路径约定（所有语言强制）

所有语言覆盖率报告必须输出到统一路径，`pipeline-check.sh` 只认路径不认语言：

```
{项目目录}/
  coverage/
    unit/index.html          ← 单元测试覆盖率
    integration/index.html   ← 集成测试覆盖率
```

各语言通过构建工具或脚本将报告输出/软链到此路径。

### Java（JaCoCo，嵌入 pom.xml）

拆分 ut/it 两个 execution，产出两份独立覆盖率报告：

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <!-- 单元测试 -->
    <execution>
      <id>jacoco-ut</id>
      <goals><goal>prepare-agent</goal></goals>
      <configuration>
        <destFile>${project.build.directory}/jacoco-ut.exec</destFile>
        <propertyName>surefireArgLine</propertyName>
      </configuration>
    </execution>
    <execution>
      <id>jacoco-ut-report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
      <configuration>
        <dataFile>${project.build.directory}/jacoco-ut.exec</dataFile>
        <outputDirectory>${project.build.directory}/site/jacoco-ut</outputDirectory>
      </configuration>
    </execution>
    <!-- 集成测试 -->
    <execution>
      <id>jacoco-it</id>
      <goals><goal>prepare-agent-integration</goal></goals>
      <configuration>
        <destFile>${project.build.directory}/jacoco-it.exec</destFile>
        <propertyName>failsafeArgLine</propertyName>
      </configuration>
    </execution>
    <execution>
      <id>jacoco-it-report</id>
      <phase>verify</phase>
      <goals><goal>report-integration</goal></goals>
      <configuration>
        <dataFile>${project.build.directory}/jacoco-it.exec</dataFile>
        <outputDirectory>${project.build.directory}/site/jacoco-it</outputDirectory>
      </configuration>
    </execution>
    <!-- 覆盖率门禁 -->
    <execution>
      <id>check</id>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>BUNDLE</element>
            <limits>
              <limit><counter>LINE</counter><value>COVEREDRATIO</value><minimum>0.95</minimum></limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>

<!-- surefire 用 ut agent -->
<plugin>
  <artifactId>maven-surefire-plugin</artifactId>
  <configuration><argLine>${surefireArgLine}</argLine></configuration>
</plugin>
<!-- failsafe 用 it agent -->
<plugin>
  <artifactId>maven-failsafe-plugin</artifactId>
  <configuration><argLine>${failsafeArgLine}</argLine></configuration>
  <executions>
    <execution><goals><goal>integration-test</goal><goal>verify</goal></goals></execution>
  </executions>
</plugin>
```

构建完成后软链到统一路径：
```bash
mkdir -p coverage/unit coverage/integration
ln -sf $PWD/target/site/jacoco-ut coverage/unit
ln -sf $PWD/target/site/jacoco-it coverage/integration
```

### Node.js / TypeScript（c8，嵌入 package.json）

c8 天然支持 `--reports-dir`，直接输出到统一路径：

```json
{
  "scripts": {
    "test:unit": "c8 --reports-dir=coverage/unit --reporter=html --lines 95 vitest run --dir tests/unit",
    "test:integration": "c8 --reports-dir=coverage/integration --reporter=html --lines 95 vitest run --dir tests/integration",
    "test": "npm run test:unit && npm run test:integration"
  }
}
```

### Python（pytest-cov，嵌入 pyproject.toml + CLI）

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

执行命令（写入 Makefile 或 scripts）：
```bash
# 单元测试覆盖率
pytest tests/unit --cov=src --cov-report=html:coverage/unit --cov-report=term --cov-fail-under=95

# 集成测试覆盖率
pytest tests/integration --cov=src --cov-report=html:coverage/integration --cov-report=term --cov-fail-under=95
```

### Go（go test -coverprofile + build tag）

测试文件用 build tag 区分层级：
```go
//go:build unit
// user_service_test.go — 单元测试

//go:build integration
// user_service_integration_test.go — 集成测试
```

Makefile 配置：
```makefile
test-unit:
	mkdir -p coverage/unit
	go test -tags=unit -coverprofile=coverage/unit.out ./...
	go tool cover -html=coverage/unit.out -o coverage/unit/index.html

test-integration:
	mkdir -p coverage/integration
	go test -tags=integration -coverprofile=coverage/integration.out ./...
	go tool cover -html=coverage/integration.out -o coverage/integration/index.html

test: test-unit test-integration
```

### Rust（cargo-tarpaulin）

Makefile 配置：
```makefile
test-unit:
	mkdir -p coverage/unit
	cargo tarpaulin --lib --skip-tests --out Html --output-dir coverage/unit

test-integration:
	mkdir -p coverage/integration
	cargo tarpaulin --tests --out Html --output-dir coverage/integration

test: test-unit test-integration
```

**效果**：不管什么语言，`pipeline-check.sh` 统一检查 `coverage/unit/index.html` 和 `coverage/integration/index.html`，各自≥95% 才通过。开发者本地就能看到分层覆盖率。

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
- 🟡/🔴项目必须参考 UI/UX 设计文档和 HTML 原型
- 技术选型必须列出对比（≥2个备选）
- 数据模型必须定义字段（不能只写表名）
- 风险识别至少3个
- 6 维度技术特性分析不能遗漏
- 知识库：更新 CONTEXT.md 阶段2段落，存入 MemPalace room=arch-decisions
