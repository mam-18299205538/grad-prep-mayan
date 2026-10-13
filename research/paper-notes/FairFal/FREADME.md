> **状态更新（2026-10-13 19:31，）：**本文保留论文精读和方法说明。两组CIFAR10-LT主方法均记录45/45阶段验收；alpha=100最新45% bundle已本地转存，远端/本地SHA一致，内含5份CSV与5个checkpoint的10项SHA逐项匹配。原始远端验收报告的聚合OVERALL=FAIL与逐项通过冲突，原因未确认；5%–40%全部原始文件是否本地归档也未核验。详见[阶段总结](../reproduction/FairFAL/阶段总结_CIFAR10LT_20261012T1630.md)与[45%本地归档核验](../reproduction/FairFAL/archive_cifar10_alpha100_ratio045_20261012/LOCAL_ARCHIVE_RECONCILIATION_20261012T191604.md)。本文不是实时看板。

# FairFAL 论文精读与复现指南

论文：**Federated Active Learning Under Extreme Non-IID and Global Class Imbalance**  
作者：Chen-Chen Zong，Sheng-Jun Huang，Nanjing University of Aeronautics and Astronautics  
会议：CVPR 2026，pp. 24534–24544  
方法：**FairFAL**（class-fair federated active learning）

> 本文档面向第一次接触联邦主动学习的读者，包含论文阅读笔记、源码与数据集入口、官方实现的运行步骤、结果核对方法，以及当前代码中需要注意的复现差异。

## 1. 论文与代码入口

- 论文主页（CVF Open Access）：<https://openaccess.thecvf.com/content/CVPR2026/html/Zong_Federated_Active_Learning_Under_Extreme_Non-IID_and_Global_Class_Imbalance_CVPR_2026_paper.html>
- 论文 PDF：<https://openaccess.thecvf.com/content/CVPR2026/papers/Zong_Federated_Active_Learning_Under_Extreme_Non-IID_and_Global_Class_Imbalance_CVPR_2026_paper.pdf>
- arXiv：<https://arxiv.org/abs/2603.10341>
- 作者官方 FairFAL 源码：<https://github.com/chenchenzong/FairFAL>
- 作者相关 IFAL 源码：<https://github.com/chenchenzong/IFAL>
- LoGo 官方源码（论文对比方法之一）：<https://github.com/raymin0223/LoGo>
- KAFAL 论文与代码线索：<https://openaccess.thecvf.com/content/ICCV2023/papers/Cao_Knowledge-Aware_Federated_Active_Learning_with_Non-IID_Data_ICCV_2023_paper.pdf>

本文档不是作者官方 README 的替代品，而是对论文和当前仓库的中文解释与复现补充。

## 2. 一句话结论

FairFAL 的核心观点是：联邦主动学习中，真正决定最终模型效果的不是“模型看起来多不确定”，而是查询样本是否能在有限标注预算下保持类别覆盖，特别是能否找到少数类样本。于是它根据全局长尾程度和本地-全局分布差异，在全局模型与本地模型之间自适应选择查询器，再用全局特征原型做伪标签分组，并在每一类内部进行“不确定性优先 + k-center 多样性”的两阶段采样。

## 3. 背景与问题定义

### 3.1 三个叠加的困难

普通联邦学习假设每个客户端拥有已标注数据；主动学习则假设有大量未标注池，只为少量样本付出标注成本。联邦主动学习（FAL）把两者结合起来：客户端不上传原始图像，只基于本地未标注池选择值得标注的样本，然后通过联邦训练得到全局模型。

论文关注的是更现实、也更困难的组合：

1. **极端 non-IID**：不同客户端的类别比例差异很大；论文用 Dirichlet 参数 `alpha` 控制，`alpha=0.1` 表示强异质，`alpha=100` 接近同质。
2. **全局类别不平衡**：把所有客户端数据汇总后，类别仍然是长尾分布；论文用全局不平衡比 `rho` 表示，`rho=20` 即头类与尾类约 20:1 的难设置。
3. **每轮标注预算有限**：论文初始随机标注本地 5%，之后每个主动学习周期再标注本地数据的 5%，一直到 45%。

