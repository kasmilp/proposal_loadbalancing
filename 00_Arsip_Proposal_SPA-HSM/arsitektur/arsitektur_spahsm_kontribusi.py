"""Membuat diagram arsitektur SPA-HSM dan pemetaan kontribusi K1-K4.

Jalankan dari root repositori:
    python arsitektur/arsitektur_spahsm_kontribusi.py

Luaran:
    arsitektur/arsitektur_spahsm_kontribusi.png
    arsitektur/arsitektur_spahsm_kontribusi.svg
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE = Path(__file__).resolve().parent

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 10

# Palet warna per lapisan
C_MEAS = ("#DDEBF7", "#2E75B6")
C_L1 = ("#FFF2CC", "#BF8F00")
C_L2 = ("#E2EFDA", "#548235")
C_L3 = ("#FCE4D6", "#C55A11")
C_DATA = ("#EDEDED", "#7F7F7F")
C_EVAL = ("#E4DFEC", "#7030A0")

BADGE = {
    "K1": "#BF8F00",
    "K2": "#548235",
    "K3": "#7030A0",
    "K4": "#2E75B6",
}


def box(ax, x, y, w, h, title, body, colors, badges=(), dashed=False, title_size=13):
    fill, edge = colors
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.25,rounding_size=0.8",
        linewidth=1.6,
        edgecolor=edge,
        facecolor=fill,
        linestyle=(0, (4, 3)) if dashed else "solid",
        zorder=2,
    )
    ax.add_patch(patch)

    ax.text(
        x + 1.8, y + h - 2.0, title,
        ha="left", va="top",
        fontsize=title_size, fontweight="bold", color="#1F1F1F", zorder=3,
    )
    ax.text(
        x + 1.8, y + h - 6.0, body,
        ha="left", va="top",
        fontsize=9.6, color="#262626", linespacing=1.35, zorder=3,
    )

    # Badge kontribusi di kanan atas
    bw, bh, gap = 4.0, 3.6, 0.7
    start = x + w - 1.6 - len(badges) * bw - (len(badges) - 1) * gap
    for i, code in enumerate(badges):
        bx = start + i * (bw + gap)
        by = y + h - 4.6
        b = FancyBboxPatch(
            (bx, by), bw, bh,
            boxstyle="round,pad=0.12,rounding_size=0.7",
            linewidth=0,
            facecolor=BADGE[code],
            zorder=4,
        )
        ax.add_patch(b)
        ax.text(
            bx + bw / 2, by + bh / 2, code,
            ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=5,
        )


def arrow(ax, x1, y1, x2, y2, label=None, dashed=False, rad=0.0):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.5,
        color="#595959",
        linestyle=(0, (4, 3)) if dashed else "solid",
        connectionstyle=f"arc3,rad={rad}",
        zorder=1,
    )
    ax.add_patch(a)
    if label:
        ax.text(
            (x1 + x2) / 2 + 1.2, (y1 + y2) / 2,
            label,
            ha="left", va="center",
            fontsize=8.2, style="italic", color="#595959", zorder=6,
        )


def main():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(-4, 100)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(
        50, 97.5, "Arsitektur Sistem SPA-HSM dan Pemetaan Kontribusi",
        ha="center", va="top", fontsize=19, fontweight="bold", color="#1F1F1F",
    )
    ax.text(
        50, 93.5, "Tiga lapis inti dengan dua bidang pendukung: pengukuran dan evaluasi ablasi",
        ha="center", va="top", fontsize=10.5, color="#595959",
    )

    # Bidang pengukuran
    box(
        ax, 10, 79, 80, 10.5,
        "BIDANG PENGUKURAN (MEASUREMENT PLANE)",
        "Probe RTT/jitter/packet loss/goodput  ·  SNMP ifHCInOctets/ifHCOutOctets  ·  telemetri RouterOS",
        C_MEAS, badges=("K4",), title_size=12.5,
    )

    # Lapis 1
    box(
        ax, 10, 62, 80, 12.5,
        "LAPIS 1 — ALGORITHM CORE",
        "EWMA smoother  →  SAW scorer  →  Asymmetric Hysteresis State Machine\n"
        "→  pemetaan status dan skor kualitas ke target rasio PCC",
        C_L1, badges=("K1",),
    )

    # Lapis 2
    box(
        ax, 10, 45, 80, 12.5,
        "LAPIS 2 — ABSTRACT ALLOCATION INTERFACE (KONTRAK)",
        "read_metrics()  ·  set_ratio()  ·  set_affinity()  ·  get_state()  ·  verify()  ·  rollback()\n"
        "AFFINITY_LOCK sebagai direktif preservasi sesi",
        C_L2, badges=("K1", "K2"),
    )

    # Lapis 3
    box(
        ax, 10, 28, 80, 12.5,
        "LAPIS 3 — PLATFORM ADAPTER / EXECUTION",
        "MikroTikAdapter: PCC mangle/routing · conntrack · connection-state=new\n"
        "MockAdapter: uji kesesuaian antarmuka dan portabilitas Algorithm Core",
        C_L3, badges=("K2", "K4"),
    )

    # Jaringan produksi
    box(
        ax, 23, 17.5, 54, 8.0,
        "JARINGAN PRODUKSI RT/RW NET",
        "FO (IndiHome)  +  LEO (Starlink)",
        C_DATA, badges=(), title_size=11.5,
    )

    # Bidang evaluasi
    box(
        ax, 10, 2, 80, 10.0,
        "BIDANG EVALUASI & ABLASI (LINTAS LAPIS)",
        "Scenario runner  ·  metric collector  ·  uji statistik\n"
        "Kontrol: histeresis none/simetris/asimetris  ·  affinity lock on/off",
        C_EVAL, badges=("K3",), dashed=True, title_size=12.5,
    )

    # Alur runtime
    arrow(ax, 50, 79, 50, 74.8, "metrik per link")
    arrow(ax, 50, 62, 50, 57.8, "status · Q · rasio")
    arrow(ax, 50, 45, 50, 40.8, "direktif netral-platform")
    arrow(ax, 50, 28, 50, 25.8, "aturan PCC")

    # Umpan balik dari data plane ke bidang pengukuran
    ax.plot([77, 93], [21.5, 21.5], color="#7F7F7F", linewidth=1.4,
            linestyle=(0, (4, 3)))
    ax.plot([93, 93], [21.5, 84.25], color="#7F7F7F", linewidth=1.4,
            linestyle=(0, (4, 3)))
    ax.annotate(
        "", xy=(90.3, 84.25), xytext=(93, 84.25),
        arrowprops=dict(
            arrowstyle="-|>", mutation_scale=14, linewidth=1.4,
            color="#7F7F7F", linestyle=(0, (4, 3)),
            connectionstyle="arc3,rad=0",
        ),
    )
    ax.text(
        94.2, 53, "umpan balik", rotation=90,
        ha="left", va="center", fontsize=8.2, style="italic", color="#7F7F7F",
    )

    # Legenda kontribusi
    ax.text(
        50, -2.6,
        "K1 formulasi terintegrasi  ·  K2 kontrak antarmuka  ·  "
        "K3 evaluasi ablasi  ·  K4 bukti empiris FO–LEO",
        ha="center", va="bottom", fontsize=9, color="#404040",
    )

    fig.tight_layout()
    png = BASE / "arsitektur_spahsm_kontribusi.png"
    svg = BASE / "arsitektur_spahsm_kontribusi.svg"
    fig.savefig(png, dpi=220, facecolor="white", bbox_inches="tight")
    fig.savefig(svg, facecolor="white", bbox_inches="tight")
    print(f"OK {png}")
    print(f"OK {svg}")


if __name__ == "__main__":
    main()
