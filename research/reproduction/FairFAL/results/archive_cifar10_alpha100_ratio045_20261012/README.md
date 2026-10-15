# CIFAR10-LT alpha=100 · 45% 原始结果归档

- Run：fairfal_cifar10_lt_rho045_alpha100_full_ca14e07_20261012T152854
- 数据：CIFAR10-LT；dd_beta=100；imb_ratio=0.05；45%；seed 1–5；100 rounds；commit ca14e07。
- 本地bundle：alpha100_ratio045_verified_bundle_20261012T162808.tar.gz（2,217,349 bytes）。
- bundle SHA256：66a5c60e196635611fa278a733309d28d66b34023031230a09527403dfd1b3df（与2026-10-12 19:13:52 CST在Jupyter读取的远端值一致）。
- 解包内容：bundle_contents/，34 files / 2,508,815 bytes。保留原始 run manifest、逐seed命令/日志/CSV/checkpoint/exit status、源验收报告、指标补充和SHA清单。
- 本地远端清单对账：10/10（5 CSV + 5 last.pt），见 LOCAL_SHA256_RECONCILIATION.tsv。
- seed级二次核验及来源差异：见 [LOCAL_ARCHIVE_RECONCILIATION_20261012T191604.md](LOCAL_ARCHIVE_RECONCILIATION_20261012T191604.md)。
- 状态JSON：[ARCHIVE_STATUS.json](ARCHIVE_STATUS.json)。

## 结果

Round 99 acc_test：seed1–5为64.70%、64.34%、64.81%、64.29%、64.51%；均值64.5300%，样本SD0.2244 pp。五份CSV各101物理行（表头+100轮），覆盖Round 0–99；每个checkpoint 473,110 bytes；退出码0；错误扫描0命中。

## 需透明保留的验收文件标志

bundle内原始远端验收报告的seed级各项和10项SHA检查均通过，但聚合项 seeds=1..5=FAIL 导致 OVERALL=FAIL。同一bundle的 run_manifest.txt列出seed 1–5，五个目录和命令与结果也逐一匹配。原验收文件不修改；本地独立内容复核结果与该聚合标志差异并列保存，聚合失败根因未确认。

## 边界

此目录只证明45%最新批次bundle已本地归档，不证明alpha=100的5%–40%全部原始结果也已在此目录。2026-10-12 19:13:52 CST仅核对了z5实例上的bundle及SHA；GPU/当前进程仍使用16:55:32 CST历史快照，未在本次重新核验。