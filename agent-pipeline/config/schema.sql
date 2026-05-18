-- pipeline.db Schema — 全局流水线状态服务
-- 用法: sqlite3 pipeline.db < schema.sql

PRAGMA foreign_keys=ON;

-- 项目表
CREATE TABLE IF NOT EXISTS projects (
  name        TEXT PRIMARY KEY,
  size        TEXT CHECK(size IN ('small','medium','large')),
  current_phase TEXT NOT NULL DEFAULT 'init',
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 阶段组完成记录
CREATE TABLE IF NOT EXISTS phase_log (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project     TEXT NOT NULL REFERENCES projects(name),
  phase       TEXT NOT NULL,  -- requirements / design / development / quality / delivery
  step        TEXT NOT NULL,  -- discovery / prd-writing / scoring / ...
  status      TEXT NOT NULL CHECK(status IN ('running','done','failed','skipped')),
  score       INTEGER,        -- 质量评分（如有）
  detail      TEXT,           -- JSON 详情
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 功能点标签表
CREATE TABLE IF NOT EXISTS features (
  project     TEXT NOT NULL REFERENCES projects(name),
  req_id      TEXT NOT NULL,  -- REQ-001, REQ-002, ...
  title       TEXT,
  priority    TEXT CHECK(priority IN ('P0','P1','P2','未标注')),
  status      TEXT NOT NULL DEFAULT 'PRD-待确认',
  updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (project, req_id)
);

-- 功能点标签历史
CREATE TABLE IF NOT EXISTS feature_history (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project     TEXT NOT NULL,
  req_id      TEXT NOT NULL,
  status      TEXT NOT NULL,
  phase       TEXT NOT NULL,
  operator    TEXT NOT NULL DEFAULT 'auto',
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 产出物注册表
CREATE TABLE IF NOT EXISTS artifacts (
  project     TEXT NOT NULL REFERENCES projects(name),
  phase       TEXT NOT NULL,
  filename    TEXT NOT NULL,
  checksum    TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (project, phase, filename)
);

-- 门禁检查记录
CREATE TABLE IF NOT EXISTS gates (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project     TEXT NOT NULL REFERENCES projects(name),
  phase       TEXT NOT NULL,
  check_name  TEXT NOT NULL,
  passed      INTEGER NOT NULL CHECK(passed IN (0,1)),
  detail      TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_phase_log_project ON phase_log(project);
CREATE INDEX IF NOT EXISTS idx_features_project ON features(project);
CREATE INDEX IF NOT EXISTS idx_feature_history_req ON feature_history(project, req_id);
CREATE INDEX IF NOT EXISTS idx_gates_project ON gates(project);
