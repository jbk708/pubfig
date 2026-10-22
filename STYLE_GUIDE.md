# Figure style guide

The rules every pubfig figure follows, with the value to use and the pubfig name that applies it. Most values are
set when you `import pubfig`; the rest come from the helpers named in the right-hand column. Where a rule has no
pubfig name, the figure script applies it.

Two kinds of rule appear below:
- **Requirements** (section 1 and anything marked *must*) come from Nature's figure guidelines or from print
  legibility. They are never traded away for looks.
- **House style** (everything else) keeps figures consistent across papers. Change it deliberately, and update this
  guide when you do.

## 1. Page and output

| Rule | Value | In pubfig |
|---|---|---|
| Width | 89 mm single column or 183 mm double column; never wider | `SINGLE`, `WIDTH`; `check_layout` fails a wider figure |
| Height | at most 170 mm (247 mm including the legend) | `MAX_HEIGHT` |
| Background | white, including card and box fills (no grey on grey) | rcParams |
| Files | SVG with editable text, vector PDF with embedded TrueType, and a 300 dpi PNG for review | `save` (`svg.fonttype none`, `pdf.fonttype 42`) |
| Nothing overlaps or is clipped | no text on text, on data points or off the page; no point cut off at its axes | `check_layout`, `require_layout` |
| Plain language | no ticket numbers, internal model IDs or unexplained abbreviations; define every abbreviation in the figure or its legend | – |

## 2. Type

| Rule | Value | In pubfig |
|---|---|---|
| Typeface | one Helvetica-class sans-serif throughout: Nimbus Sans, then Arial, then Helvetica | rcParams |
| Sizes | tick labels 5.5 pt, axis labels 6 pt, titles 6.5 pt, legend 5.5 pt, statistics and annotations 5 pt, panel letters 8 pt bold | rcParams, `MIN_FS` |
| Floor | *must*: no text below 5 pt | `MIN_FS`; `check_layout` fails smaller text |
| Taxon names | genus and species italic; "sp.", "Unknown", family and higher ranks upright; gene symbols italic, KEGG IDs upright | `italic_ticks`, `effect_bars` |
| Statistic symbols | italic *P*, *q*, *R*², *r*, ρ; subscripts through mathtext (`log$_2$`) | `p_text`, mathtext rcParams |

Font notes:
- On barnacle, Nimbus Sans is installed on the login node only; compute nodes fall back to DejaVu Sans. Render final
  figures on the login node.
- On a Mac, Arial is used. matplotlib cannot load macOS Helvetica (`Helvetica.ttc`) glyphs at 5 pt on its 100 dpi
  canvas, which breaks the layout check.
- Math text (italic *P*, subscripts) takes a single named face, so pubfig sets it to whichever face the labels
  resolve to on that machine (`MATH_FONT`): Nimbus Sans on barnacle, Arial on a Mac.

## 3. Colour

Colour encodes identity, direction or magnitude, one job per figure element. Groups are always named directly (axis
labels, titles or a legend), never by colour alone.

| Rule | Value | In pubfig |
|---|---|---|
| Up to three groups | muted blue `#3a6fb5`, orange `#d8673a`, green `#3c9a76`, always in this order. Every pair passes the colour-blind validator (worst ΔE 9.3 colour-blind, 18.3 normal vision; all ≥ 3:1 on white) | `CATEGORICAL` |
| Four groups in a stack | blue, green, orange, magenta `#b8508f` in this order. Validated for neighbouring segments only (worst ΔE 9.3 colour-blind, 15.5 normal), so use it for stacked bars, never for scatter or boxes | `CATEGORICAL_STACK` |
| More groups | do not add hues. Use small multiples and name each panel, or fold the extras into "Other" | – |
| "Other" or "Unknown" | grey `#8f8e89`, last in the stack, with white gaps and a legend | `PH` |
| Direction of an effect | red `#c9504b` = higher, blue `#3a6fb5` = lower, grey = interval crosses 0 | `DIV_POS`, `DIV_NEG`, `PH` |
| Magnitude | one blue ramp, white to dark (`SEQ`). Use a square-root scale when most values are small, and print the values | `SEQ`, `SEQ_CMAP`, `heatmap` |
| Not significant | same colour at 30% alpha with a white edge; grey when no *P* was recorded. Never an open marker | `sig_colour`, `sig_scatter`, `NS_ALPHA` |
| Translucent fills | boxes at alpha 0.40, ellipses and areas at 0.15, outlined at 0.6 pt in the full colour | `FILL_ALPHA`, `AREA_ALPHA` |
| Ink | titles and axis labels `#0b0b0b`; ticks, annotations and statistics in secondary ink `#3a3936` (11.6:1 on white). Never colour text with a series colour | `INK`, `INK2` |
| Text on fills | black or white, whichever has the higher contrast with the fill (≥ 7:1 for text, ≥ 3:1 for marks) | `text_on` |
| New palettes | run the dataviz `validate_palette.js` before use: `--pairs all` for scatter and boxes, adjacent pairs for stacks | – |

## 4. Marks and lines

