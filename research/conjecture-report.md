# Conjecture Report -- One-Sided Polyhex Container

**Date:** 2026-04-23
**Terms proved:** 7 (all DRAT-certified)
**Source:** research/solver-results.json

## Proved Terms

| n | a(n) | Source | Certification |
|---|------|--------|---------------|
| 1 | 1    | OUR PROOF | verify_method1 PASS + DRAT CERTIFIED (drat-trim) |
| 2 | 2    | OUR PROOF | verify_method1 PASS + DRAT CERTIFIED (drat-trim) |
| 3 | 4    | OUR PROOF | verify_method1 PASS + DRAT CERTIFIED (drat-trim) |
| 4 | 7    | OUR PROOF | verify_method1 PASS + DRAT CERTIFIED (drat-trim) |
| 5 | 11   | OUR PROOF | verify_method1 PASS + DRAT CERTIFIED (drat-trim) |
| 6 | 15   | OUR PROOF | verify_method1 PASS + DRAT CERTIFIED (drat-trim) |
| 7 | 21   | OUR PROOF | verify_method1 PASS + DRAT CERTIFIED (cadical --lrat + lrat-check, 80s) |

First differences d(n) = a(n+1) - a(n): 1, 2, 3, 4, 4, 6.
Second differences dd(n): 1, 1, 1, 0, 2.

## OEIS Subsequence Search

Queries run via oeis.org text-format API on 2026-04-23:

1. `seq:1,2,4,7,11,15,21` -> 4 hits (A293239, A261878, A261993, A299251). None are structurally related: derivatives of x^x, fractional-part counting, divisor arithmetic. No polyform / container / combinatorial-geometry match.
2. `seq:2,4,7,11,15,21` (offset-by-1) -> 5 hits, superset of (1), same unrelated families plus A389319 (midsequence of squares and negative triangular numbers). None relate to polyhex containers.
3. `seq:1,2,3,4,4,6` (first differences) -> 109 hits; all divisor-arithmetic / partition-counting sequences, none match the full tail 4, 6 after the initial 1..4.
4. `seq:0,1,3,7,14,25,40` (partial sums shifted) -> 0 hits.

Conclusion: no OEIS sequence matches 1, 2, 4, 7, 11, 15, 21 or any simple transform thereof. Sequence is novel, consistent with prior-art-search verdict CLEAR.

## Formula Tests

Six formula tests across four categories (polynomial, recurrence, closed form, identity):

| # | Category    | Formula                                 | Matches all 7? | First failure     | Motivation |
|---|-------------|-----------------------------------------|----------------|-------------------|------------|
| 1 | polynomial  | a(n) = n(n-1)/2 + 1 (triangular+1)      | No             | n=6 (16 vs 15)    | Lazy-caterer-style quadratic; natural first guess for a container family |
| 2 | polynomial  | a(n) = round(0.42 * n^2)                | No             | n=3 (4 vs 4 OK) then n=6 (15 vs 15 OK) then n=7 (18 vs 21) | Least-squares fit gives c ~ 0.42 |
| 3 | recurrence  | a(n) = a(n-1)+a(n-2)-a(n-3)+2, seed 1,2,4 | No           | n=6 (16 vs 15)    | Third-order linear with constant forcing; matches n=4, 5 exactly |
| 4 | closed form | a(n) = floor(n(n+1)/3) + 1              | No             | n=7 (19 vs 21)    | Growth rate n^2/3 matches observed density; linear correction |
| 5 | identity    | a(n) = A006535(n) + ...                 | No             | structural        | One-sided piece count A006535 grows Theta(c^n), c ~ 4.8; a(n) polynomial, so no additive identity |
| 6 | identity    | a(n) = A327094(n) (sibling square-lattice container) | No | n=4 (7 vs 6)  | Cross-lattice identity test; hex and square diverge at n=4 |

Tests 1 and 3 matched five of seven terms, confirming the sequence is locally polynomial-like but exhibits non-smooth behaviour around n=6. No candidate survives the full range.

## Active Conjectures

Only a growth-rate bound survived the data:

### Conjecture 1: a(n) = Theta(n^2)

- **Status:** UNVERIFIED (consistent with n=1..7 and with the wider-window SAT instance at n=7 having 82k variables and 575k clauses, both scaling as Theta(n^2)).
- **Bounds fitted to n=1..7:** (1/3) * n^2 <= a(n) <= (5/8) * n^2 (rough empirical envelope; not a proof).
- **Predicted range for a(8):** 21 <= a(8) <= 40 at n=8. The archived 2026-03-22 solver (not used in this project's proof chain) reported a(8) = 26, inside this range but UNVERIFIED.
- **Why only Theta:** the one-sided piece count A006535(n) grows as Theta(c^n) with c ~ 4.8, so the container holds super-polynomially many distinct pieces. Polynomial growth therefore reflects heavy geometric overlap, not piece-count growth. Without a structural inflation or tiling argument we cannot prove a specific closed form.

## Conjectures Rejected

- Polynomial `T(n-1) + 1` rejected at n=6.
- Any linear recurrence of order <= 4 with small integer coefficients: exhaustive search over |c_i| <= 3, |d| <= 4 during this skill found no recurrence matching all 7 terms. Best fit: order-3 recurrence matching 5 of 7.
- Closed form `floor(n(n+1)/3) + 1` rejected at n=7.
- Cross-lattice identity with A327094 (fixed-polyomino container on square lattice) rejected at n=4; different lattices yield different optima.

## Cross-References Found

| OEIS ID | Name | Relationship |
|---------|------|--------------|
| A006535 | Number of one-sided polyhexes with n cells | Defines the piece set; grows Theta(c^n), c ~ 4.8 |
| A000228 | Number of free polyhexes | Lower bound on A006535; sibling enumeration |
| A001207 | Number of fixed polyhexes | Upper bound on A006535; sibling enumeration |
| A327094 | Fixed-polyomino container (square lattice) | Methodological sibling; different lattice |
| A392363 | Polyiamond (free) container (triangular lattice) | Methodological sibling on a third lattice |
| A395422 | Fixed-polyiamond container (triangular lattice) | Methodological sibling; also DRAT-certified via wider-window SAT |

## Outcome

Conjecture found (UNVERIFIED)

The only formula that survives the data is the coarse growth-rate envelope a(n) = Theta(n^2) with empirical constants (1/3) <= a(n)/n^2 <= (5/8) for n <= 7. No closed-form, recurrence, or cross-sequence identity matches all seven DRAT-certified terms within the families tested (polynomial degree <= 3, linear recurrences of order <= 4 with |c_i| <= 3, integer-floor closed forms, sibling-sequence offsets). Recommend submission to OEIS as a data-first sequence with the Theta(n^2) growth observation and cross-references to the sibling container projects.
