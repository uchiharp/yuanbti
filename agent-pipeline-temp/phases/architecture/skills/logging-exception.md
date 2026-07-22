---
name: logging-exception
type: methodology
trigger: agent-need
description: 日志、异常、错误处理架构设计规范。定义错误码体系、异常传播策略、日志规范、脱敏规则、重试机制。
priority: medium
auto-load: false
---

# 日志/异常/错误处理架构规范

> 本 skill 供架构师在阶段 2 设计架构方案时参考，也可供开发在阶段 6 编码时查阅。

---

## 1. 错误码体系

### 分层编码规则

架构方案必须定义统一的错误码格式，推荐格式：`{模块}_{编号}`

| 模块前缀 | 说明 | 示例 |
|---------|------|------|
| `AUTH` | 认证相关 | `AUTH_001`（Token过期） |
| `PERM` | 权限相关 | `PERM_001`（无权限） |
| `USER` | 用户管理 | `USER_001`（用户不存在） |
| `SYS` | 系统级 | `SYS_001`（参数校验失败） |

### HTTP 状态码映射

| HTTP 码 | 场景 | 业务码范围 |
|---------|------|----------|
| 400 | 参数校验失败 | `SYS_001` ~ `SYS_099` |
| 401 | 未认证 | `AUTH_001` ~ `AUTH_099` |
| 403 | 已认证但无权限 | `PERM_001` ~ `PERM_099` |
| 404 | 资源不存在 | 各模块 `*_001` |
| 409 | 业务冲突 | 各模块 `*_002` ~ `*_099` |
| 500 | 系统内部错误 | `SYS_100`+ |

---

## 2. 异常传播策略

| 层 | 异常处理 |
|---|---------|
| Controller | 不捕获，交给全局异常处理器 |
| Service | 捕获业务异常转为错误码，不捕获系统异常 |
| Repository | 不捕获，让数据库异常冒泡 |
| 外部调用 | 必须捕获，转为业务异常或降级 |

### 全局异常处理器

```
GlobalExceptionHandler
  ├─ catch BusinessException → 业务错误码
  ├─ catch ValidationException → 400 + 字段错误
  ├─ catch AccessDeniedException → 403
  ├─ catch Exception → 500 + traceId
```

---

## 3. 日志规范

### 结构化日志字段

| 字段 | 说明 |
|------|------|
| timestamp | 时间戳 |
| level | DEBUG/INFO/WARN/ERROR |
| traceId | 请求链路ID |
| userId | 操作人 |
| action | 操作 |
| module | 模块 |
| message | 描述 |

### 审计日志（独立于应用日志）

| 字段 | 说明 |
|------|------|
| user_id | 操作人 |
| action | create/update/delete/login |
| resource | 资源类型 |
| resource_id | 资源ID |
| detail | 变更内容（JSON） |
| ip | 请求IP |

实现方式：AOP 切面 + `@AuditLog` 注解。

---

## 4. 重试与降级

| 场景 | 重试次数 | 间隔 |
|------|---------|------|
| 第三方 API 超时 | 3次 | 指数退避（1s/2s/4s） |
| 数据库连接失败 | 3次 | 固定 1s |
| 消息发送失败 | 5次 | 指数退避 |

规则：非幂等操作不重试，重试必须有上限。

---

## 产出要求

架构方案中必须包含：
- [ ] 错误码格式和分层规则
- [ ] 异常传播策略（各层职责）
- [ ] 日志级别使用规范
- [ ] 敏感数据脱敏清单
- [ ] 关键场景的重试/降级策略
