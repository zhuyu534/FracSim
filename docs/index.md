# FracSim

[![Conda](https://img.shields.io/conda/vn/conda-forge/FracSim)](https://anaconda.org/conda-forge/FracSim)
[![PyPI](https://img.shields.io/pypi/v/FracSim)](https://pypi.org/project/FracSim/)
[![Python Versions](https://img.shields.io/pypi/pyversions/FracSim)](https://pypi.org/project/FracSim/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FracSim** is a fast, memory-efficient command-line tool for estimating bacterial genome similarity using the **FracMinHash sketching algorithm**. It computes both **Jaccard index** and **Average Nucleotide Identity (ANI)** between genomes, enabling large-scale comparative genomics studies.

---

## ✨ Key Features

- **Fast**: FracMinHash sketching reduces computation time by orders of magnitude compared to alignment-based methods.
- **Accurate**: Provides ANI estimates closely matching gold‑standard values (e.g., from BLAST-based methods).
- **Flexible**: Accepts FASTA/Q input, configurable k‑mer size and sampling rate.
- **Scalable**: Multi‑threaded, can handle hundreds of genomes on a laptop.
- **Open source**: MIT licensed, hosted on [GitHub](https://github.com/zhuyu534/FracSim).

---

## 🚀 Quick Example

Compare two *E. coli* genomes:

```bash
FracSim -i ecoli_k12.fasta ecoli_o157.fasta -k 31 -s 0.01 --ani