"""Print style for Nature-format figures: page sizes, palette, ink and matplotlib rcParams.

Importing pubfig applies the rcParams once (as the original minderoo module did); call `use()` again to
restore them after a script overrides some. Rules and their origin are in STYLE_GUIDE.md.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

MM = 1 / 25.4            # inches per mm
WIDTH = 183 * MM         # double column
SINGLE = 89 * MM         # single column
MAX_HEIGHT = 170 * MM    # without legend (247 mm with legend)

# Muted categorical set; validate_palette.js (light, --pairs all): every check PASS, all three >= 3:1 on white.
# Past three series, validate the extra hue for the chart form (adjacent pairs for stacks) before using it.
CATEGORICAL = ["#3a6fb5", "#d8673a", "#3c9a76"]
DIV_NEG, DIV_POS = "#3a6fb5", "#c9504b"  # validated diverging pair (all checks PASS); grey = interval crosses 0
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]  # single-hue blue ramp
# Print pass: secondary ink 11.6:1 on white; grey marks >= 3:1 (non-text minimum); no text below 5 pt; lines >= 0.3 pt.
INK, INK2, GRID, PH, LAND = "#0b0b0b", "#3a3936", "#d9d8d4", "#8f8e89", "#ecebe7"
MIN_FS = 5.0
FILL_ALPHA = 0.40   # box fills
AREA_ALPHA = 0.15   # group ellipses and other area fills
DOT = dict(s=12, ec="white", lw=0.3)  # small-n points: ~3.5 pt across, hairline white edge

RCPARAMS = {
    "font.family": "sans-serif", "font.sans-serif": ["Nimbus Sans", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 6, "axes.titlesize": 6.5, "axes.labelsize": 6, "xtick.labelsize": 5.5,
    "ytick.labelsize": 5.5, "legend.fontsize": 5.5, "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2, "ytick.major.size": 2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": INK2,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "hatch.linewidth": 0.5, "axes.titlelocation": "center", "axes.titlepad": 6, "axes.titleweight": "normal",
    "legend.frameon": False, "legend.handletextpad": 0.3, "legend.borderaxespad": 0.3,
    "mathtext.fontset": "custom", "mathtext.rm": "Nimbus Sans", "mathtext.it": "Nimbus Sans:italic",
    "mathtext.bf": "Nimbus Sans:bold",
    "pdf.fonttype": 42, "svg.fonttype": "none", "savefig.dpi": 300,
}


def use():
    """Apply the print style to matplotlib's rcParams."""
    plt.rcParams.update(RCPARAMS)
