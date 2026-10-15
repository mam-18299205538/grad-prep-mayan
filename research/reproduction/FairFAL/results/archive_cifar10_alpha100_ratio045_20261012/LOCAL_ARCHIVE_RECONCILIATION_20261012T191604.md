# CIFAR10-LT alpha=100 45% 本地归档与逐文件复核

- 核验时间：2026-10-12 19:16:04（Asia/Shanghai）
- 远端 Jupyter：AutoDL 实例 z5ldwxgsn2-aad514f7；终端主机标识与该实例名一致。此处仅用于归档包读取/哈希，不代表该实例执行了原训练或完成了新的 GPU 状态核验。
- 远端 bundle：/root/autodl-tmp/results/fairfal_cifar10_lt_rho045_alpha100_full_ca14e07_20261012T152854/alpha100_ratio045_verified_bundle_20261012T162808.tar.gz
- 下载文件时间：2026-10-12 19:04:50 CST；大小：2217349 bytes。
- 远端 bundle SHA256（Jupyter，2026-10-12 19:13:52 CST）：66a5c60e196635611fa278a733309d28d66b34023031230a09527403dfd1b3df
- 本地 bundle：E:\Tencent Files\github\mayan\fuxian\10111\archive_cifar10_alpha100_ratio045_20261012\alpha100_ratio045_verified_bundle_20261012T162808.tar.gz
- 本地 SHA256：66A5C60E196635611FA278A733309D28D66B34023031230A09527403DFD1B3DF；与远端逐字节匹配：True
- 解包：34 个文件，2508815 bytes；tar 成员均为相对路径，未发现路径穿越项。
- 内嵌远端 5 CSV + 5 checkpoint manifest：本地逐文件 SHA256 匹配 10/10 项。明细见 LOCAL_SHA256_RECONCILIATION.tsv。
- run_manifest.txt：run=fairfal_cifar10_lt_rho045_alpha100_full_ca14e07_20261012T152854；ratio=0.45；dd_beta=100；seeds=1,2,3,4,5；commit=ca14e07。

## seed 级本地复核

| Seed | 配置 | CSV物理行 | Round | last.pt | exit | 错误扫描命中 | Round 99 acc_test |
|---:|---|---:|---|---:|---|---:|---:|
| 1 | 通过 | 101 | 0–99通过 | 473110 B | exit_status=0 | 0 | 64.70% |
| 2 | 通过 | 101 | 0–99通过 | 473110 B | exit_status=0 | 0 | 64.34% |
| 3 | 通过 | 101 | 0–99通过 | 473110 B | exit_status=0 | 0 | 64.81% |
| 4 | 通过 | 101 | 0–99通过 | 473110 B | exit_status=0 | 0 | 64.29% |
| 5 | 通过 | 101 | 0–99通过 | 473110 B | exit_status=0 | 0 | 64.51% |
| **均值 ± 样本SD** | | | | | | | **64.5300% ± 0.2244 pp** |

本地复核确认五个 command.sh 分别对应 seed1–5，并与 CIFAR10-LT、dd_beta=100、imb_ratio=0.05、100 rounds、resume_ratio=end_ratio=0.45 一致；CSV各101物理行（表头+100条记录），epoch覆盖0–99；checkpoint各473110 bytes；退出码均为0；训练日志对 Traceback/CUDA OOM/RuntimeError/Exception 扫描均为0命中。

## 需保留的来源报告差异

bundle 内原始 acceptance_ratio045_20261012T161836.txt 的逐 seed 文件检查、配置项和 SHA256_10_files 均标记通过，但同一文件另有 seeds=1..5=FAIL 与 OVERALL=FAIL。相同 bundle 的 run_manifest.txt 明确列出 seeds=1,2,3,4,5，且本地直接核对五个 seed 目录、逐 seed 命令、结果和10项远端manifest SHA均匹配。后续 final_metrics_ratio045_20261012T162808.txt记录了Round99指标。本地独立复核通过所列数据完整性门槛；原始远端验收报告保持原样，聚合 seeds 标志为何失败尚未证实，故在记录中显式保留，不覆盖成全绿来源报告。

## 状态边界

本次完成的是45%最新批次 bundle 的本地转存与逐文件核对；不能据此声称 alpha=100 九个比例的所有原始CSV/checkpoint都已经转存。GPU/进程最近一次历史核验仍是2026-10-12 16:55:32 CST（当时记录实例 kw79e2gzyr-bbdf8b83、CUDA设备不可见）；本次只读归档操作连接到 z5ldwxgsn2-aad514f7，没有重新核验GPU、进程或当前实验状态。