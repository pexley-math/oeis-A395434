# OEIS A395434 -- Smallest Connected Polyomino Containing All Fixed n-Ominoes

Solver code and data for [OEIS A395434](https://oeis.org/A395434).

## The Problem

a(n) is the minimum number of unit cells in an edge-connected polyomino C on the square grid such that every fixed n-omino P is a subset of C after some lattice translation. A fixed n-omino is a connected set of n unit cells counted up to translation only; rotations and reflections yield distinct pieces, so the number of fixed n-ominoes is [A001168(n)](https://oeis.org/A001168) (1, 2, 6, 19, 63, 216, 760, 2725, 9910 for n = 1..9). This is the square-grid fixed-piece analog of [A327094](https://oeis.org/A327094) (square grid, free pieces) and the square-grid counterpart of [A395422](https://oeis.org/A395422) (triangular grid, fixed pieces).

## Results

**New proved terms (this work):**

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **a(n)** | **1** | **3** | **5** | **9** | **13** | **18** | **24** | **31** | **39** |
| **Pieces (A001168)** | 1 | 2 | 6 | 19 | 63 | 216 | 760 | 2725 | 9910 |
| **Bounding box** | 1x1 | 2x2 | 3x3 | 4x4 | 5x5 | 6x6 | 7x7 | 8x8 | 9x9 |
| **Main time (s)** | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.1 | 1.4 | 11.1 | ~500 |
| **drat-trim check (s)** | <1 | <1 | <1 | <1 | <1 | <1 | <1 | ~60 | 1273 |

Each value is proved exact via SAT with CEGAR-refined connectivity and top-down ITotalizer descent inside the n x n search rectangle. Every n = 1..9 additionally carries a DRAT UNSAT certificate at k = a(n) - 1 emitted by native CaDiCaL and independently verified by drat-trim, with verdict `s VERIFIED` (REFUTATION) for every n. Every container is cross-checked by a disjoint pure-Python geometric containment verifier.

## Method

SAT solver (PySAT with CaDiCaL/Glucose backends) with counterexample-guided abstraction refinement (CEGAR) for connectivity and top-down incremental descent via an ITotalizer cardinality encoding. DRAT proofs are emitted by a native CaDiCaL 3.0.0 build against the flat CNF (with accumulated CEGAR cuts) and verified externally by drat-trim.

- **SAT encoding:** cell variables x(r, c) with an exact-k cardinality constraint (totalizer), placement variables y(i, t) for each fixed n-omino P_i and each lattice translation t that fits inside the n x n search rectangle, plus piece-coverage and piece-cell implication clauses.
- **Connectivity:** enforced via CEGAR -- each candidate model is BFS-tested under 4-adjacency on the square lattice; disconnected models trigger a disjunctive cut and a re-solve until the returned cell set is a single connected component.
- **DRAT certification:** once a(n) is found (SAT at k and UNSAT at k-1), the lower-bound instance at k = a(n) - 1 is re-emitted as a native-CaDiCaL DRAT proof and checked by drat-trim. drat-trim rebuilds unit propagation from scratch and derives the empty clause, yielding the strongest available verdict (`s VERIFIED` = REFUTATION). SHA-256 anchors for each CNF and DRAT file are stored in `research/drat/n{n}_k{k}.sidecar.json`.
- **D4 symmetry breakers:** the fixed-omino set is closed under rotation and reflection, so D4 symmetry on the container is correctness-preserving and reduces search time without affecting the proved value. The heuristic-ablation matrix in `research/` reproduces every a(n) with each toggle disabled.

## Key Findings

- The first nine values 1, 3, 5, 9, 13, 18, 24, 31, 39 do not appear in any OEIS sequence at first-9-term resolution beyond an incidental match with [A350660](https://oeis.org/A350660) (rounded bubble-sort average comparison count, from Knuth), which arises from an unrelated rounded asymptotic and under the conjecture below diverges from n = 13 onward (A395434(13) = 81 conjecturally, vs A350660(13) = 80).
- **Conjecture (unverified):** a(n) = (n^2 - n + 6)/2 for n >= 4, with a(n) = 2n - 1 for n in {1, 2, 3}. Equivalently a(n) = [A000217](https://oeis.org/A000217)(n - 1) + 3 for n >= 4. Matches all nine proved terms; predicts a(10) = 48.
- The conjectured first differences a(n) - a(n - 1) reduce to (n - 1) for n >= 6, giving the arithmetic progression 5, 6, 7, 8 observed at n = 6, 7, 8, 9.
- **D4-invariant optima.** The optimal container at each n >= 3 is invariant under the full dihedral group D4 of the square lattice (four 90-degree rotations + four reflections). See `submission/fixed-polyomino-container-figures.pdf`.

## Running the Solver

> **Note.** The scripts in `code/` are not runnable as-is from this repository alone. They import from a private shared-library monorepo (`sat_utils`, `polyform_enum`, `figure_gen_utils`) that is not published here, and their `sys.path` insertions assume the monorepo layout. The code is shipped as a reference for the method and for diff-style audit against the proof artefacts in `research/`. The proof itself (SAT witnesses, drat-trim VERIFIED DRAT certificates for n = 1..9) is self-contained in `research/drat/` and can be re-verified with any stock DRAT checker without running the solver.

**Requirements (for reference only):** Python 3.12+, python-sat (PySAT with CaDiCaL 1.5.3 and Glucose 4.2), plus the private shared libraries above. The DRAT certification step additionally needs drat-trim (MSVC build for Windows, standard `make` for Linux) and native cadical 3.0.0.

**Re-verifying the UNSAT proofs from this repo alone:**

```bash
# Example: re-check the n=9 lower bound (a(9)=39 proved by UNSAT at k=38)
gunzip -k research/drat/n9_k38.cnf.gz research/drat/n9_k38.drat.gz
drat-trim research/drat/n9_k38.cnf research/drat/n9_k38.drat
# Expected: "s VERIFIED"
```

**Example solver commands (require the private monorepo):**

```bash
# Main solver -- proves a(n) inside the n x n search rectangle,
# emits DRAT + invokes drat-trim per n.
python code/solve_new-fixed-polyomino-container.py --n 1-9 \
    --per-term-timeout 0 \
    --emit-drat --check-drat --drat-output-dir research/drat

# Independent verifier -- pure-Python geometric containment
python code/verify_method1.py 9
```

## Files

| File | Description |
|------|-------------|
| `code/solve_new-fixed-polyomino-container.py` | SAT solver with CEGAR connectivity, ITotalizer descent, and DRAT emission |
| `code/verify_method1.py` | Independent pure-Python geometric containment verifier |
| `code/generate-figures.py` | Publication figure generator |
| `research/solver-results.json` | Machine-readable results with witnesses and timings |
| `research/solver-run-log.txt` | Solver run log |
| `research/verify_method1-results.json` | Per-term geometric-verifier results |
| `research/verify_method1-run-log.txt` | Geometric-verifier run log |
| `research/drat-certification-summary.json` | Aggregate DRAT verdict table (per-n verdicts, SHA-256 anchors, timings) |
| `research/drat/n{n}_k{k}.cnf.gz` | Gzipped CNF for the lower-bound instance at k = a(n) - 1 |
| `research/drat/n{n}_k{k}.drat.gz` | Gzipped DRAT proof from native CaDiCaL |
| `research/drat/n{n}_k{k}.sidecar.json` | SHA-256 anchors for the CNF and DRAT plus the drat-trim verdict |
| `research/drat/n{n}_witness.json` | Optimal-container witness (cell coordinates) for a(n) |
| `submission/fixed-polyomino-container-figures.pdf` | Publication figures |

## Prior Art and Acknowledgments

A327094 (smallest polyomino containing all free n-ominoes, square grid) was introduced by Peter Kagey in 2019 and is the free-piece analog of this sequence. A395422 (smallest connected polyiamond containing all fixed n-iamonds, triangular grid) is the triangular-lattice counterpart. Thanks to the OEIS community for curation and prior-art cross-references.

## Hardware

AMD64 Zen 2 desktop, 8 cores, 32 GB RAM, Windows 11. drat-trim n = 9 check: 1273 s wall, 566 MB DRAT, 113M resolution steps, 1.25M core lemmas.

## License

[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) -- Peter Exley, 2026.

This work is freely available. If you find it useful, a citation or acknowledgment is appreciated but not required.

## Links

- **OEIS A395434** (this sequence): https://oeis.org/A395434
- **A327094** (square grid, free pieces): https://oeis.org/A327094
- **A395422** (triangular grid, fixed pieces): https://oeis.org/A395422
- **A001168** (number of fixed n-ominoes): https://oeis.org/A001168
- **A000217** (triangular numbers; appearing in the conjecture): https://oeis.org/A000217
