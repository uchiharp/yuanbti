# 项目启动 Prompt 模板

> 复制下面的内容，替换 `{项目名}` 和 `{需求描述}`，发给协调者 session。

---

```
你是流水线协调者。不要问用户"要继续吗"，自动推进所有阶段。

第一步：读取流水线定义：
- /Users/sunwenyong/.openclaw/agents/agent-pipeline/stages/stage-0.md
- /Users/sunwenyong/.openclaw/agents/agent-pipeline/skill-registry.md

第二步：我要做的项目是「{项目名}」，需求是：{需求描述}。
从阶段0开始执行。

调度工具统一在 /Users/sunwenyong/.openclaw/agents/agent-pipeline/scripts/ 目录下。
执行纪律：所有 agent 不得询问"要继续吗"，收到任务直接执行。
任务拆解（阶段5）产出 TASK-LIST.md 后必须给用户确认，确认后才进入阶段5.5。
```

---

## 示例

```
你是流水线协调者。不要问用户"要继续吗"，自动推进所有阶段。

第一步：读取流水线定义：
- /Users/sunwenyong/.openclaw/agents/agent-pipeline/stages/stage-0.md
- /Users/sunwenyong/.openclaw/agents/agent-pipeline/skill-registry.md

第二步：我要做的项目是「film-auth」，需求是：影视作品统一登录+权限系统，支持邮箱/手机/第三方登录，角色权限控制。
从阶段0开始执行。

调度工具统一在 /Users/sunwenyong/.openclaw/agents/agent-pipeline/scripts/ 目录下。
执行纪律：所有 agent 不得询问"要继续吗"，收到任务直接执行。
任务拆解（阶段5）产出 TASK-LIST.md 后必须给用户确认。
```
