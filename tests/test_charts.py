import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.colors import Normalize, to_rgba

import pubfig as pf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
import gallery  # noqa: E402


@pytest.fixture
def ax():
    fig, ax = plt.subplots(figsize=(pf.SINGLE, 60 * pf.MM))
    yield ax
    plt.close(fig)


def test_gallery_passes_layout_check(tmp_path):
    # Every chart form drawn together must satisfy the print rules the package enforces on real figures.
    fig = gallery.build()
    assert pf.check_layout(fig) == []
    pf.save(fig, tmp_path, "gallery")
    assert (tmp_path / "gallery.svg").exists()


def test_heatmap_ink_follows_cell_contrast(ax):
    # Values must stay readable: white on the dark end of the ramp, dark ink on the light end.
    pf.heatmap(ax, [[0.0, 1.0]], ["r"], ["light", "dark"], norm=Normalize(0, 1))
    inks = {t.get_text(): t.get_color() for t in ax.texts}
    assert inks["0.00"] == pf.INK and inks["1.00"] == "white"


def test_heatmap_leaves_missing_cells_unlabelled(ax):
    pf.heatmap(ax, [[0.2, np.nan]], ["r"], ["a", "b"])
    assert [t.get_text() for t in ax.texts] == ["0.20"]


def test_stacked_bars_reach_row_totals(ax):
    f = np.array([[0.5, 0.3, 0.2], [0.1, 0.1, 0.8]])
    pf.stacked_bars(ax, f, pf.CATEGORICAL)
    tops = [p.get_y() + p.get_height() for p in ax.patches]
    assert max(tops) == pytest.approx(1.0)


def test_sig_colour_encodes_significance():
    c = pf.CATEGORICAL[0]
    assert pf.sig_colour(c, 0.01) == c
    assert pf.sig_colour(c, 0.2) == to_rgba(c, pf.NS_ALPHA)
    assert pf.sig_colour(c, float("nan")) == pf.PH


def test_swarm_offsets_separate_ties_and_are_deterministic():
    v = [1, 1, 1, 5]
    off = pf.swarm_offsets(v)
    assert len(set(off[:3])) == 3 and off[3] == 0
    assert np.array_equal(off, pf.swarm_offsets(v))


def test_permutation_p_never_zero():
    # +1 correction: an observed value beyond every shuffle gets 1/(n+1), never 0.
    assert pf.permutation_p(np.zeros(99), 1.0) == pytest.approx(0.01)
    assert pf.permutation_p(np.ones(99), 0.0) == pytest.approx(1.0)


def test_interval_point_marks_offaxis_estimate(ax):
    # An estimate outside the axis must stay visible as an edge arrow with its value printed, not vanish.
    pf.interval_point(ax, -0.9, 0, 0.1, 0.1, pf.CATEGORICAL[0], (-0.5, 0.5))
    assert any("0.90" in t.get_text() for t in ax.texts)


def test_volcano_classifies_by_q_and_effect(ax):
    sig = pf.volcano(ax, [2.0, -2.0, 0.2, 2.0], [0.001, 0.001, 0.001, 0.5], effect_min=1)
    assert sig.tolist() == [True, True, False, False]


def test_ordination_names_axes_with_variance(ax):
    xy = np.random.default_rng(0).normal(size=(12, 2))
    pf.ordination(ax, xy, ["a"] * 6 + ["b"] * 6, {"a": pf.CATEGORICAL[0], "b": pf.CATEGORICAL[1]}, var_pct=(30.4, 12))
    assert ax.get_xlabel() == "PC1 (30%)" and len(ax.patches) == 2


def test_check_layout_flags_text_on_points():
    fig, ax = plt.subplots(figsize=(pf.SINGLE, 50 * pf.MM))
    fig.subplots_adjust(left=0.2, bottom=0.2)
    ax.scatter([0.5], [0.5], s=40)
    ax.text(0.5, 0.5, "on the dot", ha="center", va="center")
    assert any("text on" in p for p in pf.check_layout(fig))
    plt.close(fig)


def test_check_layout_ignores_undrawn_ticks():
    # matplotlib keeps tick labels just outside the view (e.g. log axes); they are never drawn, so not errors.
    fig, ax = plt.subplots(figsize=(pf.SINGLE, 50 * pf.MM))
    fig.subplots_adjust(left=0.2, bottom=0.2)
    ax.set_yscale("log")
    ax.set_ylim(1, 10)
    assert pf.check_layout(fig) == []
    plt.close(fig)