### 3.2 论文真正要回答的问题

每个客户端有两个自然的查询模型：

- **Global model**：服务器聚合后的全局模型；表示更全局，但可能被聚合平滑，丢失本地决策边界细节。
- **Local-only model**：只用当前客户端已标注数据训练的本地模型；更贴近本地分布，但可能严重偏向本地头类。

论文不是简单地问“全局模型好还是本地模型好”，而是问：在不同的 `alpha`、`rho` 和采样策略下，哪个模型能查询到更均衡的类别，尤其是更多尾类？

## 4. 论文的关键观察

作者先在 CIFAR-10 上比较 Global/Local 两种查询器，并分别测试熵不确定性采样和 Coreset 多样性采样。

### Observation 1：不确定性采样通常偏向本地模型

在熵、Margin、Least Confidence 这类不确定性策略中：

- 当全局数据比较均衡或客户端高度异质时，本地模型通常更好；本地决策边界更尖锐，能发现本地有价值的样本。
- 当全局极度长尾、但各客户端近似同质时，全局模型反而更好；因为本地模型也会复制全局长尾偏差，全局模型在聚合后拥有更完整的跨客户端知识。

### Observation 2：查询类别是否均衡比查询分数本身更重要

被查询的数据中，少数类比例越高、整体类别越均衡，最终全局精度通常越高。论文用累计查询比例和最终精度曲线展示了两者的同步变化：少数类采样差距扩大时，模型精度差距也随之扩大。

### Observation 3：Coreset 多样性采样更依赖全局模型

Coreset 主要依赖表征空间的几何结构，而全局模型由所有客户端更新聚合得到，学习到的 embedding 通常更具全局判别性。因此在论文设置下，全局模型在 Coreset 查询中稳定优于本地模型。

### 四种情形的直观决策表

| 全局长尾程度 | 客户端异质程度 | 更可能合适的查询器 | 原因 |
|---|---:|---|---|
| 低 | 高 | Local | 本地边界更有区分度，客户端之间的差异反而有助于全局覆盖 |
| 低 | 低 | Local 或相近 | 全局模型对不确定性没有明显优势 |
| 高 | 高 | 通常 Local | Global 受聚合和长尾共同影响，Local 仍可能提供更尖锐的本地信号 |
| 高 | 低 | Global | 本地模型容易复制头类偏置，全局模型更能利用共享知识 |

上表是论文观察的经验规律，不是对所有任务的理论保证；FairFAL 的意义就在于不预先固定其中一个模型。

## 5. FairFAL 方法详解

### 5.1 总体流程

每一个主动学习周期执行：

1. 读取每个客户端当前的已标注集 `D_L^k` 和未标注池 `D_U^k`。
2. 先用当前全局模型在客户端已标注数据上做一次轻量统计，并训练一个 local-only 模型。
3. 根据全局长尾程度与 local-global 差异，为每个客户端选择 Global 或 Local 查询器。
4. 用全局模型 embedding 计算类别原型，将未标注样本按原型相似度分配到伪类别。
5. 每一类先选高熵候选，再用全局梯度 embedding 做 k-center 贪心去冗余。
6. 客户端得到新标签后，进入下一轮 FedAvg；重复直到标注比例达到 45%。

### 5.2 自适应模型选择

设客户端 `k` 的已标注数据中，第 `c` 类样本数是 `n_{k,c}`。先对每个已出现类别上采样到同样数量，得到平衡子集 `B^k`，避免“某个客户端本身头类多”直接污染全局长尾估计。

用全局模型的预测概率估计全局类别先验：

```text
pi_g^k = average_{x in B^k} f_g(x)
gamma_k = min_c(pi_g^k[c]) / max_c(pi_g^k[c])
gamma_bar = average_k(gamma_k)
```

`gamma_bar` 越小，说明全局越长尾。论文只在第一个主动学习周期上传这个标量并固定下来，以减少通信和潜在隐私泄露。

再用同一个平衡子集分别经过全局模型和 local-only 模型，计算预测先验的归一化差异：

```text
d_k = (1/C) * sum_c |pi_g^k[c] - pi_l^k[c]| /
                   (pi_g^k[c] + pi_l^k[c])
```

