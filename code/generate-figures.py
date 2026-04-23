"""
Generate publication figures and a personal understanding diagram for
oeis-new-one-sided-polyhex-container.

Reads research/solver-results.json and produces:
- submission/one-sided-polyhex-container-figures.typ (+ .pdf)
- research/one-sided-polyhex-container-understanding.typ (+ .pdf)

Single-state binary rendering: every cell of the optimal container is
filled uniformly in teal on the hex grid.
"""

import json
import sys
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJ_ROOT))

from figure_gen_utils.document_builder import DocumentBuilder
from figure_gen_utils.grid_hex import hex_figure_typst

PROJ_DIR = Path(__file__).resolve().parent.parent

CONTAINER_COLOR = "#1ABC9C"   # teal


def load_results():
    path = PROJ_DIR / "research" / "solver-results.json"
    return json.loads(path.read_text())


def compute_bbox(cells):
    """Return 'R x C' from axial (q, r) cells."""
    rs = [q for q, _ in cells]
    cs = [r for _, r in cells]
    return f"{max(rs) - min(rs) + 1} x {max(cs) - min(cs) + 1}"


def proved_terms(results):
    """Return list of (n, entry) for n where status == 'PROVED', sorted by n."""
    out = []
    for k in sorted(results, key=lambda x: int(x) if x.isdigit() else 10**9):
        if not k.isdigit():
            continue
        entry = results[k]
        if isinstance(entry, dict) and entry.get("status") == "PROVED":
            out.append((int(k), entry))
    return out


def generate_publication_figures(results):
    terms = proved_terms(results)
    ns = [n for n, _ in terms]
    seq_str = ", ".join(str(e["value"]) for _, e in terms)

    doc = DocumentBuilder(
        title="Minimum Polyhex Containing All One-Sided n-Hexes",
        description=(
            "$a(n)$ = minimum number of hexagonal cells in an "
            "edge-connected polyhex that contains, under some rotation "
            "and translation, every one-sided $n$-hex. Pieces are "
            "equivalent up to rotation only (reflections are distinct)."
        ),
        sequence_line=f"$a(1..{len(ns)}) = {seq_str}$",
    )

    for n, entry in terms:
        a_n = entry["value"]
        cells = [tuple(c) for c in entry["cells"]]
        bbox = compute_bbox(cells)
        pieces = entry.get("num_pieces", "?")
        elapsed_raw = entry.get("elapsed", "?")
        elapsed = (f"{elapsed_raw:.1f}"
                   if isinstance(elapsed_raw, (int, float))
                   else str(elapsed_raw))
        detail_text = (
            f"{a_n} cells, {pieces} one-sided $n$-hexes, "
            f"bbox {bbox}, solved in {elapsed}s"
        )
        doc.add_hex_figure(
            cells=cells,
            n=n,
            k=a_n,
            status="PROVED",
            method="SAT + CEGAR + DRAT/LRAT certified",
            fill_color=CONTAINER_COLOR,
            detail_text=detail_text,
        )

    out_typ = PROJ_DIR / "submission" / "one-sided-polyhex-container-figures.typ"
    out_typ.parent.mkdir(parents=True, exist_ok=True)
    doc.generate(str(out_typ))
    print(f"Generated: {out_typ}")

    out_pdf = PROJ_DIR / "submission" / "one-sided-polyhex-container-figures.pdf"
    try:
        doc.compile(pdf_path=str(out_pdf))
        print(f"Compiled: {out_pdf}")
    except Exception as e:
        print(f"Typst compile failed: {e}")
        print("  (.typ source saved; compile manually)")


