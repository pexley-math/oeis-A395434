"""
confirm_n8_from_archive.py -- one-shot geometric confirmation that the
archived 2026-04-23 n=8 container of size 26 is a valid one-sided polyhex
container under the current pipeline's verification contract.

Also runs a sanity check on n=1..7 from the same archive: these have
already been re-proved by the current pipeline, so verify_method1 must
PASS on them. If the n=1..7 sanity passes, the n=8 verdict is trustworthy.

ISOLATED from the pipeline:
  - Reads ONLY the recovered archive file (./.tmp_archived_results.json,
    extracted from git commit 400bdee6^).
  - Writes ONLY to research/n1-7-sanity-{results.json,log.txt}
    and  research/n8-confirmation-{results.json,log.txt}.
  - Does NOT touch solver-results.json, verify_method1-results.json,
    pipeline-log.json, iteration-log.tsv, or any other pipeline artifact.

What it does:
  - Reuses verify_method1.verify_n (pure-Python BFS enumeration of all
    one-sided n-hexes via A006535, geometric set-inclusion under
    6 rotations + translation).
  - Confirms or refutes a(8) <= 26 in minutes (an UPPER bound: the
    archived 26-cell container is a valid solution iff verify_method1
    passes). Does NOT prove a(8) >= 26 (the matching lower bound
    requires UNSAT@25 SAT, which is the multi-hour task).

Exit code: 0 iff (a) all of n=1..7 sanity-checks PASS and (b) n=8
geometric containment PASSES.
"""

import json
import os
import sys
import time
from datetime import datetime

_THIS = os.path.abspath(os.path.dirname(__file__))
_PROJECT = os.path.abspath(os.path.join(_THIS, ".."))
_REPO_ROOT = os.path.abspath(os.path.join(_PROJECT, "..", "..", ".."))

if _THIS not in sys.path:
    sys.path.insert(0, _THIS)

from verify_method1 import verify_n  # disjoint geometric verifier


_BUNDLED_ARCHIVE = os.path.join(
    _PROJECT, "research", "2026-04-23-solver-results.json",
)
_LEGACY_ARCHIVE = os.path.join(_REPO_ROOT, ".tmp_archived_results.json")
ARCHIVE_PATH = (
    _BUNDLED_ARCHIVE if os.path.exists(_BUNDLED_ARCHIVE)
    else _LEGACY_ARCHIVE
)
SANITY_JSON = os.path.join(_PROJECT, "research", "n1-7-sanity-results.json")
SANITY_LOG  = os.path.join(_PROJECT, "research", "n1-7-sanity-log.txt")
CONFIRM_JSON = os.path.join(_PROJECT, "research", "n8-confirmation-results.json")
CONFIRM_LOG  = os.path.join(_PROJECT, "research", "n8-confirmation-log.txt")

PER_TERM_TIMEOUT_S = 1800  # 30 min hard cap per term


def _wrap(archive, n):
    """Wrap a single archive entry in the schema verify_n expects."""
    e = archive[str(n)]
    return {
        str(n): {
            "n": n,
            "value": e.get("size") or e.get("value"),
            "size":  e.get("size") or e.get("value"),
            "status": "PROVED",
            "cells": e.get("cells") or [],
        }
    }


def _verify(archive, n):
    """Run verify_method1.verify_n on one n; return (rec, wall_seconds)."""
    wrapped = _wrap(archive, n)
    t0 = time.time()
    deadline = t0 + PER_TERM_TIMEOUT_S
    rec = verify_n(n, wrapped, deadline=deadline)
    return rec, time.time() - t0


