# FashionMNIST-LT 本地归档完整对账

- 核验时间：2026-10-15 18:05:22 中国标准时间
- 覆盖：dd_beta=0.1/100，5%–45%，18个五seed比例组；本地11个包包含90份CSV与90个last.pt。
- 方法：GPT内置浏览器JupyterLab常规下载；本地重算SHA256，核对远端哈希与字节数，并读取tar目录。远端原件保留。
- 结果：11/11大小与SHA匹配；11/11 tar可读；90/90 CSV为epoch 0–99；90/90 checkpoint非空。

| beta | 覆盖比例 | 本地包 | bytes | SHA256 | tar项 | CSV | checkpoint | 远端SHA依据 |
|---|---|---|---:|---|---:|---:|---:|---|
| 0.1 | 5% | `FashionMNIST_beta0p1_ratio005_group_20261015T111526_ca14e07.tar.gz` | 2131976 | `ec7c534d6172aca377758ebbc4b5981f54232a2086dc7f6d8a0a475c6f27d218` | 18 | 5 | 5 | previous remote acceptance/archive record |
| 0.1 | 30% | `FashionMNIST_beta0p1_ratio030_group_20261015T1312_ca14e07.tar.gz` | 2133738 | `081abf9e6881f910ebbce5a7c362b9ebdeb66ed70b3082743d5b270fb5e9b30c` | 12 | 5 | 5 | previous remote acceptance/archive record |
| 0.1 | 35% | `FashionMNIST_beta0p1_ratio035_group_20261015T1312_ca14e07.tar.gz` | 2134588 | `5b17bc9b6939e6d1f98dd3767e93d91a49ad3a64537fb47cb251166ef4bd7c21` | 12 | 5 | 5 | previous remote acceptance/archive record |
| 0.1 | 40% | `FashionMNIST_beta0p1_ratio040_group_20261015T1308_ca14e07.tar.gz` | 2134783 | `3b5e9217861471a31bd35d4247477cc8d2356dbd31c5a24654750369bf615f04` | 12 | 5 | 5 | previous remote acceptance/archive record |
| 0.1 | 45% | `FashionMNIST_beta0p1_ratio045_group_20261015T133802_ca14e07.tar.gz` | 2134436 | `bb06d3cbd3541e210e4113aca0d4a073d5bc2961dc6b087bb6584362cec8ce10` | 12 | 5 | 5 | previous remote acceptance/archive record |
| 0.1 | 10%–25% bundle | `FashionMNIST_beta0p1_ratios010-025_group_20261015T121233_ca14e07.tar.gz` | 8888307 | `0686c07e4dcad51a3c164e88d3d9c9df59fa097eb499b8e7b82dfe1cdd20185e` | 63 | 20 | 20 | previous remote acceptance/archive record |
| 100 | 30% | `FashionMNIST_beta100_ratio030_20261015T160225+0800_ca14e07_group.tar.gz` | 2253390 | `8df0a11ad92c950df30a3d6178a11f6a8975898d730c3f70243678979db35d1e` | 17 | 5 | 5 | previous remote acceptance/archive record |
| 100 | 35% | `FashionMNIST_beta100_ratio035_20261015T160918+0800_ca14e07_group.tar.gz` | 2134956 | `56bac71bc5110efdb54936cee066d4e7d14921c40357ab719140459dc7e17455` | 11 | 5 | 5 | previous remote acceptance/archive record |
| 100 | 40% | `FashionMNIST_beta100_ratio040_20261015T160918+0800_ca14e07_group.tar.gz` | 2134613 | `1a70c611e1d9ebb0a83b3df9eba09ab07ba29b7dba05046c88ee1c3f16a2c5dd` | 11 | 5 | 5 | previous remote acceptance/archive record |
| 100 | 45% | `FashionMNIST_beta100_ratio045_20261015T160918+0800_ca14e07_group.tar.gz` | 2134867 | `c07af4d24693bcd33ca07512120efdeeacea1a722524532dac5d2b073822db7d` | 11 | 5 | 5 | previous remote acceptance/archive record |
| 100 | 5%–25% | `FashionMNIST_beta100_ratios005-025_20261015T145527+0800_ca14e07_group.tar.gz` | 10750496 | `c81ba36f303904126d430ad7826b183a030f006195bfa9a15bdf135ce7497dcf` | 57 | 25 | 25 | previous remote acceptance/archive record |

## 进程状态边界

- beta=100：五seed正式长run在2026-10-15 16:11 CST历史记录自然结束，exit_status均为0；不代表当前GPU读数。
- beta=0.1：18个比例组的结果通过验收且本地包对账通过；整条长run exit_status未核验。
- beta=100 35%–45%独立验收JSON未单独转存；本地验收摘要及包内checksum manifest保留。
