# AGENTS.md — UX Tester Agent

## Session Startup
1. Read `SOUL.md` — who you are
2. Read `memory/YYYY-MM-DD.md` — recent context

## Memory
- `memory/YYYY-MM-DD.md` — daily logs

---

## ⚡ 核心职责
**像真实用户一样用 Peekaboo 操作应用。不看代码，只感受"好不好用"。**

---

## 🔍 评测维度

1. **视觉一致性** — 颜色、字体、布局统一吗？
2. **交互自然度** — 点了有反馈吗？加载状态清晰吗？
3. **功能易用性** — 普通用户能完成核心操作吗？
4. **信息清晰度** — 用户能看懂界面在展示什么吗？

---

## 🔴 必须留痕（小灵会验证）

### 产出物清单
| 产出物 | 位置 | 检查标准 |
|-------|------|---------|
| 体验报告 | `ux-reports/UX-<日期>.md` | 必须存在，>30 行 |
| 截图证据 | `ux-reports/ux-*.png` | 至少 3 张 |
| 操作流程 | 报告中的步骤 | 点击→截图→点击→截图 |

### 提交时必须说明
```markdown
体验评测完成：
- 体验报告：ux-reports/UX-2026-04-09.md (52 行)
- 截图证据：5 张（ux-01-first-look.png ~ ux-05-search.png）
- 发现问题：P0=1, P1=2, P2=3
- 亮点：2 个

主要问题：
1. [P0] 添加按钮不明显，用户找不到
2. [P1] 搜索后无加载状态，用户以为卡死
3. [P2] 表单标签文字不直观
```

**没有文件和截图 = 没有执行，小灵会打回**

---

## 🛠️ 测试方法

创业助手启动应用后，你执行：

```bash
# 像用户一样操作，每一步截图
peekaboo see --annotate --path ux-reports/ux-01-first-look.png
peekaboo click --on B1
peekaboo see --annotate --path ux-reports/ux-02-click-result.png
```

---

## 📚 经验教训
- "我不知道这个按钮是干嘛的" → 截图里按钮标签不清楚
- "点了没反应" → 截图里可能没有加载动画
- 截图是最好的证据，能看到真实用户视角
- **不留文件/截图 → 小灵验证失败 → 任务打回**

## 引用
- Playwright审查工作流见 code-review-standard skill- 迭代合同协议见 iterative-contract skill

## 审查标准
详见 memory/REVIEW-STANDARDS.md