`d_k` 越大，表示客户端越偏离全局分布、异质性越强。最后构造模型选择分数：

```text
s_k = 1 - 0.5 * (d_k + gamma_bar)
```

当 `s_k > delta` 时使用 Global，否则使用 Local；论文默认 `delta=0.75`。由于 `gamma_bar` 小（全局严重不平衡）且 `d_k` 小（客户端较同质）时 `s_k` 大，所以自动选择 Global，和 Observation 1 一致。

### 5.3 全局原型伪标签

对客户端已标注样本，用全局模型倒数第二层得到 L2 归一化特征 `z_i`。每一类的原型是：

```text
mu_c = average_{i: y_i=c} z_i
```

对未标注样本 `x`，用全局 embedding 与各类别原型的余弦相似度进行伪标签分配：

```text
y_tilde(x) = argmax_c <z(x), mu_c>
```

这里的伪标签不是为了直接训练模型，而是为了把未标注池拆成若干类别桶，随后在每个类别桶内分配查询预算。这样做的动机是：长尾分类器的 softmax 预测容易把大量样本压到头类，而全局特征空间通常比单纯的分类 logits 更适合做类别覆盖。

### 5.4 两阶段不确定性-多样性采样

设本客户端本轮预算为 `B_k`，各伪类别获得近似均匀的子预算 `b_c^k`。

**阶段一：不确定性候选池。** 在每个类别桶中，用自适应选出的查询模型计算熵：

```text
H(x) = -sum_c p(c|x) log p(c|x)
```

每类保留 `kappa * b_c^k` 个最高熵样本作为候选，论文固定 `kappa=4`。

**阶段二：k-center 去冗余。** 把全局模型的特征和分类预测组合成梯度 embedding，在每个类别候选池中，以已经标注的同类样本作为 anchor，贪心选择覆盖最远区域的 `b_c^k` 个样本。目标是最小化候选池到“已标注 anchor + 新查询样本”的最大最近距离；精确解是 NP-hard，代码采用标准 greedy k-center 的 2-approximation 思路。

因此最终的查询样本同时满足：

- 有较高不确定性，可能改善决策边界；
- 预测类别尽量均衡，保护尾类；
- 在 embedding 空间尽量分散，减少重复图像；
- 使用全局特征保持跨客户端的一致几何空间。

## 6. 实验设置与主要结果

### 6.1 数据集

| 数据集 | 类别数 | 训练/测试规模 | 论文用途 |
|---|---:|---:|---|
| Fashion-MNIST | 10 | 60,000 / 10,000 | 简单灰度自然图像基准 |
| CIFAR-10 | 10 | 50,000 / 10,000 | 标准彩色图像基准 |
| CIFAR-100 | 100 | 50,000 / 10,000 | 更高类别数、更难的细粒度基准 |
| OCTMNIST | 4 | 97,477 / 10,832 | 天然长尾的视网膜 OCT 医学图像 |
| DermaMNIST | 7 | 7,007 / 2,005 | 天然长尾的皮肤镜医学图像 |

官方数据入口：

- Fashion-MNIST：<https://github.com/zalandoresearch/fashion-mnist>
- CIFAR-10/100：<https://www.cs.toronto.edu/~kriz/cifar.html>
- MedMNIST v2：<https://medmnist.com/v2>

代码会通过 `torchvision` 自动下载 Fashion-MNIST/CIFAR，通过 `medmnist` 自动下载 OCTMNIST/DermaMNIST。

### 6.2 训练配置

- 10 个客户端；全部客户端参与（`frac=1.0`）。
- FedAvg；每个通信轮本地训练 5 个 epoch。
- 总计 100 个通信轮；第 75 轮后学习率乘 0.1。
- SGD，初始学习率 0.01，momentum 0.9，weight decay `1e-5`，batch size 64。
- 4 层 CNN；附录另测 MobileNet 和 ResNet-18。
- 5 个随机种子：1–5；表格报告均值。
- 人工构造长尾数据时使用 `rho=20`；代码用 `imb_ratio=0.05` 表示尾类/头类比例 1:20。
- `alpha=0.1` 和 `alpha=100` 分别由代码中的 `--dd_beta 0.1`、`--dd_beta 100` 表示。

