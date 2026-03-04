import pandas as pd
import seaborn as sns
import matplotlib
# use Agg backend so script works on headless machines (no GUI)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import os


def load_metrics(path_pattern: str) -> pd.DataFrame:
    """Load one or more CSV files matching a glob pattern into a DataFrame."""
    files = glob.glob(path_pattern)
    if not files:
        raise FileNotFoundError(f"No files match pattern {path_pattern}")
    df_list = []
    for f in files:
        print(f"Loading {f}")
        df_list.append(pd.read_csv(f))
    df = pd.concat(df_list, ignore_index=True)
    return df


def heatmap_metrics(
    df: pd.DataFrame,
    metrics: list[str] | None = None,
    normalize: bool = True,
    cmap: str = "RdYlGn_r",
    output: str | None = None,
):
    """Create a heatmap of the given metrics indexed by run.

    If ``normalize`` is True each column is scaled to 0..1 so that colors
    represent relative performance.  The raw values are annotated on the map.
    """
    if metrics is None:
        # select common metrics present in dataset
        candidates = [
            "mIoU",
            "Pixel Accuracy",
            "Val Loss",
            "Dice",
            "IoU Cat",
            "IoU Human",
            "IoU Road",
        ]
        metrics = [m for m in candidates if m in df.columns]
    data = df.set_index("Run")[metrics]
    if normalize:
        # avoid divide by zero
        norm_data = (data - data.min()) / (data.max() - data.min())
    else:
        norm_data = data.copy()

    plt.figure(figsize=(10, max(4, len(data) * 0.5)))
    sns.heatmap(
        norm_data,
        annot=data.round(3),
        cmap=cmap,
        linewidths=0.5,
        cbar_kws={"label": "Normalized" if normalize else "Value"},
    )
    plt.title("Segmentation Experiment Metrics")
    plt.ylabel("")
    plt.tight_layout()
    if output:
        plt.savefig(output)
        print(f"Saved heatmap to {output}")
    else:
        plt.show()


def barplot_metrics(
    df: pd.DataFrame,
    metrics: list[str] | None = None,
    output_dir: str | None = None,
):
    """Create individual horizontal bar plots for each metric."""
    if metrics is None:
        candidates = [
            "mIoU",
            "Pixel Accuracy",
            "Val Loss",
            "Dice",
            "IoU Cat",
            "IoU Human",
            "IoU Road",
        ]
        metrics = [m for m in candidates if m in df.columns]

    for m in metrics:
        plt.figure(figsize=(8, max(3, len(df) * 0.3)))
        order = df.sort_values(m, ascending=False)["Run"]
        sns.barplot(data=df, x=m, y="Run", order=order, palette="viridis")
        plt.title(f"{m} by run")
        plt.tight_layout()
        if output_dir:
            fname = os.path.join(output_dir, f"{m.replace(' ', '_')}.png")
            plt.savefig(fname)
            print(f"Saved bar plot to {fname}")
        else:
            plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Visualize segmentation experiment metrics CSV files as heatmaps."
    )
    parser.add_argument(
        "pattern",
        help="glob pattern for metrics CSV files (e.g. 'outputs/segmentation_experiments_metrics*.csv')",
    )
    parser.add_argument(
        "--output",
        help="optional file path to save the generated heatmap (e.g. heatmap.png)",
        default=None,
    )
    parser.add_argument(
        "--barplots",
        dest="barplots",
        action="store_true",
        help="also generate individual bar plots for each metric",
    )
    parser.add_argument(
        "--output-dir",
        help="directory where bar plot images will be saved (required if --barplots)",
        default=None,
    )
    parser.add_argument(
        "--no-normalize",
        dest="normalize",
        action="store_false",
        help="do not normalize columns when coloring",
    )

    args = parser.parse_args()
    df = load_metrics(args.pattern)
    if args.output or not args.barplots:
        # generate heatmap if requested or if no barplots requested
        heatmap_metrics(df, normalize=args.normalize, output=args.output)
    if args.barplots:
        if not args.output_dir:
            parser.error("--barplots requires --output-dir to be specified")
        barplot_metrics(df, output_dir=args.output_dir)
