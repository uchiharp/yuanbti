# 参考文档（合并版）

> 原始文件在 references/ 目录，已合并为单一文件。



---

# Reference: iterative-contract.md

# 精简迭代合同协议 v2

> 原 v1 协议完整版保留在 `AGENT-ITERATIVE-CONTRACT.md`，供参考。
> 本文件是**精简版**，用于日常协作，减少通信开销。

## 核心原则

**合同不是为了写文档，是为了保证质量。用最少的文字传递最关键的信息。**

---

## 精简合同格式

### 完整流程才用完整合同，简单场景用简化版

---

### 🟢 简化合同（低风险改动）

```
📋 合同 #{N} | {发包方} → {承包方} | 🟢低风险
━━━━━━━━━━━━━━━━━━━
交付：{一句话描述交付物}
路径：{绝对路径}
验证：{一句话验证标准}
━━━━━━━━━━━━━━━━━━━
状态：⏳ 待签收
```

签收/打回回复（一行）：
```
✅ 签收 | 无问题
❌ 打回 | {一句话原因}
```

### 🟡 标准合同（中风险改动）

```markdown
📋 合同 #{N} | {发包方} → {承包方} | 🟡中风险
━━━━━━━━━━━━━━━━━━━

**交付物：**
| 交付物 | 路径 | 验证标准 |
|--------|------|---------|
| {名} | {路径} | {标准} |

**重点检查：** {2-3个需要特别关注的点}

**质量门槛：** 🔴=0, 总评≥7.0

━━━━━━━━━━━━━━━━━━━
状态：⏳ 待签收
```

签收回复：
```
✅ 签收 | 评分: X.X | 🟡问题: {如果有}
❌ 打回 | 🔴:{数量} 🟡:{数量} | 关键: {最严重的问题}
```

### 🔴 完整合同（高风险改动）

使用完整版 `AGENT-ITERATIVE-CONTRACT.md` 的格式。

---

## 通信开销控制规则

### 规则 1：风险分级决定合同复杂度

| 风险等级 | 合同类型 | 适用场景 |
|---------|---------|---------|
| 🟢 低风险 | 简化合同 | 文案修改、样式微调、配置变更 |
| 🟡 中风险 | 标准合同 | 新功能、重构、Bug修复 |
| 🔴 高风险 | 完整合同 | 支付、认证、数据迁移、安全相关 |

### 规则 2：问题清单精简化（可升级）

**默认用精简格式，但复杂问题必须展开说明。**

判断标准：
- **能用一句话说清楚** → 精简格式
- **需要解释"为什么这是问题"** → 展开说明
- **涉及多个文件/状态流转** → 必须展开
- **架构/需求层面的非代码问题** → 必须展开

❌ 冗长（可精简）：
```
问题：用户注册后页面没有跳转到首页，导致用户不知道注册是否成功，可能重复注册。
严重程度：🔴阻断
建议：注册成功后应该自动跳转到首页，并显示一个简短的欢迎提示。
```

✅ 精简（信息完整）：
```
🔴 注册后未跳转首页 → auth.ts:45 → 加 `router.push('/')`
```

✅ 展开（复杂问题必须写清楚）：
```
🔴 用户状态管理混乱
- 问题：注册→登录→修改密码，三处状态更新不一致，
  store中的user对象在注册后没有sync到localStorage，
  导致刷新页面后丢失登录态
- 影响：auth.ts:45, store/user.ts:23, utils/auth.ts:67
- 修复：统一在auth.ts的login/register/refresh三个方法末尾
  调用 syncToStorage()，而不是各自维护
```

### 规则 3：评分用速查表

不用写完整评分报告，用速查格式：

```
评分: 7.5 | 正确:8 安全:7 性能:8 健壮:7 可维护:8 规范:7 业务:8 AI味:6 | 🔴:1 🟡:2
```

### 规则 4：截图一句话说明

不用描述截图内容，截图文件名自带说明：

```
截图: register-flow-{步骤名}.png | register-error-{错误类型}.png
```

### 规则 5：签收/打回一句话

```
✅ 7.5分签收 | 1🟡建议: 注册按钮间距偏大
❌ 打回 | 🔴:注册白屏 🟡:2项 | 建议: auth.ts:32空指针
```

