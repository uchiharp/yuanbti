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

### Step 1: 执行单元测试（不需要环境）
```bash
# 逐任务执行单元测试，捕获日志
mkdir -p {项目目录}/logs/unit
for dir in {项目目录}/tests/unit/T-*/; do
  task_id=$(basename "$dir")
  echo "=== $task_id ==="
  # 根据项目类型执行，日志写入文件：
  # Java: cd $dir && mvn test 2>&1 | tee {项目目录}/logs/unit/${task_id}.log
  # Node: cd $dir && npx jest 2>&1 | tee {项目目录}/logs/unit/${task_id}.log
  # Python: cd $dir && pytest 2>&1 | tee {项目目录}/logs/unit/${task_id}.log

  # 检查结果
  if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "PASS" >> {项目目录}/logs/unit/${task_id}.log
  else
    echo "FAIL" >> {项目目录}/logs/unit/${task_id}.log
    echo "❌ $task_id 测试失败，查看日志: {项目目录}/logs/unit/${task_id}.log"
  fi
done
```

### Step 2: 执行集成测试（不需要环境或使用测试容器）
```bash
mkdir -p {项目目录}/logs/integration
cd {项目目录}/tests/integration && mvn test 2>&1 | tee {项目目录}/logs/integration/integration.log
# 检查失败用例
grep -E "Tests run:.*Failures: [1-9]|ERROR" {项目目录}/logs/integration/integration.log || true
```

### Step 3: 启动完整环境（E2E 前置，必须）

E2E 测试必须连接真实环境。在跑 E2E 之前，协调者必须启动完整环境并确认就绪：

```bash
# 3.1 使用阶段2产出的 docker-compose.test.yml 启动完整环境
cd {项目目录}
docker-compose -f docker-compose.test.yml up -d

# 3.2 等待所有服务就绪（依赖 healthcheck，不是 sleep）
echo "⏳ 等待服务就绪..."
for i in $(seq 1 60); do
  HEALTHY=$(docker-compose -f docker-compose.test.yml ps --format json 2>/dev/null | python3 -c "
import json, sys
count = 0
for line in sys.stdin:
    try:
        svc = json.loads(line)
        if 'healthy' in str(svc.get('Health', '')):
            count += 1
    except: pass
print(count)
" 2>/dev/null || echo 0)
  if [ "$HEALTHY" -gt 0 ]; then
    echo "✅ 服务就绪"
    break
  fi
  if [ $i -eq 60 ]; then
    echo "❌ 服务启动超时"
    docker-compose -f docker-compose.test.yml logs --tail=20
    exit 1
  fi
  sleep 2
done

# 3.3 验证后端健康接口
for i in $(seq 1 30); do
  if curl -sf http://localhost:8080/actuator/health > /dev/null 2>&1; then
    echo "✅ 后端就绪"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "❌ 后端健康检查失败"
    docker-compose -f docker-compose.test.yml logs backend --tail=20
    exit 1
  fi
  sleep 2
done

echo "✅ 环境就绪，开始 E2E 测试"
```

**⚠️ 禁止：不启动环境直接跑 E2E。** E2E 连不上服务会静默跳过或报错，不报错 ≠ 测试通过。

### Step 4: 执行 E2E 测试（必须在 Step 3 之后）
```bash
mkdir -p {项目目录}/logs/e2e
cd {项目目录} && npx playwright test --reporter=list 2>&1 | tee logs/e2e/e2e.log
# 检查退出码：0=全部通过，非0=有失败
E2E_EXIT=${PIPESTATUS[0]}
if [ $E2E_EXIT -ne 0 ]; then
  echo "❌ E2E 测试有失败（exit code: $E2E_EXIT）"
  echo "📋 失败用例详情："
  grep -E "✘|FAIL|Error|Timeout" logs/e2e/e2e.log || true
  # 不要静默忽略
fi
```

