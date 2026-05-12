# 阶段8：测试执行（QA + PM）

## 前置条件
- 测试交叉审查（stage-7-test-review）已通过
- 代码审查（stage-7）已通过

## 任务
QA 执行所有测试脚本，PM 验证测试覆盖 PRD 需求。

## 必读文件
1. tests/unit/ 开发写的单元测试（阶段6产出，阶段7 QA已验收）
2. tests/integration/ 开发写的集成测试（阶段6产出，阶段7 QA已验收）
3. tests/e2e/ QA 写的 E2E 测试（阶段6产出，阶段7已确认）
4. test-plan.md（阶段5产出）
5. PRD.md（验证业务逻辑）

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
| test-report.md | 测试报告（含逐项结果、通过率、问题清单） |
| qa-reports/*.png | 测试截图 ≥3张 |
| test-case-review.md | PM 测试用例评审意见 |

## 执行流程

### Step 0: 工具检查
```bash
bash agent-pipeline/scripts/check-test-tools.sh {项目目录}
```

### Step 1: 执行单元测试（复用阶段6的测试脚本）
```bash
# 逐任务执行单元测试
for dir in {项目目录}/tests/unit/T-*/; do
  task_id=$(basename "$dir")
  echo "=== $task_id ==="
  # 根据项目类型执行：
  # Java: cd $dir && mvn test
  # Node: cd $dir && npx jest
  # Python: cd $dir && pytest
done
```

### Step 2: 执行集成测试（复用阶段6的测试脚本）
```bash
cd {项目目录}/tests/integration && mvn test  # 或对应测试框架
```

### Step 3: 执行 E2E 测试（复用阶段6的测试脚本）
```bash
cd {项目目录} && npx playwright test --reporter=list
```

### Step 4: QA 自审（测试艺术家思维）
- 检查测试结果是否有遗漏
- 分析失败用例的根因
- 补充截图证据

### Step 5: PM 对照 PRD 审查
- 验证所有 P0/P1 功能有测试覆盖
- 产出 test-case-review.md

### Step 6: 协调者独立验证

```bash
# 1. 单元测试
cd {项目目录}/6 && mvn test -q 2>&1 | tail -20

# 2. E2E 测试
cd {项目目录} && npx playwright test --reporter=list 2>&1 | tail -30

# 3. 检查测试输出文件
ls -la {项目目录}/8/test-report.md
ls -la {项目目录}/8/qa-reports/*.png 2>/dev/null | wc -l

# 4. 检查截图时间戳
find {项目目录}/8/qa-reports -name "*.png" -newer {项目目录}/8/test-report.md 2>/dev/null
```

## 测试脚本复用说明
阶段8 直接复用阶段6产出的测试脚本，不需要重新编写：
- `tests/unit/{task_id}/` — 开发写，阶段7 QA验收，阶段8执行
- `tests/integration/` — 开发写，阶段7 QA验收，阶段8执行
- `tests/e2e/` — QA写，阶段7开发确认，阶段8执行

## 约束
- 测试有 P0 未修复 → 打回开发，回退阶段6
- 通过 → 推进阶段9

## 前置方案审查（强制）
测试过程中如果发现前面阶段的方案有问题、有 bug、有遗漏：
1. **能自行判断的** → 直接记录到 qa-issues.md，标注优先级
2. **无法判断如何处理的** → 立即中断，询问用户
3. **发现实现与文档不一致的** → 通知对应文档的负责人，按实际实现逻辑重新修改文档
