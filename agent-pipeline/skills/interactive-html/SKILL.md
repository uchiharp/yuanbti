# Skill: 交互式 HTML 文档生成

## 用途
生成单文件、自包含、可交互的 HTML 文档。适用于任何需要结构化展示的场景。

### Pipeline 内适用场景
| 场景 | 阶段 | 产出 |
|------|------|------|
| PRD 交互版 | 1 | docs/prd.html — 需求可点击查看详情 |
| 架构文档交互版 | 2 | docs/architecture.html — 模块可点击展开 |
| 测试报告交互版 | 8 | docs/test-report.html — 用例可点击展开 |
| 验收报告交互版 | 9 | docs/acceptance-report.html |
| 用户文档 | 10 | README / USER-GUIDE / DEPLOYMENT / CONFIG-GUIDE |
| Pipeline 自身文档 | 任意 | PIPELINE-FULL.html 等内部文档 |

凡是需要给人看的结构化文档，都可以用这个 skill 生成。

## 核心原则
- **单文件**：内联 CSS + JS，无外部依赖（Mermaid CDN 除外）
- **可交互**：关键内容点击 → 模态框详情，不是静态页面
- **易读性**：金字塔结构、分层阅读、零假设知识
- **暗色主题**：GitHub Dark 风格，护眼且专业

---

## 一、HTML 模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{文档标题}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
/* CSS 变量 + 组件样式（见第二节） */
</style>
</head>
<body>

<!-- Hero 区 -->
<div class="hero">
  <h1>{主标题}</h1>
  <p>{副标题/一句话描述}</p>
  <div class="badge-row">
    <span class="badge badge-blue">{关键数字1}</span>
    <span class="badge badge-green">{关键数字2}</span>
  </div>
  <p class="hint">点击任意卡片/节点 查看详情</p>
</div>

<div class="container">
  <!-- 侧边栏目录（可选） -->
  <nav class="toc" id="toc"></nav>

  <!-- 各 Section 内容 -->
  <h2 class="section-title"><span class="num">01</span> {章节名}</h2>
  <!-- 卡片网格 / 流程图 / 表格 -->

  <!-- 模态框（隐藏，点击触发） -->
  <div class="modal-overlay" id="m-xxx">
    <div class="modal">
      <div class="modal-header">
        <h2>{标题}</h2>
        <button class="modal-close" onclick="closeModal('m-xxx')">&times;</button>
      </div>
      <div class="modal-body">
        <!-- 详情内容 -->
      </div>
    </div>
  </div>
</div>

<footer>{生成时间 / 版本信息}</footer>

<script>
/* JS 交互逻辑（见第四节） */
</script>
</body>
</html>
```

---

## 二、CSS 样式系统

### 2.1 颜色变量（:root）

```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface2: #1c2129;
  --border: #30363d;
  --text: #e6edf3;
  --muted: #8b949e;
  --accent: #58a6ff;    /* 蓝色 - 主色 */
  --green: #3fb950;     /* 绿色 - 成功/计划 */
  --yellow: #d29922;    /* 黄色 - 警告 */
  --red: #f85149;       /* 红色 - 错误/大型 */
  --purple: #bc8cff;    /* 紫色 - 需求/PM */
  --orange: #f0883e;    /* 橙色 - 测试 */
  --cyan: #39d2c0;      /* 青色 - 开发/UX */

  /* 发光效果 */
  --glow-accent: 0 0 12px rgba(88,166,255,0.4);
  --glow-green: 0 0 12px rgba(63,185,80,0.4);
  --glow-purple: 0 0 12px rgba(188,140,255,0.4);
  --glow-orange: 0 0 12px rgba(240,136,62,0.4);
  --glow-red: 0 0 12px rgba(248,81,73,0.4);
  --glow-cyan: 0 0 12px rgba(57,210,192,0.4);
}
```

### 2.2 可点击卡片

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.25s;
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--purple));
  opacity: 0;
  transition: opacity 0.25s;
}
.card:hover {
  border-color: var(--accent);
  box-shadow: var(--glow-accent);
  transform: translateY(-2px);
}
.card:hover::before { opacity: 1; }

/* 点击提示（hover 时显示） */
.card .click-hint {
  position: absolute;
  top: 10px; right: 12px;
  font-size: 0.7em;
  color: var(--accent);
  opacity: 0;
  transition: opacity 0.25s;
}
.card:hover .click-hint { opacity: 1; }
```

