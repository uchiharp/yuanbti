# MEMORY.md - 长期记忆

## 用户偏好

- **模型选择（2026-04-07）：**
  - 日常非编码对话 → GLM-5（轻量快速）
  - startup-helper agent → GLM-5.1（需要深度推理）
  - 编码/复杂分析 → GLM-5.1
  - cron任务 → GLM-5.1（深度推理）

## 🏗️ 四层架构系统（2026-04-22）

### 系统架构
| 组件 | 状态 | 连接方式 | 位置 |
|------|------|---------|------|
| OpenClaw（编排层） | ✅ 2026.4.2 | - | Mac 本地 |
| Claude Code（编码层） | ✅ 2.1.109 | ACP + tmux | Mac 本地 |
| ~~Codex CLI~~ | ❌ 已卸载 2026-05-07 | - | - |
| Hermes（规划层） | ✅ v0.9.0 | localhost:8642 | 1060服务器 SSH隧道 |

### 模型配置
- **Claude Code：** Ark GLM-5.1（主）+ DeepSeek V3.2（轻量）
- ~~Codex CLI：~~ ❌ 2026-05-07 已卸载
- **Hermes：** GLM-5.1（智谱直连）
- **OpenClaw：** GLM-5-turbo（日常对话）
- **全部通过火山方舟 Ark Coding Plan 调用**（并发20+无压力，智谱直连并发3就限流）

### Runner 脚本（tmux 模式，实时查看执行过程）
- **claude-code-runner.sh** — tmux + 日志 + 飞书通知（深度编码，推理不打折）

### 调度规则（见 SOUL.md）
- 轻量编码 → Claude Code（ACP）
- 深度编码 → Claude Code（tmux，推理不打折）
- 想实时看执行过程 → tmux 模式
- 记忆查询/存储 → Hermes API
- 任务分解 → Hermes delegate_task

### 服务器配置
- **1060 GPU服务器：** nyaruko@192.168.31.18（内网）/ 81.70.189.52:6000（外网）
- **Hermes Gateway：** 端口8642，本地8642（SSH隧道）
- **llama-server：** 端口8088（GPU加速embedding）

---

## 硬件资源

### 阿里云服务器（2026-04-19 从创业助手同步）
- **公网IP：** 8.147.115.189
- **私网IP：** 192.168.1.30
- **配置：** 2核 2G，3Mbps 带宽
- **系统：** Alibaba Cloud Linux 3.2104 LTS 64位
- **地域：** 华北2（北京）可用区 I
- **SSH：** root@8.147.115.189（密码见用户）
- **实例ID：** i-2ze4e3ag2dlgc2mcnw88
- **已安装：** Docker 26.1.3 + Docker Compose v2.27.0
- **PostgreSQL 16 + pgvector 0.8.2**（端口5432，库: finder，用户: finder）
- **Redis 7 Alpine**（端口6379）
- **用途：** Finder App 部署、yuanbti 等项目部署

### Windows 台式机（2026-05-08 确认）
- **内网IP：** `192.168.31.134`
- **用户名：** `Administrator`
- **密码：** `Feichang@4zz`
- **系统：** Windows 10 专业版 Build 19045
- **主机名：** DESKTOP-UVFIB3N
- **硬件：** 20核CPU，16G 内存
- **GPU：** NVIDIA GeForce RTX 4070 **12GB 显存**（Driver 560.94，CUDA 12.6）
- **SSH：** 已开启 OpenSSH Server（密码认证）
- **已安装：** 飞书、Steam、Razer Synapse、罗技 G Hub、MuMu 模拟器、OneDrive、WPS
- **用途潜力：** AI绘图(ComfyUI)、本地大模型(Ollama)、游戏服务器、NAS、代理网关

### 1060 GPU 服务器（2026-04-13 确认）
- **内网IP：** `192.168.31.18`（端口22，局域网直连）
- **外网IP：** `81.70.189.52`（端口6000，不在家时用）
- **SSH账号：** `nyaruko`
- **系统：** Ubuntu 24.04.2 LTS (x86_64)
- **硬件：** GPU（型号待确认，可能是GTX 1060），97.87GB磁盘
- **已装软件：**
  - Ollama（qwen2.5:3b、minicpm-v）
  - yolo-env 虚拟环境（Python 3.12.3，ultralytics待安装）
  - Java服务部署目录：`/opt/java-services/`
