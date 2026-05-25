"""Shared model visual identity for all figures and tables.

Each model has a unique color + marker combination.
Same-family models (Qwen) use same color family with different shades/shapes.
"""

# Model visual identity
MODEL_IDENTITY = {
    "gpt-5.2": {
        "label": "GPT-5.2",
        "short": "GPT",
        "color": "#1f77b4",       # blue
        "marker": "o",            # circle
        "latex_marker": r"$\bullet$",
        "latex_color": "blue!80",
    },
    "gemini-3.1-pro": {
        "label": "Gemini",
        "short": "Gem",
        "color": "#2ca02c",       # green
        "marker": "s",            # square
        "latex_marker": r"$\blacksquare$",
        "latex_color": "green!70!black",
    },
    "llama4-maverick": {
        "label": "Llama 4",
        "short": "Lla",
        "color": "#ff7f0e",       # orange
        "marker": "^",            # triangle up
        "latex_marker": r"$\blacktriangle$",
        "latex_color": "orange!90",
    },
    "qwen3-vl-235b-a22b": {
        "label": "Qwen-235B",
        "short": "Q235",
        "color": "#9467bd",       # purple
        "marker": "o",            # circle
        "latex_marker": r"$\bullet$",
        "latex_color": "violet!80",
    },
    "qwen3-vl-30b-a3b": {
        "label": "Qwen-30B",
        "short": "Q30",
        "color": "#c5b0d5",       # light purple
        "marker": "D",            # diamond
        "latex_marker": r"$\blacklozenge$",
        "latex_color": "violet!50",
    },
    "qwen3-vl-8b": {
        "label": "Qwen-8B",
        "short": "Q8",
        "color": "#7b4ea3",       # dark purple
        "marker": "v",            # triangle down
        "latex_marker": r"$\blacktriangledown$",
        "latex_color": "violet!60",
    },
    "gemma3-27b-it": {
        "label": "Gemma",
        "short": "Gma",
        "color": "#17becf",       # teal
        "marker": "p",            # pentagon
        "latex_marker": r"$\star$",
        "latex_color": "teal!80",
    },
    "phi-4-multimodal": {
        "label": "Phi-4",
        "short": "Phi",
        "color": "#d62728",       # red
        "marker": "X",            # x marker
        "latex_marker": r"$\times$",
        "latex_color": "red!80",
    },
}

# Display order (by baseline MQM, descending)
MODEL_ORDER = [
    "gpt-5.2",
    "gemini-3.1-pro",
    "llama4-maverick",
    "qwen3-vl-235b-a22b",
    "qwen3-vl-8b",
    "qwen3-vl-30b-a3b",
    "gemma3-27b-it",
    "phi-4-multimodal",
]
