"""
verify_method1.py -- independent geometric verifier for new-fixed-polyomino-container.

DISJOINT CODE PATH from solve_new-fixed-polyomino-container.py:
  - Piece enumeration: pure-Python BFS over square grid coordinates
    with 4-adjacency. Does NOT import polyform_enum.
  - Containment check: direct set-inclusion over translated piece cells.
    Does NOT use any SAT backend.
  - Connectivity: BFS over the cell set with 4-adjacency.
  - No imports from solve_*.py.

What it verifies: given the solver's reported a(n) and container cells
for each n, confirm that (i) the container is edge-connected under the
square 4-adjacency, and (ii) every fixed n-omino (enumerated
independently) fits inside the container as a translated copy.

Outputs (independent audit trail, per the two-verifier rule):
  research/verify_method1-results.json   (per-n pass/fail + timing)
  research/verify_method1-run-log.txt    (verbose stdout transcript)

Usage:
    python verify_method1.py                              # all proved terms
    python verify_method1.py 7                             # verify n=1..7
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


def _sq_neighbours(cell):
    r, c = cell
    return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]


def _origin_shift(cells):
    mr = min(r for r, _ in cells)
    mc = min(c for _, c in cells)
    return frozenset((r - mr, c - mc) for r, c in cells)


def enumerate_fixed_pure(n):
    """Enumerate all fixed n-cell polyominoes via Python BFS growth.

    Fixed = distinct up to translation only (no rotation, no reflection).
    Independent of polyform_enum. Counts match A001168.
    """
    if n <= 0:
        return [frozenset()]
    if n == 1:
        return [frozenset({(0, 0)})]
    prev = enumerate_fixed_pure(n - 1)
    seen = set()
    out = []
    for p in prev:
        for cell in p:
            for nb in _sq_neighbours(cell):
                if nb in p:
                    continue
                grown = _origin_shift(p | {nb})
                if grown not in seen:
                    seen.add(grown)
                    out.append(grown)
    return out


def _is_connected(cells):
    cs = set(cells)
    if len(cs) <= 1:
        return True
    start = next(iter(cs))
    seen = {start}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        for nb in _sq_neighbours(cell):
            if nb in cs and nb not in seen:
                seen.add(nb)
                queue.append(nb)
    return len(seen) == len(cs)


def _piece_fits(piece, container):
    cells = list(piece)
    if not cells:
        return True
    pr_min = min(r for r, _ in cells)
    pr_max = max(r for r, _ in cells)
    pc_min = min(c for _, c in cells)
    pc_max = max(c for _, c in cells)
    cr_min = min(r for r, _ in container)
    cr_max = max(r for r, _ in container)
    cc_min = min(c for _, c in container)
    cc_max = max(c for _, c in container)
    for dr in range(cr_min - pr_min, cr_max - pr_max + 1):
        for dc in range(cc_min - pc_min, cc_max - pc_max + 1):
            placed = {(r + dr, c + dc) for r, c in cells}
            if placed.issubset(container):
                return True
    return False


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
    status_val = res.get("status")
    if status_val != "PROVED":
        base["detail"] = f"n={n}: solver status is {status_val}, not PROVED"
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

    pieces = enumerate_fixed_pure(n)
    expected_count = {1: 1, 2: 2, 3: 6, 4: 19, 5: 63, 6: 216,
                      7: 760, 8: 2725, 9: 9910, 10: 36446}.get(n)
    if expected_count is not None and len(pieces) != expected_count:
        base["detail"] = (
            f"n={n}: independent enum returned {len(pieces)} pieces, "
            f"expected {expected_count} (A001168)"
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
        if not _piece_fits(p, container):
            base["detail"] = (
                f"n={n}: fixed piece #{idx} ({sorted(p)}) does not fit"
            )
            base["pieces_checked"] = idx
            base["elapsed"] = time.time() - t0
            return base

    base["ok"] = True
    base["status"] = "PASS"
    base["pieces_checked"] = len(pieces)
    base["detail"] = (
        f"n={n}: {len(container)} cells connected, all {len(pieces)} "
        f"fixed {n}-ominoes contained (method1 geometric)"
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
            "geometric set-inclusion on square lattice "
            "(pure Python BFS, 4-adjacency, disjoint enumeration)"
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
        "Method: square-lattice geometric set-inclusion (pure Python BFS)",
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


_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_RESULTS_PATH = os.path.join(_PROJECT_DIR, "research", "solver-results.json")


class Method1Verifier(VerifierBase):
    name = "verify_method1 (square geometric, pure-Python, independent enum)"
    description = (
        "Independent geometric verifier for fixed-polyomino container: "
        "pure-Python piece enumeration with translation only, "
        "set-inclusion containment, and 4-adjacency BFS connectivity. "
        "Disjoint code path from the solver."
    )
    default_max_n = 8
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
