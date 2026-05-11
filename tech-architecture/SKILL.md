---
name: tech-architecture
type: methodology
trigger: user-request
description: 技术架构设计方法论。从系统架构图到技术选型的完整流程，含数据模型模板、API设计规范、安全措施检查、风险评估、技术Spike触发条件。触发词：架构设计、技术方案、技术选型、系统设计。
priority: high
auto-load: true
---

# 技术架构设计方法论

> 本 skill 可在 agent-pipeline 流程中使用，也可独立使用。

## 角色定义

- **执行者：** 架构师
- **评审官：** 架构评审官（架构审计师思维）
- **交叉评审方：** 开发、QA

## 流程概览

```
PRD（已签收）
  │
  ▼
架构师产出技术架构方案
  │
  ▼
架构评审官审查（最多2轮迭代 → 签收）
  │
  ▼
交叉评审（开发+QA 并发，24h时限）
  │
  ▼
架构师修订 → 评审官快速复核（1轮）→ 最终签收
  │
  ▼
高风险技术点 → 触发技术Spike（参考 tech-spike skill）
```

---

## 第一步：产出技术架构方案

架构师应基于已签收的 PRD，产出完整的技术架构文档：

```markdown
## 技术架构方案

### 1. 系统架构图
（文字描述架构分层）

### 2. 技术选型
| 层 | 技术方案 | 选型理由 |
|---|---------|---------|
| 前端 | Vue 3 + TypeScript | 团队熟悉、生态成熟 |
| 后端 | Java 21 + Spring Boot 3 | 类型安全、性能好 |
| 数据库 | PostgreSQL | pgvector支持AI功能 |
| 缓存 | Redis | 会话管理、热数据 |
| 部署 | Docker | 标准化环境 |

### 3. 数据模型
{ER图或表结构描述}

### 4. API设计
{核心接口列表}

### 5. 扩展性分析
| 场景 | 当前 | 10倍流量 | 100倍流量 |
|------|------|---------|----------|
| 用户注册 | 单库写入 | 读写分离 | 分库分表 |

### 6. 安全措施
- JWT + Refresh Token
- 密码 bcrypt 加密
- SQL 注入防护（参数化查询）
- XSS 防护（输入过滤+输出转义）

### 7. 高风险技术点（触发Spike）
| # | 技术点 | 风险等级 | 是否触发Spike |
|---|--------|---------|--------------|
| 1 | WebSocket长连接 | 🟡 | 是 |
| 2 | 图片AI识别 | 🔴 | 是 |
```

---

## 第二步：架构评审官审查

架构评审官从以下维度审查：
- 3年后还撑得住吗？
- 技术选型是否过度/不足
- 扩展性瓶颈在哪
- 安全措施是否充分
- 数据模型是否合理（范式/反范式权衡）
- 高风险技术点是否正确识别

最多2轮迭代，签收后进入交叉评审。

---

## 第三步：交叉评审

**模式：** 并发评审，不做迭代，只提意见
**时限：** 24h

### 各角色评审维度

| 角色 | 评审视角 | 典型问题 |
|------|---------|---------|
| 开发 | 技术可行性 | 技术选型熟悉吗？接口合理吗？有无过度设计？ |
| QA | 可测试性 | 方便测试吗？日志监控够吗？能自动化吗？ |

### 汇总处理

1. 收集开发和QA的评审意见
2. 交给架构师修订
3. 架构评审官快速复核（1轮）
4. 最终签收

---

## 高风险技术点与 Spike 触发

架构方案中标记的高风险技术点，应触发技术 Spike 验证。

**Spike 判断标准：**
- 🔴 高风险：核心技术可行性未知、涉及第三方不稳定API、性能要求极高
- 🟡 中风险：技术方案已知但有实现细节不确定性、依赖不熟悉的库

**触发 Spike 后，参考 `tech-spike` skill 执行验证。**

---

## 代码架构规范（阶段2必须产出）

架构方案必须包含「代码架构」章节，定义项目的代码组织规范。以下为通用模板，架构师根据技术栈调整。

### 1. 分层架构（职责边界）

```
Controller → Service → Repository
   ↓           ↓          ↓
 接收请求    业务逻辑    数据访问
 参数校验    事务管理    SQL/ORM
 返回响应    权限检查    数据转换
```

**强制规则：**
- Controller 不得直接调用 Repository，必须经过 Service
- Service 不得依赖 HttpServletRequest/Response（框架对象）
- Repository 不得包含业务逻辑，只做 CRUD
- 各层之间通过 DTO/VO 传递数据，不直接暴露实体

