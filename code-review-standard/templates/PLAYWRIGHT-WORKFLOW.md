# Playwright 实操审查工作流

## 核心流程

```
原Agent完成开发 → 评审官启动Playwright实操 → 发现问题 → 返回反馈给原Agent
     ↑                                                            ↓
测试Agent更新用例并执行 ← 原Agent修改完成 ← 原Agent根据反馈修改代码
     ↓
测试结果 → 如果失败 → 返回原Agent继续修
         → 如果通过 → 通知完成
```

## 三轮协作机制

### 第一轮：评审官 Playwright 实操审查

**评审官必须真实操作应用，不能只看代码！**

#### 启动应用
```bash
# 确认应用是否在运行
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# 如果没运行，启动应用
```

#### 实操检查清单（必须全部执行）

1. **页面加载** — 打开每个页面，截图，检查是否白屏/报错
2. **导航流程** — 按照用户旅程走一遍：首页→搜索→详情→操作
3. **表单交互** — 填写、提交、验证错误提示、清空
4. **数据展示** — 列表加载、分页、空状态、加载状态
5. **响应式检查** — 切换不同视口（375px/768px/1280px），截图对比
6. **交互细节** — 按钮 hover/active 状态、loading 状态、成功/失败反馈
7. **边界操作** — 快速连续点击、输入超长文本、网络断开重试
8. **控制台检查** — 检查是否有 JS 错误、网络请求失败

#### Playwright 审查脚本模板

```javascript
// reviewer-playwright.mjs — 评审官实操审查脚本
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const BASE_URL = process.env.APP_URL || 'http://localhost:3000';
const SCREENSHOT_DIR = process.env.SCREENSHOT_DIR || 'tmp/review-screenshots';

fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1280, height: 800 },
  locale: 'zh-CN'
});

const issues = []; // 发现的问题列表

async function checkPage(name, url, checks) {
  const page = await context.newPage();
  const pageErrors = [];
  const consoleErrors = [];
  
  page.on('pageerror', err => pageErrors.push(err.message));
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  
  try {
    console.log(`\n🔍 检查: ${name} → ${url}`);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
    
    // 截图
    await page.screenshot({ 
      path: path.join(SCREENSHOT_DIR, `${name}-desktop.png`), 
      fullPage: true 
    });
    
    // 执行各项检查
    for (const check of checks) {
      const result = await check(page);
      if (result) {
        issues.push({ page: name, ...result });
        console.log(`  🔴 ${result.title}`);
      }
    }
    
    // 记录控制台错误
    if (consoleErrors.length > 0) {
      issues.push({
        page: name,
        severity: '🔴',
        title: 'JavaScript 控制台错误',
        detail: consoleErrors.slice(0, 5).join('\n'),
        screenshot: `${name}-desktop.png`
      });
    }
    
    console.log(`  ✅ ${name} 检查完成`);
  } catch (err) {
    issues.push({
      page: name,
      severity: '🔴',
      title: '页面加载失败',
      detail: err.message,
      url: url
    });
  } finally {
    await page.close();
  }
}

// ===== 在这里添加要检查的页面和检查逻辑 =====
// 示例：
await checkPage('首页', `${BASE_URL}/`, [
  async (page) => {
    const title = await page.title();
    if (!title || title.includes('Error')) {
      return { severity: '🔴', title: '首页标题异常', detail: `标题: "${title}"` };
    }
    return null;
  },
  async (page) => {
    const hasContent = await page.locator('main, .content, #app').count() > 0;
    if (!hasContent) {
      return { severity: '🔴', title: '首页内容区域为空', screenshot: '首页-desktop.png' };
    }
    return null;
  }
]);

// ===== 响应式检查 =====
const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 }
];

for (const vp of viewports) {
  const page = await context.newPage();
  await page.setViewportSize(vp);
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.screenshot({ 
    path: path.join(SCREENSHOT_DIR, `首页-${vp.name}.png`), 
    fullPage: true 
  });
  await page.close();
}

// ===== 输出报告 =====
console.log('\n' + '='.repeat(50));
console.log(`📋 审查报告：共发现 ${issues.length} 个问题`);
console.log('='.repeat(50));

const blocked = issues.filter(i => i.severity === '🔴');
const important = issues.filter(i => i.severity === '🟡');

console.log(`\n🔴 阻断级: ${blocked.length} 项`);
console.log(`🟡 重要级: ${important.length} 项`);
console.log(`🟢 建议级: ${issues.length - blocked.length - important.length} 项`);

if (issues.length > 0) {
  fs.writeFileSync(
    path.join(SCREENSHOT_DIR, 'review-issues.json'),
    JSON.stringify(issues, null, 2)
  );
  console.log(`\n问题详情已保存: ${SCREENSHOT_DIR}/review-issues.json`);
}

await browser.close();

// 退出码：有阻断级问题返回1
process.exit(blocked.length > 0 ? 1 : 0);
```

