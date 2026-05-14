# Pipeline 优化对比分析

> 对比 pipeline-optimization.md、film-auth-test-handbook.md 与现有实现的真实差距
> 日期：2026-05-14

---

## 一、pipeline-optimization.md 逐项评审

### 1.1 P0 项评审（声称"完全没有"）

| 声称缺失 | 实际情况 | 判定 |
|---------|---------|------|
| **性能测试** | qa-workflow SKILL.md 已有性能基准（API P95<200ms, 首屏<2s, 并发≥100），但**无自动化 gate rule 强制执行** | ⚠️ 有规范无执行，需加 gate |
| **CI/CD 集成** | 这不是 pipeline 的测试能力缺口，是部署自动化缺口。pipeline 本身就是 CI/CD 的替代方案（agent 驱动） | ❌ 不采纳，理由见下 |
| **测试数据隔离** | qa-review-workflow 9维评分已有"测试独立性"维度（10%权重），agent-discipline 有回归测试规则 | ⚠️ 有评审无自动检测，但不需要 gate rule |
| **代码风险自动分析** | riskforge 是外部 skill，我们的 qa-review-workflow 9维评分已覆盖风险识别（覆盖率、边界、异常、mock 合理性） | ❌ 不采纳，理由见下 |

**详细论证：**

**CI/CD 集成 — 不采纳**
- pipeline-optimization.md 把 CI/CD 和测试混在一起谈。我们的 pipeline 本身就是 CI/CD——agent 驱动的 9 阶段流水线 + 门禁脚本 + 自动评审
- `ci-cd-pipeline-builder` 这个 skill 是给没有 pipeline 的项目生成 GitHub Actions/Jenkins 配置用的，我们不需要
- 真正的问题是：pipeline 的门禁脚本是否自动执行？这是 Plugin 升级的问题，不是"缺 CI/CD"

**代码风险自动分析（riskforge）— 不采纳**
- riskforge 做的事：扫描代码 → 生成风险报告 → 推荐测试策略
- 我们的 qa-review-workflow 已经做了：9 维度评分 + 扣分制 + 否决条件
- riskforge 的优势是"基于代码自动分析"，但 LLM agent 本身就在读代码，风险分析已内置在评审 prompt 中
- 安装一个评分 1.98 的 skill 来替代我们已有的 9 维评分体系，不值得

### 1.2 P1 项评审（声称"有但不够强"）

| 声称不够强 | 实际情况 | 判定 |
|-----------|---------|------|
| **E2E 测试模式** | pipeline-optimization 说 `run-tests`"只跑命令"，但 qa-review-workflow 有完整 Playwright 3 轮评审流程 + ui-test skill | ❌ 差距被夸大 |
| **PRD→领域建模** | 确实没有 DDD 建模 skill，从 PRD 直接到架构设计有断层 | ✅ 值得采纳 |
| **设计系统自动化** | finder-ui 是项目特化的，不是通用设计系统 | ❌ 项目级，不进 pipeline |
| **竞品分析** | 无 | ❌ 不进 pipeline，是项目前期决策 |
| **头脑风暴** | 无 | ❌ 不进 pipeline，是需求阶段的方法论 |

**详细论证：**

**E2E 测试模式 — 不采纳（差距被夸大）**
- pipeline-optimization.md 说我们只有 `run-tests`，实际上：
  - qa-workflow 有用户旅程测试（新用户首次使用、核心业务流程、异常恢复）
  - qa-review-workflow 有 Playwright 3 轮评审（ reviewer 实际操作 → 修复 → 复测）
  - ui-test skill 有 AI 对抗性测试
  - run-tests 有三层执行策略（单元 → 集成 → E2E）
- `e2e-testing-patterns` 的 Page Object 模式等是编码模式，不是 pipeline 需要强制的 gate
- 我们的真问题不是"缺模式"，而是"E2E 执行率低"——这靠 agent-discipline 的铁律已经约束

**PRD→领域建模 — 采纳**
- 现状：requirements-analysis → PRD → 直接进架构设计
- 断层：架构师从 PRD 推导实体关系、聚合根、值对象全靠经验，没有结构化方法
- prd-to-ddd-design 评分低（1.98），但思路对——我们需要的是从 PRD 提取领域模型的 prompt，不一定要装这个 skill
- **建议**：在 Phase 2（架构设计）的 prompt 中加入 DDD 建模步骤，而不是安装外部 skill

### 1.3 P2 项评审

| 项 | 判定 | 理由 |
|----|------|------|
| Git Worktree 隔离 | ❌ | Claude Code 已内置 worktree 支持，不需要 skill |
| 编码会话共享 | ❌ | 协作工具，不影响 pipeline 质量 |
| 测试覆盖分析 | ⚠️ | gate-checker 已有 test_realness_check，但缺覆盖率阈值 gate |

---

