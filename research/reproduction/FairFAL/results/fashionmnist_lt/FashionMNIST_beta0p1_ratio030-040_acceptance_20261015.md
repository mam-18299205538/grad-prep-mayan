# FashionMNIST-LT beta=0.1：30%–40% 组级验收与转存

记录时间：2026-10-15（Asia/Shanghai）。源代码 commit：ca14e07。验证方式：AutoDL 远端 CPU；五路正式训练继续运行。

## 验收结果

30%、35%、40% 三组均通过：每组 seed1–5 的 results.csv 为表头+100行（Round 0–99），每个 seed 的 last.pt 非空（460,822 bytes），组内结果文件做了至少2秒稳定性核对，当前运行日志错误扫描为0匹配。逐文件 SHA256 已写入对应 checksums 清单。长 run 跨比例运行，比例级 exit_status 不伪造；整体退出码待该 run 自然结束。

## 远端归档与本地对账

| 比例 | 远端验收 | 本地包大小 | 远端/本地 SHA256 | 本地归档 |
|---|---|---:|---|---|
| 10%–25% | 远端历史报告 PASS；本轮重新计算远端包哈希 | 8,888,307 B | 0686c07e4dcad51a3c164e88d3d9c9df59fa097eb499b8e7b82dfe1cdd20185e | archives/FashionMNIST_beta0p1_ratios010-025_group_20261015T121233_ca14e07.tar.gz |
| 30% | 2026-10-15 13:16 CST，5/5 PASS | 2,133,738 B | 081abf9e6881f910ebbce5a7c362b9ebdeb66ed70b3082743d5b270fb5e9b30c | archives/FashionMNIST_beta0p1_ratio030_group_20261015T1312_ca14e07.tar.gz |
| 35% | 2026-10-15 13:16 CST，5/5 PASS | 2,134,588 B | 5b17bc9b6939e6d1f98dd3767e93d91a49ad3a64537fb47cb251166ef4bd7c21 | archives/FashionMNIST_beta0p1_ratio035_group_20261015T1312_ca14e07.tar.gz |
| 40% | 2026-10-15 13:09 CST，5/5 PASS | 2,134,783 B | 3b5e9217861471a31bd35d4247477cc8d2356dbd31c5a24654750369bf615f04 | archives/FashionMNIST_beta0p1_ratio040_group_20261015T1308_ca14e07.tar.gz |

四个组包均通过 GPT 内置浏览器 JupyterLab 的正常 Download 菜单下载；本地 SHA256 与远端一致，远端原件保留。10%–25%包的远端 SHA 于13:17 CST重新计算后与既有记录一致。5%包此前已完成本地SHA对账。

## 当前训练快照

2026-10-15 13:18:30 CST：RTX 3080 Ti GPU 46%，显存2451/12288 MiB，65°C，206.12 W。原有五个训练 PID 2185/2187/2188/2189/2190 均存活；seed1–5最新可读轮次为77/82/85/81/83。日志可见进展，GPU非零。当前比例标记本轮未核验，不能仅由轮次推断45%已完成或组级通过。最后通过的完整比例组是40%。

## 核验未覆盖项与下一步

- 当前五路进程的整 run 退出码：待自然结束。
- 45%：尚未验收；文件稳定后用远端CPU完成同样门槛，训练保持运行，再生成远端归档并按浏览器正常下载到本地核对SHA。
- 不改代码/参数、不重启存活进程、不覆盖原始结果；进程状态或文件状态异常时保留现场并记录。