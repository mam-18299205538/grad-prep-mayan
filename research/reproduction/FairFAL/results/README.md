# FairFAL复现资料索引

本目录整理CIFAR10-LT FairFAL阶段总结和后续研究记录。正式运行证据在fuxian项目；本目录不替代原始CSV、checkpoint、日志和哈希清单。

## 当前总结

[FairFAL CIFAR10-LT阶段总结（截至2026-10-12 16:30）](阶段总结_CIFAR10LT_20261012T1630.md)

该时点完成dd_beta=0.1与100两组、各九比例五seed，共90/360个v2.1阶段单元。alpha=0.1原始结果已本地归档。19:31补记：alpha=100的45%最新bundle已转存并完成本地复核，远端/本地bundle SHA一致，内含5份CSV与5个checkpoint逐项匹配；原始远端验收报告仍含聚合OVERALL=FAIL，详见[归档核验记录](archive_cifar10_alpha100_ratio045_20261012/LOCAL_ARCHIVE_RECONCILIATION_20261012T191604.md)。这不证明5%–40%的原始结果均已转存。

## 资料入口

- 论文精读和方法拆解：../../papers/FREADME.md
- 公式与实现阅读笔记：../../paper-notes/02-xxx.md/联邦主动学习阅读笔记.md
- 后续研究问题：../../ideas/idea-03.md
- v2.1计划：../../../../fuxian/NEXT_EXECUTION_PLAN_FairFAL_20261010_v2_1.md
- alpha=0.1归档：../../../../fuxian/1011/archive_cifar10_alpha0p1_20261011/README.md
- alpha=100日志：../../../../fuxian/10111/ALPHA100_EXECUTION_LOG.md
- alpha=100最新45%本地归档：archive_cifar10_alpha100_ratio045_20261012/README.md

“完成”指配置的五seed、九比例阶段通过验收；“本地归档”还需本地文件及可核验来源。本文是有日期的历史总结，不自动代表其后状态。
