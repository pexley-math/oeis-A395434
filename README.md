# OEIS A395434 -- Minimum polyhex containing all one-sided n-hexes

Solver code, verifiers, DRAT/LRAT certificates, figures, and paper for [OEIS A395434](https://oeis.org/A395434):

> a(n) = minimum number of hexagonal cells in an edge-connected polyhex that contains, under some rotation and translation, every one-sided n-hex.

![Container animation n=1..4 cycling + n=5..7 slideshow](research/container-animation.gif)

*n=1..4 cycle through every one-sided n-hex placed inside the optimal container (red highlight); n=5..7 are shown as a slideshow since the piece counts (33, 147, 620) are too many to cycle.*

## What is a one-sided polyhex?

A *polyhex* is a connected set of unit hexagonal cells on the hexagonal lattice. Two polyhexes are *one-sided equivalent* if one is a rotation of the other; reflections are treated as distinct pieces. The count of one-sided n-hexes is [OEIS A006535](https://oeis.org/A006535): 1, 1, 3, 10, 33, 147, 620, 2821, ...

A polyhex C is a *container* for one-sided n-hexes if every one-sided n-hex can be placed inside C under some rotation and translation, with all cells of the placed piece lying inside C.

## Known Terms

**DRAT/LRAT-certified values:**

| n | a(n) | container box | solver wall (s) | one-sided n-hex count (A006535) |
|---|------|---------------|-----------------|---------------------------------|
| 1 | 1    | 1 x 1         | 0.001           | 1   |
| 2 | 2    | 1 x 2         | 0.001           | 1   |
| 3 | 4    | 2 x 3         | 0.002           | 3   |
| 4 | 7    | 4 x 3         | 0.010           | 10  |
| 5 | 11   | 3 x 6         | 0.597           | 33  |
| 6 | 15   | 6 x 6         | 8.290           | 147 |
| 7 | 21   | 8 x 5         | 1797.2          | 620 |

Each value is certified two ways:

1. An independent pure-Python geometric verifier (`code/verify_method1.py`) re-enumerates the one-sided n-hexes and checks that every piece fits inside the solver's reported container under some rotation and translation.
2. A machine-verified UNSAT proof that no container of size a(n) - 1 exists in the (n+1) x (n+1) axial rectangle: drat-trim `s DERIVATION` for n = 1..6, and cadical `--lrat=true` + lrat-check `c VERIFIED` for n = 7 (the 1.1 GB binary DRAT exceeded drat-trim's practical memory budget; the LRAT path is faster and produces a stronger linear-checkable certificate).

No closed-form, recurrence, or cross-sequence identity matches all seven values within the families tested (polynomial degree at most 3, linear recurrences of order at most 4 with small integer coefficients, integer-floor closed forms, sibling-sequence offsets). Observed growth: a(n) = Theta(n^2), with n^2 / 3 <= a(n) <= 5 n^2 / 8 for n = 1..7 (UNVERIFIED as a general bound).

## Method Summary

The decision problem "does a container of size k exist inside the (n+1) x (n+1) axial rectangle?" is encoded as a Boolean SAT instance with cell variables, piece-placement variables, rotation-aware placement-implies-selection clauses, a CEGAR connectivity loop, and an ITotalizer cardinality encoding. An incremental driver walks k downward until UNSAT at a(n) - 1. At that point cadical emits a DRAT or LRAT proof, which drat-trim or lrat-check machine-verifies.

## File Listing

| Path | Role |
|------|------|
| `code/solve_one-sided-polyhex-container.py` | Main solver (glue over the shared SAT framework). |
| `code/verify_method1.py` | Independent pure-Python geometric verifier. |
| `code/generate-figures.py` | Figure generator (publication + personal-understanding diagrams). |
| `research/solver-results.json` | Proved values with container cells and timings. |
| `research/verify_method1-results.json` | Per-n PASS records from the geometric verifier. |
| `research/drat-certification-summary.json` | Per-n DRAT/LRAT certification verdict. |
| `research/drat/n{N}_k{K}.{cnf,drat,lrat,sidecar.json}` | CNF + proof certificate + SHA-256 sidecar per n. |
| `submission/paper.md` / `paper.pdf` | Paper draft and compiled PDF. |
| `submission/oeis-draft.txt` | OEIS submission text. |
| `submission/oeis-copy-helper.html` | Click-to-copy helper for the OEIS web form. |
| `submission/one-sided-polyhex-container-figures.pdf` | Publication figures. |
| `research/one-sided-polyhex-container-understanding.pdf` | Personal understanding diagram. |

## Reproducing the proof

Compute the full proved range with DRAT emission + verification (~30 minutes for n = 1..7 on consumer hardware):

    python code/solve_one-sided-polyhex-container.py --n 1-7 --per-term-timeout 1800 --emit-drat --check-drat

Re-run the independent geometric verifier:

    python code/verify_method1.py 7

For n = 7, the 1.1 GB DRAT exceeds drat-trim's practical budget. Re-emit in LRAT format and check with lrat-check:

    external-tools/cadical/build/cadical.exe --lrat=true --binary=false research/drat/n7_k20.cnf research/drat/n7_k20.lrat
    external-tools/drat-trim/lrat-check.exe research/drat/n7_k20.cnf research/drat/n7_k20.lrat

Expected: `c VERIFIED` on stdout, ~80 seconds on consumer hardware.

## Cross-references

- [A006535](https://oeis.org/A006535) -- Number of one-sided n-hexes.
- [A000228](https://oeis.org/A000228) -- Number of free n-hexes.
- [A001207](https://oeis.org/A001207) -- Number of fixed n-hexes.
- [A327094](https://oeis.org/A327094) -- Square-grid analog, free polyominoes.
- [A392363](https://oeis.org/A392363) -- Triangular-grid analog, free polyiamonds.
- [A395422](https://oeis.org/A395422) -- Triangular-grid analog, fixed polyiamonds.

## License

CC-BY-4.0. See `LICENSE`.
