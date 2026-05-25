#!/usr/bin/env python3
"""Generate a Nature-style architecture diagram for Science Bench V2.

The script intentionally uses only the Python standard library so the figure can be
regenerated in lightweight agent environments.  Visual constants mirror the
`nature-figure` skill: editable SVG text, a restrained semantic palette, lowercase
panel labels, and a schematic-led multi-panel layout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from textwrap import wrap


WIDTH = 1800
HEIGHT = 1220

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "gold": "#FFD700",
    "neutral_light": "#EFEFF2",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "neutral_black": "#272727",
    "bg_lilac": "#E0E0F0",
    "bg_aqua": "#E0F0F0",
    "bg_peach": "#F0E0D0",
    "white": "#FFFFFF",
}

FONT_STACK = "Arial, DejaVu Sans, Liberation Sans, sans-serif"


@dataclass
class Svg:
    width: int = WIDTH
    height: int = HEIGHT
    elements: list[str] = field(default_factory=list)

    def add(self, element: str) -> None:
        self.elements.append(element)

    def render(self) -> str:
        defs = f"""
  <defs>
    <marker id="arrow" markerWidth="14" markerHeight="10" refX="12" refY="5"
            orient="auto" markerUnits="strokeWidth">
      <path d="M 0 0 L 14 5 L 0 10 z" fill="{PALETTE['neutral_dark']}"/>
    </marker>
    <marker id="arrow-blue" markerWidth="14" markerHeight="10" refX="12" refY="5"
            orient="auto" markerUnits="strokeWidth">
      <path d="M 0 0 L 14 5 L 0 10 z" fill="{PALETTE['blue_main']}"/>
    </marker>
    <filter id="shadow" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
  </defs>"""
        body = "\n".join(self.elements)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}"
     viewBox="0 0 {self.width} {self.height}" role="img"
     aria-label="Science Bench V2 architecture diagram">
{defs}
  <rect width="100%" height="100%" fill="{PALETTE['white']}"/>
{body}
</svg>
"""

    def save(self, path: Path) -> None:
        path.write_text(self.render(), encoding="utf-8")


def rect(
    svg: Svg,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    stroke: str = "#FFFFFF",
    sw: float = 1.4,
    rx: float = 18,
    opacity: float = 1.0,
    shadow: bool = False,
) -> None:
    filt = ' filter="url(#shadow)"' if shadow else ""
    svg.add(
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:.1f}" '
        f'opacity="{opacity:.3f}"{filt}/>'
    )


def line(
    svg: Svg,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str = PALETTE["neutral_dark"],
    sw: float = 3,
    arrow: bool = True,
    dash: str | None = None,
) -> None:
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    svg.add(
        f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw:.1f}" stroke-linecap="round"{marker}{dash_attr}/>'
    )


def polyline(
    svg: Svg,
    points: list[tuple[float, float]],
    stroke: str = PALETTE["neutral_dark"],
    sw: float = 3,
    arrow: bool = True,
    dash: str | None = None,
) -> None:
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    point_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    svg.add(
        f'  <polyline points="{point_str}" fill="none" stroke="{stroke}" '
        f'stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round"{marker}{dash_attr}/>'
    )


def text(
    svg: Svg,
    x: float,
    y: float,
    value: str,
    size: float = 20,
    fill: str = PALETTE["neutral_black"],
    weight: str = "400",
    anchor: str = "start",
    style: str = "normal",
) -> None:
    svg.add(
        f'  <text x="{x:.1f}" y="{y:.1f}" font-family="{FONT_STACK}" '
        f'font-size="{size:.1f}" font-weight="{weight}" font-style="{style}" '
        f'fill="{fill}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def text_block(
    svg: Svg,
    x: float,
    y: float,
    value: str | list[str],
    max_chars: int = 26,
    size: float = 17,
    fill: str = PALETTE["neutral_black"],
    weight: str = "400",
    anchor: str = "start",
    line_height: float = 1.28,
) -> float:
    lines: list[str] = []
    if isinstance(value, str):
        for part in value.split("\n"):
            wrapped = wrap(part, width=max_chars, break_long_words=False) or [""]
            lines.extend(wrapped)
    else:
        for item in value:
            wrapped = wrap(item, width=max_chars, break_long_words=False) or [""]
            lines.extend(wrapped)
    for idx, item in enumerate(lines):
        text(svg, x, y + idx * size * line_height, item, size=size, fill=fill, weight=weight, anchor=anchor)
    return y + len(lines) * size * line_height


