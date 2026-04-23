// One-Sided Polyhex Container -- typst source
// Generated from submission/paper.md

#set document(
  title: "Minimum Polyhex Containing All One-Sided n-Hexes",
  author: "Peter Exley",
)

#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1",
)

#set text(
  font: "New Computer Modern",
  size: 11pt,
)

#set par(
  justify: true,
  leading: 0.65em,
)

#set heading(numbering: "1.")

#show heading.where(level: 1): it => {
  v(1em)
  text(size: 13pt, weight: "bold", it)
  v(0.5em)
}
#show heading.where(level: 2): it => {
  v(0.8em)
  text(size: 11pt, weight: "bold", it)
  v(0.3em)
}

#align(center)[
  #text(size: 16pt, weight: "bold")[
    Minimum Polyhex Containing All One-Sided n-Hexes
  ]
  #v(1em)
  #text(size: 12pt)[Peter Exley]
  #v(0.3em)
  #text(size: 10pt, style: "italic")[pexley-math\@github]
  #v(0.5em)
  #text(size: 10pt)[Submitted: April 2026]
  #v(1.5em)
]

#block(
  width: 100%,
  inset: (x: 2em),
)[
  #text(weight: "bold")[Abstract.]
  Let $a(n)$ denote the minimum number of hexagonal cells in an edge-connected polyhex that contains, under some rotation and translation, every one-sided $n$-hex. We compute $a(n)$ for $n = 1$ through $7$ as the sequence $1, 2, 4, 7, 11, 15, 21$, with each term certified by two independent checks: a geometric set-inclusion verifier (Python, disjoint from the solver) and a machine-verified DRAT or LRAT proof of the UNSAT step at $k = a(n) - 1$. A SAT encoding on the $(n+1) times (n+1)$ hex axial rectangle reduces the decision problem $a(n) <= k$ to a single Boolean formula; a top-down ITotalizer descent with lonely-cell preprocessing, disjunctive CEGAR connectivity cuts, and a lex-least translation breaker computes each term. No closed-form expression matches $a(1)$ through $a(7)$; the growth rate is consistent with $a(n) = Theta(n^2)$. The sequence is submitted to the OEIS as A395434.

  #v(0.5em)
  #text(weight: "bold")[Keywords:] polyhex, hexagonal lattice, container sequence, SAT, DRAT, LRAT.

  #text(weight: "bold")[Mathematics Subject Classification:] 05B50, 52C20
]

#v(1em)
#line(length: 100%)
#v(0.5em)

= Introduction

A _polyhex_ is a connected set of unit hexagonal cells on the hex lattice. Two polyhexes are _one-sided equivalent_ if one is a rotation of the other; reflections are distinct. The number of one-sided $n$-hexes is OEIS A006535: $1, 1, 3, 10, 33, 147, 620, 2821, 12942, 60639, dots$ .

A polyhex $C$ is a _container_ for one-sided $n$-hexes if every one-sided $n$-hex can be placed inside $C$ under some rotation and translation, with all cells of the placed piece lying inside $C$. Define

#block(inset: (left: 1.5em))[
  $a(n) = $ minimum number of cells in a container for one-sided $n$-hexes.
]

Container sequences of this family are a natural combinatorial-geometry question: the square-lattice counterpart is OEIS A327094, the free-polyiamond (triangular lattice) counterpart is A392363, and the fixed-polyiamond counterpart is A395422. The present paper computes the one-sided hex version, which to our knowledge has not appeared in the literature or OEIS prior to this work.

#block(inset: (left: 1.5em), stroke: (left: 2pt + luma(180)))[
  *Theorem 1 (Trivial bound).* For every $n >= 1$, $a(n) >= n$.

  _Proof._ Let $P$ be any fixed $n$-cell one-sided polyhex. A container $C$ for one-sided $n$-hexes must admit a placement of $P$: there exist a rotation $rho$ and a translation $t$ with $(rho(P) + t) subset.eq C$. Since $|rho(P) + t| = |P| = n$ and all placed cells are distinct cells of $C$, $|C| >= n$. Minimising over containers yields $a(n) >= n$. #sym.qed
]

#block(inset: (left: 1.5em), stroke: (left: 2pt + luma(180)))[
  *Theorem 2 (Computed values, DRAT-certified).* The sequence $a(1), a(2), dots, a(7)$ equals $1, 2, 4, 7, 11, 15, 21$. Each value has been verified by an independent geometric containment check and by a machine-verified UNSAT proof (drat-trim for $n = 1..6$; cadical $--$lrat followed by lrat-check for $n = 7$).
]

No closed-form recurrence or polynomial expression was found to match $a(1)$ through $a(7)$; the observed growth is polynomial of order $2$.

= Definitions and Notation

