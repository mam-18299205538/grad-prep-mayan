# 智能旅行助手｜当前版本完整交接文档

最后更新：2026-10-07  
交接对象：后续开发者、维护人员、需要在本机继续测试的技术人员

## 1. 一句话结论

这是一个 Vue 3 + FastAPI 的智能旅行规划应用。当前本机已经配置为 Live 模式：前端负责填写旅行条件和展示结果，后端负责调用 DeepSeek 与高德 MCP 生成真实行程数据，结果页再使用高德 Web JS API 展示交互地图。

当前页面已经完成 Apple Store 风格的视觉统一，首页和结果页的蓝色已替换为石墨灰、钛银灰和雾灰，并加入非常轻的纹理层。

## 2. 项目位置与当前运行地址

- 项目目录：`E:\Tencent Files\github\mayan\work\engineering\travel`
- 前端页面：<http://127.0.0.1:5174/>
- 后端 API：<http://127.0.0.1:8000/>
- 后端 Swagger：<http://127.0.0.1:8000/docs>
- 后端 ReDoc：<http://127.0.0.1:8000/redoc>
- 推荐浏览器：Microsoft Edge
- 当前后端模式：`live`
- 当前后端版本：`1.1.0`

说明：Vite 默认端口是 5173，但本机该端口已有其他进程占用，因此本项目当前用命令行覆盖为 5174。不要把 8000 当作网页地址；8000 是后端接口地址。

## 3. 当前验收状态

截至本次交接，运行状态检查结果如下：

```text
GET http://127.0.0.1:8000/health
status=healthy
mode=live

GET http://127.0.0.1:8000/api/map/health
status=healthy
mode=live
mcp_tools_count=16

GET http://127.0.0.1:5174/
HTTP 200
```

已经完成的真实链路验收：

| 链路 | 状态 | 说明 |
|---|---|---|
| DeepSeek | 已通过 | `deepseek-chat` 最小请求成功返回 |
| 高德 MCP | 已通过 | 成功发现 16 个工具 |
| 高德 POI | 已通过 | 成功搜索景点并补齐经纬度 |
| 高德天气 | 已通过 | 成功获取天气预报并映射到结果模型 |
| 高德路线 | 已通过 | 成功获取路线距离、时间和路径信息 |
| 端到端规划 | 已通过 | Live 模式成功生成多日旅行方案 |
| 高德 Web JS API | 已通过 | 前端脚本 HTTP 请求成功，地图配置已注入 |
| 前端生产构建 | 已通过 | `npm run build` 成功；仅有第三方包体积提示 |
| 前端视觉改造 | 已完成 | 首页、结果页统一为 Apple-inspired 灰阶体系 |

## 4. 系统工作流程

```text
Edge 浏览器
  │
  ├─ 前端 Vue 3 / Vite（5174）
  │      └─ POST /api/trip/plan
  │
  └─ FastAPI 后端（8000）
         ├─ 校验旅行表单
         ├─ DeepSeek 多智能体规划
         ├─ 高德 MCP：POI / 天气 / 酒店 / 路线
         ├─ 解析和整理为统一 TripPlan
         └─ 返回前端结果页

结果页
  ├─ 展示每日景点、酒店、餐饮、天气和预算
  ├─ 允许编辑、排序、新增和删除景点
  ├─ 使用高德 Web JS API 渲染地图
  └─ 没有地图时显示离线路线示意图
```

## 5. 关键目录和文件

