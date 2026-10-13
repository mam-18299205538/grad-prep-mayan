# 科研训练与论文复现

> 本目录整理论文阅读、方法理解和科研反思。FairFAL的实验数据与执行证据主要保存在同级fuxian项目；本目录的总结链接回原始记录。总览入口见 [work README](../README.md)。

## 当前科研主线：FairFAL

事实截止时间：**2026-10-12 19:31（Asia/Shanghai）**。

| 设置 | 阶段进度 | 证据状态 | 45% Round99 |
|---|---:|---|---:|
| CIFAR10-LT，dd_beta=0.1 | 9比例×5seed，45/45 | CSV/checkpoint已本地归档；哈希对账80/80 MATCH | 60.576% ± 0.359 pp |
| CIFAR10-LT，dd_beta=100 | 9比例×5seed，45/45 | 45%最新批次已本地归档；bundle哈希匹配，内含10/10 CSV/checkpoint逐文件匹配；原始聚合验收标志冲突已披露 | 64.530% ± 0.224 pp |

v2.1规划八组配置；截至该时点完成2/8组、10/40条完整seed曲线、90/360个配置×比例×seed阶段单元。这不代表论文全部基线或消融已完成。45%归档的边界、逐seed复核及来源验收冲突见[本地归档记录](reproduction/FairFAL/archive_cifar10_alpha100_ratio045_20261012/LOCAL_ARCHIVE_RECONCILIATION_20261012T191604.md)和[阶段总结补记](reproduction/FairFAL/阶段总结_CIFAR10LT_20261012T1630.md)。

## 复现过程中的能力训练

练习将论文主张转成可核验问题：区分客户端异质参数和全局长尾参数；映射论文公式、公开代码和运行参数；核对数据计数；按seed和阶段追溯CSV、checkpoint、退出码与哈希；汇总冲突时回到canonical结果更正；说明结论边界，提出有证据需求的下一步。

- [FairFAL论文精读与复现指南](papers/FREADME.md)
- [联邦主动学习详细阅读笔记](paper-notes/02-xxx.md/联邦主动学习阅读笔记.md)
- [阶段总结与证据索引](reproduction/FairFAL/阶段总结_CIFAR10LT_20261012T1630.md)
- [研究想法：客户端异质性与类别级查询证据](ideas/idea-03.md)

## 其他论文材料

多模态乘法计算论文及阅读笔记保留在papers/和paper-notes/多模态乘法计算/。旧版FairFAL导读保留作方法背景；其进度文字由带日期的阶段总结更新。避免把不同时间或不同run的结果合并。

## 目录导航

- paper-notes/：论文精读和方法推导。
- papers/：论文PDF与方法指南。
- reproduction/：阶段总结和复现记录。
- ideas/：由论文和当前结果启发的可检验问题。
