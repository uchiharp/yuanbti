# Skills - Learn Bot 可用技能

> 📚 **主动使用这些技能来更好地帮助用户**

---

## 🎯 核心技能（主动使用）

### 1. **superpowers** - TDD开发流程
**触发场景：**
- 用户要写代码/开发功能
- 需要系统化的开发流程
- Bug修复需要结构化方法

**使用方式：**
```
读取：/Users/sunwenyong/.openclaw/workspace/skills/superpowers/SKILL.md
```

---

### 2. **self-improving-agent** - 避免重复犯错
**触发场景：**
- 用户纠正了你的错误
- 发现了之前犯过的类似错误
- 需要记住重要教训

**使用方式：**
```
读取：/Users/sunwenyong/.openclaw/workspace/skills/self-improving-agent-cn/SKILL.md
```

---

### 3. **show-thinking** - 展示思考过程
**触发场景：**
- **每次回复都必须使用**
- 复杂问题需要推理
- 用户想看到你的思路

**使用方式：**
```
格式：
🧠 思考过程
[分析→选项→决策→盲点]
---
[正文]
```

---

### 4. **find-skills** - 搜索新技能
**触发场景：**
- 遇到现有技能无法解决的问题
- 用户需要新功能
- 想扩展能力

**使用方式：**
```
读取：/Users/sunwenyong/.agents/skills/find-skills/SKILL.md
```

---

## 🌐 网络相关（按需使用）

### 5. **web-extractor** - 网页内容提取
**触发场景：**
- 需要爬取学习资料网页
- 提取在线文档内容
- 获取结构化的Markdown

**使用方式：**
```
读取：/Users/sunwenyong/.openclaw/workspace/skills/web-extractor/SKILL.md
```

---

### 6. **playwright-npx** - 浏览器自动化
**触发场景：**
- 需要截图演示
- 复杂的网页交互
- 自动化测试

**使用方式：**
```
读取：/Users/sunwenyong/.openclaw/workspace/skills/playwright-npx/SKILL.md
```

---

### 7. **deerflow-integration** - DeerFlow 深度研究 ⭐ 重要
**触发场景：**
- **深度研究任务**（如搜索 AO3、学术论文等）
- **复杂多步骤任务**
- **需要子智能体协作**
- **网页访问受限**（AO3、Google Scholar 等）
- **报告生成、PPT、网页设计**

**DeerFlow 内置能力：**
| 技能 | 描述 |
|------|------|
| deep-research | 深度研究和信息收集 ⭐ |
| data-analysis | 数据分析和可视化 |
| ppt-generation | PPT 生成 |
| image-generation | 图像生成 |
| web-design | 网页设计 |

**使用方式：**
```
读取：/Users/sunwenyong/.agents/skills/deerflow-integration/SKILL.md
```

**重要**：遇到 AO3、学术论文、深度调研等任务，**优先考虑 DeerFlow**

---

## ✍️ 写作相关

### 7. **humanizer** - 文本人性化
**触发场景：**
- 生成的代码注释太机器化
- 解释过于生硬
- 需要更自然的表达

**使用方式：**
```
读取：/Users/sunwenyong/.openclaw/workspace/skills/ai-humanizer/SKILL.md
```

---

## 📚 完整技能索引

查看所有可用技能：
```
/Users/sunwenyong/.openclaw/workspace/SKILLS_INDEX.md
```

---

## 🚀 使用原则

### ✅ 主动识别
- **不要等用户说**"用XX技能"
- **主动判断**需求并使用对应技能
- **主动告知**用户你正在使用什么技能

### 🔄 组合使用
```
爬取教程 (web-extractor)
→ 整理笔记 (humanizer) 
→ 生成练习题 (superpowers)
```

### 📖 先读后用
使用任何技能前，先读取对应的 SKILL.md

---

_这个文件帮助你主动使用技能，提供更好的学习支持。_


---

## 📥 **feishu-media** - 下载飞书消息中的图片/视频/文件
**触发场景：**
- 用户发送图片、视频或文件
- 需要在本地处理媒体文件（如图片识别、视频分析）

**使用方式：**
```
读取：/Users/sunwenyong/.openclaw/workspace/skills/feishu-media/SKILL.md
```

**下载命令：**
```bash
python3 ~/.openclaw/workspace/skills/feishu-media/scripts/download_media.py \
  --message-id "om_xxxxx" --file-key "file_v3_xxxxx" \
  --file-name "output.mp4" --type video --account-id <当前bot的account_id>
```

**用完后清理：**
```bash
python3 ~/.openclaw/workspace/skills/feishu-media/scripts/download_media.py --cleanup
```

