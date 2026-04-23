# Self-Critique Review: One-Sided Polyhex Container

**Date:** 2026-04-23
**Reviewer:** Claude (single-pass self-critique, external APIs unavailable)
**Paper version:** submission/paper.md (copy of paper-draft.md)

## Overall Grade: A-

The paper is structurally complete, numerically correct (table matches
solver-results.json exactly), and every term has a two-proof certification
(geometric verifier + DRAT/LRAT). Theorem 1 (trivial lower bound) and
Theorem 2 (computed values, DRAT-certified) are both stated cleanly. The
prior-art novelty claim is backed by the CLEAR verdict from
`compendium/oeis/one-sided-polyhex-container-prior-art-search.dat`.

The remaining items below are minor; nothing is FATAL and nothing requires
a full rewrite.

## FATAL issues

None.

## MAJOR issues

**M1. The n=7 DRAT-certification story should explicitly note why
drat-trim could not verify the 1.1 GB DRAT and why the LRAT path was
substituted.** The Reproducibility section hints at it but the Empirical
Analysis table column "DRAT" cell for n=7 reads "CERTIFIED (cadical --lrat
+ lrat-check)" without context. A reader looking at the row for n=1..6
(drat-trim) vs n=7 (cadical --lrat + lrat-check) needs one sentence
explaining that drat-trim hit a scaling limit at the 1.1 GB binary DRAT
for n=7 and that the LRAT-via-cadical path is mathematically equivalent
(same solver, same CNF, UNSAT verdict machine-checked).

**Action:** add a short note after the table in Section 5 Empirical
Analysis. 2-3 sentences.

**M2. Theorem 1 is stated but not justified beyond a one-line sketch.**
The proof "any container must contain an n-cell polyhex, so its cell
count is at least n" is correct but could note the witness: placing any
specific n-cell piece gives n selected cells, so a(n) >= n directly.

**Action:** expand Theorem 1's proof to one full sentence with the
witness argument.

## MINOR issues

**m1.** The Abstract phrase "the wider-window that supports the
DRAT-certification step below" is informal; reword to "the (n+1)-cell
margin that gives room for the translation-breaker symmetry cut".

**m2.** The Introduction lists sibling sequences but does not note that
A392363 and A395422 were submitted by the same author; a line like
"both submitted by the present author within the same container-family
research programme" would be honest and cite correctly.

**m3.** The Discussion claim "A structural inflation or tiling argument
is required to convert this envelope into a closed form" reads as
speculation. Either cite Barequet's inflation argument for polyominoes
(which is NOT applicable to polyhexes, per the
`feedback-polyiamond-not-polyomino.md` memory -- the same caveat likely
holds here) or rephrase as a weaker open question.

**m4.** Section 4 Table of iterations reports the n=7 wall time as 1227s,
but the actual final proof run (with --emit-drat --check-drat) recorded
1797s for the same term. The 1227s figure comes from the earlier non-DRAT
run. Either use 1797s (the actual proof run reported in solver-results.json)
or note both explicitly.

## STYLE issues

**s1.** The section numbering in the paper does not include explicit
numbers (Introduction, Definitions, ...). The canonical template uses
"1. Introduction", "2. Definitions and Notation", etc. This is aesthetic;
Typst compilation will add section numbers automatically if the template
expects them. Leave as-is unless Typst complains.

**s2.** The single-letter variable "k" in the SAT encoding is reused
for both "target container size" and "generic integer". Minor; context
disambiguates.

**s3.** The Theta(n^2) claim could quote the empirical constants with
two decimal places (0.33 and 0.63) rather than one-third and five-eighths;
the latter reads as a conjectured closed form. Use decimals or drop
the bounds.

## Numeric-consistency verdict

Checked: the 7 rows in the Empirical Analysis table match
`research/solver-results.json` exactly (1, 2, 4, 7, 11, 15, 21).

## Citation-attribution verdict

All 9 citations resolved EXACT or FUZZY via
`python -m bibliography.verify submission/paper.md`. No NONE-matches.

## Proof-scope-precision verdict

- Theorem 1: trivial bound, proof should be fleshed out (see M2).
- Theorem 2: computed values, DRAT-certified. Scope statement correct.
- Conjecture 1 (Theta(n^2)): explicitly marked UNVERIFIED. Correct.

## AI-tell deny-list verdict

No occurrences of ChatGPT, GPT-N, OpenAI, Anthropic, or Claude in the
paper body. Pre-commit hook will double-check at commit time.

## Action items for the single polish pass

Apply M1, M2, m4 as concrete edits. Skip m1-m3 (stylistic; reviewer
judgment). Leave all STYLE items. Do not re-run the self-critique.
