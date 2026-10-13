# FairFAL alpha=100 latest-batch archive update — 2026-10-12 19:31 CST

The locally archived CIFAR10-LT, dd_beta=100, ratio=0.45 bundle matches the remote bundle SHA256. All 10 embedded manifest entries (five CSVs and five checkpoints) match locally. Independent checks found five 101-line CSVs covering rounds 0–99, five non-empty last.pt checkpoints, exit status 0, and no matched training-error signatures.

The original bundled acceptance report contains a conflicting aggregate seeds=1..5=FAIL / OVERALL=FAIL despite its per-seed and file/hash checks showing PASS. The cause is unconfirmed; the source report is preserved unchanged. This archive covers the latest 45% batch only and does not establish that all 5%–40% raw outputs are locally archived. GPU and current process state were not rechecked during this archive operation.

See README.md and LOCAL_ARCHIVE_RECONCILIATION_20261012T191604.md in this folder.