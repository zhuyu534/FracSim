# Changelog

All notable changes to FracSim are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added
- (Planned features for next release)

### Changed
- (Changes in existing functionality)

### Fixed
- (Bug fixes)

--- 

## [v1.0.2](https://github.com/zhuyu534/FracSim/releases/tag/v1.0.2) – 2026-04-13

### Added
- **Bioconda release**: FracSim is now available via `conda install -c bioconda fracsim`.
- **GitHub Actions CI/CD**:
  - Automated unit testing (`pytest`) on Python 3.8–3.14 across Linux, macOS, and Windows.
- **Support TSV**: Add TSV output format
- **Performance monitoring**: `-p, --performance` flag to report total time and peak memory usage.

### Changed
- Default `kmer-size` remains `16` (optimal based on benchmarking).

### Fixed
- **Critical:** Fixed signed/unsigned mismatch in MurmurHash3 that caused incorrect sampling (FracMinHash threshold not applied properly).

---


