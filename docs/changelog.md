# Changelog

All notable changes to FracSim are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added
- (Add new features here before the next release)

### Changed
- (Add changes in existing functionality here)

### Fixed
- (Add bug fixes here)

### Deprecated
- (Add soon-to-be removed features here)

### Removed
- (Add removed features here)

### Security
- (Add security fixes here)

## [v1.0.0](https://github.com/zhuyu534/FracSim/releases/tag/v1.0.0) - 2026-03-17

### Added
- **Initial pre-release of FracSim** – a lightweight tool for bacterial genome similarity estimation using FracMinHash sketching.
- **FASTA/FASTQ input support** – accepts plain and compressed files (`.gz`, `.bz2`, `.xz`, `.zip`) with auto‑detection.
- **FracMinHash sketching** – configurable scaled factor (`-s, --scaled`) to control sketch size.
- **Similarity metrics** – computes Jaccard index and estimates Average Nucleotide Identity (ANI) using the Mash distance formula.
- **Canonical k‑mers** – handles reverse complements to avoid double counting (enabled by default).
- **Flexible output formats** – table (console), CSV, and JSON; output can be saved to file (`-o, --output`) with format auto‑detection.
- **Multi‑threading** – parallel k‑mer extraction for long sequences (`--threads`).
- **Cross‑platform binaries** – pre‑built executables for Linux (amd64), Windows (amd64), and macOS (arm64) via GitHub Releases.
- **Command‑line interface** – comprehensive options documented via `--help`.
- **Installation from PyPI** – `pip install FracSim` for users who prefer the Python package.

### Changed
- (None for this initial release)

### Fixed
- (None for this initial release)

---
