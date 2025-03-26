import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties

# Global style configurations
STYLE_CONFIG = {
    # Colors
    "background_color": "#FFF9E6",
    "text_color": "#2F4F4F",
    "grid_color": "#666666",
    "spine_color": "#666666",
    # Font sizes
    "title_size": 36,
    "axis_label_size": 20,
    "tick_label_size": 16,
    "annotation_size": 18,
    # Font weights
    "title_weight": "bold",
    "label_weight": "bold",
    "annotation_weight": "bold",
    # Line properties
    "spine_width": 1.5,
    "grid_alpha": 0.2,
    "line_alpha": 0.8,
    "line_width": 2.5,
    # Spacing
    "title_pad": 30,
    "annotation_pad": 5,
    # Bar properties
    "bar_height": 0.9,
    "bar_alpha": 0.8,
    # Figure size
    "figure_size": (14, 18),
}

# Score threshold configurations
SCORE_THRESHOLDS = [
    (539, "本科第一批", "#FF6B6B"),
    (495, "本科线", "#FF8F00"),
    (459, "本科第二批", "#4CAF50"),
    (150, "专科批", "#2196F3"),
]


def calculate_percentile_score(df, percentile):
    """Calculate score at given percentile based on cumulative counts"""
    total_students = df["累计人数"].max()
    target_count = total_students * (percentile / 100)
    return df[df["累计人数"] >= target_count].iloc[0]["score"]


def create_score_distribution_plot(data_path, output_path):
    # Read the data
    df = pd.read_csv(data_path)

    # Process the score range data
    def extract_score(score_range):
        if "-" in str(score_range):
            return int(score_range.split("-")[0])
        return int(score_range)

    df["score"] = df["分数"].apply(extract_score)

    # Calculate median
    median_score = calculate_percentile_score(df, 50)

    # Create the figure with light yellow background
    plt.figure(figsize=STYLE_CONFIG["figure_size"])

    # Set background color
    plt.rcParams["figure.facecolor"] = STYLE_CONFIG["background_color"]
    plt.rcParams["axes.facecolor"] = STYLE_CONFIG["background_color"]

    # Set font configurations
    plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False

    # Create the symmetric distribution plot
    max_count = df["人数"].max()

    # Create custom color gradients (purple-blue color scheme)
    colors = plt.cm.RdPu(np.linspace(0.2, 0.7, len(df)))

    # Plot bars with enhanced visual effect
    bars_right = plt.barh(
        df["score"],
        df["人数"],
        height=STYLE_CONFIG["bar_height"],
        color=colors,
        alpha=STYLE_CONFIG["bar_alpha"],
        edgecolor="none",
    )
    bars_left = plt.barh(
        df["score"],
        -df["人数"],
        height=STYLE_CONFIG["bar_height"],
        color=colors,
        alpha=STYLE_CONFIG["bar_alpha"],
        edgecolor="none",
    )

    # Add title with custom style
    plt.title(
        "高考分数分布图",
        fontsize=STYLE_CONFIG["title_size"],
        pad=STYLE_CONFIG["title_pad"],
        color=STYLE_CONFIG["text_color"],
        fontweight=STYLE_CONFIG["title_weight"],
    )

    plt.xlabel(
        "人数",
        fontsize=STYLE_CONFIG["axis_label_size"],
        color=STYLE_CONFIG["text_color"],
        fontweight=STYLE_CONFIG["label_weight"],
    )
    plt.ylabel(
        "分数",
        fontsize=STYLE_CONFIG["axis_label_size"],
        color=STYLE_CONFIG["text_color"],
        fontweight=STYLE_CONFIG["label_weight"],
    )

    # Add score lines with enhanced style
    for score, label, color in SCORE_THRESHOLDS:
        plt.axhline(
            y=score,
            color=color,
            linestyle="--",
            alpha=STYLE_CONFIG["line_alpha"],
            linewidth=STYLE_CONFIG["line_width"],
        )
        plt.text(
            max_count * 0.82,
            score,
            f"{label} ({score})",
            fontsize=STYLE_CONFIG["annotation_size"],
            fontweight=STYLE_CONFIG["annotation_weight"],
            color=color,
            bbox=dict(
                facecolor=STYLE_CONFIG["background_color"],
                edgecolor="none",
                alpha=STYLE_CONFIG["line_alpha"],
                pad=STYLE_CONFIG["annotation_pad"],
            ),
        )

    # Add median score
    plt.text(
        -max_count * 1.15,
        median_score,
        f"中位数: {median_score}",
        fontsize=STYLE_CONFIG["annotation_size"],
        fontweight=STYLE_CONFIG["annotation_weight"],
        color=STYLE_CONFIG["text_color"],
        bbox=dict(
            facecolor=STYLE_CONFIG["background_color"],
            edgecolor="none",
            alpha=STYLE_CONFIG["line_alpha"],
            pad=STYLE_CONFIG["annotation_pad"],
        ),
    )

    # Adjust the axis
    plt.xlim(-max_count * 1.2, max_count * 1.2)

    # Remove spines and customize remaining ones
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_color(STYLE_CONFIG["spine_color"])
    plt.gca().spines["bottom"].set_color(STYLE_CONFIG["spine_color"])
    plt.gca().spines["left"].set_linewidth(STYLE_CONFIG["spine_width"])
    plt.gca().spines["bottom"].set_linewidth(STYLE_CONFIG["spine_width"])

    # Add subtle grid
    plt.grid(
        True,
        axis="y",
        alpha=STYLE_CONFIG["grid_alpha"],
        color=STYLE_CONFIG["grid_color"],
        linestyle=":",
    )

    # Customize tick labels with larger font
    plt.gca().set_xticks([-max_count, -max_count // 2, 0, max_count // 2, max_count])
    plt.gca().set_xticklabels([max_count, max_count // 2, 0, max_count // 2, max_count])
    plt.tick_params(
        colors=STYLE_CONFIG["text_color"],
        labelsize=STYLE_CONFIG["tick_label_size"],
        width=STYLE_CONFIG["spine_width"],
        length=6,
    )

    # Save the plot with higher quality
    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
        facecolor=STYLE_CONFIG["background_color"],
    )
    plt.close()


if __name__ == "__main__":
    data_path = "data/processed/四川省204年高考一分一段表公布.csv"
    output_path = "output/figures/score_distribution.png"
    create_score_distribution_plot(data_path, output_path)