### 6.3 主要结果摘录

在 `rho=20`、`alpha=0.1` 下，FairFAL 在 FMNIST/CIFAR-10/CIFAR-100 的 15%、25%、35%、45% 标注比例准确率分别为：

| 数据集 | 15% | 25% | 35% | 45% |
|---|---:|---:|---:|---:|
| FMNIST | 85.21 | 86.46 | 87.18 | 87.37 |
| CIFAR-10 | 52.12 | 56.90 | 59.62 | 60.44 |
| CIFAR-100 | 18.47 | 24.29 | 25.94 | 29.20 |

在更接近同质的 `alpha=100` 下，对应结果为：

| 数据集 | 15% | 25% | 35% | 45% |
|---|---:|---:|---:|---:|
| FMNIST | 85.81 | 87.48 | 88.43 | 88.90 |
| CIFAR-10 | 53.25 | 59.17 | 62.62 | 64.57 |
| CIFAR-100 | 18.89 | 24.45 | 26.47 | 30.02 |

医学数据在 `alpha=0.1` 时的最终轮准确率：OCTMNIST 72.80%，DermaMNIST 73.77%。论文还报告：

- 自适应模型选择、类别级采样、两阶段采样逐步加入后均有收益；
- `kappa=2/3/4/5` 的差异不大，最终选 `kappa=4`；
- `delta` 从 0.65 到 0.85 时性能较稳定，默认 0.75；
- 在 FedProx、SCAFFOLD、5/20 客户端以及 MobileNet/ResNet-18 下仍保持较强表现。

## 7. 官方源码结构

```text
FairFAL/
├── main.py                         # 数据加载、主动学习周期、联邦训练主循环
├── query_strategies/
│   ├── __init__.py                 # 初始随机查询与后续 FairFAL 查询
│   ├── strategy.py                 # 预测、embedding、原型、local-only 训练
│   └── fairfal_sampling.py         # 模型选择、伪标签、候选池、k-center
├── fl_methods/
│   ├── fedavg.py                   # 默认 FedAvg
│   ├── fedprox.py                  # 附录实验
│   └── scaffold.py                 # 附录实验
├── util/
│   ├── args.py                     # 参数和数据集元信息
│   ├── data_simulator.py           # shard/Dirichlet 客户端划分
│   ├── longtail_dataset.py         # FMNIST/CIFAR 长尾构造
│   └── path.py                     # 结果与索引保存路径
└── models/                         # CNN4Conv、MobileNet、ResNet
```

## 8. 从零开始复现

### 8.1 获取源码

```bash
git clone https://github.com/chenchenzong/FairFAL.git
cd FairFAL
```

### 8.2 创建环境

推荐 Python 3.9。作者的 `requirements.txt` 较旧，且把 PyTorch 安装行注释掉了；因此先按本机 CUDA 版本安装 PyTorch，再安装其余依赖。

Linux/macOS：

```bash
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# 选择与你的 CUDA 匹配的 torch/torchvision；CPU 用户可安装官方 CPU wheel
python -m pip install torch torchvision
python -m pip install -r requirements.txt
```

Windows PowerShell：

```powershell
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install torch torchvision
python -m pip install -r requirements.txt
```

如果旧版 `numpy==1.19.5`、`scikit-learn==1.0.1` 在当前 Python/CUDA 环境无法安装，优先使用 Python 3.9；也可以保留代码逻辑，改装与当前 PyTorch 兼容的较新版本。复现论文数字时，应记录 Python、PyTorch、CUDA、GPU 型号和依赖版本。

### 8.3 先做 CPU 冒烟测试

先用极少通信轮验证导入、数据下载、联邦训练和结果保存是否都正常：

```bash
python main.py --gpu -1 --seed 1 --al_method fairfal \
  --model cnn4conv --dataset fmnist_lt --imb_ratio 0.05 \
  --partition dir_balance --dd_beta 0.1 --num_users 2 --frac 1.0 \
  --rounds 2 --local_ep 1 --reset random --query_ratio 0.05 \
  --end_ratio 0.05
```

