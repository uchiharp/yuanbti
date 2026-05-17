# 全 Skill 定义（合并版）

> 原始文件在 skills/*/SKILL.md，已合并为单一文件供快速查阅。



---

# Skill: engineering-robustness

---
name: engineering-robustness
description: 工程健壮性设计规范 — 防抖/并发/边界/超时/缓存/限流/上传/连接池/降级/脱敏/幂等。架构师设计时、开发实现时、QA/审查时必须加载。
---

## 元数据
- **type:** methodology
- **triggers:** agent-need
- **requires:** read
- **auto-load:** false
- **priority:** high

---

# Engineering Robustness — 工程健壮性规范

> 本 skill 是**设计+实现+审查**的完整参考。
> 架构师阶段2设计 → 开发阶段6实现 → 审查者阶段7验证，三个角色共用同一份规范。

---

## 1. 前端防抖/节流

### 设计表（架构师填入 ARCHITECTURE.md）

| 场景 | 策略 | 延迟 | 说明 |
|------|------|------|------|
| 提交按钮 | 防抖 + loading 状态 | 300ms | 防止重复提交，按钮点击后 disabled 直到响应返回 |
| 搜索输入 | 防抖 | 500ms | 输入停止 500ms 后才发请求 |
| 滚动加载 | 节流 | 200ms | 滚动事件每 200ms 最多触发一次 |
| 窗口 resize | 节流 | 300ms | 避免频繁重排 |
| 表单自动保存 | 防抖 | 2000ms | 用户停止编辑 2s 后自动保存 |

### 实现要求（开发遵守）
- 提交按钮：点击后立即 `disabled`，请求返回后恢复
- 搜索输入：`debounce(500ms)` 后才发请求，不是每次 keyup 都发
- 滚动加载：`throttle(200ms)` 限制触发频率
- 实现方式：手写或 lodash，不允许用 `setTimeout` + `clearTimeout` 的裸写法
- 每个防抖/节流点必须有对应的单测（验证只触发一次）
- 组件卸载时清理定时器（无泄漏）

### 审查要点
- [ ] 提交按钮有 disabled + loading 防重复提交
- [ ] 搜索输入有 debounce（500ms）
- [ ] 滚动/resize 有 throttle
- [ ] 组件卸载时清理定时器（无泄漏）

---

## 2. 分布式锁/并发控制

### 设计表（架构师填入 ARCHITECTURE.md）

| 场景 | 方案 | 说明 |
|------|------|------|
| 库存扣减 | Redis 原子操作 (`DECR`) 或分布式锁 | 防止超卖 |
| 订单创建 | 数据库唯一约束 + 幂等键 | 防止重复下单 |
| 状态流转 | 乐观锁（版本号 `WHERE version=?`） | 防止并发覆盖 |
| 定时任务 | Redis 分布式锁（`SET NX EX`） | 防止多实例重复执行 |
| 文件上传 | 前端去重 + 后端 hash 校验 | 防止重复上传 |

### 实现要求（开发遵守）
- 乐观锁：`UPDATE ... SET version=version+1 WHERE id=? AND version=?`，更新失败返回 409
- 幂等：创建类接口必须支持幂等键（前端生成 UUID，后端去重）
- Redis 分布式锁：`SET lock_key $unique_id NX EX 30`，释放用 Lua 脚本保证原子性
- **禁止**：只用 `SELECT ... WHERE` 判断后 `INSERT`（存在 TOCTOU 竞态）

### 审查要点
- [ ] 写操作有乐观锁/分布式锁/幂等（按 ARCHITECTURE.md 方案）
- [ ] 状态流转用 `WHERE version=?` 防并发覆盖
- [ ] 无 SELECT-then-INSERT 竞态（有唯一约束兜底）
- [ ] 定时任务有分布式锁防重复执行

---

## 3. 边界条件

### 设计表（架构师为每个 API 填入 ARCHITECTURE.md）

| 边界类型 | 处理方式 |
|---------|---------|
| 空值输入 | 必填字段校验，返回 400 + 具体字段名 |
| 空集合 | 返回空数组 `[]`，不返回 null |
| 分页边界 | `page<1` 修正为 1，`size>100` 修正为 100，空结果返回 `{data:[], total:0}` |
| 字符串超长 | 截断或 400，前端实时计数提示 |
| 数值溢出 | 后端 BigDecimal/Long，前端禁用科学计数法输入 |
| 日期边界 | 起止日期互换校验，时区统一 UTC+8 |
| 并发冲突 | 返回 409 Conflict + 重试建议 |
| 资源不存在 | 返回 404 + 具体资源类型（不是通用 "Not Found"） |

### 实现要求（开发遵守）
- 空值：所有必填字段 `@NotNull` / `@NotBlank` + 自定义错误消息
- 空集合：返回 `[]` 不返回 `null`，用 `Collections.emptyList()` 而非 `null`
- 分页：`page = max(1, page)`，`size = min(100, max(1, size))`
- 字符串：输入长度校验 + 数据库字段长度匹配（VARCHAR(255) 不接受 256 字符）
- 数值：金额用 `BigDecimal`，ID 用 `Long`，前端数字输入禁用科学计数法
- 日期：统一 `yyyy-MM-dd HH:mm:ss`，时区 `Asia/Shanghai`，起止日期校验
- 每个边界条件必须有对应的测试用例

### 审查要点
- [ ] 必填字段有 `@NotNull`/`@NotBlank` 校验
- [ ] 返回空集合而非 null
- [ ] 分页参数有上下界修正
- [ ] 字符串长度与数据库字段长度匹配
- [ ] 金额用 BigDecimal，ID 用 Long
- [ ] 日期有时区一致性（Asia/Shanghai）

---

## 4. 超时设计

### 设计表（架构师填入 ARCHITECTURE.md）

| 调用类型 | 建议超时 | 说明 |
|---------|---------|------|
| HTTP 外部 API | 连接 3s，读取 10s | 第三方接口不可控，必须设上限 |
| 数据库查询 | 30s | 慢查询告警阈值，超时直接 kill |
| Redis 操作 | 连接 1s，读写 2s | Redis 通常毫秒级，超时即异常 |
| 文件上传 | 30s（按文件大小调整） | 大文件走分片，单片超时 30s |
| 消息队列发送 | 5s | 发送超时后进重试队列 |
| 内部服务调用 | 连接 2s，读取 5s | 微服务间调用必须熔断+超时 |

### 实现要求（开发遵守）
- OkHttp/RestTemplate：`connectTimeout=3s`，`readTimeout=10s`
- Redis：`timeout=2s`，`connectTimeout=1s`
- 数据库：HikariCP `connectionTimeout=3000ms`
- 慢查询超过 3s 必须有日志告警
- **禁止**：`timeout=0`（无限等待）或不设超时

### 审查要点
- [ ] 所有外部 HTTP 调用有显式超时（connect + read）
- [ ] Redis/DB 连接有超时配置
- [ ] 无 `timeout=0` 或未设超时的情况

---

## 5. 缓存策略

### 设计表（架构师填入 ARCHITECTURE.md）

| 场景 | 问题 | 方案 |
|------|------|------|
| 缓存穿透 | 查询不存在的数据，每次都打 DB | 布隆过滤器 / 缓存空值（TTL=60s） |
| 缓存雪崩 | 大量 key 同时过期，DB 瞬时压力 | 过期时间加随机偏移（`TTL + random(0,300s)`） |
| 缓存击穿 | 热 key 过期，并发请求穿透 | 互斥锁（`SETNX`） / 永不过期 + 后台异步刷新 |
| 缓存一致性 | DB 更新后缓存未同步 | Cache Aside（先更新 DB，再删缓存） / 延迟双删 |
| 热 key | 单 key QPS 过高 | 本地缓存 / key 拆分（`hot_key_1` ~ `hot_key_N`） |

### 实现要求（开发遵守）
- 缓存穿透：查询不存在的数据时缓存空值（TTL=60s），或用布隆过滤器
- 缓存雪崩：过期时间加随机偏移 `TTL + random(0,300)`
- 缓存击穿：热 key 用互斥锁（`SETNX`）或逻辑过期
- 缓存一致性：先更新 DB 再删缓存（Cache Aside），不先更新缓存
- **禁止**：缓存和 DB 双写不一致（先更新缓存再更新 DB）

### 审查要点
- [ ] 有缓存穿透防护（布隆过滤器或缓存空值）
- [ ] 过期时间有随机偏移（防雪崩）
- [ ] 热 key 有互斥锁或逻辑过期（防击穿）
- [ ] 更新策略是 Cache Aside（先 DB 后删缓存）

---

## 6. 限流

### 设计表（架构师填入 ARCHITECTURE.md）

| 维度 | 策略 | 说明 |
|------|------|------|
| 接口级 | 令牌桶 / 滑动窗口 | 单接口 QPS 上限，超限返回 429 |
| 用户级 | 令牌桶 | 单用户每分钟请求数上限 |
| IP 级 | 滑动窗口 | 防爬虫，异常 IP 自动封禁 |
| 全局 | 计数器 | 系统总 QPS 保护，超限降级 |

### 实现要求（开发遵守）
- 使用注解或拦截器实现限流（如 Guava RateLimiter / Redis + Lua 滑动窗口）
- 超限返回 HTTP 429 + `Retry-After` 头
- 前端收到 429 时展示友好提示，不静默失败
- 每个公开 API 必须有明确的限流阈值配置

### 审查要点
- [ ] 公开 API 有限流配置（注解或拦截器）
- [ ] 超限返回 429 + Retry-After
- [ ] 前端对 429 有友好提示

---

## 7. 文件上传安全

### 设计表（架构师填入 ARCHITECTURE.md）

| 检查项 | 说明 |
|--------|------|
| 文件类型 | 白名单校验（`content-type` + 文件头 magic bytes），不只看后缀 |
| 文件大小 | 单文件上限（如 10MB），超限返回 413 |
| 文件名 | 重命名为 UUID，禁止原始文件名（防路径穿越） |
| 存储路径 | 禁止用户控制存储路径，统一存到 OSS/独立目录 |
| 病毒扫描 | 生产环境接入病毒扫描服务 |
| 访问权限 | 上传文件默认私有，需签名 URL 访问 |

### 实现要求（开发遵守）
- 文件类型：校验 `content-type` + 文件头 magic bytes，不只看后缀名
- 文件大小：单文件上限 10MB（按业务调整），超限返回 413
- 文件名：重命名为 `{uuid}.{ext}`，禁止使用原始文件名
- 存储路径：禁止用户控制路径，统一存到 OSS 或独立目录
- **禁止**：直接用用户上传的文件名拼接路径（路径穿越漏洞）

### 审查要点
- [ ] 文件类型校验 content-type + magic bytes（不只看后缀）
- [ ] 文件大小有上限
- [ ] 文件名重命名为 UUID（防路径穿越）
- [ ] 存储路径不由用户控制

---

## 8. 连接池配置

### 设计表（架构师填入 ARCHITECTURE.md）

| 组件 | 关键参数 | 建议值 |
|------|---------|--------|
| 数据库（HikariCP） | `maximumPoolSize` | CPU 核心数 × 2 + 磁盘数 |
| 数据库（HikariCP） | `connectionTimeout` | 3000ms |
| 数据库（HikariCP） | `idleTimeout` | 600000ms（10min） |
| Redis（Lettuce） | `maxTotal` | 50-100（按并发量调整） |
| Redis（Lettuce） | `maxIdle` | 20 |
| HTTP Client | `maxConnectionsPerRoute` | 50 |
| HTTP Client | `connectionRequestTimeout` | 3000ms |

### 实现要求（开发遵守）
- 数据库连接池：HikariCP，`maximumPoolSize = CPU核数 × 2 + 磁盘数`
- Redis 连接池：`maxTotal=50-100`，`maxIdle=20`
- HTTP Client：`maxConnectionsPerRoute=50`，`connectionRequestTimeout=3s`
- **禁止**：不配置连接池使用默认值（通常不合理）

### 审查要点
- [ ] 数据库连接池已显式配置（HikariCP 参数）
- [ ] Redis/HTTP Client 连接池已配置
- [ ] 不依赖框架默认值

---

## 9. 优雅降级

### 设计表（架构师填入 ARCHITECTURE.md）

| 场景 | 降级策略 |
|------|---------|
| 搜索服务不可用 | 返回"搜索暂时不可用"，不阻塞主流程 |
| 推荐服务超时 | 返回默认推荐列表（热门/最新） |
| 短信发送失败 | 进重试队列（5次，指数退降），超过进死信队列 |
| 第三方登录不可用 | 隐藏第三方登录入口，仅保留账号密码 |
| 缓存全部失效 | 限流降级，只允许读不允许写 |

### 实现要求（开发遵守）
- 非核心依赖不可用时必须有 fallback，不阻塞主流程
- 熔断器：使用 Resilience4j 或 Sentinel，半开状态自动探测恢复
- 重试：指数退避（1s, 2s, 4s），最大重试次数 3-5 次
- 超过重试上限进入死信队列，不丢数据
- **禁止**：无限重试或不设重试上限

### 审查要点
- [ ] 非核心依赖不可用时有 fallback
- [ ] 重试有上限（3-5次，指数退避）
- [ ] 无无限重试
- [ ] 超过重试上限有死信队列或告警

---

## 10. 数据脱敏

### 设计表（架构师填入 ARCHITECTURE.md）

| 场景 | 脱敏规则 |
|------|---------|
| 日志输出 | 手机号 `138****1234`，身份证 `110***********1234`，密码不记录 |
| API 响应 | 邮箱 `t***@example.com`，银行卡 `****1234` |
| 数据库存储 | 密码 bcrypt，敏感字段 AES 加密 |
| 前端展示 | 输入框 `type=password`，展示时部分遮挡 |

### 实现要求（开发遵守）
- 日志：密码不记录，手机号/身份证/银行卡部分遮挡
- API 响应：邮箱 `t***@example.com`，手机号 `138****1234`
- 数据库：密码 bcrypt 加密存储，敏感字段 AES 加密
- 前端：密码输入框 `type=password`，敏感信息展示时遮挡
- **禁止**：日志中打印完整密码/token/身份证号

### 审查要点
- [ ] 日志中无完整密码/token/身份证号
- [ ] API 响应中敏感字段已遮挡
- [ ] 密码存储用 bcrypt（非明文或 MD5）

---

## 11. 幂等性设计

### 设计表（架构师填入 ARCHITECTURE.md）

| 场景 | 幂等方案 |
|------|---------|
| 创建操作 | 幂等键（前端生成 UUID），后端去重表或唯一约束 |
| 更新操作 | 乐观锁（`WHERE version=?`），版本号不匹配返回 409 |
| 删除操作 | 软删除 + 唯一约束，重复删除返回 200（不报错） |
| 支付回调 | 订单状态机，已支付的订单重复回调忽略 |
| 消息消费 | 消费端去重表（message_id 唯一） |

### 实现要求（开发遵守）
- 创建接口：前端生成幂等键（UUID），后端唯一约束或去重表
- 更新接口：乐观锁 `WHERE version=?`，版本不匹配返回 409
- 删除接口：软删除，重复删除返回 200
- 支付回调：状态机校验，已处理的回调忽略
- 消息消费：消费端去重表（message_id 唯一约束）
- **禁止**：创建接口不做幂等，网络重试导致重复数据

### 审查要点
- [ ] 创建接口有幂等键 + 唯一约束
- [ ] 更新接口有乐观锁
- [ ] 支付回调有状态机防重复处理

---

## 使用场景

| 场景 | 怎么用 |
|------|--------|
| 架构师设计 | 参考"设计表"章节，逐项填入 ARCHITECTURE.md |
| 开发实现 | 参考"实现要求"章节，逐项编码 + 写测试 |
| QA/审查 | 参考"审查要点"章节，逐项确认 |
| pipeline-check.sh | 检查 ARCHITECTURE.md 是否包含 11 项设计表 |

---

# Skill: feature-tagging

# 功能点标签系统 Skill

> 本 Skill 定义全流程功能点打标规范，贯穿 Pipeline 所有阶段。

---

## 1. 标签体系

### 1.1 标签状态定义

| 标签 | 含义 | 阶段 | 打标方式 |
|------|------|------|---------|
| `PRD-待确认` | PRD 已编写，等待用户确认 | 1 | 自动 |
| `PRD-已确认` | 用户已确认 PRD | 1.6 | 人工确认 |
| `UI/UX-设计中` | UI/UX 设计进行中 | 1.7 | 自动 |
| `UI/UX-设计完成` | UI/UX 设计完成，含 HTML 原型 | 1.7 | 自动 |
| `PRD-已细化` | PRD 已根据 UI/UX 反向细化 | 1.8 | 自动 |
| `PRD-细化确认` | 细化 PRD 经人工确认 | 1.9 | 人工确认 |
| `技术方案-待确认` | 架构方案已产出，待确认 | 2 | 自动 |
| `技术方案-已确认` | 架构方案经评审确认 | 2.5/2.6 | 人工确认 |
| `开发-进行中` | 任务开发中 | 6 | 自动 |
| `开发-完成` | 开发任务完成 | 6 | 自动 |
| `测试-通过` | 测试验证通过 | 8 | 自动 |
| `测试-失败` | 测试未通过，需返工 | 8 | 自动 |
| `验收-通过` | PM 验收通过 | 8.5 | 人工确认 |
| `交付-完成` | 全流程交付完成 | 9 | 自动 |

### 1.2 标签状态机

```
PRD-待确认 → PRD-已确认 → UI/UX-设计中 → UI/UX-设计完成
    → PRD-已细化 → PRD-细化确认 → 技术方案-待确认 → 技术方案-已确认
    → 开发-进行中 → 开发-完成 → 测试-通过 → 验收-通过 → 交付-完成
                                          ↘ 测试-失败 → 开发-进行中（回退）
```

合法转换规则：
- 只能按顺序前进，不能跳跃
- 回退仅限：`测试-失败` → `开发-进行中`
- `人工确认`类标签必须等待人工操作

---

## 2. 存储格式

### 2.1 功能点标签文件
存储路径：`pipeline/feature-tags.json`

```json
{
  "version": "1.0",
  "project": "{项目名}",
  "last_updated": "2025-05-15T10:30:00Z",
  "features": {
    "REQ-001": {
      "title": "用户登录",
      "status": "PRD-已确认",
      "history": [
        {"status": "PRD-待确认", "timestamp": "2025-05-15T09:00:00Z", "operator": "auto", "phase": "1"},
        {"status": "PRD-已确认", "timestamp": "2025-05-15T10:30:00Z", "operator": "manual", "phase": "1.6", "confirmed_by": "user"}
      ]
    },
    "REQ-002": {
      "title": "数据导出",
      "status": "开发-进行中",
      "history": [
        {"status": "PRD-待确认", "timestamp": "...", "operator": "auto", "phase": "1"},
        {"status": "PRD-已确认", "timestamp": "...", "operator": "manual", "phase": "1.6", "confirmed_by": "user"},
        {"status": "UI/UX-设计中", "timestamp": "...", "operator": "auto", "phase": "1.7"},
        {"status": "UI/UX-设计完成", "timestamp": "...", "operator": "auto", "phase": "1.7"},
        {"status": "PRD-已细化", "timestamp": "...", "operator": "auto", "phase": "1.8"},
        {"status": "PRD-细化确认", "timestamp": "...", "operator": "manual", "phase": "1.9", "confirmed_by": "user"},
        {"status": "技术方案-待确认", "timestamp": "...", "operator": "auto", "phase": "2"},
        {"status": "技术方案-已确认", "timestamp": "...", "operator": "manual", "phase": "2.5"},
        {"status": "开发-进行中", "timestamp": "...", "operator": "auto", "phase": "6"}
      ]
    }
  },
  "pipeline_status": {
    "current_phase": "6",
    "phase_tags": {
      "0": "completed",
      "1": "completed",
      "1.6": "completed",
      "1.7": "completed",
      "1.8": "completed",
      "1.9": "completed",
      "2": "completed",
      "2.5": "completed",
      "5": "completed",
      "5.5": "completed",
      "6": "in_progress"
    }
  }
}
```

### 2.2 Pipeline 阶段标签

| 标签 | 含义 |
|------|------|
| `pending` | 阶段未开始 |
| `in_progress` | 阶段进行中 |
| `completed` | 阶段已完成 |
| `blocked` | 阶段被阻塞 |
| `skipped` | 阶段被跳过（规模裁剪） |

---

## 3. 自动打标规则

### 3.1 阶段完成时自动打标

| 阶段完成 | 自动操作 |
|---------|---------|
| 阶段 1 完成 | 所有 REQ → `PRD-待确认` |
| 阶段 1.6 完成 | 用户确认的 REQ → `PRD-已确认` |
| 阶段 1.7 开始 | 所有 REQ → `UI/UX-设计中` |
| 阶段 1.7 完成 | 所有 REQ → `UI/UX-设计完成` |
| 阶段 1.8 完成 | 所有 REQ → `PRD-已细化` |
| 阶段 1.9 完成 | 用户确认后 → `PRD-细化确认` |
| 阶段 2 完成 | 所有 REQ → `技术方案-待确认` |
| 阶段 2.5/2.6 完成 | 所有 REQ → `技术方案-已确认` |
| 阶段 6 任务开始 | 对应 REQ → `开发-进行中` |
| 阶段 6 任务完成 | 对应 REQ → `开发-完成` |
| 阶段 8 测试通过 | 对应 REQ → `测试-通过` |
| 阶段 8 测试失败 | 对应 REQ → `测试-失败` |
| 阶段 8.5 完成 | 对应 REQ → `验收-通过` |
| 阶段 9 完成 | 所有 REQ → `交付-完成` |

### 3.2 人工确认打标

需要人工确认的标签，协调者必须暂停并通知用户：
- `PRD-已确认`：阶段 1.6 用户审阅后
- `PRD-细化确认`：阶段 1.9 细化 PRD 审阅后
- `技术方案-已确认`：阶段 2.5/2.6 评审后
- `验收-通过`：阶段 8.5 PM 验收后

---

## 4. 进度看板

每次标签变更时，自动生成进度摘要（追加到 `pipeline/feature-tags-summary.md`）：

```markdown
# 功能点进度看板
> 最后更新：2025-05-15 10:30:00

| REQ | 功能 | 当前状态 | 阶段 |
|-----|------|---------|------|
| REQ-001 | 用户登录 | PRD-已确认 | 1.6 ✅ |
| REQ-002 | 数据导出 | 开发-进行中 | 6 🔄 |
| REQ-003 | 权限管理 | 测试-通过 | 8 ✅ |

**统计**：
- 总功能点：3
- 已完成：1（33%）
- 进行中：1（33%）
- 待开发：1（33%）
```

---

## 5. 脚本集成

### 5.1 标签操作脚本
```bash
# 初始化标签（阶段1完成后调用）
bash scripts/feature-tags.sh init <项目目录>

# 更新标签（每阶段完成后调用）
bash scripts/feature-tags.sh update <项目目录> <阶段> <新状态>

# 人工确认（等待用户操作）
bash scripts/feature-tags.sh confirm <项目目录> <REQ编号>

# 生成进度看板
bash scripts/feature-tags.sh summary <项目目录>

# 检查所有标签是否一致
bash scripts/feature-tags.sh check <项目目录>
```

### 5.2 pipeline-check.sh 集成
在阶段检查时增加标签一致性验证：
- 阶段 N 的检查逻辑中，验证所有 REQ 的标签 ≥ 该阶段对应的标签状态
- 不一致则报 🟡 警告

---

# Skill: interactive-html

# Skill: 交互式 HTML 文档生成

## 用途
生成单文件、自包含、可交互的 HTML 文档。适用于任何需要结构化展示的场景。

### Pipeline 内适用场景
| 场景 | 阶段 | 产出 |
|------|------|------|
| PRD 交互版 | 1 | docs/prd.html — 需求可点击查看详情 |
| 架构文档交互版 | 2 | docs/architecture.html — 模块可点击展开 |
| 测试报告交互版 | 8 | docs/test-report.html — 用例可点击展开 |
| 验收报告交互版 | 9 | docs/acceptance-report.html |
| 用户文档 | 10 | README / USER-GUIDE / DEPLOYMENT / CONFIG-GUIDE |
| Pipeline 自身文档 | 任意 | PIPELINE-FULL.html 等内部文档 |

凡是需要给人看的结构化文档，都可以用这个 skill 生成。

## 核心原则
- **单文件**：内联 CSS + JS，无外部依赖（Mermaid CDN 除外）
- **可交互**：关键内容点击 → 模态框详情，不是静态页面
- **易读性**：金字塔结构、分层阅读、零假设知识
- **暗色主题**：GitHub Dark 风格，护眼且专业

---

## 一、HTML 模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{文档标题}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
/* CSS 变量 + 组件样式（见第二节） */
</style>
</head>
<body>