---

## 合同存储方案

### 目录结构

```
.contracts/
├── _index.json          ← 合同索引（所有合同的快速检索）
├── _config.json         ← 全局配置（默认阈值、存储策略）
└── {project-name}/
    ├── {task-name}/
    │   ├── c01.md       ← 合同1（精简版，5-10行）
    │   ├── c02.md       ← 合同2
    │   ├── c03.md       ← 合同3
    │   └── summary.md   ← 任务总结（最终状态+经验）
    └── ...
```

### 索引文件格式 (_index.json)

```json
{
  "lastUpdated": "2026-04-11T14:30:00+08:00",
  "contracts": [
    {
      "id": "finder-app-auth-register",
      "task": "用户注册功能",
      "project": "finder-app",
      "status": "completed",
      "rounds": 3,
      "finalScore": 7.8,
      "agents": ["dev1", "architect", "qa"],
      "contracts": ["c01.md", "c02.md", "c03.md"],
      "createdAt": "2026-04-11T14:00:00+08:00",
      "completedAt": "2026-04-11T14:25:00+08:00"
    }
  ],
  "stats": {
    "total": 1,
    "completed": 1,
    "inProgress": 0,
    "averageRounds": 3,
    "averageScore": 7.8
  }
}
```

### 合同恢复机制

**问题：跨会话后如何知道哪些合同还在进行中？**

**方案：每次会话启动时读取 `_index.json`，找出 `status: "inProgress"` 的合同。**

```markdown
## 会话恢复流程

1. 读取 `.contracts/_index.json`
2. 找出 `status: "inProgress"` 的合同
3. 读取最后一份合同文件，确定当前状态
4. 从断点继续执行
```

### 合同自动清理

- **已完成合同**：保留30天后自动归档到 `.contracts/_archive/`
- **进行中合同**：如果最后更新时间超过7天，标记为 `stale`
- **配置在 `_config.json` 中可调**

```json
{
  "defaults": {
    "maxRounds": 3,
    "passThreshold": 7.0,
    "aiFlavorThreshold": 6.0,
    "maxBlockers": 0,
    "maxImportant": 2
  },
  "storage": {
    "retentionDays": 30,
    "staleAfterDays": 7,
    "archiveDir": "_archive"
  }
}
```

---

## 与风险分级的集成

### 自动风险分级

**发包方在发合同时必须标注风险等级：**

| 判断标准 | 风险等级 |
|---------|---------|
| 涉及支付/认证/权限/数据删除/迁移 | 🔴 高风险 |
| 新功能/重构/API变更/数据库变更 | 🟡 中风险 |
| 文案/样式/配置/文档/bugfix(非核心) | 🟢 低风险 |

### 不确定时升级

**如果发包方和承包方对风险等级有分歧，按高等级执行。**

### 风险等级影响

| | 🟢 低风险 | 🟡 中风险 | 🔴 高风险 |
|---|---------|---------|---------|
| 合同格式 | 简化(3行) | 标准(10行) | 完整(30行) |
| Playwright | 走查关键路径 | 完整实操 | 完整实操+边界测试 |
| 评分维度 | 3个核心 | 6个重点 | 全部维度 |
| 最大迭代 | 1轮 | 2轮 | 3轮 |
| 一眼AI检查 | 抽查 | 全检 | 全检+人工复核 |

---

# Reference: security-scan-templates.md

# 安全扫描脚本模板（QA Playwright 实操时使用）

> 这些脚本嵌入在 Playwright 审查流程中，不是单独运行。
> QA 在阶段7 Playwright 实操时，按需调用这些扫描。

---

## 1. SQL 注入检测脚本