def generate_understanding_figure(results):
    terms = proved_terms(results)
    if not terms:
        print("No proved terms; skipping understanding figure.")
        return
    n, entry = terms[-1]
    a_n = entry["value"]
    container = [tuple(c) for c in entry["cells"]]
    num_pieces = entry.get("num_pieces", "?")
    bbox = compute_bbox(container)
    ns_available = [k for k, _ in terms]
    a006535_vals = {1: 1, 2: 1, 3: 3, 4: 10, 5: 33, 6: 147,
                    7: 620, 8: 2821, 9: 12942, 10: 60639}
    a006535_str = ", ".join(str(a006535_vals[k])
                            for k in ns_available if k in a006535_vals)
    seq_str = ", ".join(str(e["value"]) for _, e in terms)

    body, w_cm, h_cm = hex_figure_typst(container, fill_color=CONTAINER_COLOR)

    parts = []
    parts.append('#set page(paper: "a4", margin: 1.5cm)')
    parts.append('#set text(font: "New Computer Modern", size: 10pt)')
    parts.append("")
    parts.append("#align(center)[")
    parts.append(f'  #text(size: 14pt, weight: "bold")'
                 f'[What does $a({n}) = {a_n}$ mean?]')
    parts.append("  #v(0.3em)")
    parts.append(f'  #text(size: 10pt)[This {a_n}-cell connected polyhex '
                 f"contains every one-sided {n}-cell polyhex "
                 f"({num_pieces} shapes) under some rotation + translation]")
    parts.append("]")
    parts.append("#v(0.8em)")
    parts.append("#align(center)[")
    parts.append(body)
    parts.append("]")
    parts.append("#v(0.8em)")
    parts.append("#text(size: 10pt)[")
    parts.append(f"*The idea.* Every one of the {num_pieces} one-sided "
                 f"{n}-cell polyhexes (rotations identified, reflections "
                 f"distinct) can be placed, under some rotation and "
                 f"translation, somewhere inside the teal region above. "
                 f"The bounding box of the container is {bbox}, fitting "
                 f"inside the $(n+1) times (n+1)$ search rectangle "
                 f"$={n+1} times {n+1}$.")
    parts.append("]")
    parts.append("#v(0.5em)")
    parts.append("#text(size: 10pt)[")
    parts.append(f"*Piece count.* The one-sided polyhex count "
                 f'(OEIS A006535) is ${a006535_str}$ for $n = 1$ '
                 f"through ${n}$. At $n = {n}$, the container holds "
                 f"{num_pieces} distinct shapes in just {a_n} cells by "
                 f"overlap -- most piece placements share cells with "
                 f"other placements.")
    parts.append("]")
    parts.append("#v(0.5em)")
    parts.append("#text(size: 10pt)[")
    parts.append(f"*How it was proved.* For each $n = 1, ..., {n}$, a "
                 f"SAT solver (cadical) with CEGAR connectivity search "
                 f"descended $k -> k - 1$ within the $(n+1) times (n+1)$ "
                 f"axial rectangle until producing a model of size $a(n)$ "
                 f"and an UNSAT certificate at $a(n) - 1$. Each value is "
                 f"cross-checked by an independent pure-Python geometric "
                 f"verifier (disjoint code path from the solver) AND a "
                 f"machine-verified DRAT or LRAT proof (drat-trim for "
                 f"$n = 1..6$, cadical-`--lrat` + lrat-check for $n = 7$). "
                 f"All three stacks agree on $n = 1..{n}$.")
    parts.append("]")
    parts.append("#v(0.5em)")
    parts.append("#text(size: 10pt)[")
    parts.append(f"*Sequence so far.* $a(1..{len(ns_available)}) = "
                 f"{seq_str}$. No closed-form or small-coefficient "
                 f"recurrence matches all seven values; the observed "
                 f"growth is polynomial of order 2 with "
                 f"$n^2 \\/ 3 <= a(n) <= 5n^2 \\/ 8$ empirically for "
                 f"$n <= {n}$ (UNVERIFIED as a general bound).")
    parts.append("]")

    typ_path = (PROJ_DIR / "research"
                / "one-sided-polyhex-container-understanding.typ")
    typ_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Generated: {typ_path}")

    pdf_path = typ_path.with_suffix(".pdf")
    import subprocess
    try:
        subprocess.run(
            ["typst", "compile", str(typ_path), str(pdf_path)],
            check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        print(f"Compiled: {pdf_path}")
    except Exception as e:
        print(f"Typst compile failed for understanding: {e}")


def main():
    results = load_results()
    generate_publication_figures(results)
    generate_understanding_figure(results)


if __name__ == "__main__":
    main()
