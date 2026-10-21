#!/usr/bin/env python3
"""Every pubfig chart form on one 183 mm page, from seeded synthetic data (watermarked as such).

    python examples/gallery.py [--outdir examples]   # -> examples/gallery.{svg,pdf,png}

The page must pass pubfig's layout check, so it doubles as a regression test (tests/test_gallery.py).
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

import pubfig as pf

R = np.random.default_rng(7)


def heatmap_panel(ax):
    m = R.uniform(0, 1, (4, 5))
    m /= m.sum(1, keepdims=True)
    pf.heatmap(ax, m, ["Beetle", "Fly", "Carcass", "Soil"], ["Beetle", "Fly", "Carcass", "Soil", "Unknown"],
               norm=Normalize(0, 1), cbar_ax=True, cbar_ticks=[0, 0.5, 1], cbar_label="Mean proportion")
    ax.set_title("Heatmap: leave-one-out")


def stacked_panel(ax):
    f = R.dirichlet([4, 2, 2, 0.5, 1], 24)
    colours = pf.CATEGORICAL_STACK + [pf.PH]
    names = ["Beetle", "Fly", "Carcass", "Soil", "Unknown"]
    pf.stacked_bars(ax, f, colours, names)
    ax.set_xticks([])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Proportion")
    ax.set_title("Stacked bars: sources")
    ax.legend(ncols=3, loc="upper center", bbox_to_anchor=(0.5, -0.04), handlelength=0.8, columnspacing=0.8)


def diverging_panel(ax):
    pf.diverging_counts(ax, ["Genera", "KEGG KOs", "Proteins"], [140, 109, 62], [203, 169, 35], [628, 1256, 900])
    ax.set_xlabel("Credible features (%)")
    ax.set_title("Diverging counts: credible")


def interval_panel(ax):
    rows = ["Metadata", "Genera", "Proteins", "Both"]
    for i, (m, sd) in enumerate([(0.32, 0.05), (0.43, 0.06), (0.41, 0.2), (-0.9, 0.3)]):
        pf.interval_point(ax, m, i, sd, sd, pf.CATEGORICAL[i % 3], (-0.5, 0.7))
    ax.set_yticks(range(4), rows)
    ax.set_ylim(3.6, -0.6)
    ax.axvline(0, color=pf.GRID, lw=0.5, zorder=0)
    ax.set_xlabel("Held-out R² (mean ± s.d.)")
    ax.set_title("Interval: off-axis arrows")


def strip_panel(ax):
    for i, c in enumerate(pf.CATEGORICAL):
        v = R.normal(0.3 + 0.05 * i, 0.04, 5)
        pf.strip_mean(ax, i, v, c)
        pf.strip_mean(ax, i + 3.5, v - 0.25, c, filled=False)
    ax.set_xticks([1, 4.5], ["As measured", "Region removed"])
    ax.tick_params(axis="x", length=0)
    ax.axhline(0, color=pf.GRID, lw=0.5, zorder=0)
    ax.set_ylim(-0.1, 0.5)
    ax.set_ylabel("Test R² per split")
    ax.set_title("Strip + mean: CV splits")


def null_panel(ax):
    for i, c in enumerate(pf.CATEGORICAL):
        pf.null_strip(ax, i, R.normal(0, 0.06, 99), 0.25 + 0.03 * i, c, p_y=0.42)
    ax.set_xticks(range(3), ["Genera", "KOs", "Proteins"])
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(-0.25, 0.55)
    ax.set_ylabel("Mean R²")
    ax.set_title("Null strip: vs shuffled")


def agreement_panel(ax):
    x = R.normal(0, 1.5, 400)
    y = x + R.normal(0.3, 0.5, 400)
    pf.agreement(ax, x, y, highlight=np.abs(x) > 2, shift=0.3, label_hi="Credible", label_lo="Other")
    ax.set(xlabel="Effect, relative", ylabel="Effect, absolute")
    ax.legend(loc="upper left", handletextpad=0.1, borderaxespad=0.1, labelspacing=0.2)
    ax.set_title("Agreement: two models")


def ordination_panel(ax):
    groups = np.repeat(["Seawater", "Aquarium", "Mesocosm"], 15)
    centres = {"Seawater": (0, 0), "Aquarium": (2.5, 1), "Mesocosm": (1, -2)}
    xy = np.vstack([R.normal(centres[g], 0.6) for g in groups])
    pf.ordination(ax, xy, groups, dict(zip(centres, pf.CATEGORICAL)), var_pct=(32, 14), head_frac=0.18)
    pf.legend_markers(ax, list(zip(centres, pf.CATEGORICAL)), loc="upper center", ncols=3, columnspacing=0.6,
                      bbox_to_anchor=(0.5, -0.1))
    pf.stat_note(ax, "PERMANOVA $R^2$ = 0.41, " + pf.p_text(0.001), 0.02, 0.98, va="top")
    ax.set_title("Ordination: PCoA")


def hist_panel(ax):
    v = R.normal(0.33, 0.8, 3000)
    cat = np.where(v > 1.2, "up", np.where(v < -0.6, "down", "no"))
    spec = [("down", pf.DIV_NEG, "Below"), ("no", pf.PH, "Includes shift"), ("up", pf.DIV_POS, "Above")]
    pf.category_hist(ax, v, cat, spec, np.arange(-3, 3.6, 0.2), ref_lines=[(0, "No change", True),
                                                                          (0.33, "Median", False)], headroom=1.9)
    ax.set(xlabel="Effect (natural log)", ylabel="Metabolites")
    ax.legend(loc="center right", bbox_to_anchor=(1, 0.62), handlelength=0.8, borderaxespad=0.1)
    ax.set_title("Category histogram: effects")


def volcano_panel(ax):
    eff = R.normal(0, 1, 800)
    q = np.clip(np.exp(-np.abs(eff) * R.uniform(1, 4, 800)), 1e-12, 1)
    names = np.array([f"Gene{i}" for i in range(800)])
    pf.volcano(ax, eff, q, effect_min=1, names=names, n_labels=2)
    ax.set_xlabel("log$_2$ fold change")
    ax.set_title("Volcano: differential")


def box_panel(ax):
    a, b = R.normal(0.5, 0.2, 30), R.normal(0.3, 0.2, 30)
    pf.box_strip(ax, a, 0, pf.CATEGORICAL[0])
    pf.box_strip(ax, b, 1, pf.CATEGORICAL[1])
    ax.set_xticks([0, 1], ["Active", "Advanced"])
    ax.set_ylim(-0.3, 1.5)
    ax.set_yticks([0, 0.5, 1])
    pf.bracket(ax, 0, 1, 1.12, f"{pf.stars(0.004)} {pf.p_text(0.004)}")
    pf.stat_note(ax, "Mann–Whitney", 0.02, 0.98, va="top")
    ax.set_ylabel("Proportion")
    ax.set_title("Box + points: two groups")


def effect_panel(ax):
    names = ["Pseudomonas", "Vibrio", "Bacillus", "Clostridium", "Lactobacillus", "Prevotella"]
    eff = np.array([1.2, 0.8, 0.3, -0.4, -0.9, -1.3])
    sd = np.array([0.3, 0.3, 0.5, 0.5, 0.3, 0.4])
    pf.effect_bars(ax, names, eff, eff - 1.9 * sd, eff + 1.9 * sd, np.abs(eff) > 1.9 * sd)
    ax.set_xlabel("Effect (94% HDI)")
    ax.set_title("Effect bars: per genus")


def sig_panel(ax):
    v = np.array([1, 1, 2, 2, 2, 3, 4, 6, 8, 10, 1, 2, 5])
    p = np.array([0.01, 0.2, 0.03, 0.5, 0.01, np.nan, 0.04, 0.3, 0.01, 0.02, 0.6, 0.01, 0.2])
    x = np.r_[np.zeros(10), np.ones(3)]
    off = np.r_[pf.swarm_offsets(v[:10], log=True), pf.swarm_offsets(v[10:], log=True)]  # per group
    pf.sig_scatter(ax, x + off, v, p, pf.CATEGORICAL[1])
    ax.set_yscale("log")
    ax.set_xticks([0, 1], ["Archaea", "Bacteria"])
    ax.set_xlim(-0.7, 1.7)
    ax.set_ylabel("Samples detected")
    pf.legend_markers(ax, [("$P$ < 0.05", pf.CATEGORICAL[1]), ("$P$ ≥ 0.05", pf.sig_colour(pf.CATEGORICAL[1], 0.5)),
                           ("No $P$", pf.PH)], loc="upper right")
    ax.set_title("Swarm + significance fill")


PANELS = [heatmap_panel, stacked_panel, diverging_panel, interval_panel, strip_panel, null_panel, agreement_panel,
          ordination_panel, hist_panel, volcano_panel, box_panel, effect_panel, sig_panel]


def build():
    fig = plt.figure(figsize=(pf.WIDTH, 232 * pf.MM))
    gs = fig.add_gridspec(5, 3, hspace=0.95, wspace=0.75, left=0.11, right=0.97, top=0.95, bottom=0.05)
    for k, draw in enumerate(PANELS):
        ax = fig.add_subplot(gs[k // 3, k % 3])
        draw(ax)
        pf.label(ax, "abcdefghijklm"[k], dx=-24)
    return fig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=str(Path(__file__).parent))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    fig = build()
    pf.require_layout(fig, force=a.force)
    pf.save(fig, a.outdir, "gallery", watermark_text="pubfig gallery · synthetic example data")
    print(f"wrote {a.outdir}/gallery.(svg|pdf|png)")


if __name__ == "__main__":
    main()
