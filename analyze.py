"""Analyze the extracted YouTube metrics.

Reads the Excel produced by yt-analysis.py, derives engagement metrics, prints a
summary, and writes a chart. Runs offline — no API key needed.

    python analyze.py [path/to/metrics.xlsx]
"""
import sys

import matplotlib
matplotlib.use("Agg")  # headless-safe; writes the figure to disk
import matplotlib.pyplot as plt
import pandas as pd

DEFAULT_XLSX = "buzzfeed_youtube_metrics.xlsx"
NUMERIC = ["View Count", "Like Count", "Comment Count", "Length (seconds)"]


def load(path=DEFAULT_XLSX) -> pd.DataFrame:
    df = pd.read_excel(path)
    for c in NUMERIC:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["View Count"]).copy()

    # Engagement rate = (likes + comments) / views  — the project's North Star
    df["Engagement Rate %"] = (
        (df["Like Count"].fillna(0) + df["Comment Count"].fillna(0))
        / df["View Count"].replace(0, pd.NA) * 100
    )
    df["Length (min)"] = df["Length (seconds)"] / 60
    return df


def summarize(df: pd.DataFrame) -> str:
    n = len(df)
    lines = [
        f"Videos analyzed:        {n}",
        f"Total views:            {int(df['View Count'].sum()):,}",
        f"Median views:           {int(df['View Count'].median()):,}",
        f"Mean engagement rate:   {df['Engagement Rate %'].mean():.2f}%",
        f"Median length:          {df['Length (min)'].median():.1f} min",
    ]
    corr = df["Length (min)"].corr(df["View Count"])
    lines.append(f"Corr(length, views):    {corr:+.2f}")

    top_views = df.nlargest(5, "View Count")[["Title", "View Count"]]
    top_eng = df.nlargest(5, "Engagement Rate %")[["Title", "Engagement Rate %"]]
    out = ["=== BuzzFeed YouTube — summary ===", *lines,
           "\nTop 5 by views:"]
    out += [f"  {int(v):>10,}  {t[:48]}" for t, v in top_views.itertuples(index=False)]
    out += ["\nTop 5 by engagement rate:"]
    out += [f"  {e:>6.2f}%  {t[:48]}" for t, e in top_eng.itertuples(index=False)]
    return "\n".join(out)


def make_chart(df: pd.DataFrame, save_path="figures/engagement.png"):
    import os
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.scatter(df["Length (min)"], df["View Count"], alpha=0.5, color="#dc2626")
    ax1.set_xlabel("Video length (min)")
    ax1.set_ylabel("View count")
    ax1.set_yscale("log")
    ax1.set_title("Views vs. length")
    ax1.grid(True, alpha=0.3)

    ax2.hist(df["Engagement Rate %"].dropna(), bins=25, color="#1d4ed8", alpha=0.8)
    ax2.set_xlabel("Engagement rate (%)")
    ax2.set_ylabel("Number of videos")
    ax2.set_title("Distribution of engagement rate")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=110)
    plt.close(fig)
    return save_path


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XLSX
    df = load(path)
    print(summarize(df))
    chart = make_chart(df)
    print(f"\nChart saved to {chart}")


if __name__ == "__main__":
    main()
