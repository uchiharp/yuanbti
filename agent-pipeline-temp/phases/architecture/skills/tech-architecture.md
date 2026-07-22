---
name: tech-architecture
type: methodology
trigger: agent-need
description: 架构设计方法论。技术选型、数据模型、API设计、安全策略、扩展性、性能指标、代码架构。
priority: high
auto-load: false
---

# 技术架构设计方法论

> 本 skill 供架构师在阶段2设计架构方案时参考。
> 设计目标：不仅要满足需求，还需主动分析架构约束、性能指标、安全策略、扩展性、技术债务处理等。

---

## 1. 技术选型方法论

### 选型流程

1. **需求分析** — 从 PRD 提取技术需求（性能、安全、扩展性）
2. **候选方案** — 列出≥2个备选技术方案
3. **对比评估** — 用统一维度对比（性能、学习曲线、社区活跃度、维护成本）
4. **Trade-off 分析** — 明确选择某方案放弃什么
5. **决策记录** — 记录选型理由，方便后续复盘

### 选型维度

| 维度 | 说明 | 评估方法 |
|------|------|---------|
| 性能 | QPS、响应时间、资源占用 | 基准测试、社区 benchmark |
| 学习曲线 | 团队上手难度 | 团队技能评估 |
| 社区活跃度 | GitHub stars、issue 响应、版本发布频率 | 数据调研 |
| 维护成本 | 长期维护难度、升级成本 | 经验评估 |
| 生态 | 周边库/工具/文档完善度 | 调研 |
| 许可证 | 开源协议是否兼容 | 法务确认 |

### 输出格式

```markdown
### {技术点} 选型

| 维度 | 方案A | 方案B | 方案C |
|------|-------|-------|-------|
| 性能 | ... | ... | ... |
| 学习曲线 | ... | ... | ... |
| 社区活跃度 | ... | ... | ... |
| 维护成本 | ... | ... | ... |
| 生态 | ... | ... | ... |

**选择：方案X**
**理由：** ...
**Trade-off：** 放弃了方案Y的{优点}，因为{原因}
```

---

## 2. 数据模型设计

### 设计原则

- **实体关系**：明确一对多、多对多关系
- **核心字段**：每个表必须定义核心字段（不能只写表名）
- **索引策略**：高频查询字段必须建索引
- **软删除**：生产数据用 `deleted_at` 字段，不物理删除
- **审计字段**：`created_at`、`updated_at`、`created_by`、`updated_by`

### 输出格式

```markdown
### 数据模型

#### 用户表 (users)
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 用户ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| email | VARCHAR(100) | UNIQUE, NOT NULL | 邮箱 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| created_at | DATETIME | NOT NULL, DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW | 更新时间 |
| deleted_at | DATETIME | NULL | 软删除时间 |

**索引：**
- idx_users_email (email)
- idx_users_username (username)

#### 实体关系
users 1:N orders
users N:N roles (via user_roles)
```

---

## 3. API 设计规范

### RESTful 规范

| 方法 | 路径 | 说明 | 状态码 |
|------|------|------|--------|
| GET | /api/v1/{resource} | 列表查询 | 200 |
| GET | /api/v1/{resource}/:id | 单条查询 | 200/404 |
| POST | /api/v1/{resource} | 创建 | 201 |
| PUT | /api/v1/{resource}/:id | 全量更新 | 200/404 |
| PATCH | /api/v1/{resource}/:id | 部分更新 | 200/404 |
| DELETE | /api/v1/{resource}/:id | 删除 | 204/404 |

### 响应格式

```json
// 成功
{
  "code": 0,
  "data": { ... },
  "message": "success"
}

// 分页
{
  "code": 0,
  "data": {
    "list": [...],
    "total": 100,
    "page": 1,
    "size": 20
  }
}

// 错误
{
  "code": "AUTH_001",
  "message": "Token已过期，请重新登录",
  "detail": null,
  "timestamp": "2026-05-11T10:30:00Z",
  "traceId": "abc-123-def"
}
```

---

## 4. 架构风格选择

| 风格 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| 单体 | 小型项目、MVP | 简单、部署方便 | 扩展性差 |
| 模块化单体 | 中型项目 | 结构清晰、可渐进拆分 | 需要模块边界设计 |
| 微服务 | 大型项目、多团队 | 独立部署、技术栈自由 | 运维复杂、分布式事务 |
| Serverless | 事件驱动、低频调用 | 按需计费、免运维 | 冷启动、调试困难 |

---

## 5. 代码架构模式

### 分层架构

```
Controller → Service → Repository → Database
    ↓           ↓           ↓
  DTO       Business     Entity
```

### 模块组织

```
src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.repository.ts
│   │   ├── auth.dto.ts
│   │   └── auth.module.ts
│   └── user/
│       └── ...
├── common/
│   ├── guards/
│   ├── interceptors/
│   ├── filters/
│   └── decorators/
└── config/
```

### 设计模式选型表

| 模式 | 适用场景 | 实现方式 |
|------|---------|---------|
| 策略模式 | 多种认证方式 | 接口 + 实现类 |
| 工厂模式 | 多种消息格式 | 工厂类 + 注册表 |
| 观察者模式 | 事件驱动 | 事件总线 |
| 装饰器模式 | 功能增强 | AOP / 中间件 |
| 模板方法 | 流程固定、步骤可变 | 抽象类 + 钩子方法 |

---

## 6. 非功能需求设计

### 性能设计

- **缓存策略**：多级缓存（本地 → Redis → DB）
- **异步处理**：耗时操作走消息队列
- **数据库优化**：索引、分页、批量操作
- **CDN**：静态资源走 CDN

### 安全设计

- **认证**：JWT + Refresh Token
- **授权**：RBAC 基于角色的访问控制
- **传输**：全站 HTTPS
- **存储**：密码 bcrypt，敏感字段 AES
- **审计**：操作日志独立存储

### 可用性设计

- **健康检查**：`/health` 端点
- **优雅关闭**：收到 SIGTERM 后等待请求处理完毕
- **重试机制**：指数退避，最大重试次数
- **熔断器**：非核心依赖故障时降级