```javascript
// sql-injection-test.mjs
// 在表单输入框中注入 SQL payload，检查是否报错
const SQL_PAYLOADS = [
  "' OR '1'='1",
  "1; DROP TABLE users--",
  "' UNION SELECT * FROM users--",
  "admin'--",
  "1' AND '1'='1",
  "' OR 1=1--",
  "'; WAITFOR DELAY '0:0:5'--",  // 时间盲注
];

async function testSQLInjection(page, formSelector) {
  const results = [];
  for (const payload of SQL_PAYLOADS) {
    const before = Date.now();
    try {
      // 找到表单输入框
      const inputs = await page.$$(formSelector + ' input[type="text"], ' + formSelector + ' input[type="email"], ' + formSelector + ' input[type="search"], ' + formSelector + ' textarea');
      for (const input of inputs) {
        await input.fill(payload);
      }
      await page.click(formSelector + ' button[type="submit"], ' + formSelector + ' button');
      await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});
      
      const after = Date.now();
      const responseTime = after - before;
      
      // 检查异常迹象
      const pageText = await page.textContent('body').catch(() => '');
      const hasError = /sql|syntax|error|exception|warning|mysql|postgresql|oracle/i.test(pageText);
      const isSlow = responseTime > 4500; // 时间盲注特征
      const unusualResponse = pageText.length > 10000; // UNION SELECT 返回大量数据
      
      if (hasError || isSlow || unusualResponse) {
        results.push({
          payload: payload.substring(0, 30) + '...',
          issue: hasError ? 'SQL错误信息泄露' : isSlow ? '疑似时间盲注' : '异常大量数据返回',
          responseTime: responseTime + 'ms',
          severity: '🔴'
        });
      }
    } catch (e) {
      // 网络错误也可能是注入成功的表现
      results.push({
        payload: payload.substring(0, 30) + '...',
        issue: `请求异常: ${e.message.substring(0, 50)}`,
        severity: '🟡'
      });
    }
  }
  return results;
}
```

---

## 2. XSS 检测脚本

```javascript
// xss-test.mjs
const XSS_PAYLOADS = [
  '<script>alert("xss")</script>',
  '<img src=x onerror=alert(1)>',
  '"><script>alert(document.cookie)</script>',
  "javascript:alert(1)",
  '{{7*7}}',  // 模板注入
  '<svg onload=alert(1)>',
  "'-alert(1)-'",
];

async function testXSS(page, inputSelector) {
  const results = [];
  for (const payload of XSS_PAYLOADS) {
    try {
      const input = await page.$(inputSelector);
      if (!input) continue;
      
      await input.fill(payload);
      // 触发 blur/change 事件
      await input.dispatchEvent('blur');
      await page.waitForTimeout(500);
      
      // 检查 payload 是否被原样渲染（未被转义）
      const pageContent = await page.content();
      const isReflected = pageContent.includes('<script>') || 
                          pageContent.includes('onerror=') ||
                          pageContent.includes('onload=') ||
                          pageContent.includes('javascript:');
      
      if (isReflected) {
        results.push({
          payload: payload.substring(0, 40) + '...',
          issue: 'XSS payload 未被转义，原样渲染',
          severity: '🔴'
        });
      }
    } catch (e) {
      // 忽略
    }
  }
  return results;
}

// 检查页面中已有内容是否被正确转义
async function checkContentEscaping(page) {
  const issues = [];
  const inputs = await page.$$('input, textarea');
  
  // 检查 input 的 value 是否被转义
  for (const input of inputs) {
    const value = await input.getAttribute('value').catch(() => '');
    if (value && (value.includes('<') || value.includes('>'))) {
      const type = await input.getAttribute('type').catch(() => 'text');
      if (type === 'text' || type === 'email' || type === 'search') {
        issues.push({
          element: 'input[type=' + type + ']',
          issue: `值包含未转义的HTML字符: "${value.substring(0, 30)}"`,
          severity: '🟡'
        });
      }
    }
  }
  
  // 检查 dangerouslySetInnerHTML 或 v-html
  const pageContent = await page.content();
  if (pageContent.includes('dangerouslySetInnerHTML') || pageContent.includes('v-html')) {
    issues.push({
      element: '页面源码',
      issue: '使用了危险的HTML直接渲染（dangerouslySetInnerHTML/v-html）',
      severity: '🟡'
    });
  }
  
  return issues;
}
```

---

## 3. 依赖漏洞检查

