import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global style configurations
STYLE_CONFIG = {
    # Colors
    "background_color": "#FFF9E6",
    "text_color": "#2F4F4F",
    "grid_color": "#666666",
    "spine_color": "#666666",
    # Font sizes - Adjusted for compact display
    "title_size": 48,
    "axis_label_size": 32,
    "tick_label_size": 24,
    "annotation_size": 24,  # Reduced for more compact labels
    # Font weights
    "title_weight": "bold",
    "label_weight": "bold",
    "annotation_weight": "bold",
    # Line properties
    "spine_width": 2.0,
    "grid_alpha": 0.15,
    "line_alpha": 0.9,
    "line_width": 2.0,
    # Spacing
    "title_pad": 40,
    "annotation_pad": 4,  # Reduced padding for more compact labels
    # Bar properties
    "bar_height": 1.0,
    "bar_alpha": 0.85,
    # Figure size - Changed to 9:16 aspect ratio for mobile
    "figure_size": (9, 16),
    # Text offset
    "text_y_offset": 5,  # New: control text position above lines
}

# Score threshold configurations
SCORE_THRESHOLDS = [
    (539, "本科第一批", "#FF6B6B"),
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

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

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

    # Create custom color gradients with more vibrant colors
    colors = plt.cm.RdPu(
        np.linspace(0.1, 0.8, len(df))
    )  # Adjusted color range for more vibrancy

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

    # Add title with custom style and increased emphasis
    plt.title(
        "高考分数分布图",
        fontsize=STYLE_CONFIG["title_size"],
        pad=STYLE_CONFIG["title_pad"],
        color=STYLE_CONFIG["text_color"],
        fontweight=STYLE_CONFIG["title_weight"],
        bbox=dict(
            facecolor=STYLE_CONFIG["background_color"],
            edgecolor="none",
            alpha=0.8,
            pad=10,
        ),
    )

    # Adjust axis labels with more emphasis
    plt.xlabel(
        "人数",
        fontsize=STYLE_CONFIG["axis_label_size"],
        color=STYLE_CONFIG["text_color"],
        fontweight=STYLE_CONFIG["label_weight"],
        labelpad=20,
    )
    plt.ylabel(
        "分数",
        fontsize=STYLE_CONFIG["axis_label_size"],
        color=STYLE_CONFIG["text_color"],
        fontweight=STYLE_CONFIG["label_weight"],
        labelpad=20,
    )

    # Add score lines with enhanced style and visibility
    for score, label, color in SCORE_THRESHOLDS:
        plt.axhline(
            y=score,
            color=color,
            linestyle="--",
            alpha=STYLE_CONFIG["line_alpha"],
            linewidth=STYLE_CONFIG["line_width"],
            zorder=2,  # Ensure lines are above the grid
        )
        # Position text above the line
        plt.text(
            max_count * 0.85,
            score + STYLE_CONFIG["text_y_offset"],  # Use consistent offset
            f"{label}",
            fontsize=STYLE_CONFIG["annotation_size"],
            fontweight=STYLE_CONFIG["annotation_weight"],
            color=color,
            bbox=dict(
                facecolor=STYLE_CONFIG["background_color"],
                edgecolor=color,
                alpha=0.95,
                pad=STYLE_CONFIG["annotation_pad"],
                linewidth=1.5,
                boxstyle="round,pad=0.5",
            ),
            verticalalignment="bottom",
            zorder=3,  # Ensure text is above everything
        )

    # Add median line and score with enhanced visibility
    plt.axhline(
        y=median_score,
        color=STYLE_CONFIG["text_color"],
        linestyle="--",
        alpha=STYLE_CONFIG["line_alpha"],
        linewidth=STYLE_CONFIG["line_width"],
        zorder=2,
    )
    plt.text(
        -max_count * 1.2,
        median_score + STYLE_CONFIG["text_y_offset"],  # Use consistent offset
        f"中位数",
        fontsize=STYLE_CONFIG["annotation_size"],
        fontweight=STYLE_CONFIG["annotation_weight"],
        color=STYLE_CONFIG["text_color"],
        bbox=dict(
            facecolor=STYLE_CONFIG["background_color"],
            edgecolor=STYLE_CONFIG["text_color"],
            alpha=0.95,
            pad=STYLE_CONFIG["annotation_pad"],
            linewidth=1.5,
            boxstyle="round,pad=0.5",
        ),
        verticalalignment="bottom",
        zorder=3,
    )

    # Adjust the axis with more padding
    plt.xlim(-max_count * 1.3, max_count * 1.3)

    # Remove all spines
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # Add subtle grid
    plt.grid(
        True,
        axis="y",
        alpha=STYLE_CONFIG["grid_alpha"],
        color=STYLE_CONFIG["grid_color"],
        linestyle=":",
        zorder=1,  # Ensure grid is at the bottom
    )

    # Customize tick labels with larger font and more spacing
    plt.gca().set_xticks([-max_count, -max_count // 2, 0, max_count // 2, max_count])
    plt.gca().set_xticklabels([max_count, max_count // 2, 0, max_count // 2, max_count])
    plt.tick_params(
        colors=STYLE_CONFIG["text_color"],
        labelsize=STYLE_CONFIG["tick_label_size"],
        width=0,  # Remove tick marks
        length=0,  # Remove tick marks
        pad=10,
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

    # Log the output file path
    logging.info(f"Score distribution plot saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    data_path = "data/processed/四川省204年高考一分一段表公布.csv"
    output_path = "output/visualizations/高考分数分布图.png"
    create_score_distribution_plot(data_path, output_path)
