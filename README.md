# 消防设施巡检维保平台（fire-inspect）

面向园区和物业公司的消防设备巡检、隐患整改、维保计划和合规台账系统。

本版本新增**可发布巡检清单（版本固定）**能力：物业发布新清单不会再“换掉”已领取任务的检查项；任务建单时固定当时已发布版本，提交按该版本判级，异常项生成隐患单，同一设备存在未关闭隐患时合并并累计发现次数；发布、任务完成、隐患合并全过程可追溯。

## 快速启动

```bash
cp .env.example .env && docker compose up -d
```

- 前端：<http://localhost:20103>
- 后端健康检查：<http://localhost:21103/health>

## 版本固定巡检清单（本次变更说明）

### 业务规则

1. **清单只有发布后才能被任务引用**：清单版本有 `DRAFT / PUBLISHED / ARCHIVED` 三态；发布新草稿时，同任务类型的旧已发布版本归档。
2. **建任务时固定版本**：创建任务即在 `checklist:{task_type}` 锁内读取“当前最新已发布版本”，把版本号、版本 ID 与**检查项+判级规则快照**整体冻结到任务上（`checklist_version / checklist_version_id / checklist_snapshot / version_pinned_at`）。执行期间后续发布只归档清单表中的旧版本，任务快照不变。
3. **提交按固定版本判级**：`POST /api/inspection-task/{id}/submit` 以任务快照为唯一判级依据：
   - 快照中的检查项逐个判定，未录入记为 `NOT_CHECKED`，不凭空判异常；
   - 提交了不属于固定版本的检查项（例如新版本新增项）返回 `RESULT_ITEM_UNKNOWN`（422），杜绝按新规则误判；
   - 支持三类规则：选项判定 `options`、阈值区间 `threshold`、有无判定 `presence`，异常等级取条目上的 `fail_severity`。
4. **异常项生成隐患单，同设备未关闭隐患合并**：异常结果触发隐患单；若该 `device_id` 已有 `OPEN/RECTIFYING/REVIEWING` 单据，则合并原单：`found_count += 1`、刷新 `latest_result_id/updated_at`、隐患等级就高不就低。关闭后再次发现异常则新建单据。
5. **可追溯**：发布（含旧版本归档）、建任务固定版本、任务提交判级、隐患创建/合并/关闭均写入审计台账 `GET /api/audit-log`（可按 `action`、`target_type` 过滤）。
6. **发布与建任务同时发生**：二者经同一把命名锁串行化；建任务时间与版本发布时间相差 ≤1s 视为同时发生，新任务采用刚发布的版本，并通过任务上的 `version_notice` 提示创建人，审计日志记录 `simultaneous_publish=true`。

### 主要接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/checklist-version` | 清单版本列表（含检查项与规则） |
| POST | `/api/checklist-version/draft` | 起草新版本 |
| POST | `/api/checklist-version/{id}/publish?actor_id=` | 发布草稿，旧版本归档 |
| GET | `/api/inspection-task` | 任务列表（含固定版本快照） |
| POST | `/api/inspection-task` | 建任务，固定当前已发布版本（可能返回 `version_notice`） |
| POST | `/api/inspection-task/{id}/submit` | 按固定版本判级提交，异常项生成/合并隐患单 |
| GET | `/api/hazard-ticket` | 隐患单列表（含 `found_count` 合并次数） |
| POST | `/api/hazard-ticket/{id}/close` | 复验关闭 |
| GET | `/api/audit-log` | 发布/完成/合并追溯 |

### CLI 示例

```bash
# 1. 发布 v2 清单（v1 自动归档；进行中任务不受影响）
curl -X POST "http://localhost:21103/api/checklist-version/2/publish?actor_id=1"

# 2. 建任务：自动固定当前最新已发布版本
curl -X POST http://localhost:21103/api/inspection-task \
  -H "Content-Type: application/json" \
  -d '{"building_id":1,"inspector_id":2,"plan_date":"2026-10-01","task_type":"HYDRANT","created_by":1}'

# 3. 提交：按任务固定版本判级，异常项生成/合并隐患单
curl -X POST http://localhost:21103/api/inspection-task/1/submit \
  -H "Content-Type: application/json" \
  -d '{"actor_id":1,"results":[{"item_code":"HYD-PRESSURE","measured_value":"0.10","device_id":1}]}'

# 4. 追溯隐患合并记录
curl "http://localhost:21103/api/audit-log?action=HazardTicket.merge"
```

后端测试（覆盖：发布不影响已领取任务、按固定版本判级、异常建单、同设备合并累计、关闭后新建、未知项拒绝、并发发布/建任务、审计追溯）：

```bash
cd backend && python3 -m pytest tests/ -q
```

## 本地开发方式

- 前端：`cd frontend && npm install && npm run dev`（Vite，端口 5173，接口统一走 `/api`）
- 后端：`cd backend && pip install -r requirements.txt && uvicorn src.main:app --reload --port 8000`
- 后端启动时以内存种子数据引导：预置已发布清单 `HYDRANT v1.0.0` 与待发布草稿 `v2.0.0`（收紧压力阈值），便于直接验证“发布不影响已领取任务、只影响新任务”。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | React 18 + TypeScript + Vite + Material UI + Redux Toolkit（状态层使用 zustand store） |
| 后端 | FastAPI + Python 3.11 + SQLAlchemy 2.0 |
| 数据库 | PostgreSQL 15（当前运行态数据为内存存储，`database/init.sql` 给出对应表结构） |
| 部署 | Docker Compose |

