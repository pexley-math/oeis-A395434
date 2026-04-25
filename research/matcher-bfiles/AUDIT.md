# Matcher b-files: first-hand audit

**Date:** 2026-04-25
**Source:** `https://oeis.org/A<NUM>/b<NUM>.txt` for each of the four
matchers, fetched via `curl` (raw b-files; OEIS canonical sequence
data, not summaries or paraphrases).

## Files

| Sequence | b-file path |
|---|---|
| A293239 | `b293239.txt` |
| A261878 | `b261878.txt` |
| A261993 | `b261993.txt` |
| A299251 | `b299251.txt` |

## Method

For each matcher, locate the contiguous 7-term window in the b-file
that equals A395434(1..7) = `[1, 2, 4, 7, 11, 15, 21]`, then read off
the very next OEIS index. That next-index value is what the matcher
predicts at the alignment that maps to A395434(8).

## Result

```
A261878: A395434(1..7) = b(1..7)  => A395434(8) predicted = b(8)  = 28
A261993: A395434(1..7) = b(1..7)  => A395434(8) predicted = b(8)  = 28
A293239: A395434(1..7) = b(0..6)  => A395434(8) predicted = b(7)  = 28
A299251: A395434(1..7) = b(3..9)  => A395434(8) predicted = b(10) = 28
```

**Every matcher predicts 28 at the index aligned with A395434(8).**

## Disambiguation

A395434(8) <= 26 (proved 1.2 s by `code/confirm_n8.py`).
26 < 28. Therefore A395434(n) differs from each of A293239, A261878,
A261993, A299251 at index 8.

## Trust chain

- The b-files above are bit-identical copies of OEIS canonical data
  retrieved 2026-04-25.
- The verifier `verify_method1.verify_n` is a disjoint geometric
  enumerator (no SAT, no shared imports with the solver) whose piece
  count is cross-checked against A006535(8) = 2,821 from this same
  OEIS authority.
- The audit script that produced the predictions table is the python
  block in this commit message; rerunning it on these b-files is
  deterministic.

No external trust is required to reproduce the disambiguation: the
b-files are saved here, the verifier scripts are in `code/`, and the
26-cell placement is bundled at
`research/2026-04-23-solver-results.json` (originally recovered from
the upstream monorepo at git commit `400bdee6^`).
