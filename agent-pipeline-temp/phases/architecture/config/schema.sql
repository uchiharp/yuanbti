-- pipeline.db Schema — 共用流水线状态
-- 需求组 + 架构组 + 后续阶段 共用同一个 database
-- 用法: sqlite3 pipeline.db < schema.sql

PRAGMA foreign_keys=ON;

-- ─── 项目表 ───
CREATE TABLE IF NOT EXISTS projects (
  name          TEXT PRIMARY KEY,
  size          TEXT CHECK(size IN ('small','medium','large')),
  current_phase TEXT NOT NULL DEFAULT 'init',
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── 阶段日志表 ───
-- phase 字段区分不同阶段组：
--   'requirements' — 需求组（discovery, prd-writing, scoring, review, finalize）
--   'architecture' — 架构组（arch-design, arch-quality-score, arch-review, arch-user-review, tech-spike, arch-finalize）
--   'design'       — 旧设计组（兼容 film-auth2.0 已有数据）
--   'development'  — 开发组（未来扩展）
--   'qa'           — QA组（未来扩展）
CREATE TABLE IF NOT EXISTS phase_log (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project     TEXT NOT NULL REFERENCES projects(name),
  phase       TEXT NOT NULL,
  step        TEXT NOT NULL,
  status      TEXT NOT NULL CHECK(status IN ('running','done','failed','skipped')),
  score       INTEGER,
  detail      TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── 功能点表 ───
-- 需求组写入 REQ-xxx，架构组读取并更新状态
CREATE TABLE IF NOT EXISTS features (
  project     TEXT NOT NULL REFERENCES projects(name),
  req_id      TEXT NOT NULL,
  title       TEXT,
  priority    TEXT CHECK(priority IN ('P0','P1','P2','未标注')),
  status      TEXT NOT NULL DEFAULT 'PRD-待确认',
  updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (project, req_id)
);

-- ─── 功能点历史表 ───
CREATE TABLE IF NOT EXISTS feature_history (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project     TEXT NOT NULL,
  req_id      TEXT NOT NULL,
  status      TEXT NOT NULL,
  phase       TEXT NOT NULL,
  operator    TEXT NOT NULL DEFAULT 'auto',
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── 产出物注册表 ───
-- 架构组注册 ARCHITECTURE.md, docker-compose.test.yml 等
CREATE TABLE IF NOT EXISTS artifacts (
  project     TEXT NOT NULL REFERENCES projects(name),
  phase       TEXT NOT NULL,
  filename    TEXT NOT NULL,
  checksum    TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (project, phase, filename)
);

-- ─── 索引 ───
CREATE INDEX IF NOT EXISTS idx_phase_log_project ON phase_log(project);
CREATE INDEX IF NOT EXISTS idx_features_project ON features(project);
CREATE INDEX IF NOT EXISTS idx_feature_history_req ON feature_history(project, req_id);
CREATE INDEX IF NOT EXISTS idx_phase_log_phase_step ON phase_log(project, phase, step);