### 2.3 可点击标签（行内）

```css
.click-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 0.82em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}
.click-tag:hover { transform: scale(1.05); }

/* 颜色变体 */
.click-tag-accent { background: rgba(88,166,255,0.15); color: var(--accent); border-color: rgba(88,166,255,0.3); }
.click-tag-accent:hover { box-shadow: var(--glow-accent); border-color: var(--accent); }
.click-tag-green  { background: rgba(63,185,80,0.15); color: var(--green); border-color: rgba(63,185,80,0.3); }
.click-tag-green:hover  { box-shadow: var(--glow-green); border-color: var(--green); }
.click-tag-purple { background: rgba(188,140,255,0.15); color: var(--purple); border-color: rgba(188,140,255,0.3); }
.click-tag-purple:hover { box-shadow: var(--glow-purple); border-color: var(--purple); }
.click-tag-orange { background: rgba(240,136,62,0.15); color: var(--orange); border-color: rgba(240,136,62,0.3); }
.click-tag-orange:hover { box-shadow: var(--glow-orange); border-color: var(--orange); }
.click-tag-red    { background: rgba(248,81,73,0.15); color: var(--red); border-color: rgba(248,81,73,0.3); }
.click-tag-red:hover    { box-shadow: var(--glow-red); border-color: var(--red); }
.click-tag-cyan   { background: rgba(57,210,192,0.15); color: var(--cyan); border-color: rgba(57,210,192,0.3); }
.click-tag-cyan:hover   { box-shadow: var(--glow-cyan); border-color: var(--cyan); }
```

### 2.4 模态框

```css
.modal-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.7);
  z-index: 1000;
  backdrop-filter: blur(4px);
  overflow-y: auto;
  padding: 40px 20px;
}
.modal-overlay.active { display: block; }

.modal {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  max-width: 960px;
  margin: 0 auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.modal-header {
  padding: 24px 28px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-close {
  background: none;
  border: 1px solid var(--border);
  color: var(--muted);
  width: 32px; height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1em;
  transition: all 0.2s;
}
.modal-close:hover { border-color: var(--red); color: var(--red); }
.modal-body {
  padding: 24px 28px 28px;
  max-height: 75vh;
  overflow-y: auto;
}
.modal-body h3 { color: var(--accent); margin: 20px 0 10px; }
```

### 2.5 其他组件

```css
/* 表格 */
table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 0.9em; }
th { background: var(--surface); font-weight: 600; padding: 10px 12px; border: 1px solid var(--border); color: var(--accent); }
td { padding: 10px 12px; border: 1px solid var(--border); }
tr:hover td { background: rgba(88,166,255,0.04); }

/* 代码块 */
pre { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 18px; overflow-x: auto; font-size: 0.86em; }
code { font-family: 'SF Mono','Fira Code','Cascadia Code',monospace; font-size: 0.9em; }
:not(pre)>code { background: rgba(88,166,255,0.1); padding: 2px 6px; border-radius: 4px; color: var(--accent); }

/* 提示框 */
.callout { border-left: 4px solid; padding: 12px 16px; border-radius: 0 8px 8px 0; margin: 14px 0; }
.callout strong { display: block; margin-bottom: 4px; }
.callout-info    { border-color: var(--accent); background: rgba(88,166,255,0.08); }
.callout-warn    { border-color: var(--yellow); background: rgba(210,153,34,0.08); }
.callout-error   { border-color: var(--red); background: rgba(248,81,73,0.08); }
.callout-success { border-color: var(--green); background: rgba(63,185,80,0.08); }

/* Mermaid 容器 */
.mermaid-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  margin: 16px 0;
  overflow-x: auto;
}
.mermaid-wrap .dtitle {
  font-size: 0.8em;
  color: var(--muted);
  margin-bottom: 12px;
  text-align: center;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 脉冲动画（引导用户点击） */
@keyframes glow {
  0%,100% { box-shadow: 0 0 5px rgba(88,166,255,0.2) }
  50% { box-shadow: 0 0 15px rgba(88,166,255,0.5) }
}
.pulse { animation: glow 2s ease-in-out infinite; }

/* 响应式 */
@media(max-width: 768px) {
  .card-grid { grid-template-columns: 1fr; }
  .modal { margin: 10px; }
  .modal-body { padding: 16px; }
}
```

