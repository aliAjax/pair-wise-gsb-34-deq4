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

-- 巡检清单版本：DRAFT 可编辑，PUBLISHED 后整行不可变，仅供任务快照引用
CREATE TABLE IF NOT EXISTS checklist_version (
  id INTEGER PRIMARY KEY,
  task_type TEXT NOT NULL,
  scope_key TEXT NOT NULL DEFAULT 'DEFAULT',
  version INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'DRAFT',
  items JSONB NOT NULL DEFAULT '[]',
  remark TEXT,
  published_at TEXT,
  published_by TEXT,
  created_at TEXT,
  created_by TEXT,
  UNIQUE (task_type, scope_key, version)
);

CREATE INDEX IF NOT EXISTS idx_checklist_published
  ON checklist_version (task_type, scope_key, status, version);

CREATE TABLE IF NOT EXISTS inspection_task (
  id INTEGER PRIMARY KEY,
  building_id TEXT,
  inspector_id TEXT,
  plan_date TEXT,
  task_type TEXT,
  status TEXT,
  checklist_version TEXT,
  finished_at TEXT,
  -- 建任务时固定的清单版本主键/版本号与检查项快照（含判级规则）
  checklist_version_id INTEGER REFERENCES checklist_version(id),
  version_no INTEGER,
  pinned_items JSONB NOT NULL DEFAULT '[]',
  created_at TEXT,
  created_by TEXT,
  -- 发布与建任务并发时回传给创建人的提示
  version_notice TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_task_pinned_version ON inspection_task (checklist_version_id);

CREATE TABLE IF NOT EXISTS inspection_result (
  id INTEGER PRIMARY KEY,
  task_id TEXT,
  device_id TEXT,
  item_code TEXT,
  result_status TEXT,
  measured_value TEXT,
  photo_url TEXT,
  note TEXT,
  -- 按任务固定版本判出的等级
  judged_severity TEXT,
  checklist_version TEXT,
  submitted_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_result_task ON inspection_result (task_id);

CREATE TABLE IF NOT EXISTS hazard_ticket (
  id INTEGER PRIMARY KEY,
  result_id TEXT,
  severity TEXT,
  owner_id TEXT,
  deadline TEXT,
  rectify_status TEXT,
  rectify_note TEXT,
  closed_at TEXT,
  -- 设备冗余用于"同设备未关闭隐患"合并；found_count 累计发现次数
  device_id TEXT,
  found_count INTEGER NOT NULL DEFAULT 1,
  merged_result_ids JSONB NOT NULL DEFAULT '[]',
  last_found_at TEXT,
  created_at TEXT
);

-- 同一设备最多一张未关闭隐患单（OPEN 以外的状态视为已关闭，不参与合并）
CREATE UNIQUE INDEX IF NOT EXISTS uq_open_ticket_per_device
  ON hazard_ticket (device_id)
  WHERE rectify_status <> 'CLOSED';

CREATE INDEX IF NOT EXISTS idx_ticket_device_status ON hazard_ticket (device_id, rectify_status);

CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY,
  actor TEXT,
  action TEXT,
  target_type TEXT,
  target_id TEXT,
  detail TEXT,
  created_at TEXT
);

-- 发布、任务完成、隐患合并的追溯查询
CREATE INDEX IF NOT EXISTS idx_audit_target ON audit_log (target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log (action, created_at);