<!-- Hero 区 -->
<div class="hero">
  <h1>{主标题}</h1>
  <p>{副标题/一句话描述}</p>
  <div class="badge-row">
    <span class="badge badge-blue">{关键数字1}</span>
    <span class="badge badge-green">{关键数字2}</span>
  </div>
  <p class="hint">点击任意卡片/节点 查看详情</p>
</div>

<div class="container">
  <!-- 侧边栏目录（可选） -->
  <nav class="toc" id="toc"></nav>

  <!-- 各 Section 内容 -->
  <h2 class="section-title"><span class="num">01</span> {章节名}</h2>
  <!-- 卡片网格 / 流程图 / 表格 -->

  <!-- 模态框（隐藏，点击触发） -->
  <div class="modal-overlay" id="m-xxx">
    <div class="modal">
      <div class="modal-header">
        <h2>{标题}</h2>
        <button class="modal-close" onclick="closeModal('m-xxx')">&times;</button>
      </div>
      <div class="modal-body">
        <!-- 详情内容 -->
      </div>
    </div>
  </div>
</div>

<footer>{生成时间 / 版本信息}</footer>

<script>
/* JS 交互逻辑（见第四节） */
</script>
</body>
</html>
```

---

## 二、CSS 样式系统

### 2.1 颜色变量（:root）

```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface2: #1c2129;
  --border: #30363d;
  --text: #e6edf3;
  --muted: #8b949e;
  --accent: #58a6ff;    /* 蓝色 - 主色 */
  --green: #3fb950;     /* 绿色 - 成功/计划 */
  --yellow: #d29922;    /* 黄色 - 警告 */
  --red: #f85149;       /* 红色 - 错误/大型 */
  --purple: #bc8cff;    /* 紫色 - 需求/PM */
  --orange: #f0883e;    /* 橙色 - 测试 */
  --cyan: #39d2c0;      /* 青色 - 开发/UX */

  /* 发光效果 */
  --glow-accent: 0 0 12px rgba(88,166,255,0.4);
  --glow-green: 0 0 12px rgba(63,185,80,0.4);
  --glow-purple: 0 0 12px rgba(188,140,255,0.4);
  --glow-orange: 0 0 12px rgba(240,136,62,0.4);
  --glow-red: 0 0 12px rgba(248,81,73,0.4);
  --glow-cyan: 0 0 12px rgba(57,210,192,0.4);
}
```

### 2.2 可点击卡片

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.25s;
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--purple));
  opacity: 0;
  transition: opacity 0.25s;
}
.card:hover {
  border-color: var(--accent);
  box-shadow: var(--glow-accent);
  transform: translateY(-2px);
}
.card:hover::before { opacity: 1; }

/* 点击提示（hover 时显示） */
.card .click-hint {
  position: absolute;
  top: 10px; right: 12px;
  font-size: 0.7em;
  color: var(--accent);
  opacity: 0;
  transition: opacity 0.25s;
}
.card:hover .click-hint { opacity: 1; }
```

