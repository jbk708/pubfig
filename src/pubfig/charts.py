"""Chart forms that recur across the minderoo, FEAST and related figures, ported from their scripts.

Each function draws on an existing Axes and leaves titles, panel letters and limits it does not need to the caller.
"""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_rgba
from matplotlib.lines import Line2D

from .helpers import ellipse, p_text, stat_note, text_on
from .style import DIV_NEG, DIV_POS, DOT, GRID, INK, INK2, MIN_FS, MM, PH, SEQ

NS_ALPHA = 0.30  # P >= 0.05: same colour, pale fill (STYLE_GUIDE section 3); never an open marker
DASH = (0, (3, 2))
SEQ_CMAP = LinearSegmentedColormap.from_list("pubfig_seq", ["#ffffff"] + SEQ)


# ---------------------------------------------------------------- layout
def axes_mm(fig, x, top, w, h):
    """Axes placed in mm from the figure's top-left corner."""
    W, H = fig.get_size_inches() / MM
    return fig.add_axes([x / W, 1 - (top + h) / H, w / W, h / H])


def italic_ticks(ax, names=None, axis="y"):
    """Italicise tick labels (taxon names); all of them, or only those in `names`."""
    labels = ax.get_yticklabels() if axis == "y" else ax.get_xticklabels()
    for t in labels:
        if names is None or t.get_text() in names:
            t.set_fontstyle("italic")


# ---------------------------------------------------------------- markers
def sig_colour(colour, p):
    """Fill for a point with p-value p: full colour if P < 0.05, pale if not, grey if no P was recorded."""
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return PH
    return colour if p < 0.05 else to_rgba(colour, NS_ALPHA)


def sig_scatter(ax, x, y, p, colour, marker="o", s=DOT["s"], **kw):
    """Scatter whose fills follow sig_colour (one p per point, or one for all)."""
    p = np.broadcast_to(np.asarray(p, float), np.shape(x))
    fc = [sig_colour(colour, pi) for pi in p]
    return ax.scatter(x, y, marker=marker, s=s, fc=fc, ec="white", lw=0.3, zorder=3, **kw)


