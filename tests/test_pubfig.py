import matplotlib.pyplot as plt
import numpy as np
import pytest

import pubfig as pf


def test_import_applies_print_style():
    # Figures must embed editable text (SVG) and TrueType (PDF); these are the Nature output rules.
    assert plt.rcParams["svg.fonttype"] == "none"
    assert plt.rcParams["pdf.fonttype"] == 42
    assert plt.rcParams["xtick.labelsize"] >= pf.MIN_FS


def test_check_layout_catches_overlapping_text():
    fig, ax = plt.subplots(figsize=(pf.SINGLE, 40 * pf.MM))
    ax.text(0.5, 0.5, "first label", transform=ax.transAxes)
    ax.text(0.5, 0.5, "second label", transform=ax.transAxes)
    assert any("overlap" in p for p in pf.check_layout(fig))
    plt.close(fig)


def test_check_layout_catches_small_text_and_wide_figure():
    fig, ax = plt.subplots(figsize=(pf.WIDTH * 1.2, 40 * pf.MM))
    # Bundled font: macOS's Helvetica.ttc fails to render glyphs this small, which is not what is under test.
    ax.text(0.1, 0.1, "tiny", fontsize=4, fontfamily="DejaVu Sans")
    problems = pf.check_layout(fig)
    assert any("below" in p for p in problems)
    assert any("wider" in p for p in problems)
    plt.close(fig)


def test_clean_figure_passes_and_saves_all_formats(tmp_path):
    fig, ax = plt.subplots(figsize=(pf.SINGLE, 50 * pf.MM))
    fig.subplots_adjust(left=0.2, bottom=0.15, top=0.85)
    pf.box_strip(ax, np.arange(10.0), 0, pf.CATEGORICAL[0])
    ax.set_title("Test: clean panel")
    pf.label(ax, "a")
    assert pf.check_layout(fig) == []
    pf.save(fig, tmp_path, "clean")
    assert sorted(p.suffix for p in tmp_path.iterdir()) == [".pdf", ".png", ".svg"]


def test_require_layout_refuses_bad_layout():
    fig, ax = plt.subplots(figsize=(pf.SINGLE, 40 * pf.MM))
    ax.text(0.5, 0.5, "same", transform=ax.transAxes)
    ax.text(0.5, 0.5, "same", transform=ax.transAxes)
    with pytest.raises(SystemExit):
        pf.require_layout(fig)
    assert pf.require_layout(fig, force=True)
    plt.close(fig)


def test_p_text_and_stars():
    assert pf.p_text(0.0004) == "$P$ < 0.001"
    assert pf.p_text(0.0331, "q") == "$q$ = 0.033"
    assert [pf.stars(p) for p in (0.0005, 0.005, 0.03, 0.2)] == ["***", "**", "*", "n.s."]


def test_text_on_picks_readable_ink():
    assert pf.text_on((0.05, 0.2, 0.42)) == "white"
    assert pf.text_on((1, 1, 1)) == pf.INK