## 项目目录结构

```text
frontend/src/
├── api/                  # 按实体分文件（含 ChecklistVersion.ts、AuditLog.ts）
├── stores/               # 按实体分文件（含 ChecklistVersionStore）
├── types/                # ChecklistVersion / TaskSubmitResponse / AuditLog 等
├── constants/            # 枚举、错误码、错误消息、日志模板、状态文案
├── constructors/         # 默认对象/表单/响应构造器
├── components/common/    # StatusBadge / ChecklistPanel / TimelineList / HazardSeverityTag …
├── hooks/                # useChecklistProgress（固定版本进度）/ useHazardFlow（提交+隐患合并）
├── pages/                # Dashboard / Devices / Tasks / Hazards / Reports
├── router/ utils/ mocks/
backend/src/
├── routes/ controllers/ services/ repositories/ models/
├── middlewares/          # auth / rbac / audit_log / error_handler
├── constants/            # checklist_status / result_outcome / hazard_rectify_status / 错误码/日志模板
├── constructors/ types/ exceptions/ utils/ config/
backend/tests/            # 版本固定与隐患合并端到端测试
database/init.sql         # 清单版本、固定版本字段、隐患合并字段、审计表结构
```

## 环境变量说明

- `COMPOSE_PROJECT_NAME`: Compose 项目名，默认 `fire-inspect`
- `FRONTEND_PORT`: 前端端口，默认 `20103`
- `BACKEND_PORT`: 后端端口，默认 `21103`
- `DB_PORT`: 数据库宿主机端口，默认 `54320`
- `DB_USER/DB_PASSWORD/DB_NAME`: 数据库凭据（默认 `app_user/app_password/app_db`）
- `JWT_SECRET`: 本地开发密钥

## Docker 部署说明

- 根 Compose 文件不写 `version`，顶层 `name: fire-inspect`。
- 容器名均使用 `${COMPOSE_PROJECT_NAME:-fire-inspect}` 前缀；前端 `${FRONTEND_PORT:-20103}:80`，后端 `${BACKEND_PORT:-21103}:8000`。
- 数据库使用命名卷 `db_data`，不绑定挂载到中文路径；`db` 配置 healthcheck，后端 `depends_on: condition: service_healthy`，前端依赖后端健康。
- 前端 Nginx 将 `/api/` 反代到 `http://backend:8000/`，并配置 `try_files $uri $uri/ /index.html;`。
- 常见问题：端口占用时改 `.env` 端口后 `docker compose up -d`；重置数据执行 `docker compose down -v`。

## 枚举/常量出现位置清单

- **DeviceType**: `constants/DeviceType(.ts/.py)`、`types/`、构造器、日志模板、错误消息、筛选器、展示组件/控制器。
- **InspectionStatus**: 前后端 `constants/InspectionStatus`（后端另含 `TASK_SUBMITTABLE_STATUSES`）、类型、构造器、日志模板（pin/submit/review）、错误消息（TASK_NOT_SUBMITTABLE）、任务列表筛选与 `StatusBadge` 展示、提交服务判空。
- **HazardSeverity**: 前后端 `constants/HazardSeverity`、类型、`HazardSeverityTag` 展示、清单条目 `fail_severity`、隐患合并就高不就低（后端 `_SEVERITY_RANK`）、日志与错误消息。
- **ChecklistStatus（新增）**: 后端 `constants/checklist_status.py`、发布/归档服务与错误码（CHECKLIST_NOT_PUBLISHABLE）、审计日志模板；前端 `constants/ChecklistStatus.ts`、`types/ChecklistVersion.ts`、发布面板 `StatusBadge` 与 store。
- **ResultOutcome（新增）**: 后端 `constants/result_outcome.py`、`utils/checklist_grader.py`、结果模型/构造器/数据库列、提交服务；前端 `constants/ResultOutcome.ts`、结果类型、提交结果列表样式。
- **HazardRectifyStatus（新增）**: 后端 `constants/hazard_rectify_status.py`（含 `HAZARD_OPEN_STATUSES` 合并判定）、隐患服务/仓储查询；前端同名常量、隐患列表与关闭按钮显隐。
- 错误码：后端 `constants/error_codes.py` + `error_messages.py`（service/controller 分别包装为 `ServiceError/ControllerError`），前端 `constants/errorCodes.ts` + `errorMessages.ts`（`useHazardFlow` 映射提示）。

## 为什么会牵一发动全身

检查项规则、版本状态、判级结论与整改状态被刻意分散在常量、类型、构造器、仓储、服务、控制器、store、hooks、页面组件和数据库脚本中；调整一次判级口径或合并条件，需要同步后端常量/判级器/服务/审计模板、前端枚举/类型/构造器/hook/展示组件、`database/init.sql`、种子数据与 README，并由跨层测试兜底。

## License

MIT