def swarm_offsets(values, step=0.11, tol=0.06, log=False):
    """Deterministic offsets (0, -s, +s, -2s, ...) so no two points closer than tol (in value units, or
    decades when log) share a position. Use instead of random jitter when n is small."""
    v = np.log10(np.asarray(values, float)) if log else np.asarray(values, float)
    off = np.zeros(len(v))
    placed = []
    for i in np.argsort(v, kind="stable"):
        used = {off[j] for j in placed if abs(v[j] - v[i]) < tol}
        k = 0
        while (cand := (k + 1) // 2 * step * (1 if k % 2 == 0 else -1)) in used:
            k += 1
        off[i] = cand
        placed.append(i)
    return off


# ---------------------------------------------------------------- heatmap
def heatmap(ax, values, row_labels, col_labels, cmap=SEQ_CMAP, norm=None, fmt="{:.2f}", cbar_ax=None,
            cbar_label=None, cbar_ticks=None, annotate=True):
    """Matrix with every value printed in black or white by computed contrast; no spines, no tick marks.

    values: 2-D array (NaN cells are left white and unlabelled). Pass cbar_ax (or True for a colorbar beside the
    axes) to draw a colour bar. Returns the AxesImage."""
    vals = np.asarray(values, float)
    norm = norm or Normalize(np.nanmin(vals), np.nanmax(vals))
    im = ax.imshow(np.ma.masked_invalid(vals), cmap=cmap, norm=norm, aspect="auto")
    if annotate:
        for (r, c), v in np.ndenumerate(vals):
            if not np.isnan(v):
                ax.text(c, r, fmt.format(v), ha="center", va="center", fontsize=MIN_FS, color=text_on(cmap(norm(v))))
    ax.set_xticks(range(vals.shape[1]), col_labels)
    ax.set_yticks(range(vals.shape[0]), row_labels)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    if cbar_ax is not None:
        kw = dict(cax=cbar_ax) if cbar_ax is not True else dict(ax=ax, fraction=0.05, pad=0.03)
        cb = ax.figure.colorbar(im, ticks=cbar_ticks, **kw)
        cb.outline.set_visible(False)
        cb.ax.tick_params(length=2, width=0.5)
        if cbar_label:
            cb.set_label(cbar_label, fontsize=MIN_FS + 0.5)
    return im


# ---------------------------------------------------------------- bars
def stacked_bars(ax, fractions, colours, labels=None, x=None, width=0.86, horizontal=False, gap_lw=0.3):
    """Stacked bars (one per row of `fractions`, one segment per column), white hairline gaps between segments.
    Returns the bar positions. Validate the colour order for adjacent pairs (stacks) before use."""
    f = np.asarray(fractions, float)
    x = np.arange(len(f)) if x is None else np.asarray(x)
    base = np.zeros(len(f))
    for j, col in enumerate(colours):
        lab = labels[j] if labels is not None else None
        if horizontal:
            ax.barh(x, f[:, j], left=base, height=width, color=col, ec="white", lw=gap_lw, label=lab)
        else:
            ax.bar(x, f[:, j], bottom=base, width=width, color=col, ec="white", lw=gap_lw, label=lab)
        base += f[:, j]
    return x


def diverging_counts(ax, row_labels, up, down, totals, lower="← Lower", higher="Higher →"):
    """Per row, the share (%) of features credibly higher (right, DIV_POS) and lower (left, DIV_NEG), each bar
    labelled with its count; direction labels written in the panel instead of a legend."""
    up, down, totals = (np.asarray(a, float) for a in (up, down, totals))
    span = 100 * max((up / totals).max(), (down / totals).max())
    for i in range(len(row_labels)):
        for count, sign, dy, col in [(up[i], 1, -0.18, DIV_POS), (down[i], -1, 0.18, DIV_NEG)]:
            v = sign * 100 * count / totals[i]
            ax.barh(i + dy, v, height=0.34, color=col, lw=0)
            ax.text(v + sign * 0.025 * span, i + dy, f"{int(count):,}", va="center",
                    ha="left" if sign > 0 else "right", fontsize=MIN_FS, color=INK2)
    ax.axvline(0, color=INK2, lw=0.5)
    ax.set_yticks(range(len(row_labels)), row_labels)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(len(row_labels) - 0.45, -1.0)
    ax.set_xlim(-span * 1.3, span * 1.3)
    ax.xaxis.set_major_formatter(lambda v, _: f"{abs(v):g}")  # shares are positive both ways
    ax.text(-0.05 * span, -0.72, lower, ha="right", va="center", fontsize=MIN_FS, color=DIV_NEG)
    ax.text(0.05 * span, -0.72, higher, ha="left", va="center", fontsize=MIN_FS, color=DIV_POS)


# ---------------------------------------------------------------- points and intervals
def interval_point(ax, x, y, lo_err, hi_err, colour, xlim, filled=True):
    """Horizontal estimate with interval at row y. An interval end beyond xlim becomes an arrowhead at the edge; an
    estimate beyond xlim becomes an edge arrow with the value printed (so nothing is silently clipped)."""
    lo, hi = xlim
    if not lo < x < hi:
        edge = lo if x <= lo else hi
        ax.scatter(edge, y, marker="<" if x <= lo else ">", s=14, fc=colour, ec="none", zorder=3, clip_on=False)
        ax.text(edge + (0.018 if x <= lo else -0.018) * (hi - lo), y, f"{x:.2f}".replace("-", "−"),
                ha="left" if x <= lo else "right", va="center", fontsize=MIN_FS, color=INK)
        return
    a, b = max(x - lo_err, lo), min(x + hi_err, hi)
    ax.plot([a, b], [y, y], color=colour, lw=0.6, zorder=2, solid_capstyle="butt")
    for e, inside in ((x - lo_err, x - lo_err > lo), (x + hi_err, x + hi_err < hi)):
        if inside:
            ax.plot([e, e], [y - 0.13, y + 0.13], color=colour, lw=0.6, zorder=2)
        else:
            ax.plot([lo if e <= lo else hi], [y], marker="<" if e <= lo else ">", ms=2.6, color=colour, mew=0,
                    clip_on=False, zorder=2)
    ax.scatter(x, y, marker="o", s=16, fc=colour if filled else "white", ec="white" if filled else colour,
               lw=0.3 if filled else 0.7, zorder=3)
    ax.set_xlim(lo, hi)


def strip_mean(ax, x, values, colour, filled=True, spread=0.045, s=5):
    """Every value (e.g. per CV split) as a small dot around x, with a dark tick at the mean."""
    v = np.asarray(values, float)
    kw = dict(fc=colour, ec="white", lw=0.3) if filled else dict(fc="white", ec=colour, lw=0.6)
    ax.scatter(x + np.linspace(-spread, spread, len(v)), v, s=s, zorder=3, **kw)
    ax.plot([x - 0.1, x + 0.1], [v.mean()] * 2, color=INK, lw=0.9, zorder=4, solid_capstyle="butt")


def permutation_p(null, observed, greater=True):
    """One-sided permutation P with the +1 correction: (#null at least as extreme + 1) / (n + 1)."""
    null = np.asarray(null, float)
    k = (null >= observed).sum() if greater else (null <= observed).sum()
    return (k + 1) / (len(null) + 1)


def null_strip(ax, x, null, observed, colour, seed=3, p_y=None):
    """Permutation null as a grey cloud left of x, the observed value as a diamond right of it, P above.
    Returns P (one-sided, observed >= null)."""
    r = np.random.default_rng(seed)
    null = np.asarray(null, float)
    p = permutation_p(null, observed)
    ax.scatter(x - 0.12 + r.uniform(-0.09, 0.09, len(null)), null, s=3, color=PH, edgecolors="none", zorder=2)
    ax.scatter([x + 0.2], [observed], marker="D", s=16, fc=colour, ec="white", lw=0.3, zorder=3)
    top = max(null.max(), observed) if p_y is None else p_y
    ax.annotate(p_text(p), xy=(x, top), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                fontsize=MIN_FS, color=INK2)
    return p


# ---------------------------------------------------------------- relationships
def agreement(ax, x, y, highlight=None, line="identity", shift=0.0, rho=None, label_hi=None, label_lo=None,
              note_loc=(0.98, 0.02)):
    """Effect vs effect (two models, two tables, two contrasts): all points small grey, `highlight` (bool mask)
    darker on top, a dashed identity (or y = x + shift) line, and a Spearman rho note in a free corner.
    Sets equal limits around the data."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    hi = np.zeros(len(x), bool) if highlight is None else np.asarray(highlight, bool)
    ax.scatter(x[~hi], y[~hi], s=3, fc=PH, lw=0, zorder=2, label=label_lo)
    if hi.any():
        ax.scatter(x[hi], y[hi], s=6, fc=INK2, ec="white", lw=0.2, zorder=3, label=label_hi)
    if line:
        ax.axline((0, shift), slope=1, lw=0.5, ls=DASH, color=INK2, zorder=1)
    lim = np.nanmax(np.abs(np.r_[x, y])) * 1.08
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal", adjustable="box")
    if rho is None:
        from scipy.stats import spearmanr  # optional dependency, only when rho is not given
        rho = spearmanr(x, y, nan_policy="omit").statistic
    stat_note(ax, f"Spearman ρ = {rho:.2f}", *note_loc, ha="right" if note_loc[0] > 0.5 else "left")
    return rho


def ordination(ax, coords, groups, colours, var_pct=None, ellipses=True, filled=None, head_frac=0.0, pad=0.04,
               s=9):
    """PCoA/PCA scatter coloured by group, with 2-s.d. covariance ellipses (groups with >= 3 points), no tick
    values, axes named "PC1 (x%)". coords: (n, 2); groups: length-n labels; colours: {group: colour};
    filled: {group: bool} (open markers only where the style guide defines a meaning for them).
    Limits fit points and ellipses, keeping head_frac of the height free at the top for notes."""
    coords = np.asarray(coords, float)
    groups = np.asarray(groups)
    outlines = [coords]
    for g, col in colours.items():
        m = groups == g
        if not m.any():
            continue
        if ellipses and m.sum() >= 3:
            e = ellipse(ax, coords[m, 0], coords[m, 1], col)
            outlines.append(_ellipse_outline(e))
        fill = True if filled is None else filled.get(g, True)
        ax.scatter(coords[m, 0], coords[m, 1], s=s, fc=col if fill else "white", ec="white" if fill else col,
                   lw=0.3 if fill else 0.6, zorder=3 if fill else 4, label=str(g))
    allp = np.vstack(outlines)
    (x0, y0), (x1, y1) = allp.min(0), allp.max(0)
    dx, dy = x1 - x0, y1 - y0
    ax.set_xlim(x0 - pad * dx, x1 + pad * dx)
    lo, top = y0 - pad * dy, y1 + pad * dy
    ax.set_ylim(lo, top + (top - lo) * head_frac / (1 - head_frac))
    ax.set_xticks([])
    ax.set_yticks([])
    if var_pct is not None:
        ax.set_xlabel(f"PC1 ({var_pct[0]:.0f}%)", labelpad=2)
        ax.set_ylabel(f"PC2 ({var_pct[1]:.0f}%)", labelpad=2)


def _ellipse_outline(e, n=200):
    t = np.linspace(0, 2 * np.pi, n)
    a, b, th = e.width / 2, e.height / 2, np.radians(e.angle)
    x = e.center[0] + a * np.cos(t) * np.cos(th) - b * np.sin(t) * np.sin(th)
    y = e.center[1] + a * np.cos(t) * np.sin(th) + b * np.sin(t) * np.cos(th)
    return np.c_[x, y]


# ---------------------------------------------------------------- distributions
def category_hist(ax, values, categories, spec, bins, ref_lines=(), headroom=1.35):
    """Stacked histogram of `values` split by `categories`; spec = [(category, colour, legend label), ...] in stack
    order. ref_lines = [(x, text, solid?), ...] drawn as vertical lines labelled near the top."""
    values, categories = np.asarray(values, float), np.asarray(categories)
    ax.hist([values[categories == c] for c, _, _ in spec], bins=bins, stacked=True, color=[c for _, c, _ in spec],
            lw=0, label=[lab for _, _, lab in spec])
    top = ax.get_ylim()[1]
    ax.set_ylim(0, top * headroom)
    xr = np.ptp(ax.get_xlim())
    for i, (x, text, solid) in enumerate(ref_lines):
        ax.axvline(x, color=INK, lw=0.6, ls="-" if solid else DASH)
        side = -1 if i % 2 == 0 else 1
        ax.text(x + side * 0.01 * xr, top * (headroom - 0.05), text, ha="right" if side < 0 else "left", va="top",
                fontsize=MIN_FS, color=INK2)


def volcano(ax, effect, q, alpha=0.05, effect_min=0.0, names=None, n_labels=0, s=4):
    """Effect vs -log10(q): significant-and-large points in DIV_POS / DIV_NEG by direction, the rest grey; dashed
    threshold lines; optionally the n_labels most significant points named (check the layout after)."""
    effect, q = np.asarray(effect, float), np.asarray(q, float)
    y = -np.log10(np.clip(q, 1e-300, 1))
    sig = (q < alpha) & (np.abs(effect) >= effect_min)
    ax.scatter(effect[~sig], y[~sig], s=s, fc=PH, lw=0, zorder=2)
    for m, col in ((sig & (effect > 0), DIV_POS), (sig & (effect < 0), DIV_NEG)):
        ax.scatter(effect[m], y[m], s=s + 2, fc=col, ec="white", lw=0.2, zorder=3)
    ax.axhline(-np.log10(alpha), color=INK2, lw=0.5, ls=DASH, zorder=1)
    for e in {effect_min, -effect_min} - {0.0}:
        ax.axvline(e, color=INK2, lw=0.5, ls=DASH, zorder=1)
    ax.axvline(0, color=GRID, lw=0.5, zorder=0)
    xm = np.nanmax(np.abs(effect)) * (1.35 if n_labels else 1.08)  # room for names beside the outermost points
    ax.set_xlim(-xm, xm)
    ax.set_ylim(0, np.nanmax(y) * (1.25 if n_labels else 1.08))
    if names is not None and n_labels:
        # names sit centred just above their points, pulled inward from the axes edges
        for i in np.argsort(q)[:n_labels]:
            if sig[i]:
                ha = "center" if abs(effect[i]) < 0.6 * xm else ("right" if effect[i] > 0 else "left")
                ax.annotate(names[i], (effect[i], y[i]), xytext=(0, 3), textcoords="offset points", ha=ha,
                            va="bottom", fontsize=MIN_FS, color=INK2, fontstyle="italic")
    ax.set_ylabel("−log$_{10}$ $q$")
    return sig


def legend_markers(ax, items, loc="best", marker="o", **kw):
    """Frameless legend of filled circles: items = [(label, colour), ...] (use for colours not tied to artists)."""
    h = [Line2D([], [], ls="", marker=marker, ms=3.5, mfc=c, mec="white", mew=0.3, label=lab) for lab, c in items]
    return ax.legend(handles=h, loc=loc, fontsize=MIN_FS, handletextpad=0.1, borderaxespad=0.2, **kw)
