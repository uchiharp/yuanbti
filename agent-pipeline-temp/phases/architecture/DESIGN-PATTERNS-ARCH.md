# 架构组 Pipeline 设计模式

从 requirements-pipeline 继承的通用设计模式 + 架构组特有的设计决策。

---

## 继承自 requirements-pipeline 的 10 个通用设计模式

以下模式完全复用，实现细节参见 `DESIGN-PATTERNS.md`：

### 1. 断点续跑（Checkpoint & Resume）
- DB `phase_log` 表记录每个 step 的 `running/done/failed/skipped`
- DB 说 `running` 但产出文件已存在 → 视为 `done(file)`（文件兜底）
- `--status` 命令只读模式查看断点
- `--step` 参数可指定只运行某个步骤

### 2. 前置条件校验（Precondition Check）
- `require_file(path, desc)` — 文件必须存在且非空
- `require_step_done(step)` — 上游步骤必须已完成
- 架构组特有：检查 `requirements_done` 前置状态

### 3. 产出物校验（Artifact Validation）
- `validate_artifact(path, desc, min_lines)` — 文件存在 + 非空 + 行数 >= min_lines
- ARCHITECTURE.md 最低 100 行
- cross-review-arch.md 最低 30 行
- SPIKE-REPORT.md 最低 20 行

### 4. 产出物清理（Downstream Cleanup）
- 清理粒度递增：
  - arch-design → 全部架构产出
  - arch-quality-score → 评审+审阅+spike
  - arch-review → 审阅+spike
  - arch-user-review → spike

### 5. 错误传播（Error Propagation）
- Exit code 区间：30-39（架构组专用）
- trap ERR 兜底标记当前步骤为 failed
- trap EXIT 检查 running 状态并标记 failed

### 6. 可观测性（Observability）
- 执行时长：`step_timer_start` / `step_timer_elapsed`
- 评分详情完整存入 `detail` JSON
- 6维度 + 11项健壮性检查结果实时输出

### 7. 安全设计（Security）
- SQL 转义：`sql_escape()` 防注入
- JSON 转义：`json_escape()` 处理特殊字符
- 非交互模式：`--yes` + `confirm_or_auto()`

### 8. 调度解耦（Dispatch Decoupling）
- 无调度模式（默认）：脚本暂停等用户手动完成
- DISPATCH_CMD 模式：环境变量指定调度命令
- prompt 组装在脚本内，调度在外部

### 9. 规模自适应（Size Adaptation）
- 前置估算：根据 PRD 的 REQ 数量推断规模
- small 项目用精简模板
- medium/large 项目用完整模板

### 10. 配色约定
- ✅ 步骤完成 / ⏩ 跳过 / ❌ 失败 / 🔄 运行中 / ⚪ 未开始 / ⚠️ 警告 / 🔜 断点

---

## 架构组特有设计决策

### 1. 与需求组共用 pipeline.db

**决策**：架构组不创建独立的 DB，而是与需求组共用同一个 `pipeline.db`。

**理由**：
- 两个 pipeline 服务同一个项目，数据天然关联
- features 表的状态流转跨越两个阶段（PRD-已确认 → 技术方案-已确认）
- 减少文件数量，简化管理

**实现**：
- `phase` 字段区分：需求组用 `requirements`，架构组用 `architecture`
- `current_phase` 字段：`requirements_done` → `architecture_done`
- 复用 `pipeline-db.sh` 库，不修改任何函数签名

### 2. 6步流水线设计

**决策**：架构组采用 6 步流水线（比需求组多 1 步）。

**步骤链**：
```
arch-design → arch-quality-score → arch-review → arch-user-review → [tech-spike] → arch-finalize
```

**理由**：
- arch-design：核心产出步骤，生成 ARCHITECTURE.md
- arch-quality-score：自动评分，提供客观质量度量
- arch-review：4角色交叉评审（比需求组多1个角色）
- arch-user-review：HTML 转换 + 用户确认
- tech-spike：条件触发，只在有高风险标记时执行
- arch-finalize：入库，更新 features 状态

### 3. tech-spike 条件触发

**决策**：tech-spike 不是必选步骤，只在 ARCHITECTURE.md 中有高风险标记时触发。

