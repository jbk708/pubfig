"""pubfig: Nature-format print style, chart helpers and layout checks for matplotlib figures.

    import pubfig as pf
    fig = plt.figure(figsize=(pf.WIDTH, 120 * pf.MM))
    ...
    pf.label(ax, "a")
    pf.require_layout(fig)
    pf.save(fig, "figures", "fig1")
"""
from .charts import (DASH, NS_ALPHA, SEQ_CMAP, agreement, axes_mm, category_hist, diverging_counts, heatmap,
                     interval_point, italic_ticks, legend_markers, null_strip, ordination, permutation_p,
                     sig_colour, sig_scatter, stacked_bars, strip_mean, swarm_offsets, volcano)
from .checks import check_layout, require_layout
from .helpers import (bracket, box_strip, effect_bars, ellipse, label, luminance, p_text, rng, save, stars,
                      stat_note, text_on, watermark)
from .style import (AREA_ALPHA, CATEGORICAL, CATEGORICAL_STACK, DIV_NEG, DIV_POS, DOT, FILL_ALPHA, GRID, INK, INK2,
                    LAND, MATH_FONT, MAX_HEIGHT, MIN_FS, MM, PH, RCPARAMS, SANS, SEQ, SINGLE, WIDTH, use)

__version__ = "0.2.1"
use()

__all__ = [
    # style
    "AREA_ALPHA", "CATEGORICAL", "CATEGORICAL_STACK", "DASH", "DIV_NEG", "DIV_POS", "DOT", "FILL_ALPHA", "GRID",
    "INK", "INK2", "LAND", "MATH_FONT", "MAX_HEIGHT", "MIN_FS", "MM", "NS_ALPHA", "PH", "RCPARAMS", "SANS", "SEQ",
    "SEQ_CMAP", "SINGLE", "WIDTH", "use",
    # annotation, layout and saving
    "axes_mm", "bracket", "check_layout", "italic_ticks", "label", "legend_markers", "luminance", "p_text",
    "permutation_p", "require_layout", "rng", "save", "stars", "stat_note", "text_on", "watermark",
    # marks and charts
    "agreement", "box_strip", "category_hist", "diverging_counts", "effect_bars", "ellipse", "heatmap",
    "interval_point", "null_strip", "ordination", "sig_colour", "sig_scatter", "stacked_bars", "strip_mean",
    "swarm_offsets", "volcano",
]
