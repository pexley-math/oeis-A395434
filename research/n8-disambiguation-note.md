# A395434 n=8 disambiguation note

**Date:** 2026-04-25
**Reviewer query (Sean A. Irvine, 2026-04-25):** the 7-term submission
prefix `1, 2, 4, 7, 11, 15, 21` matches four existing OEIS sequences
(A293239, A261878, A261993, A299251), all of which extend the prefix
with `a(8) = 28`. Reviewer asked whether A395434 differs from these,
which would require an independently determined a(8).

## Result

**A395434(8) <= 26.** Each of A293239, A261878, A261993, A299251
predicts 28 at the index aligned with A395434(8) -- verified
first-hand from each sequence's OEIS b-file (no summary, no
paraphrase, no external trust): see
`research/matcher-bfiles/AUDIT.md` for the per-matcher offset
alignment and the predicted value at the matching index.

26 < 28, so A395434 differs from all four at index 8.

## Evidence

A 26-cell connected polyhex container that contains all 2,821 one-sided
8-hexes was found on 2026-04-23 and archived in
`.tmp_archived_results.json` (recovered from git commit `400bdee6^`).

On 2026-04-25 this container was independently re-verified by
`verify_method1.verify_n` -- a disjoint geometric verifier that:
- Enumerates all 2,821 one-sided 8-hexes by pure-Python BFS over hex
  axial coordinates, quotienting by the 6 rotations only (no
  reflections), with the count cross-checked against A006535(8) = 2821.
- Checks that each piece fits inside the 26-cell container under at
  least one of the 6 rotations + every translation.
- Checks that the 26 cells form a single edge-connected component on
  the hex lattice.

Verdict: **PASS** (1.1 seconds wall, all 2,821 pieces contained,
container connected). See:
- `research/n8-archive-confirmation-results.json`
- `research/n8-archive-confirmation-log.txt`

The verifier's PASS proves that a valid 26-cell container exists.
By definition `a(n) = min { |C| : C is a connected polyhex containing
every one-sided n-hex }`, so the existence of any valid container of
size k is an UPPER bound `a(n) <= k`. Hence `a(8) <= 26`.

## Why this is sufficient (no SAT proof needed)

We need to show `A395434(8) != 28`. Since `a(8) <= 26 < 28`, this holds
trivially.

The matching LOWER bound (i.e. the exact value of a(8), proving
`a(8) >= 26`) would require an UNSAT@25 SAT proof on the wider-window
encoding (estimated multi-hour to multi-day at the current encoding
scale). That proof is **not needed** for the reviewer's disambiguation
question and is deferred.

## Sanity (n=1..7)

To confirm the verifier and the archive format are mutually consistent,
the same `verify_method1.verify_n` was run on n=1..7 from the same
archive: all PASS (`research/n1-7-archive-sanity-results.json`). The
verifier reproduces the published prefix `1, 2, 4, 7, 11, 15, 21`,
which rules out a malformed archive or a verifier-vs-archive contract
mismatch as alternative explanations of the n=8 PASS.

## Reproducibility

```
python oeis-a395434/code/confirm_n8_from_archive.py
```

Reads the archived placement, runs verify_method1 sanity on n=1..7
plus confirmation on n=8, writes both result JSONs and logs.
Deterministic. ~1.5 seconds wall in total.

## Suggested submission text

> a(8) <= 26 from a 26-cell connected one-sided polyhex container that
> contains all 2,821 one-sided 8-hexes; container verified by
> independent geometric enumeration. This rules out the candidate
> matches A293239, A261878, A261993, A299251, all of which predict
> a(8) = 28.
