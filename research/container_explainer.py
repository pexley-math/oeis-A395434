"""Manim animation explaining the container problem for one-sided polyhex
containers (this project).

Cycles through n = 1 .. 4. For each n, draws the optimal container
(a(n) cells in teal) and then highlights each of the A006535(n)
one-sided n-hexes in turn at a valid rotation + translation placement
inside the container. Each piece holds on screen for ~2 seconds.

For n = 5 .. 7 the piece counts grow fast (33, 147, 620), so those
n are shown as a slideshow -- container shape only, held briefly
per n, no per-piece highlighting.

Modelled on research-outputs/paper-project/oeis-a395422/research/container_explainer.py
and uses the same shared helpers plus the new hex-grid primitives in
figure_gen_utils.manim_grids (hex_vertices / make_hex / build_hex_shape_colored).

Run:
    manim -ql container_explainer.py ContainerExplainer
"""

from manim import *
import json
import os
import sys

# Shared library on sys.path (same pattern as A395422)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from figure_gen_utils.manim_grids import (
    hex_center, build_hex_shape_colored,
)
from figure_gen_utils.manim_patterns import bottom_text, snake_walk_order


# ---------------------------------------------------------------------------
# Pure-Python one-sided polyhex enumerator (disjoint from polyform_enum so
# the explainer can be read as a standalone script). Matches verify_method1.
# ---------------------------------------------------------------------------

_HEX_DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]


def _hex_nb(cell):
    q, r = cell
    return [(q + dq, r + dr) for dq, dr in _HEX_DIRS]


def _rot60(cell):
    """60 deg CCW rotation in axial coordinates: (q, r) -> (-r, q + r)."""
    q, r = cell
    return (-r, q + r)


def _normalise(cells):
    mq = min(q for q, _ in cells)
    mr = min(r for q, r in cells if q == mq)
    return frozenset((q - mq, r - mr) for q, r in cells)


def _rotations_of(piece):
    rots = []
    cur = piece
    for _ in range(6):
        cur = frozenset(_rot60(c) for c in cur)
        rots.append(_normalise(cur))
    return rots


def _enumerate_fixed(n):
    if n <= 0:
        return [frozenset()]
    if n == 1:
        return [frozenset({(0, 0)})]
    prev = _enumerate_fixed(n - 1)
    seen = set()
    out = []
    for p in prev:
        for cell in p:
            for nb in _hex_nb(cell):
                if nb in p:
                    continue
                grown = _normalise(p | {nb})
                if grown not in seen:
                    seen.add(grown)
                    out.append(grown)
    return out


def _enumerate_one_sided(n):
    fixed = _enumerate_fixed(n)
    seen_canon = set()
    out = []
    for p in fixed:
        canon = min(sorted(tuple(sorted(r)) for r in _rotations_of(p)))
        if canon not in seen_canon:
            seen_canon.add(canon)
            out.append(frozenset(canon))
    return out


def _find_placement(piece, container_set):
    """Find a rotation + translation of `piece` that fits in container_set.

    Returns a frozenset of the placed cells, or None if the piece does
    not fit. Checks all 6 rotations and all translations whose bounding
    box fits inside the container's bounding box.
    """
    cr_min = min(q for q, _ in container_set)
    cr_max = max(q for q, _ in container_set)
    cc_min = min(r for _, r in container_set)
    cc_max = max(r for _, r in container_set)
    for rot in _rotations_of(piece):
        cells = list(rot)
        pr_min = min(q for q, _ in cells)
        pr_max = max(q for q, _ in cells)
        pc_min = min(r for _, r in cells)
        pc_max = max(r for _, r in cells)
        for dq in range(cr_min - pr_min, cr_max - pr_max + 1):
            for dr in range(cc_min - pc_min, cc_max - pc_max + 1):
                placed = frozenset((q + dq, r + dr) for q, r in cells)
                if placed.issubset(container_set):
                    return placed
    return None


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------

CONTAINER_COLOR = TEAL_C
PIECE_COLOR = RED

BOTTOM_TEXT_Y = -3.2
HOLD_SECONDS = 2.0

# Hex circumradius per n; smaller n gets bigger hexes to fill the frame.
SCALE_FOR_N = {1: 1.2, 2: 1.0, 3: 0.85, 4: 0.65, 5: 0.5, 6: 0.42, 7: 0.38}


