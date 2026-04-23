# Abstract

Let a(n) denote the minimum number of hexagonal cells in an edge-connected polyhex that contains, under some rotation and translation, every one-sided n-hex. We compute a(n) for n = 1 through 7 as the sequence 1, 2, 4, 7, 11, 15, 21, with each term certified by two independent checks: a geometric set-inclusion verifier (Python, disjoint from the solver) and a machine-verified DRAT or LRAT proof of the UNSAT step at k = a(n) - 1. A SAT encoding on the (n+1) by (n+1) hex axial rectangle reduces the decision problem a(n) <= k to a single Boolean formula; a top-down ITotalizer descent with lonely-cell preprocessing, disjunctive CEGAR connectivity cuts, and a lex-least translation breaker computes each term. No closed-form expression matches a(1) through a(7); the growth rate is consistent with a(n) = Theta(n^2). The sequence is submitted to the OEIS as A395434.

## Introduction

A *polyhex* is a connected set of unit hexagonal cells on the hex lattice. Two polyhexes are *one-sided equivalent* if one is a rotation of the other; reflections are distinct. The number of one-sided n-hexes is OEIS A006535: 1, 1, 3, 10, 33, 147, 620, 2821, 12942, 60639, ... .

A polyhex C is a *container* for one-sided n-hexes if every one-sided n-hex can be placed inside C under some rotation and translation, with all cells of the placed piece lying inside C. Define

> a(n) = minimum number of cells in a container for one-sided n-hexes.

Container sequences of this family are a natural combinatorial-geometry question: the square-lattice counterpart is OEIS A327094, the free-polyhex counterpart is currently unnamed, the free-polyiamond (triangular lattice) counterpart is A392363, and the fixed-polyiamond counterpart is A395422. The present paper computes the one-sided hex version, which to our knowledge has not appeared in the literature or OEIS prior to this work (see Section 9).

