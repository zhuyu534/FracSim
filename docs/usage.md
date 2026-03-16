```markdown
# Usage

## Command Line Options

| Argument               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `-i, --input`          | Space-separated list of input genome files (FASTA/Q).                      |
| `-l, --list`           | File containing one input file path per line.                              |
| `-k, --kmer-size`      | k-mer length (1–64, default: 31).                                          |
| `-s, --scaled`         | FracMinHash sampling rate (0–1, default: 0.01).                            |
| `--seed`               | Random seed for hashing (default: 42).                                     |
| `--ani`                | Compute ANI in addition to Jaccard index.                                  |
| `--threads`            | Number of threads for parallel processing (default: 1).                    |
| `--format`             | Output format: `table`, `csv`, `json` (default: `table`).                  |
| `-o, --output`         | Output file path (default: stdout).                                        |
| `--min-similarity`     | Only output pairs with Jaccard index ≥ this value (default: 0.0).          |
| `--verbose`            | Print detailed progress information.                                       |
| `--version`            | Show program version and exit.                                             |
| `-h, --help`           | Show this help message and exit.                                           |

## Input Formats

- **FASTA** (`.fasta`, `.fa`, `.fna`, `.ffn`, `.frn`): sequences only.
- **FASTQ** (`.fastq`, `.fq`): sequences and quality scores (quality is ignored for sketching).

## Output Formats

### Table (default)