# Validation Report -- oeis-new-one-sided-polyhex-container

**Date:** 2026-04-23
**Pipeline version:** 3.3
**Verdict:** PASS

## Summary

All 11 upstream pipeline skills completed successfully, and the automated gate `validate-complete.py` exits 0 (PASS). The project is DRAFT READY for /publish.

## Proved range

a(1..7) = 1, 2, 4, 7, 11, 15, 21 (7 terms).

Every term certified by two independent proofs:
- **Verifier 1** (geometric set-inclusion, pure Python, disjoint code path): PASS for n = 1..7.
- **DRAT/LRAT** (machine-verified UNSAT proof at k = a(n) - 1): CERTIFIED for n = 1..7
  - drat-trim `s DERIVATION` for n = 1..6
  - cadical `--lrat=true` + lrat-check `c VERIFIED` for n = 7 (binary DRAT exceeded drat-trim's memory budget; LRAT path was used as the stronger, faster alternative)

Solver, verifier 1, and DRAT all reconcile for every n in 1..7.

## Validated artifacts

| Skill | Deliverable | Status |
|-------|-------------|--------|
| 1 project-init        | `base-project.md`, `project-manifest.json`, `pipeline-log.json`, `LICENSE`, `iteration-log.tsv` | OK |
| 2 prior-art-search    | `compendium/oeis/one-sided-polyhex-container-prior-art-search.dat` (VERDICT: CLEAR) | OK |
| 3 solver-design       | `code/solve_one-sided-polyhex-container.py`, `research/design-rationale.md` | OK |
| 4 solver-verify       | `code/verify_method1.py`, `research/verify_method1-results.json`, `research/verification-report.md` (VERDICT: PASS) | OK |
| 5 solver-iterate      | 6 kept iterations across 4 categories + 2 self-critique; `iteration-log.tsv`, `research/solver-results.json`, `research/solver-run-log.txt`, `research/solver-summary-log.txt`, `research/solver-review/claude-selfcritique-20260423.md` | OK |
| 6 conjecture-search   | `research/conjecture-report.md` (Outcome: Conjecture found UNVERIFIED -- Theta(n^2)) | OK |
| 7 paper-draft         | `submission/paper-draft.md` (9 citations all matched against `references.bib`) | OK |
| 8 paper-polish        | `submission/paper.md`, `submission/paper.pdf` (168 KB), `submission/reviews/review-selfcritique.md` (grade A-) | OK |
| 9 figure-generate     | `code/generate-figures.py`, `submission/one-sided-polyhex-container-figures.{typ,pdf}`, `research/one-sided-polyhex-container-understanding.{typ,pdf}` | OK |
| 10 oeis-draft         | `submission/oeis-draft.txt`, `submission/oeis-copy-helper.html`, `README.md` | OK |
| 11 project-validate   | this report + `project-manifest.json` stamped pipeline_version=3.3 + tracker updated | in progress |

## OEIS format checks

- ASCII only: OK
- US English (no "proven", no "colour"): OK
- No AI attribution: OK
- Single (Start)/(End) block in COMMENTS: N/A (new-submission format uses no wrapper per the template)
- DATA section present and cross-checks solver-results.json: OK (7 terms match)
- Author field contains Peter Exley: OK

## Pipeline-level changes landed during this run

- `sat_utils/frameworks/container.py` now guards `lonely_cell_clauses` with `n >= 2` (commit `0edd24c1`). Root-cause fix for an a(1) = 2 correctness break exposed when `use_lonely_cell_clauses=True` was combined with a tight upper bound.
- `/solver-verify` + `/solver-iterate` updated so DRAT certification (from `--emit-drat --check-drat`) replaces the slow Glucose `verify_method2.py` as the second independent proof (commit `f01c06cb`). Skill docs, the block-premature-complete hook, and `validate-verify.py` all updated.
- Skill documentation numbering fixed across 8 skill files to use dense 1..11 indices matching run-pipeline.py and the hook (commit `95aa8b97`).
- Memory: new feedback notes saved at `feedback-absolute-paths-only.md`, `feedback-lonely-cell-n1-guard.md`, `feedback-drat-replaces-method2.md`, plus project note `project-pipeline-heartbeat-logger.md` (deferred future enhancement).

## Next step

Project is DRAFT READY. `/publish` is OPTIONAL -- only invoke when ready to submit to OEIS. Current preference is to park as DRAFT READY pending final review.
