# pubfig

Nature-format print style, annotation helpers and layout checks for matplotlib figures. This is the shared figure style first written for the minderoo multi-omics paper, pulled out so other projects can reuse it.

## Install

```bash
pip install "git+ssh://git@github.com/jbk708/pubfig.git"
# or, for local edits
git clone git@github.com:jbk708/pubfig.git && pip install -e pubfig
```

## Use

```python
import matplotlib.pyplot as plt
import pubfig as pf          # importing applies the print style (rcParams)

fig = plt.figure(figsize=(pf.WIDTH, 120 * pf.MM))
ax = fig.add_subplot()
pf.box_strip(ax, values, 0, pf.CATEGORICAL[0])
pf.bracket(ax, 0, 1, 1.05, f"{pf.stars(q)}\n{pf.p_text(q, 'q')}")
ax.set_title("Wilcoxon: change with stage")
pf.label(ax, "a")

pf.require_layout(fig)       # exits without writing if text overlaps, runs off the page, is < 5 pt, or > 183 mm
pf.save(fig, "figures", "fig1")   # -> figures/fig1.{svg,pdf,png}
```

| Name | What |
|---|---|
| `WIDTH`, `SINGLE`, `MAX_HEIGHT`, `MM` | 183 mm / 89 mm / 170 mm page sizes; `MM` converts mm to inches |
| `CATEGORICAL` | three muted hues that pass the colour-blind validator for all pairs |
| `DIV_NEG`, `DIV_POS`, `PH` | the diverging blue/red pair; grey for "interval crosses 0" |
| `SEQ` | single-hue blue ramp for magnitudes (heatmaps) |
| `INK`, `INK2`, `GRID`, `LAND` | primary ink, secondary ink `#3a3936`, gridline, and land fill colours |
| `MIN_FS`, `FILL_ALPHA`, `AREA_ALPHA`, `DOT` | the 5 pt text floor, box and area fill alphas, and point style |
| `label` | bold lowercase panel letter on the title baseline |
| `bracket`, `stars`, `p_text`, `stat_note` | statistics annotations |
| `box_strip`, `ellipse`, `effect_bars` | box with every point, covariance ellipse, diverging effect bars |
| `text_on`, `luminance` | black or white text, picked by computed contrast with the fill |
| `check_layout`, `require_layout` | pre-save layout checks |
| `save`, `watermark` | write SVG + PDF + PNG; optional "mockup" watermark |
| `use()` | re-apply the rcParams after a script overrides some |

## Fonts

The type is Nimbus Sans (Helvetica class). On barnacle it is installed on the login node only, and the compute nodes fall back to DejaVu Sans, so render final figures on the login node. On a Mac, Helvetica is used.

## Format rules (Nature)
- **Width:** 89 mm single column or 183 mm double column; height ≤ 170 mm (≤ 247 mm with legend).
- **Type:** sans-serif (Helvetica class), 5–7 pt; panel labels bold lowercase 8 pt.
- **Output:** SVG (editable text, `svg.fonttype none`) and vector PDF (embedded TrueType, `pdf.fonttype 42`); 300 dpi PNG for review only.
- **Colour:** validate every categorical palette with the dataviz `validate_palette.js` for the chart form (`--pairs all` for scatter and boxes, adjacent pairs for stacks). Name groups directly, never by colour alone. Effects use the blue ↔ red diverging pair with a grey midpoint. Boxes are filled at alpha 0.40 and areas at 0.15, outlined in the full colour.
- **Print legibility:** no text below 5 pt; text ≥ 7:1 contrast; marks ≥ 3:1; white card fills; heatmap labels pick black or white by contrast; lines ≥ 0.3 pt.
- **Titles:** short, neutral, sentence case, one line, centred, named after the method where one applies ("PERMANOVA: variance explained"). No conclusions in titles. Statistics go inside the panel (bracket + stars + exact italic *P*; test name in a free corner).
- **Plain language:** no internal model or ticket IDs in figures; define every abbreviation.
- **Axes and stats:** one y-scale per panel. Give n, the test and the multiple-testing method in every legend, and define every error bar.

The full rules, their values and where each came from are in [`STYLE_GUIDE.md`](STYLE_GUIDE.md).

## Tests

```bash
pip install -e ".[test]" && pytest
```