### 2.3 可点击标签（行内）

```css
.click-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 0.82em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}
.click-tag:hover { transform: scale(1.05); }

/* 颜色变体 */
.click-tag-accent { background: rgba(88,166,255,0.15); color: var(--accent); border-color: rgba(88,166,255,0.3); }
.click-tag-accent:hover { box-shadow: var(--glow-accent); border-color: var(--accent); }
.click-tag-green  { background: rgba(63,185,80,0.15); color: var(--green); border-color: rgba(63,185,80,0.3); }
.click-tag-green:hover  { box-shadow: var(--glow-green); border-color: var(--green); }
.click-tag-purple { background: rgba(188,140,255,0.15); color: var(--purple); border-color: rgba(188,140,255,0.3); }
.click-tag-purple:hover { box-shadow: var(--glow-purple); border-color: var(--purple); }
.click-tag-orange { background: rgba(240,136,62,0.15); color: var(--orange); border-color: rgba(240,136,62,0.3); }
.click-tag-orange:hover { box-shadow: var(--glow-orange); border-color: var(--orange); }
.click-tag-red    { background: rgba(248,81,73,0.15); color: var(--red); border-color: rgba(248,81,73,0.3); }
.click-tag-red:hover    { box-shadow: var(--glow-red); border-color: var(--red); }
.click-tag-cyan   { background: rgba(57,210,192,0.15); color: var(--cyan); border-color: rgba(57,210,192,0.3); }
.click-tag-cyan:hover   { box-shadow: var(--glow-cyan); border-color: var(--cyan); }
```

