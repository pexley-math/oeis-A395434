"""
verify_method1.py -- independent geometric verifier for one-sided-polyhex-container.

DISJOINT CODE PATH from solve_one-sided-polyhex-container.py:
  - Piece enumeration: pure-Python BFS over hex axial (q, r) coordinates,
    quotienting by the 6 rotations (NO reflections) to get one-sided
    equivalence classes. Does NOT import polyform_enum.
  - Containment check: direct set-inclusion over all 6 rotations and all
    translations of each one-sided piece. Does NOT use any SAT backend.
  - No imports from solve_*.py.

What it verifies: given the solver's reported a(n) and container cells
for each n, confirm that (i) the container is edge-connected under the
hex lattice adjacency, and (ii) every one-sided n-hex (enumerated
independently) fits inside the container under some rotation +
translation.

Outputs (independent audit trail, per the two-verifier rule):
  research/verify_method1-results.json   (per-n pass/fail + timing)
  research/verify_method1-run-log.txt    (verbose stdout transcript)

Usage:
    python verify_method1.py                              # all proved terms
    python verify_method1.py 6                             # verify n=1..6
    python verify_method1.py --n 3                         # single n
    python verify_method1.py --per-term-timeout 3600       # 1h per term
    python verify_method1.py --no-timeout                  # disable cap

Exit code: 0 iff all checks pass within budget.
"""

import json
import os
import sys
import time
from collections import deque
from datetime import datetime

_SHARED = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", ".."))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)
try:
    from figure_gen_utils.pipeline_timeouts import VERIFIER_TIMEOUT_S
except ImportError:
    VERIFIER_TIMEOUT_S = 3600
from sat_utils.verifier_base import VerifierBase


# ----------------------------------------------------------------------
# Hex axial (q, r) adjacency and rotation
# ----------------------------------------------------------------------

# Six neighbour directions in axial (q, r) coordinates.
_HEX_DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]


def _hex_neighbours(cell):
    q, r = cell
    return [(q + dq, r + dr) for dq, dr in _HEX_DIRS]


def _rot60(cell):
    """Rotate (q, r) by 60 degrees CCW about the origin: (q, r) -> (-r, q + r)."""
    q, r = cell
    return (-r, q + r)


def _rotations_of(piece):
    """Return the list of all 6 rotational images of a piece (as frozensets),
    each normalised by min-shift so the minimum q is 0 (and among q=0 cells,
    minimum r is 0). This is the canonical form under translation only.
    """
    rots = []
    cur = piece
    for _ in range(6):
        cur = frozenset(_rot60(c) for c in cur)
        mq = min(q for q, _ in cur)
        mr = min(r for q, r in cur if q == mq)
        shift = frozenset((q - mq, r - mr) for q, r in cur)
        rots.append(shift)
    return rots


# ----------------------------------------------------------------------
# Independent pure-Python one-sided polyhex enumeration
# ----------------------------------------------------------------------

def _normalise(cells):
    """Canonical form under translation only: shift min-q to 0, and among
    cells with minimum q shift min-r to 0.
    """
    mq = min(q for q, _ in cells)
    mr = min(r for q, r in cells if q == mq)
    return frozenset((q - mq, r - mr) for q, r in cells)


def enumerate_fixed_polyhexes(n):
    """Enumerate all fixed n-cell polyhexes via pure-Python BFS growth.
    Fixed = distinct up to translation only. No rotation, no reflection.
    Independent of polyform_enum.
    """
    if n <= 0:
        return [frozenset()]
    if n == 1:
        return [frozenset({(0, 0)})]
    prev = enumerate_fixed_polyhexes(n - 1)
    seen = set()
    out = []
    for p in prev:
        for cell in p:
            for nb in _hex_neighbours(cell):
                if nb in p:
                    continue
                grown = _normalise(p | {nb})
                if grown not in seen:
                    seen.add(grown)
                    out.append(grown)
    return out


