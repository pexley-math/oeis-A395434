"""Generate publication and understanding figures for new-fixed-polyomino-container.

Reads research/solver-results.json and produces:
  submission/oeis-a395434-figures.typ -- one binary
    container figure per proved n, ready to compile to PDF.
  research/oeis-a395434-understanding.typ -- the same
    set with extra annotation captions for personal review.

Usage:
    python code/generate-figures.py [PROJECT_DIR]
    (PROJECT_DIR defaults to the project this file lives in.)
"""

import json
import os
import sys

# Make sure the shared paper-project root is importable for the figure
# generation library, mirroring the verifiers' import shim.
_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from figure_gen_utils.document_builder import DocumentBuilder


SEQUENCE_NAME = "oeis-a395434"
TITLE = "Smallest polyomino containing all FIXED $n$-ominoes (square grid)"
DESCRIPTION = (
    "Minimum cells in a connected polyomino on the square grid that "
    "contains every fixed $n$-omino as a translated subregion."
)


def _shifted(cells_list):
    """Translate cells so the bounding-box origin is (0, 0). Returns
    the shifted set plus the bbox dimensions (rows, cols).
    """
    pairs = [(c[0], c[1]) for c in cells_list]
    if not pairs:
        return set(), 1, 1
    min_r = min(r for r, _ in pairs)
    min_c = min(c for _, c in pairs)
    max_r = max(r for r, _ in pairs)
    max_c = max(c for _, c in pairs)
    rows = max_r - min_r + 1
    cols = max_c - min_c + 1
    shifted = {(r - min_r, c - min_c) for r, c in pairs}
    return shifted, rows, cols


def _proved_terms(results):
    out = []
    for k, v in results.items():
        if not k.isdigit() or not isinstance(v, dict):
            continue
        if v.get("status") != "PROVED":
            continue
        out.append((int(k), v))
    out.sort(key=lambda kv: kv[0])
    return out


def _sequence_line(terms):
    bits = [f"$a({n}) = {v.get('value')}$" for n, v in terms]
    return ", ".join(bits)


def _build_publication_doc(terms):
    doc = DocumentBuilder(
        title=TITLE,
        description=DESCRIPTION,
        sequence_line=_sequence_line(terms),
        author="Peter Exley",
        date="April 2026",
    )
    doc.set_binary_legend(["Container cell"], ["#1ABC9C"])
    for n, v in terms:
        cells, rows, cols = _shifted(v.get("cells") or [])
        method = (
            "SAT + CEGAR connectivity (Glucose42 via PySAT); "
            "two-verifier cross-check (geometric + Glucose42 SAT)."
        )
        doc.add_binary_figure(
            cells=cells,
            bbox_rows=rows,
            bbox_cols=cols,
            n=n,
            k=v.get("value"),
            status=v.get("status", "PROVED"),
            method=method,
            mode="container",
        )
    return doc


def _build_understanding_doc(terms):
    """Same figures as publication, but with annotated detail text that
    spells out the SAT-derivation lineage for each term."""
    doc = DocumentBuilder(
        title=TITLE + " -- Understanding",
        description=DESCRIPTION,
        sequence_line=_sequence_line(terms),
        author="Peter Exley",
        date="April 2026",
    )
    doc.set_binary_legend(["Container cell"], ["#1ABC9C"])
    for n, v in terms:
        cells, rows, cols = _shifted(v.get("cells") or [])
        elapsed = v.get("elapsed", 0.0)
        a_val = v.get("value")
        bbox_label = f"{rows} x {cols}"
        detail = (
            f"n = {n}, a({n}) = {a_val}. Bounding box {bbox_label} on the "
            f"square grid. Solver wall time: {elapsed:.1f} s. "
            f"Status: {v.get('status', 'PROVED')}. Independent geometric "
            f"verifier confirms containment of all fixed {n}-ominoes."
        )
        doc.add_binary_figure(
            cells=cells,
            bbox_rows=rows,
            bbox_cols=cols,
            n=n,
            k=a_val,
            status=v.get("status", "PROVED"),
            mode="container",
            detail_text=detail,
        )
    return doc


def main(argv):
    if len(argv) >= 2:
        project_dir = os.path.abspath(argv[1])
    else:
        project_dir = os.path.abspath(os.path.join(_HERE, ".."))

    results_path = os.path.join(project_dir, "research", "solver-results.json")
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    terms = _proved_terms(results)
    if not terms:
        print("No PROVED terms in solver-results.json", file=sys.stderr)
        return 1

    pub_path = os.path.join(
        project_dir, "submission", f"{SEQUENCE_NAME}-figures.typ"
    )
    und_path = os.path.join(
        project_dir, "research", f"{SEQUENCE_NAME}-understanding.typ"
    )

    pub = _build_publication_doc(terms)
    pub.generate(pub_path)
    und = _build_understanding_doc(terms)
    und.generate(und_path)

    print(f"Wrote {pub_path}")
    print(f"Wrote {und_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