```bash
# dependency-check.sh
# 检查前端和后端依赖的已知漏洞

echo "🔍 依赖漏洞检查"
echo "━━━━━━━━━━━━━━━━━━━"

# 前端 npm audit
if [ -f "package.json" ]; then
  echo ""
  echo "📦 前端依赖 (npm audit):"
  npm audit --json 2>/dev/null | python3 -c "
import json, sys
try:
  data = json.load(sys.stdin)
  vulns = data.get('vulnerabilities', {})
  if not vulns:
    print('  ✅ 无已知漏洞')
  else:
    high = sum(1 for v in vulns.values() if v.get('severity') == 'high')
    moderate = sum(1 for v in vulns.values() if v.get('severity') == 'moderate')
    low = sum(1 for v in vulns.values() if v.get('severity') == 'low')
    print(f'  🔴 高危: {high}')
    print(f'  🟡 中危: {moderate}')
    print(f'  🟢 低危: {low}')
    if high > 0:
      for name, info in vulns.items():
        if info.get('severity') == 'high':
          print(f'    - {name}: {info.get(\"title\", \"?\")} ({info.get(\"via\", [\"?\"])[0] if isinstance(info.get(\"via\"), list) else info.get(\"via\", \"?\")})')
except: print('  ⚠️ 无法解析 audit 结果')
" 2>/dev/null || echo "  ⚠️ npm audit 不可用"
fi

# 后端 Maven OWASP dependency-check (如果配置了)
if [ -f "pom.xml" ]; then
  echo ""
  echo "📦 后端依赖 (Maven):"
  # 检查是否有已知漏洞版本的依赖
  mvn dependency:check-for-updates 2>/dev/null | grep -i "security\|vulnerability" | head -5 || echo "  ⚠️ 建议配置 OWASP dependency-check-maven 插件"
fi
```

---

## 4. 健壮性故障注入测试

```javascript
// resilience-test.mjs
// 模拟各种异常情况，检查应用的容错能力

async function testResilience(page, baseUrl) {
  const results = [];
  
  // 1. 网络中断恢复
  console.log('  📡 测试网络中断恢复...');
  const context = page.context();
  try {
    await context.setOffline(true);
    await page.goto(baseUrl, { waitUntil: 'domcontentloaded', timeout: 5000 });
    const offlineText = await page.textContent('body').catch(() => '');
    
    const hasOfflineUI = /离线|网络|连接|offline|network/i.test(offlineText);
    if (!hasOfflineUI) {
      results.push({
        test: '网络中断',
        issue: '断网后无离线提示UI',
        severity: '🟡'
      });
    }
  } finally {
    await context.setOffline(false);
  }
  
  // 2. 超大输入
  console.log('  📝 测试超大输入...');
  const longInputs = await page.$$('input[type="text"], input[type="email"], textarea');
  for (const input of longInputs) {
    const placeholder = await input.getAttribute('placeholder') || await input.getAttribute('name') || 'input';
    try {
      await input.fill('A'.repeat(10000));
      await input.dispatchEvent('change');
      await page.waitForTimeout(300);
      
      const value = await input.inputValue().catch(() => '');
      if (value.length > 1000 && !await page.$('.error, .error-message, [class*="error"]')) {
        results.push({
          test: '超大输入',
          issue: `"${placeholder}" 接受了${value.length}字符输入，无长度校验提示`,
          severity: '🟡'
        });
      }
      // 清空
      await input.fill('');
    } catch (e) {
      // 输入框可能被禁用，忽略
    }
  }
  
  // 3. 快速连续点击
  console.log('  🖱️ 测试快速连续点击...');
  const submitBtn = await page.$('button[type="submit"], button:has-text("提交"), button:has-text("确认"), button:has-text("保存")');
  if (submitBtn) {
    try {
      await Promise.all([
        submitBtn.click(),
        submitBtn.click(),
        submitBtn.click(),
        submitBtn.click(),
        submitBtn.click(),
      ]);
      await page.waitForTimeout(1000);
      
      // 检查是否出现了多个成功提示（重复提交）
      const successMsgs = await page.$$('[class*="success"], [class*="toast"], [class*="message"]');
      if (successMsgs.length > 1) {
        results.push({
          test: '快速连续点击',
          issue: `出现了${successMsgs.length}个成功提示，疑似重复提交`,
          severity: '🔴'
        });
      }
    } catch (e) {}
  }
  
  // 4. 并发请求模拟
  console.log('  ⚡ 测试并发请求...');
  try {
    const apis = [];
    const links = await page.$$eval('a[href^="/api/"]', els => els.map(a => a.href));
    if (links.length > 0) {
      const apiCall = links[0];
      const responses = await Promise.all(
        Array(10).fill(null).map(() => page.evaluate(url => fetch(url).then(r => r.status).catch(() => 'error'), apiCall))
      );
      const errors = responses.filter(r => r === 'error' || r >= 500);
      if (errors.length > 0) {
        results.push({
          test: '并发请求',
          issue: `10个并发请求中${errors.length}个失败`,
          severity: '🟡'
        });
      }
    }
  } catch (e) {}
  
  // 5. 特殊字符输入
  console.log('  🔣 测试特殊字符...');
  const specialChars = ['中文测试', '日本語テスト', '🎉🎉🎉', '<>&"\'\\/', 'null', 'undefined', 'NaN', '', ' '];
  const textInputs = await page.$$('input[type="text"]');
  for (const input of textInputs.slice(0, 3)) { // 只测前3个
    for (const char of specialChars) {
      try {
        await input.fill(char);
        await input.dispatchEvent('change');
        await page.waitForTimeout(200);
        
        // 检查是否崩溃（空白页）
        const bodyText = await page.textContent('body').catch(() => '');
        if (bodyText.length < 10) {
          results.push({
            test: '特殊字符',
            issue: `输入"${char}"后页面崩溃（内容为空）`,
            severity: '🔴'
          });
          break;
        }
        await input.fill('');
      } catch (e) {}
    }
  }
  
  return results;
}
```