def panel(svg: Svg, label: str, title: str, x: float, y: float, w: float, h: float) -> None:
    rect(svg, x, y, w, h, "#FAFAFC", PALETTE["neutral_light"], sw=1.6, rx=24, shadow=True)
    text(svg, x + 22, y + 38, label, size=28, weight="700")
    text(svg, x + 62, y + 38, title, size=25, weight="700")


def node(
    svg: Svg,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body: str,
    fill: str,
    stroke: str,
    title_color: str | None = None,
    body_size: float = 15.5,
) -> None:
    rect(svg, x, y, w, h, fill, stroke, sw=2.2, rx=18)
    text(svg, x + 18, y + 30, title, size=19, weight="700", fill=title_color or PALETTE["neutral_black"])
    text_block(svg, x + 18, y + 58, body, max_chars=max(18, int(w / 10.5)), size=body_size, fill=PALETTE["neutral_dark"])


def chip(svg: Svg, x: float, y: float, w: float, label: str, fill: str, stroke: str | None = None) -> None:
    rect(svg, x, y, w, 36, fill, stroke or fill, sw=1.0, rx=18)
    text(svg, x + w / 2, y + 24, label, size=15.5, weight="700", anchor="middle", fill=PALETTE["neutral_black"])


def draw_header(svg: Svg) -> None:
    text(svg, 70, 58, "Science Bench V2 procedural benchmark architecture", size=34, weight="700")
    text(
        svg,
        70,
        92,
        "60 domains | hidden simulators | I/U/R/C layered discovery | 32-point hold-out gates",
        size=19,
        fill=PALETTE["neutral_dark"],
    )
    rect(svg, 1340, 38, 380, 58, PALETTE["neutral_light"], "none", rx=20)
    text(svg, 1365, 62, "figure contract", size=14, weight="700", fill=PALETTE["neutral_mid"])
    text(svg, 1365, 84, "schematic-led composite; SVG-first output", size=15, fill=PALETTE["neutral_dark"])


def draw_pipeline_panel(svg: Svg) -> None:
    panel(svg, "a", "End-to-end benchmark pipeline", 60, 125, 1160, 520)

    y = 225
    x0 = 100
    gap = 34
    w = 155
    h = 142
    items = [
        (
            "Domain catalogs",
            "60 fixed domains\nphysics / chemistry / biology\n3-5 layers each",
            PALETTE["bg_lilac"],
            PALETTE["baseline_dark"] if "baseline_dark" in PALETTE else PALETTE["violet"],
        ),
        (
            "Layer prompts",
            "runtime assembly\nrelation: initial, utilize,\nrefine, correct",
            PALETTE["bg_aqua"],
            PALETTE["teal"],
        ),
        (
            "Hidden benches",
            "physics probe -> z\nchem/bio atomic actions\nweak noise by seed",
            PALETTE["bg_peach"],
            PALETTE["gold"],
        ),
        (
            "LLM runner",
            "DeepSeek chat / reasoner\nJSON action loop\nround limits",
            PALETTE["green_1"],
            PALETTE["green_3"],
        ),
        (
            "Law submit",
            "def discovered_law(...)\nexecutable Python\nsame template for utilize",
            PALETTE["red_1"],
            PALETTE["red_strong"],
        ),
        (
            "Evaluation",
            "32 hidden hold-out points\nconformance + cross-layer\nadvance if score >=55",
            "#E8EFF8",
            PALETTE["blue_main"],
        ),
    ]

    centers = []
    for idx, (title, body, fill, stroke) in enumerate(items):
        x = x0 + idx * (w + gap)
        centers.append((x + w / 2, y + h / 2))
        node(svg, x, y, w, h, title, body, fill, stroke, body_size=14.0)
        if idx < len(items) - 1:
            line(svg, x + w + 6, y + h / 2, x + w + gap - 6, y + h / 2, sw=3.2)

    # Cross-layer branch and outputs.
    rect(svg, 172, 448, 880, 118, "#FFFFFF", PALETTE["neutral_light"], sw=1.4, rx=18)
    text(svg, 202, 482, "Layer-to-layer mechanics", size=20, weight="700")
    text_block(
        svg,
        202,
        512,
        [
            "utilize: new law keeps the same template and still fits the previous layer domain",
            "correct: previous law must fail in the anomaly region; new law covers the full range",
        ],
        max_chars=80,
        size=15.5,
        fill=PALETTE["neutral_dark"],
    )
    polyline(svg, [(1055, 296), (1110, 296), (1110, 506), (1055, 506)], stroke=PALETTE["blue_main"], sw=3.5)
    text(svg, 1085, 333, "reports", size=15, weight="700", anchor="middle", fill=PALETTE["blue_main"])
    text(svg, 1085, 357, "scores", size=15, weight="700", anchor="middle", fill=PALETTE["blue_main"])

    # Discipline-specific bench lanes.
    lane_y = 390
    chip(svg, 112, lane_y, 168, "Physics: probe(...)", "#E8EFF8", PALETTE["blue_secondary"])
    chip(svg, 302, lane_y, 194, "Chemistry: add/read", PALETTE["bg_peach"], PALETTE["gold"])
    chip(svg, 518, lane_y, 176, "Biology: dose/read", PALETTE["green_1"], PALETTE["green_3"])
    text(svg, 715, lane_y + 25, "all lanes submit the same object: an executable prediction law", size=15.5)


