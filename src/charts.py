"""Chart drawing shared by the GUI (app.py) and the CLI (main.py)."""

from matplotlib.ticker import MaxNLocator


def draw_weekly_chart(ax, labels, values):
    """Draw the 'sets per day' bar chart on a matplotlib Axes."""
    ax.clear()

    ax.bar(labels, values)

    ax.set_title("Sets per day (last 7 days)")
    ax.set_ylabel("Total sets")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(axis="x", labelrotation=45)

    if not any(values):
        ax.set_ylim(0, 1)
        ax.text(
            0.5,
            0.5,
            "No workouts in the last 7 days",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )