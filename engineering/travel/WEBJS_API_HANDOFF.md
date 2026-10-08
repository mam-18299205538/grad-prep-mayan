# 智能旅行助手：Web JS 与 API 模式交接记录

最后更新：2026-10-07

最终交接版本请优先参考：`FINAL_HANDOFF.md`；普通用户启动说明请参考：`USER_STARTUP_GUIDE.md`。

## 项目与目标

- 目标项目：`engineering\travel`
- 当前目标：将旅行助手从 Mock 演示模式切换为持久化的 Live/API 模式，并启用高德 Web JS 地图。
- 用户已提供高德 Web 服务 Key、高德 Web JS Key、高德安全密钥和 DeepSeek Key。**本文件不记录任何真实密钥。**

## 已完成的实现

### 后端

- FastAPI 后端支持 `APP_MODE=mock` 和 `APP_MODE=live`。
- `backend/app/config.py` 在 Live 模式校验高德服务 Key 与 LLM Key。
- Mock 模式下 `/health`、`/api/trip/plan`、POI、天气与路线接口均已验证。
- Live 模式已使用项目虚拟环境真实启动并验证：
  - `/health` 返回 `mode: live`；
  - DeepSeek `deepseek-chat` 最小请求返回 `OK`；
  - 高德 MCP 发现 16 个工具；
  - POI、天气、步行路线接口均返回真实数据；
  - 北京 1 日行程端到端生成成功，返回 4 个景点和预算。
- Live 依赖已安装到项目虚拟环境，包括 `uv`、`uvx` 和 `huggingface_hub`，不再依赖临时 `PYTHONPATH`。
- 已修复高德 MCP 返回结构适配：天气字段映射、路线 `paths[0]` 解析、POI 详情坐标补全。

### 前端

- Vue 3 + TypeScript + Vite 前端已完成行程表单与结果页。
- 未配置高德 JS Key 时，结果页会显示离线路线示意，避免地图区报错或白屏。
- 前端生产构建已成功完成；当前 Vite 开发服务器在 `127.0.0.1:5174` 提供测试页面（5173 已被其他进程占用）。
- 结果页已读取 `VITE_AMAP_WEB_JS_KEY` 和 `VITE_AMAP_SECURITY_JS_CODE`；首次 `AMapLoader.load()` 前会设置 `window._AMapSecurityConfig`。
- 地图加载失败时会在控制台记录是否检测到两类 Key，并显示高德返回的错误详情，便于区分 Key 类型、域名白名单和安全密钥问题。

## 已验证的服务状态

以下进程与端口为上一次会话状态，重新打开应用后不能假定仍在运行：

- 后端：`http://127.0.0.1:8000`（Live）
- 前端：`http://127.0.0.1:5174`

建议每次继续工作前先验证：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

如果返回 `mode: live`，说明当前后端进程确实使用 API 模式；如果是 `mock`，需重新按下文配置和启动。

## 当前状态与剩余阻塞

当前聊天已经可以写入 E 盘项目，以下修改已完成并通过构建验证：

- `frontend/src/env.d.ts`
- `frontend/src/views/Result.vue`
- `frontend/.env.example`
- 清理 `backend/.env.example` 中残留的真实凭据
- 重新构建 `frontend/dist`

本轮已创建并填入用户提供的前端和后端真实配置：

```text
frontend/.env（已创建，已填入 Web JS Key 与安全密钥；不提交 Git）
backend/.env（已创建，已填入高德 Web Service Key 与 DeepSeek Key；不提交 Git）
```

后端当前运行在 Live 模式；修改任一 `.env` 后都必须重启对应服务。

### 本轮真实验收结果

```text
DeepSeek: provider=deepseek, model=deepseek-chat, response=OK
高德 MCP: mode=live, mcp_tools_count=16
高德 POI: 10 条结果，首条含真实经纬度
高德天气: 4 条预报，天气和温度字段正确映射
高德路线: 步行 1064 米，851 秒
端到端行程: mode=live，1 天，4 个景点，包含预算
高德 Web JS: HTTP 200，脚本可访问
```