第一次运行会自动下载数据。若只想测试 CIFAR-10，把 `fmnist_lt` 替换为 `cifar10_lt`；在 Windows 上若遇到 DataLoader 多进程问题，先保持默认单进程设置，不要额外改动。

### 8.4 复现论文主设置

下面是根据当前源码校正过的命令。**注意：不要加作者 README 中的 `--num_classes`，因为当前 `util/args.py` 没有定义该参数；类别数会由数据集名称自动设置。**

#### FMNIST，alpha=0.1

```bash
python main.py --gpu 0 --seed 1 --al_method fairfal \
  --model cnn4conv --dataset fmnist_lt --imb_ratio 0.05 \
  --partition dir_balance --dd_beta 0.1 --num_users 10 --frac 1.0 \
  --rounds 100 --local_ep 5 --reset random --query_ratio 0.05
```

#### CIFAR-10，alpha=0.1

```bash
python main.py --gpu 0 --seed 1 --al_method fairfal \
  --model cnn4conv --dataset cifar10_lt --imb_ratio 0.05 \
  --partition dir_balance --dd_beta 0.1 --num_users 10 --frac 1.0 \
  --rounds 100 --local_ep 5 --reset random --query_ratio 0.05
```

#### CIFAR-100，alpha=0.1

```bash
python main.py --gpu 0 --seed 1 --al_method fairfal \
  --model cnn4conv --dataset cifar100_lt --imb_ratio 0.05 \
  --partition dir_balance --dd_beta 0.1 --num_users 10 --frac 1.0 \
  --rounds 100 --local_ep 5 --reset random --query_ratio 0.05
```

把 `--dd_beta 0.1` 改为 `--dd_beta 100` 即可测试 `alpha=100`。医疗数据不使用人工 `imb_ratio`：

```bash
python main.py --gpu 0 --seed 1 --al_method fairfal \
  --model cnn4conv --dataset octmnist \
  --partition dir_balance --dd_beta 0.1 --num_users 10 --frac 1.0 \
  --rounds 100 --local_ep 5 --reset random --query_ratio 0.05

python main.py --gpu 0 --seed 1 --al_method fairfal \
  --model cnn4conv --dataset dermamnist \
  --partition dir_balance --dd_beta 0.1 --num_users 10 --frac 1.0 \
  --rounds 100 --local_ep 5 --reset random --query_ratio 0.05
```

### 8.5 五个随机种子

论文用 `seed=1,2,3,4,5`。Linux/macOS 可以运行：

```bash
for seed in 1 2 3 4 5; do
  python main.py --gpu 0 --seed $seed --al_method fairfal \
    --model cnn4conv --dataset cifar10_lt --imb_ratio 0.05 \
    --partition dir_balance --dd_beta 0.1 --num_users 10 --frac 1.0 \
    --rounds 100 --local_ep 5 --reset random --query_ratio 0.05
done
```

PowerShell：

