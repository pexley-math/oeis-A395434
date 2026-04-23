"""
Smallest Polyhex Containing All One-Sided n-Hexes

Finds the minimum connected polyhex that contains every one-sided
n-hex as a subregion. One-sided pieces are equivalence classes
under rotation only (reflections are distinct). The framework
places each piece in any of its rotation orbit (6 rotations for
a chiral piece, fewer for a piece with rotational symmetry) but
does NOT consider reflections -- that is the one_sided piece_mode.

Hex-grid one-sided analog of A327094 (square fixed container).
Sibling of oeis-new-polyhex-container (free) and the fixed-polyhex
container family.

Usage:
    python solve_one-sided-polyhex-container.py --n 1-6

Outputs (written by the framework via sat_utils + figure_gen_utils helpers):
    research/solver-results.json  -- per-n proof record (save_versioned)
    research/solver-run-log.txt   -- verbose run log (SolverLogger)

License: CC-BY-4.0
"""

import sys

from polyform_enum import HEX, enumerate_one_sided

from sat_utils.frameworks import ContainerSolverFramework
from sat_utils.frameworks.container import default_bridge_candidates


solver = ContainerSolverFramework(
    seq_id="NEW",
    description=(
        "Smallest polyhex containing all ONE-SIDED n-hexes "
        "(one-sided hex analog of A327094)"
    ),
    method_label="SAT + CEGAR connectivity (CaDiCaL via PySAT)",
    software_label=(
        "solve_one-sided-polyhex-container.py via ContainerSolverFramework"
    ),
    geometry="hex",
    piece_enumerator=lambda n: enumerate_one_sided(n, HEX),
    piece_mode="one_sided",
    # Tighter upper bound: empirically a(n) grows roughly as n^2/2 on
    # the one-sided hex family; n*(n+1)//2 + n is an n^2/2 + n upper
    # cap, safely above observed values 1..15 at n=1..6 while cutting
    # the ITotalizer descent length relative to the loose n*n seed.
    upper_bound=lambda n: n * (n + 1) // 2 + n,
    # grid_shape_fn omitted: framework default for hex is (n+1, n+1),
    # which is exactly what we want (wider-window margin for DRAT).
    use_lonely_cell_clauses=True,
    incremental=True,
    bridge_candidates_fn=default_bridge_candidates,
    use_translation_breaker=True,
)


if __name__ == "__main__":
    sys.exit(solver.main())
