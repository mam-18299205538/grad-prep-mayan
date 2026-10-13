# FairFAL源码与复现记录

此目录保留FairFAL源码快照，源码目录为FairFAL-main/。正式实验状态不从快照README推断；CIFAR10-LT训练与验收证据位于fuxian项目的专属日志和结果目录。

- [截至2026-10-12 16:30的阶段总结](../FairFAL/阶段总结_CIFAR10LT_20261012T1630.md)
- [v2.1计划](../../../../fuxian/NEXT_EXECUTION_PLAN_FairFAL_20261010_v2_1.md)
- [alpha=0.1归档](../../../../fuxian/1011/archive_cifar10_alpha0p1_20261011/README.md)
- [alpha=100执行日志](../../../../fuxian/10111/ALPHA100_EXECUTION_LOG.md)

该时点dd_beta=0.1与100两组CIFAR10-LT各完成五seed、九比例的FairFAL主方法阶段。alpha=0.1最新结果已本地归档；截至2026-10-12 19:31，alpha=100的45%最新bundle已本地转存，bundle及内含10项SHA对账通过，逐seed数据门槛通过。原始验收报告的聚合OVERALL=FAIL与逐项PASS冲突，根因未确认；5%–40%原始结果是否全部转存仍未核验。旧alpha=100 seed2–5结果单独保留，不拼入当前组。本文不代表论文全部基线、消融或数据集均已完成。
