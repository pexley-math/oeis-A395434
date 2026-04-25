# OEIS A395434 -- Smallest Connected Polyhex Containing All One-Sided n-Hexes

Solver code and data for [OEIS A395434](https://oeis.org/A395434).

![Container animation](research/container-animation.gif)

## The Problem

a(n) is the minimum number of hexagonal cells in an edge-connected polyhex C such that every one-sided n-hex P is a subset of C after some rotation by a multiple of 60 degrees and some translation of the hexagonal lattice. A one-sided n-hex is a connected set of n unit hexagons counted up to rotation only; reflections yield distinct pieces, so the number of one-sided n-hexes is [A006535(n)](https://oeis.org/A006535) (1, 1, 3, 10, 33, 147, 620, 2821, 12942, 60639, ... for n = 1, 2, 3, ...). This is the hexagonal-grid one-sided-piece analog of [A327094](https://oeis.org/A327094) (square grid, free pieces) and [A395422](https://oeis.org/A395422) (triangular grid, fixed pieces).

## Results

**New proved terms (this work):**

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **a(n)** | **1** | **2** | **4** | **7** | **11** | **15** | **21** |
| **Pieces (A006535)** | 1 | 1 | 3 | 10 | 33 | 147 | 620 |
| **Container bbox** | 1x1 | 1x2 | 2x3 | 4x3 | 3x6 | 6x6 | 8x5 |
| **Solver time (s)** | 0.002 | 0.001 | 0.004 | 0.016 | 0.968 | 13.988 | 1797.2 |

Each value is proved by matching SAT/UNSAT certificates (SAT at k = a(n), UNSAT at k = a(n) - 1) inside an (n+1) x (n+1) axial rectangle, with a machine-verified UNSAT proof at the lower bound: drat-trim verdict `s DERIVATION` for n = 1..6, and cadical `--lrat=true` + lrat-check verdict `c VERIFIED` for n = 7 (the 1.1 GB binary DRAT exceeded drat-trim's practical memory budget; the LRAT path is faster and produces a linear-checkable certificate). Every value is additionally cross-checked by an independent pure-Python geometric containment verifier with a disjoint code path from the solver.

### n = 8 disambiguation (2026-04-25)

The 7-term prefix `1, 2, 4, 7, 11, 15, 21` coincides with four unrelated OEIS sequences (A293239, A261878, A261993, A299251), each of which takes the value 28 at the index aligned with A395434(8). To rule out a coincidental duplication, this repository carries:

- **A 26-cell connected polyhex container** that contains all 2,821 one-sided 8-hexes. Bundled at `research/archived-2026-04-23-solver-results.json` (the 2026-04-23 solver placement, recovered from the upstream monorepo's git history).
- **An independent geometric verifier** (`code/confirm_n8_from_archive.py` + `code/verify_method1.py`) that re-enumerates all 2,821 one-sided 8-hexes by pure-Python BFS over hex axial coordinates, cross-checks the count against [A006535](https://oeis.org/A006535)(8) = 2,821, and confirms that every piece fits inside the 26-cell container under at least one of the 6 rotations and some translation. Result: PASS in ~1.2 seconds, sanity-checked against n = 1..7 in the same archive (also PASS, reproducing `1, 2, 4, 7, 11, 15, 21`). Outputs at `research/n8-archive-confirmation-results.json` and `research/n1-7-archive-sanity-results.json`.
- **First-hand b-files** for each matcher (`research/matcher-bfiles/b{293239,261878,261993,299251}.txt`, fetched from oeis.org) and a per-matcher offset audit at `research/matcher-bfiles/AUDIT.md` showing each matcher predicts 28 at the index aligned with A395434(8).

The 26-cell container gives the upper bound `a(8) <= 26`; combined with the matcher predictions of 28, this yields `a(8) <= 26 < 28`, so A395434 differs from each of A293239, A261878, A261993, A299251 at n = 8. Full argument: `research/n8-disambiguation-note.md`. Reproduce with `python code/confirm_n8_from_archive.py` (deterministic, ~1.5 s wall, no SAT solver required).

The matching lower bound (UNSAT at k = 25, which together with the upper bound would prove `a(8) = 26` exactly) is not required for this disambiguation and is deferred.

## Running the Solver

> **Note.** The scripts in `code/` are not runnable as-is from this repository alone. They import from a private shared-library monorepo (`sat_utils`, `polyform_enum`, `figure_gen_utils`) that is not published here, and their `sys.path` insertions assume the monorepo layout. The code is shipped as a reference for the method and for diff-style audit against the proof artefacts in `research/`. The proofs themselves (SAT witnesses plus drat-trim `s DERIVATION` certificates for n = 1..6 and an lrat-check `c VERIFIED` certificate for n = 7) are self-contained in `research/drat/` and can be re-verified with any stock DRAT or LRAT checker without running the solver.

**Requirements (for reference only):** Python 3.12+, python-sat (PySAT with CaDiCaL), plus the private shared libraries above. The DRAT / LRAT pipeline additionally needs drat-trim, native cadical 3.0.0, and lrat-check (all built from upstream sources).

**Re-verifying the UNSAT proofs from this repo alone:**

```bash
# Example: re-check the n = 6 lower bound (a(6) = 15 proved by UNSAT at k = 14)
drat-trim research/drat/n6_k14.cnf research/drat/n6_k14.drat
# Expected: "s DERIVATION"

# n = 7: regenerate LRAT from the CNF (binary DRAT is 1.1 GB, not committed),
# then check with lrat-check (~80 s on consumer hardware).
cadical --lrat=true --binary=false \
    research/drat/n7_k20.cnf research/drat/n7_k20.lrat
lrat-check research/drat/n7_k20.cnf research/drat/n7_k20.lrat
# Expected: "c VERIFIED"
```

See `research/drat/README.md` for the per-n file layout and the n = 7 proof-file exclusion rationale.

**Example solver commands (require the private monorepo):**

```bash
# Main solver -- proves a(n) with DRAT emission and verification
python code/solve_one-sided-polyhex-container.py --n 1-7 \
    --per-term-timeout 1800 --emit-drat --check-drat

# Independent verifier -- pure-Python geometric containment
python code/verify_method1.py 7
```

## Files

| File | Description |
|------|-------------|
| `code/solve_one-sided-polyhex-container.py` | SAT solver with CEGAR connectivity and ITotalizer descent |
| `code/verify_method1.py` | Independent verifier (pure-Python geometric containment) |
| `code/generate-figures.py` | Publication figure generator |
| `research/solver-results.json` | Machine-readable results with witnesses and timings |
| `research/solver-run-log.txt` | Solver run log |
| `research/verify_method1-results.json` | Per-term geometric-verifier results |
| `research/verify_method1-run-log.txt` | Geometric-verifier run log |
| `research/drat-certification-summary.json` | Per-n DRAT / LRAT verdicts with SHA-256 anchors |
| `research/drat/` | CNF (`.cnf`), DRAT proof (`.drat`) for n = 1..6, sidecar (`.sidecar.json`), and optimal-container witness (`_witness.json`) per term. The n = 7 raw proof files are omitted (1.1 GB DRAT, 3.2 GB LRAT) -- see `research/drat/README.md`. |
| `research/container_explainer.py` | Manim scene generating the animation above |
| `research/container-animation.gif` | n = 1..4 piece cycling + n = 5..7 shape slideshow (embedded above) |
| `submission/one-sided-polyhex-container-figures.pdf` | Publication figures |

## Prior Art and Acknowledgments

This is a new sequence -- no prior OEIS entry exists for this problem. The square-grid free-piece analog is [A327094](https://oeis.org/A327094), submitted to OEIS by Peter Kagey (Sep 2019); the underlying Minimum Common Superform question for pentominoes was posed by T. R. Dawson in 1942 (*Fairy Chess Review* Vol. 5 No. 4). The triangular-grid free-piece and fixed-piece analogs are [A392363](https://oeis.org/A392363) and [A395422](https://oeis.org/A395422) respectively; the hexagonal-grid piece-count reference is [A006535](https://oeis.org/A006535) (one-sided), with siblings [A000228](https://oeis.org/A000228) (free) and [A001207](https://oeis.org/A001207) (fixed). Methodologically this work follows the SAT-based computational-combinatorics tradition exemplified by Heule and Kullmann's Boolean Pythagorean triples proof (2016) and by the DRAT / LRAT proof-checking infrastructure developed for SAT Competition instances.

This work was inspired by the [OEIS](https://oeis.org/) and the community of contributors who maintain it.

## Hardware

AMD Ryzen 5 5600 (6-core / 12-thread), 16 GB RAM, Windows 11, single-threaded.

## License

[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) -- Peter Exley, 2026.

This work is freely available. If you find it useful, a citation or acknowledgment is appreciated but not required.

## Links

- **A395434** (this sequence): https://oeis.org/A395434
- **A006535** (one-sided n-hex count, solver input): https://oeis.org/A006535
- **A000228** (free n-hex count): https://oeis.org/A000228
- **A001207** (fixed n-hex count): https://oeis.org/A001207
- **A327094** (square grid, free pieces -- methodology template): https://oeis.org/A327094
- **A392363** (triangular grid, free pieces -- companion): https://oeis.org/A392363
- **A395422** (triangular grid, fixed pieces -- sibling in the container family): https://oeis.org/A395422
