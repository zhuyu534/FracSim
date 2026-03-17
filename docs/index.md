# FracSim

[![Conda](https://img.shields.io/conda/vn/conda-forge/FracSim)](https://anaconda.org/conda-forge/FracSim)
[![PyPI](https://img.shields.io/pypi/v/FracSim?color=0080ff)](https://pypi.org/project/FracSim/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FracSim** is a fast, memory-efficient command-line tool for estimating bacterial genome similarity using the **FracMinHash sketching algorithm**. It computes both **Jaccard index** and **Average Nucleotide Identity (ANI)** between genomes, enabling large-scale comparative genomics studies.

---

## ✨ Key Features

- **Fast**: Uses FracMinHash sketching to dramatically lower memory footprint and runtime.
- **Accurate**: Provides Jaccard index and ANI (Average Nucleotide Identity) estimates.
- **Flexible**: Supports FASTA/Q formats, configurable k‑mer size and sampling rate.
- **Easy to use**: Clean command‑line interface with multi‑threading support.
- **Open source**: MIT licensed – contributions and usage are welcome.hosted on [GitHub](https://github.com/zhuyu534/FracSim).

---

## 🚀 Quick Example

Compare two *E. coli* genomes:

```bash
fracsim -i ecoli_k12.fasta ecoli_o157.fasta -k 31 -s 0.01 --ani
```