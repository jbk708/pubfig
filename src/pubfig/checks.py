"""Layout checks to run before saving: a figure that fails should not be written."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PathCollection

from .style import MIN_FS, WIDTH


def _scatter_points(fig):
    """(axes, centres px, radii px) for every clipped scatter collection drawn in an axes (not legend handles).
    Collections drawn with clip_on=False (edge arrows) are deliberate and skipped."""
    out = []
    for ax in fig.axes:
        for coll in ax.collections:
            if not isinstance(coll, PathCollection) or not coll.get_visible() or not coll.get_clip_on():
                continue
            off = coll.get_offsets()
            if len(off) == 0:
                continue
            xy = coll.get_offset_transform().transform(np.asarray(off, float))
            s = np.broadcast_to(coll.get_sizes() if len(coll.get_sizes()) else [36.0], (len(xy),))
            out.append((ax, xy, np.sqrt(s) / 2 * fig.dpi / 72))
    return out


def _undrawn_tick_labels(fig):
    """ids of tick labels whose tick lies outside the axis view: matplotlib keeps them but never draws them."""
    ids = set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            span = (hi - lo) * 1e-9
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                loc = tick.get_loc()
                if loc is None or not lo - span <= loc <= hi + span:
                    ids.update({id(tick.label1), id(tick.label2)})
    return ids


def check_layout(fig, max_width=WIDTH, min_fs=MIN_FS, tol_px=1.0, points=True):
    """Return a list of problems; an empty list means the layout passed.

    Checks: text overlapping text, text off the page, text below min_fs, figure wider than max_width, and (with
    points=True) text drawn over a scatter point and scatter points clipped by their axes. Overlaps are judged on
    axis-aligned text boxes, so rotated labels can report false overlaps; prefer two-line horizontal labels.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    hidden = _undrawn_tick_labels(fig)
    texts = [t for t in fig.findobj(plt.Text) if t.get_visible() and t.get_text().strip() and id(t) not in hidden]
    boxes = [(t, t.get_window_extent(r)) for t in texts]
    page = fig.bbox
    problems = []
    for i, (t, b) in enumerate(boxes):
        if t.get_fontsize() < min_fs - 1e-9:
            problems.append(f"below {min_fs} pt: {t.get_text()!r} ({t.get_fontsize()} pt)")
        if b.x0 < page.x0 - tol_px or b.x1 > page.x1 + tol_px or b.y0 < page.y0 - tol_px or b.y1 > page.y1 + tol_px:
            problems.append(f"off page: {t.get_text()!r}")
        for t2, b2 in boxes[i + 1:]:
            if min(b.x1, b2.x1) - max(b.x0, b2.x0) > tol_px and min(b.y1, b2.y1) - max(b.y0, b2.y0) > tol_px:
                problems.append(f"overlap: {t.get_text()!r} vs {t2.get_text()!r}")
    if points:
        for ax, xy, rad in _scatter_points(fig):
            a = ax.get_window_extent(r)
            out = (xy[:, 0] < a.x0 - tol_px) | (xy[:, 0] > a.x1 + tol_px) | (xy[:, 1] < a.y0 - tol_px) | \
                  (xy[:, 1] > a.y1 + tol_px)
            if out.any():
                problems.append(f"{out.sum()} point(s) outside their axes (clipped) in {ax.get_title()!r}")
            for t, b in boxes:
                hit = (xy[:, 0] + rad > b.x0 + tol_px) & (xy[:, 0] - rad < b.x1 - tol_px) & \
                      (xy[:, 1] + rad > b.y0 + tol_px) & (xy[:, 1] - rad < b.y1 - tol_px)
                if hit.any():
                    problems.append(f"text on {hit.sum()} point(s): {t.get_text()!r}")
    if fig.get_figwidth() > max_width + 1e-6:
        problems.append(f"wider than {max_width * 25.4:.0f} mm")
    return problems


def require_layout(fig, force=False, **kw):
    """Raise SystemExit listing the problems if check_layout fails (unless force)."""
    problems = check_layout(fig, **kw)
    if problems and not force:
        raise SystemExit("layout check failed, nothing written:\n  " + "\n  ".join(problems))
    return problems
