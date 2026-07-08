# API

FastAPI 后端骨架，按 MVP 主链路拆出规则书、提问和健康检查入口。当前实现只返回占位数据，不进行真实 OCR、embedding、向量检索或 LLM 调用。

## 本地启动

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m uvicorn app.main:app --reload --port 8000
```

根目录可用：

```powershell
npm run dev:api
```

## 数据库

根目录运行：

```powershell
docker compose up -d postgres
```

首次创建数据库时会执行 `migrations/0001_initial_schema.sql`，启用 `pgvector` 并创建 MVP 最小数据表。已经存在的 Docker volume 不会自动重放迁移。

## 模块边界

- `app/api/routes`：HTTP 路由。
- `app/domain`：Pydantic schema 和领域枚举。
- `app/services/ports.py`：OCR、embedding、向量检索和 LLM 的可替换接口。
- `migrations`：PostgreSQL + pgvector 初始 schema。
