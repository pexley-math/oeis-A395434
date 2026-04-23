"""
Smallest Polyomino Containing All FIXED n-Ominoes

Computes the smallest connected polyomino on the square grid that contains
every fixed n-omino as a subregion via translation only (no rotation,
no reflection of the contained piece). This is the square-grid analog
of the fixed-polyiamond-container project, and a cousin of A327094 (free
pieces) and the one-sided variant. The translation-only containment
predicate makes it a genuinely new sequence (verdict CLEAR per the
prior-art-search step).

Architecture: instantiates ``sat_utils.frameworks.ContainerSolverFramework``
with the square-grid defaults. The framework supplies SAT + CEGAR
connectivity, top-down search descent, D4 symmetry breaking, the
solver-CLI wrapper, versioned JSON output, and the SolverLogger. This
module is glue.

Usage:
    python solve_new-fixed-polyomino-container.py --n 1-5
    python solve_new-fixed-polyomino-container.py --n 1-7 --per-term-timeout 1800

License: CC-BY-4.0
"""

import sys

from polyform_enum import SQUARE, enumerate_fixed

from sat_utils.frameworks import (
    ContainerSolverFramework,
    default_bridge_candidates,
)


# A001168 -- number of fixed polyominoes with n cells. Used by the
# banner extra_lines_fn to sanity-check the polyform_enum Cython
# backend is returning the right counts.
FIXED_POLYOMINO_COUNTS = {
    1: 1, 2: 2, 3: 6, 4: 19, 5: 63, 6: 216,
    7: 760, 8: 2725, 9: 9910, 10: 36446,
}


def _a001168_banner_lines():
    """Sanity-check lines emitted into the solver banner.

    Verifies the polyform_enum.enumerate_fixed backend returns the
    expected A001168 counts for n=1..10.
    """
    lines = ["  Fixed polyomino counts (A001168):"]
    for test_n in range(1, 11):
        try:
            count = len(list(enumerate_fixed(test_n, SQUARE)))
        except Exception as exc:  # pragma: no cover -- diagnostic only
            count = f"err({exc!s})"
        expected = FIXED_POLYOMINO_COUNTS.get(test_n, "?")
        tag = "OK" if count == expected else f"MISMATCH expected {expected}"
        lines.append(f"    n={test_n}: {count} fixed {test_n}-ominoes  {tag}")
    return lines


solver = ContainerSolverFramework(
    seq_id="NEW",
    description=(
        "Smallest polyomino containing all FIXED n-ominoes "
        "(translation only; square grid)"
    ),
    method_label="SAT + CEGAR connectivity (CaDiCaL via PySAT)",
    software_label="solve_new-fixed-polyomino-container.py via "
                   "ContainerSolverFramework (square)",
    geometry="square",
    piece_enumerator=lambda n: enumerate_fixed(n, SQUARE),
    piece_mode="fixed",
    # Trivial upper bound a(n) <= n*n: the n x n square box contains
    # every fixed n-omino as a translate (any fixed n-omino has
    # bounding box at most n x n). Floor at 1 for n=1.
    upper_bound=lambda n: max(1, n * n),
    # Tight n x n bounding grid -- matches the n=1 trivial case
    # (1 x 1) and is exactly large enough to host any fixed n-omino.
    grid_shape_fn=lambda n: (max(1, n), max(1, n)),
    # CaDiCaL-153 measured fastest on the polyiamond sibling; default
    # here while we wait for the iterate-skill A/B at the square scale.
    solver_name="glucose42",
    use_symmetry=True,            # D4 breakers on the container (set is D4-invariant)
    bridge_candidates_fn=None,    # SELFCRITIQUE D: drop bridge cuts
    incremental=True,             # ITotalizer descent: one solver across the k sweep
    use_lonely_cell_clauses=False,  # ITER 4 (simplification): no precomputed lonely-cell clauses
    extra_lines_fn=_a001168_banner_lines,
)


if __name__ == "__main__":
    sys.exit(solver.main())
