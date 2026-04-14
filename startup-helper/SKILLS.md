# SKILLS.md - 创业助手技能

## 可用技能

| 技能 | 用途 | 触发场景 |
|------|------|----------|
| **feishu-doc** | 飞书文档读写 | 需要读取/编辑飞书文档时 |
| **feishu-drive** | 飞书云盘管理 | 需要上传/下载文件时 |
| **feishu-wiki** | 飞书知识库 | 需要查询知识库内容时 |
| **web_search** | 网络搜索 | 市场调研、竞品分析 |

---

## 飞书集成配置

**App ID:** `cli_a944cc3f77b89bd2`
**App Secret:** 已保存在 `auth-profiles.json`

**权限范围：**
- 文档读写
- 消息接收
- 机器人对话

---

## 使用说明

1. 用户通过飞书机器人发送消息
2. Agent 接收消息并处理
3. 根据需要调用飞书 API（文档/云盘/知识库）
4. 返回处理结果

---

*技能配置会根据实际使用逐步完善 🚀*


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