### 输出格式（返回给原Agent的反馈）

评审官实操完成后，必须以以下格式输出反馈：

```markdown
📋 Playwright 实操审查报告
━━━━━━━━━━━━━━━━━━━
审查时间：YYYY-MM-DD HH:mm
审查页面：[列出所有检查的页面]
截图目录：{SCREENSHOT_DIR}

## 🔴 阻断级问题（必须修复）

### 问题1：{标题}
- **页面：** {页面名}
- **表现：** {具体描述}
- **截图：** {截图路径}
- **控制台错误：** {如果有}
- **期望行为：** {应该怎样}
- **修复建议：** {具体到文件和代码行}

## 🟡 重要级问题（建议修复）
...

## 🟢 建议优化（可选）
...

## 📊 评估评分
| 维度 | 分数 | 说明 |
|------|------|------|
| 页面加载 | X/10 | ... |
| 导航流程 | X/10 | ... |
| 表单交互 | X/10 | ... |
| 响应式 | X/10 | ... |
| 去AI味 | X/10 | ... |
| **总评分** | **X.X/10** | ... |

## 截图附件
- 首页-desktop.png
- 首页-mobile.png
- ...
```

### 第二轮：原Agent 根据反馈修改

原Agent收到反馈后：

1. **读取 review-issues.json** — 获取所有问题的结构化数据
2. **查看截图** — 理解问题的视觉表现
3. **按优先级修复** — 🔴 → 🟡 → 🟢
4. **每修一个问题** — 更新 review-issues.json 的修复状态
5. **修改完成后** — 编译验证 + 提交修改清单

### 第三轮：测试Agent 更新用例并执行

测试Agent（qa-reviewer 或其他测试角色）：

1. **根据新修改更新测试用例** — 新增/修改对应的测试
2. **执行全量测试** — 确保修改没有引入新问题
3. **如果测试失败** — 返回失败详情给原Agent继续修
4. **如果测试通过** — 输出最终测试报告

## 循环机制

```
评审官审查 → 有问题 → 原Agent修复 → 测试Agent验证
                  ↑                        ↓
                  ←← 测试失败 ←←←←←←←←←←←
                  ↓
              测试通过 → 流程结束
```

**最多循环 3 轮**，超过 3 轮仍有问题则升级处理（报告给协调者）。

## 评审官实操注意事项

1. **必须截图** — 每个检查的页面都要截图，问题要有截图佐证
2. **必须记录控制台错误** — JS错误、网络错误都要记录
3. **必须真实操作** — 不能只看页面渲染，要真的点击、填表、导航
4. **必须检查响应式** — 至少检查 375px（手机）和 768px（平板）
5. **必须给具体修复建议** — 不能只说"有问题"，要说"哪个文件哪行怎么改"
6. **截图存储** — 统一存到 `tmp/review-screenshots/` 目录
