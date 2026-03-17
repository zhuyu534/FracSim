# Algorithms

## FracMinHash Sketching

FracMinHash is a variant of the MinHash technique designed for comparing datasets of different sizes. The process consists of the following steps:

1. **k‑mer extraction**: The genome sequence is split into all overlapping substrings of length *k* (k‑mers).
2. **Hashing**: Each k‑mer is hashed to a 64‑bit integer using MurmurHash3 (with a user‑supplied seed).
3. **Sampling**: Only those hashes that are smaller than a threshold `max_hash = floor(2⁶⁴ × scaled)` are retained. This ensures that approximately a fraction `scaled` of all k‑mers are kept, independent of genome length.
4. **Sketch**: The set of retained hashes is the genome sketch.

## Jaccard Index

Given two sketches *A* and *B*, the Jaccard index is defined as:

\[
J(A,B) = \frac{|A \cap B|}{|A \cup B|}
\]

It ranges from 0 (no shared k‑mers) to 1 (identical sets of k‑mers). FracSim uses the sketches to estimate this value directly.

## ANI Estimation

Average Nucleotide Identity (ANI) is approximated from the Jaccard index using the relationship derived in the Mash paper (Ondov et al., 2016):

\[
\text{ANI} \approx 1 - \frac{1}{k} \ln\left(\frac{2J}{1+J}\right)
\]

where *k* is the k‑mer length and *J* is the Jaccard index. This formula assumes that mutations are randomly distributed and that k‑mers are unique. For very low similarities (J < 0.1), the estimate becomes less reliable.

## References

- Ondov, B. D., et al. (2016). Mash: fast genome and metagenome distance estimation using MinHash. *Genome Biology*, 17(1), 132.
- Irber, L. C., et al. (2020). Decentralizing indices for genomic data. *University of California, Davis*.