---

## 5. 安全 Header 检查

```javascript
// security-headers-check.mjs
async function checkSecurityHeaders(page, baseUrl) {
  const results = [];
  
  const response = await page.goto(baseUrl, { waitUntil: 'commit' });
  const headers = response.headers();
  
  const REQUIRED_HEADERS = [
    { name: 'x-content-type-options', expected: 'nosniff', severity: '🟡' },
    { name: 'x-frame-options', expected: 'DENY or SAMEORIGIN', severity: '🔴' },
    { name: 'x-xss-protection', expected: '1; mode=block', severity: '🟡' },
    { name: 'content-security-policy', expected: '存在', severity: '🟡' },
    { name: 'strict-transport-security', expected: '存在', severity: '🟡' },
    { name: 'referrer-policy', expected: '存在', severity: '🟢' },
  ];
  
  for (const h of REQUIRED_HEADERS) {
    const value = headers[h.name.toLowerCase()];
    if (!value) {
      results.push({
        header: h.name,
        issue: `缺少安全Header: ${h.name}`,
        severity: h.severity
      });
    }
  }
  
  return results;
}
```

---

## 使用方式

在 QA 的 Playwright 审查流程中，在"页面加载→截图"之后、"写出审查报告"之前，插入以下步骤：

```
标准 Playwright 实操流程：
1. 页面加载 + 截图                    ← 已有
2. 导航流程 + 交互测试                ← 已有  
3. 响应式检查                          ← 已有
4. ⬇️ 新增安全扫描步骤 ⬇️
5. SQL注入测试（如果有表单）           ← 新增
6. XSS检测（如果有输入框）             ← 新增
7. 依赖漏洞检查（npm audit）          ← 新增
8. 安全Header检查                      ← 新增
9. 健壮性测试（断网/超大输入/快速点击） ← 新增
10. 合并所有结果 → 审查报告           ← 已有
```

**注意：安全扫描只在🔴高风险和🟡中风险的合同中执行，🟢低风险跳过。**

## 对应风险分级

| 风险等级 | 扫描范围 |
|---------|---------|
| 🔴 高风险 | SQL注入 + XSS + 依赖漏洞 + Header检查 + 全部健壮性测试 |
| 🟡 中风险 | XSS检测 + Header检查 + 快速点击 + 超大输入 |
| 🟢 低风险 | 跳过安全扫描（只做基本Playwright走查）|