### Step 5: 清理环境
```bash
# 停止后端
kill $BACKEND_PID 2>/dev/null
# 停止 Docker 容器（如使用）
docker-compose -f {项目目录}/docker-compose.yml down 2>/dev/null
```

### Step 6: QA 自审（测试艺术家思维）
- 检查测试结果是否有遗漏
- 分析失败用例的根因
- 补充截图证据
- **确认 E2E 测试是在真实环境上跑的（不是 mock）**

### Step 7: PM 对照 PRD 审查
- 验证所有 P0/P1 功能有测试覆盖
- 产出 test-case-review.md

### Step 8: 协调者独立验证

```bash
# 1. 单元测试
cd {项目目录}/6 && mvn test -q 2>&1 | tail -20

# 2. 重新启动环境 + E2E（协调者独立验证，不信任 QA 的报告）
# 重复 Step 3 的环境启动流程
# ...
cd {项目目录} && npx playwright test --reporter=list 2>&1 | tail -30

# 3. 检查 E2E 测试输出（关键：确认测试真的跑了，不是 0 个用例）
E2E_COUNT=$(cd {项目目录} && npx playwright test --reporter=json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('stats',{}).get('expected',0))" 2>/dev/null || echo "0")
if [ "$E2E_COUNT" -eq 0 ]; then
  echo "❌ E2E 测试用例数为 0 — 测试可能未执行"
  exit 1
fi
echo "✅ E2E 执行了 $E2E_COUNT 个用例"

# 4. 检查测试输出文件
ls -la {项目目录}/pipeline/8/test-report.md
ls -la {项目目录}/pipeline/8/qa-reports/*.png 2>/dev/null | wc -l

# 5. 检查截图时间戳
find {项目目录}/pipeline/8/qa-reports -name "*.png" -newer {项目目录}/pipeline/8/test-report.md 2>/dev/null
```

## 测试脚本复用说明
阶段8 直接复用阶段6产出的测试脚本，不需要重新编写：
- `tests/unit/{task_id}/` — 开发写，阶段7 QA验收，阶段8执行
- `tests/integration/` — 开发写，阶段7 QA验收，阶段8执行
- `tests/e2e/` — QA写，阶段7开发确认，阶段8执行

## 检查项（脚本强制）
- [ ] test-report.md 存在
- [ ] 覆盖率报告存在（JaCoCo: target/site/jacoco/index.html / c8: coverage/index.html）
- [ ] 行覆盖率 ≥95%（低于阈值则构建失败，阶段2架构师配置）
- [ ] 集成测试连接真实 DB（非 mock）
- [ ] E2E 测试用例数 > 0（防止环境未启动导致 0 用例）
- [ ] E2E 测试截图 ≥3 张（证明真的跑了）
- [ ] qa-reports/ 截图时间戳晚于 test-report.md（证明是本次执行的）
- [ ] E2E 测试退出码 = 0（有失败用例则不通过）
- [ ] 单元测试通过率 ≥95%
- [ ] 集成测试通过率 100%
- [ ] 测试日志存在于 logs/ 目录（logs/unit/、logs/integration/、logs/e2e/）
- [ ] 失败用例有对应日志，日志中包含错误堆栈

## 约束
- 覆盖率 <95% → 打回开发，回退阶段6
- 集成测试 mock DB → 打回开发，回退阶段6
- E2E 必须在完整环境上运行（后端+前端+DB），禁止 mock
- E2E 用例数为 0 → 打回，检查环境是否启动
- 测试有失败 → 打回开发，回退阶段6
- 通过 → 推进阶段9

## 前置方案审查（强制）
测试过程中如果发现前面阶段的方案有问题、有 bug、有遗漏：
1. **能自行判断的** → 直接记录到 qa-issues.md，标注优先级
2. **无法判断如何处理的** → 立即中断，询问用户
3. **发现实现与文档不一致的** → 通知对应文档的负责人，按实际实现逻辑重新修改文档