### 2.4 模态框

```css
.modal-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.7);
  z-index: 1000;
  backdrop-filter: blur(4px);
  overflow-y: auto;
  padding: 40px 20px;
}
.modal-overlay.active { display: block; }

.modal {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  max-width: 960px;
  margin: 0 auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.modal-header {
  padding: 24px 28px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-close {
  background: none;
  border: 1px solid var(--border);
  color: var(--muted);
  width: 32px; height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1em;
  transition: all 0.2s;
}
.modal-close:hover { border-color: var(--red); color: var(--red); }
.modal-body {
  padding: 24px 28px 28px;
  max-height: 75vh;
  overflow-y: auto;
}
.modal-body h3 { color: var(--accent); margin: 20px 0 10px; }
```

### 2.5 其他组件

```css
/* 表格 */
table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 0.9em; }
th { background: var(--surface); font-weight: 600; padding: 10px 12px; border: 1px solid var(--border); color: var(--accent); }
td { padding: 10px 12px; border: 1px solid var(--border); }
tr:hover td { background: rgba(88,166,255,0.04); }

/* 代码块 */
pre { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 18px; overflow-x: auto; font-size: 0.86em; }
code { font-family: 'SF Mono','Fira Code','Cascadia Code',monospace; font-size: 0.9em; }
:not(pre)>code { background: rgba(88,166,255,0.1); padding: 2px 6px; border-radius: 4px; color: var(--accent); }

/* 提示框 */
.callout { border-left: 4px solid; padding: 12px 16px; border-radius: 0 8px 8px 0; margin: 14px 0; }
.callout strong { display: block; margin-bottom: 4px; }
.callout-info    { border-color: var(--accent); background: rgba(88,166,255,0.08); }
.callout-warn    { border-color: var(--yellow); background: rgba(210,153,34,0.08); }
.callout-error   { border-color: var(--red); background: rgba(248,81,73,0.08); }
.callout-success { border-color: var(--green); background: rgba(63,185,80,0.08); }

/* Mermaid 容器 */
.mermaid-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  margin: 16px 0;
  overflow-x: auto;
}
.mermaid-wrap .dtitle {
  font-size: 0.8em;
  color: var(--muted);
  margin-bottom: 12px;
  text-align: center;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 脉冲动画（引导用户点击） */
@keyframes glow {
  0%,100% { box-shadow: 0 0 5px rgba(88,166,255,0.2) }
  50% { box-shadow: 0 0 15px rgba(88,166,255,0.5) }
}
.pulse { animation: glow 2s ease-in-out infinite; }

/* 响应式 */
@media(max-width: 768px) {
  .card-grid { grid-template-columns: 1fr; }
  .modal { margin: 10px; }
  .modal-body { padding: 16px; }
}
```

