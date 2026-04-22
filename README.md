## <img src="https://raw.githubusercontent.com/zhuyu534/FracSim/main/images/logo.png" width="40" height="40" style="vertical-align: text-bottom; margin-right: 8px;"> FracSim:fast bacterial genome similarity estimation using FracMinHash sketching

[![Latest Version](https://img.shields.io/github/v/release/zhuyu534/FracSim?include_prereleases&color=red)](https://github.com/zhuyu534/FracSim/releases)
[![Bioconda](https://img.shields.io/badge/conda-bioconda-brightgreen.svg)](https://anaconda.org/bioconda/fracsim)
[![PyPI version](https://img.shields.io/pypi/v/FracSim?color=0080ff)](https://pypi.org/project/FracSim/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-00BFFF.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey?color=orange)](https://github.com/zhuyu534/FracSim)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdownload-stats-api.vercel.app%2Fapi%2Fapp&query=%24.total_downloads&label=Downloads&color=green)
</div>

**FracSim** is a **fast** and **accurate** tool for estimating **bacterial** genome similarity, based on the **FracMinHash** genome sketching algorithm. It compresses large genomes into compact hash sets to rapidly compute **Jaccard similarity** and **ANI (Average Nucleotide Identity)** between genomes.

Whether for **species identification**, **strain typing**, or **large-scale genome comparison**, FracSim significantly reduces memory usage and computation time while maintaining high accuracy, especially for closely related strains (ANI > 95%).

📚 **Full documentation**: [https://zhuyu534.github.io/FracSim](https://zhuyu534.github.io/FracSim)

---

## ✨ Features

- **Fast**: Uses FracMinHash sketching to dramatically lower memory footprint (≈33 MB per pair) and runtime.
- **Accurate**: Provides Jaccard index and ANI estimates;achieves MAE < 0.25% for ANI > 95%.
- **Fully self‑contained**: No dependency on BioPython, k‑mer counting libraries, or heavy bioinformatics frameworks.
- **Flexible input**: Supports FASTA/FASTQ (plain or gzip/bzip2/xz/zip compressed), single or multiple files, and file lists.
- **Easy to use**: Clean command‑line interface with multi‑processing support and progress indicators.
- **Multiple output formats**: Table, CSV, TSV, JSON; can be saved to file.
- **Open source**: MIT licensed – contributions and usage are welcome.

## 📦 Installation

### Requirements
- Python 3.8 or higher

### Method 1: Install via Conda (Bioconda)

```bash
conda install -c bioconda fracsim
```

### Method 2: Install From PyPI

```bash
pip install FracSim
```

### Method 3: Download binaries (no Python required)

Check out the [Releases Page](https://github.com/zhuyu534/FracSim/releases) for pre-built binaries across all supported platforms.

### Method 4: Install from source 

```bash
git clone https://github.com/zhuyu534/FracSim.git
cd FracSim
pip install -e .
```

## 🚀 Quick Start

### Compare two E. coli genomes:

```bash
fracsim -i ecoli_k12.fasta ecoli_o157.fasta -k 21 -s 100 --ani
```

### Example output (table format):

```text
Genome1       Genome2       Hashes1  Hashes2  SharedHashes  Jaccard    ANI
ecoli_k12     ecoli_o157    12456    11892    11234          0.9023     97.85
```

### For a list of genomes (one per line in genomes.txt):

```bash
fracsim -l genomes.txt -k 21 -s 100 --ani -o results.csv
```

## 📖 Usage & Options

```text
usage: fracsim [-h] (-i INPUT [INPUT ...] | -l LIST) [options]
FracSim -- a FracMinHash-based genome similarity estimator for bacteria
```

### Command Line Options

| Argument               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `-i, --input`          | Space-separated list of input genome files (FASTA/Q).                      |
| `-l, --list`           | File containing one input file path per line.                              |
| `-k, --kmer-size`      | k-mer length (1–64, default: 16).                                          |
| `-s, --scaled`         | FracMinHash sampling rate (integer >= 1, default: 100).                            |
| `--seed`               | Random seed for hashing (default: 42).                                     |
| `-a, --ani`                | Compute ANI in addition to Jaccard index (Percentage).                                  |
| `-t, --threads`            | Number of parallel tasks (default: 1).                    |
| `-f, --format`             | Output format: `table`, `csv`, `json`, `tsv` (default: `table`).                  |
| `-o, --output`         | Output file path.                                        |
| `-m, --min-similarity`     | Minimum similarity threshold (Jaccard index, or ANI if --ani is set),Only output pairs with similarity ≥ this value (default: 0.0).          |
| `-p, --performance`    | Show total time and peak memory usage.   |
| `-V, --verbose`            | Print detailed progress information.                                       |
| `-v, --version`            | Show program version and exit.                                             |
| `-h, --help`           | Show help message.                                           |


### Examples:

```bash
# Basic pairwise comparison with ANI, using 4 threads
fracsim -i genome1.fna genome2.fna -k 21 -s 100 --ani -t 4

# Batch comparison, save as TSV
fracsim -l genome_list.txt -k 21 -s 1000 -o results_output/result.tsv

# Filter high‑similarity pairs only (Jaccard ≥ 0.95)
fracsim -i A.fasta B.fasta -m 95
```

## 💻 Algorithm Overview

FracSim estimates genome similarity using the **FracMinHash** sketching algorithm.

### 1. Sketching (FracMinHash)
- Split each genome into overlapping **k‑mers** (length `k`, default 16).
- Hash each k‑mer with MurmurHash3 (64‑bit, unsigned).
- Keep only hashes smaller than `max_hash = floor((2⁶⁴‑1) // scaled)`.  
  This retains a fixed **fraction** (`scaled`) of all k‑mers, independent of genome size.
- The set of kept hashes is the genome **sketch**.

### 2. Similarity metrics
- **Jaccard index**  
  \( J(A,B) = \frac{|A \cap B|}{|A \cup B|} \), computed directly from the two sketches.
- **ANI (Average Nucleotide Identity)** – estimated from Jaccard using the Mash formula:  
  \[
  ANI \approx 1 + \frac{1}{k} \ln\left(\frac{2J}{1+J}\right)
  \]

#### All components (FASTA/Q parsing, k‑mer extraction, hashing) are implemented from scratch – no external bioinformatics libraries required.