def enumerate_one_sided_polyhexes(n):
    """Enumerate all one-sided n-cell polyhexes.

    One-sided = distinct up to rotation AND translation, but NOT reflection.
    Algorithm: enumerate fixed polyhexes, group by rotation-orbit, keep one
    representative per rotation-orbit. Two fixed pieces belong to the same
    rotation-orbit iff one is a rotation of the other; we use the
    lexicographic minimum over the 6 rotations as the canonical rep.
    """
    fixed = enumerate_fixed_polyhexes(n)
    seen_canon = set()
    out = []
    for p in fixed:
        canon = min(sorted(tuple(sorted(r)) for r in _rotations_of(p)))
        if canon not in seen_canon:
            seen_canon.add(canon)
            out.append(frozenset(canon))
    return out


# ----------------------------------------------------------------------
# Connectivity and containment
# ----------------------------------------------------------------------

def _is_connected(cells):
    cs = set(cells)
    if len(cs) <= 1:
        return True
    start = next(iter(cs))
    seen = {start}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        for nb in _hex_neighbours(cell):
            if nb in cs and nb not in seen:
                seen.add(nb)
                queue.append(nb)
    return len(seen) == len(cs)


def _piece_fits_anywhere(piece, container):
    """Does some rotation + translation of `piece` fit inside `container`?"""
    cr_min = min(q for q, _ in container)
    cr_max = max(q for q, _ in container)
    cc_min = min(r for _, r in container)
    cc_max = max(r for _, r in container)
    for rot in _rotations_of(piece):
        cells = list(rot)
        pr_min = min(q for q, _ in cells)
        pr_max = max(q for q, _ in cells)
        pc_min = min(r for _, r in cells)
        pc_max = max(r for _, r in cells)
        for dq in range(cr_min - pr_min, cr_max - pr_max + 1):
            for dr in range(cc_min - pc_min, cc_max - pc_max + 1):
                placed = {(q + dq, r + dr) for q, r in cells}
                if placed.issubset(container):
                    return True
    return False


# ----------------------------------------------------------------------
# Per-n verification driver
# ----------------------------------------------------------------------

def verify_n(n, solver_results, deadline=None):
    t0 = time.time()
    base = {
        "n": n, "ok": False, "status": "FAIL", "detail": "",
        "elapsed": 0.0, "pieces_checked": 0, "container_size": 0,
    }
    key = str(n)
    if key not in solver_results:
        base["detail"] = f"n={n}: no entry in solver-results.json"
        base["elapsed"] = time.time() - t0
        return base
    res = solver_results[key]
    if res.get("status") != "PROVED":
        base["detail"] = f"n={n}: solver status is {res.get('status')}, not PROVED"
        base["elapsed"] = time.time() - t0
        return base

    cells_list = res.get("cells") or []
    container = {(c[0], c[1]) for c in cells_list}
    reported = res.get("size") or res.get("value")
    base["container_size"] = len(container)
    if len(container) != reported:
        base["detail"] = (
            f"n={n}: reported size {reported} != cell count {len(container)}"
        )
        base["elapsed"] = time.time() - t0
        return base

    if not _is_connected(container):
        base["detail"] = f"n={n}: reported container is NOT connected"
        base["elapsed"] = time.time() - t0
        return base

    pieces = enumerate_one_sided_polyhexes(n)
    # A006535: authoritative OEIS one-sided polyhex counts.
    # a(1..10) = 1, 1, 3, 10, 33, 147, 620, 2821, 12942, 60639
    expected_count = {1: 1, 2: 1, 3: 3, 4: 10, 5: 33, 6: 147, 7: 620,
                      8: 2821, 9: 12942, 10: 60639}.get(n)
    if expected_count is not None and len(pieces) != expected_count:
        base["detail"] = (
            f"n={n}: independent enum returned {len(pieces)} pieces, "
            f"expected {expected_count} (A006535)"
        )
        base["elapsed"] = time.time() - t0
        return base

    for idx, p in enumerate(pieces):
        if deadline is not None and time.time() >= deadline:
            base["status"] = "TIMEOUT"
            base["detail"] = (
                f"n={n}: timed out after checking {idx}/{len(pieces)} "
                f"pieces in {time.time() - t0:.1f}s"
            )
            base["pieces_checked"] = idx
            base["elapsed"] = time.time() - t0
            return base
        if not _piece_fits_anywhere(p, container):
            base["detail"] = (
                f"n={n}: one-sided piece #{idx} ({sorted(p)}) does not fit"
            )
            base["pieces_checked"] = idx
            base["elapsed"] = time.time() - t0
            return base

    base["ok"] = True
    base["status"] = "PASS"
    base["pieces_checked"] = len(pieces)
    base["detail"] = (
        f"n={n}: {len(container)} cells connected, all {len(pieces)} "
        f"one-sided {n}-hexes contained (method1 geometric)"
    )
    base["elapsed"] = time.time() - t0
    return base


