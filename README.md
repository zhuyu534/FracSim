## <img src="images/logo.png" width="40" height="40" style="border-radius: 50%; vertical-align: text-bottom; margin-right: 8px;"> FracSim:fast bacterial genome similarity estimation using FracMinHash sketching

[![Latest Version](https://img.shields.io/github/v/release/zhuyu534/FracSim?color=red)](https://github.com/zhuyu534/FracSim/releases)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey?color=orange)](https://github.com/zhuyu534/FracSim)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

FracSim is a **fast** and **accurate** tool for estimating **bacterial** genome similarity, based on the **FracMinHash** genome sketching algorithm. It compresses large genomes into compact hash sets to rapidly compute **Jaccard similarity** and **ANI (Average Nucleotide Identity)** between genomes.

Whether for **species identification**, **strain typing**, or **large-scale genome comparison**, FracSim significantly reduces memory usage and computation time while maintaining high accuracy.

Documents: https://zhuyu534.github.io/FracSim

## ✨ Features

- **Fast**: Uses FracMinHash sketching to dramatically lower memory footprint and runtime.
- **Accurate**: Provides Jaccard index and ANI (Average Nucleotide Identity) estimates.
- **Flexible**: Supports FASTA/Q formats, configurable k‑mer size and sampling rate.
- **Easy to use**: Clean command‑line interface with multi‑threading support.
- **Open source**: MIT licensed – contributions and usage are welcome.

## 📦 Installation

### Requirements
- Python 3.8 or higher
- pip package manager

### Install from source 

```bash
git clone https://github.com/zhuyu534/FracSim.git
cd FracSim
pip install -e .