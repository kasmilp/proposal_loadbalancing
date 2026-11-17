"""
Render arsitektur sistem ALQI-SAW (tri-link) yang diselaraskan dengan
kolektor baseline (ether1-ISP-A, ether2-ISP-B, ether3-ISP-C).
Jalankan:  python arsitektur_ALQI_SAW.py
Luaran :  arsitektur_ALQI_SAW.png, arsitektur_ALQI_SAW.svg
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(15, 9.5))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

C_TITLE = "#12263a"
C_WAN, C_WAN_E = "#e8f1fb", "#2b6cb0"
C_RTR, C_RTR_E = "#fdf3e3", "#b7791f"
C_COL, C_COL_E = "#eef2ff", "#4c51bf"
C_CTL, C_CTL_E = "#eafaf0", "#2f855a"
C_STG, C_STG_E = "#f0f0f5", "#4a5568"
C_STO, C_STO_E = "#fdf0f4", "#b83280"


def box(x, y, w, h, text, fc, ec, fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.35,rounding_size=1.3",
                 linewidth=1.3, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=C_TITLE, fontweight="bold" if bold else "normal")


def arrow(x1, y1, x2, y2, color="#444444", ls="-", lw=1.3, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                 mutation_scale=13, color=color, linestyle=ls, linewidth=lw))


def label(x, y, text, fs=7.6, color="#333333"):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color)


ax.text(50, 97.5, "Arsitektur Sistem \u2014 Indeks Kualitas Link Berbasis SAW  "
                  "(tri-link, selaras kolektor baseline)",
        ha="center", va="center", fontsize=13, fontweight="bold", color=C_TITLE)

# ---------- Data plane ----------
label(11, 89.5, "Data plane \u2014 interface (sesuai collector.py)", 8.6, "#555555")
for t, y in [("ether1-ISP-A\nStarlink LEO-1", 78),
             ("ether2-ISP-B\nStarlink LEO-2", 62),
             ("ether3-ISP-C\nFO IndiHome", 46)]:
    box(2, y, 18, 9, t, C_WAN, C_WAN_E, 8.2)

# ---------- Router ----------
box(26, 42, 20, 46, "", C_RTR, C_RTR_E)
ax.text(36, 84.5, "Router RB1100AHx4", ha="center", va="center",
        fontsize=9.5, fontweight="bold", color=C_RTR_E)
for t, y in [("Mangle / PCC\n+ connection mark", 75),
             ("conntrack\n(stok S_i)", 65.5),
             ("/ping interface=\n(probe di router)", 56),
             ("API-SSL (librouteros)", 47.5)]:
    box(28, y, 16, 7.4, t, "#ffffff", C_RTR_E, 7.8)

# ---------- Adapter ----------
box(26, 30, 20, 9, "Adapter\nMikroTik / mock", C_STG, C_STG_E, 8.2)

# ---------- Collector ----------
box(52, 70, 44, 18, "", C_COL, C_COL_E)
ax.text(74, 85.6, "Kolektor collector.py  \u00b7  read-only",
        ha="center", va="center", fontsize=9.3, fontweight="bold", color=C_COL_E)
ax.text(74, 79.5, "/print  +  /ping interface=  \u2192  JSONL "
                  "{ts_utc, site, router, kind, data}",
        ha="center", va="center", fontsize=7.8, color=C_TITLE)
ax.text(74, 74.5, "\u2192 analyze_baseline / analyze_periodicity  "
                  "(FFT \u00b7 ACF 15 s \u00b7 korelasi antar-WAN)",
        ha="center", va="center", fontsize=7.8, color=C_TITLE)

# ---------- Scoring & Decision engine ----------
box(52, 30, 44, 38, "", C_CTL, C_CTL_E)
ax.text(74, 64.5, "Scoring & Decision Engine", ha="center", va="center",
        fontsize=9.3, fontweight="bold", color=C_CTL_E)
for t, y in [("EWMA \u2192 Normalisasi (batas tetap) \u2192 Bobot hibrida (\u03b3)", 55.5),
             ("Skor  Q_i(t)  \u2014  3 link  (0\u2013100)", 47),
             ("Gerbang histeresis + state machine (8 state)", 38.5)]:
    box(56, y, 36, 6.6, t, "#ffffff", C_CTL_E, 8.0)
box(56, 31, 36, 6.4, "Alokasi & bucket mapping 3 link", "#ffffff", C_CTL_E, 8.0)

# ---------- Store & observability ----------
box(52, 18, 44, 8, "Time-series store  \u00b7  audit log  \u00b7  config versioning",
    C_STO, C_STO_E, 8.2)
box(2, 18, 46, 8, "Observability:  fail-static  \u00b7  watchdog  \u00b7  "
                  "snapshot / rollback", C_STG, C_STG_E, 8.2)

# ---------- Arrows ----------
for y in (78, 62, 46):
    arrow(20, y + 4.5, 26, 64)

arrow(46, 80, 52, 80, color="#4c51bf", style="<|-|>")
label(49, 82.5, "read-only", 7.4, "#4c51bf")

arrow(74, 70, 74, 68, color="#2f855a")
arrow(52, 35, 46, 34.5, color="#2f855a")
label(49, 32.5, "policy", 7.4, "#2f855a")

arrow(36, 39, 36, 42, color="#4a5568")
label(40.5, 40.5, "apply / verify", 7.4, "#4a5568")

arrow(74, 30, 74, 26, color="#b83280", ls=(0, (3, 2)))
label(74, 28, "log Q / status / rasio", 7.4, "#b83280")

arrow(48, 22, 52, 22, color="#4a5568", style="<|-|>")
label(50, 23.6, "kendali", 7.4, "#4a5568")

plt.tight_layout()
fig.savefig("arsitektur_ALQI_SAW.png", dpi=180, bbox_inches="tight", facecolor="white")
fig.savefig("arsitektur_ALQI_SAW.svg", bbox_inches="tight", facecolor="white")
print("OK: arsitektur_ALQI_SAW.png / .svg")
