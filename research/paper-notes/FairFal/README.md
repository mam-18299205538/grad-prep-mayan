# 联邦主动学习：论文阅读与复现反思

论文：*Federated Active Learning Under Extreme Non-IID and Global Class Imbalance*  
作者：Chen-Chen Zong、Sheng-Jun Huang；CVPR 2026。  
本页面向研一阶段科研训练。方法详解见[FairFAL指南](../FREADME.md)，阶段结果见[截至16:30总结](../../reproduction/FairFAL/阶段总结_CIFAR10LT_20261012T1630.md)。

## 1. 研究问题与方法理解

论文将联邦学习、主动学习和长尾分布结合，讨论全局模型与本地模型如何用于查询、查询样本是否覆盖少数类，以及如何在有限预算下结合不确定性与多样性。FairFAL的设计包括自适应模型选择、原型引导的类别伪标签、类别内不确定性候选池与gradient k-center采样。

阅读和复现时，我需要把论文观察、方法设计、代码事实和实验假设分开。只看到总准确率不能证明方法内部模块按论文执行，更不能证明某个模块造成结果差异。

## 2. 本阶段范围

截至2026-10-12 19:31，v2.1八组配置中已记录CIFAR10-LT dd_beta=0.1与100两组完成45/45阶段，共90/360个配置×比例×seed阶段单元。alpha=0.1已本地归档；alpha=100最新45% bundle已本地转存，远端/本地bundle SHA及10项内容SHA匹配。原始远端聚合验收标志存在OVERALL=FAIL冲突；5%–40%全部原始文件本地状态未核验。详情见[45%本地归档复核](../../reproduction/FairFAL/archive_cifar10_alpha100_ratio045_20261012/LOCAL_ARCHIVE_RECONCILIATION_20261012T191604.md)。

dd_beta对应论文客户端Dirichlet参数alpha；imb_ratio=0.05对应全局rho=20长尾设置。配置经代码、命令和数据类别计数审计。结果逐阶段检查CSV、checkpoint、退出码、错误扫描与哈希。

## 3. 复现教会我的核验步骤

### 先查变量含义

论文公式、参数解析器、命令行和数据计数应相互印证。CIFAR10-LT类别数从5000到250，尾类/头类为0.05；dd_beta改变客户端划分，而不是全局长尾强度。

### 让统计值能回到原始结果

均值要绑定seed、ratio、run和代码提交。CSV行数、Round范围、checkpoint、退出码和hash回答不同问题，不能互相替代。

### 发现错误后更正并保留审计轨迹

旧alpha=0.1 35%汇总62.824%与canonical CSV冲突，复核后采用59.438%；30% seed1按正式CSV为57.92%。旧值继续作为历史记录保存，不用于当前结论。这让我练习了查来源、重算统计和修订解释。

### 让结论不超过证据

45%时alpha=0.1为60.576%±0.359 pp，alpha=100为64.530%±0.224 pp。3.954个百分点差异是描述性线索；没有配对统计和类别级查询数据时，不写成显著性或公平机制因果结论。

## 4. 下一轮研究问题

在CIFAR10-LT和相同rho=20下，改变客户端异质程度后，五seed学习曲线差异是否伴随类别级查询覆盖变化？alpha=100最新45% bundle的本地哈希对账已完成；下一步对齐两组同seed的Round99与AULC，核查query_info、已标注索引和客户端类别计数，并区分真实标签、伪标签和预测类别统计。缺少证据时标记未核验。新增Random或跨数据集实验按v2.1和最新授权执行，不从本总结推导启动许可。

## 5. 证据入口

- [阶段总结](../../reproduction/FairFAL/阶段总结_CIFAR10LT_20261012T1630.md)
- [alpha=0.1协议审计](../../../../fuxian/1011/archive_cifar10_alpha0p1_20261011/metadata/PROTOCOL_AUDIT.md)
- [alpha=0.1归档对账](../../../../fuxian/1011/archive_cifar10_alpha0p1_20261011/metadata/REMOTE_MANIFEST_RECONCILIATION.tsv)
- [alpha=100执行日志](../../../../fuxian/10111/ALPHA100_EXECUTION_LOG.md)
- [v2.1计划](../../../../fuxian/NEXT_EXECUTION_PLAN_FairFAL_20261010_v2_1.md)