| Rule | Value | In pubfig |
|---|---|---|
| Lines | 0.5 pt for spines, whiskers, error bars, brackets and reference lines; never below 0.3 pt. Ticks 2 pt long | rcParams |
| Axes | top and right spines off, no grid. A faint `GRID` line marks zero where it matters | rcParams, `GRID` |
| Points | filled circles, 12 pt² (about 3.5 pt across), with a 0.3 pt white edge | `DOT` |
| Open markers | white fill and a 0.6 pt coloured edge, reserved for one stated second condition (for example, an adjusted version of the same measure). Define it in the legend. Never use it for "not significant" | `strip_mean(filled=False)`, `ordination(filled=…)` |
| Box with points | box = quartiles, whiskers to the extremes, no caps, no fliers, 0.9 pt dark median; every point drawn over it | `box_strip` |
| Many small-n points | place them with deterministic offsets, so the figure is the same on every run and no two points overlap | `swarm_offsets` |
| Effect bars | bar height 0.78 of the row; 0.5 pt capped whiskers; credible effects coloured with a 7 pt star beyond the whisker, others grey with no star; 0.5 pt zero line | `effect_bars` |
| Ellipses | 2-s.d. covariance ellipse per group with at least 3 points | `ellipse`, `ordination` |
| Stacked bars | white 0.3 pt gaps between segments | `stacked_bars` |
| Values beyond the axis | never clip silently. An interval end becomes an arrowhead at the edge; an estimate becomes an edge arrow with its value printed | `interval_point` |

## 5. Statistics on the plot

| Rule | Value | In pubfig |
|---|---|---|
| Comparison between groups | 0.5 pt bracket with 2.5 pt legs, stars, then the exact value: `** P = 0.004`, `n.s. q = 0.23` | `bracket`, `stars`, `p_text(p, "q")` |
| Exact values | two significant figures; "< 0.001" below that | `p_text` |
| Side-by-side brackets | put the stars on their own line, or stagger the bracket heights so the labels do not touch | `bracket` |
| Test name and statistic | inside the panel, in a free corner that touches no mark ("Mann–Whitney", "Spearman ρ = 0.93"); if no corner is free, leave headroom above the data or put it under the panel | `stat_note` |
| Star meaning | stated once per panel or in the legend ("* 94% HDI excludes 0") | – |
| Legends | give n, the test, the multiple-testing method, and what every error bar or box shows | – |
| Permutation tests | one-sided *P* with the +1 correction, so it is never 0 | `permutation_p`, `null_strip` |

## 6. Titles, labels and legends

| Rule | Value | In pubfig |
|---|---|---|
| Titles | short, neutral and one line, centred over the axes. Name the method where one applies, "Method: subject" with a colon, never a dash ("PERMANOVA: variance explained"). No conclusions in titles | rcParams |
| Panel letters | bold lowercase, 8 pt, on the title baseline at the panel's top left. Move a letter left with `dx` when long tick labels would meet it | `label(ax, "a", dx=-11)` |
| Direct labels first | write direction labels ("← Lower", "Higher →") and group names in the panel instead of adding a legend | `diverging_counts` |
| Legends | frameless, inside the panel where a corner is free, otherwise directly under it | rcParams, `legend_markers` |
| Taxon labels | the two lowest assigned ranks, each with its level initial and a colon: `f: Planococcaceae; g: Savagea`. Drop database suffixes (`Clostridia_258483` → `Clostridia`) | – |
| Axes | one y-scale per panel; never a second y-axis | – |

## 7. Layout

| Rule | Value | In pubfig |
|---|---|---|
| Placement | fix margins and panel positions (gridspec or millimetres from the top left); no automatic tight layout that moves panels between runs | `axes_mm` |
| Balance | panels of matching shape share a row; no large empty gaps | – |
| Rotated labels | avoid them. Break long labels onto two lines instead; rotated labels also trip the overlap check | – |
| Check before saving | run `require_layout(fig)` before `save`. It refuses the figure if text overlaps text or a data point, runs off the page or is under 5 pt, if a point is clipped by its axes, or if the figure is wider than 183 mm | `require_layout` |
| Look at it | the check cannot judge balance or meaning; view every figure at 300 dpi before it goes out | – |
| Mockups | anything drawn from synthetic data carries a watermark | `save(watermark_text=…)` |

## 8. Chart forms

Every form below is drawn in `examples/gallery.py`, which must pass the layout check.

- **Heatmap** (`heatmap`): print every value in its cell, black or white by contrast; no spines or tick marks; colour
  bar with ticks at real values. Use a square-root scale when most cells are small.
- **Stacked proportions** (`stacked_bars`): one bar per sample, segments in the stack palette with "Other" or
  "Unknown" last in grey.
- **Ordination** (`ordination`): no tick values; axes named "PC1 (32%)"; ellipses for groups of 3 or more; keep
  headroom for the test note.
- **Effect vs effect** (`agreement`): equal axes, dashed identity (or shift) line, the subset of interest darker on
  top, Spearman ρ in a corner.
- **Estimates with intervals** (`interval_point`, `strip_mean`): show every split or replicate, not only the mean.
- **Permutation nulls** (`null_strip`): the null as a grey cloud, the observed value as a diamond, *P* above.
- **Distributions by category** (`category_hist`): stacked histogram, labelled reference lines (zero, median).
- **Volcano** (`volcano`): coloured only when significant and past the effect threshold; label few points, then check
  the layout.
- **Many sources or species**: small multiples with the name in each panel title and colour used for a second
  variable (for example, decay stage), rather than one colour per species.

## Where these rules came from

The style was developed for the minderoo multi-omics paper and is now shared through pubfig. Its marks and
statistics conventions (boxes with every point, bracketed comparisons, ellipses on ordinations, diverging effect
bars, method-named titles) were adapted from a published two-group microbiome figure the authors liked. Where that
figure conflicted with Nature's requirements, the requirements won:
- lowercase panel letters, not uppercase;
- a Helvetica-class typeface, not a humanist sans;
- statistics text held at the 5 pt floor;
- notes kept off the data rather than boxed over it.

Its own green and purple failed the colour-blind validator's chroma floor, so pubfig's three hues were muted toward
that look instead of copied.
