#工程实践：智能旅行助手
###0.序章
  
    复现工程原因：当前大家做攻略，都是经过问豆包，千问，deepseek，经过多轮对话，有些存在幻象，不符合当下旅游，走马观花，并且展现不突出，存在一定旅游攻略歧义，
    开发复现该工程，有效支撑我们现在旅行的需求，经过一轮对话就可以满足我们的旅游需求。

##1.项目介绍

智能旅行助手是一个本地运行的Web旅行规划应用。用户在首页输入目的地、日期、交通方式、住宿偏好和兴趣标签，后端调用DeepSeek与高德MCP生成真实旅行方案，结果页展示每日安排、景点、酒店、餐饮、天气、预算、路线和地图。

本次归档对应的源代码位于：

```text
engineering/src/travel-planner/
```
开源代码位于：https://github.com/datawhalechina/hello-agents/tree/main/code/chapter13/helloagents-trip-planner


##2.已完成能力

-Vue3+TypeScript+Vite旅行规划首页；
-FastAPI后端和Swagger接口文档；
-DeepSeekLive模式规划；
-高德MCP景点、天气、酒店和路线工具；
-高德WebJSAPI交互地图；
-地图不可用时的离线路线示意；
-每日行程、预算、天气和住宿展示；
-结果页编辑、新增、删除、排序景点；
-图片和PDF导出入口；
-高级灰视觉主题；
-WindowsPowerShell启动说明和完整交接文档。

##3.技术栈

|层|技术|
|---|---|
|前端|Vue3、TypeScript、Vite、AntDesignVue、Axios|
|地图|高德WebJSAPI、@amap/amap-jsapi-loader|
|后端|Python、FastAPI、Pydantic、Uvicorn|
|智能规划|DeepSeek、HelloAgents、多智能体规划|
|外部数据|高德WebService/MCP|
|导出|html2canvas、jsPDF|

##4.运行方式

当前本机使用：

-前端：<http://127.0.0.1:5174/>
-后端：<http://127.0.0.1:8000/>
-Swagger：<http://127.0.0.1:8000/docs>
-模式：`live`

后端窗口：

```powershell
cd"E:\TencentFiles\github\mayan\work\engineering\travel\backend"
.\.venv\Scripts\python.exe-Xutf8-muvicornapp.api.main:app--host127.0.0.1--port8000
```

前端窗口：

```powershell
cd"E:\TencentFiles\github\mayan\work\engineering\travel\frontend"
npmrundev----host127.0.0.1--port5174
```

更完整的说明见归档源代码中的：

-`docs/FINAL_HANDOFF.md`
-`docs/USER_STARTUP_GUIDE.md`
-`docs/WEBJS_API_HANDOFF.md`

##5.运行截图
见\engineering\travel复现结果result.docx

##6.验收结果

```text
GET/health->healthy,mode=live
GET/api/map/health->healthy,mode=live,mcp_tools_count=16
GEThttp://127.0.0.1:5174/->HTTP200
npmrunbuild->通过
```

已完成DeepSeek、高德MCP、POI、天气、路线和端到端行程生成联调。
##7.配置与安全

归档源代码不包含真实`.env`。原开发目录中的配置文件为：

```text
E:\TencentFiles\github\mayan\work\engineering\travel\backend\.env
E:\TencentFiles\github\mayan\work\engineering\travel\frontend\.env
```

归档代码恢复后，需要由维护人员重新配置：

-DeepSeekAPIKey；
-高德WebServiceKey；
-高德WebJSKey；
-高德安全密钥。

不要将任何真实密钥提交到本地归档、Git、截图或聊天记录。

##8.归档内容说明

`engineering/src/travel-planner/`包含可恢复的项目源代码、依赖清单、配置模板和交接文档，但排除了：

-`.env`；
-`.venv`；
-`node_modules`；
-`dist`；
-`.git`；
-上游源码快照；
-临时缓存和运行日志。



