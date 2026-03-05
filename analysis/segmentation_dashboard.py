from pathlib import Path
import argparse

import pandas as pd
import plotly.graph_objects as go


def build_dashboard(csv_path: Path, output_html: Path) -> None:
    df = pd.read_csv(csv_path)

    metrics = [
        "mIoU",
        "Dice",
        "Dice background",
        "Dice Cat",
        "Dice Human",
        "Dice Road",
        "IoU background",
        "IoU Cat",
        "IoU Human",
        "IoU Road",
        "Train Time (min)",
    ]

    # normalise only training time to [0, 1] so that
    # it shares a comparable scale with the other metrics.
    time_col = "Train Time (min)"
    time_min = df[time_col].min()
    time_max = df[time_col].max()

    def maybe_normalise(m: str, value: float) -> float:
        if m != time_col:
            return value
        if pd.isna(value) or pd.isna(time_min) or pd.isna(time_max):
            return float("nan")
        if time_max == time_min:
            return 0.5
        return (value - time_min) / (time_max - time_min)

    background_x = []
    background_y = []
    background_text = []

    for _, row in df.iterrows():
        label = f"{row['Model']} | {row['Run']}"
        for m in metrics:
            norm_val = maybe_normalise(m, row[m])
            background_x.append(norm_val)
            background_y.append(m)
            background_text.append(label)

    background_trace = go.Scatter(
        x=background_x,
        y=background_y,
        mode="markers",
        marker=dict(size=6, color="rgba(129, 140, 248, 0.45)"),
        name="Diğer runlar",
        hovertemplate="%{y}<br>Value: %{x:.3f}<br>%{text}<extra></extra>",
        text=background_text,
    )

    def metric_values(row):
        return [maybe_normalise(m, row[m]) for m in metrics]

    first_row = df.iloc[0]

    highlight_trace = go.Scatter(
        x=metric_values(first_row),
        y=metrics,
        mode="markers+lines",
        marker=dict(
            size=14,
            color="#0f172a",
            line=dict(color="#38bdf8", width=3),
            symbol="square",
        ),
        line=dict(color="#38bdf8", width=2),
        name=f"Seçili: {first_row['Model']} | {first_row['Run']}",
        hovertemplate="%{y}<br>Value: %{x:.3f}<br>%{text}<extra></extra>",
        text=[f"{first_row['Model']} | {first_row['Run']}"] * len(metrics),
    )

    fig = go.Figure(data=[background_trace, highlight_trace])

    buttons = []
    for _, row in df.iterrows():
        label = f"{row['Model']} | {row['Run']}"
        x_vals = metric_values(row)
        text_vals = [label] * len(metrics)

        buttons.append(
            dict(
                label=label,
                method="update",
                args=[
                    {
                        "x": [background_x, x_vals],
                        "y": [background_y, metrics],
                        "text": [background_text, text_vals],
                    },
                    {
                        "title": f"Segmentation model evaluation: {label}",
                    },
                ],
            )
        )

    n_rows = len(metrics)

    fig.update_layout(
        title=dict(
            text="Interactive Model Comparison",
            x=0.01,
            xanchor="left",
        ),
        xaxis=dict(
            title="Metrik değeri (0–1)",
            range=[0, 1.05],
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.15)",
            zeroline=False,
        ),
        yaxis=dict(
            title="Metrikler",
            categoryorder="array",
            categoryarray=metrics[::-1],
        ),
        plot_bgcolor="#020617",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                showactive=True,
                x=0.01,
                xanchor="left",
                y=1.15,
                yanchor="top",
            )
        ],
        margin=dict(l=120, r=80, t=80, b=60),
        shapes=[
            dict(
                type="line",
                x0=1.0,
                x1=1.0,
                y0=-0.5,
                y1=n_rows - 0.5,
                line=dict(color="#22c55e", width=2, dash="dot"),
            )
        ],
        annotations=[
            dict(
                x=0.0,
                y=n_rows - 0.2,
                xref="x",
                yref="paper",
                text="kötü",
                showarrow=False,
                font=dict(size=11, color="#9ca3af"),
                xanchor="left",
            ),
            dict(
                x=1.0,
                y=n_rows - 0.2,
                xref="x",
                yref="paper",
                text="iyi",
                showarrow=False,
                font=dict(size=11, color="#22c55e"),
                xanchor="right",
            ),
        ],
    )

    output_html.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_html), auto_open=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build an interactive segmentation metrics dashboard from a CSV file. "
            "The CSV must contain at least the columns: "
            "'Run', 'Model', 'Train Time (min)', 'mIoU', 'Dice', "
            "'Dice background', 'Dice Cat', 'Dice Human', 'Dice Road', "
            "'IoU background', 'IoU Cat', 'IoU Human', 'IoU Road'."
        )
    )

    repo_root = Path(__file__).resolve().parents[1]
    default_csv = repo_root / "data" / "segmentation_experiments_metrics.csv"
    default_output = repo_root / "docs" / "software" / "assets" / "segmentation_dashboard.html"

    parser.add_argument(
        "--csv",
        type=Path,
        default=default_csv,
        help=(
            "Path to the metrics CSV file. "
            f"Defaults to '{default_csv.relative_to(repo_root)}'."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help=(
            "Path to the output HTML file. "
            f"Defaults to '{default_output.relative_to(repo_root)}'."
        ),
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build_dashboard(args.csv, args.output)