---

## 三、内容组织模式

### 3.1 卡片网格（最常用）

```html
<div class="card-grid">
  <div class="card" onclick="openModal('m-xxx')">
    <div class="click-hint">点击查看详情</div>
    <div class="card-title"><span class="tag tag-pm">PM</span> 需求分析</div>
    <div class="card-body">和用户讨论需求，产出 PRD.md</div>
  </div>
  <!-- 更多卡片... -->
</div>
```

### 3.2 流程节点行

```html
<div class="flow-row">
  <span class="flow-node req" onclick="openModal('m-stage0')">0 启动</span>
  <span class="flow-arrow">→</span>
  <span class="flow-node req" onclick="openModal('m-stage1')">1 PRD</span>
  <span class="flow-arrow">→</span>
  <span class="flow-node des" onclick="openModal('m-stage2')">2 架构</span>
</div>
```

流程节点颜色分类：
- `req`（紫色）= 需求相关
- `des`（蓝色）= 设计相关
- `plan`（绿色）= 计划/分解
- `dev`（青色）= 开发相关
- `test`（橙色）= 测试相关
- `del`（红色）= 交付/验收

### 3.3 可点击标签（行内交叉引用）

```html
执行者：<span class="click-tag click-tag-purple" onclick="openModal('m-pm')">PM</span>
```

