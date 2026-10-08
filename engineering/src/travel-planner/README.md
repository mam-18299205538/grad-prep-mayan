# 智能旅行助手｜源代码归档

这是智能旅行助手的可恢复源代码归档。当前交付使用 Live 模式，前端运行在 5174，后端运行在 8000。

## 先读这些文档

- `docs/FINAL_HANDOFF.md`：开发者完整交接文档；
- `docs/USER_STARTUP_GUIDE.md`：初学者启动和使用说明；
- `docs/WEBJS_API_HANDOFF.md`：高德 Web JS API 专项说明；
- `docs/README-handoff.md`：交接入口。

## 代码目录

- `backend/`：FastAPI、Live 规划服务和高德 MCP；
- `frontend/`：Vue 3、Vite、页面和地图展示；
- `backend/.env.example`、`frontend/.env.example`：配置模板。

归档不包含真实 `.env`、虚拟环境、`node_modules`、构建产物和 Git 元数据。恢复运行前请按 `docs/FINAL_HANDOFF.md` 重新安装依赖并配置本地密钥。