- **注意：** nyaruko用户无sudo免密权限，nvidia-smi需要密码
- **SSH连接：** 两台地址用的是同一个ed25519密钥，是同一台机器

---

## 地点

- **常驻地区：** 北京天通苑（2026-03-24 更新）

---

## 用户纠正（2026-04-02）

### 1. "老张"称呼的真相
- ❌ 错误理解：刘繇友好地叫张邈"老张"
- ✅ 正确理解：刘繇以为张邈姓"老"（文化水平不高，误解姓氏）
- 🎭 张邈调侃刘繇"不太有学识，只喜欢酒肉美人"
- 体现了两人的文化差距和张邈的毒舌

### 2. "愚弟"的正确理解
- ❌ 错误理解：张邈自称"愚弟"
- ✅ 正确理解：张邈称呼弟弟张超为"愚弟"
- 原文："这是愚弟，张超。愚蠢的弟弟，给殿下打招呼。"
- 体现了张邈对弟弟的毒舌调侃

---

## 🖥️ Windows 台式机 - AI 绘图工作站（2026-05-08）

### 硬件信息
- **IP：** 192.168.31.134（局域网直连）
- **SSH：** `Administrator@192.168.31.134`，密码 `Feichang@4zz`
- **主机名：** DESKTOP-UVFIB3N
- **系统：** Windows 10 专业版 Build 19045
- **CPU：** 20 核
- **内存：** 16GB
- **GPU：** NVIDIA GeForce RTX 4070，12GB 显存（Driver 560.94，CUDA 12.6）

### 网络限制（⚠️ 重要）
- **无代理**，无法直接访问 GitHub、HuggingFace、CivitAI 等国外网站
- **GitHub 镜像：** ghfast.top（已配置 git 全局 insteadOf）
- **HuggingFace 镜像：** hf-mirror.com（已配置 HF_ENDPOINT 环境变量）
- **pip 镜像：** 清华 pypi.tuna.tsinghua.edu.cn（已配置）
- **所有依赖下载必须走国内镜像**，否则必定超时失败

### 已安装软件
- **Python 3.10.11** — `C:\Users\Administrator\AppData\Local\Programs\Python\Python310`
- **Git 2.47.1** — `C:\Program Files\Git\cmd`
- **PyTorch 2.11.0+cu126** + torchvision 0.26.0+cu126 + torchaudio 2.11.0+cu126
- **Node.js 22** — `C:\Program Files\nodejs`
- **FFmpeg 8.1.1** — `C:\ffmpeg\ffmpeg-8.1.1-essentials_build\bin`
- 其他：飞书、Steam、Razer Synapse、罗技 G Hub、MuMu 模拟器、OneDrive、WPS、GameViewer Virtual Display Adapter

### ComfyUI（AI 绘图 - 节点式）
- **路径：** `C:\ComfyUI`（版本 0.20.1）
- **访问：** http://192.168.31.134:8188
- **启动方式：** `cmd /c C:\ComfyUI\start_comfyui.bat`（WMI 后台进程，SSH 断了不中断）
- **防火墙：** 已放行 8188 端口（规则名 ComfyUI）
- **模型：**
  - Checkpoint: `Illustrious-XL-v2.0.safetensors`（6.6GB）— NoobAI 底模，动漫二次元
  - CLIP L: `sd_xl_clip_l.safetensors`（470MB）
  - CLIP G: `sd_xl_clip_g.safetensors`（2.7GB）
  - VAE: `sdxl_vae.safetensors`（319MB，fp16-fix）
- **默认工作流：** `C:\ComfyUI\user\default_workflow.json`（CheckpointLoaderSimple 格式）
- **当前问题：** ComfyUI 新版默认工作流用分拆节点（diffusion_models/text_encoders），需要 Load Default 加载自定义工作流

