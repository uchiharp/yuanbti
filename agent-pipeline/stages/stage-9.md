# 阶段9：交付验收（协调者）

## 任务
端到端验收，产出验收报告和交付文档。

## 必读文件
所有阶段产出物

## 加载 Skill
无

## 产出物
| 文件 | 最低行数 | 说明 |
|------|---------|------|
| ACCEPTANCE-REPORT.md | 50 | 验收报告（7项 checklist 全部 ✅） |
| docs/user-manual.md | 100 | 用户使用手册 |
| docs/api-docs.md | — | API 接口文档 |
| docs/rpc-api-docs.md | — | RPC 接口文档 |
| docs/integration-guide.md | — | 接入指南（必须含步骤说明） |
| docs/*.html | — | 关键文档的 HTML 版本（结构清晰、便于阅读） |

## 交付文档写作规则
- **必须在阶段7签收后才能写**（基于最终代码）
- 写完后开发确认准确性 + QA 验证可操作性
- 时限：4小时

## HTML 转换（必须）
将以下文档转成 HTML 版本，存入 `docs/` 目录：
- ACCEPTANCE-REPORT.md → docs/acceptance-report.html
- PRD.md → docs/prd.html
- ARCHITECTURE.md → docs/architecture.html
- docs/user-manual.md → docs/user-manual.html
- docs/api-docs.md → docs/api-docs.html

**HTML 要求：**
- 单文件、内联 CSS、无外部依赖
- 表格/标题/代码块/标签样式清晰
- 参考 `agent-pipeline/PIPELINE-GUIDE.html` 的样式风格

## 协调者冒烟验证（交付前必须）

在产出验收报告前，协调者必须亲自跑以下命令确认系统可用：

```bash
# 1. 编译通过
cd {项目目录}/6 && mvn compile -q 2>&1
# 或 Node.js：npm run build 2>&1

# 2. 应用启动（后台运行，检查启动日志）
cd {项目目录}/6 && mvn spring-boot:run > /tmp/app-startup.log 2>&1 &
sleep 15
# 检查启动是否成功
grep -E "Started|ERROR|Exception" /tmp/app-startup.log | tail -5
# 检查端口是否监听
curl -s http://localhost:8080/actuator/health 2>/dev/null || echo "健康检查失败"
kill %1 2>/dev/null

# 3. 核心接口冒烟（至少3个接口）
curl -s http://localhost:8080/api/xxx | head -5
curl -s http://localhost:8080/api/yyy | head -5
curl -s http://localhost:8080/api/zzz | head -5

# 4. 检查测试报告真实性（截图时间戳）
find {项目目录}/8/qa-reports -name "*.png" -mtime -1 | wc -l
```

**冒烟失败处理：**
- 编译失败 → 回退阶段6，发给开发
- 启动失败 → 检查日志，发给开发修复
- 接口失败 → 发给对应开发修复
- 超过2轮冒烟仍失败 → 升级给用户

## 检查项（脚本强制）
- [ ] ACCEPTANCE-REPORT.md 存在
- [ ] 7项验收 checklist 全部 ✅ 或 [x]
- [ ] 无 escalated 合同
- [ ] 安全扫描 0 严重问题
- [ ] 测试报告无 P0 遗留
- [ ] docs/ 归档完整（5个过程文档均存在）
- [ ] 交付文档齐全：
  - user-manual.md ≥100行
  - api-docs.md 存在
  - rpc-api-docs.md 存在
  - integration-guide.md 含步骤说明

## 约束
- 通过 → 输出"项目交付完成"
- 不通过 → 输出缺失项，协调者修复后重检
- 知识库：更新 CONTEXT.md 阶段9段落，存入 MemPalace room=project-lessons
