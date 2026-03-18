# Usage

## Command Line Options

| Argument               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `-i, --input`          | Space-separated list of input genome files (FASTA/Q).                      |
| `-l, --list`           | File containing one input file path per line.                              |
| `-k, --kmer-size`      | k-mer length (1–64, default: 31).                                          |
| `-s, --scaled`         | FracMinHash sampling rate (0–1, default: 0.01).                            |
| `--seed`               | Random seed for hashing (default: 42).                                     |
| `-a, --ani`                | Compute ANI in addition to Jaccard index.                                  |
| `-t, --threads`            | Number of parallel tasks (default: 1).                    |
| `-f, --format`             | Output format: `table`, `csv`, `json` (default: `table`).                  |
| `-o, --output`         | Output file path (default: stdout).                                        |
| `--min-similarity`     | Only output pairs with Jaccard index ≥ this value (default: 0.0).          |
| `-V, --verbose`            | Print detailed progress information.                                       |
| `-v, --version`            | Show program version and exit.                                             |
| `-h, --help`           | Show this help message and exit.                                           |


## Parameters

### Input Options
| Option | Description |
|--------|-------------|
| `-i, --input` | Space-separated list of input genome files. |
| `-l, --list` | File containing one input file path per line. Alternative to `-i` for handling many files. |


#### Supported file formats

- **FASTA** (`.fasta`, `.fa`, `.fna`, `.ffn`, `.frn`): sequences only.
- **FASTQ** (`.fastq`, `.fq`): sequences and quality scores (quality is ignored for sketching).
- **Compressed files** (`.gz`, `.bz2`, `.xz`, `.zip`): all above formats can be compressed and will be auto-detected and decompressed on the fly.  


### k-mer Settings

| Option | Description |
|--------|-------------|
| `-k, --kmer-size` | k-mer length (1–64, default: 31). Longer k-mers provide higher specificity but require more memory. |
| `-s, --scaled` | FracMinHash sampling rate (0–1, default: 0.01). Controls sketch size: lower values = smaller sketches (faster but less sensitive). |
| `--seed` | Random seed for hashing (default: 42). Change to get different hash values for the same input. |

### Output Control

| Option | Description |
|--------|-------------|
| `-a, --ani` | Compute ANI (Average Nucleotide Identity) in addition to Jaccard index. Adds ANI column to output. |
| `-f, --format` | Output format: `table`, `csv`, `json` (default: `table`). Console always displays formatted results. |
| `-o, --output` | Output file path. Format is auto-detected from extension (`.csv`, `.json`, `.txt`). |
| `--min-similarity` | Filter results: only output pairs with Jaccard index ≥ this value (default: 0.0). Useful for focusing on high-similarity genomes. |

#### Output Formats
FracSim supports multiple output formats to suit different needs:

- **Table**: Human-readable formatted table  
- **CSV**: Comma-separated values, ideal for spreadsheet software or further analysis
- **JSON**: Structured data format, perfect for programmatic processing and integration

### Performance

| Option | Description |
|--------|-------------|
| `-t, --threads` | Number of parallel tasks (sketch generation phase is accelerated using multiprocessing), default 1. |

### Information

| Option | Description |
|--------|-------------|
| `-V, --verbose` | Print detailed progress information, including sketch sizes and processing time. |
| `-v, --version` | Show program version and exit. |
| `-h, --help` | Show this help message and exit. |



## Usage Examples

### Basic pairwise comparison
```bash
fracsim -i genome1.fna genome2.fna -k 31 -s 0.01 --ani 
```

### Batch processing multiple files
```bash
# Using space-separated list
fracsim -i genome1.fna genome2.fna genome3.fna -k 31 -s 0.001
# Using list file
fracsim -l genome_list.txt -k 31 -s 0.001
```

### Controlling output

##### Save results as CSV
```bash
fracsim -i genome1.fna genome2.fna -k 31 -s 0.01 --ani -o results.csv
```
##### Filter high-similarity pairs only
```bash
fracsim -i genome1.fna genome2.fna -k 31 -s 0.01 --min-similarity 0.8
```
##### JSON output with verbose logging
```bash
fracsim -i genome1.fna genome2.fna -k 31 -s 0.01 --format json -o results.json -V
```

### Performance optimization
##### Parallel processing of large genomes
```bash
fracsim -i large_genome.fna reference_genome.fna -k 31 -s 0.01 --threads 8
```

### Working with compressed files
```bash
# Auto-detects and decompresses .gz files
fracsim -i genome1.fna.gz genome2.fna.gz -k 31 -s 0.01 --ani
```