### SD Forge（AI 绘图 - 传统 WebUI）
- **路径：** `C:\sd-forge`（版本 f2.0.1v1.10.1，commit dfdcbab6）
- **访问：** http://192.168.31.134:7860
- **状态：** ✅ 可用（2026-05-08 验证通过）
- **启动方式：** schtasks 计划任务 `StartForge`（WMI 启动失败，schtasks 成功持久化）
- **防火墙：** 已放行 7860 端口（规则名 Forge）
- **模型：** 通过符号链接共用 ComfyUI 的 `Illustrious-XL-v2.0.safetensors`
- **启动环境变量：** `CLIP_PACKAGE=openai-clip`, `OPENCLIP_PACKAGE=open-clip-torch`, `HF_ENDPOINT=https://hf-mirror.com`
- **已装依赖：** openai-clip（二进制安装）、scikit-image 0.25.2、setuptools<82
- **限制：** ❌ xformers 在 Windows 上编译失败，启动不加 --xformers

### ⚠️ GPU 资源冲突
- **ComfyUI 和 Forge 不能同时运行**（12GB 显存不够两个同时加载模型）
- 需要先关一个再启动另一个
- 切换方式：`taskkill /F /IM python.exe` → 启动另一个
- **推荐：** 日常用 Forge（WebUI 更友好），批量/自动化用 ComfyUI（API 接口）

### SSH 远程操作注意事项
- 路径含空格需反斜杠转义引号
- `$env:PATH` 会被本地 shell 展开
- PowerShell `-File` 在 SSH 中有路径解析问题，用 `-Command "& script"` 替代
- `start /b` 和 `Start-Process cmd /c` 在 SSH 断开后进程会终止
- **永久后台进程：** WMI 或 schtasks 计划任务（Forge 用 schtasks，ComfyUI 用 WMI）
- **WMI 有时返回 ReturnValue=9（权限不足），备用 schtasks：** `schtasks /create /tn StartForge /tr "cmd /c C:\sd-forge\webui-user.bat" /sc once /st 00:00 /ru SYSTEM /f && schtasks /run /tn StartForge`
- Windows 无 base64 命令，用 PowerShell `[Convert]::FromBase64String` + certutil -decode
- PowerShell Expand-Archive 不支持 .tgz，用 `cmd /c tar -xzf`
- 上传 Python 脚本方式：本地 base64 → PowerShell 写入远程
- SSH 密码认证频繁调用会被限制（Too many authentication failures），需间隔 10 秒

---

## 互动记录

### 2026-04-23
- **Agent健康检查脚本创建**
  - 原脚本不存在，已创建完整健康检查脚本，包含6个检查项目
  - 检查结果：发现3个Git仓库有未提交更改
  - 系统健康度：🟢健康(95/100)
- **自动记忆整理任务执行**
  - 健康检查：发现3个Git仓库有未提交更改
  - 记忆蒸馏：昨日记忆已处理，无新文件需要蒸馏
  - MemPalace清理：session-memory相关wing状态正常
  - Git备份：需要推送3个仓库

### 2026-04-12
- **Agent配置健康检查问题**
  - 发现4个问题：文件过长、截图文件过多、skill数量较多
  - 系统整体健康度：🟢健康(90/100)，Git远程备份未配置
- **上架达人spawn白名单问题**
  - 缺失3个reviewer：backend-reviewer、frontend-reviewer、dev3-reviewer
  - 需修改白名单配置

### 2026-04-11
- **agent-pipeline skill 完善**
  - 迭代合同核心规则写入SKILL.md
  - 通用交付规则写入SKILL.md
- **OpenClaw 多Agent研究**
  - 确认sessions_spawn支持agentId参数
  - 子agent模型限制：只能用glm-5-turbo
- **飞书机器人批量创建与绑定**
  - 9个评审官飞书机器人创建成功
  - 绑定问题修复，6个评审官完成配对批准

### 2026-04-09
- **每日记忆整理完成**
  - Agent文件：183行，MemPalace：49个drawers，状态健康
  - 知识图谱：88个entities，61个triples，无过期事实
- **定时任务监控机制建立**
  - 设置监控cron任务：cron-health-check（每天10:00）
  - 修复配置，更新HEARTBEAT.md