def _write_outputs(records, project_dir, all_pass, cli_args):
    from figure_gen_utils.versioned_output import save_versioned
    research_dir = os.path.join(project_dir, "research")
    os.makedirs(research_dir, exist_ok=True)

    summary = {
        "verifier": "verify_method1",
        "method": (
            "geometric set-inclusion on hex axial lattice "
            "(pure Python BFS, rotation + translation, "
            "disjoint enumeration, one-sided quotient)"
        ),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "per_term_timeout_s": cli_args.get("per_term_timeout_s"),
        "overall_status": "PASS" if all_pass else "FAIL_OR_TIMEOUT",
        "results": records,
    }
    json_path = os.path.join(research_dir, "verify_method1-results.json")
    save_versioned(summary, json_path)

    log_lines = [
        "verify_method1 run log",
        "=" * 60,
        "Method: hex geometric set-inclusion (pure Python BFS, one-sided)",
        f"Timestamp: {summary['timestamp']}",
        f"Per-term timeout: {cli_args.get('per_term_timeout_s')} s",
        f"Overall: {summary['overall_status']}",
        "",
    ]
    for r in records:
        log_lines.append(
            f"  [{r['status']}] {r['detail']}  [{r['elapsed']:.1f}s]"
        )
    log_lines.append("")
    log_lines.append(
        "NO pre-primed values. All values derived from scratch by "
        "independent pure-Python enumeration."
    )
    log_text = "\n".join(log_lines)
    log_path = os.path.join(research_dir, "verify_method1-run-log.txt")
    save_versioned(log_text, log_path)


# ----------------------------------------------------------------------
# VerifierBase subclass
# ----------------------------------------------------------------------

_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_RESULTS_PATH = os.path.join(_PROJECT_DIR, "research", "solver-results.json")


class Method1Verifier(VerifierBase):
    name = "verify_method1 (hex geometric, pure-Python, one-sided)"
    description = (
        "Independent geometric verifier for one-sided-polyhex container: "
        "pure-Python piece enumeration over hex axial coordinates, "
        "one-sided quotient by 6-rotation orbits, set-inclusion "
        "containment under rotation + translation. Disjoint code path "
        "from the solver (no polyform_enum, no SAT backend)."
    )
    default_max_n = 6
    verify_tag = "1"
    default_per_term_timeout = float(VERIFIER_TIMEOUT_S)

    def __init__(self):
        if not os.path.exists(_RESULTS_PATH):
            raise FileNotFoundError(
                f"solver-results.json not found at {_RESULTS_PATH}; "
                f"run the solver first."
            )
        with open(_RESULTS_PATH, "r", encoding="utf-8") as f:
            self._solver_results = json.load(f)
        self._records = []

    @classmethod
    def select_ns(cls, args):
        if not os.path.exists(_RESULTS_PATH):
            return []
        with open(_RESULTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        proved = sorted(
            int(k) for k, v in data.items() if v.get("status") == "PROVED"
        )
        if args.n is not None:
            return [args.n] if args.n in proved else []
        return [n for n in proved if n <= args.max_n]

    def verify_n(self, n):
        rec = verify_n(
            n, self._solver_results, deadline=self._per_term_deadline
        )
        self._records.append(rec)
        if rec["status"] == "PASS":
            return rec.get("container_size"), rec["detail"]
        if rec["status"] == "TIMEOUT":
            return None, f"TIMEOUT: {rec['detail']}"
        return None, rec["detail"]

    def expected(self, n):
        key = str(n)
        if key not in self._solver_results:
            return None
        res = self._solver_results[key]
        return res.get("size") or res.get("value")

    def save_artifacts(self, summary, log_text):
        _write_outputs(
            self._records,
            _PROJECT_DIR,
            summary["all_ok"],
            cli_args={"per_term_timeout_s": summary["per_term_timeout_s"]},
        )


if __name__ == "__main__":
    sys.exit(Method1Verifier.run())