## 二、test-handbook 与现有能力真实对比

### 2.1 已覆盖（无需重复建设）

| Handbook 章节 | 覆盖位置 | 覆盖程度 |
|---|---|---|
| 2.1 测试分层 | pipeline-config.json Phase 8（三层）+ run-tests（三层执行） | 完整 |
| 2.2 单元测试规则 | agent-discipline qa.md + test_realness_check gate | 完整 |
| 2.4 E2E 测试规则 | qa-workflow（用户旅程）+ qa-review-workflow（Playwright 3轮）+ ui-test | 完整 |
| 2.8 测试数据隔离 | qa-review-workflow 维度7"测试独立性"（10%）+ 维度8"Mock 合理性"（10%） | 评审级覆盖 |
| 2.9 覆盖率工具 | 项目级配置，不该进 pipeline | N/A |
| 2.10 通用铁律 | agent-discipline 铁律 + task-verifier 证据要求 | 完整 |
| 2.11 历史教训 | MemPalace + self-evolver | 完整 |

### 2.2 部分覆盖（需增强为自动化 gate）

| Handbook 章节 | 当前覆盖 | 缺口 | 建议增强 |
|---|---|---|---|
| 2.3 集成测试 | qa-review-workflow 有评审维度 | 无 API 契约自动检测 | **加 `contract_test_pass` gate** |
| 2.5 性能测试 | qa-workflow 有基准值 | 无自动执行和阈值检查 | **加 `performance_test_pass` gate** |
| 2.6 边界条件 | qa-review-workflow 维度4（10%） | 只在人工评审时检查 | **加 `boundary_test_check` gate** |
| 2.7 错误场景 | qa-review-workflow 维度5（10%） | 只在人工评审时检查 | 可合并到 boundary_test_check |

### 2.3 完全缺失

无。所有 handbook 内容都在 skills/discipline 中有对应，只是部分缺少自动化 gate。

---

## 三、采纳建议汇总

### 3.1 值得采纳（3 项）

| # | 内容 | 形式 | 理由 |
|---|------|------|------|
| 1 | **性能测试 gate** | `performance_test_pass` gate rule | 有规范无执行，加 gate 让性能阈值可自动拦截 |
| 2 | **API 契约测试 gate** | `contract_test_pass` gate rule | 2026-04-11 事故证明这是最高风险接缝 |
| 3 | **边界条件覆盖 gate** | `boundary_test_check` gate rule | 人工评审容易漏，自动扫描测试文件中的边界关键词 |

### 3.2 值得采纳但不需要安装 ClawHub Skill（1 项）

| # | 内容 | 形式 | 理由 |
|---|------|------|------|
| 4 | **PRD→DDD 建模** | 在 Phase 2 prompt 中加入 DDD 建模步骤 | 断层确实存在，但 prd-to-ddd-design 评分低，自建 prompt 更可控 |

### 3.3 不采纳（8 项）

| # | 内容 | 不采纳原因 |
|---|------|-----------|
| 1 | CI/CD 集成 | 我们本身就是 CI/CD，不需要再生成 CI/CD 配置 |
| 2 | riskforge 代码风险分析 | qa-review-workflow 9维评分已覆盖，LLM agent 本身就是代码分析器 |
| 3 | e2e-testing-patterns | 差距被夸大，我们已有完整的 E2E 评审+执行体系 |
| 4 | 设计系统自动化 | 项目级，不是 pipeline 通用能力 |
| 5 | 竞品分析 | 项目前期决策，不属于开发 pipeline |
| 6 | 头脑风暴 | 需求阶段方法论，不属于开发 pipeline |
| 7 | Git Worktree skill | Claude Code 内置支持 |
| 8 | 编码会话共享 | 协作工具，不影响 pipeline 质量 |

---

## 四、不值得采纳的核心理由

pipeline-optimization.md 的问题是把"我们没有一个 skill"等同于"我们缺失这个能力"。实际上：

1. **Skill 只是知识的载体，不是能力的全部。** 我们的 agent-discipline + qa-workflow + qa-review-workflow 组合已经覆盖了大部分声称缺失的能力，只是不在一个叫 `xxx-skill` 的独立文件里。
2. **ClawHub skill 评分普遍低。** 推荐安装的 skill 评分最高 4.25（ui-design-system），最低 0.60（competitor-teardown）。低评分意味着质量不可靠，安装后可能需要大量改造。
3. **测试数据隔离不需要 gate rule。** 这是编码规范，不是门禁检查——你无法用脚本判断"测试是否真的隔离了"，只能通过评审。我们已有评审维度覆盖。
4. **自研 5 个 skill 的 ROI 不高。** pipeline-optimization 建议自研 test-data-isolation、pipeline-smoke-protocol、contract-verification、performance-budget、test-idempotency-check。其中 3 个可以合并为一个 gate rule 实现，不需要 5 个独立 skill。

