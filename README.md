# 消防设施巡检维保平台

面向园区和物业公司的消防设备巡检、隐患整改、维保计划和合规台账系统。

## 快速启动

```bash
cp .env.example .env && docker compose up -d
```

## 访问地址或 CLI 示例

前端：<http://localhost:20103>

后端健康检查：<http://localhost:21103/health>


## 本地开发方式

- 前端：`cd frontend && npm install && npm run dev`
- 后端：进入 `backend` 后按技术栈运行开发命令，接口统一挂在 `/api`。


## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | React 18 + TypeScript + Vite + Material UI + Redux Toolkit |
| 后端 | FastAPI + Python 3.11 + SQLAlchemy 2.0 |
| 数据库 | PostgreSQL 15 |
| 部署 | Docker Compose |

## 项目目录结构

```text
frontend/src/api, stores, types, constants, constructors, components/common, hooks, pages, router, utils, mocks
backend/src/routes, controllers, services, models, repositories, middlewares, constants, constructors, utils, types, config
```

## 环境变量说明

- `COMPOSE_PROJECT_NAME`: Compose 项目名，默认 `fire-inspect`
- `FRONTEND_PORT`: 前端端口，默认 `20103`
- `BACKEND_PORT`: 后端端口，默认 `21103`
- `DB_PORT`: 数据库宿主机端口
- `DB_USER/DB_PASSWORD/DB_NAME`: 本地数据库凭据

## Docker 部署说明

- 根 Compose 文件不写 `version`，顶层 `name: fire-inspect`。
- 容器名均使用 `${COMPOSE_PROJECT_NAME:-fire-inspect}` 前缀。
- 数据库使用命名卷，避免绑定中文路径。
- 常见问题：端口占用时修改 `.env` 中端口后重启；需要重置数据时执行 `docker compose down -v`。

## 巡检清单版本化（发布-建任务-提交-隐患闭环）

平台核心业务规则，解决"物业发布新清单后在执行任务被换掉、按新规则判级、隐患单重复"的问题：

1. **清单可发布、版本不可变**：清单按设备类型（`task_type`）维护草稿（`DRAFT`），`POST /api/checklist-version/{id}/publish` 发布为 `PUBLISHED`；已发布版本行永久冻结，只保留不覆盖。
2. **建任务时固定版本**：`POST /api/inspection-task` 在全局锁内读取"当前已发布版本"，把版本号、版本主键与**检查项+判级规则快照**（`pinned_items`）写入任务；任务执行期间不再受后续发布影响。
3. **提交按固定版本判级**：`POST /api/inspection-task/{id}/submit` 仅接受 `pinned_items` 中存在的 `item_code`（不属于该版本直接报 `CHECKLIST_ITEM_NOT_FOUND`），由 `utils/checklist_grader.py` 按 NUMERIC / CHOICE / TEXT 规则判定 NORMAL/ABNORMAL 与 LOW/MEDIUM/HIGH/CRITICAL 等级。
4. **异常项生成隐患单并合并去重**：异常结果生成隐患单；若**同一设备已有未关闭**（`rectify_status != CLOSED`）隐患，则并入原单：`found_count` 累计 +1、等级取最高、`merged_result_ids` 追加；复验关闭后同设备再次异常才新开单。数据库层用唯一部分索引 `uq_open_ticket_per_device` 兜底。
5. **发布与建任务并发**：发布与建任务共用同一把锁串行化；创建表单带上打开时看到的 `expected_version_id`，落库时若版本已变，任务采用最新已发布版本，并在响应 `version_notice` 中提示创建人（前端顶部通知条展示）；未带版本号但发布发生在 30 秒并发窗口内也会提示。
6. **全程可追溯**：发布（`ChecklistVersion.publish` / `.publish_concurrent`）、建任务固定版本（`InspectionTask.create.pinned_checklist`）、任务完成（`InspectionTask.submit`）、隐患新建/合并（`HazardTicket.create` / `.merge`）/关闭（`HazardTicket.status`）均写入 `audit_log`，可经 `GET /api/audit-log?target_type=&target_id=` 按对象回溯。

新增接口：

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/checklist-version` / `?task_type=HYDRANT` | 清单版本列表 |
| GET | `/api/checklist-version/current/{task_type}` | 某类型当前已发布版本 |
| POST | `/api/checklist-version/draft` | 新建草稿（含判级规则项） |
| POST | `/api/checklist-version/{id}/publish` | 发布（不可变） |
| POST | `/api/inspection-task` | 建任务并固定当时已发布版本（返回 `version_notice`） |
| GET | `/api/inspection-task/{id}` | 任务详情（含 `pinned_items` 与结果） |
| POST | `/api/inspection-task/{id}/submit` | 按固定版本判级，生成/合并隐患单 |
| POST | `/api/hazard-ticket/{id}/close` | 复验关闭（之后不再合并） |
| GET | `/api/audit-log` | 发布/完成/合并追溯 |

## 枚举/常量出现位置清单

- DeviceType: `backend/src/constants/device_type.py`、前端 `constants/DeviceType.ts`；前端出现在 types/DeviceType、constructors（TaskCreateDialog 默认类型）、mocks/seedData、日志模板、TasksPage/ChecklistPublishPanel 筛选与展示。
- InspectionStatus: `backend/src/constants/inspection_status.py`、前端 `constants/InspectionStatus.ts`；出现在 types、constructors、logTemplates、errorMessages、任务状态筛选、StatusBadge 展示。
- HazardSeverity: `backend/src/constants/hazard_severity.py`、前端 `constants/HazardSeverity.ts`；出现在 types、constructors、清单判级规则默认等级（checklist_grader/ChecklistItem）、formatters.formatRisk、HazardSeverityTag、隐患列表与合并升级逻辑。
- ChecklistRuleType / ChecklistPublishStatus: `backend/src/constants/checklist_rule_type.py`、前端 `constants/ChecklistVersion.ts`；出现在类型（ChecklistVersion.ts）、判级器（checklist_grader.py）、构造器（ChecklistVersionConstructor）、ChecklistPanel 展示、formatters.formatRuleType、发布面板 StatusBadge。
- ResultStatus: `backend/src/constants/result_status.py`、前端 `constants/ResultStatus.ts`；出现在 InspectionResult 类型、判级器、提交结果与 ChecklistPanel。
- RectifyStatus: `backend/src/constants/rectify_status.py`、前端 `constants/RectifyStatus.ts`；出现在 HazardTicket 类型、隐患合并查询（未关闭判定）、隐患页筛选/关闭按钮、formatters.formatRectifyStatus。

## 为什么会牵一发动全身

实体字段、枚举、日志模板、错误消息、构造器、筛选器和展示组件被刻意拆散到多个目录；修改一个状态值通常需要同步类型、构造器、服务、控制器、store、页面、README 与数据库种子。

## License

MIT
