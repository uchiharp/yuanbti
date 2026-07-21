-- schema.sql — 架构师 Pipeline 数据库结构
-- ---------------------------------------------------------------------------
-- 设计要点：
--   1. 与 requirements-pipeline 共用同一个 pipeline.db（每个项目目录下一个）
--   2. 全部 CREATE TABLE IF NOT EXISTS —— 共用 db 时 requirements 阶段已建好
--      基础 5 表（projects/phase_log/features/feature_history/artifacts），本脚本
--      只负责幂等补建架构师专用表（design_items/design_decisions/risks/review_feedback）
--   3. phase 字段区分阶段：phase_log.phase = 'requirements' | 'architecture' | ...
--      artifacts.phase 同理
--   4. projects.current_phase 流转：requirements_done → architecture_done
-- ---------------------------------------------------------------------------

PRAGMA foreign_keys = ON;

-- ─── 项目（共用，已存在则跳过） ───
CREATE TABLE IF NOT EXISTS projects (
  name          TEXT PRIMARY KEY,
  size          TEXT CHECK(size IN ('small','medium','large')),
  current_phase TEXT NOT NULL DEFAULT 'init',
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── 阶段步骤日志（断点续跑核心，共用） ───
-- 每次状态变更 INSERT 新行（只追加，不 UPDATE），最新状态靠 ORDER BY id DESC LIMIT 1
CREATE TABLE IF NOT EXISTS phase_log (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project     TEXT NOT NULL REFERENCES projects(name),
  phase       TEXT NOT NULL,                    -- 'requirements' / 'architecture' / ...
  step        TEXT NOT NULL,                    -- 'arch-design'/'arch-quality-score'/...
  status      TEXT NOT NULL CHECK(status IN ('running','done','failed','skipped')),
  score       INTEGER,                          -- 评分步骤填（架构质量评分）
  detail      TEXT,                             -- JSON: duration_sec/grade/req_count/...
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_phase_log_project ON phase_log(project);

-- ─── 功能点（共用，跨阶段状态机） ───
-- status 流转：PRD-待确认 → PRD-已确认 → 技术方案-待确认 → 技术方案-已确认
--              → ARCH-已设计 → 开发-进行中 → ...
CREATE TABLE IF NOT EXISTS features (
  project     TEXT NOT NULL REFERENCES projects(name),
  req_id      TEXT NOT NULL,
  title       TEXT,
  priority    TEXT CHECK(priority IN ('P0','P1','P2','未标注')),
  status      TEXT NOT NULL DEFAULT 'PRD-待确认',
  updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (project, req_id)
);
CREATE INDEX IF NOT EXISTS idx_features_project ON features(project);

-- ─── 功能点状态历史（审计追踪，共用） ───
CREATE TABLE IF NOT EXISTS feature_history (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project     TEXT NOT NULL,
  req_id      TEXT NOT NULL,
  status      TEXT NOT NULL,
  phase       TEXT NOT NULL,
  operator    TEXT NOT NULL DEFAULT 'auto',
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_feature_history_req ON feature_history(project, req_id);

-- ─── 产出物校验和（共用） ───
CREATE TABLE IF NOT EXISTS artifacts (
  project     TEXT NOT NULL REFERENCES projects(name),
  phase       TEXT NOT NULL,
  filename    TEXT NOT NULL,
  checksum    TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (project, phase, filename)
);

-- ─── 设计项（架构师专用） ───
-- 架构师把 PRD 的 REQ 和自己识别的 TECH 点都登记进来
CREATE TABLE IF NOT EXISTS design_items (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  project       TEXT NOT NULL REFERENCES projects(name),
  item_id       TEXT NOT NULL,           -- REQ-001 或 TECH-001
  item_type     TEXT NOT NULL CHECK(item_type IN ('req','tech')),
  title         TEXT NOT NULL,
  category      TEXT,                    -- tech 类型: infra/middleware/cross-cutting/deploy/monitor
  status        TEXT NOT NULL DEFAULT 'designed' CHECK(status IN ('designed','approved','implemented','verified')),
  module        TEXT,                    -- 所属架构模块
  description   TEXT,
  related_items TEXT,                    -- JSON: 关联的其他 item_id
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(project, item_id)
);
CREATE INDEX IF NOT EXISTS idx_design_items_project ON design_items(project);
CREATE INDEX IF NOT EXISTS idx_design_items_type ON design_items(project, item_type);

-- ─── 架构决策记录 ADR（架构师专用） ───
CREATE TABLE IF NOT EXISTS design_decisions (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  project        TEXT NOT NULL REFERENCES projects(name),
  adr_id         TEXT NOT NULL,            -- ADR-001
  title          TEXT NOT NULL,
  status         TEXT NOT NULL DEFAULT 'proposed' CHECK(status IN ('proposed','accepted','deprecated','superseded')),
  context        TEXT,                     -- 背景
  decision       TEXT,                     -- 决策内容
  alternatives   TEXT,                     -- 备选方案
  consequences   TEXT,                     -- 后果
  related_items  TEXT,                     -- JSON: ["REQ-001","TECH-002"]
  created_at     TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(project, adr_id)
);
CREATE INDEX IF NOT EXISTS idx_design_decisions_project ON design_decisions(project);

-- ─── 风险登记（架构师专用，含 Spike 触发信息） ───
CREATE TABLE IF NOT EXISTS risks (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  project        TEXT NOT NULL REFERENCES projects(name),
  risk_id        TEXT NOT NULL,            -- RISK-001
  category       TEXT NOT NULL CHECK(category IN ('technical','performance','security','dependency','debt')),
  probability    TEXT CHECK(probability IN ('high','medium','low')),
  impact         TEXT CHECK(impact IN ('critical','high','medium','low')),
  description    TEXT NOT NULL,
  mitigation     TEXT,
  related_items  TEXT,                     -- JSON
  requires_spike INTEGER NOT NULL DEFAULT 0,  -- 1=需要 Spike 验证（触发 tech-spike 步骤）
  spike_json     TEXT,                     -- {"goal":"...","timebox_hours":4,"success_criteria":"...","fallback":"..."}
  spike_status   TEXT DEFAULT 'pending' CHECK(spike_status IN ('pending','passed','failed','skipped')),
  status         TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','mitigated','accepted','closed')),
  created_at     TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(project, risk_id)
);
CREATE INDEX IF NOT EXISTS idx_risks_project ON risks(project);
CREATE INDEX IF NOT EXISTS idx_risks_status ON risks(project, status);

-- ─── 评审反馈（对抗评审产物，架构师专用） ───
-- 记录评审中标记为 false 的 blocker/important 数量，供 finalize 追溯
CREATE TABLE IF NOT EXISTS review_feedback (
  id                    INTEGER PRIMARY KEY AUTOINCREMENT,
  project               TEXT NOT NULL REFERENCES projects(name),
  review_file           TEXT NOT NULL,
  blockers_marked_false INTEGER DEFAULT 0,
  important_marked_false INTEGER DEFAULT 0,
  notes                 TEXT,
  marked_at             TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_review_feedback_project ON review_feedback(project);
