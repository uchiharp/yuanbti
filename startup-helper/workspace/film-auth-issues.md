# film-auth 已知问题清单

## 🔴 A 类：前后端不匹配（导致功能不可用）

### A1. 数据库缺少权限数据（影响最大）
- **问题：** super_admin 角色只有 9 个权限，缺少以下权限：
  - `auth:app:read` / `auth:app:manage` — 应用管理页面完全不可见
  - `auth:project:manage` — 新建/编辑/删除项目按钮不可见
  - `auth:permission:manage` — 新建/编辑/删除权限、权限模板按钮不可见
- **PRD 定义：** super_admin 应拥有所有权限
- **影响：** 11 个 E2E 测试失败（应用管理 7 个 + 项目创建/删除 2 个 + 权限创建/删除 2 个）
- **修复：** 在数据库补全权限数据 + 分配给 super_admin 角色
- **来源：** 后端开发没按 PRD 3.3.1（"超级管理员拥有所有权限"）实现

### A2. 前端 `fetchUserInfo` 调了不存在的接口
- **问题：** 前端 `user.ts` 调 `GET /auth/verify`，但后端原本没有这个接口
- **PRD/技术方案定义：**
  - 服务间接口：`GET /api/internal/token/verify`（已实现为 `POST /external/v1/token/verify`）
  - 前端专用接口：PRD 没有明确定义
- **现状：** 我补了 `GET /api/v1/auth/verify`，但没按文档规范
- **修复方向：**
  - 方案1：前端改调已有的 `GET /api/v1/oauth/userinfo`（OAuth 接口，返回用户信息）
  - 方案2：保留 `/api/v1/auth/verify` 作为前端专用接口，但在 PRD 里补定义
- **影响：** 所有需要认证的页面首次加载时路由守卫都会调这个接口

### A3. 表单提交后 dialog 不关闭（8 个测试）
- **问题：** 创建角色/用户/权限模板等操作，提交后 el-dialog 不关闭
- **可能原因：**
  1. 后端接口报错（验证失败），前端没处理错误提示
  2. 前端表单必填字段和后端 DTO 不一致
  3. 后端返回格式不符合前端预期
- **需逐一排查：** role-form, user-form, permission-template-form
- **影响测试：** role-management（创建角色）、user-management（创建/批量创建）、permission-template（创建/删除）

### A4. token-blacklist.spec.ts 不适配 storageState
- **问题：** 测试 `goto('/login')` 但因为 storageState 里有 token，路由守卫自动跳转到 dashboard
- **根因：** 测试脚本假设无 token 状态访问 login 页面，但 Playwright 注入了 storageState
- **修复：** 这些测试需要用独立的 context（不继承 storageState）

### A5. error-page.spec.ts 测试逻辑与前端行为不符
- **问题1：** 404 测试期望页面含"404/找不到/not found"，但前端 `/:pathMatch(.*)` 重定向到 dashboard
- **问题2：** 未认证测试清除 cookies 后期望跳 login，但 localStorage 还有 token
- **来源：** 测试脚本没按前端实际路由配置写（前端没有专门的 404 页面）

---

## 🟡 B 类：PRD/技术方案与实现偏差

### B1. 技术栈偏差（前端整体）
- **PRD 定义：** React 18 + Shadcn UI + Zustand + React Router
- **实际实现：** Vue 3 + Element Plus + Pinia + Vue Router
- **说明：** 整个前端用 Vue 而不是 React，但功能上是等价的
- **建议：** 更新 PRD/技术方案文档，以实际实现为准

### B2. API 路径前缀
- **PRD 定义：** `/api/auth/*`, `/api/users/*`, `/api/roles/*` ...
- **实际实现：** `/api/v1/auth/*`, `/api/v1/users/*`, `/api/v1/roles/*` ...
- **说明：** 后端加了 `/v1` 版本前缀，PRD 没有定义
- **建议：** 更新 PRD 的 API 路径，或认为这是合理的版本管理

### B3. 服务间接口路径
- **PRD 定义：** `GET /api/internal/token/verify`
- **实际实现：** `POST /external/v1/token/verify`
- **差异：** 方法不同（GET vs POST）、前缀不同（/api/internal vs /external/v1）
- **建议：** 更新 PRD 以实际实现为准

### B4. 前端路由路径
- **PRD 定义：** `/users`, `/roles`, `/permissions`, `/apps`, `/audit`
- **实际实现：** `/admin/users`, `/admin/roles`, `/admin/permissions`, `/admin/apps`, `/admin/audit-logs`
- **说明：** 实际加了 `/admin` 前缀
- **建议：** 更新 PRD 以实际实现为准

### B5. 数据库差异（PostgreSQL vs MySQL）
- **PRD 定义：** PostgreSQL 16
- **实际实现：** MySQL（本地部署用的 MySQL）
- **说明：** 后端代码用 MyBatis Plus，兼容 MySQL 和 PostgreSQL，本地用 MySQL 可以
- **建议：** 生产环境应按 PRD 用 PostgreSQL

---

## 🟢 C 类：测试脚本问题

### C1. login.spec.ts 正常登录超时
- **问题：** 测试用户密码不正确或首次登录弹窗阻塞
- **根因：** setup 创建用户后密码被 resetPassword 改了，但 first_login=1 会弹修改密码弹窗
- **修复：** setup 里创建用户后设 `first_login=0` + `password_changed_at=NOW()`

### C2. 测试间状态污染
- **token-blacklist.spec.ts** 禁用用户但不恢复
- **profile-extended.spec.ts** 改密码但不改回
- **login 破坏性测试** 锁定测试账号
- **修复：** 每个破坏性测试需要 afterAll 恢复状态，或在 setup 里重置

### C3. waitForResponse 超时（3 个）
- **audit-log** 按 userId 筛选、**login-history** 按 userId 筛选、**user-management** 搜索
- **原因：** 测试脚本先 click 再 waitForResponse，但请求可能在 click 之前就发出了（因为 input change 触发了自动搜索）
- **修复：** 改用 Promise.race 或先设 waitForResponse 再 click

### C4. dashboard.spec.ts strict mode
- **问题：** `locator('text=仪表盘')` 匹配到 3 个元素
- **修复：** 用 `.first()` 或更精确的选择器如 `getByRole('heading')`

---

## 修复优先级

1. **A1** — 补权限数据（一次 SQL，修 11 个测试）
2. **A2** — 确认 verify 接口方案
3. **C1+C2** — 修复 setup 和测试状态管理
4. **A3** — 逐一排查 dialog 不关闭的原因
5. **A4+A5** — 修复测试脚本逻辑
6. **C3+C4** — 修复测试写法
7. **B 类** — 更新文档以实际实现为准