```text
travel/
├── backend/
│   ├── app/
│   │   ├── api/main.py                    # FastAPI 入口、CORS、健康检查
│   │   ├── api/routes/trip.py             # 旅行计划接口
│   │   ├── api/routes/map.py              # POI、天气、路线、地图健康检查
│   │   ├── api/routes/poi.py              # 图片和 POI 相关接口
│   │   ├── config.py                      # 环境变量和 Mock/Live 模式
│   │   ├── models/schemas.py              # Pydantic 请求/响应模型
│   │   ├── agents/trip_planner_agent.py   # Live 多智能体规划实现
│   │   └── services/
│   │       ├── planner_service.py         # 规划服务门面
│   │       ├── mock_travel_service.py     # Mock 演示数据
│   │       ├── amap_service.py            # 高德 MCP 与地图业务解析
│   │       ├── llm_service.py             # LLM 服务封装
│   │       └── unsplash_service.py        # 图片服务及降级
│   ├── .env                               # 本机真实配置，不提交
│   ├── .env.example                       # 配置模板
│   ├── requirements.txt                   # 基础依赖
│   └── requirements-live.txt              # Live 模式依赖
├── frontend/
│   ├── src/App.vue                        # 全局布局和 Ant Design 主题
│   ├── src/main.ts                        # 前端入口和全局样式入口
│   ├── src/styles/apple.css                # Apple-inspired 全局灰阶样式
│   ├── src/views/Home.vue                  # 首页规划表单
│   ├── src/views/Result.vue                # 行程结果、地图和编辑功能
│   ├── src/services/api.ts                 # Axios API 客户端
│   ├── .env                               # 本机前端配置，不提交
│   ├── .env.example                       # 配置模板
│   ├── package.json                       # npm 命令和依赖
│   └── vite.config.ts                     # Vite 端口和代理
├── backups/
│   └── travel-v1.0-backup-20261007-160744.zip
├── FINAL_HANDOFF.md                       # 本文档
├── USER_STARTUP_GUIDE.md                  # 初学者使用文档
├── WEBJS_API_HANDOFF.md                   # 高德 Web JS API 专项交接
└── README-handoff.md                      # 交接入口说明
```

## 6. 本机密钥和环境配置

真实密钥仅应存在以下两个本地文件：

- `backend\.env`
- `frontend\.env`

不要把它们上传、复制到聊天、提交到 Git 或放进截图。

后端 `.env` 主要包含：

```dotenv
APP_MODE=live
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=真实 DeepSeek Key
LLM_BASE_URL=https://api.deepseek.com/v1
AMAP_API_KEY=真实高德 Web Service Key
AMAP_MCP_COMMAND=uvx
```

前端 `.env` 主要包含：

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_AMAP_WEB_JS_KEY=高德 Web JS Key
VITE_AMAP_SECURITY_JS_CODE=高德安全密钥
```

重要区别：

- `AMAP_API_KEY` 是后端 Web Service / MCP 使用的 Key。
- `VITE_AMAP_WEB_JS_KEY` 是浏览器地图 JS API 使用的 Key。
- 两者不能互相替代。
- `VITE_AMAP_SECURITY_JS_CODE` 必须和 Web JS Key 属于同一个高德应用。

由于密钥曾经在工作沟通中出现，正式继续使用前建议在高德和 DeepSeek 控制台轮换密钥，并同步更新本地 `.env`。

## 7. 启动方式

### 7.1 后端

打开 PowerShell 窗口：

```powershell
cd "engineering\travel\backend"
.\.venv\Scripts\python.exe -X utf8 -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

必须保留 `-X utf8`，它可以避免 Windows 默认编码导致的启动或日志乱码问题。

### 7.2 前端

再打开第二个 PowerShell 窗口：

```powershell
cd "engineering\travel\frontend"
npm run dev -- --host 127.0.0.1 --port 5174
```

然后在 Edge 打开：<http://127.0.0.1:5174/>

修改任何 `frontend\.env` 中的 `VITE_*` 配置后，必须重启前端窗口，Vite 不会自动重新读取环境变量。

## 8. 首次安装或环境损坏时

### 后端依赖

```powershell
cd "engineering\travel\backend"
.\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements-live.txt
```

### 前端依赖

```powershell
cd "engineering\travel\frontend"
npm install --cache .npm-cache
```

如果公司网络或安全软件阻止下载，请先处理网络权限；不要删除 `.env` 文件来解决依赖安装问题。

## 9. API 入口概览

| 方法 | 路径 | 用途 |
|---|---|---|
| `GET` | `/` | 查看后端名称、版本和文档入口 |
| `GET` | `/health` | 查看后端是否健康及当前模式 |
| `POST` | `/api/trip/plan` | 生成旅行计划 |
| `GET` | `/api/trip/health` | 查看旅行规划服务状态 |
| `GET` | `/api/map/health` | 查看地图服务、Live 模式和 MCP 工具数 |
| `GET` | `/api/map/poi` | 搜索景点或 POI |
| `GET` | `/api/map/weather` | 查询天气 |
| `POST` | `/api/map/route` | 查询路线 |
| `GET` | `/api/poi/photo` | 获取景点图片；失败时安全降级 |

