"""Generate summary plots for the SciFig dataset README."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

BASE = Path(__file__).resolve().parent.parent.parent / "Dataset"
GT = BASE / "groundtruth"
PLOTS_DIR = BASE / "distributions"
PLOTS_DIR.mkdir(exist_ok=True)

SUBFOLDERS = ["bulgarian_only", "chinese_only", "english_only", "german_only", "multi_language"]
SUBFOLDER_LABELS = ["Bulgarian", "Chinese", "English", "German", "Multi-language"]

# Colors
LANG_COLORS = {"English": "#4C72B0", "Bulgarian": "#DD8452", "German": "#55A868", "Chinese": "#C44E52"}
SUBFOLDER_COLORS = ["#DD8452", "#C44E52", "#4C72B0", "#55A868", "#8172B3"]
FIG_TYPE_COLORS = {
    "Line Plot": "#4C72B0",
    "Bar Chart": "#DD8452",
    "Pie Chart": "#55A868",
    "Other": "#8172B3",
    "Heatmap": "#C44E52",
    "Scatter Plot": "#937860",
    "Flow Diagram": "#DA8BC3",
}


def load_data():
    data = {}
    for sf in SUBFOLDERS:
        figures = []
        for fp in sorted((GT / sf).glob("*.json")):
            with open(fp) as f:
                figures.append(json.load(f))
        data[sf] = figures
    return data


def plot_figure_type_distribution(data):
    """Bar chart of figure types across subfolders (stacked)."""
    fig_types = ["Line Plot", "Bar Chart", "Pie Chart", "Other", "Heatmap", "Scatter Plot", "Flow Diagram"]

    counts = {ft: [] for ft in fig_types}
    for sf in SUBFOLDERS:
        sf_types = {}
        for fig in data[sf]:
            ft = fig["figure_type"]
            sf_types[ft] = sf_types.get(ft, 0) + 1
        for ft in fig_types:
            counts[ft].append(sf_types.get(ft, 0))

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(SUBFOLDER_LABELS))
    width = 0.55
    bottom = np.zeros(len(SUBFOLDER_LABELS))

    for ft in fig_types:
        vals = np.array(counts[ft])
        if vals.sum() == 0:
            continue
        ax.bar(x, vals, width, bottom=bottom, label=ft, color=FIG_TYPE_COLORS[ft])
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels(SUBFOLDER_LABELS, fontsize=11)
    ax.set_ylabel("Number of Figures", fontsize=12)
    ax.set_title("Figure Type Distribution by Subset", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right", fontsize=9)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    for i, total in enumerate(bottom):
        ax.text(i, total + 3, str(int(total)), ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "figure_type_distribution.png", dpi=150)
    plt.close(fig)


def plot_annotation_language_distribution(data):
    """Pie chart of annotation language distribution."""
    lang_counts = {}
    for sf in SUBFOLDERS:
        for fig in data[sf]:
            for ann in fig["annotations"]:
                lang = ann["annotation_language"]
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

    labels = list(lang_counts.keys())
    sizes = list(lang_counts.values())
    colors = [LANG_COLORS.get(l, "#999999") for l in labels]

    fig, ax = plt.subplots(figsize=(7, 5.5))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct=lambda p: f"{p:.1f}%\n({int(p * sum(sizes) / 100)})",
        startangle=90, textprops={"fontsize": 11},
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title("Annotation Language Distribution", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "annotation_language_distribution.png", dpi=150)
    plt.close(fig)


def plot_figures_and_annotations_per_subset(data):
    """Grouped bar chart: figures vs annotations per subset."""
    fig_counts = [len(data[sf]) for sf in SUBFOLDERS]
    ann_counts = [sum(len(fig["annotations"]) for fig in data[sf]) for sf in SUBFOLDERS]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(SUBFOLDER_LABELS))
    width = 0.32

    bars1 = ax.bar(x - width / 2, fig_counts, width, label="Figures", color="#4C72B0")
    bars2 = ax.bar(x + width / 2, ann_counts, width, label="Annotations", color="#DD8452")

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4,
                str(int(bar.get_height())), ha="center", fontsize=9, fontweight="bold")
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4,
                str(int(bar.get_height())), ha="center", fontsize=9, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(SUBFOLDER_LABELS, fontsize=11)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title("Figures and Annotations per Subset", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "figures_and_annotations_per_subset.png", dpi=150)
    plt.close(fig)


def plot_annotator_contributions(data):
    """Horizontal bar chart of annotator contributions, colored by language."""
    annotator_lang = {}
    for sf in SUBFOLDERS:
        for fig in data[sf]:
            for ann in fig["annotations"]:
                aid = ann["annotated_by"]
                lang = ann["annotation_language"]
                annotator_lang.setdefault(aid, {})
                annotator_lang[aid][lang] = annotator_lang[aid].get(lang, 0) + 1

    aids = sorted(annotator_lang.keys())
    langs_ordered = ["English", "Bulgarian", "German", "Chinese"]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    y = np.arange(len(aids))
    left = np.zeros(len(aids))

    for lang in langs_ordered:
        vals = np.array([annotator_lang[a].get(lang, 0) for a in aids])
        if vals.sum() == 0:
            continue
        ax.barh(y, vals, left=left, label=lang, color=LANG_COLORS[lang], height=0.6)
        left += vals

    ax.set_yticks(y)
    ax.set_yticklabels([f"Annotator {a}" for a in aids], fontsize=10)
    ax.set_xlabel("Number of Annotations", fontsize=12)
    ax.set_title("Annotator Contributions by Language", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=10)

    for i, total in enumerate(left):
        ax.text(total + 3, i, str(int(total)), va="center", fontsize=9)

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "annotator_contributions.png", dpi=150)
    plt.close(fig)


def plot_annotation_length_distribution(data):
    """Box plot of annotation lengths per subset."""
    lengths_by_subset = {}
    for sf, label in zip(SUBFOLDERS, SUBFOLDER_LABELS):
        lengths = []
        for fig in data[sf]:
            for ann in fig["annotations"]:
                lengths.append(len(ann["annotation"]))
        lengths_by_subset[label] = lengths

    fig, ax = plt.subplots(figsize=(10, 5))
    bp = ax.boxplot(
        [lengths_by_subset[l] for l in SUBFOLDER_LABELS],
        tick_labels=SUBFOLDER_LABELS,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black", markersize=6),
    )
    for patch, color in zip(bp["boxes"], SUBFOLDER_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel("Annotation Length (characters)", fontsize=12)
    ax.set_title("Annotation Length Distribution by Subset", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "annotation_length_distribution.png", dpi=150)
    plt.close(fig)


def main():
    data = load_data()
    plot_figure_type_distribution(data)
    plot_annotation_language_distribution(data)
    plot_figures_and_annotations_per_subset(data)
    plot_annotator_contributions(data)
    plot_annotation_length_distribution(data)
    print(f"Plots saved to {PLOTS_DIR}/")


if __name__ == "__main__":
    main()
