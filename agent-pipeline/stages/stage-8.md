# 阶段8：测试执行（QA + PM）

## 前置条件
- 测试交叉审查（stage-7-test-review）已通过
- 代码审查（stage-7）已通过

## 任务
QA 执行所有测试脚本，PM 验证测试覆盖 PRD 需求。

**测试用例必须基于细化后的 PRD 和 UI 原型编写**，覆盖交互流程和异常场景。

## 必读文件
1. tests/unit/ 开发写的单元测试（阶段6产出，阶段7 QA已验收）
2. tests/integration/ 开发写的集成测试（阶段6产出，阶段7 QA已验收）
3. tests/e2e/ QA 写的 E2E 测试（阶段6产出，阶段7已确认）
4. test-plan.md（阶段5产出）
5. PRD.md（🟡/🔴项目为细化后的 PRD，含交互细节/边界/异常处理描述）
6. PRD-REFINED.md（🟡/🔴项目，阶段1.8产出的细化 PRD，测试用例需覆盖细化内容）
7. UI-UX-DESIGN.md（🟡/🔴项目，阶段1.7产出，测试交互行为需与设计一致）
8. docs/ui-prototype.html（🟡/🔴项目，阶段1.7产出的 HTML 原型，验证 UI 行为）

## 加载 Skill
- `qa-workflow`

## 前置工具检查

```bash
# 检查测试工具是否已安装（缺失才安装）
bash agent-pipeline/scripts/check-test-tools.sh {项目目录}
```

## 产出物
| 文件 | 说明 |
|------|------|
| test-report.md | 测试报告（含逐项结果、通过率、问题清单、REQ 追溯矩阵） |
| qa-reports/*.png | 测试截图 ≥3张 |
| test-case-review.md | PM 测试用例评审意见 |
| error-monitor/error-report.md | 错误监控报告（前后端隐含错误） |

## 执行流程

### Step 0: 工具检查
```bash
bash agent-pipeline/scripts/check-test-tools.sh {项目目录}
```

### Step 1: 测试用例对照（基于细化 PRD 和 UI 原型）

QA 必须基于以下基准验证测试覆盖：

**细化 PRD（🟡/🔴项目）**：
- 交互细节测试：验证每个 REQ 的操作路径、交互方式、反馈时机
- 边界情况测试：验证每个 REQ 标注的边界场景
- 文案规范测试：验证页面标题、按钮、提示文案符合规范
- 异常处理测试：验证输入校验、网络异常、权限异常等路径

**UI 原型（🟡/🔴项目）**：
- 交互一致性：实际 UI 行为与 HTML 原型一致
- 组件状态：正常/空/加载/错误状态切换正确
- 响应式：至少验证 Desktop + Mobile 两种布局

**🟢小型项目**：基于原始 PRD 验收标准测试即可。

### Step 2: 测试执行
按 test-plan.md 顺序执行：
1. 单元测试 → `mvn test` / `npm test`
2. 集成测试 → `mvn verify` / `npm run test:integration`
3. E2E 测试 → `npx playwright test`
4. 记录每个测试结果

### Step 3: REQ 追溯矩阵
生成测试报告时，必须包含 REQ 追溯矩阵：

```markdown
## REQ 追溯矩阵
| REQ | 功能 | TC 数 | 通过 | 失败 | 覆盖率 |
|-----|------|-------|------|------|--------|
| REQ-001 | 用户登录 | 5 | 5 | 0 | 100% |
| REQ-002 | 数据导出 | 8 | 7 | 1 | 87.5% |
```

### Step 4: 功能点标签更新
- 测试通过的 REQ → `测试-通过`
- 测试失败的 REQ → `测试-失败`（回退到开发-进行中）

### Step 5: PM 测试用例评审
PM 对照 PRD 验证：
- 每个 REQ 至少有 1 个正向 TC + 1 个逆向 TC
- 边界场景已覆盖（🟡/🔴项目参考细化 PRD 的边界情况章节）
- 异常路径已覆盖（🟡/🔴项目参考细化 PRD 的异常处理章节）
- 交互行为与 UI 设计一致（🟡/🔴项目）

## 检查项（脚本强制）
- [ ] test-report.md 存在且 ≥50行
- [ ] qa-reports/ 存在且含截图 ≥3张
- [ ] REQ 追溯矩阵完整（每个 REQ 至少 1 个 TC）
- [ ] 每个 REQ 至少 1 正向 + 1 逆向 TC
- [ ] 覆盖率 ≥95%
- [ ] 集成测试连接真实 DB
- [ ] 功能点标签已更新

## 约束
- 合同：🔴高风险 最多3轮
- 测试失败 → 开发修复 → QA 回归验证
- 修复后仅重跑失败用例（非全量重跑）
- 单次回归超时：1小时
