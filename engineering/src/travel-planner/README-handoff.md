# HelloAgents 智能旅行助手｜交接入口

最后更新：2026-10-07

本项目当前已经完成本机 Live 模式配置、DeepSeek 与高德 MCP 联调、高德 Web JS 地图接入、Edge 测试以及 Apple-inspired 高级灰视觉改造。

## 请按使用场景阅读

- 开发者、维护人员：阅读 [FINAL_HANDOFF.md](FINAL_HANDOFF.md)
- 完全不熟悉开发的普通用户：阅读 [USER_STARTUP_GUIDE.md](USER_STARTUP_GUIDE.md)
- 只处理高德 Web JS API：阅读 [WEBJS_API_HANDOFF.md](WEBJS_API_HANDOFF.md)
- 项目原始说明：阅读 [README.md](README.md)

## 当前地址

- 网页：<http://127.0.0.1:5174/>
- 后端：<http://127.0.0.1:8000/>
- Swagger：<http://127.0.0.1:8000/docs>

## 当前模式

```text
APP_MODE=live
DeepSeek：已配置
高德 Web Service / MCP：已配置
高德 Web JS API：已配置
MCP 工具数：16
```

## 当前备份

```text
backups\travel-v1.0-backup-20261007-160744.zip
```

备份不包含本机 `.env`、虚拟环境、`node_modules`、`dist` 和 `.git`。恢复后需要重新安装依赖，并按完整交接文档重新配置本地密钥。

## 最短启动方式

后端窗口：

```powershell
cd "E:\Tencent Files\github\mayan\work\engineering\travel\backend"
.\.venv\Scripts\python.exe -X utf8 -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

前端窗口：

```powershell
cd "E:\Tencent Files\github\mayan\work\engineering\travel\frontend"
npm run dev -- --host 127.0.0.1 --port 5174
```

然后打开 <http://127.0.0.1:5174/>。