---

## 三、内容组织模式

### 3.1 卡片网格（最常用）

```html
<div class="card-grid">
  <div class="card" onclick="openModal('m-xxx')">
    <div class="click-hint">点击查看详情</div>
    <div class="card-title"><span class="tag tag-pm">PM</span> 需求分析</div>
    <div class="card-body">和用户讨论需求，产出 PRD.md</div>
  </div>
  <!-- 更多卡片... -->
</div>
```

### 3.2 流程节点行

```html
<div class="flow-row">
  <span class="flow-node req" onclick="openModal('m-stage0')">0 启动</span>
  <span class="flow-arrow">→</span>
  <span class="flow-node req" onclick="openModal('m-stage1')">1 PRD</span>
  <span class="flow-arrow">→</span>
  <span class="flow-node des" onclick="openModal('m-stage2')">2 架构</span>
</div>
```

流程节点颜色分类：
- `req`（紫色）= 需求相关
- `des`（蓝色）= 设计相关
- `plan`（绿色）= 计划/分解
- `dev`（青色）= 开发相关
- `test`（橙色）= 测试相关
- `del`（红色）= 交付/验收

### 3.3 可点击标签（行内交叉引用）

```html
执行者：<span class="click-tag click-tag-purple" onclick="openModal('m-pm')">PM</span>
```

### 3.4 表格（数据对比）

直接用 `<table>`，不需要额外 class。hover 行高亮已内置。

### 3.5 代码块

```html
<pre><code>npm install && npm run build</code></pre>
```

### 3.6 提示框

```html
<div class="callout callout-error">
  <strong>禁止</strong>
  不允许的操作说明
</div>
```

### 3.7 Mermaid 图表

```html
<div class="mermaid-wrap">
  <div class="dtitle">图表标题</div>
  <pre class="mermaid">
graph LR
    A[开始] --> B[处理]
    B --> C[结束]
  </pre>
</div>
```

---

## 四、JavaScript 交互系统

### 4.1 Mermaid 初始化

```javascript
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  themeVariables: {
    darkMode: true,
    background: '#161b22',
    primaryColor: '#58a6ff',
    primaryTextColor: '#e6edf3',
    primaryBorderColor: '#30363d',
    lineColor: '#8b949e',
    secondaryColor: '#bc8cff',
    tertiaryColor: '#3fb950',
    fontSize: '13px',
    fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif'
  },
  flowchart: { curve: 'basis', padding: 16 },
  stateDiagram: { useMaxWidth: true }
});
```

### 4.2 模态框控制

```javascript
function openModal(id) {
  document.getElementById(id).classList.add('active');
  document.body.style.overflow = 'hidden';
  // 模态框内的 Mermaid 重新渲染
  setTimeout(() => {
    const modal = document.getElementById(id);
    const unprocessed = modal.querySelectorAll('.mermaid:not([data-processed])');
    if (unprocessed.length > 0) {
      mermaid.run({ nodes: unprocessed });
    }
  }, 50);
}

function closeModal(id) {
  document.getElementById(id).classList.remove('active');
  document.body.style.overflow = '';
}

// 点击遮罩层关闭
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
});

// Escape 键关闭
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(m => {
      m.classList.remove('active');
    });
    document.body.style.overflow = '';
  }
});
```

### 4.3 代码复制按钮（可选增强）

