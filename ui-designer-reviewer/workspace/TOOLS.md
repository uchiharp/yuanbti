# TOOLS.md - UI设计师·评审官

## UI审查

- 使用 ui-review skill 进行视觉设计评审
- 产出审查报告到协调者指定的路径

## 浏览器预览

```bash
npm run dev                    # 启动前端查看设计效果
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

## 项目信息（由协调者传入）

- **被审查agent：** UI设计师
- **产出路径：** {协调者指定}
---


## 阿里云服务器

- **公网IP:** 8.147.115.189
- **私网IP:** 192.168.1.30
- **配置:** 2核 2G，3Mbps 带宽
- **系统:** Alibaba Cloud Linux 3.2104 LTS 64位
- **地域:** 华北2（北京）可用区 I
- **SSH:** root@8.147.115.189（密码见用户）
- **实例ID:** i-2ze4e3ag2dlgc2mcnw88

### 已安装服务
- **Docker 26.1.3** + Docker Compose v2.27.0
- **PostgreSQL 16 + pgvector 0.8.2**
  - 端口: 5432
  - 数据库: finder
  - 用户: finder
  - 密码: Finder2026secure!
- **Redis 7 Alpine**
  - 端口: 6379
  - 密码: Finder2026redis!

---


## Karpathy 工程准则

编码时必须遵循的四原则（来源：andrej-karpathy-skills）：
1. **先想再写** — 不假设，不确定就问，暴露取舍
2. **简洁优先** — 最少代码解决问题，200行能50行就重写
3. **精准修改** — 只动该动的，不"顺手"改别的代码
4. **目标驱动** — 模糊任务转可验证目标，先列计划

详见：`~/.openclaw/workspace/skills/karpathy-engineering-guidelines/SKILL.md`


## 手机（Termux）

- **ADB 序列号:** ffba2240
- **IP:** 192.168.31.9（局域网）
- **SSH:** `ssh u0_a247@192.168.31.9 -p 8022`，密码 `Feichang@4zz`
- **系统:** Android (ARM64), Termux, Python 3.13.13

### 手机上运行的服务
- **LiteLLM Proxy 1.83.14** → `http://192.168.31.9:4000`（局域网可访问）
  - 可用模型: `glm-4-flash`（智谱 Coding Plan）, `deepseek-v3.2`（火山 Coding Plan）
  - API 格式: OpenAI 兼容，`/v1/chat/completions`

### 远程操作手机
```bash
# SSH 方式
sshpass -p 'Feichang@4zz' ssh -o StrictHostKeyChecking=no u0_a247@192.168.31.9 -p 8022 'command'

# ADB 方式（需 USB 连接）
adb -s ffba2240 shell "run-as com.termux /data/data/com.termux/files/usr/bin/python3 -c '...'"
```

