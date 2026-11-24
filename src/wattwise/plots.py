"""Las dos gráficas del producto, ya con el estilo de WattWise.

Uso desde el cuaderno (cuando el análisis esté listo):

    from wattwise.plots import plot_hourly_profile, plot_peak_breakdown
    plot_hourly_profile(avg_kwh_by_hour, peak_hour, "outputs/figures/fig1_hourly_profile.png")
    plot_peak_breakdown(kwh_by_group, "18:00-19:00", "outputs/figures/fig2_peak_breakdown.png")

Después ejecuten `python ui/make_screens.py` y las pantallas toman las gráficas solas.
"""
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import config as C


def _style():
    plt.rcParams.update({
        "font.family": ["Inter", "DejaVu Sans"],
        "font.size": 15,
        "axes.edgecolor": C.COLORS["line"],
        "axes.labelcolor": C.COLORS["slate"],
        "xtick.color": C.COLORS["slate"],
        "ytick.color": C.COLORS["slate"],
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def _badge(ax, illustrative):
    if illustrative:
        ax.text(0.99, 1.04, "Datos ilustrativos", transform=ax.transAxes, ha="right",
                va="bottom", fontsize=13, color=C.COLORS["ink"],
                bbox=dict(boxstyle="round,pad=0.35", fc=C.COLORS["amber_soft"], ec="none"))


def plot_hourly_profile(avg_by_hour, peak_hour, out_path, illustrative=False):
    """avg_by_hour: 24 valores (kWh promedio por hora, índice 0..23)."""
    _style()
    hours = list(range(24))
    fig, ax = plt.subplots(figsize=C.FIG_SIZE_INCHES, dpi=C.DPI)
    ax.axvspan(peak_hour - 0.5, peak_hour + 0.5, color=C.COLORS["amber_soft"], zorder=0)
    ax.plot(hours, avg_by_hour, color=C.COLORS["teal"], lw=3.2, zorder=2)
    ax.scatter([peak_hour], [avg_by_hour[peak_hour]], s=170, color=C.COLORS["amber"],
               edgecolor="white", linewidth=2.5, zorder=3)
    ax.annotate(f"{C.LABEL_PEAK}: {peak_hour:02d}:00\n{avg_by_hour[peak_hour]:.2f} kWh",
                xy=(peak_hour, avg_by_hour[peak_hour]),
                xytext=(peak_hour - 5.2, avg_by_hour[peak_hour] * 0.92),
                fontsize=17, fontweight="bold", color=C.COLORS["ink"],
                arrowprops=dict(arrowstyle="-", color=C.COLORS["ink"], lw=1.4))
    ax.set_xticks(range(0, 24, 3))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 3)])
    ax.set_xlim(-0.5, 23.5)
    ax.set_ylim(0, max(avg_by_hour) * 1.18)
    ax.set_xlabel(C.LABEL_X_HOURLY, labelpad=10)
    ax.set_ylabel(C.LABEL_Y_HOURLY, labelpad=10)
    ax.grid(axis="y", color=C.COLORS["line"], lw=1)
    _badge(ax, illustrative)
    fig.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor="white")
    plt.close(fig)


def plot_peak_breakdown(kwh_by_group, window_label, out_path, illustrative=False, highlight=None):
    """kwh_by_group: dict con las claves de config.GROUP_ORDER (kWh en la franja).

    highlight: clave del circuito a resaltar. Por defecto, el circuito MEDIDO con mayor aporte
    (se excluye "other", que es el resto no medido y no se puede atribuir a un equipo)."""
    _style()
    keys = C.GROUP_ORDER
    labels = ["\n".join(textwrap.wrap(C.GROUP_LABELS[k], 24)) for k in keys]
    values = [kwh_by_group[k] for k in keys]
    if highlight is None:
        highlight = max((k for k in keys if k != "other"), key=lambda k: kwh_by_group[k])
    top = keys.index(highlight)
    colors = [C.COLORS["amber"] if i == top else C.COLORS["teal"] for i in range(len(values))]
    fig, ax = plt.subplots(figsize=C.FIG_SIZE_INCHES, dpi=C.DPI)
    y = list(range(len(keys)))[::-1]
    ax.barh(y, values, color=colors, height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=16, color=C.COLORS["ink"])
    for yi, v in zip(y, values):
        ax.text(v + max(values) * 0.015, yi, f"{v:.2f} kWh", va="center",
                fontsize=16, fontweight="bold", color=C.COLORS["ink"])
    ax.set_xlim(0, max(values) * 1.2)
    ax.set_xlabel(f"{C.LABEL_X_BREAKDOWN}  |  {window_label}", labelpad=10)
    ax.grid(axis="x", color=C.COLORS["line"], lw=1)
    ax.set_axisbelow(True)
    _badge(ax, illustrative)
    fig.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor="white")
    plt.close(fig)