class ContainerExplainer(Scene):
    """What does a(n) measure for one-sided polyhex containers?"""

    def construct(self):
        # ---- title ----
        title = Text("What does a(n) measure?", font_size=40, weight=BOLD)
        sub = Text("Smallest polyhex containing all one-sided n-hexes",
                   font_size=22, color=GREY_B, weight=BOLD)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(sub))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(sub))

        # ---- load solver witnesses ----
        results_path = os.path.join(os.path.dirname(__file__),
                                    "solver-results.json")
        with open(results_path) as f:
            results = json.load(f)

        # Full piece cycling for n = 1..4 (piece counts 1, 1, 3, 10 --
        # comfortably short).
        for n in range(1, 5):
            self.show_an(n, results)

        # Slideshow for n = 5..7 (piece counts 33, 147, 620 -- too many
        # to cycle through in a GIF).
        self.slideshow(list(range(5, 8)), results)

        # ---- final card ----
        f1 = Text("a(n) = smallest connected polyhex",
                  font_size=32, weight=BOLD)
        f2 = Text("containing every one-sided n-hex under rotation + translation",
                  font_size=24, weight=BOLD)
        f3 = Text("a(1..7) = 1, 2, 4, 7, 11, 15, 21",
                  font_size=30, color=YELLOW, weight=BOLD)
        fg = VGroup(f1, f2, f3).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(Write(f1), Write(f2))
        self.wait(1)
        self.play(Write(f3))
        self.wait(3)

    def show_an(self, n, results):
        """Show the container for a(n) and cycle through all one-sided n-hexes."""
        a_n = results[str(n)]["value"]
        container_cells = [tuple(c) for c in results[str(n)]["cells"]]
        container_set = set(container_cells)

        pieces = _enumerate_one_sided(n)

        placements = {}
        for p in pieces:
            pl = _find_placement(p, container_set)
            if pl is None:
                raise RuntimeError(
                    f"n={n} piece {sorted(p)} does not fit inside the "
                    f"solver witness container")
            placements[p] = frozenset(pl)
        pieces = snake_walk_order(pieces, lambda p: placements[p])

        s = SCALE_FOR_N.get(n, 0.35)

        header = Text(f"a({n}) = {a_n}",
                      font_size=44, color=YELLOW, weight=BOLD)
        header.to_edge(UP, buff=0.5)

        orbit_map = {qr: 0 for qr in container_cells}
        group, hexes = build_hex_shape_colored(
            container_cells, orbit_map, [CONTAINER_COLOR], s,
        )

        self.play(Write(header), *[FadeIn(h) for h in hexes.values()])

        piece_count = len(pieces)
        intro = bottom_text(
            f"{a_n}-cell container for every one-sided {n}-hex "
            f"({piece_count} shape{'s' if piece_count > 1 else ''})",
            y=BOTTOM_TEXT_Y,
            font_size=22 if n <= 3 else 20,
        )
        self.play(FadeIn(intro))
        self.wait(1.5)

        prev_caption = intro
        for i, piece in enumerate(pieces, 1):
            placed = placements[piece]
            new_color_idx = {qr: 0 for qr in container_cells}
            for qr in placed:
                new_color_idx[qr] = 1
            colors = [CONTAINER_COLOR, PIECE_COLOR]

            anims = []
            for qr, h in hexes.items():
                target = colors[new_color_idx[qr]]
                anims.append(h.animate.set_fill(target, opacity=0.85))

            caption = bottom_text(
                f"Piece {i} of {piece_count}: a {n}-cell one-sided {n}-hex, "
                f"shown in red inside the {a_n}-cell container",
                y=BOTTOM_TEXT_Y, color=GREEN,
                font_size=20 if n <= 3 else 18,
            )
            self.play(*anims,
                      ReplacementTransform(prev_caption, caption),
                      run_time=0.4)
            self.wait(HOLD_SECONDS)
            prev_caption = caption

        final = bottom_text(
            f"All {piece_count} one-sided {n}-hex"
            f"{'es' if piece_count > 1 else ''} fit. a({n}) = {a_n}.",
            y=BOTTOM_TEXT_Y, color=YELLOW,
            font_size=24 if n <= 3 else 20,
        )
        self.play(ReplacementTransform(prev_caption, final))
        self.wait(2)
        self.play(*[FadeOut(m) for m in [header, group, final]])

    def slideshow(self, ns, results):
        """Slideshow of the optimal containers for each n in `ns`.

        No piece highlighting -- just the overall container shape
        per n, a short header + caption, held for ~3 s each.
        """
        intro = Text("Optimal containers for n = 5 .. 7",
                     font_size=34, weight=BOLD)
        sub = Text("(shapes only; one-sided counts A006535(n) grow fast)",
                   font_size=22, color=GREY_B, weight=BOLD)
        sub.next_to(intro, DOWN, buff=0.3)
        self.play(Write(intro), FadeIn(sub))
        self.wait(1.5)
        self.play(FadeOut(intro), FadeOut(sub))

        for n in ns:
            a_n = results[str(n)]["value"]
            container_cells = [tuple(c) for c in results[str(n)]["cells"]]
            num_pieces = results[str(n)].get("num_pieces", "?")

            s = SCALE_FOR_N.get(n, 0.35)
            header = Text(f"a({n}) = {a_n}", font_size=42,
                          color=YELLOW, weight=BOLD)
            header.to_edge(UP, buff=0.5)

            orbit_map = {qr: 0 for qr in container_cells}
            group, hexes = build_hex_shape_colored(
                container_cells, orbit_map, [CONTAINER_COLOR], s,
            )

            caption = bottom_text(
                f"{a_n}-cell container for all {num_pieces} one-sided {n}-hexes",
                y=BOTTOM_TEXT_Y,
                font_size=22 if n <= 5 else 20,
            )

            self.play(Write(header),
                      *[FadeIn(h) for h in hexes.values()],
                      FadeIn(caption),
                      run_time=0.8)
            self.wait(3.0)
            self.play(FadeOut(header), FadeOut(group), FadeOut(caption),
                      run_time=0.4)
