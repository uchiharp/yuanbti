# Available Skills 清单

## 📦 自定义技能（~/.agents/skills）

| Skill | 说明 |
|-------|------|
| **code-quality-guard** | 代码质量检查（编译、逻辑、安全） |
| **db9** | Serverless Postgres 数据库 |
| **deerflow-integration** | DeerFlow 多 Agent 框架集成 |
| **find-skills** | 搜索和发现新技能 |
| **finder-qa** | Finder App 专用 QA 工具 |
| **finder-ui** | Finder App UI 设计规范 |
| **humanize-code** | 去除代码 AI 味 |
| **last30days-cn** | 中国平台深度研究（微博、小红书、知乎等） |
| **reasoning-rag** | 推理型 RAG 工作流 |
| **xiaohongshu-cli** | 小红书操作工具 |

---

## 🔧 OpenClaw 核心技能

### 开发工具
| Skill | 说明 |
|-------|------|
| **coding-agent** | 通用编码 Agent |
| **skill-creator** | 创建和编辑 Agent Skills |
| **clawflow** | 工作流引擎 |
| **clawflow-inbox-triage** | 收件箱分类工作流 |
| **clawhub** | 技能市场（clawhub.com） |
| **github** | GitHub 操作 |
| **gh-issues** | GitHub Issues 管理 |

### 飞书集成
| Skill | 说明 |
|-------|------|
| **feishu-doc** | 飞书文档读写 |
| **feishu-drive** | 飞书云空间 |
| **feishu-wiki** | 飞书知识库 |
| **feishu-perm** | 飞书权限管理 |

### 搜索与信息
| Skill | 说明 |
|-------|------|
| **tavily** | Tavily 搜索（web_search 就是它） |
| **summarize** | 文本摘要 |
| **blogwatcher** | 博客监控 |
| **gifgrep** | GIF 搜索 |

### 笔记与知识库
| Skill | 说明 |
|-------|------|
| **notion** | Notion 操作 |
| **obsidian** | Obsidian 笔记 |
| **apple-notes** | 苹果备忘录 |
| **bear-notes** | Bear 笔记 |

### 消息与通讯
| Skill | 说明 |
|-------|------|
| **wacli** | WhatsApp CLI |
| **xurl** | X (Twitter) API |
| **slack** | Slack 操作 |
| **discord** | Discord 操作 |
| **imsg** | iMessage |
| **bluebubbles** | BlueBubbles (Android 短信) |
| **qqbot** | QQ 机器人 |

### 媒体与语音
| Skill | 说明 |
|-------|------|
| **sag** | ElevenLabs TTS 语音合成 |
| **openai-whisper** | OpenAI Whisper 本地语音识别 |
| **openai-whisper-api** | OpenAI Whisper API |
| **sherpa-onnx-tts** | 本地 TTS |
| **spotify-player** | Spotify 控制 |
| **sonoscli** | Sonos 音响控制 |
| **video-frames** | 视频帧提取 |

### 智能家居与设备
| Skill | 说明 |
|-------|------|
| **openhue** | Philips Hue 灯光 |
| **eightctl** | 八爪鱼遥控器 |
| **tmux** | Tmux 会话管理 |
| **camsnap** | 摄像头拍照 |

### 安全与系统
| Skill | 说明 |
|-------|------|
| **1password** | 1Password 密码管理 |
| **healthcheck** | 系统安全巡检 |
| **node-connect** | OpenClaw 节点连接诊断 |

### 其他工具
| Skill | 说明 |
|-------|------|
| **weather** | 天气查询 |
| **himalaya** | Himalaya 播客 |
| **things-mac** | Things 任务管理 |
| **trello** | Trello 看板 |
| **apple-reminders** | 苹果提醒事项 |
| **oracle** | Oracle 数据库 |
| **canvas** | Canvas LMS |
| **gog** | GOG 游戏平台 |
| **goplaces** | 地点搜索 |
| **ordercli** | 订单管理 |
| **songsee** | 歌曲识别 |
| **blucli** | Blue 工具 |
| **mcporter** | Minecraft 服务器 |
| **nano-pdf** | PDF 处理 |
| **voice-call** | 语音通话 |
| **session-logs** | 会话日志 |
| **model-usage** | 模型用量统计 |
| **gemini** | Google Gemini |

---

## 🎯 当前 Agent 使用的 Skills

| Agent | Skills |
|-------|--------|
| **startup-helper** | feishu-doc, feishu-drive, feishu-wiki, web_search, code-quality-guard |
| **frontend** | code-quality-guard, humanize-code |
| **backend** | code-quality-guard, humanize-code |
| **code-review** | code-quality-guard, humanize-code |
| **pm** | （无特殊技能） |
| **architect** | （无特殊技能） |
| **learn（我）** | 所有可用技能 |

---

## 💡 如何添加新 Skill

```bash
# 1. 从 clawhub 安装
clawhub install <skill-name>

# 2. 在 agent.json 中配置
{
  "skills": ["skill-name"]
}
```
