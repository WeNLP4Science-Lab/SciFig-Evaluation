"""Regenerate transforms gallery figure for thesis.

Shows 9 transforms + 2 in-paper context views (no grayscale).
Output: thesis/main/figures/transformations_gallery.pdf
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

BASE = "adversarial_experiments/figures/english_only/english_fig_033"
PDF_OUT = "thesis/main/figures/transformations_gallery.pdf"

# 11 panels: 3 rows of 3, then 1 row of 2
PANELS = [
    # Row 1
    (f"{BASE}/original.png", "Original", "clean figure"),
    (f"{BASE}/transforms/jpeg_compression.png", "JPEG compression", "q = 15"),
    (f"{BASE}/transforms/noise.png", "Gaussian noise", "\u03c3 = 30"),
    # Row 2
    (f"{BASE}/transforms/aspect_ratio.png", "Aspect ratio", "\u00d71.2"),
    (f"{BASE}/transforms/low_contrast.png", "Low contrast", "\u00d70.5"),
    (f"{BASE}/transforms/rotation.png", "Rotation", "30\u00b0"),
    # Row 3
    (f"{BASE}/transforms/axis_blurred.png", "Axis blur", "strip 15/15/12%"),
    (f"{BASE}/transforms/selective_blur.png", "Selective blur", "one in-chart element"),
    (None, None, None),  # placeholder
    # Row 4 (wider panels)
    (f"{BASE}/original_in_paper.jpeg", "Original in paper", "figure in page context"),
    (f"{BASE}/transforms/blurred_in_paper.png", "Blurred in paper", "figure region blurred"),
]


def main():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 7,
        "axes.linewidth": 0.4,
    })

    fig = plt.figure(figsize=(7.0, 9.0))

    # Title
    fig.text(0.5, 0.97, "Adversarial visual transforms on a single figure (english_fig_033)",
             ha="center", fontsize=9, fontweight="bold")
    fig.text(0.5, 0.955, "Nine parameter-fixed transforms plus two in-paper context views.",
             ha="center", fontsize=7, fontstyle="italic", color="#555555")

    # Rows 1-3: 3 columns
    for i in range(9):
        if PANELS[i][0] is None:
            continue
        row, col = divmod(i, 3)
        # y positions for rows 0,1,2
        y_top = 0.93 - row * 0.24
        x_left = 0.03 + col * 0.33
        ax = fig.add_axes([x_left, y_top - 0.20, 0.30, 0.20])

        img = mpimg.imread(PANELS[i][0])
        ax.imshow(img)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#A0A0A0")
            spine.set_linewidth(0.5)

        # Title above
        ax.set_title(PANELS[i][1], fontsize=7, fontweight="bold", pad=3)
        # Subtitle below
        ax.text(0.5, -0.08, PANELS[i][2], transform=ax.transAxes,
                ha="center", fontsize=6, fontstyle="italic", color="#555555")

    # Row 4: 2 wider panels
    for j in range(2):
        path, title, sub = PANELS[9 + j]
        x_left = 0.03 + j * 0.48
        y_top = 0.93 - 3 * 0.24
        ax = fig.add_axes([x_left, y_top - 0.20, 0.44, 0.20])

        img = mpimg.imread(path)
        ax.imshow(img)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#A0A0A0")
            spine.set_linewidth(0.5)

        ax.set_title(title, fontsize=7, fontweight="bold", pad=3)
        ax.text(0.5, -0.08, sub, transform=ax.transAxes,
                ha="center", fontsize=6, fontstyle="italic", color="#555555")

    fig.savefig(PDF_OUT, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {PDF_OUT}")


if __name__ == "__main__":
    main()