**检查方法：** 搜索 Controller 类中是否 import 了 Repository/Mapper 类

### 2. 模块解耦策略

每个业务模块独立目录，模块间通过接口（Interface）通信，不直接引用实现类。

```
模块A                    模块B
├── XxxController        ├── YyyController
├── XxxService           ├── YyyService
├── XxxServiceImpl       ├── YyyServiceImpl
├── XxxRepository        ├── YyyRepository
└── dto/                 └── dto/
```

**模块间通信方式：**
| 场景 | 方式 | 示例 |
|------|------|------|
| 同步调用 | 注入接口（Interface） | `AuthService.validate(token)` |
| 异步通知 | 事件机制 | `UserCreatedEvent → 发送欢迎邮件` |
| 共享数据 | 公共 DTO | `UserDTO` 在 auth 和 permission 模块间传递 |

**禁止：** 模块A直接 import 模块B的 ServiceImpl 类

### 3. 可复用组件清单

架构方案必须识别以下通用组件，并定义其接口：

| 组件 | 职责 | 接口示例 |
|------|------|---------|
| 认证过滤器 | 拦截请求、验证 Token、注入用户上下文 | `JwtAuthFilter extends OncePerRequestFilter` |
| 权限注解 | 声明式权限检查 | `@RequirePermission("user:manage")` |
| 统一响应 | 标准化 API 返回格式 | `Result<T> { code, message, data }` |
| 全局异常处理 | 统一异常捕获和错误码映射 | `@RestControllerAdvice GlobalExceptionHandler` |
| 审计日志切面 | 自动记录操作日志 | `@AuditLog(action="create", resource="user")` |
| 用户上下文 | 线程级用户信息持有 | `SecurityContextHolder / ThreadLocal<UserContext>` |

**架构师必须定义这些组件的接口签名和所在包路径。**

### 4. 目录结构规范

架构方案必须产出完整的目录结构树，格式：

```
{project}/
├── src/main/java/com/{company}/{project}/
│   ├── config/              # 配置类（Security、JWT、MyBatis 等）
│   ├── common/              # 公共组件（Result、异常、工具类）
│   │   ├── Result.java
│   │   ├── GlobalExceptionHandler.java
│   │   └── UserContext.java
│   ├── auth/                # 认证模块
│   │   ├── AuthController.java
│   │   ├── AuthService.java
│   │   └── JwtAuthFilter.java
│   ├── {module}/            # 业务模块（每个模块独立目录）
│   │   ├── {Module}Controller.java
│   │   ├── {Module}Service.java
│   │   ├── {Module}ServiceImpl.java
│   │   ├── {Module}Repository.java
│   │   ├── entity/          # 数据库实体
│   │   └── dto/             # 请求/响应 DTO
│   └── ...
├── src/main/resources/
│   ├── application.yml
│   └── db/migration/        # 数据库迁移脚本
└── src/test/
```

**命名规范：**
| 类型 | 命名规则 | 示例 |
|------|---------|------|
| Controller | `{Module}Controller` | `UserController` |
| Service 接口 | `{Module}Service` | `UserService` |
| Service 实现 | `{Module}ServiceImpl` | `UserServiceImpl` |
| Repository | `{Module}Repository` 或 `{Module}Mapper` | `UserMapper` |
| DTO | `{Action}{Module}Request/Response` | `CreateUserRequest` |
| 实体 | `{Module}` | `User` |

### 5. 扩展点设计

架构方案必须定义「新增业务系统接入」的扩展接口：

| 扩展点 | 接口 | 新增时做什么 |
|--------|------|------------|
| 新增权限 | `PermissionRegistry.register(code, name)` | 注册新权限编码 |
| 新增角色 | 直接在管理后台创建 | 无需改代码 |
| 新增业务系统 | `AppRegistry.register(clientId, redirectUri)` | 注册应用 + 配置回调 |
| 新增审计事件 | `@AuditLog(action="new-action")` | 加注解即可 |
| 新增数据范围 | `DataScopeEvaluator` 接口 | 实现新范围的过滤逻辑 |

**原则：** 新增业务系统接入时，只改配置不改代码（或只加注解）。

### 6. 设计模式选型

架构方案必须说明各模块使用的设计模式，格式：