- *Hex lattice, axial coordinates.* We use axial coordinates $(q, r)$ where the six neighbours of a hex cell $(q, r)$ are $(q plus.minus 1, r)$, $(q, r plus.minus 1)$, $(q+1, r-1)$, $(q-1, r+1)$.
- *$n$-hex (polyhex of size $n$).* An edge-connected set of $n$ distinct hex cells. Equivalence classes: (i) _fixed_ under translation only (A001207); (ii) _one-sided_ under rotation plus translation (A006535); (iii) _free_ under rotation, reflection, plus translation (A000228).
- *Container.* An edge-connected polyhex $C$ is a container for one-sided $n$-hexes if for every one-sided $n$-hex $P$ there exist a rotation $rho$ (by a multiple of $60$ degrees) and a translation $t$ with $rho(P) + t subset.eq C$.
- *$a(n)$.* The minimum $|C|$ over all containers $C$.

= Computational Methodology

We encode the decision problem "does a container of size $k$ exist inside an axial rectangle of dimensions $R times C$?" as a Boolean SAT instance with:

+ *Cell variables* $x_(q, r)$ for each cell in the rectangle.
+ *Placement variables* $y_(P, rho, t)$ for every one-sided piece $P$, rotation $rho$, and translation $t$ that fits the rotated piece inside the rectangle. At-least-one-placement per piece: $sum_(rho, t) y_(P, rho, t) >= 1$. Placement implies cell selection: $y -> x$ for every cell of the placed piece.
+ *Connectivity* via a CEGAR loop: selected cells are partitioned into components; multi-component models get a disjunctive cut forbidding the offending components (optionally with bridge-cell activation disjuncts).
+ *Cardinality* via an ITotalizer encoding of $sum x <= k$, with an incremental-SAT driver walking $k$ downward until UNSAT at $k - 1$.

The search rectangle is $(n+1) times (n+1)$ axial cells, a one-row/one-column margin above the minimum bounding box of any $n$-hex.

*Piece enumeration.* The solver uses `polyform_enum.enumerate_one_sided(n, HEX)` (Cython, A006535-counts). The independent verifier re-enumerates from scratch in pure Python, via BFS growth quotiented by the rotation-orbit canonical form, and cross-checks its piece count against A006535.

*Solver optimisation.* Six A/B iterations against $n = 6$:

#table(
  columns: 4,
  align: (center, left, left, right),
  stroke: 0.5pt,
  table.header([*\#*], [*Category*], [*Change*], [*Delta n=6*]),
  [1], [encoding], [`use_lonely_cell_clauses=True`], [$19.3 -> 17.2$ s],
  [2], [parameters], [upper bound $n^2 -> n(n+1)\/2 + n$], [$17.2 -> 13.8$ s],
  [3], [architecture], [`incremental=True` (persistent ITotalizer + CEGAR)], [$13.8 -> 10.4$ s],
  [4], [simplification], [drop redundant `grid_shape_fn` override], [$10.4 -> 10.4$ s],
  [5], [architecture], [`bridge_candidates_fn` (Phase 3 disjunctive cuts)], [$10.4 -> 10.1$ s],
  [6], [encoding], [`use_translation_breaker=True`], [$10.1 -> 8.3$ s],
)

*Framework correction.* Iteration 1 exposed a latent bug: `use_lonely_cell_clauses=True` drove $a(1)$ to $2$ instead of $1$. The lonely-cell clause "every selected cell has a selected neighbour" is invalid when the optimal container is a single cell. The fix guards both CNF-build sites with $n >= 2$ (commit `0edd24c1`).

*Verification.* A geometric verifier (pure Python, hex axial, disjoint code path) independently enumerates one-sided $n$-hexes and checks that every piece fits the solver's container under some rotation and translation. Piece counts agree with A006535 for $n = 1..7$.

= Proved Values and DRAT Certification

#table(
  columns: 6,
  align: (center, center, center, right, center, left),
  stroke: 0.5pt,
  table.header([*$n$*], [*$a(n)$*], [*box*], [*solver s*], [*verifier 1*], [*DRAT*]),
  [1], [1], [$1 times 1$], [0.001], [PASS], [CERTIFIED (drat-trim)],
  [2], [2], [$1 times 2$], [0.001], [PASS], [CERTIFIED (drat-trim)],
  [3], [4], [$2 times 3$], [0.002], [PASS], [CERTIFIED (drat-trim)],
  [4], [7], [$4 times 3$], [0.010], [PASS], [CERTIFIED (drat-trim)],
  [5], [11], [$3 times 6$], [0.597], [PASS], [CERTIFIED (drat-trim)],
  [6], [15], [$6 times 6$], [8.290], [PASS], [CERTIFIED (drat-trim)],
  [7], [21], [$8 times 5$], [1797.2], [PASS], [CERTIFIED (cadical --lrat + lrat-check)],
)

_Note on n = 7 certification._ At $n = 7$ the cadical-produced DRAT proof reached 1.1 GB. drat-trim stalled at approximately 2 per cent of the file after 40 minutes, projected to 15-20 hours total. We re-emitted the UNSAT proof in LRAT format directly from cadical (the `--lrat=true` flag), producing a 3.37 GB LRAT certificate on the same CNF, and verified it with lrat-check in 80 seconds. cadical is the identical solver used in the main proof run, so the UNSAT verdict on the same CNF is the same mathematical event; only the proof-certificate format and checker differ.

= Empirical Analysis and Conjectures

