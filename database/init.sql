CREATE TABLE IF NOT EXISTS building (
  id INTEGER PRIMARY KEY,
  name TEXT,
  campus TEXT,
  floor_count TEXT,
  fire_grade TEXT,
  manager_id TEXT,
  address_code TEXT
);

CREATE TABLE IF NOT EXISTS fire_device (
  id INTEGER PRIMARY KEY,
  building_id TEXT,
  device_code TEXT,
  device_type TEXT,
  floor TEXT,
  location_desc TEXT,
  install_date TEXT,
  status TEXT,
  next_maintenance_at TEXT
);

-- 巡检清单版本：草稿 -> 已发布 -> （被新版本取代）已归档
CREATE TABLE IF NOT EXISTS checklist_version (
  id INTEGER PRIMARY KEY,
  task_type TEXT NOT NULL,
  version TEXT NOT NULL,
  status TEXT NOT NULL,              -- DRAFT / PUBLISHED / ARCHIVED
  remark TEXT,
  created_by INTEGER,
  published_by INTEGER,
  created_at TEXT,
  published_at TEXT,
  archived_at TEXT,
  items_json TEXT,                   -- 检查项及判级规则（建任务时整体快照）
  UNIQUE(task_type, version)
);
CREATE INDEX IF NOT EXISTS idx_checklist_published
  ON checklist_version(task_type, status, published_at);

CREATE TABLE IF NOT EXISTS inspection_task (
  id INTEGER PRIMARY KEY,
  building_id TEXT,
  inspector_id TEXT,
  plan_date TEXT,
  task_type TEXT,
  status TEXT,
  checklist_version TEXT,
  finished_at TEXT,
  -- 建任务时固定当时版本：版本 ID、固定时间、检查项快照 JSON
  checklist_version_id INTEGER REFERENCES checklist_version(id),
  version_pinned_at TEXT,
  checklist_snapshot_json TEXT,
  created_by INTEGER,
  -- 发布与建任务同时发生时给创建人的提示
  version_notice TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS inspection_result (
  id INTEGER PRIMARY KEY,
  task_id TEXT,
  device_id TEXT,
  item_code TEXT,
  result_status TEXT,
  measured_value TEXT,
  photo_url TEXT,
  note TEXT,
  -- 按任务固定版本判级写入：结论、判级所用版本、判级时间
  outcome TEXT,                     -- NORMAL / ABNORMAL / NOT_CHECKED
  checklist_version TEXT,
  graded_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_result_task ON inspection_result(task_id);

CREATE TABLE IF NOT EXISTS hazard_ticket (
  id INTEGER PRIMARY KEY,
  result_id TEXT,
  device_id INTEGER,                -- 同设备未关闭隐患合并的关联键
  severity TEXT,
  owner_id TEXT,
  deadline TEXT,
  rectify_status TEXT,              -- OPEN / RECTIFYING / REVIEWING / CLOSED
  rectify_note TEXT,
  closed_at TEXT,
  -- 发现次数累计 + 首末异常结果，便于追溯合并过程
  found_count INTEGER DEFAULT 1,
  first_result_id INTEGER,
  latest_result_id INTEGER,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_hazard_device_open
  ON hazard_ticket(device_id, rectify_status);

-- 审计台账：发布、建任务固定版本、任务完成、隐患合并/关闭均可追溯
CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY,
  actor_id TEXT,
  action TEXT,
  target_type TEXT,
  target_id TEXT,
  detail_json TEXT,
  created_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action, created_at);