| 模块/场景 | 选用模式 | 原因 |
|----------|---------|------|
| 认证方式切换（JWT/OAuth/SAML） | Strategy | 多种认证算法可互换 |
| 消息通知（邮件/短信/站内信） | Strategy | 通知渠道可扩展 |
| 权限校验链（Token→角色→策略→数据范围） | Chain of Responsibility | 多级校验逐层传递 |
| 用户创建后的副作用（发邮件+初始化+日志） | Observer | 解耦核心逻辑和副作用 |
| API 日志/限流/权限 注入 Controller | Decorator / AOP | 不侵入业务代码 |
| 各模块统一 CRUD 骨架 | Template Method | 只覆写差异部分 |
| 创建不同类型实体（普通/VIP/管理员） | Factory | 封装创建逻辑 |
| 跨模块状态变更通知 | Domain Event + Observer | 模块解耦 |

**要求：** 不需要解释模式是什么，但必须说清楚「为什么这里用这个模式」。如果某个模块不需要特殊模式，写「标准 CRUD，无特殊模式」即可。

### 7. DDD 模块划分（可选，复杂业务推荐）

对于业务复杂的项目，架构方案可采用 DDD 思维划分模块：

| 概念 | 作用 | 示例 |
|------|------|------|
| Bounded Context | 模块边界，各管各的数据模型 | 认证上下文 vs 权限上下文 vs 项目上下文 |
| Aggregate | 事务一致性边界 | `User`（聚合根）+ `UserRole`（子实体） |
| Domain Event | 模块间松耦合通信 | `UserCreatedEvent` → 发欢迎邮件 |
| Value Object | 不可变的业务描述 | `Email`、`Permission`（资源:操作编码） |
| Application Service | 编排业务流程 | `AuthService.login()` 调用多个领域服务 |
| Domain Service | 纯业务逻辑 | `PolicyEngine.evaluate()` 策略评估 |

**要求：** 简单项目用标准三层架构即可，不必强行 DDD。只有当模块间关系复杂、数据一致性要求高时才用。

### 8. 日志/异常/错误处理架构

架构方案必须定义统一的日志和异常处理策略（详见 `logging-exception` skill）：

| 维度 | 必须定义 |
|------|---------|
| 错误码体系 | 分层编码规则（如 `AUTH_001`、`PERM_002`） |
| 异常传播策略 | 哪些层捕获、哪些层抛出、全局异常处理器 |
| 日志规范 | 结构化字段（traceId/userId/action）、日志级别使用场景 |
| 敏感数据脱敏 | 哪些字段脱敏、脱敏方式 |

### 架构方案验收标准

- [ ] 技术选型有理由（为什么选A不选B）
- [ ] 接口定义完整（请求/响应/错误码）
- [ ] 数据模型清晰（实体关系、字段说明）
- [ ] 已识别技术风险（至少列出3个潜在风险）
- [ ] 代码架构章节完整（分层+模块+组件+目录+扩展点+模式选型+日志异常）
- [ ] 行数 ≥ 80行

---

## 防空签收规则

签收报告必须包含：
- 至少3个具体检查过的点（写明章节号/技术点）
- 至少1个🟢建议或观察
- 各维度评分

打回报告必须包含：
- 每个问题的具体位置（章节号）
- 具体的修改建议
- 预期修改后的效果

**以下视为空签收（不合格）：**
- ❌ "架构设计没问题，签收"
- ❌ "方案合理，通过"

---

## ⚠️ 防偷懒规则

### 1. 禁止跳过步骤

- **必须读取 PRD**（不能靠记忆或概括）
- 技术选型 **必须列出对比**（为什么选A不选B，至少2个备选方案）
- 数据模型 **必须定义字段**（不能只写"用户表、订单表"，要列出核心字段和关系）
- 风险识别 **至少3个**（不允许"没有已知风险"）

### 2. 架构文档强制内容

| 章节 | 强制要求 | 偷懒信号 |
|------|---------|---------|
| 技术选型 | 列出≥2个备选 + 选择理由 + trade-off | ❌ 只写"使用React"不解释原因 |
| 数据模型 | 实体关系 + 核心字段 + 索引策略 | ❌ 只列实体名不列字段 |
| API设计 | 请求/响应格式 + 错误码 + 认证方式 | ❌ 只写API路径不写格式 |
| 安全措施 | 认证/授权/输入校验/敏感数据处理 | ❌ 只写"使用JWT" |
| 风险识别 | ≥3个风险 + 应对方案 | ❌ "暂无风险" |

### 3. 偷懒检测信号

**以下行为视为偷懒：**
- ARCHITECTURE.md 行数 < 80
- 技术选型只有一个方案没有对比
- 数据模型没有字段说明
- 风险识别为空或少于3个
- API设计只有路径没有请求/响应格式


> **产出路径：** 由调用方（协调者/用户）在任务消息中指定。未指定时默认 `/tmp/agent-skills-output/`。本skill不硬编码产出位置，可独立使用于任何项目。