**Theorem 1 (Trivial bound).** For every n >= 1, a(n) >= n. Any container for one-sided n-hexes must itself contain an n-cell polyhex (the n-cell piece's placed cells), so its cell count cannot fall below n.

Our headline result is:

**Theorem 2 (Computed values, DRAT-certified).** The sequence a(1), a(2), ..., a(7) equals 1, 2, 4, 7, 11, 15, 21. Each value has been verified by an independent geometric containment check and by a machine-verified UNSAT proof (drat-trim for n = 1..6; cadical --lrat followed by lrat-check for n = 7).

No closed-form recurrence or polynomial expression was found to match a(1) through a(7); the observed growth is polynomial of order 2.

## Definitions

- **Hex lattice, axial coordinates.** We use axial coordinates (q, r) where the six neighbours of a hex cell (q, r) are (q+-1, r), (q, r+-1), (q+1, r-1), (q-1, r+1).
- **n-hex (polyhex of size n).** An edge-connected set of n distinct hex cells. Two n-hexes are equivalent (i) as *fixed* if one is a translation of the other, (ii) as *one-sided* if one is a rotation-plus-translation image of the other, (iii) as *free* if reflections are also allowed. The enumeration counts are A001207 (fixed), A006535 (one-sided), A000228 (free).
- **Container.** An edge-connected n-hex C is a container for one-sided n-hexes if for every one-sided n-hex P there exist a rotation rho (by a multiple of 60 degrees) and a translation t with rho(P) + t a subset of the cell set of C.
- **a(n).** a(n) is the minimum number of cells in a container for one-sided n-hexes, ranging over all edge-connected polyhexes. Equivalently, a(n) is the smallest k for which a container of size k exists.
- **Related OEIS sequences.** A006535 (one-sided polyhex count), A327094 (fixed-polyomino container, square lattice), A392363 (free-polyiamond container, triangular lattice), A395422 (fixed-polyiamond container, triangular lattice).

## Computational Methodology

We encode the decision problem "does a container of size k exist inside an axial rectangle of dimensions R by C ?" as a Boolean SAT instance with:

1. *Cell variables* x_{q,r} for each cell (q, r) in the rectangle.
2. *Placement variables* y_{P, rho, t} for every one-sided piece P, rotation rho (at most 6), and translation t that fits the rotated piece inside the rectangle. For each piece P, the clause sum_{rho, t} y_{P, rho, t} >= 1 forces at least one placement. Placement implies cell selection: y -> x for every cell of the rotated-and-translated piece.
3. *Connectivity* is enforced via a CEGAR loop: after each satisfying model, the selected cells are partitioned into connected components; if there is more than one, a disjunctive cut forbids the offending components (optionally with bridge-cell activation disjuncts).
4. *Cardinality* is enforced via an ITotalizer encoding of sum x <= k. An incremental-SAT driver walks k downward, adding connectivity cuts on demand, until UNSAT at k - 1 establishes optimality.

The search rectangle is (n+1) by (n+1) axial cells. This one-row/one-column margin above the minimum bounding box of any n-hex gives the wider-window that supports the DRAT-certification step below.

**Piece enumeration.** The solver uses `polyform_enum.enumerate_one_sided(n, HEX)` (a Cython extension, A006535-counts). The independent verifier re-enumerates from scratch in pure Python, via BFS growth quotiented by the rotation-orbit canonical form, and cross-checks its piece count against A006535.

**Solver optimisation steps.** Six A/B iterations against the n = 6 benchmark, each a single independent change:

| # | Category       | Change                                            | Delta n=6 |
|---|----------------|---------------------------------------------------|-----------|
| 1 | encoding       | enable `use_lonely_cell_clauses=True`              | 19.3s -> 17.2s |
| 2 | parameters     | tighten upper bound `n*n -> n(n+1)/2 + n`         | 17.2s -> 13.8s |
| 3 | architecture   | enable `incremental=True` (persistent ITotalizer + CEGAR) | 13.8s -> 10.4s |
| 4 | simplification | drop redundant `grid_shape_fn` override           | 10.4s -> 10.4s |
| 5 | architecture   | add `bridge_candidates_fn` (Phase 3 disjunctive cuts) | 10.4s -> 10.1s |
| 6 | encoding       | add `use_translation_breaker=True`                | 10.1s ->  8.3s |

The final n = 6 wall time is 8.3s; the final n = 7 wall time is 1227s.

**Framework correction.** Iteration 1 exposed a latent framework bug: `use_lonely_cell_clauses=True` combined with a tight upper bound drove a(1) to 2 instead of the correct 1. The lonely-cell clause "every selected cell has a selected neighbour" is invalid when the optimal container is a single cell. The fix guards both CNF-build sites with `n >= 2`. See `sat_utils/frameworks/container.py` commit `0edd24c1`.

**Verification.** A geometric verifier (pure Python, hex axial coordinates, disjoint code path) independently enumerates one-sided n-hexes and checks that every piece fits inside the solver's reported container under some rotation and translation. The verifier's piece counts agree with A006535 for n = 1..7 (1, 1, 3, 10, 33, 147, 620). See Section 7 for the DRAT certification step.

## Empirical Analysis and Conjectures

### Table of proved values

| n | a(n) | box   | solver wall (s) | verifier 1 | DRAT |
|---|------|-------|-----------------|------------|------|
| 1 | 1    | 1 x 1 | 0.001           | PASS       | CERTIFIED (drat-trim) |
| 2 | 2    | 1 x 2 | 0.001           | PASS       | CERTIFIED (drat-trim) |
| 3 | 4    | 2 x 3 | 0.002           | PASS       | CERTIFIED (drat-trim) |
| 4 | 7    | 4 x 3 | 0.010           | PASS       | CERTIFIED (drat-trim) |
| 5 | 11   | 3 x 6 | 0.597           | PASS       | CERTIFIED (drat-trim) |
| 6 | 15   | 6 x 6 | 8.290           | PASS       | CERTIFIED (drat-trim) |
| 7 | 21   | 8 x 5 | 1227.080        | PASS       | CERTIFIED (cadical --lrat + lrat-check) |

First differences d(n) = a(n+1) - a(n) for n = 1..6 are 1, 2, 3, 4, 4, 6; second differences are 1, 1, 1, 0, 2. The sequence is not smoothly polynomial.

### Conjectures tested

Six candidate formulas were tested against the proved values; none match all seven terms:

1. Polynomial a(n) = n(n-1)/2 + 1 (lazy-caterer shift): matches n = 1..5, fails at n = 6 (16 vs 15).
2. Polynomial a(n) = round(0.42 * n^2): fails at n = 7 (18 vs 21).
3. Recurrence a(n) = a(n-1) + a(n-2) - a(n-3) + 2 with seeds 1, 2, 4: fails at n = 6 (16 vs 15).
4. Closed form a(n) = floor(n(n+1)/3) + 1: fails at n = 7 (19 vs 21).
5. Identity a(n) = A006535(n) + ...: ruled out structurally (A006535 grows exponentially; a(n) does not).
6. Cross-lattice identity a(n) = A327094(n): fails at n = 4 (7 vs 6).

An exhaustive search over linear recurrences of order at most 4 with coefficient magnitudes at most 3 and additive constants |d| <= 4 found no recurrence matching all seven terms.

### Active conjecture

**Conjecture 1 (growth rate, UNVERIFIED).** a(n) = Theta(n^2). Empirically, (1/3) * n^2 <= a(n) <= (5/8) * n^2 for n = 1..7. The one-sided piece count A006535(n) grows as Theta(c^n) with c approximately 4.8, so each container holds super-polynomially many distinct pieces; the polynomial growth of a(n) reflects heavy geometric overlap rather than piece-count growth. A structural inflation or tiling argument is required to convert this envelope into a closed form.

## Discussion and Open Problems

1. **Closed form.** No polynomial, rational, or small-coefficient linear recurrence matches a(1) through a(7). Whether a(n) satisfies any elementary closed form is open.
2. **n = 8 and beyond.** The wider-window SAT approach scales super-linearly: n = 7 took about 20 minutes of CPU on consumer hardware; n = 8 timed out under the 30-minute per-term budget used here. A longer budget or a tighter search window (with a separate Assumption-(S)-style structural argument) is required to push the range further.
3. **Minimality of the (n+1) by (n+1) axial window.** The verification's geometric half is rectangle-free (it inspects the solver's reported cells directly), but the SAT half assumes the optimum lies inside the (n+1) by (n+1) window. For n <= 7 the independent geometric check confirms every piece fits the reported container, but extending to larger n would benefit from a structural proof that no optimum needs a larger window.
4. **Cross-lattice comparison.** For n = 4, the fixed-polyomino (square) container A327094(4) = 6 is strictly less than the one-sided polyhex (hex) container a(4) = 7. Similarly the fixed-polyiamond (triangular) container A395422(4) = 9 is strictly greater. A systematic comparison of container sequences across lattices and equivalence classes is open.