完整参数以 Swagger 为准：<http://127.0.0.1:8000/docs>。

## 10. 验收命令

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/map/health
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:5174/
```

Live 模式至少应看到：

```text
health.status = healthy
health.mode = live
map.mcp_tools_count = 16
前端 HTTP 状态码 = 200
```

前端生产构建：

```powershell
cd "engineering\travel\frontend"
npm run build
```

当前构建已通过。Vite 只提示地图、PDF 和图片相关第三方依赖体积偏大，不属于构建失败。

## 11. 已完成的重要修复

- 创建并接入前后端 `.env`。
- 修复高德 Web JS API 安全密钥必须在加载 JS API 前注入的问题。
- 区分高德 Web JS Key 与 Web Service Key。
- 修复 Windows 环境下 `uvx` 命令路径问题，优先使用 `backend\.venv\Scripts\uvx.exe`。
- 修复高德 MCP POI、天气、路线返回结果的解析和字段映射。
- 修复 MCP 返回文本前缀导致的 JSON 解析问题。
- 增加地图加载失败诊断信息。
- 增加无地图 Key 时的离线路线示意图。
- 增加 Live 端到端行程生成验证。
- 完成首页、结果页和 Ant Design 全局主题的 Apple-inspired 灰阶改造。
- 已生成 v1.0 本地备份：`backups\travel-v1.0-backup-20261007-160744.zip`。

## 12. 常见故障排查

### 12.1 8000 端口已被占用

```powershell
netstat -ano | findstr LISTENING | findstr :8000
```

先确认占用进程确实属于本项目，再处理旧进程。不要结束不明系统进程。

### 12.2 页面打不开

依次检查：

1. 后端窗口是否仍在运行；
2. `Invoke-RestMethod http://127.0.0.1:8000/health` 是否返回 `healthy`；
3. 前端是否使用 5174 端口；
4. Edge 是否打开了 `http://127.0.0.1:5174/`，而不是 8000；
5. 前端启动窗口是否显示 `Local: http://127.0.0.1:5174/`。

### 12.3 Live 行程生成失败

检查：

- 后端 `/health` 是否仍为 `mode=live`；
- `/api/map/health` 是否为 `mcp_tools_count=16`；
- DeepSeek 余额、模型权限和网络是否正常；
- 高德 Web Service Key 是否有效、是否超配额；
- 后端日志中是否出现 MCP 启动、超时或 JSON 解析错误。

### 12.4 地图无法显示但行程正常

先确认：

- 浏览器打开的是 5174 页面；
- `frontend\.env` 使用 Web JS Key，而不是 Web Service Key；
- 安全密钥和 Web JS Key 属于同一高德应用；
- 高德控制台已启用 Web 端（JS API）；
- 修改 `.env` 后已重启 Vite；
- Edge 使用 `Ctrl + F5` 强制刷新。

即使地图失败，结果页仍应显示离线路线示意图，这不代表行程接口失败。

### 12.5 Windows 编码错误

使用：

```powershell
.\.venv\Scripts\python.exe -X utf8 -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

不要省略 `-X utf8`。

## 13. 停止方式

分别回到前端和后端 PowerShell 窗口，按 `Ctrl + C`。两个窗口都停止后，本地服务才算完全关闭。

## 14. 备份与恢复

当前 v1.0 备份文件：

travel\backups\travel-v1.0-backup-20261007-160744.zip`

该备份为源代码备份，已排除 `.env`、虚拟环境、`node_modules`、`dist` 和 `.git`。恢复后需要重新安装依赖，并手动重新创建本机 `.env` 文件。

## 15. 后续建议

优先级较高的后续工作：

1. 增加 pytest 后端测试、前端组件测试和 Playwright 浏览器测试；
2. 为 DeepSeek、高德 MCP 增加超时、重试和单服务降级；
3. 对 Live 调用增加请求 ID、耗时和成本日志；
4. 按需拆分地图、PDF、图片等体积较大的前端依赖；
5. 增加计划持久化、登录认证、限流和 HTTPS 后再考虑公网部署；
6. 正式使用前轮换已在工作沟通中出现过的 API 密钥。