def _write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def _write_log(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    if not os.path.exists(ARCHIVE_PATH):
        print(f"FAIL: archive not found at {ARCHIVE_PATH}", file=sys.stderr)
        return 2

    with open(ARCHIVE_PATH, "r", encoding="utf-8") as f:
        archive = json.load(f)

    missing = [str(n) for n in range(1, 9) if str(n) not in archive]
    if missing:
        print(f"FAIL: archive missing entries for n in {missing}", file=sys.stderr)
        return 2

    timestamp = datetime.now().isoformat(timespec="seconds")

    # ------------------------------------------------------------------
    # Phase 1: sanity check n=1..7 (must all PASS for n=8 verdict to be trustworthy)
    # ------------------------------------------------------------------
    print("=" * 60)
    print("PHASE 1: sanity check n=1..7 (these are already PROVED)")
    print("=" * 60)
    sanity_records = []
    sanity_wall_total = 0.0
    all_sanity_ok = True
    for n in range(1, 8):
        e = archive[str(n)]
        size = e.get("size") or e.get("value")
        cells = e.get("cells") or []
        print(f"  n={n}: claimed size={size}, cells={len(cells)} ... ", end="", flush=True)
        rec, wall = _verify(archive, n)
        sanity_wall_total += wall
        sanity_records.append({"n": n, "wall_seconds": wall, **rec})
        ok = rec.get("ok", False)
        all_sanity_ok = all_sanity_ok and ok
        print(f"{rec.get('status')} ({wall:.1f}s)")
        if not ok:
            print(f"    detail: {rec.get('detail')}")

    sanity_summary = {
        "purpose": "Sanity check: verify n=1..7 from the archived "
                   "2026-04-23 solver-results agree with the current "
                   "pipeline's verify_method1 contract. If these pass, "
                   "the n=8 verdict in the companion file is trustworthy.",
        "source": "git commit 400bdee6^ (archived solver-results.json), "
                  "recovered to .tmp_archived_results.json",
        "method": "verify_method1.verify_n (pure-Python BFS enumeration "
                  "of one-sided n-hexes via A006535, set-inclusion "
                  "containment under rotation + translation)",
        "timestamp": timestamp,
        "per_term_timeout_s": PER_TERM_TIMEOUT_S,
        "wall_seconds_total": sanity_wall_total,
        "all_pass": all_sanity_ok,
        "results": sanity_records,
    }
    _write_json(SANITY_JSON, sanity_summary)
    _write_log(SANITY_LOG, [
        "n=1..7 archive sanity-check log",
        "=" * 60,
        f"Timestamp: {timestamp}",
        f"Total wall: {sanity_wall_total:.1f}s",
        f"Source:    {sanity_summary['source']}",
        f"Method:    {sanity_summary['method']}",
        "",
        *[f"  n={r['n']}: [{r['status']}] {r['detail']} "
          f"[wall {r['wall_seconds']:.1f}s, "
          f"checked {r.get('pieces_checked', 0)} pieces]"
          for r in sanity_records],
        "",
        f"VERDICT: {'ALL PASS' if all_sanity_ok else 'AT LEAST ONE FAILED'}",
    ])

    if not all_sanity_ok:
        print()
        print("ABORTING n=8 confirmation: sanity check failed on n=1..7.")
        print("This means the archived placement format is incompatible "
              "with the current verifier; the n=8 verdict would be "
              "untrustworthy. See:", SANITY_JSON)
        return 1

    # ------------------------------------------------------------------
    # Phase 2: n=8 confirmation
    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("PHASE 2: n=8 confirmation (the actual question)")
    print("=" * 60)
    e8 = archive["8"]
    size8 = e8.get("size") or e8.get("value")
    cells8 = e8.get("cells") or []
    print(f"  archive n=8: claimed size={size8}, cell_count={len(cells8)}, "
          f"grid={e8.get('grid_size')}")
    print(f"  enumerating 2821 one-sided 8-hexes and checking containment...")
    rec8, wall8 = _verify(archive, 8)
    print(f"  result: {rec8.get('status')} ({wall8:.1f}s)")
    print(f"  detail: {rec8.get('detail')}")

    confirm_summary = {
        "purpose": "Geometric confirmation that the 2026-04-23 archived "
                   "n=8 container of size 26 satisfies the current "
                   "pipeline's verify_method1 contract.",
        "source": "git commit 400bdee6^ (archived solver-results.json), "
                  "recovered to .tmp_archived_results.json",
        "method": "verify_method1.verify_n (pure-Python BFS enumeration "
                  "of all 2821 one-sided 8-hexes via A006535, "
                  "set-inclusion containment under rotation + translation)",
        "timestamp": timestamp,
        "per_term_timeout_s": PER_TERM_TIMEOUT_S,
        "wall_seconds": wall8,
        "n": 8,
        "claimed_size": size8,
        "result": {"n": 8, "wall_seconds": wall8, **rec8},
        "verdict": ("CONFIRMED a(8) <= 26 (geometric containment of all "
                    "2821 pieces; upper bound only)") if rec8.get("ok") else
                   ("NOT CONFIRMED: " + rec8.get("detail", "see record")),
    }
    _write_json(CONFIRM_JSON, confirm_summary)
    _write_log(CONFIRM_LOG, [
        "n=8 archive confirmation log",
        "=" * 60,
        f"Timestamp: {timestamp}",
        f"Wall time: {wall8:.1f}s",
        f"Source:    {confirm_summary['source']}",
        f"Method:    {confirm_summary['method']}",
        "",
        f"Archive claim: a(8) = {size8}, container has {len(cells8)} cells",
        f"verify_method1 status: {rec8.get('status')}",
        f"Detail:        {rec8.get('detail')}",
        f"Pieces checked: {rec8.get('pieces_checked', 0)}/2821",
        "",
        f"VERDICT: {confirm_summary['verdict']}",
        "",
        "NOTE: This script confirms ONLY that 26 is geometrically "
        "achievable, giving the UPPER bound a(8) <= 26. It does NOT "
        "prove a(8) >= 26 (the matching LOWER bound); that would "
        "require the UNSAT@25 SAT proof. The upper bound alone is "
        "sufficient to disambiguate from sequences predicting "
        "a(8) = 28 (A293239 etc.), since 26 < 28.",
    ])

    print()
    print("=" * 60)
    print(f"SANITY (n=1..7): {'ALL PASS' if all_sanity_ok else 'FAILED'}")
    print(f"  -> {SANITY_JSON}")
    print(f"CONFIRMATION (n=8): {confirm_summary['verdict']}")
    print(f"  -> {CONFIRM_JSON}")
    return 0 if rec8.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
