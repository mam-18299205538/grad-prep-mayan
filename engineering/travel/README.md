# HelloAgents 智能旅行助手

基于 HelloAgents 第十三章复现并增强的全栈旅行规划应用。它默认以 **Mock 演示模式**运行，因此没有 LLM、高德或 Unsplash Key 也能完成一次可编辑、可导出的旅行规划；配置密钥后可切换到真实多智能体与高德 MCP 模式。

## 已实现功能

- 根据城市、日期、出行方式、住宿偏好与旅行偏好生成多日行程
- 景点、酒店、三餐、天气、预算和总体建议展示
- 地图标记及按天路线；未配置高德 JS Key 时显示离线路线示意图
- 景点新增、编辑、排序、删除，并在保存时重算预算
- 图片和 PDF 导出、侧边导航、响应式结果页
- 高德 POI、天气、路线 API；Mock 模式下可直接联调
- `mock` / `live` 双模式，避免外部服务或 Key 缺失阻塞开发

## 目录

```text
travel/
├── backend/                 # FastAPI、数据模型、Mock/Live 服务层
├── frontend/                # Vue 3 + TypeScript + Vite
└── README.md
```

## 快速启动：Mock 演示模式

要求：Python 3.10+、Node.js 18+。Windows 下可在两个终端分别执行：

```powershell
# 终端 1：后端
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

```powershell
# 终端 2：前端
cd frontend
npm install --cache .npm-cache
npm run dev -- --host 127.0.0.1
```

打开 `http://127.0.0.1:5173`。后端 API 文档在 `http://127.0.0.1:8000/docs`。

默认不需要创建 `.env`。如果需要显式指定模式，可复制 `backend/.env.example` 为 `backend/.env`，并保持：

```dotenv
APP_MODE=mock
```

Mock 模式内置北京、上海、成都的演示数据；其他城市会使用通用城市行程，用于验证完整前后端流程，不能替代真实出行信息。

## 切换为真实 LLM + 高德 MCP 模式

1. 安装真实服务依赖：

   ```powershell
   cd backend
   .\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements-live.txt
   ```

2. 将 `backend/.env.example` 复制为 `backend/.env`，填入下列配置：

   ```dotenv
   APP_MODE=live
   LLM_MODEL_ID=your-model-name
   LLM_API_KEY=your-api-key
   LLM_BASE_URL=https://api.openai.com/v1
   AMAP_API_KEY=your-amap-web-service-key
   AMAP_MCP_COMMAND=uvx
   UNSPLASH_ACCESS_KEY=your-unsplash-access-key
   ```

3. 为前端创建 `frontend/.env`。配置高德 Web 端 JS Key 后，结果页会替换离线路线示意图为可缩放地图：

   ```dotenv
   VITE_API_BASE_URL=http://127.0.0.1:8000
   VITE_AMAP_WEB_JS_KEY=your-amap-js-key
   ```

若未安装 `uvx`，可将 `AMAP_MCP_COMMAND` 改为 `npx`。真实模式受模型服务、高德接口额度、天气预报范围和网络状况影响；实际出行前请复核开放时间、价格与路线。

## 主要接口

| 方法 | 地址 | 用途 |
|---|---|---|
| `GET` | `/health` | 应用状态和当前模式 |
| `POST` | `/api/trip/plan` | 创建多日旅行计划 |
| `GET` | `/api/map/poi` | 搜索景点 |
| `GET` | `/api/map/weather` | 查询天气 |
| `POST` | `/api/map/route` | 查询路线 |

## 验证状态

已在本机验证：后端健康检查、三日旅行计划、POI、天气、路线接口，以及前端生产构建。前端生产构建会提示体积较大的第三方地图/导出依赖包，但不会阻断运行。
