# Design Rationale -- One-Sided Polyhex Container

## Chosen approach

**SAT + CEGAR connectivity** via `sat_utils.frameworks.ContainerSolverFramework`,
enumerating pieces with `polyform_enum.enumerate_one_sided(n, HEX)` and running
incremental ITotalizer descent to prove the minimum cell count `a(n)`.

Glue file: `code/solve_one-sided-polyhex-container.py`. The framework owns
the CNF build, solver selection, CEGAR connectivity loop, top-down k descent,
and JSON/log output. The glue file supplies only four facts:

1. `geometry="hex"`,
2. `piece_enumerator=lambda n: enumerate_one_sided(n, HEX)`,
3. `piece_mode="one_sided"` -- placement step rotates each piece through its
   full rotation orbit (6 for chiral, fewer for C6-symmetric pieces) but does
   NOT add reflections, matching the one-sided equivalence class,
4. `upper_bound=lambda n: n*n`, `grid_shape_fn=lambda n: (n+1, n+1)`.

## Decision-tree result (cookbook)

- Container family (minimum piece-bounding polyform) -> ContainerSolverFramework.
- Pieces = one-sided equivalence classes -> `piece_mode="one_sided"`.
- Hex lattice geometry -> `geometry="hex"`, `grids.HEX` in enumerator.
- Connectivity of the container is required -> framework's default CEGAR-on-demand
  connectivity cutting planes handle this without pre-materialising all
  connectivity lemmas.
- Wider window (n+1) x (n+1) chosen over tight (n) x (n) so the same code path
  is reusable for the DRAT-certified unconditional result in /solver-verify /
  wider-window (see feedback-wider-window-discharges-S.md).

## Alternatives considered

- **Pure enumerate-and-fit** (no SAT): infeasible at n >= 5 where the one-sided
  piece count (A006535: 33 at n=5, 147 at n=6) combined with O(grid * rotations)
  placements blows up the search tree.
- **CP-SAT instead of PySAT**: framework supports both, PySAT gave comparable
  results on sibling projects (fixed-polyhex, fixed-polyiamond). No reason to
  switch.
- **Tight (n) x (n) grid**: matches the free polyhex-container legacy exactly
  but leaves no margin for wider-window DRAT upgrade in /solver-verify. Chose
  (n+1) x (n+1) for compatibility with downstream verification.

## Expected performance characteristics

- Trivial terms n=1, 2, 3 solve in seconds (confirmed: a(1)=1 and a(2)=2 each
  < 0.1s on a smoke run; the framework's SAT + CEGAR loop is dominated by piece
  enumeration at small n).
- Baseline benchmark set expected around n=1..6 under the 120s per-term cap,
  based on the free polyhex-container sibling's profile and the larger
  one-sided piece count.
- Frontier work (pushing past the benchmark) belongs to /solver-iterate, not
  this skill.
