"""
Diagram arsitektur jaringan MikroTik Multi-WAN (3 ISP) + PCC + failover + LAN.
Jalankan:  python arsitektur_jaringan_mikrotik.py
Luaran :  arsitektur_jaringan_mikrotik.png / .svg
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Patch

fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(-7, 100); ax.set_ylim(0, 100); ax.axis("off")

C_TITLE = "#12263a"
WAN,   WAN_E   = "#e3f0fb", "#1f6fb2"   # jalur WAN      (biru)
LB,    LB_E    = "#fdf3dc", "#b7791f"   # routing/LB     (kuning)
LAN,   LAN_E   = "#efe9fb", "#6b46c1"   # jaringan LAN   (ungu)
CLI,   CLI_E   = "#e9f7ee", "#2f855a"   # client         (hijau)
CTL,   CTL_E   = "#f3f4f6", "#4b5563"   # kontrol        (abu)
FAIL,  FAIL_E  = "#fdecef", "#c53030"   # failover       (merah)


def box(x, y, w, h, text, fc, ec, fs=9, bold=False, lw=1.4, rnd=1.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.35,rounding_size={rnd}",
                 linewidth=lw, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=C_TITLE, fontweight="bold" if bold else "normal")


def arrow(x1, y1, x2, y2, color="#444444", ls="-", lw=1.6, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                 mutation_scale=15, color=color, linestyle=ls, linewidth=lw))


def label(x, y, text, fs=8.2, color="#333333", bold=False):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal")


ax.text(50, 98.5, "Arsitektur Jaringan MikroTik Multi-WAN (3 ISP) "
                  "\u2014 PCC Load Balancing + Failover",
        ha="center", va="center", fontsize=14, fontweight="bold", color=C_TITLE)
label(50, 95.2, "ether1-ISP-A (Starlink)  \u00b7  ether2-ISP-B (Starlink)  \u00b7  "
                "ether3-ISP-C (Fiber Optic)", 9, "#555555")

# ================= ZONA WAN (biru) =================
label(1, 88, "Jalur WAN", 9.5, WAN_E, bold=True)
for cx, t in [(16, "ISP A\nStarlink"), (50, "ISP B\nStarlink"),
              (84, "ISP C\nFiber Optic (FO)")]:
    ax.add_patch(Ellipse((cx, 88), 24, 9, facecolor=WAN, edgecolor=WAN_E, lw=1.6))
    ax.text(cx, 88, t, ha="center", va="center", fontsize=9, color=C_TITLE)

# interface WAN
for cx, ifn in [(16, "ether1-ISP-A"), (50, "ether2-ISP-B"), (84, "ether3-ISP-C")]:
    box(cx - 9, 78, 18, 5, ifn, "#ffffff", WAN_E, 8.2, bold=True)
    arrow(cx, 83.4, cx, 78.1, color=WAN_E)

# ================= ROUTER =================
box(4, 30, 66, 46, "", "#fffdf7", LB_E, lw=1.8, rnd=1.8)
ax.text(37, 73.6, "MikroTik RB1100AHx4 \u2014 RouterOS v7  \u00b7  Multi-WAN",
        ha="center", va="center", fontsize=10.5, fontweight="bold", color=LB_E)

for cx, ifn in [(16, "ether1-ISP-A"), (50, "ether2-ISP-B"), (84, "ether3-ISP-C")]:
    arrow(cx, 78, cx, 76.2, color=WAN_E, lw=1.8)

box(7, 65.5, 60, 6.5, "WAN in : ether1-ISP-A  \u00b7  ether2-ISP-B  \u00b7  ether3-ISP-C",
    "#ffffff", WAN_E, 8.4, bold=True)
box(7, 57.5, 60, 6.5, "Mangle  \u00b7  PCC classifier (both-addresses-and-ports)  "
                      "+  connection mark", "#ffffff", LB_E, 8.4, bold=True)
box(7, 49.5, 60, 6.5, "Routing mark  \u2192  to-ISP-A  /  to-ISP-B  /  to-ISP-C",
    "#ffffff", LB_E, 8.4, bold=True)
box(7, 41.5, 60, 6.5, "Failover :  check-gateway + netwatch  \u00b7  distance (backup)",
    FAIL, FAIL_E, 8.4, bold=True)
box(7, 33.5, 60, 6.5, "NAT masquerade per WAN  \u00b7  LAN bridge (out-interface)",
    "#ffffff", LAN_E, 8.4)

# ================= KONTROLER =================
box(74, 45, 23, 20, "", CTL, CTL_E, rnd=1.6)
ax.text(85.5, 61.5, "Server Controller", ha="center", va="center",
        fontsize=9.3, fontweight="bold", color=CTL_E)
ax.text(85.5, 54.5, "(API-SSL / librouteros)\npengatur rasio PCC\n& verifikasi aturan",
        ha="center", va="center", fontsize=8, color=C_TITLE)
arrow(74, 55, 70.2, 55, color=CTL_E, style="<|-|>", lw=1.6)
label(72, 57.5, "injeksi\nrasio", 7.6, CTL_E)

# ================= ZONA LAN (ungu) =================
label(1, 20, "Jaringan LAN", 9.5, LAN_E, bold=True)

box(6, 15, 26, 9, "Switch LAN\n(bridge-LAN, ether4+)", LAN, LAN_E, 8.6, bold=True)
box(40, 15, 24, 9, "Access Point (AP)\nWi-Fi SSID", LAN, LAN_E, 8.6, bold=True)
box(10, 5.5, 20, 6.5, "Client kabel", CLI, CLI_E, 8.4, bold=True)
box(42, 5.5, 20, 6.5, "Client Wi-Fi", CLI, CLI_E, 8.4, bold=True)

arrow(37, 30, 19, 24.2, color=LAN_E, lw=1.8)
label(25, 29, "LAN", 7.8, LAN_E)
arrow(32, 19.5, 40, 19.5, color=LAN_E, lw=1.8)
arrow(19, 15, 19, 12.1, color=CLI_E, lw=1.6)
arrow(52, 15, 52, 12.1, color=CLI_E, lw=1.6)

# ================= LEGENDA =================
legend = [
    Patch(facecolor=WAN, edgecolor=WAN_E, label="Jalur WAN (3 ISP)"),
    Patch(facecolor=LB, edgecolor=LB_E, label="Routing / Load balancing (PCC)"),
    Patch(facecolor=FAIL, edgecolor=FAIL_E, label="Failover"),
    Patch(facecolor=LAN, edgecolor=LAN_E, label="Distribusi LAN"),
    Patch(facecolor=CLI, edgecolor=CLI_E, label="Client"),
    Patch(facecolor=CTL, edgecolor=CTL_E, label="Kontrol (eksternal)"),
]
ax.legend(handles=legend, loc="lower right", fontsize=8.6, ncol=2,
          frameon=True, framealpha=0.95, borderpad=0.8)

plt.tight_layout()
fig.savefig("arsitektur_jaringan_mikrotik.png", dpi=180, bbox_inches="tight",
            facecolor="white")
fig.savefig("arsitektur_jaringan_mikrotik.svg", bbox_inches="tight", facecolor="white")
print("OK: arsitektur_jaringan_mikrotik.png / .svg")