**检测方法**：
```bash
grep -ciE '高风险|spike|需验证|待验证|技术风险' "$arch_file"
```

**路由逻辑**：
- 无高风险标记 → 自动 skip，直接进入 finalize
- 有高风险标记 → 执行 Spike，根据结论路由：
  - 全部通过 → finalize
  - 部分不通过 → 建议回退 arch-design
  - 全部不通过 → 强制退出

### 4. arch-parser.sh 独立解析库

**决策**：架构组有自己的解析库 `arch-parser.sh`（类似需求组的 `prd-parser.sh`）。

**功能**：
- `arch_req_list` — 从架构文档提取 REQ 引用
- `arch_req_count` — REQ 总数
- `arch_has_chapter` — 章节检测
- `arch_score_inline` — 内联质量评分（11项检查，总分55）
- `arch_check_dimensions` — 6维度检测
- `arch_check_robustness` — 11项健壮性检测
- `arch_has_high_risk` — 高风险标记检测
- `arch_req_coverage` — 需求覆盖率检查

### 5. 4角色交叉评审（比需求组多1个角色）

**决策**：架构评审采用 4 个角色（需求组是 3 个）。

**角色**：
1. **RD（开发视角）**：技术可行性 — 技术选型、接口合理性、过度设计
2. **架构师视角**：架构一致性 — 分层合规、模块耦合、设计模式
3. **QA 视角**：可测试性 — 测试覆盖、日志监控、自动化
4. **PM 视角**：需求完整性 — PRD 覆盖、优先级、逻辑闭环

**理由**：架构决策影响面广，需要更多视角把关。

### 6. 质量评分体系差异

**需求组**：12项检查，总分60分
**架构组**：11项检查，总分55分

| 检查项 | 需求组 | 架构组 |
|--------|--------|--------|
| Executive Summary | ✅ 5分 | — |
| User Impact | ✅ 5分 | — |
| Business Impact | ✅ 5分 | — |
| SMART Goals | ✅ 5分 | — |
| System Overview | ✅ 5分 | — |
| User Story Criteria | ✅ 5分 | — |
| REQ Numbering | ✅ 5分 | — |
| REQ Module Coverage | ✅ 5分 | — |
| Testable Criteria | ✅ 5分 | — |
| Out of Scope | ✅ 5分 | — |
| NFR Quantified | ✅ 5分 | — |
| Task Hints | ✅ 5分 | — |
| Architecture Diagram | — | ✅ 5分 |
| Tech Selection | — | ✅ 5分 |
| Data Model | — | ✅ 5分 |
| API Design | — | ✅ 5分 |
| Security | — | ✅ 5分 |
| Risk Identification | — | ✅ 5分 |
| Code Architecture | — | ✅ 5分 |
| 6 Dimensions | — | ✅ 5分 |
| Robustness (11项) | — | ✅ 5分 |
| Logging/Exception | — | ✅ 5分 |
| Vague Language | — | ✅ 5分 |

### 7. 评级标准

| 评级 | 需求组 | 架构组 |
|------|--------|--------|
| EXCELLENT | ≥90% | ≥90% |
| GOOD | 75-89% | 75-89% |
| ACCEPTABLE | 60-74% | 60-74% |
| NEEDS_WORK | <60% | <60% |

---

## 文件命名约定

| 产出物 | 文件名 | 说明 |
|--------|--------|------|
| 架构方案 | ARCHITECTURE.md | 核心产出 |
| 测试环境 | docker-compose.test.yml | E2E 环境定义 |
| 交叉评审 | cross-review-arch.md | 4角色评审报告 |
| HTML 版本 | architecture-draft.html | 用户审阅用 |
| Spike 报告 | SPIKE-REPORT.md | 技术验证报告 |

## DB 状态流转

```
projects.current_phase:
  init → requirements_done → architecture_done

features.status:
  PRD-已确认 → 技术方案-已确认

phase_log (phase=architecture):
  arch-design: running → done/failed
  arch-quality-score: running → done/failed
  arch-review: running → done/failed
  arch-user-review: running → done/failed
  tech-spike: running → done/failed/skipped
  arch-finalize: running → done/failed
```
