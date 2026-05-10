# agent-discipline — Agent 执行纪律条款

## 是什么

为 agent 提供标准化的执行纪律条款。派任务时附加到消息末尾，确保 agent 严格按标准执行。

**本 skill 无任何外部依赖，可独立使用。**

## 触发条件

向 agent 派发任务时自动触发。

## 使用场景

- 向 agent 派发任何任务（流水线内/外）
- 新建 agent 后配置执行纪律
- agent 产出质量不达标，需要加强约束

## 执行流程

```
1. 确定目标 agent 的 agent-id
2. 读取 rules/{agent-id}.md → 不存在则按优先级匹配：
   - pm → rules/pm.md
   - architect → rules/architect.md
   - backend/frontend/dev3 → rules/developer.md
   - 其他 → rules/default.md
3. 将条款内容原样追加到任务消息末尾
```

## 角色映射

| agent-id | 条款文件 | 条款数 |
|----------|---------|--------|
| pm | rules/pm.md | 5 |
| architect | rules/architect.md | 5 |
| backend/frontend/dev3 | rules/developer.md | 5 |
| startup-helper | rules/startup-helper.md | 6 |
| qa | rules/qa.md | 7 |
| [其他所有] | rules/default.md | 4 |

## 约束

1. 派任务不附条款 = 违规
2. 条款不可删减或改写
3. 没有专属条款的角色必须用 default.md
4. 协调者可以加更多要求，但不能减少

## 扩展

在 `rules/` 下创建 `{agent-id}.md`，格式：⚠️ 开头 + 编号条款。

## 文件结构

```
agent-discipline/
├── SKILL.md
└── rules/
    ├── default.md
    ├── pm.md
    ├── architect.md
    ├── developer.md
    ├── startup-helper.md
    └── qa.md
```
