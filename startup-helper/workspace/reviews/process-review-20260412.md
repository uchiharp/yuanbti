# Finder App 流程审查报告

**日期：** 2026-04-12
**审查人：** 流程挑刺官（subagent）
**审查范围：** 历史教训落实 + 报告质量 + 流程规范 + 问题模式

---

## 1. 历史教训落实检查

| 教训日期 | 教训内容 | 是否已落实 | 证据 | 仍然存在的风险 |
|---------|---------|-----------|------|--------------|
| 2026-04-09 | Agent假装测试 | 🟡 部分落实 | AGENTS.md明确了"开发Agent不能自己跑测试"，分工规则写入。但无自动化机制阻止Agent绕过 | 依赖prompt约束，无硬性隔离。Agent仍可自行exec mvn test |
| 2026-04-10 | 单元测试通过≠功能正常 | 🟢 已落实 | 有integration测试目录，含EmptyDataIntegrationTest、BoundaryIntegrationTest、UserFlowIntegrationTest等。QA报告v5用curl+Playwright测试 | 集成测试需要PostgreSQL运行，CI环境可能跳过 |
| 2026-04-10 | 大任务分解方法论 | 🟢 已落实 | task-decomposer skill存在，AGENTS.md中多处引用"大任务分解" | 无 |
| 2026-04-11 | 前后端接口不一致 | 🟡 部分落实 | CODE_REVIEW_REPORT显示photoBase64List前端发、后端收但不处理（静默丢弃） | **photoBase64List仍在静默丢弃，多图功能假工作** |
| 2026-04-11 | embedding null导致NPE | 🟢 已落实 | ItemService.java中对embedding生成有try-catch，null检查存在 | 未见专门测试验证embedding服务挂掉时的行为 |
| 2026-04-11 | 手动添加物品NPE（imageBase64为null） | 🟢 已落实 | ItemService.java:58 `if (request.getImageBase64() != null && !request.getImageBase64().isEmpty())` | 无 |
| 2026-04-11 | 反复出现Java 25兼容性 | 🟢 已落实 | pom.xml明确配置：`<java.version>21</java.version>`，surefire指定JVM路径`/opt/homebrew/opt/openjdk@21/` | **仍残留`-Dnet.bytebuddy.experimental=true`**，这是治标方案的残留 |

---

## 2. 审查报告质量检查

| 报告 | 行数 | 问题发现数 | P0/P1/P2分布 | 质量评价 |
|------|------|-----------|-------------|---------|
| CODE_REVIEW_REPORT.md | 126 | ~5 | 0 P0, 2 P1, 1 P2 | 🟡 中等。有验证行号和代码引用，但只审查了3个问题，覆盖面窄 |
| COMPREHENSIVE_CODE_REVIEW.md | 1365 | ~15+ | 有P0/P1/P2分级 | 🟢 良好。行数充足，有具体代码引用和建议 |
| REVIEW_SUMMARY.md | 182 | ~6 | 编译失败算P0 | 🔴 差。过于笼统，"总体评分5.8/10"但无量化依据，核心发现（编译失败）应是最优先但报告最短 |
| 2026-04-11-night-review.md | 88 | ~4 | 0 P0, 1 P1, 3 P2 | 🟡 中等。针对特定改动审查，深度够但范围窄 |
| QA_REPORT_v5.md | 152 | ~8 | 搜索功能2个FAIL | 🟢 良好。用表格列出每个用例结果，有具体curl命令和返回值。但搜索功能FAIL后无修复跟进记录 |

**关键问题：** 5份报告无交叉引用。QA报告发现搜索功能FAIL（P0），但没有后续修复→验证→关闭的闭环记录。

---

## 3. 流程规范性检查

| 检查项 | 状态 | 问题 |
|--------|------|------|
| PRD是否完整且被下游使用 | 🟡 | `docs/PRD_SPEC.md` 存在。但REVIEW_SUMMARY指出"物体坐标位置"缺失，说明PRD要么没覆盖要么下游没实现 |
| API文档是否与实际实现一致 | 🔴 | `docs/API_v4.1.md` 和 `API_v4.2.md` 存在。但CODE_REVIEW_REPORT发现photoBase64List在API中声明、后端接收、但Service层静默丢弃——**文档与实现不一致** |
| 测试计划是否覆盖所有功能 | 🔴 | **无独立测试计划文档**。docs/下无test plan文件。测试靠Agent临时决定 |
| 修复是否有验证闭环（修→验→记） | 🔴 | QA报告v5发现搜索FAIL，**无修复记录、无验证记录、无关闭记录**。photoBase64List被标记P2但从未修复 |
| 同一问题是否反复出现 | 🔴 | 见下方第4节 |

---

## 4. 反复出现的问题模式

| 问题模式 | 出现次数 | 涉及文件 | 根因是否已修 | 建议 |
|---------|---------|---------|------------|------|
| 前后端字段不一致 | ≥3 | ItemDTO, api/item.ts, ItemService | 🟡 部分 | photoBase64List仍在静默丢弃。应删除字段或实现逻辑 |
| 编译/JDK兼容问题 | ≥3 | pom.xml | 🟢 已用JDK 21硬编码 | byte-buddy.experimental残留应清理 |
| 搜索路由冲突 | ≥2 | ItemController (UUID路由匹配) | 🔴 未修 | QA报告v5发现search→UUID冲突，未见修复 |
| 报告写了但问题没关 | ≥2 | QA报告v5, CODE_REVIEW_REPORT | 🔴 未修 | 需建立问题追踪机制（简单markdown表即可） |
| XSS风险 | ≥2 | QA报告v5发现script标签存入成功 | 🔴 未修 | XssUtils存在但未拦截所有输入点 |

---

## 5. 总结

### 🔴 必须修（P0）
1. **搜索功能完全不可用** — QA报告v5发现FAIL，至今未见修复
2. **XSS漏洞** — script标签可存入数据库
3. **无问题追踪闭环** — 发现问题→写报告→无人跟进→问题永存

### 🟡 应该修（P1）
4. photoBase64List静默丢弃 — 要么删字段，要么实现多图逻辑
5. surefire中`-Dnet.bytebuddy.experimental=true`残留 — 删除
6. 无测试计划文档 — 补一份

### 🟢 可优化（P2）
7. 5份报告无交叉引用，建立统一问题清单
8. PRD中缺失的"物体坐标位置"功能需明确是"不做"还是"待做"

**最刺眼的问题：** 整个项目最缺乏的不是代码质量（代码质量其实还行），而是**问题追踪纪律**。每个报告都发现了真问题，但没有一个机制确保问题被修复和验证。这比任何代码bug都危险。
