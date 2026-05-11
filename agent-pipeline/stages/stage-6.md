# 阶段6：开发执行

## 任务
按任务清单开发代码，QA 同步写 E2E 测试脚本。

## 必读文件（按顺序，强制）
1. docs/ARCHITECTURE.md（代码架构规范 — 分层、模块、模式、日志异常）
2. docs/CODE-MAP.md（现有代码地图）
3. TASK-LIST.md（分配的任务）
4. CONTEXT.md

## 加载 Skill
| 角色 | Skill |
|------|-------|
| 开发 | `code-quality-guard`, `logging-exception` |
| QA（并行） | `qa-workflow` |

## 产出物
| 文件 | 说明 |
|------|------|
| dev/ 代码文件 | 按任务清单开发 |
| tests/ 测试脚本 | QA 同步产出 Playwright E2E |

## 执行顺序
**P0 → P1 → P2 不做**

## 开发前强制步骤
1. 读 ARCHITECTURE.md（理解分层、模块、模式选型）
2. 读 CODE-MAP.md（理解现有代码）
3. 读任务中标注的所有涉及文件（理解现状）
4. 确认要改的接口/函数的当前签名和返回值
5. **然后**才开始写代码

## 测试要求（开发写）
- 单元测试 → `tests/unit/`
- 基础集成测试 → `tests/integration/`
- mock 比例 ≤ 50%，核心业务逻辑禁止 mock
- 每个 test case 至少 1 个有效断言
- 写完立刻跑测试，不通过当场修

## 检查项（脚本强制）
- [ ] dev/ 目录存在且含代码文件
- [ ] tests/ 目录存在且含测试文件
- [ ] 合同轮次 ≤3
- [ ] 代码遵循分层架构（Controller 不直接引用 Repository）
- [ ] CONTEXT.md 阶段6段落已更新

## 约束
- 合同：🔴高风险 完整合同 最多3轮
- ❌ 禁止只看任务描述就直接写代码
- ❌ 禁止在此阶段写 E2E 测试（QA 负责）
- 知识库：更新 CONTEXT.md 阶段6段落，存入 MemPalace room=dev-notes
