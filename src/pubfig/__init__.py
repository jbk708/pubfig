"""pubfig: Nature-format print style and helpers for matplotlib figures.

    import pubfig as pf
    fig = plt.figure(figsize=(pf.WIDTH, 120 * pf.MM))
    ...
    pf.label(ax, "a")
    pf.require_layout(fig)
    pf.save(fig, "figures", "fig1")
"""
from .checks import check_layout, require_layout
from .helpers import (bracket, box_strip, effect_bars, ellipse, label, luminance, p_text, rng, save, stars,
                      stat_note, text_on, watermark)
from .style import (AREA_ALPHA, CATEGORICAL, DIV_NEG, DIV_POS, DOT, FILL_ALPHA, GRID, INK, INK2, LAND, MAX_HEIGHT,
                    MIN_FS, MM, PH, RCPARAMS, SEQ, SINGLE, WIDTH, use)

__version__ = "0.1.0"
use()

__all__ = [
    "AREA_ALPHA", "CATEGORICAL", "DIV_NEG", "DIV_POS", "DOT", "FILL_ALPHA", "GRID", "INK", "INK2", "LAND",
    "MAX_HEIGHT", "MIN_FS", "MM", "PH", "RCPARAMS", "SEQ", "SINGLE", "WIDTH", "bracket", "box_strip",
    "check_layout", "effect_bars", "ellipse", "label", "luminance", "p_text", "require_layout", "rng", "save",
    "stars", "stat_note", "text_on", "use", "watermark",
]