### 3.4 表格（数据对比）

直接用 `<table>`，不需要额外 class。hover 行高亮已内置。

### 3.5 代码块

```html
<pre><code>npm install && npm run build</code></pre>
```

### 3.6 提示框

```html
<div class="callout callout-error">
  <strong>禁止</strong>
  不允许的操作说明
</div>
```

### 3.7 Mermaid 图表

```html
<div class="mermaid-wrap">
  <div class="dtitle">图表标题</div>
  <pre class="mermaid">
graph LR
    A[开始] --> B[处理]
    B --> C[结束]
  </pre>
</div>
```

---

## 四、JavaScript 交互系统

### 4.1 Mermaid 初始化

```javascript
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  themeVariables: {
    darkMode: true,
    background: '#161b22',
    primaryColor: '#58a6ff',
    primaryTextColor: '#e6edf3',
    primaryBorderColor: '#30363d',
    lineColor: '#8b949e',
    secondaryColor: '#bc8cff',
    tertiaryColor: '#3fb950',
    fontSize: '13px',
    fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif'
  },
  flowchart: { curve: 'basis', padding: 16 },
  stateDiagram: { useMaxWidth: true }
});
```

### 4.2 模态框控制

```javascript
function openModal(id) {
  document.getElementById(id).classList.add('active');
  document.body.style.overflow = 'hidden';
  // 模态框内的 Mermaid 重新渲染
  setTimeout(() => {
    const modal = document.getElementById(id);
    const unprocessed = modal.querySelectorAll('.mermaid:not([data-processed])');
    if (unprocessed.length > 0) {
      mermaid.run({ nodes: unprocessed });
    }
  }, 50);
}

function closeModal(id) {
  document.getElementById(id).classList.remove('active');
  document.body.style.overflow = '';
}

// 点击遮罩层关闭
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
});

// Escape 键关闭
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(m => {
      m.classList.remove('active');
    });
    document.body.style.overflow = '';
  }
});
```

### 4.3 代码复制按钮（可选增强）

```javascript
document.querySelectorAll('pre').forEach(pre => {
  const btn = document.createElement('button');
  btn.textContent = '复制';
  btn.style.cssText = 'position:absolute;top:8px;right:8px;padding:4px 10px;border-radius:6px;background:var(--surface2);border:1px solid var(--border);color:var(--muted);cursor:pointer;font-size:0.75em;';
  btn.onclick = () => {
    navigator.clipboard.writeText(pre.textContent);
    btn.textContent = '已复制';
    btn.style.color = 'var(--green)';
    setTimeout(() => { btn.textContent = '复制'; btn.style.color = 'var(--muted)'; }, 2000);
  };
  pre.style.position = 'relative';
  pre.appendChild(btn);
});
```

### 4.4 侧边栏目录生成（可选增强）

```javascript
function buildTOC() {
  const toc = document.getElementById('toc');
  if (!toc) return;
  const titles = document.querySelectorAll('.section-title');
  titles.forEach((t, i) => {
    const id = 'section-' + i;
    t.id = id;
    const a = document.createElement('a');
    a.href = '#' + id;
    a.textContent = t.textContent;
    a.style.cssText = 'display:block;padding:6px 0;color:var(--muted);font-size:0.85em;text-decoration:none;border-bottom:1px solid var(--border);';
    a.onmouseenter = () => a.style.color = 'var(--accent)';
    a.onmouseleave = () => a.style.color = 'var(--muted)';
    toc.appendChild(a);
  });
}
buildTOC();
```

### 4.5 术语表 Tooltip（可选增强）

```javascript
const glossary = {
  'REQ-xxx': '需求编号，PRD 中每个功能的唯一标识',
  'acpx': 'Claude Code 的 headless 模式调度命令',
  'flock': 'Linux 文件锁，用于并发安全'
};
document.querySelectorAll('.term').forEach(el => {
  const term = el.textContent;
  if (glossary[term]) {
    el.title = glossary[term];
    el.style.borderBottom = '1px dashed var(--muted)';
    el.style.cursor = 'help';
  }
});
```

---