### 2026-04-08
- Agent文件大规模重构（1078→510行）
- 创建共享规则wing：wing_agent_style_guide/room_shared_rules
- 建立定期整理计划

### 2026-04-07
- 科技简报升级为"新闻+大佬观点"双拼版
- BWiki全量爬取完成，新增44KB内容
- 小红书/B站cookie过期，待办cookie自动续期脚本

### 2026-04-06
- 科技简报系统升级（v1→v2）
- 建立AI资讯分析框架
- 追踪安全事件，建立三级优先级信息分类

### 2026-03-24
- 解决Mac合盖断网问题
- 解决Kimi API 401问题
- 卸载Amphetamine，改用系统原生方案## 📈 TradingAgents 金融分析服务（2026-04-28）

### 部署信息
- **位置：** 1060 GPU 服务器 `nyaruko@192.168.31.18:~/TradingAgents`
- **环境：** `~/miniconda3/envs/tradingagents`（Python 3.13）
- **模型：** GLM-5-turbo（智谱 Coding Plan 通道）
- **API：** `https://open.bigmodel.cn/api/coding/paas/v4`
- **代理：** mihomo `127.0.0.1:29538`（LA 节点）
- **Mac 本地已清理**，金融分析只在 1060 上跑

### 三条硬规则
1. **金融分析走 1060** — 所有金融相关任务（TradingAgents、量化分析等）都在 1060 服务器上执行，不在 Mac 本地跑
2. **mihomo GLOBAL 保持 Proxy** — 1060 的 mihomo 代理必须保持 GLOBAL=Proxy 模式，切 DIRECT 会导致外网不通
3. **中文金融内容触发敏感词** — 智谱 Coding Plan 对中文金融讨论（买入/卖出/股价等）容易触发 1301 敏感词过滤，建议 output_language 用 English

### 运行命令
```bash
ssh nyaruko@192.168.31.18
source ~/miniconda3/etc/profile.d/conda.sh
conda activate tradingagents
cd ~/TradingAgents
OPENAI_API_KEY=xxx \
  NO_PROXY=localhost,127.0.0.1,open.bigmodel.cn,*.bigmodel.cn \
  HTTPS_PROXY=http://127.0.0.1:29538 \
  HTTP_PROXY=http://127.0.0.1:29538 \
  python3 -u run_test2.py
```

---

## 2026-04-29 记录
- 记忆蒸馏任务执行完成：健康检查发现2个警告（workspace未提交、agents未提交），MemPalace新增7个drawer和7个fact
- 微店抢票失败教训总结，建立时间敏感任务提前准备规则
- Cron任务修复：三个任务统一用cron-reporter agent，GLM-5.1模型，600s超时
- TradingAgents在1060服务器部署完成，建立金融任务三大硬规则
- 微店抢票任务准备：夏夜叹天津场半自动ADB方案确定
- Playwright电脑端抢票方案失败，确认ADB手机端方案可行
- Cron任务深度分析：发现feishu_doc工具未调用、模型配置错误等共同问题

## 2026-04-27 记录
- 记忆蒸馏任务执行完成：健康检查发现2个警告（workspace未提交、agents未提交），MemPalace新增2个drawer和2个fact
- 中美AI技术差距缩小至2.7%，DeepSeek-V3在算力效率方面取得重大进展

## frp 内网穿透（外网访问）

| 服务 | 地址 |
|------|------|
| 1060 SSH | `ssh -p 6000 nyaruko@8.147.115.189`（密码 Feichang@4zz） |
| 手机 SSH | `ssh -p 6001 u0_a247@8.147.115.189`（密码 Feichang@4zz） |
| 1060 MySQL | `8.147.115.189:6010`（guardian/Feichang@4zz） |
| 1060 Sentinel | `http://8.147.115.189:6020` |
| 手机 Sentinel | `http://8.147.115.189:6021` |
| frps Dashboard | `http://8.147.115.189:7500`（admin/Feichang@4zz） |

- frps 在阿里云 `root@8.147.115.189`（密码 Feichang@4zz）
- frpc 分别跑在 1060（systemd 自启）和手机（Termux bashrc + Termux:Boot）
- SSH config 别名：`ssh 1060-wan` / `ssh phone-wan`