def draw_domain_panel(svg: Svg) -> None:
    panel(svg, "b", "Domain and relation landscape", 1260, 125, 480, 520)

    cards = [
        ("Physics", "20 domains", "one-step probe -> scalar z", "#E8EFF8", PALETTE["blue_main"]),
        ("Chemistry", "20 domains", "titration / buffer operations", PALETTE["bg_peach"], PALETTE["gold"]),
        ("Biology", "20 domains", "dose / incubate / response", PALETTE["green_1"], PALETTE["green_3"]),
    ]
    for idx, (title, count, body, fill, stroke) in enumerate(cards):
        x = 1300
        y = 205 + idx * 88
        rect(svg, x, y, 400, 66, fill, stroke, sw=2.0, rx=18)
        text(svg, x + 22, y + 29, title, size=20, weight="700")
        text(svg, x + 282, y + 29, count, size=18, weight="700", anchor="middle", fill=stroke)
        text(svg, x + 22, y + 54, body, size=15, fill=PALETTE["neutral_dark"])

    text(svg, 1300, 505, "Layer relation vocabulary", size=19, weight="700")
    relation_x = [1304, 1402, 1500, 1598]
    relation = [
        ("I", "initial", PALETTE["blue_secondary"]),
        ("U", "utilize", PALETTE["teal"]),
        ("R", "refine", PALETTE["violet"]),
        ("C", "correct", PALETTE["red_strong"]),
    ]
    for (letter, label, color), x in zip(relation, relation_x):
        rect(svg, x, 528, 74, 66, color, color, sw=1.0, rx=16)
        text(svg, x + 37, 556, letter, size=24, weight="700", anchor="middle", fill=PALETTE["white"])
        text(svg, x + 37, 580, label, size=12.5, weight="700", anchor="middle", fill=PALETTE["white"])
    text(svg, 1300, 620, "Common chains: IURC, IUC, IURCC", size=15.5, fill=PALETTE["neutral_dark"])


def draw_loop_panel(svg: Svg) -> None:
    panel(svg, "c", "Single-layer agent loop and gate", 60, 690, 820, 430)

    loop_nodes = [
        (130, 780, 160, 74, "Read task", "phenomenon + actions"),
        (360, 780, 160, 74, "Experiment", "probe or atomic ops"),
        (590, 780, 160, 74, "Observation", "scalar / pH / response"),
        (590, 960, 160, 74, "Submit law", "Python function"),
        (360, 960, 160, 74, "Hold-out", "32 hidden points"),
        (130, 960, 160, 74, "Decision", "advance or stop"),
    ]
    for x, y, w, h, title, body in loop_nodes:
        node(svg, x, y, w, h, title, body, "#FFFFFF", PALETTE["neutral_light"], body_size=14.0)

    arrows = [
        ((294, 817), (356, 817)),
        ((524, 817), (586, 817)),
        ((670, 858), (670, 956)),
        ((586, 997), (524, 997)),
        ((356, 997), (294, 997)),
        ((210, 956), (210, 858)),
    ]
    for (x1, y1), (x2, y2) in arrows:
        line(svg, x1, y1, x2, y2, stroke=PALETTE["blue_main"], sw=3.5)

    rect(svg, 323, 872, 244, 62, PALETTE["neutral_light"], "none", rx=20)
    text(svg, 445, 898, "hypothesis update", size=17, weight="700", anchor="middle")
    text(svg, 445, 921, "agent plans next action", size=14.5, anchor="middle", fill=PALETTE["neutral_dark"])

    rect(svg, 105, 1050, 320, 42, "#E8EFF8", PALETTE["blue_secondary"], sw=1.2, rx=18)
    text(svg, 265, 1077, "Physics: <=40 rounds, >=6 probes", size=15, weight="700", anchor="middle")
    rect(svg, 455, 1050, 360, 42, PALETTE["bg_peach"], PALETTE["gold"], sw=1.2, rx=18)
    text(svg, 635, 1077, "Chem/Bio: <=48 rounds, >=8 valid experiments", size=15, weight="700", anchor="middle")


