---
name: deerflow-integration
version: 2.0.0
description: 与本地DeerFlow服务集成，提供深度研究、数据分析、PPT生成、图像生成、视频生成等强大能力
homepage: https://github.com/your-org/deerflow
metadata: {"api_base":"http://localhost:8001","langgraph":"http://localhost:2024","webui":"http://localhost:3000"}
---

## 元数据
- **type:** tool
- **triggers:** user-request
- **requires:** exec, web_fetch
- **auto-load:** false
- **priority:** medium

---

# DeerFlow Integration

与本地 DeerFlow 服务集成的技能，让你可以通过 Claude Code 调用 DeerFlow 的强大能力。

## 触发条件

当用户请求以下任务时自动激活：
- 深度研究（deep research）
- 复杂多步骤任务
- 需要子智能体协作
- 代码执行和沙盒环境
- 报告生成、PPT 生成、网页设计等

## 配置

确保 DeerFlow 服务正在运行：
- LangGraph API: http://localhost:2024
- Gateway API: http://localhost:8001
- Web UI: http://localhost:3000

## 使用方式

### 1. 通过 Gateway API 调用

```bash
# 发送消息到 DeerFlow
curl -X POST http://localhost:8001/threads/{thread_id}/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "lead_agent",
    "input": {
      "messages": [{"role": "user", "content": "你的问题"}]
    }
  }'
```

### 2. 创建新会话

```bash
# 创建线程
curl -X POST http://localhost:8001/threads \
  -H "Content-Type: application/json" \
  -d '{}'

# 返回 {"thread_id": "xxx-xxx-xxx"}
```

### 3. 获取可用模型

```bash
curl http://localhost:8001/models
```

### 4. 获取可用技能

```bash
curl http://localhost:8001/skills
```

## DeerFlow 内置技能

DeerFlow 自带以下强大技能：

| 技能 | 描述 |
|------|------|
| deep-research | 深度研究和信息收集 |
| data-analysis | 数据分析和可视化 |
| ppt-generation | PPT 演示文稿生成 |
| podcast-generation | 播客内容生成 |
| image-generation | 图像生成 |
| video-generation | 视频生成 |
| web-design | 网页设计 |
| frontend-design | 前端设计 |
| chart-visualization | 图表可视化 |

## 环境变量

在 `~/projects/deer-flow/.env` 中配置：
- `KIMI_API_KEY` - Kimi/Moonshot API 密钥

## 启动 DeerFlow

```bash
cd ~/projects/deer-flow

# 启动后端
cd backend && uv run langgraph dev --no-browser --allow-blocking &
uv run uvicorn app.gateway.app:app --host 0.0.0.0 --port 8001 &

# 启动前端
cd ../frontend && pnpm dev &
```

## 服务端口

| 服务 | 端口 |
|------|------|
| LangGraph | 2024 |
| Gateway | 8001 |
| Frontend | 3000 |
| Nginx (可选) | 2026 |

## 故障排查

### 检查服务状态

```bash
curl http://localhost:2024/ok
curl http://localhost:8001/health
```

### 查看日志

```bash
tail -f ~/projects/deer-flow/logs/langgraph.log
tail -f ~/projects/deer-flow/logs/gateway.log
tail -f ~/projects/deer-flow/logs/frontend.log
```

## 注意事项

1. DeerFlow 需要 Python 3.12+ 和 Node.js 22+
2. 首次启动可能需要下载依赖
3. 使用本地沙盒模式时，命令直接在主机上执行
4. 如需 Docker 沙盒，请安装 Docker Desktop

## 项目位置

DeerFlow 安装目录：`~/projects/deer-flow`