```powershell
1..5 | ForEach-Object {
  python main.py --gpu 0 --seed $_ --al_method fairfal `
    --model cnn4conv --dataset cifar10_lt --imb_ratio 0.05 `
    --partition dir_balance --dd_beta 0.1 --num_users 10 --frac 1.0 `
    --rounds 100 --local_ep 5 --reset random --query_ratio 0.05
}
```

### 8.6 查看结果

每个主动学习比例会生成一个结果目录，重点查看：

- `results.csv`：每个通信轮的训练损失、测试损失、测试准确率；
- `last.pt`：当前标注比例训练结束后的全局模型；
- `query_info.txt`：每个客户端查询前后的类别计数、Global/Local 测试准确率；
- `dict_users_train_label_*.pkl`：每个客户端当前的已标注样本索引；
- `clients_data_num.pickle`：Dirichlet 划分后的客户端类别统计。

论文的曲线横轴是已标注数据比例，不能只看最后一个通信轮；应读取每个 label-ratio 目录下 `results.csv` 的最后一行，再对五个 seed 求均值和标准差。

## 9. 复现边界与代码注意事项

1. **官方仓库目前主要提供 FairFAL 主方法。** 当前 `query_strategies/__init__.py` 只注册了 `fairfal`，论文中 Random、Entropy、Margin、LC、Coreset、BADGE、GCNAL、ALFA-Mix、KAFAL、LoGo、IFAL 等对比方法并没有全部集成到这个仓库中。因此可以直接复现 FairFAL 主流程和 FedProx/SCAFFOLD 附录设置，但不能仅靠该仓库一条命令重现论文全部 baseline 表格。
2. **`--num_classes` 参数问题。** 作者 README 的示例命令包含它，但 parser 没有定义；本 README 已删除。不要为了绕过错误去改 `sources/`，应只修改你自己克隆的 FairFAL 工作副本。
3. **论文的 `rho=20` 与代码的 `imb_ratio=0.05` 是倒数关系。** 长尾构造函数按类别索引从头类到尾类使用指数衰减，代码参数 0.05 对应尾/头约 1/20。
4. **医疗数据是天然长尾。** OCTMNIST 和 DermaMNIST 不使用 `imb_ratio`，应直接使用 MedMNIST 官方划分。
5. **计算量很大。** 每个标注比例都要进行 100 个联邦通信轮，且后续每轮查询还要训练 local-only 模型；先跑 CPU 冒烟测试，再上 GPU 和完整五个 seed。
6. **随机性不只来自 seed。** 数据首次下载、长尾抽样、Dirichlet 划分、客户端选择、PyTorch/CUDA 算子都可能造成差异；论文报告均值，不应期待单个 seed 精确等于论文表格。
7. **指标解释。** 代码输出的是整体测试 accuracy；医学数据 label 需要 `squeeze()`，这也是仓库中多处特殊处理的原因。若研究医疗部署，不应只看 accuracy，还应补充 macro-F1、balanced accuracy 和各类召回率。

## 10. 建议的复现顺序

1. 先跑 `fmnist_lt + num_users=2 + rounds=2 + end_ratio=0.05`，确认环境正常。
2. 跑 CIFAR-10、`alpha=0.1`、单 seed 的完整 9 个主动学习周期。
3. 再跑 `alpha=100`，核对全局/本地模型选择比例和最终曲线趋势。
4. 扩展到 FMNIST、CIFAR-100，再跑 OCTMNIST/DermaMNIST。
5. 最后重复 5 个 seed，并统一汇总 `results.csv`。
6. 如需复现论文的 baseline 表格，先以作者的 LoGo/IFAL 仓库为基础移植基线，再保证所有方法使用相同数据划分、初始化、客户端数、通信轮数和标注预算。

## 11. 论文贡献的评价与可继续研究的问题

### 贡献

- 把 FAL 中“Global 还是 Local”从固定选择问题转化为由数据状态驱动的自适应选择问题。
- 把“类别均衡”明确提升为 FAL 查询质量的核心诊断指标，而不只比较 uncertainty score。
- 原型伪标签、类别级预算和 k-center 去冗余形成了清晰的模块化设计，容易移植到 FedProx、SCAFFOLD 或其他查询器。
- 在自然图像、天然医学长尾、不同客户端数、FL 优化器和 backbone 上做了较完整的稳健性验证。

### 局限与可研究方向

- 伪标签只覆盖客户端已出现的类别，真正“客户端完全没有该类”时，FairFAL 无法凭本地原型主动发现该类；跨客户端尾类发现仍依赖全局模型和数据在客户端的存在。
- `gamma_bar` 第一个周期估计后固定，若标注分布迅速变化，后续模型选择可能滞后。
- 论文使用的隐私分析主要是“只上传标量统计量”的工程性设计，还不是带正式差分隐私保证的协议。
- 代码仓库未同时集成全部 baseline、实验配置文件和论文表格自动汇总脚本，严格复现需要额外工程整理。
- 类别配额依赖原型伪标签质量；在新域、标签噪声或极少数标注样本下，可以研究置信度校准、软配额、跨客户端原型聚合和隐私保护原型。

## 12. 引用

```bibtex
@InProceedings{Zong_2026_CVPR,
  author = {Zong, Chen-Chen and Huang, Sheng-Jun},
  title = {Federated Active Learning Under Extreme Non-IID and Global Class Imbalance},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  month = {June},
  year = {2026},
  pages = {24534-24544}
}
```

