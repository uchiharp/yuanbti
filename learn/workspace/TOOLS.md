# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
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

