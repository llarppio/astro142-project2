import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

from make_rgb_mosaic import build_rgb_cube


def cutout_square(rgb, x_center, y_center, half_size):
    """
    Return a square cutout around (x_center, y_center) in pixel coordinates.
    """
    h, w, _ = rgb.shape

    x0 = int(max(0, x_center - half_size))
    x1 = int(min(w, x_center + half_size))
    y0 = int(max(0, y_center - half_size))
    y1 = int(min(h, y_center + half_size))

    sub = rgb[y0:y1, x0:x1, :]
    return sub, x0, y0, x1 - x0, y1 - y0


def main():
    # Build RGB cube and WCS from make_rgb script
    rgb, r_wcs, hmin, wmin = build_rgb_cube()

    fig = plt.figure(figsize=(12, 6))
    gs = fig.add_gridspec(
        3,
        4,
        width_ratios=[3.0, 0.1, 1.0, 1.0],
        hspace=0.15,
        wspace=0.35,
    )

    # Main HUDF mosaic (panel a)
    ax_main = fig.add_subplot(gs[:, 0], projection=r_wcs)
    ax_main.imshow(rgb, origin="lower")
    ax_main.set_xlabel("RA")
    ax_main.set_ylabel("Dec")
    ax_main.set_title("HUDF RGB with Inset Regions")
    ax_main.grid(color="white", alpha=0.2, linestyle=":")

    ax_main.text(
        0.02,
        0.97,
        "(a)",
        transform=ax_main.transAxes,
        color="white",
        fontsize=11,
        ha="left",
        va="top",
    )

    # six regions in fractional image coordinates (x_frac, y_frac)
    regions = [
        ("(b)", 0.43, 0.72),
        ("(c)", 0.60, 0.70),
        ("(d)", 0.30, 0.48),
        ("(e)", 0.55, 0.50),
        ("(f)", 0.50, 0.25),
        ("(g)", 0.60, 0.40),
    ]

    # Inset axes grid on the right: 3 rows × 2 columns
    inset_positions = [
        gs[0, 2],
        gs[0, 3],
        gs[1, 2],
        gs[1, 3],
        gs[2, 2],
        gs[2, 3],
    ]

    half_size = 175  # make higher for tighter zooms!

    for (label, x_frac, y_frac), pos in zip(regions, inset_positions):
        x_center = x_frac * wmin
        y_center = y_frac * hmin

        sub, x0, y0, width, height = cutout_square(
            rgb, x_center, y_center, half_size
        )

        # Draw the indicator box on the main panel in pixel coordinates
        rect = Rectangle(
            (x0, y0),
            width,
            height,
            edgecolor="white",
            facecolor="none",
            linewidth=1.2,
        )
        ax_main.add_patch(rect)

        # Inset panel itself
        ax_ins = fig.add_subplot(pos)
        ax_ins.imshow(sub, origin="lower")
        ax_ins.set_xticks([])
        ax_ins.set_yticks([])
        ax_ins.text(
            0.02,
            0.95,
            label,
            transform=ax_ins.transAxes,
            color="white",
            fontsize=11,
            ha="left",
            va="top",
        )

    plt.savefig("../plots/xdf_multi_panel_insets.png", dpi=300)
    print("saved ../plots/xdf_multi_panel_insets.png")


if __name__ == "__main__":
    main()

