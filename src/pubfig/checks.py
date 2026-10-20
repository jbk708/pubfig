"""Layout checks to run before saving: a figure that fails should not be written."""
import matplotlib.pyplot as plt

from .style import MIN_FS, WIDTH


def check_layout(fig, max_width=WIDTH, min_fs=MIN_FS, tol_px=1.0):
    """Return a list of problems: text overlapping text, text off the page, text below min_fs, figure too wide.

    Overlaps are judged on axis-aligned text boxes, so rotated labels can report false overlaps;
    prefer two-line horizontal labels to rotation. An empty list means the layout passed.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    texts = [t for t in fig.findobj(plt.Text) if t.get_visible() and t.get_text().strip()]
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
    if fig.get_figwidth() > max_width + 1e-6:
        problems.append(f"wider than {max_width * 25.4:.0f} mm")
    return problems


def require_layout(fig, force=False, **kw):
    """Raise SystemExit listing the problems if check_layout fails (unless force)."""
    problems = check_layout(fig, **kw)
    if problems and not force:
        raise SystemExit("layout check failed, nothing written:\n  " + "\n  ".join(problems))
    return problems
