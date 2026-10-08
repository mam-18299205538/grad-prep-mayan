# 智能旅行助手｜初学者完整使用说明

这份说明写给不熟悉代码、PowerShell 和 API 的使用者。你只需要启动两个窗口，然后在 Edge 浏览器中打开网页即可。

## 1. 你需要知道的三件事

1. **前端**就是你看到的网页，地址是 `http://127.0.0.1:5174/`。
2. **后端**是网页背后的服务，地址是 `http://127.0.0.1:8000/`。
3. 前端和后端都要启动，网页才能正常生成旅行计划。

不要直接在浏览器使用 8000 端口。8000 是后台接口，5174 才是给普通用户打开的网页。

## 2. 每次使用前的准备

确认：

- 电脑已经开机；
- 项目文件夹仍在：
  `E:\Tencent Files\github\mayan\work\engineering\travel`
- 可以使用 Microsoft Edge；
- 不要删除或修改项目里的 `.env` 文件。

## 3. 启动后端

### 第一步：打开 PowerShell

按键盘上的 Windows 键，搜索“PowerShell”，打开 Windows PowerShell。

### 第二步：复制并执行后端命令

把下面整段命令复制到 PowerShell，按 Enter：

```powershell
cd "E:\Tencent Files\github\mayan\work\engineering\travel\backend"
.\.venv\Scripts\python.exe -X utf8 -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

这个窗口出现类似下面的文字，说明后端已经启动：

```text
Uvicorn running on http://127.0.0.1:8000
运行模式: live
```

不要关闭这个窗口。关闭窗口就等于关闭后端。

## 4. 启动前端网页

### 第一步：再打开一个 PowerShell

保留刚才的后端窗口，再打开第二个 PowerShell 窗口。

### 第二步：复制并执行前端命令

```powershell
cd "E:\Tencent Files\github\mayan\work\engineering\travel\frontend"
npm run dev -- --host 127.0.0.1 --port 5174
```

看到类似下面的文字，说明网页已经启动：

```text
Local: http://127.0.0.1:5174/
```

这个窗口也不要关闭。

## 5. 打开网页

打开 Microsoft Edge，在地址栏输入：

<http://127.0.0.1:5174/>

如果之前已经打开过网页，建议按一次 `Ctrl + F5`，让 Edge 重新加载最新页面。

## 6. 如何生成一份旅行计划

在首页按下面顺序填写：

1. 在“目的地城市”输入城市，例如：`北京`；
2. 选择开始日期；
3. 选择结束日期；
4. 选择交通方式；
5. 选择住宿偏好；
6. 勾选你感兴趣的旅行偏好；
7. 在最后的文字框补充要求，例如“希望安排适合老人步行的路线”；
8. 点击“生成旅行方案”；
9. 等待方案生成完成。

Live 模式需要访问真实的 DeepSeek 和高德服务，第一次生成可能需要几十秒。生成期间不要重复点击按钮，也不要关闭两个 PowerShell 窗口。

## 7. 结果页可以查看什么

结果页通常包含：

- 总体旅行信息；
- 每天的景点安排；
- 景点地址、介绍和预计游览时长；
- 酒店和餐饮建议；
- 每日天气；
- 预算明细；
- 高德交互地图、景点标记和路线；
- 编辑、排序、新增或删除景点的功能；
- 图片或 PDF 导出入口（具体可用性取决于浏览器和外部服务）。

当前页面使用石墨灰、钛银灰和雾灰风格。如果地图服务暂时不可用，结果页会显示离线路线示意图，行程文字仍可能正常显示。

## 8. 最简单的健康检查

如果不确定后端是否运行，可以打开第三个 PowerShell，执行：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

正常时会看到类似：

```text
status : healthy
mode   : live
```

再检查高德 MCP：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/map/health
```

正常时应包含：

```text
status          : healthy
mode            : live
mcp_tools_count : 16
```

## 9. 如何停止程序

使用完成后：

1. 回到运行后端的 PowerShell 窗口；
2. 按 `Ctrl + C`；
3. 回到运行前端的 PowerShell 窗口；
4. 按 `Ctrl + C`；
5. 关闭 Edge 页面即可。

如果只关闭 Edge，后台服务仍可能继续运行；如果只关闭一个 PowerShell，另一个服务仍然运行。

## 10. 常见问题

### 页面显示“无法连接后端”

先确认后端窗口没有关闭，再执行：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

如果命令失败，重新执行“启动后端”一节的命令。

### 页面打不开或白屏

确认浏览器地址是：

<http://127.0.0.1:5174/>

不要使用 8000。然后按 `Ctrl + F5` 刷新。如果仍然打不开，把前端 PowerShell 窗口最后几行文字发给维护人员。

### 生成方案一直等待

Live 模式需要访问外部服务。先等待几十秒，然后检查：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/map/health
```

如果健康检查正常但生成仍失败，把后端窗口中显示的错误文字发给维护人员。不要把 `.env` 文件发出去。

### 地图没有显示

按 `Ctrl + F5` 刷新页面，确认浏览器地址使用 5174。如果行程文字和路线示意图仍能显示，通常只是地图 JS API 暂时失败；请把页面截图和后端错误信息发给维护人员。

### PowerShell 显示“找不到路径”

确认项目目录没有移动，并完整复制下面的路径：

```text
E:\Tencent Files\github\mayan\work\engineering\travel
```

### 端口占用

如果启动时提示端口被占用，不要随便关闭其他程序。把提示文字完整发给维护人员，由维护人员确认是否是本项目的旧进程。

## 11. 安全注意事项

以下文件含有真实服务密钥，普通用户不需要打开：

- `E:\Tencent Files\github\mayan\work\engineering\travel\backend\.env`
- `E:\Tencent Files\github\mayan\work\engineering\travel\frontend\.env`

请不要：

- 把 `.env` 文件发到群聊或上传网盘；
- 截图时露出密钥；
- 把密钥复制到网页表单；
- 把密钥提交到 Git；
- 为了解决页面问题自行修改密钥。

如果需要报错，请只提供错误提示、页面截图和两个 PowerShell 窗口中不含密钥的日志。

## 12. 需要向维护人员反馈什么

遇到问题时，按下面格式反馈最有效：

```text
1. 我打开的地址：
2. 我执行的是后端还是前端命令：
3. 页面具体提示：
4. /health 是否返回 healthy：是 / 否
5. /api/map/health 的 mcp_tools_count：
6. 后端窗口最后几行非敏感错误：
7. 是否已经按 Ctrl+F5：是 / 否
```

不要附上 `.env` 文件，也不要把 Key 复制到反馈内容中。