## 五、易读性要求

### 5.1 结构层
- **金字塔原则**：结论先行，细节在后。每个 Section 开头一句话总结
- **分层阅读**：概览（卡片/流程图）→ 详情（模态框）→ 原理（模态框内的 Mermaid/代码）
- **目录锚点**：长文档必须有 TOC（可用第四节的自动生成方案）

### 5.2 内容层
- **零假设知识**：不假设读者知道背景，第一段写"这是什么"
- **术语表**：专有名词用 `<span class="term">` 包裹，hover 显示解释
- **代码可复制**：代码块有复制按钮
- **错误优先**：常见报错 + 解决方案放在醒目位置
- **What-Why-How**：先说"是什么"，再说"为什么"，最后说"怎么用"

### 5.3 格式层
- 表格代替大段文字
- 步骤用有序列表
- 每个模态框内容不超过一屏（~30行），超过就拆子章节
- 代码示例用 `代码块`，不是纯文本

### 5.4 语言层
- 中文为主，技术术语保持英文（"API" 不说 "应用程序接口"）
- 禁用"此处省略"、"详见xxx" — 直接放内容
- 一个句子只说一件事

---

## 六、生成检查清单

生成 HTML 文件后，逐项检查：

- [ ] 单文件、内联 CSS + JS，无外部依赖（Mermaid CDN 除外）
- [ ] 暗色主题，颜色变量统一
- [ ] 可点击元素有 hover 发光效果（`box-shadow` + `translateY`）
- [ ] 模态框支持 Escape 关闭 + 点击外部关闭
- [ ] 模态框内 Mermaid 图表自动渲染
- [ ] 代码块有复制按钮
- [ ] 长文档有侧边栏 TOC
- [ ] 术语有 tooltip 解释
- [ ] 表格/代码块/提示框样式正确
- [ ] 移动端响应式（`@media max-width: 768px`）
- [ ] 每个模态框内容不超过一屏
- [ ] 无"详见xxx"跳转式写法
- [ ] 中文为主，技术术语保持英文

---

# Skill: prd-refinement

# PRD 反向细化 Skill

> 本 Skill 用于阶段 1.8（PRD 反向细化），根据 UI/UX 设计产出将 PRD 从"功能描述"细化为完整文档。

---

## 1. 核心目标

将阶段 1 产出的原始 PRD（功能描述级别）结合阶段 1.7 的 UI/UX 设计成果，补充交互细节、边界情况、文案规范、异常处理，形成开发可直接使用的完整 PRD。

---

## 2. 细化维度（4 个维度全覆盖）

### 2.1 交互细节补充
对照 UI/UX 设计和 HTML 原型，为每个 REQ 补充：
- **操作路径**：用户从哪个入口进入，每一步的操作描述
- **交互方式**：点击/拖拽/滑动/快捷键
- **反馈时机**：操作后何时给反馈（即时/延迟/异步通知）
- **组件行为**：下拉刷新、无限滚动、分页、排序、筛选等
- **键盘交互**：Tab 顺序、Enter 触发、Esc 关闭
- **手势操作**（移动端）：左滑删除、下拉刷新、双指缩放

### 2.2 边界情况补充
为每个 REQ 识别并补充：
- **数据边界**：空数据/超大数据/特殊字符/超长文本/负数/零
- **状态边界**：未登录/无权限/已过期/并发冲突/离线
- **时序边界**：快速重复点击/网络延迟/操作超时/异步操作未完成时切换页面
- **设备边界**：小屏设备/弱网/横竖屏切换/浏览器兼容性

### 2.3 文案规范
为每个 REQ 定义：
- **页面标题**：格式统一（动词+名词 或 名词短语）
- **按钮文案**：动作明确（"提交"而非"确定"），字数 ≤4 字
- **提示文案**：成功/失败/警告的统一句式
- **占位符文案**：引导性描述而非空提示
- **空状态文案**：原因说明 + 引导操作
- **错误文案**：具体原因 + 解决建议（非"系统错误"）

### 2.4 异常处理路径
为每个 REQ 补充完整异常路径：
- **输入校验异常**：字段级别校验规则 + 错误提示位置 + 实时/提交时校验策略
- **业务规则异常**：业务校验失败的提示 + 允许的恢复操作
- **网络异常**：超时/断网的重试策略 + 数据缓存策略
- **服务端异常**：500 错误的兜底展示 + 错误上报
- **权限异常**：未登录跳转 + 无权限提示 + 功能降级方案

---

## 3. 细化执行流程

### Step 1：读取原始 PRD
- 加载阶段 1 产出的 PRD.md
- 提取所有 REQ-xxx 功能点

### Step 2：读取 UI/UX 设计产出
- 加载 UI-UX-DESIGN.md（阶段 1.7 产出）
- 加载 docs/ui-prototype.html（HTML 原型）
- 加载 prd-refinement-notes.md（UI/UX 设计师标记的待细化项）

### Step 3：逐 REQ 细化
对每个 REQ-xxx：
1. 对照 UI/UX 设计，补充 4 个维度的内容
2. 标记新增内容为 `[UI/UX细化]` 前缀，便于人工审查
3. 标记潜在冲突或不确定项为 `[待确认]` 前缀

### Step 4：生成细化 PRD
- 输出为 `PRD-REFINED.md`（保留原始 PRD 结构，追加细化内容）
- 生成 `prd-diff.md`（变更对比：原始 → 细化，便于审查）

### Step 5：更新功能点标签
- 所有经过细化的 REQ，标签从 `PRD-已确认` → `PRD-已细化`

---

## 4. 细化 PRD 格式规范

每个 REQ 细化后的格式：

```markdown
### REQ-xxx: {功能名称}

{原始描述}

**验收标准**：
- {原始验收标准}

#### [UI/UX细化] 交互细节
- 操作路径：{入口} → {步骤1} → {步骤2} → {结果}
- 交互方式：{点击/拖拽/...}
- 反馈时机：{即时/延迟}
- 组件行为：{分页/滚动/筛选}

#### [UI/UX细化] 边界情况
- {边界场景1} → {处理方式}
- {边界场景2} → {处理方式}

#### [UI/UX细化] 文案规范
- 页面标题：{文案}
- 按钮：{文案}
- 成功提示：{文案}
- 错误提示：{文案}

#### [UI/UX细化] 异常处理
- 输入校验：{规则} → {提示}
- 网络异常：{重试策略} → {兜底展示}
- 权限异常：{跳转/提示}

#### [待确认] 需人工确认项
- {不确定的设计决策}
```

