# FashionMNIST-LT dd_beta=100：5%–25%远端组验收

- 验收时间：2026-10-15 14:55:37 CST
- 实例：`kw79e2gzyr-bbdf8b83`
- 固定代码：`ca14e07`；正式run：`fmnist_beta100_seed{1..5}_20261015T1039_ca14e07`
- 验收范围：5%、10%、15%、20%、25%，seed1–5，共25个seed-stage。
- 方法：AutoDL远端CPU；每CSV 100条数据行，字段`epoch`精确覆盖0–99；`last.pt`非空；CSV/checkpoint间隔2秒大小和mtime稳定；五条run日志fatal扫描；逐文件SHA256。

## 结果

25/25 seed-stage均PASS。每个CSV共101行（含表头），每个checkpoint 460,822 bytes；稳定检查通过；fatal错误扫描0匹配；SHA清单已生成。beta=100五条长run仍存活，因此整体退出码待自然结束，不创建比例级exit_status。

首次检查器只识别`Round`列名，返回BLOCKED；核对CSV表头后发现代码实际输出`epoch`，修正字段映射并完成上述通过验收。首次BLOCKED报告保留在远端，不代表数据异常。

## 远端交付物

- 接受报告：`/root/autodl-tmp/archives/fmnist_lt/FashionMNIST_beta100_ratios005-025_20261015T145527+0800_ca14e07_acceptance.json`
- SHA清单：`/root/autodl-tmp/archives/fmnist_lt/FashionMNIST_beta100_ratios005-025_20261015T145527+0800_ca14e07_checksums.sha256`
- 归档包：`/root/autodl-tmp/archives/fmnist_lt/FashionMNIST_beta100_ratios005-025_20261015T145527+0800_ca14e07_group.tar.gz`
- 归档大小：10,750,496 bytes
- 远端SHA256：`c81ba36f303904126d430ad7826b183a030f006195bfa9a15bdf135ce7497dcf`
- 独立sha256sum与sidecar一致；tar.gz目录可读，共57项。远端原件保留。

## 本地转存状态

截至较早记录时为PENDING；后续已于2026-10-15 17:51完成内置浏览器下载、本地10,750,496字节与SHA256匹配，状态现为LOCAL_RECONCILED。最终值见archives/FashionMNIST_local_archive_reconciliation_20261015.md。

## 本轮训练快照（与组验收分开）

2026-10-15 14:57:46 CST，GPU 49%、2451/12288 MiB、65°C、216.09 W。五条进程存活；seed1–5最新可读轮次41/43/53/39/43，精确当前比例未核验。30%结果路径存在，但尚未组级验收。


哈希纠正补记（2026-10-15 16:34 CST）：Jupyter Terminal对远端原包重新分段复读，确认SHA长度64。5%–25%合包：`c81ba36f303904126d430ad7826b183a030f006195bfa9a15bdf135ce7497dcf`；30%包：`8df0a11ad92c950df30a3d6178a11f6a8975898d730c3f70243678979db35d1e`。此前分别漏录1字符，现以上述值为准；两包本地转存仍待完成。

## 本地转存闭环（2026-10-15 17:51:13 CST）
最终PASS合包已下载并完成本地大小/SHA对账，LOCAL_RECONCILED；sidecar与本地实算匹配，详见归档对账清单。