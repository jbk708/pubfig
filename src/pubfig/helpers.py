"""Panel letters, statistics annotations, marks and saving, in the pubfig print style."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import Ellipse

from .style import AREA_ALPHA, DIV_NEG, DIV_POS, DOT, FILL_ALPHA, INK, INK2, MIN_FS, PH

# Jitter for box_strip. Seeded once per process so a script's figures are reproducible run to run.
rng = np.random.default_rng(11)


# ---------------------------------------------------------------- colour
def luminance(rgb):
    """WCAG relative luminance of an RGB(A) tuple in 0-1."""
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb[:3]]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def text_on(rgb):
    """Black ink or white, whichever has the higher WCAG contrast on this fill."""
    L = luminance(rgb)
    white = 1.05 / (L + 0.05)
    black = (L + 0.05) / (luminance((0.043, 0.043, 0.043)) + 0.05)
    return "white" if white > black else INK


# ---------------------------------------------------------------- panel letters and saving
def label(ax, letter, x=None):
    """Bold panel letter at a fixed point offset left of the axes' top-left, on the title baseline."""
    ax.annotate(letter, xy=(0, 1), xycoords="axes fraction", xytext=(-11, 6), textcoords="offset points",
                fontsize=8, fontweight="bold", va="baseline", ha="right", annotation_clip=False)


def watermark(fig, text):
    """Small italic note above the top-right of the figure (e.g. "MOCKUP · synthetic placeholder data")."""
    top = max(a.get_position().y1 for a in fig.axes)
    fig.text(0.995, top + 0.045, text, ha="right", va="bottom", fontsize=5, color="#a3a29e", fontstyle="italic")


def save(fig, out, name, watermark_text=None, formats=("svg", "pdf", "png")):
    """Write out/name.{svg,pdf,png} with a tight bounding box and close the figure."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if watermark_text:
        watermark(fig, watermark_text)
    for ext in formats:
        fig.savefig(out / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- statistics annotation
def stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."


def p_text(p, symbol="P"):
    """'$P$ = 0.002' / '$P$ < 0.001' (exact value to two significant figures); symbol="q" for adjusted."""
    return f"${symbol}$ < 0.001" if p < 0.001 else f"${symbol}$ = {p:.2g}"


def bracket(ax, x0, x1, y, text, leg_pt=2.5):
    """Significance bracket from x0 to x1 at height y (data); legs drop leg_pt points; text centred above.
    Call after the axes limits are final (the legs are sized in display units)."""
    (X0, Y), (X1, _) = ax.transData.transform([(x0, y), (x1, y)])
    d = leg_pt * ax.figure.dpi / 72
    pts = ax.transData.inverted().transform([(X0, Y - d), (X0, Y), (X1, Y), (X1, Y - d)])
    ax.plot(*pts.T, color=INK2, lw=0.5, solid_capstyle="butt", clip_on=False)
    return ax.annotate(text, xy=((x0 + x1) / 2, y), xytext=(0, 1.2), textcoords="offset points", ha="center",
                       va="bottom", fontsize=MIN_FS, color=INK2)


def stat_note(ax, text, x, y, ha="left", va="bottom"):
    """Test name + statistic inside the panel (axes fraction), in secondary ink, placed in free space."""
    return ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=MIN_FS, color=INK2)


# ---------------------------------------------------------------- marks
def ellipse(ax, x, y, colour, n_std=2.0):
    """Translucent covariance ellipse (n_std s.d.) with a full-colour outline."""
    vals, vecs = np.linalg.eigh(np.cov(x, y))
    ang = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    ax.add_patch(Ellipse((np.mean(x), np.mean(y)), 2 * n_std * np.sqrt(vals[1]), 2 * n_std * np.sqrt(vals[0]),
                         angle=ang, fc=to_rgba(colour, AREA_ALPHA), ec=colour, lw=0.6, zorder=1))


def box_strip(ax, values, pos, colour, filled=True, width=0.5):
    """Box (quartiles, whiskers to the extremes, no caps) with translucent fill, every point overlaid."""
    fc = to_rgba(colour, FILL_ALPHA) if filled else "white"
    ax.boxplot([values], positions=[pos], widths=width, patch_artist=True, showfliers=False, showcaps=False,
               whis=(0, 100), medianprops=dict(color=INK, lw=0.9, solid_capstyle="butt"),
               whiskerprops=dict(color=INK2, lw=0.5), boxprops=dict(fc=fc, ec=colour, lw=0.6))
    jit = rng.uniform(-width * 0.28, width * 0.28, len(values))
    kw = DOT if filled else dict(s=DOT["s"], fc="white", ec=colour, lw=0.6)
    ax.scatter(pos + jit, values, zorder=3, **({"fc": colour} if filled else {}), **kw)


def effect_bars(ax, names, eff, lo, hi, credible):
    """Diverging horizontal effect bars, interval whiskers, a star beyond the whisker when credible, italic names.
    Rows run top to bottom in the given order."""
    y = -np.arange(len(names))
    cols = [(DIV_POS if e > 0 else DIV_NEG) if c else PH for e, c in zip(eff, credible)]
    ax.barh(y, eff, height=0.78, color=cols, lw=0)
    ax.errorbar(eff, y, xerr=[eff - lo, hi - eff], fmt="none", ecolor=INK2, elinewidth=0.5, capsize=1.2,
                capthick=0.5)
    for yi, l, h, e, c in zip(y, lo, hi, eff, credible):
        if c:
            end, dx, ha = (h, 1.5, "left") if e > 0 else (l, -1.5, "right")
            ax.annotate("*", xy=(end, yi), xytext=(dx, -2.2), textcoords="offset points", ha=ha, va="center",
                        fontsize=7, color=INK2)
    ax.axvline(0, color=INK2, lw=0.5)
    ax.set_yticks(y, names, fontstyle="italic")
    ax.set_ylim(y[-1] - 0.7, 0.7)
    ax.tick_params(axis="y", length=0)
    return y
