"""
Render arsitektur sistem ALQI-SAW (tri-link) yang diselaraskan dengan
kolektor baseline (ether1-ISP-A, ether2-ISP-B, ether3-ISP-C).

Revisi v3 (perbaikan analisis D-01..D-12):
 - frame "Server Controller (out-of-band)" melingkupi Kolektor + Engine + Adapter
 - panah korelasi antar-LEO -> gerbang histeresis
 - alur stok koneksi S_i (conntrack -> connection_stock -> engine)
 - panah kolektor -> store (raw JSONL), terpisah dari log engine
 - panah Router -> Kolektor satu arah (read-only)
 - kanal tulis terpisah: Adapter -> Router (write, akun terpisah)
 - Observability -> Adapter (rollback / fail-static)
 - legenda warna + tag lapisan L0..L7
 - "API-SSL service" (router) vs librouteros (klien/kolektor)
 - catatan cakupan: control plane (LAN/MGMT di dok 16)

Jalankan:  python arsitektur_ALQI_SAW.py
Luaran :  arsitektur_ALQI_SAW.png / .svg
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch

fig, ax = plt.subplots(figsize=(17.5, 9.5))
ax.set_xlim(-6, 122); ax.set_ylim(0, 100); ax.axis("off")

C_TITLE = "#12263a"
C_WAN,  C_WAN_E  = "#e8f1fb", "#2b6cb0"
C_RTR,  C_RTR_E  = "#fdf3e3", "#b7791f"
C_COL,  C_COL_E  = "#eef2ff", "#4c51bf"
C_ENG,  C_ENG_E  = "#eafaf0", "#2f855a"
C_ADP,  C_ADP_E  = "#f3f4f6", "#4b5563"
C_STO,  C_STO_E  = "#fdf0f4", "#b83280"
C_FRM,  C_FRM_E  = "#f7f9fc", "#2f855a"
C_CORR = "#c53030"


def box(x, y, w, h, text, fc, ec, fs=8.5, bold=False, lw=1.3, rnd=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.3,rounding_size={rnd}",
                 linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=C_TITLE, fontweight="bold" if bold else "normal")


def frame(x, y, w, h, ec=C_FRM_E, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.3,rounding_size=1.8",
                 linewidth=lw, edgecolor=ec, facecolor=C_FRM, alpha=0.35))


def arrow(x1, y1, x2, y2, color="#444444", ls="-", lw=1.5, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                 mutation_scale=14, color=color, linestyle=ls, linewidth=lw))


def label(x, y, text, fs=7.6, color="#333333", rot=0, bold=False):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color,
            rotation=rot, fontweight="bold" if bold else "normal")


# ===================== JUDUL =====================
ax.text(58, 98, "Arsitektur Sistem \u2014 Indeks Kualitas Link Berbasis SAW  "
                "(tri-link, selaras kolektor baseline)",
        ha="center", va="center", fontsize=13.5, fontweight="bold", color=C_TITLE)
label(58, 94.6, "cakupan: control plane  \u00b7  topologi & LAN/MGMT ada di "
                "16_Arsitektur_Jaringan_MikroTik.md", 8.6, "#666666")

# ===================== DATA PLANE (L0) =====================
label(10, 91.6, "Data plane (L0)", 9, "#555555", bold=True)
for t, y in [("ether1-ISP-A\nStarlink LEO-1", 80),
             ("ether2-ISP-B\nStarlink LEO-2", 64),
             ("ether3-ISP-C\nFO IndiHome", 48)]:
    box(0, y, 20, 9, t, C_WAN, C_WAN_E, 8.2)

# ===================== ROUTER (aktuator) =====================
box(25, 34, 21, 58, "", C_RTR, C_RTR_E, lw=1.5)
ax.text(35.5, 88.8, "Router RB1100AHx4\nAktuator (L0)", ha="center", va="center",
        fontsize=9, fontweight="bold", color=C_RTR_E)
for t, y in [("Mangle / PCC\n+ connection mark", 79.5),
             ("conntrack\n(stok S_i)", 70),
             ("/ping interface=\n(probe di router)", 60.5),
             ("API-SSL service\n(librouteros)", 51),
             ("NAT masquerade per WAN", 41.5)]:
    box(27, y, 17, 7.6, t, "#ffffff", C_RTR_E, 7.4)

for y in (80, 64, 48):
    arrow(20, y + 4.5, 25, 70, color="#444444")

# ===================== FRAME CONTROLLER =====================
frame(50, 30, 49, 63)
ax.text(74.5, 90.6, "Server Controller (out-of-band)", ha="center", va="center",
        fontsize=10.5, fontweight="bold", color=C_FRM_E)

# --- Kolektor (L1/L2) ---
box(54, 79, 41, 10.6, "", C_COL, C_COL_E, lw=1.4)
ax.text(74.5, 87.3, "L1 \u00b7 Kolektor collector.py  \u00b7  read-only",
        ha="center", va="center", fontsize=8.8, fontweight="bold", color=C_COL_E)
ax.text(74.5, 83.8, "/print  +  /ping interface=  \u2192  JSONL "
                    "{ts_utc, site, router, kind, data}",
        ha="center", va="center", fontsize=7.6, color=C_TITLE)
ax.text(74.5, 80.9, "L2 \u00b7 analyze_baseline / analyze_periodicity  "
                    "(FFT \u00b7 ACF 15 s \u00b7 korelasi antar-WAN)",
        ha="center", va="center", fontsize=7.6, color=C_TITLE)

# --- Engine (L3/L4) ---
box(54, 45, 41, 31, "", C_ENG, C_ENG_E, lw=1.4)
ax.text(74.5, 73.2, "L3\u2013L4 \u00b7 Scoring & Decision Engine",
        ha="center", va="center", fontsize=9, fontweight="bold", color=C_ENG_E)
for t, y in [("EWMA \u2192 Normalisasi (batas tetap) \u2192 Bobot hibrida (\u03b3)", 63.5),
             ("Skor  Q_i(t)  \u2014  3 link  (0\u2013100)", 56.5),
             ("Gerbang histeresis + state machine (8 state)", 49.5)]:
    box(57, y, 35, 6.2, t, "#ffffff", C_ENG_E, 7.8)
box(57, 45.6, 35, 3.0, "Alokasi & bucket mapping 3 link", "#ffffff", C_ENG_E, 7.4)

# --- Adapter (L5) ---
box(54, 33.5, 41, 9, "L5 \u00b7 Adapter  \u2014  MikroTik (nyata) / mock",
    C_ADP, C_ADP_E, 8.4, bold=True)

# ===================== STORE (L6) & OBS (L7) & LEGENDA =====================
box(101, 64, 20, 16, "L6 \u00b7 Time-series store\naudit log\nconfig versioning",
    C_STO, C_STO_E, 8.2, bold=True)
box(101, 40, 20, 16, "L7 \u00b7 Observability\nfail-static\nwatchdog\nsnapshot / rollback",
    C_ADP, C_ADP_E, 8.2, bold=True)

# ===================== PANAH =====================
# baca: Router -> Kolektor (satu arah, read-only)
arrow(46, 86, 54, 84.5, color=C_COL_E)
label(50, 89.6, "GET /print + /ping\n(read-only)", 7.2, C_COL_E)

# alur stok koneksi S_i (dashed)
arrow(46, 73.5, 54, 81, color="#718096", ls=(0, (3, 2)))
label(50.5, 76.2, "connection_stock\n(stok S_i)", 7.0, "#718096")

# Kolektor -> Engine
arrow(74.5, 79, 74.5, 76, color=C_ENG_E)

# korelasi antar-LEO -> gerbang histeresis (dashed) : koridor kanan inner box
arrow(95, 81, 92.4, 52.6, color=C_CORR, ls=(0, (3, 2)), lw=1.4)
label(97.6, 66, "korelasi A\u2013B", 7.2, C_CORR, rot=90)

# Engine -> Adapter
arrow(74.5, 45, 74.5, 42.5, color=C_ADP_E)

# Adapter -> Router : kanal tulis (akun terpisah)
arrow(54, 38, 46, 38, color="#c05621", lw=1.7)
label(50, 35.4, "apply / verify \u00b7 write\n(akun terpisah)", 7.0, "#c05621")

# Kolektor -> Store (raw JSONL)
arrow(95, 84.5, 101, 76, color=C_COL_E, ls=(0, (3, 2)))
label(99.5, 86.5, "raw JSONL", 7.0, C_COL_E)

# Engine -> Store (Q / status / rasio)
arrow(95, 56, 101, 68, color=C_STO_E, ls=(0, (3, 2)))
label(99.5, 57.5, "Q / status /\nrasio", 7.0, C_STO_E)

# Observability -> Adapter (rollback)
arrow(101, 46, 95, 39, color=C_ADP_E, ls=(0, (3, 2)))
label(100.5, 43.6, "rollback", 7.0, C_ADP_E)

# Store <-> Observability (kendali)
arrow(111, 64, 111, 56.5, color="#4a5568", style="<|-|>", ls=(0, (2, 2)), lw=1.2)
label(114.5, 60, "kendali", 7.0, "#4a5568", rot=90)

# ===================== LEGENDA =====================
legend = [
    Patch(facecolor=C_WAN, edgecolor=C_WAN_E, label="Data plane / WAN (L0)"),
    Patch(facecolor=C_RTR, edgecolor=C_RTR_E, label="Router / aktuator"),
    Patch(facecolor=C_COL, edgecolor=C_COL_E, label="Kolektor \u00b7 baca (L1\u2013L2)"),
    Patch(facecolor=C_ENG, edgecolor=C_ENG_E, label="Skoring & keputusan (L3\u2013L4)"),
    Patch(facecolor=C_ADP, edgecolor=C_ADP_E, label="Adapter / observability (L5, L7)"),
    Patch(facecolor=C_STO, edgecolor=C_STO_E, label="Penyimpanan & audit (L6)"),
]
ax.legend(handles=legend, loc="lower left", bbox_to_anchor=(-0.01, 0.02),
          fontsize=8.4, ncol=1, frameon=True, framealpha=0.96, borderpad=0.8,
          title="Legenda  \u2014  garis putus-putus = aliran data/audit  \u00b7  "
                "L0\u2013L7 = lapisan (15 \u00a74)", title_fontsize=8.0)

plt.tight_layout()
fig.savefig("arsitektur_ALQI_SAW.png", dpi=180, bbox_inches="tight", facecolor="white")
fig.savefig("arsitektur_ALQI_SAW.svg", bbox_inches="tight", facecolor="white")
print("OK: arsitektur_ALQI_SAW.png / .svg (v3)")
