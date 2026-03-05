# 🧬 FracSim

基于FracMinHash基因组素描算法的细菌基因组相似度估计工具

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 📖 简介

**FracSim** 是一个高效、准确的细菌基因组相似度估计工具，基于 **FracMinHash** 基因组素描算法。它可以将大型基因组压缩为小型哈希集合，从而快速计算基因组间的 Jaccard 相似度和 ANI（平均核苷酸一致性）值。

无论是进行**物种鉴定**、**菌株分型**还是**大规模基因组比较**，FracSim 都能在保持高准确性的同时，显著降低内存占用和计算时间。

## ✨功能特点

- **高效**: 使用FracMinHash素描算法，大幅降低内存占用和计算时间
- **准确**: 提供Jaccard指数和ANI（平均核苷酸一致性）估计
- **灵活**: 支持FASTA/Q格式，可配置k-mer长度和采样率
- **易用**: 简洁的命令行界面，支持多线程并行计算
- **开源**: MIT协议，欢迎贡献和使用

## 📦安装

### 环境要求
- Python 3.8 或更高版本
- pip 包管理工具

### 从源码安装（推荐）

```bash
git clone https://github.com/zhuyu534/FracSim.git
cd FracSim
pip install -e .