# DRAT / LRAT certificates

Each file `nN_kK.cnf` encodes the UNSAT decision "no container of size K exists for one-sided N-hexes inside the (N+1) x (N+1) axial rectangle". The matching `.drat` (or `.lrat`) file is the proof artifact; the `.sidecar.json` records SHA-256 hashes and the machine verdict from drat-trim or lrat-check.

## Files in this directory

- `n1_k0.{cnf,drat,sidecar.json}` .. `n6_k14.{cnf,drat,sidecar.json}` -- full DRAT proofs, verdict `s DERIVATION` from drat-trim.
- `n7_k20.cnf` + `n7_k20.sidecar.json` -- LRAT verdict `c VERIFIED` from lrat-check. The raw proofs are not committed (see below).
- `nN_witness.json` -- optimal-container witness cells at size a(N).

## Why n7_k20.drat and n7_k20.lrat are not in the repo

Per the paper, the binary DRAT for n = 7 is 1.1 GB and the LRAT re-emission is 3.2 GB. Both exceed GitHub's 100 MB per-file hard limit. The `n7_k20.sidecar.json` records the SHA-256 of the LRAT file and the `c VERIFIED` verdict; the proofs can be regenerated from `n7_k20.cnf` as shown in the root `README.md` ("Reproducing the proof"), reproducing the same SHA-256 modulo cadical build.