```javascript
document.querySelectorAll('pre').forEach(pre => {
  const btn = document.createElement('button');
  btn.textContent = '复制';
  btn.style.cssText = 'position:absolute;top:8px;right:8px;padding:4px 10px;border-radius:6px;background:var(--surface2);border:1px solid var(--border);color:var(--muted);cursor:pointer;font-size:0.75em;';
  btn.onclick = () => {
    navigator.clipboard.writeText(pre.textContent);
    btn.textContent = '已复制';
    btn.style.color = 'var(--green)';
    setTimeout(() => { btn.textContent = '复制'; btn.style.color = 'var(--muted)'; }, 2000);
  };
  pre.style.position = 'relative';
  pre.appendChild(btn);
});
```

### 4.4 侧边栏目录生成（可选增强）

```javascript
function buildTOC() {
  const toc = document.getElementById('toc');
  if (!toc) return;
  const titles = document.querySelectorAll('.section-title');
  titles.forEach((t, i) => {
    const id = 'section-' + i;
    t.id = id;
    const a = document.createElement('a');
    a.href = '#' + id;
    a.textContent = t.textContent;
    a.style.cssText = 'display:block;padding:6px 0;color:var(--muted);font-size:0.85em;text-decoration:none;border-bottom:1px solid var(--border);';
    a.onmouseenter = () => a.style.color = 'var(--accent)';
    a.onmouseleave = () => a.style.color = 'var(--muted)';
    toc.appendChild(a);
  });
}
buildTOC();
```

### 4.5 术语表 Tooltip（可选增强）

```javascript
const glossary = {
  'REQ-xxx': '需求编号，PRD 中每个功能的唯一标识',
  'acpx': 'Claude Code 的 headless 模式调度命令',
  'flock': 'Linux 文件锁，用于并发安全'
};
document.querySelectorAll('.term').forEach(el => {
  const term = el.textContent;
  if (glossary[term]) {
    el.title = glossary[term];
    el.style.borderBottom = '1px dashed var(--muted)';
    el.style.cursor = 'help';
  }
});
```

---

## 五、易读性要求

### 5.1 结构层
- **金字塔原则**：结论先行，细节在后。每个 Section 开头一句话总结
- **分层阅读**：概览（卡片/流程图）→ 详情（模态框）→ 原理（模态框内的 Mermaid/代码）
- **目录锚点**：长文档必须有 TOC（可用第四节的自动生成方案）

### 5.2 内容层
- **零假设知识**：不假设读者知道背景，第一段写"这是什么"
- **术语表**：专有名词用 `<span class="term">` 包裹，hover 显示解释
- **代码可复制**：代码块有复制按钮
- **错误优先**：常见报错 + 解决方案放在醒目位置
- **What-Why-How**：先说"是什么"，再说"为什么"，最后说"怎么用"

### 5.3 格式层
- 表格代替大段文字
- 步骤用有序列表
- 每个模态框内容不超过一屏（~30行），超过就拆子章节
- 代码示例用 `代码块`，不是纯文本

### 5.4 语言层
- 中文为主，技术术语保持英文（"API" 不说 "应用程序接口"）
- 禁用"此处省略"、"详见xxx" — 直接放内容
- 一个句子只说一件事

---

## 六、生成检查清单

生成 HTML 文件后，逐项检查：

- [ ] 单文件、内联 CSS + JS，无外部依赖（Mermaid CDN 除外）
- [ ] 暗色主题，颜色变量统一
- [ ] 可点击元素有 hover 发光效果（`box-shadow` + `translateY`）
- [ ] 模态框支持 Escape 关闭 + 点击外部关闭
- [ ] 模态框内 Mermaid 图表自动渲染
- [ ] 代码块有复制按钮
- [ ] 长文档有侧边栏 TOC
- [ ] 术语有 tooltip 解释
- [ ] 表格/代码块/提示框样式正确
- [ ] 移动端响应式（`@media max-width: 768px`）
- [ ] 每个模态框内容不超过一屏
- [ ] 无"详见xxx"跳转式写法
- [ ] 中文为主，技术术语保持英文