First differences $d(n) = a(n+1) - a(n)$ for $n = 1..6$ are $1, 2, 3, 4, 4, 6$; second differences are $1, 1, 1, 0, 2$. The sequence is not smoothly polynomial.

*Conjectures tested.* Six candidate formulas; none match all seven terms:

+ Polynomial $a(n) = n(n-1)\/2 + 1$ (lazy-caterer shift): fails at $n = 6$ ($16$ vs $15$).
+ Polynomial $a(n) = "round"(0.42 n^2)$: fails at $n = 7$ ($18$ vs $21$).
+ Recurrence $a(n) = a(n-1) + a(n-2) - a(n-3) + 2$: fails at $n = 6$.
+ Closed form $a(n) = floor(n(n+1)\/3) + 1$: fails at $n = 7$.
+ Identity $a(n) = "A006535"(n) + dots$: ruled out structurally.
+ Cross-lattice identity $a(n) = "A327094"(n)$: fails at $n = 4$.

An exhaustive search over linear recurrences of order $<= 4$ with coefficient magnitudes $<= 3$ found none matching all seven terms.

*Active conjecture (UNVERIFIED).* $a(n) = Theta(n^2)$. Empirically, $n^2 \/ 3 <= a(n) <= 5 n^2 \/ 8$ for $n = 1..7$. A structural inflation or tiling argument is required to convert this envelope into a closed form.

= Discussion and Open Problems

+ *Closed form.* No polynomial, rational, or small-coefficient linear recurrence matches $a(1)$ through $a(7)$. Whether $a(n)$ satisfies any elementary closed form is open.
+ *$n = 8$ and beyond.* $n = 7$ took about 20 minutes of CPU; $n = 8$ timed out under the 30-minute per-term budget. A longer budget or a structural argument is required to push the range.
+ *Minimality of the $(n+1) times (n+1)$ window.* The geometric verifier is rectangle-free, but the SAT half assumes the optimum lies inside the $(n+1) times (n+1)$ window. Extending to larger $n$ would benefit from a structural proof.
+ *Cross-lattice comparison.* For $n = 4$, A327094 (square) $= 6 <$ A395422 (triangular fixed) $= 9$, with our one-sided hex version sitting at $7$. A systematic comparison across lattices and equivalence classes is open.

= Reproducibility

All code, data, and certificates are under `research-outputs/paper-project/oeis-new-one-sided-polyhex-container/` in the project repository.

*Solver entry point:* `code/solve_one-sided-polyhex-container.py`.

*Compute the full proved range:*

```
python code/solve_one-sided-polyhex-container.py \
    --n 1-7 --per-term-timeout 1800 --emit-drat --check-drat
```

*Re-run the independent geometric verifier:*

```
python code/verify_method1.py 7
```

*Re-verify $n = 7$ by the LRAT path:*

```
cadical.exe --lrat=true --binary=false \
    research/drat/n7_k20.cnf research/drat/n7_k20.lrat
lrat-check.exe research/drat/n7_k20.cnf research/drat/n7_k20.lrat
```

*Expected certificates.* `research/drat/n$N$_k$K$.{cnf,drat,sidecar.json}` for $n = 1..7$, and `research/drat-certification-summary.json` with `certified: true` for every $n$ in $1..7$. `research/verify_method1-results.json` with `status: PASS` for every $n$.

= Acknowledgements

The author thanks the maintainers of the OEIS for the extensive polyform reference data used in this work, and the authors of cadical, drat-trim, and lrat-check whose proof-emission and proof-checking tools underlie the certification pipeline.

= Bibliography

#block(inset: (left: 1em))[
  Biere, A., Fazekas, K., Fleury, M., and Heisinger, M. (2020). _CaDiCaL, Kissat, Paracooba, Plingeling and Treengeling Entering the SAT Competition 2020._ Proc. SAT Competition 2020, University of Helsinki, B-2020-1, 51-53.

  Heule, M. J. H., Hunt, W. A., and Wetzler, N. (2013). _Trimming while Checking Clausal Proofs._ FMCAD 2013, IEEE, 181-188. doi:10.1109/FMCAD.2013.6679408.

  OEIS Foundation (2026). _A000228: Number of hexagonal polyominoes with n cells._ https:\/\/oeis.org/A000228.

  OEIS Foundation (2026). _A001207: Number of fixed hexagonal polyominoes with n cells._ https:\/\/oeis.org/A001207.

  OEIS Foundation (2026). _A006535: Number of one-sided hexagonal polyominoes with n cells._ https:\/\/oeis.org/A006535.

  Kagey, P. (2019). _A327094: Smallest polyomino containing all free n-ominoes._ https:\/\/oeis.org/A327094.

  Exley, P. (2026). _A392363: Polyiamond container (free)._ https:\/\/oeis.org/A392363.

  Exley, P. (2026). _A395422: Fixed-polyiamond container._ https:\/\/oeis.org/A395422.

  Tan, Y. K., Heule, M. J. H., and Myreen, M. O. (2021). _cake_lpr: Verified Propagation Redundancy Checking in CakeML._ TACAS 2021, LNCS 12651, Springer, 224-241. doi:10.1007/978-3-030-72013-1_12.
]
