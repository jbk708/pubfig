# Figure style guide

Rules for every figure drawn with pubfig. They were written for the minderoo multi-omics paper and are implemented once in this package: the rcParams and palette constants in `pubfig/style.py`, and the helpers `label`, `bracket`, `stars`, `p_text`, `stat_note`, `ellipse`, `box_strip` and `effect_bars` in `pubfig/helpers.py`. The format rules in the [README](README.md) still apply and win over anything here. Where a rule below names "modality" colours, read them as `CATEGORICAL` slots 1–3 (in minderoo they encode metagenomics, metabolomics and proteomics).

## Where these rules come from

Most of the rules were learned from a reference figure the authors liked. It was a two-group microbiome figure with:
- boxplots with overlaid points and significance brackets;
- a robust Aitchison PCA with group ellipses;
- diverging log2 fold-change bar charts;
- method-named panel titles.

The figure is not in the repo. Each rule below is marked:

- **Adopt:** taken over as it is.
- **Adapt:** the idea is kept, with values changed to fit our print rules.
- **Keep ours:** the reference differs, and our current rule stays.

Measurements were taken from the reference PNG. It was a 2002 px-wide raster with no physical size, so sizes are given relative to its tick-label cap height ("cap").

## Hard constraints (never traded for style)

- 183 mm maximum width.
- No text under 5 pt.
- Secondary ink `#3a3936`.
- White background.
- Outputs are SVG (live text), PDF (TrueType) and 300 dpi PNG.
- Plain language, with no ticket numbers or internal model IDs.
- No label overlaps a dot, line, legend or other label.
- Nothing is clipped.
- Panels are balanced, with no large gaps.
- Modality colours are distinct and colour-blind safe.

## 1. Colour

| Rule | Reference | Ours | Decision |
|---|---|---|---|
| Muted, mid-lightness identity colours, not saturated primaries | green `#4b9c7a`, purple `#7470ae` (sampled) | modalities `#3a6fb5` metagenomics, `#d8673a` metabolomics, `#3c9a76` proteomics (were `#2a78d6`, `#eb6834`, `#1baf7a`) | **Adapt.** Same three hues, muted toward the reference. The reference pair itself fails the chroma floor (C 0.094–0.096 < 0.10), so it was not copied. |
| Palette passes the colour-blind validator | – | `validate_palette.js "#3a6fb5,#d8673a,#3c9a76" --mode light --pairs all`: **all PASS**. Worst protan/deutan ΔE 9.3 (target 8); worst normal-vision ΔE 18.3 (floor 15); every colour ≥ 3:1 on white. The old set had a contrast WARN on aqua (2.74:1), which this removes. | **Adopt** (rule of ours). |
| Effect direction coloured by the group it favours | green bars = up in group 1, purple = up in group 2 | diverging pair `#c9504b` (higher) / `#3a6fb5` (lower), validated all PASS (ΔE 16.5 colour-blind, 25.8 normal); grey `#8f8e89` = interval crosses 0 | **Adapt.** We keep blue↔red, muted to match. |
| Translucent box fills | fill alpha **0.40** (`#afd7ca` = green at 0.40) | `FILL_ALPHA = 0.40` | **Adopt** |
| Translucent ellipse / area fills | fill alpha **0.13–0.15** (`#e4f1ed`, `#edecf4`) | `AREA_ALPHA = 0.15` | **Adopt** |
| Outline of a translucent shape in the full colour | box and ellipse edges in the group colour | box edge 0.6 pt, ellipse edge 0.6 pt, both in full colour | **Adopt** |
| Near-black tick labels | `#0c0c0c`-ish | ticks stay secondary ink `#3a3936` | **Keep ours** (hard constraint) |

## 2. Type

| Rule | Reference | Ours | Decision |
|---|---|---|---|
| One clean sans-serif throughout | humanist sans (Noto/Open Sans look) | Nimbus Sans (Helvetica class); Noto Sans is installed on barnacle but not used | **Keep ours.** Nature asks for Helvetica/Arial-class type. |
| Flat size hierarchy | ticks = axis labels = taxon labels ≈ 1.0 cap; title ≈ 1.1; stat text ≈ 0.8; panel letter ≈ 1.2 bold | ticks 5.5 pt, axis labels 6, titles 6.5, stat/annotation text 5 (the floor), panel letters 8 bold | **Adapt.** Same ordering. Stat text cannot go below 5 pt, and Nature fixes the panel letter at 8 pt. |
| Taxon names in italics | every species/genus label italic | `effect_bars` and the Extended Data genus axis set `fontstyle="italic"`; KO IDs and gene symbols stay upright | **Adopt** for genera. Italic gene symbols are not done yet. |
| Subscripts and italic statistic symbols | "log₂ FC", upright "P" | italic $P$, $q$ and subscripts via mathtext in Nimbus Sans (`mathtext.fontset: custom`) | **Adapt.** Nature italicises P. |

## 3. Titles and panel letters

