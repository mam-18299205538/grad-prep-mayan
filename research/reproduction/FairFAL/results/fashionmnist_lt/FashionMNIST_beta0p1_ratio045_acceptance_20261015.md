# FashionMNIST-LT dd_beta=0.1 ratio 45% 验收

- 远端验收时间：2026-10-15 13:38:02 CST；固定代码标记：ca14e07。
- 组级结果：5/5 seed 通过远端 CPU 文件门槛。CSV各101行并覆盖Round 0–99；last.pt各非空460,822 bytes；2秒稳定性检查通过；错误扫描0匹配。
- 远端验收报告：`/root/autodl-tmp/archives/fmnist_lt/FashionMNIST_beta0p1_ratio045_acceptance_20261015T133802_ca14e07.json`
- 逐文件哈希清单：`/root/autodl-tmp/archives/fmnist_lt/FashionMNIST_beta0p1_ratio045_checksums_20261015T133802_ca14e07.sha256`
- 远端归档：`/root/autodl-tmp/archives/fmnist_lt/FashionMNIST_beta0p1_ratio045_group_20261015T133802_ca14e07.tar.gz`
- 归档大小：2,134,436 bytes
- 归档 SHA256：`bb06d3cbd3541e210e4113aca0d4a073d5bc2961dc6b087bb6584362cec8ce10`
- 远端原件：保留。
- 本地转存：PENDING。GPT内置浏览器JupyterLab正常Download菜单已尝试三次，本地目标文件未发现；本地大小/SHA未核验。
- 训练并发边界：13:37:01 CST GPU单点98%，2441/12288 MiB，64°C，203.03 W；PID 8512、8630、8723、8850、8983仍存活。seed映射、当前比例/轮次和整run退出码未核验。
- 下一步：继续正常浏览器下载；文件落地后核对大小与SHA。不要因组级验收通过而宣称整run退出或本地归档完成。

## 本地转存闭环（2026-10-15 17:51:13 CST）
常规浏览器下载后，本地包大小/SHA与远端sidecar匹配，LOCAL_RECONCILED；详细表见archives/FashionMNIST_local_archive_reconciliation_20261015.md。