---

## 五、系统性建议

### 5.1 Gate Rule 体系化

当前 gate rules 是零散添加的（file_exists → file_lines → smoke_test_pass → test_run_pass → test_realness_check），缺乏分层设计。

**建议的分层结构：**

```
Gate Rules
├── 产出物检查（静态）
│   ├── file_exists        ✅ 已有
│   ├── file_lines         ✅ 已有
│   └── artifact_count     ✅ 已有
│
├── 执行验证（动态）
│   ├── smoke_test_pass    ✅ 已有
│   ├── test_run_pass      ✅ 已有
│   ├── performance_test_pass  🆕 新增
│   └── contract_test_pass     🆕 新增
│
├── 质量分析（静态+动态）
│   ├── test_realness_check    ✅ 已有
│   └── boundary_test_check    🆕 新增
│
└── 评审质量（内容分析）
    ├── review_count       ✅ 已有
    ├── review_roles       ✅ 已有
    └── review_content     ✅ 已有
```

### 5.2 Phase 8 门禁链优化

当前 Phase 8 的门禁是扁平的（5 条规则并行检查），应该改为有序门禁链：

```
test_run_pass (先确保能跑)
    ↓ 通过
test_realness_check (再检查质量)
    ↓ 通过
boundary_test_check (再检查覆盖面)
    ↓ 通过
contract_test_pass (最后检查接口契约)
    ↓ 通过
performance_test_pass (性能是锦上添花，不影响通过)
    ↓ 通过/警告
产出物检查 (test-report.md + screenshots)
```

**理由：** 测试跑都跑不过，检查 mock ratio 没意义。应该先过基础门槛，再逐步加严。

### 5.3 Gate Rule 参数标准化

当前 gate rule 的参数格式不统一：

| 现有规则 | 参数格式 | 问题 |
|---------|---------|------|
| `file_exists:test-report.md` | `规则:参数` | 简单清晰 |
| `test_realness_check:max_mock_ratio:0.5` | `规则:参数:值` | 可以，但多参数时难扩展 |
| `test_run_pass:npm test` | `规则:命令` | 命令含空格时解析困难 |

**建议**：新 gate rule 统一用 JSON 配置：

```json
{
  "type": "performance_test_pass",
  "params": {
    "command": "k6 run performance.js",
    "thresholds": {
      "p95_ms": 500,
      "error_rate": 0.01
    }
  }
}
```

但这与现有格式不兼容，建议在 types.ts 中用联合类型兼容两种格式，新 rule 用结构化对象。

### 5.4 Phase 2 加入 DDD 建模步骤

不安装 prd-to-ddd-design skill，而是在架构师的 prompt 中加入：

```
## DDD 建模步骤（强制）

1. 从 PRD 提取领域事件和命令
2. 识别聚合根和值对象
3. 划定限界上下文（Bounded Context）
4. 定义上下文间映射关系
5. 产出：实体关系图 + 聚合根清单 + 上下文映射图
```

这样零成本补上断层，不需要新 skill。

### 5.5 测试报告结构化

当前 test-report.md 是自由格式的 markdown，gate 只检查行数。建议：

1. 定义 test-report.md 的 JSON Schema（必须包含：layer, total, passed, failed, skipped, issues）
2. gate-checker 新增 `test_report_valid` rule，验证报告格式
3. 这样 Phase 8.5 QA Sign-off 可以直接对比报告和实际执行结果，不再需要人工抽查

### 5.6 性能测试渐进式落地

性能测试 gate 不应该一开始就要求所有项目跑 k6。建议分两步：

**Step 1**：`performance_test_pass` 先支持简单的 curl 计时模式（零依赖），检查 P95 和错误率
**Step 2**：项目可选用 k6 模式（更精确的并发压测），通过 params 区分

```json
{
  "type": "performance_test_pass",
  "params": {
    "mode": "curl",  // 或 "k6"
    "endpoints": ["/api/projects", "/api/users"],
    "p95_ms": 500,
    "error_rate": 0.01
  }
}
```

### 5.7 Plugin 升级路径修正

pipeline-optimization.md 的 Plugin 升级路线图方向对，但步骤需要修正：

| 原建议 | 修正 | 理由 |
|-------|------|------|
| Step 1: 状态机 Plugin | **Step 1: 门禁 Plugin** | 门禁是当前最大痛点（手动执行），状态机目前文件系统够用 |
| Step 2: 调度 Plugin | **Step 2: 调度 Plugin** | 正确 |
| Step 3: 门禁 Plugin | **Step 3: 通信 Plugin** | 门禁已在 Step 1 解决 |
| Step 4: 通信 Plugin | **Step 4: 状态机 Plugin** | 优先级最低，文件系统目前可用 |

门禁自动执行是最高优先级——每次阶段切换都要人跑脚本，这比状态机管理更影响效率。