def draw_bar(svg: Svg, x: float, y: float, w: float, h: float, value: float, total: float, color: str, label: str) -> None:
    rect(svg, x, y, w, h, "#FFFFFF", PALETTE["neutral_light"], sw=1.0, rx=12)
    fill_w = w * value / total if total else 0
    if fill_w > 0:
        rect(svg, x, y, fill_w, h, color, color, sw=1.0, rx=12)
    text(svg, x + 12, y + h / 2 + 5, label, size=14.5, weight="700", fill=PALETTE["neutral_black"])
    text(svg, x + w - 12, y + h / 2 + 5, f"{int(value)}/{int(total)}", size=14.5, weight="700", anchor="end")


def draw_scoring_panel(svg: Svg) -> None:
    panel(svg, "d", "Scoring, gates and observed execution", 920, 690, 820, 430)

    rect(svg, 960, 770, 330, 116, "#FFFFFF", PALETTE["neutral_light"], sw=1.4, rx=18)
    text(svg, 982, 804, "Layer conformance", size=19, weight="700")
    text(svg, 982, 835, "pointScore = 100 x exp(-(relErr / th)^2)", size=15.5, fill=PALETTE["neutral_dark"])
    text(svg, 982, 863, "advance gate: mean score >= 55", size=15.5, weight="700", fill=PALETTE["blue_main"])

    rect(svg, 960, 915, 330, 116, "#FFFFFF", PALETTE["neutral_light"], sw=1.4, rx=18)
    text(svg, 982, 949, "Domain composite", size=19, weight="700")
    text(svg, 982, 980, "0.45 x processScore + 0.55 x finalRuleScore", size=15.5, fill=PALETTE["neutral_dark"])
    text(svg, 982, 1008, "runner stops when a layer fails the gate", size=15.5, fill=PALETTE["neutral_dark"])

    # Mini vertical comparison chart.
    chart_x = 1355
    chart_y = 780
    chart_w = 280
    chart_h = 220
    line(svg, chart_x, chart_y + chart_h, chart_x + chart_w, chart_y + chart_h, stroke=PALETTE["neutral_mid"], sw=1.4, arrow=False)
    line(svg, chart_x, chart_y, chart_x, chart_y + chart_h, stroke=PALETTE["neutral_mid"], sw=1.4, arrow=False)
    for tick in [0, 30, 60]:
        yy = chart_y + chart_h - chart_h * tick / 60
        line(svg, chart_x - 6, yy, chart_x, yy, stroke=PALETTE["neutral_mid"], sw=1.2, arrow=False)
        text(svg, chart_x - 12, yy + 5, str(tick), size=12.5, anchor="end", fill=PALETTE["neutral_mid"])

    bars = [("chat", 0, PALETTE["neutral_mid"]), ("reasoner", 31, PALETTE["blue_main"])]
    for idx, (label, value, color) in enumerate(bars):
        bx = chart_x + 60 + idx * 100
        bh = chart_h * value / 60
        rect(svg, bx, chart_y + chart_h - bh, 58, bh if bh > 0 else 2, color, color, sw=1.0, rx=8)
        text(svg, bx + 29, chart_y + chart_h + 26, label, size=14, anchor="middle", fill=PALETTE["neutral_dark"])
        text(svg, bx + 29, chart_y + chart_h - bh - 12, f"{value}/60", size=14, weight="700", anchor="middle", fill=color)
    text(svg, chart_x + chart_w / 2, chart_y - 18, "Full-chain domains", size=18, weight="700", anchor="middle")

    draw_bar(svg, 1350, 1040, 305, 34, 13, 20, PALETTE["blue_secondary"], "Physics reasoner")
    draw_bar(svg, 1350, 1083, 305, 34, 18, 40, PALETTE["teal"], "Chem/Bio reasoner")
    text(svg, 960, 1082, "Oracle smoke: 4/4 layers passed, supporting implementation validity.", size=16, fill=PALETTE["neutral_dark"])


def draw_footer(svg: Svg) -> None:
    text(
        svg,
        70,
        1178,
        "Source synthesis: Science Bench V2 evaluation report (seed 0) and nature-figure design rules; generated as editable SVG.",
        size=14.5,
        fill=PALETTE["neutral_mid"],
    )


def build() -> Svg:
    svg = Svg()
    draw_header(svg)
    draw_pipeline_panel(svg)
    draw_domain_panel(svg)
    draw_loop_panel(svg)
    draw_scoring_panel(svg)
    draw_footer(svg)
    return svg


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "science_bench_v2_architecture.svg"
    build().save(out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
