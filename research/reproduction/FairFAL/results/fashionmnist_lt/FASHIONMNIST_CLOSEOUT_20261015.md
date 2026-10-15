# FashionMNIST-LT 全量收尾记录

更新时间：2026-10-15 17:53:38 CST

## 总体结论

dd_beta=0.1和100的5%–45%九档共18个组，均有远端五seed组级PASS记录；11个tar.gz包本地覆盖全部比例。六个剩余包已完成内置浏览器转存，字节数、SHA256及tar目录读取均6/6通过。远端原始结果保留，未重跑任何已验收阶段。

归档目录：E:\Tencent Files\github\mayan\fuxian\1015\fashionmnist_lt\archives

## 本轮闭环六包（本地已归档）

| beta | 比例包 | 文件 | 字节 | SHA256 | 状态 |
|---|---|---|---:|---|---|
| 0.1 | 45% | FashionMNIST_beta0p1_ratio045_group_20261015T133802_ca14e07.tar.gz | 2134436 | bb06d3cbd3541e210e4113aca0d4a073d5bc2961dc6b087bb6584362cec8ce10 | LOCAL_RECONCILED |
| 100 | 5%–25% | FashionMNIST_beta100_ratios005-025_20261015T145527+0800_ca14e07_group.tar.gz | 10750496 | c81ba36f303904126d430ad7826b183a030f006195bfa9a15bdf135ce7497dcf | LOCAL_RECONCILED |
| 100 | 30% | FashionMNIST_beta100_ratio030_20261015T160225+0800_ca14e07_group.tar.gz | 2253390 | 8df0a11ad92c950df30a3d6178a11f6a8975898d730c3f70243678979db35d1e | LOCAL_RECONCILED |
| 100 | 35% | FashionMNIST_beta100_ratio035_20261015T160918+0800_ca14e07_group.tar.gz | 2134956 | 56bac71bc5110efdb54936cee066d4e7d14921c40357ab719140459dc7e17455 | LOCAL_RECONCILED |
| 100 | 40% | FashionMNIST_beta100_ratio040_20261015T160918+0800_ca14e07_group.tar.gz | 2134613 | 1a70c611e1d9ebb0a83b3df9eba09ab07ba29b7dba05046c88ee1c3f16a2c5dd | LOCAL_RECONCILED |
| 100 | 45% | FashionMNIST_beta100_ratio045_20261015T160918+0800_ca14e07_group.tar.gz | 2134867 | c07af4d24693bcd33ca07512120efdeeacea1a722524532dac5d2b073822db7d | LOCAL_RECONCILED |

远端SHA依据：beta=0.1/45%、beta=100/5–25%、beta=100/30%使用sidecar；beta=100/35%、40%、45%来自远端Jupyter Terminal sha256sum。

## 进度与核验边界
- 远端比例组验收18/18 PASS，队列0。
- beta100五seed run在16:11 CST历史观测中自然结束，exit_status均为0。当前GPU/进程本轮未读取。
- beta0.1全部比例组产物PASS；整体run exit_status本轮未核验。
- beta100/35–45独立验收JSON未单独转存；本地阶段Markdown保留PASS摘要，tar内含CSV、checkpoint和checksum manifest，不影响本地包SHA核验。
- 当前数据材料已修正此前beta100 SHA抄录错误；执行日志保留历史原值并附更正记录。

细表：archives/FashionMNIST_local_archive_reconciliation_20261015.md  
看板：FashionMNIST_dashboard_current.html/.json  
交接：FASHIONMNIST_HANDOFF.md；过程日志：FASHIONMNIST_EXECUTION_LOG.md

## 17:53 CST 状态更正

六包的本地SHA和字节数已再次实算，并与远端对照值6/6匹配。转存队列为0，远端原包保留。机器可读明细见 `archives/FASHIONMNIST_LOCAL_ARCHIVE_RECONCILIATION_20261015.json`。历史日志中的pending状态是旧检查点，不代表当前状态。


## 复现阶段报告与 CSV 汇总｜2026-10-15 18:01:50 CST

- 已按附件阶段结果 DOCX 的结构完成全量阶段报告：`FashionMNIST_LT_reproduction_stage_report_v1.0_20261015T1805.docx`。
- 从本地11个tar.gz直接汇总并检查：90/90 CSV 各有100条记录且epoch=0–99；90/90 last.pt非空；所有11包实算SHA与远端对账记录匹配。
- 指标口径：每组5个seed的epoch 99 `acc_test`，报告内给出seed向量、均值、样本标准差和图；可机器读取汇总为`FashionMNIST_epoch99_summary_v1.0_20261015.csv`。
- 范围结论：beta=0.1/100各5%–45%共18个组级远端验收PASS，11个本地包覆盖完整结果；beta=100整run五seed exit_status=0（历史记录），beta=0.1整run退出码未核验，因此只确认阶段结果与本地归档闭环。


### 2026-10-15 18:04:46 CST｜FashionMNIST 双 beta 阶段闭环报告
- 归档完整清单已扩展为11包；本地逐包重算SHA/大小与远端记录相符，tar目录可读。
- 全量索引覆盖18个五seed比例组：90份CSV均为epoch 0–99，90个last.pt非空。
- 阶段报告：`FashionMNIST_LT_reproduction_stage_report_v1.0_20261015T1805.docx`；配套图和epoch99统计CSV已链接到current看板。
- beta=100长run五个exit_status=0（16:11 CST历史记录）；beta=0.1整体exit_status未核验。GPU没有在本次本地文档/归档核验中采样。


## 闭环终态更新｜2026-10-15 18:05:41 CST

- 当前权威本地归档清单扩展为11个包，覆盖beta=0.1/100共18个五seed组；11/11包字节数与远端记录一致、SHA256一致、tar目录可读。包内90份CSV均为100轮epoch 0–99，90个last.pt非空。
- 阶段报告：`FashionMNIST_LT_reproduction_stage_report_v1.0_20261015T1805.docx`；图：`FashionMNIST_LT_epoch99_accuracy_by_label_ratio.png`；18组epoch99汇总：`FashionMNIST_epoch99_summary_v1.0_20261015.csv`。
- beta=100正式长run五seed exit_status=0（2026-10-15 16:11 CST历史证据）；beta=0.1整体run exit_status未核验。两种设置的阶段结果与本地数据包闭环不受该边界影响。
- 本次未重新访问AutoDL或采样GPU；current HTML/JSON刷新的是报告与本地归档状态，GPU数据仍标原观测时间。