| Rule | Reference | Ours | Decision |
|---|---|---|---|
| Method-named titles, "Method: subject" | "ANCOM-BC: Sylph", "Sylph — Robust Aitchison PCA" | "PERMANOVA: variance explained", "BIRDMAn: genera vs domoic acid", "MMvec: archaea vs shuffled"; descriptive titles where no single method applies ("Sampling areas") | **Adopt** (colon form, never an em dash) |
| Titles centred over the axes | centred | `axes.titlelocation: center`; Fig. 1 panel d centres its hand-placed title over the whole panel | **Adopt.** This replaces our old left-aligned rule. |
| Panel letters bold **uppercase**, at the top-left of the panel | A, B, C | bold **lowercase** 8 pt, 11 pt left of the axes on the title baseline | **Keep ours.** Nature uses lowercase bold. |
| No conclusions in titles | neutral | neutral | Same rule already |

## 4. Marks and lines

| Rule | Reference | Ours | Decision |
|---|---|---|---|
| Points as filled circles with a hairline white edge | ≈ 1.0 cap across, white edge | `DOT = s 12 pt² (~3.5 pt), white edge 0.3 pt`; open markers (white fill, coloured 0.6 pt edge) mean "region and depth removed" (or "site, month and depth removed") / proteomic baseline and nothing else; *P* ≥ 0.05 is a pale fill (same colour at 30% alpha, white edge), never an open marker | **Adopt** |
| Box + every point | box = quartiles, whiskers to the extremes, no caps, no fliers, thick dark median | `box_strip`: same; median `#0b0b0b` 0.9 pt, whiskers 0.5 pt secondary ink | **Adopt** |
| Diverging horizontal effect bars | bar height ≈ 0.8 of row pitch; dark capped error bars; star beyond the whisker; zero line | `effect_bars`: height 0.78, 0.5 pt capped whiskers in secondary ink, 7 pt `*` just beyond the whisker, 0.5 pt zero line, credible = coloured + star, otherwise grey with no star | **Adopt** |
| Group ellipses on ordinations | covariance ellipses, translucent | `ellipse(ax, x, y, colour, n_std)` | **Adopt** |
| Thin lines | spines/whiskers/error bars ≈ 1/8 cap | 0.5 pt everywhere (≥ 0.3 pt print floor); 2 pt ticks | Same rule already |
| Open axes, no grid | top/right spines off, no grid | same | Same rule already |

## 5. Statistics on the plot

| Rule | Reference | Ours | Decision |
|---|---|---|---|
| Bracket + stars + exact P between compared groups | "*** P<0.001", "n.s. P=0.241" over a thin bracket with short legs | `bracket(ax, x0, x1, y, f"{stars(p)} {p_text(p)}")`: 0.5 pt bracket, 2.5 pt legs, 5 pt secondary-ink text; P to 2 significant figures, "< 0.001" below that; stars on their own line when brackets sit side by side | **Adopt** |
| Test statistic as a note inside the plot | "PERMANOVA F = 7.8, P = 0.0002" at lower left on a white box over the ellipse | `stat_note(...)` names the test ("Mann–Whitney", "Spearman ρ = …") in free space, in a corner that touches no mark | **Adapt.** The reference's white box covers part of an ellipse, which breaks our no-overlap rule. |
| Star meaning stated | implicit | stated once per panel ("* 94% HDI excludes 0") or in the legend | **Adapt** |

## 6. Legends and whitespace

| Rule | Reference | Ours | Decision |
|---|---|---|---|
| Frameless legend inside the plot, in free space | upper-left, circle handles, no frame | `legend.frameon: False`; placed inside where a corner is free (Fig. 2c, Fig. 3b), otherwise directly under the panel; Fig. 1b's legend is placed by the free-space search | **Adopt** |
| Prefer direct labels to legends | categorical axis labels | direction labels written in the panel ("← Lower", "Higher →" in Fig. 3c) instead of a three-item legend; modalities always named | **Adopt.** This removed a legend that left a gap. |
| Even gutters | tight, regular | fixed gridspec margins; all panels checked visually at 300 dpi | Same rule already |

## Conflicts with the reference (kept our rule; for the authors to decide)

1. **Panel letters.** The reference uses bold uppercase (A, B); Nature uses bold lowercase (a, b). We kept lowercase.
2. **Typeface.** The reference uses a humanist sans (Noto/Open Sans look); Nature asks for Helvetica/Arial-class type. We kept Nimbus Sans. Noto Sans is installed if the authors prefer it.
3. **Tick and label ink.** The reference uses near-black; we use the agreed secondary ink `#3a3936` for ticks and annotations, and black for axis labels and titles.
4. **Stat note on a white box over data.** The reference's PERMANOVA note covers part of an ellipse; our no-overlap rule forbids this, so notes go in free corners.
5. **Group palette.** The reference's green and purple fall just below the validator's chroma floor, and its green is almost the proteomics colour. We muted our own three hues instead of adopting theirs.
6. **Stat text size.** The reference's stat text is about 0.8× the tick size; at our 5.5 pt ticks that would be 4.4 pt, so it is held at the 5 pt floor.
