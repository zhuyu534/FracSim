# FracSim

[![Latest Version](https://img.shields.io/github/v/release/zhuyu534/FracSim?include_prereleases&color=red)](https://github.com/zhuyu534/FracSim/releases)
[![Conda](https://img.shields.io/conda/vn/bioconda/fracsim.svg?color=brightgreen)](https://anaconda.org/bioconda/fracsim)
[![PyPI](https://img.shields.io/pypi/v/FracSim?color=0080ff)](https://pypi.org/project/FracSim/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-00BFFF.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey?color=orange)](https://github.com/zhuyu534/FracSim)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FracSim** is a fast, memory-efficient command-line tool for estimating bacterial genome similarity using the **FracMinHash sketching algorithm**. It computes both **Jaccard index** and **Average Nucleotide Identity (ANI)** between genomes, enabling large-scale comparative genomics studies.

---

## ✨ Key Features

- **Fast**: Uses FracMinHash sketching to dramatically lower memory footprint (≈33 MB per pair) and runtime.
- **Accurate**: Provides Jaccard index and ANI estimates;achieves MAE < 0.25% for ANI > 95%.
- **Fully self‑contained**: No dependency on BioPython, k‑mer counting libraries, or heavy bioinformatics frameworks.
- **Flexible input**: Supports FASTA/FASTQ (plain or gzip/bzip2/xz/zip compressed), single or multiple files, and file lists.
- **Easy to use**: Clean command‑line interface with multi‑processing support and progress indicators.
- **Multiple output formats**: Table, CSV, TSV, JSON; can be saved to file.
- **Open source**: MIT licensed – contributions and usage are welcome.hosted on [GitHub](https://github.com/zhuyu534/FracSim).

---

## 🚀 Quick Example

Compare two *E. coli* genomes:

```bash
fracsim -i ecoli_k12.fasta ecoli_o157.fasta -k 21 -s 0.01 --ani
```