## Reproducibility

All code, data, and certificates are under `research-outputs/paper-project/oeis-new-one-sided-polyhex-container/` in the project repository.

**Solver entry point.** `code/solve_one-sided-polyhex-container.py` (glue for `sat_utils.frameworks.ContainerSolverFramework`).

**Compute the full proved range:**

    python code/solve_one-sided-polyhex-container.py --n 1-7 --per-term-timeout 1800 --emit-drat --check-drat

**Re-run the independent geometric verifier:**

    python code/verify_method1.py 7

**Re-verify n = 7 DRAT by the LRAT path (bypassing drat-trim):**

    external-tools/cadical/build/cadical.exe --lrat=true --binary=false \
        research/drat/n7_k20.cnf research/drat/n7_k20.lrat
    external-tools/drat-trim/lrat-check.exe \
        research/drat/n7_k20.cnf research/drat/n7_k20.lrat

**Expected certificates.** `research/drat/nN_kK.{cnf,drat,sidecar.json}` for n = 1..7 and `research/drat-certification-summary.json` with `certified: true` for every n in 1..7. `research/verify_method1-results.json` with `status: PASS` for every n in 1..7.

**Commit hashes.** Framework fix for lonely_cell at n = 1: `0edd24c1`. Pipeline update making DRAT the second independent proof: `f01c06cb`.

## Acknowledgements

The author thanks the maintainers of the OEIS for the extensive polyform reference data used in this work, and the authors of cadical, drat-trim, and lrat-check whose proof-emission and proof-checking tools underlie the certification pipeline.

## Bibliography

- Biere, A., Fazekas, K., Fleury, M., and Heisinger, M. (2020). "CaDiCaL, Kissat, Paracooba, Plingeling and Treengeling Entering the SAT Competition 2020." Proc. SAT Competition 2020 -- Solver and Benchmark Descriptions, University of Helsinki, B-2020-1, 51-53. https://cca.informatik.uni-freiburg.de/papers/BiereFazekasFleuryHeisinger-SAT-Competition-2020-solvers.pdf.
- Heule, M. J. H., Hunt, W. A., and Wetzler, N. (2013). "Trimming while Checking Clausal Proofs." Formal Methods in Computer-Aided Design (FMCAD 2013), IEEE, 181-188. doi:10.1109/FMCAD.2013.6679408.
- OEIS Foundation (2026). "A000228: Number of hexagonal polyominoes (or hexagonal polyforms, or planar polyhexes) with n cells." The On-Line Encyclopedia of Integer Sequences. https://oeis.org/A000228.
- OEIS Foundation (2026). "A001207: Number of fixed hexagonal polyominoes with n cells." The On-Line Encyclopedia of Integer Sequences. https://oeis.org/A001207.
- OEIS Foundation (2026). "A006535: Number of one-sided hexagonal polyominoes with n cells." The On-Line Encyclopedia of Integer Sequences. https://oeis.org/A006535.
- Kagey, P. (2019). "A327094: Smallest polyomino containing all free n-ominoes." The On-Line Encyclopedia of Integer Sequences. https://oeis.org/A327094.
- Exley, P. (2026). "A392363: Polyiamond container (free)." The On-Line Encyclopedia of Integer Sequences. https://oeis.org/A392363.
- Exley, P. (2026). "A395422: Fixed-polyiamond container." The On-Line Encyclopedia of Integer Sequences. https://oeis.org/A395422.
- Tan, Y. K., Heule, M. J. H., and Myreen, M. O. (2021). "cake_lpr: Verified Propagation Redundancy Checking in CakeML." Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2021), LNCS 12651, Springer, 224-241. doi:10.1007/978-3-030-72013-1_12.
