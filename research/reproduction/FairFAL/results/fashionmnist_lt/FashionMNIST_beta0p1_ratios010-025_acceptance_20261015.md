# FashionMNIST-LT beta=0.1：10%–25%比例组验收

- 验收时间：2026-10-15 12:11:40 CST（远端）
- 代码：`ca14e07bad60c1d1d29a5cb1dbc8ff812689e87e`
- 范围：标注比例10%、15%、20%、25%；每比例seed 1–5，共20个seed-stage单元。
- 结论：四个比例组均通过，每组5/5；这属于阶段产物验收，不代表beta0.1整条长进程退出。

## 门槛证据

- 20份`results.csv`均含表头及100条epoch记录，epoch恰为0–99（101行）。
- 20份`last.pt`均存在、非空、各460,822 bytes；CSV与checkpoint的size/mtime在读取前后及间隔1秒复查均稳定。
- 20个CSV及20个checkpoint的SHA256均记录在远端最终验收JSON与归档包`acceptance.json`/`file_manifest.json`。
- 五条当前训练命令均仍存活，seed、数据集、beta、模型、方法、100轮和比例续接参数与计划一致；固定代码commit已核对。
- 20/20 seed日志递归扫描，致命错误匹配数为0。
- 因每seed beta0.1是跨比例的长进程，未虚构比例级`exit_status=0`；整run退出码待自然结束后登记。

## 归档状态

- 远端包：`/root/autodl-tmp/archives/fmnist_lt/FashionMNIST_beta0p1_ratios010-025_group_20261015T121233_ca14e07.tar.gz`
- 大小：8,888,307 bytes
- SHA256：`0686c07e4dcad51a3c164e88d3d9c9df59fa097eb499b8e7b82dfe1cdd20185e`
- 本地转存：待完成。已尝试JupyterLab文件浏览器下载，但本地Downloads未出现该包；因此没有声称本地SHA对账通过。远端原始结果及归档包保留。

## 训练状态边界

2026-10-15 12:15:21 CST单点`nvidia-smi`：RTX 3080 Ti 64% GPU、2,449/12,288 MiB、63°C、207.92 W；PID 2185、2187、2188、2189、2190均存活。日志文件mtime更新至约12:15 CST；本轮未读其日志内容，30%当前轮次标为未核验。单点利用率不是持续平均值。
 
## 本地转存状态更新｜2026-10-15 12:29 CST

远端10%–25%组级最终验收结果保持PASS，归档SHA为 0686c07e4dcad51a3c164e88d3d9c9df59fa097eb499b8e7b82dfe1cdd20185e。按用户授权操作JupyterLab下载菜单后，本地Downloads仍未生成归档；同源Jupyter文件直链返回 ERR_BLOCKED_BY_CLIENT。因此尚无本地包可供SHA对账。保留远端原件；不绕过浏览器策略。后续使用经可信渠道核验主机身份的传输方式，或由用户从外部浏览器下载后再核对SHA。

## 本地转存重试｜2026-10-15 12:45 CST

再次通过 GPT 内置浏览器的 JupyterLab 文件浏览器“下载”菜单尝试转存。目标包未出现在本地 Downloads 或本实验 archives 目录，因此没有本地包大小或 SHA256 可记录；本地转存及哈希对账仍未完成。远端原包保留，远端SHA256仅沿用12:11验收记录，本轮未重算。不得把远端组验收PASS误写为本地归档完成。