---

## 5. 质量检查项

- [ ] 每个 REQ 都有 4 个细化维度
- [ ] 新增内容有 `[UI/UX细化]` 标记
- [ ] 不确定项有 `[待确认]` 标记
- [ ] prd-diff.md 变更对比清晰
- [ ] 文案规范不出现"确定""系统错误"等模糊词
- [ ] 每个 REQ 至少覆盖 2 个边界情况
- [ ] 每个 REQ 至少覆盖 3 条异常处理路径
- [ ] 功能点标签已更新为 `PRD-已细化`

---

# Skill: ui-ux-design

# UI/UX 设计执行 Skill

> 本 Skill 用于阶段 1.7（UI/UX 设计），指导 agent 进行专业化的 UI/UX 设计并生成 HTML 原型。

---

## 1. 角色定义

你是一名资深 UI/UX 设计师，同时具备前端工程能力。你的任务不是简单翻译 PRD，而是从用户视角出发，结合技术特性进行深度设计。

---

## 2. 技术特性分析框架（强制执行）

每个 UI/UX 设计必须覆盖以下 8 个维度，缺一不可：

### 2.1 技术栈适配
- 确认项目使用的前端框架（React/Vue/Next.js/小程序等）
- 组件库选型（Ant Design/Material UI/Shadcn/Element Plus 等）
- 设计决策必须与选定的技术栈一致

### 2.2 设计系统
- 色彩系统：主色、辅色、语义色（成功/警告/错误/信息）、中性色阶
- 字体规范：字号层级（h1-h6/body/caption）、字重、行高
- 间距规范：基于 4px/8px 网格的间距体系
- 圆角规范：不同组件的圆角大小
- 阴影层级：卡片、弹窗、悬浮等不同阴影

### 2.3 组件设计
- 原子组件：Button、Input、Select、Modal、Toast、Badge 等
- 分子组件：SearchBar、Card、FormItem、TableCell 等
- 有机体组件：Header、Sidebar、DataTable、Form 等
- 每个组件需定义：正常/悬浮/激活/禁用/加载/错误 六种状态

### 2.4 响应式策略
- 断点定义：Mobile（<768px）、Tablet（768-1024px）、Desktop（>1024px）
- 布局变化策略：堆叠→并排、隐藏→折叠、简化→完整
- 触摸适配：最小可点击区域 44px、手势支持

### 2.5 暗黑模式
- 色彩反转策略（HSL 调整而非简单反色）
- 图片/图标适配方案
- 对比度保证（WCAG AA 标准）

### 2.6 动效设计
- 页面转场：淡入淡出/滑动/缩放
- 交互反馈：按钮点击涟漪、加载骨架屏、操作成功动画
- 列表动画：进入/退出/重排
- 动效时长规范：微交互 100-200ms，页面转场 200-400ms

### 2.7 可访问性（Accessibility）
- 对比度 ≥ 4.5:1（正文）、≥ 3:1（大文本）
- 所有交互元素可通过键盘操作
- 图片/图标有 aria-label
- 表单有 label 关联
- 焦点管理（Modal 打开时焦点锁定）

### 2.8 异常与边界
- 空状态设计（无数据、无结果、无权限）
- 加载状态设计（骨架屏、进度条、骨架按钮）
- 错误状态设计（网络错误、表单校验、系统异常）
- 操作反馈（成功/失败 Toast、确认弹窗）

---

## 3. HTML 原型生成规范

### 3.1 生成要求
设计完成后，**必须**自动生成一个 HTML 功能页面，要求：
- 单文件、内联 CSS、无外部依赖
- 包含所有核心页面/流程
- 展示组件的不同状态（正常/空/加载/错误）
- 交互可点击（Tab 切换、弹窗开关、表单验证）
- 响应式布局（至少 Desktop + Mobile 两种布局）

### 3.2 HTML 结构模板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{项目名} — UI/UX 设计原型</title>
  <style>
    /* CSS 变量（设计系统 Token） */
    :root {
      --color-primary: #...;
      --color-success: #...;
      --color-warning: #...;
      --color-error: #...;
      --color-bg: #...;
      --color-text: #...;
      --font-size-h1: ...;
      --spacing-xs: 4px;
      --radius-sm: 4px;
      /* ... */
    }
    /* 响应式、组件样式 */
  </style>
</head>
<body>
  <!-- 导航栏 -->
  <!-- 核心页面（Tab 切换展示多页面） -->
  <!-- 组件状态展示区 -->
  <!-- 异常状态展示区 -->
  
  <script>
    // Tab 切换、弹窗控制、表单验证等交互逻辑
  </script>
</body>
</html>
```

### 3.3 必须展示的模块
1. **核心流程页面**：用户最常用的 2-3 个流程完整展示
2. **组件状态矩阵**：关键组件的 6 种状态
3. **异常场景**：空状态、加载中、错误页、无权限
4. **响应式演示**：桌面端和移动端布局

---

## 4. PRD 细化触发条件

UI/UX 设计完成后，自动触发 PRD 反向细化，条件：
- UI/UX 设计中发现了 PRD 未明确的交互细节
- 存在需要补充的边界情况
- 文案规范需要统一
- 异常处理路径 PRD 未覆盖

细化内容写入 `prd-refinement-notes.md`，供阶段 1.8 使用。

---

## 5. 产出物清单

| 产出物 | 说明 |
|--------|------|
| UI-UX-DESIGN.md | 完整的 UI/UX 设计文档（含 8 维度分析） |
| docs/ui-prototype.html | 可交互的 HTML 原型页面 |
| prd-refinement-notes.md | 触发 PRD 细化的补充说明 |

---

## 6. 质量检查项

- [ ] 8 个技术特性维度全部覆盖
- [ ] HTML 原型包含核心流程、组件状态、异常场景
- [ ] HTML 原型可交互（Tab/弹窗/表单验证）
- [ ] 响应式至少覆盖 Desktop + Mobile
- [ ] 设计系统 Token 定义完整（色彩/字体/间距/圆角/阴影）
- [ ] 每个组件定义了 6 种状态
- [ ] 空状态/加载/错误有明确设计
- [ ] PRD 细化说明已产出