## 下次继续时需要执行的修改

### 1. `backend/.env`（已完成）

文件位置：`engineering\travel\backend\.env`

不记录真实密钥的配置结构：

```dotenv
APP_MODE=live
HOST=127.0.0.1
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

AMAP_API_KEY=<高德 Web 服务 Key>
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=<DeepSeek Key>
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_TIMEOUT=90
AMAP_MCP_COMMAND=uvx
```

### 2. `frontend/.env`（已完成）

文件位置：`engineering\travel\frontend\.env`

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_AMAP_WEB_JS_KEY=<高德 Web JS Key>
VITE_AMAP_SECURITY_JS_CODE=<高德安全密钥>
```

### 3. 修改 `frontend/src/env.d.ts`（已完成）

将环境变量类型改为：

```typescript
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
  readonly VITE_AMAP_WEB_JS_KEY?: string
  readonly VITE_AMAP_SECURITY_JS_CODE?: string
}
```

### 4. 修改 `frontend/src/views/Result.vue`（已完成）

在 `hasMapKey` 定义后增加：

```typescript
const amapSecurityJsCode =
  import.meta.env.VITE_AMAP_SECURITY_JS_CODE || ''
```

在 `initMap()` 中、`AMapLoader.load(...)` 前增加：

```typescript
if (amapSecurityJsCode) {
  ;(window as any)._AMapSecurityConfig = {
    securityJsCode: amapSecurityJsCode
  }
}
```

### 5. 安装与构建（前端构建已完成）

后端：

```powershell
cd "engineering\travel\backend"
.\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements-live.txt
.\.venv\Scripts\python.exe -m pip install uv
```

前端：

```powershell
cd "engineering\travel\frontend"
npm install --cache .npm-cache
npm run build
```

### 6. 重启并验证

启动后端：

```powershell
cd "engineering\travel\backend"
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

启动前端：

```powershell
cd "engineering\travel\frontend"
npm run dev -- --host 127.0.0.1
```

验证后端：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

必须返回：

```json
{ "status": "healthy", "mode": "live" }
```

然后在前端生成一份行程；地图区域应显示高德底图、Marker 和路线，而不是“未配置高德 JS Key”的离线路线卡片。

## 已知问题与排查

| 现象 | 原因与处理 |
|---|---|
| `No module named 'huggingface_hub'` | 安装 `requirements-live.txt`，不要继续使用临时 `PYTHONPATH` 方案。 |
| `uvx` 找不到 | 已改为优先使用 `backend/.venv/Scripts/uvx.exe` 的绝对路径，避免仅启动 python 时 PATH 不含虚拟环境。 |
| POI 返回空坐标或路线为 0 | 高德 MCP 返回结构不是本地模型字段；适配层已映射天气字段、路线 `paths[0]`，并用 POI 详情补坐标。 |
| Vite 报 `.vite-temp` 的 `EPERM` | 当前项目目录没有写权限；以新的 E 盘主项目打开后再运行 `npm run dev` / `npm run build`。 |
| `--configLoader runner` 报 `__dirname is not defined` | 不使用该规避方式；修复写权限后使用标准 Vite 构建。 |
| `INVALID_USER_KEY` | 检查前端是否填入 Web JS Key，而不是 Web 服务 Key。 |
| `USERKEY_PLAT_NOMATCH` | 高德 Key 类型不匹配，检查高德控制台启用的 JS API 服务。 |
| 安全密钥报错 | 确保 `_AMapSecurityConfig` 在 `AMapLoader.load()` 前设置，且安全密钥与同一高德应用关联。 |

## 安全清理

- `backend/.env.example` 已恢复为占位符；真实配置只应保存于本地 `backend/.env`。
- 只在 `backend/.env` 和 `frontend/.env` 保存真实密钥。
- 确认 `.gitignore` 忽略 `.env` 与 `.env.*`，但保留 `.env.example`。
- 因密钥曾出现在聊天和示例文件中，建议测试完成后在高德和 DeepSeek 控制台轮换密钥。
