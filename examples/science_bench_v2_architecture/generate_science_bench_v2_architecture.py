#!/usr/bin/env python3
"""Generate a Nature-style schematic architecture figure for Science Bench V2.

This version follows the `nature-figure` Python track: matplotlib patches,
editable SVG text, restrained colour families, lowercase panel letters, direct
labels, and a schematic-led composite layout.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from textwrap import fill

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path as MplPath


# Mandatory nature-figure rules: editable SVG text and publication font stack.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["svg.hashsalt"] = "science-bench-v2-architecture"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


PALETTE = {
    "ink": "#272727",
    "muted": "#606060",
    "line": "#4D4D4D",
    "hairline": "#C9CDD3",
    "blue": "#0F4D92",
    "blue_mid": "#3775BA",
    "blue_soft": "#DCE9F6",
    "teal": "#42949E",
    "teal_soft": "#DCEFF1",
    "green": "#6FB36F",
    "green_soft": "#E1F1E2",
    "rose": "#B64342",
    "rose_soft": "#F4D8D5",
    "violet": "#7C6CCF",
    "violet_soft": "#E8E4F8",
    "gold": "#C89B2D",
    "gold_soft": "#F4E8CB",
    "grey_soft": "#F2F3F5",
    "white": "#FFFFFF",
}

FIXED_EXPORT_DATE = datetime(2026, 5, 25, tzinfo=timezone.utc)


DISCIPLINES = [
    ("Physics", "20 domains", "one-step probe -> scalar z", PALETTE["blue"], PALETTE["blue_soft"]),
    ("Chemistry", "20 domains", "titration / buffer operations", PALETTE["gold"], PALETTE["gold_soft"]),
    ("Biology", "20 domains", "dose / incubate / response", PALETTE["green"], PALETTE["green_soft"]),
]

RELATIONS = [
    ("I", "initial", "first predictive law", PALETTE["blue"]),
    ("U", "utilize", "extrapolate while keeping prior fit", PALETTE["teal"]),
    ("R", "refine", "same family, tighter parameters", PALETTE["violet"]),
    ("C", "correct", "anomaly falsifies old law", PALETTE["rose"]),
]


def setup_axes(ax: plt.Axes) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def add_panel_label(ax: plt.Axes, label: str, x: float = 0.0, y: float = 1.03) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
        fontweight="bold",
        color=PALETTE["ink"],
    )


def add_title(ax: plt.Axes, title: str) -> None:
    ax.text(
        0.10,
        1.03,
        title,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.5,
        fontweight="bold",
        color=PALETTE["ink"],
    )


def add_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    wh: tuple[float, float],
    title: str,
    body: str = "",
    *,
    fc: str = PALETTE["white"],
    ec: str = PALETTE["line"],
    lw: float = 0.75,
    radius: float = 0.015,
    title_color: str = PALETTE["ink"],
    body_color: str = PALETTE["muted"],
    title_size: float = 7.2,
    body_size: float = 6.1,
    wrap_width: int = 24,
) -> FancyBboxPatch:
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.006,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        mutation_aspect=1,
    )
    ax.add_patch(patch)
    ax.text(
        x + 0.018,
        y + h - 0.035,
        title,
        ha="left",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=title_color,
    )
    if body:
        ax.text(
            x + 0.018,
            y + h - 0.070,
            fill(body, wrap_width),
            ha="left",
            va="top",
            fontsize=body_size,
            color=body_color,
            linespacing=1.25,
        )
    return patch


def add_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = PALETTE["line"],
    lw: float = 0.8,
    rad: float = 0,
    mutation_scale: float = 8,
    linestyle: str = "-",
) -> None:
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=lw,
        color=color,
        shrinkA=2,
        shrinkB=2,
        connectionstyle=f"arc3,rad={rad}",
        linestyle=linestyle,
    )
    ax.add_patch(arrow)


def add_chip(ax: plt.Axes, x: float, y: float, text: str, color: str, width: float = 0.13) -> None:
    patch = FancyBboxPatch(
        (x, y),
        width,
        0.038,
        boxstyle="round,pad=0.003,rounding_size=0.018",
        facecolor=color,
        edgecolor=color,
        linewidth=0.5,
    )
    ax.add_patch(patch)
    ax.text(x + width / 2, y + 0.019, text, ha="center", va="center", fontsize=5.8, color=PALETTE["ink"])


def draw_pipeline(ax: plt.Axes) -> None:
    setup_axes(ax)
    add_panel_label(ax, "a")
    add_title(ax, "Science Bench V2: hidden procedural discovery pipeline")

    # A fine baseline makes this read as a methods schematic instead of a UI card row.
    ax.plot([0.03, 0.97], [0.50, 0.50], color=PALETTE["hairline"], lw=0.7, zorder=0)

    steps = [
        ("Catalogs", "60 domains\n3-5 layers", PALETTE["violet"], PALETTE["violet_soft"]),
        ("Prompts", "catalog fields\n+ relation", PALETTE["teal"], PALETTE["teal_soft"]),
        ("Bench", "hidden probe\nor actions", PALETTE["gold"], PALETTE["gold_soft"]),
        ("Agent", "JSON loop\nchat / reasoner", PALETTE["green"], PALETTE["green_soft"]),
        ("Law", "discovered_law(...)\nPython", PALETTE["rose"], PALETTE["rose_soft"]),
        ("Gate", "32 hold-outs\nmean >=55", PALETTE["blue"], PALETTE["blue_soft"]),
    ]

    xs = [0.07, 0.235, 0.400, 0.565, 0.730, 0.895]
    y = 0.53
    for idx, ((title, body, edge, fill_color), x) in enumerate(zip(steps, xs)):
        add_box(
            ax,
            (x - 0.065, y),
            (0.13, 0.19),
            title,
            body,
            fc=fill_color,
            ec=edge,
            lw=0.85,
            radius=0.012,
            title_color=edge,
            title_size=6.9,
            body_size=5.7,
            wrap_width=16,
        )
        ax.plot([x, x], [0.50, y], color=edge, lw=0.8)
        ax.add_patch(Circle((x, 0.50), 0.009, facecolor=edge, edgecolor="white", linewidth=0.45, zorder=3))
        if idx < len(xs) - 1:
            add_arrow(ax, (x + 0.071, y + 0.095), (xs[idx + 1] - 0.071, y + 0.095), lw=0.75)

    # Discipline lanes are direct labels, not legend boxes.
    lane_y = 0.33
    lane_items = [
        ("physics probe -> z", PALETTE["blue_soft"], 0.07, 0.22),
        ("chemistry titration", PALETTE["gold_soft"], 0.39, 0.20),
        ("biology dose-response", PALETTE["green_soft"], 0.68, 0.23),
    ]
    for label, color, x, w in lane_items:
        add_chip(ax, x, lane_y, label, color, width=w)

    # Cross-layer constraints are drawn as a subtle returning path.
    path_data = [
        (MplPath.MOVETO, (0.895, 0.52)),
        (MplPath.CURVE4, (0.895, 0.20)),
        (MplPath.CURVE4, (0.360, 0.20)),
        (MplPath.CURVE4, (0.360, 0.52)),
    ]
    codes, verts = zip(*path_data)
    feedback = PathPatch(MplPath(verts, codes), facecolor="none", edgecolor=PALETTE["blue"], lw=0.9, alpha=0.9)
    ax.add_patch(feedback)
    add_arrow(ax, (0.366, 0.515), (0.360, 0.535), color=PALETTE["blue"], lw=0.0, mutation_scale=7)
    ax.text(0.60, 0.235, "cross-layer checks: prior fit retention and anomaly correction", ha="center", va="center", fontsize=6.2, color=PALETTE["blue"])


def draw_domain_relation(ax: plt.Axes) -> None:
    setup_axes(ax)
    add_panel_label(ax, "b")
    add_title(ax, "Domains and relation types")

    # Domain composition as a compact horizontal stacked strip.
    x0, y0, h = 0.04, 0.74, 0.15
    widths = [0.29, 0.29, 0.29]
    x = x0
    for (name, count, desc, edge, fill_color), w in zip(DISCIPLINES, widths):
        rect = Rectangle((x, y0), w, h, facecolor=fill_color, edgecolor=edge, linewidth=0.75)
        ax.add_patch(rect)
        ax.text(x + 0.018, y0 + 0.098, name, ha="left", va="center", fontsize=6.8, fontweight="bold", color=edge)
        ax.text(x + 0.018, y0 + 0.052, count, ha="left", va="center", fontsize=6.2, color=PALETTE["ink"])
        x += w

    ax.text(0.04, 0.65, "Experiment forms: physics probe; chemistry titration; biology dose-response", fontsize=5.6, color=PALETTE["muted"])
    ax.text(0.04, 0.595, "Layer chains: IURC, IUC, IURCC", fontsize=6.3, color=PALETTE["ink"], fontweight="bold")

    # Relation map: a sequence of scientific tasks.
    xs = [0.11, 0.34, 0.57, 0.80]
    y = 0.34
    for idx, ((letter, name, desc, color), x) in enumerate(zip(RELATIONS, xs)):
        ax.add_patch(Circle((x, y), 0.045, facecolor=color, edgecolor="white", linewidth=0.8))
        ax.text(x, y + 0.004, letter, ha="center", va="center", fontsize=11, fontweight="bold", color="white")
        ax.text(x, y - 0.082, name, ha="center", va="center", fontsize=6.3, fontweight="bold", color=PALETTE["ink"])
        ax.text(x, y - 0.135, fill(desc, 17), ha="center", va="top", fontsize=5.2, color=PALETTE["muted"], linespacing=1.15)
        if idx < len(xs) - 1:
            add_arrow(ax, (x + 0.052, y), (xs[idx + 1] - 0.052, y), lw=0.75)


def draw_agent_loop(ax: plt.Axes) -> None:
    setup_axes(ax)
    add_panel_label(ax, "c")
    add_title(ax, "Single-layer agent loop")

    cx, cy = 0.50, 0.50
    r = 0.28
    loop = [
        ("read", "task", 100, PALETTE["violet"], PALETTE["violet_soft"]),
        ("experiment", "probe / ops", 25, PALETTE["gold"], PALETTE["gold_soft"]),
        ("observe", "numeric readout", -50, PALETTE["teal"], PALETTE["teal_soft"]),
        ("submit", "Python law", -125, PALETTE["rose"], PALETTE["rose_soft"]),
        ("score", "hidden points", -200, PALETTE["blue"], PALETTE["blue_soft"]),
    ]

    points: list[tuple[float, float]] = []
    for title, body, deg, edge, fill_color in loop:
        import math

        x = cx + r * math.cos(math.radians(deg))
        y = cy + r * math.sin(math.radians(deg))
        points.append((x, y))
        add_box(
            ax,
            (x - 0.085, y - 0.043),
            (0.17, 0.086),
            title,
            body,
            fc=fill_color,
            ec=edge,
            lw=0.75,
            radius=0.012,
            title_color=edge,
            title_size=6.4,
            body_size=5.3,
            wrap_width=14,
        )

    for p1, p2 in zip(points, points[1:] + [points[0]]):
        add_arrow(ax, p1, p2, lw=0.7, rad=0.16, mutation_scale=7)

    ax.add_patch(Circle((cx, cy), 0.105, facecolor=PALETTE["grey_soft"], edgecolor=PALETTE["hairline"], linewidth=0.65))
    ax.text(cx, cy + 0.022, "hypothesis", ha="center", va="center", fontsize=7, fontweight="bold", color=PALETTE["ink"])
    ax.text(cx, cy - 0.022, "update", ha="center", va="center", fontsize=6.2, color=PALETTE["muted"])

    ax.plot([0.09, 0.91], [0.13, 0.13], color=PALETTE["hairline"], lw=0.7)
    ax.text(0.10, 0.080, "physics: <=40 rounds, >=6 probes", fontsize=5.6, color=PALETTE["blue"])
    ax.text(0.10, 0.040, "chem/bio: <=48 rounds, >=8 valid experiments", fontsize=5.6, color=PALETTE["gold"])


def draw_scoring(ax: plt.Axes) -> None:
    setup_axes(ax)
    add_panel_label(ax, "d")
    add_title(ax, "Scoring and seed-0 summary")

    add_box(
        ax,
        (0.03, 0.68),
        (0.45, 0.20),
        "layer conformance",
        "mean of 32 hidden hold-out points; point score decays with relative error",
        fc=PALETTE["blue_soft"],
        ec=PALETTE["blue"],
        title_color=PALETTE["blue"],
        title_size=6.5,
        body_size=5.0,
        wrap_width=26,
    )
    add_box(
        ax,
        (0.52, 0.68),
        (0.45, 0.20),
        "domain composite",
        "0.45 x processScore + 0.55 x finalRuleScore; runner stops at failed gate",
        fc=PALETTE["grey_soft"],
        ec=PALETTE["hairline"],
        title_color=PALETTE["ink"],
        title_size=6.5,
        body_size=5.0,
        wrap_width=26,
    )

    # Minimal bar chart with direct labels.
    chart_left, chart_bottom = 0.10, 0.22
    chart_w, chart_h = 0.78, 0.34
    ax.plot([chart_left, chart_left], [chart_bottom, chart_bottom + chart_h], color=PALETTE["line"], lw=0.6)
    ax.plot([chart_left, chart_left + chart_w], [chart_bottom, chart_bottom], color=PALETTE["line"], lw=0.6)
    for tick in [0, 30, 60]:
        yy = chart_bottom + chart_h * tick / 60
        ax.plot([chart_left - 0.012, chart_left], [yy, yy], color=PALETTE["line"], lw=0.5)
        ax.text(chart_left - 0.025, yy, str(tick), ha="right", va="center", fontsize=5.3, color=PALETTE["muted"])

    bars = [("chat", 0, PALETTE["muted"]), ("reasoner", 31, PALETTE["blue"])]
    for idx, (label, value, color) in enumerate(bars):
        bx = chart_left + 0.22 + idx * 0.24
        bw = 0.105
        bh = chart_h * value / 60
        ax.add_patch(Rectangle((bx, chart_bottom), bw, max(bh, 0.006), facecolor=color, edgecolor=color, linewidth=0.6))
        ax.text(bx + bw / 2, chart_bottom - 0.055, label, ha="center", va="top", fontsize=5.8, color=PALETTE["ink"])
        ax.text(bx + bw / 2, chart_bottom + bh + 0.025, f"{value}/60", ha="center", va="bottom", fontsize=6.1, fontweight="bold", color=color)

    ax.text(0.50, 0.60, "full-chain domains", ha="center", va="center", fontsize=6.5, fontweight="bold", color=PALETTE["ink"])
    ax.text(0.10, 0.100, "reasoner: 13/20 physics; 18/40 chemistry/biology", fontsize=5.7, color=PALETTE["muted"])
    ax.text(0.10, 0.055, "oracle smoke: 4/4 layers passed", fontsize=5.7, color=PALETTE["muted"])


def build_figure() -> plt.Figure:
    fig = plt.figure(figsize=(7.35, 6.20), facecolor="white")
    gs = fig.add_gridspec(
        2,
        3,
        height_ratios=[0.95, 1.0],
        width_ratios=[1.0, 1.0, 1.0],
        left=0.055,
        right=0.985,
        top=0.875,
        bottom=0.075,
        hspace=0.38,
        wspace=0.32,
    )
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])
    ax_d = fig.add_subplot(gs[1, 2])

    fig.text(
        0.055,
        0.955,
        "Science Bench V2 procedural benchmark architecture",
        ha="left",
        va="top",
        fontsize=11.5,
        fontweight="bold",
        color=PALETTE["ink"],
    )
    fig.text(
        0.055,
        0.920,
        "A multi-layer scientific discovery benchmark with hidden simulators, executable laws and cross-layer gates",
        ha="left",
        va="top",
        fontsize=7.1,
        color=PALETTE["muted"],
    )

    draw_pipeline(ax_a)
    draw_domain_relation(ax_b)
    draw_agent_loop(ax_c)
    draw_scoring(ax_d)
    return fig


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    fig = build_figure()
    stem = out_dir / "science_bench_v2_architecture"
    fig.savefig(
        stem.with_suffix(".svg"),
        bbox_inches="tight",
        metadata={
            "Date": FIXED_EXPORT_DATE.isoformat(),
            "Creator": "science_bench_v2_architecture.py",
        },
    )
    fig.savefig(
        stem.with_suffix(".pdf"),
        bbox_inches="tight",
        metadata={
            "CreationDate": FIXED_EXPORT_DATE,
            "ModDate": FIXED_EXPORT_DATE,
            "Creator": "science_bench_v2_architecture.py",
        },
    )
    fig.savefig(stem.with_suffix(".png"), dpi=450, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {stem.with_suffix('.svg')}")
    print(f"Wrote {stem.with_suffix('.pdf')}")
    print(f"Wrote {stem.with_suffix('.png')}")


if __name__ == "__main__":
    main()
