import sys
sys.path.insert(0, "/home/claude/diagrams")
from lib import *

LEG_ALL = [("ex", "Existing"), ("ad", "Adaptasi"), ("dev", "Pengembangan"),
           ("gap", "Research gap"), ("rc", "Kontribusi"), ("data", "Aliran data"),
           ("ctrl", "Aliran kontrol"), ("mon", "Pengukuran")]


def legend_block(s, y, items=LEG_ALL):
    s.rect(30, y - 12, s.w - 60, 44, fill="#FAFAFA", stroke="#CFD8DC", sw=1, rx=8)
    s.text(46, y + 15, "Legenda:", size=13, weight="bold")
    s.legend(130, y, items)


# =====================================================================
# DIAGRAM 1 — EXISTING
# =====================================================================
def d1():
    s = SVG(1600, 1000)
    s.title("Diagram 1 — Existing Network Architecture",
            "PCC 3-link sudah aktif dengan rasio tetap 1:1:1; tidak ada komponen yang mengambil keputusan dari kualitas link (snapshot router 12 Nov 2026)")
    s.band(20, 92, 1080, 800, "DATA PLANE (router + LAN)")
    s.band(1120, 92, 460, 600, "MONITORING PASIF (penelitian)")

    isp = [("ISP-A · Starlink", ["ether1-ISP-A", "192.168.1.76/24"], ic_starlink),
           ("ISP-B · Starlink", ["ether2-ISP-B", "192.168.2.160/24"], ic_starlink),
           ("ISP-C · Fiber Optic", ["ether3-ISP-C", "192.168.3.2/24"], ic_fiber)]
    for i, (t, b, ic) in enumerate(isp):
        x = 60 + i * 340
        s.rect(x, 110, 300, 100, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
        ic(s, x + 14, 130)
        s.text(x + 84, 140, t, size=15, weight="bold")
        s.lines(x + 84, 164, b, size=12.5, color=QUIET)
        s.arrow([(x + 150, 210), (x + 150, 268)], both=True)

    # router
    s.rect(60, 270, 980, 400, fill="#F5F7F8", stroke=CAT["ex"][1], sw=2)
    ic_router(s, 76, 280)
    s.text(146, 306, "MikroTik RB1100AHx4 · RouterOS 7.22.2", size=16, weight="bold")
    s.box(80, 330, 300, 112, "ex", "Mangle PCC (23 aturan)",
          ["both-addresses-and-ports:3/0 → A", "3/1 → B · 3/2 → C", "Rasio tetap 1:1:1 (manual)"])
    s.box(400, 330, 290, 112, "ex", "Connection → routing mark",
          ["prerouting: mark-connection", "mark-routing → VIA ISP 1/2/3", "input/output: trafik router"])
    s.box(710, 330, 310, 112, "ex", "Routing table",
          ["VIA ISP 1/2/3 → ether1/2/3", "main: 3 default route distance 1", "(ambigu untuk trafik tak ter-mark)"])
    s.box(80, 460, 300, 120, "ex", "Failover",
          ["Hanya status gateway lokal", "(modem/dish 192.168.x.1)", "Netwatch: tidak ada"])
    s.box(400, 460, 290, 120, "ex", "NAT",
          ["Masquerade per WAN", "Didominasi aturan hotspot"])
    s.box(710, 460, 310, 120, "gap", "Decision plane: KOSONG",
          ["Tidak ada penilaian kualitas,", "peredam perpindahan, atau", "pengatur rasio otomatis"], dash="7 4")
    s.rect(80, 596, 940, 52, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    s.text(100, 628, "bridge-LAN / hotspot  →  DHCP, gateway client", size=14, weight="bold")
    s.arrow([(380, 386), (400, 386)])
    s.arrow([(690, 386), (710, 386)])
    # gap tags
    s.tag(316, 334, "G6")
    s.tag(316, 464, "G1")
    s.tag(726, 546, "G2"); s.tag(774, 546, "G3"); s.tag(822, 546, "G4"); s.tag(870, 546, "G5")

    # LAN
    s.arrow([(550, 670), (550, 720)])
    s.rect(160, 720, 280, 96, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_switch(s, 176, 744); s.text(246, 762, "Switch LAN", size=15, weight="bold"); s.text(246, 784, "ether4+ (kabel)", size=12.5, color=QUIET)
    s.rect(480, 720, 280, 96, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_ap(s, 496, 742); s.text(566, 762, "Access Point", size=15, weight="bold"); s.text(566, 784, "SSID hotspot", size=12.5, color=QUIET)
    s.rect(800, 720, 260, 96, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_client(s, 812, 742); s.text(882, 762, "Client", size=15, weight="bold"); s.text(882, 784, "LAN & wireless", size=12.5, color=QUIET)
    s.arrow([(550, 720), (550, 710), (300, 710), (300, 720)])
    s.arrow([(440, 768), (480, 768)])
    s.arrow([(760, 768), (800, 768)])
    s.arrow([(300, 816), (300, 850), (930, 850), (930, 816)])
    s.text(615, 870, "client kabel", size=12, color=QUIET, anchor="middle")

    # monitoring
    s.rect(1150, 120, 410, 120, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_monitor(s, 1164, 140)
    s.text(1224, 146, "Kolektor collector.py", size=15, weight="bold")
    s.lines(1224, 170, ["API-SSL, akun read-only", "/ping interface= tiap 2 s", "counter interface tiap 10 s"], size=12.5, color=QUIET)
    s.rect(1150, 290, 410, 110, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_db(s, 1166, 312)
    s.text(1224, 318, "JSONL baseline", size=15, weight="bold")
    s.lines(1224, 342, ["2,2 jam · 19.706 record", "3 WAN × 2 target probe"], size=12.5, color=QUIET)
    s.rect(1150, 450, 410, 120, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    s.text(1166, 476, "Analisis offline", size=15, weight="bold")
    s.lines(1166, 500, ["Starlink: 35–84 episode / 2,2 jam", "Korelasi RTT A–B 0,68–0,70", "Hasil hanya untuk laporan"], size=12.5, color=QUIET)
    s.arrow([(1040, 300), (1150, 180)], color="#1E88E5", dash="3 4", marker="arB")
    s.text(1060, 226, "baca", size=12, color="#1E88E5")
    s.arrow([(1355, 240), (1355, 290)])
    s.arrow([(1355, 400), (1355, 450)])
    # no feedback
    s.line([(1150, 540), (1040, 600)], color="#E53935", dash="6 5", sw=2)
    s.add("<path d='M1085 560 L1105 580 M1105 560 L1085 580' stroke='#E53935' stroke-width='3'/>")
    s.text(1160, 610, "Tidak ada umpan balik", size=13, weight="bold", color="#E53935")
    s.text(1160, 630, "dari ukuran kualitas ke routing", size=13, color="#E53935")
    s.tag(1480, 596, "G6")

    s.note(1140, 730, ["Keterangan:",
                       "• Semua komponen abu-abu: teknologi umum.",
                       "• Kotak merah putus-putus: plane yang kosong.",
                       "• G1–G6: hipotesis research gap (§7).",
                       "• Sumber: snapshot read-only 12 Nov 2026",
                       "  dan hasil baseline 13 Nov 2026."])
    legend_block(s, 930, [("ex", "Existing"), ("gap", "Research gap / kosong"), ("data", "Aliran data"), ("mon", "Pengukuran pasif")])
    s.save("/home/claude/diagrams/D1_existing.svg")


# =====================================================================
# DIAGRAM 2 — MONITORING
# =====================================================================
def d2():
    s = SVG(1600, 900)
    s.title("Diagram 2 — Network Monitoring Architecture",
            "Probe aktif dieksekusi router per interface; counter pasif dibaca dari router; semuanya mengalir ke ALQI Engine")
    # ISPs
    isp = [("ISP-A Starlink", "ether1-ISP-A", ic_starlink), ("ISP-B Starlink", "ether2-ISP-B", ic_starlink),
           ("ISP-C Fiber Optic", "ether3-ISP-C", ic_fiber)]
    for i, (t, e, ic) in enumerate(isp):
        y = 120 + i * 150
        s.rect(30, y, 230, 110, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
        ic(s, 42, y + 22)
        s.text(106, y + 46, t, size=13.5, weight="bold")
        s.text(106, y + 68, e, size=12, color=QUIET)
        s.arrow([(260, y + 55), (300, y + 55)], both=True)
    s.rect(300, 110, 230, 420, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=2)
    ic_router(s, 316, 124)
    s.text(316, 196, "Router MikroTik", size=15, weight="bold")
    s.lines(316, 222, ["Eksekutor pengukuran:", "", "/ping address=…", "  interface=etherX-ISP-Y", "", "/interface (rx/tx byte)", "", "/ip/firewall/connection", "  (agregat per mark)"], size=12.5, color=QUIET, lh=19)

    # active band
    s.rect(560, 100, 560, 312, fill="#F7FBFF", stroke="#90CAF9", sw=1.4, rx=14, dash="6 4")
    s.text(580, 128, "PENGUKURAN AKTIF (menyuntik paket uji)", size=14, weight="bold", color="#1565C0")
    s.box(580, 146, 255, 118, "ex", "Latency (RTT)",
          ["ICMP ke 1.1.1.1 dan 8.8.8.8", "lewat tiap interface", "Interval: 2 s → 1–2 s", "Satuan: ms (median, p95)"])
    s.box(850, 146, 255, 118, "ex", "Jitter",
          ["Selisih RTT berurutan", "(estimator RFC 3550)", "Per sampel probe", "Satuan: ms"])
    s.box(580, 278, 255, 118, "ex", "Packet loss",
          ["Rasio probe gagal", "Jendela 30–60 sampel", "Interval: 2 s", "Satuan: %"])
    s.box(850, 278, 255, 118, "ad", "Status konektivitas",
          ["Probe ke IP publik,", "bukan gateway lokal", "(rute rekursif)", "Interval: 2 s"])
    s.tag(1050, 282, "G1")

    # passive band
    s.rect(560, 430, 560, 260, fill="#F7FBFF", stroke="#90CAF9", sw=1.4, rx=14, dash="6 4")
    s.text(580, 458, "PENGUKURAN PASIF (membaca counter)", size=14, weight="bold", color="#1565C0")
    s.box(580, 474, 255, 104, "ad", "Throughput",
          ["Delta counter rx/tx per WAN", "Interval: 10 s → 1 s", "(uji siklus 15 s)"])
    s.box(850, 474, 255, 104, "ad", "Bandwidth utilization",
          ["Throughput ÷ kapasitas", "efektif terukur", "Interval: 1–2 s"])
    s.box(580, 592, 525, 84, "ex", "Stok koneksi per connection-mark (opsional)",
          ["Agregat conntrack conn-A / conn-B / conn-C", "Interval: 120 s → 30 s · dibatasi karena beban CPU router"])

    for y in (300, 560):
        s.arrow([(530, y), (560, y)], color="#1E88E5", dash="3 4", marker="arB")

    # collector -> store -> ALQI
    s.rect(1160, 230, 190, 150, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_monitor(s, 1174, 246)
    s.text(1174, 316, "Kolektor", size=15, weight="bold")
    s.lines(1174, 338, ["collector.py", "API-SSL read-only"], size=12, color=QUIET)
    s.rect(1160, 470, 190, 150, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_db(s, 1176, 486)
    s.text(1174, 558, "Time-series store", size=14, weight="bold")
    s.lines(1174, 580, ["JSONL → SQLite/Influx", "ts, link, kind, nilai"], size=12, color=QUIET)
    s.rect(1390, 400, 180, 130, fill=CAT["dev"][0], stroke=CAT["dev"][1], sw=2)
    ic_gear(s, 1404, 414)
    s.text(1404, 486, "ALQI Engine", size=15, weight="bold")
    s.text(1404, 508, "(Layer 3)", size=12, color=QUIET)
    s.arrow([(1120, 300), (1160, 300)])
    s.arrow([(1120, 560), (1140, 560), (1140, 330), (1160, 330)])
    s.arrow([(1255, 380), (1255, 470)])
    s.arrow([(1350, 545), (1370, 545), (1370, 465), (1390, 465)])
    s.text(1400, 376, "deret metrik", size=12, color=QUIET)
    s.text(1400, 392, "per ISP, T_s", size=12, color=QUIET)
    s.tag(1400, 540, "G2")
    s.text(1400, 584, "sebelumnya tidak", size=12, color="#E53935")
    s.text(1400, 600, "dipakai untuk kendali", size=12, color="#E53935")

    s.note(40, 740, ["Keterangan:",
                     "• Aktif = mengukur jalur dengan paket uji kecil (RTT, loss, jitter, keterjangkauan). Pasif = membaca counter tanpa beban jalur, tetapi hanya melihat trafik yang lewat.",
                     "• Format interval: existing → usulan. iperf3 tidak dipakai rutin (membebani link pelanggan); hanya di staging.",
                     "• Sampel timeout dihitung sebagai loss, bukan RTT. Resampling ke T_s dilakukan di tahap preprocessing ALQI."])
    legend_block(s, 850, [("ex", "Existing"), ("ad", "Adaptasi"), ("dev", "Pengembangan"), ("gap", "Research gap"), ("data", "Aliran data"), ("mon", "Pengukuran")])
    s.save("/home/claude/diagrams/D2_monitoring.svg")


# =====================================================================
# DIAGRAM 3 — PROPOSED
# =====================================================================
def d3():
    s = SVG(1600, 1340)
    s.title("Diagram 3 — Proposed ALQI-SAW Architecture",
            "ALQI menilai tiap ISP terhadap baseline-nya sendiri; SAW memeringkat ISP layak terhadap acuan absolut; keduanya bertemu di Routing Control")
    # L1 data plane
    s.band(20, 92, 1560, 200, "L1 · DATA PLANE")
    isp = [("ISP-A Starlink", "ether1-ISP-A", ic_starlink), ("ISP-B Starlink", "ether2-ISP-B", ic_starlink),
           ("ISP-C Fiber Optic", "ether3-ISP-C", ic_fiber)]
    for i, (t, e, ic) in enumerate(isp):
        x = 50 + i * 215
        s.rect(x, 130, 200, 120, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
        ic(s, x + 12, 146)
        s.text(x + 74, 168, t.split()[0], size=14, weight="bold")
        s.text(x + 74, 188, " ".join(t.split()[1:]), size=12.5, color=QUIET)
        s.text(x + 12, 230, e, size=12.5, color=QUIET)
        s.line([(x + 100, 250), (x + 100, 268), (700, 268)], color="#37474F")
    s.arrow([(700, 268), (700, 200), (720, 200)], both=False)
    s.rect(720, 110, 400, 168, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=2)
    ic_router(s, 734, 120)
    s.text(800, 146, "MikroTik RouterOS v7", size=15, weight="bold")
    s.lines(734, 192, ["PCC 20 bucket → conn-A / conn-B / conn-C",
                       "mark-routing → to-ISP-A / B / C (tetap)",
                       "Rute rekursif + cadangan distance 2",
                       "NAT masquerade · conntrack"], size=12.5, color=QUIET, lh=19)
    s.arrow([(1120, 200), (1150, 200)])
    for i, (t, ic) in enumerate([("Switch", ic_switch), ("Access Point", ic_ap), ("Client", ic_client)]):
        x = 1150 + i * 140
        s.rect(x, 140, 128, 120, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
        ic(s, x + 34, 156)
        s.text(x + 64, 236, t, size=13, weight="bold", anchor="middle")
        if i < 2:
            s.arrow([(x + 128, 200), (x + 140, 200)])

    # L2 monitoring
    s.band(20, 306, 1560, 160, "L2 · MONITORING")
    s.box(50, 324, 340, 124, "ex", "Probe aktif (di router)",
          ["RTT, jitter, loss via /ping interface=", "ke IP publik · tiap 1–2 s"])
    s.box(410, 324, 340, 124, "ad", "Counter pasif",
          ["Throughput, utilisasi · tiap 1 s", "Stok koneksi per mark · 30 s"])
    s.rect(770, 324, 350, 124, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    ic_db(s, 784, 344)
    s.text(840, 352, "Kolektor + time-series store", size=14, weight="bold")
    s.lines(840, 376, ["JSONL · API-SSL read-only", "audit: state, V_i, bucket"], size=12, color=QUIET)
    s.tag(330, 328, "G1")
    s.arrow([(390, 386), (410, 386)])
    s.arrow([(750, 386), (770, 386)])
    s.arrow([(900, 278), (900, 300), (220, 300), (220, 324)], color="#1E88E5", dash="3 4", marker="arB")
    s.text(540, 296, "eksekusi probe & counter di router", size=12, color="#1E88E5")

    # L3/L4 decision
    s.band(20, 480, 1560, 420, "L3–L4 · DECISION PLANE")
    s.rect(50, 496, 720, 390, fill=CAT["dev"][0], stroke=CAT["dev"][1], sw=2.2, op=0.6)
    ic_gear(s, 64, 506)
    s.text(118, 524, "L3 · ALQI Processing Engine", size=16, weight="bold")
    s.text(118, 544, "Pertanyaan: apakah ISP ini memburuk dibanding normalnya sendiri?", size=12.5, color=QUIET)
    st = [("ex", "1 Acquisition", ["JSONL → deret", "per ISP"]),
          ("ex", "2 Preprocessing", ["resampling T_s,", "timeout = loss"]),
          ("ad", "3 Baseline per ISP", ["median & MAD", "bergulir"]),
          ("dev", "4 Normalisasi", ["deviasi robust", "z → d ∈ [0,1]"]),
          ("dev", "5 Assessment", ["A_i(t) =", "1 − Σ v_j d_ij"]),
          ("ad", "6 Filtering", ["Hampel + EWMA α"]),
          ("ad", "7 Hysteresis", ["θ_deg/θ_rec,", "k_down < k_up"]),
          ("dev", "8 Output", ["state NORMAL/", "DEGRADED/DOWN"])]
    for i, (c, t, b) in enumerate(st):
        r, k = divmod(i, 4)
        x = 66 + k * 174
        y = 566 + r * 160
        s.box(x, y, 160, 120, c, t, b, tsize=13, bsize=12)
        if k < 3:
            s.arrow([(x + 160, y + 60), (x + 174, y + 60)])
    s.arrow([(66 + 3 * 174 + 80, 686), (66 + 3 * 174 + 80, 700), (146, 700), (146, 726)])
    s.tag(530, 652, "G3")
    s.tag(530, 812, "G5")
    s.arrow([(945, 448), (945, 470), (410, 470), (410, 496)])
    s.arrow([(945, 470), (1060, 470), (1060, 496)])

    s.rect(800, 496, 520, 350, fill=CAT["ad"][0], stroke=CAT["ad"][1], sw=2.2, op=0.6)
    ic_saw(s, 814, 500)
    s.text(872, 524, "L4 · SAW Decision Engine", size=16, weight="bold")
    s.text(872, 544, "Pertanyaan: berapa porsi koneksi baru tiap ISP?", size=12.5, color=QUIET)
    sw_ = [("ex", "1 Matriks keputusan", ["ISP layak × C1–C4"]),
           ("ex", "2 Kriteria", ["C1–C3 cost, C4 benefit"]),
           ("ad", "3 Pembobotan", ["statis / entropy / γ"]),
           ("ad", "4 Normalisasi N-c", ["acuan TIPHON tetap"]),
           ("ex", "5 Preferensi", ["V_i = Σ w_j r_ij"]),
           ("dev", "6 Ranking + δ", ["deadband peringkat"])]
    for i, (c, t, b) in enumerate(sw_):
        r, k = divmod(i, 2)
        x = 816 + k * 248
        y = 566 + r * 94
        s.box(x, y, 236, 80, c, t, b, tsize=13, bsize=12)
    s.tag(1250, 570, "G2")
    s.tag(1250, 664, "G4")

    s.rect(1350, 496, 210, 390, fill=CAT["dev"][0], stroke=CAT["dev"][1], sw=2.4)
    s.text(1364, 526, "D1 · Gerbang", size=15, weight="bold")
    s.lines(1364, 552, ["eligibility × preference", "", "e_i dari state ALQI:", "NORMAL = 1", "DEGRADED = ε", "DOWN = 0", "", "× V_i dari SAW", "× C_i kapasitas", "efektif"], size=12.5, color=INK, lh=20)
    s.arrow([(770, 870), (1350, 870)], color="#EF6C00", marker="arO")
    s.text(830, 864, "state + A_i(t)  (juga menyaring baris matriks SAW)", size=12, color="#EF6C00")
    s.arrow([(1320, 680), (1350, 680)])

    # L5 control
    s.band(20, 914, 1560, 196, "L5 · CONTROL PLANE")
    s.rect(50, 930, 760, 164, fill=CAT["dev"][0], stroke=CAT["dev"][1], sw=2.2)
    ic_route(s, 64, 944)
    s.text(122, 962, "Routing Control Engine (D2 + D3)", size=16, weight="bold")
    s.lines(70, 1000, ["T_i ∝ e_i · V_i · C_i   →   b_i = clip(round(N·T_i), b_min, b_max),  Σ b_i = N = 20",
                       "Reassignment minimum: hanya bucket yang berubah ditulis ulang",
                       "Change budget per menit · snapshot → apply → verify → rollback"], size=13, color=INK, lh=22)
    s.tag(740, 936, "G6")
    s.rect(840, 930, 330, 164, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    s.text(856, 960, "Aktuator RouterOS (API-SSL)", size=14, weight="bold")
    s.lines(856, 986, ["Akun write terpisah", "set new-connection-mark", "pada aturan PCC 20/k", "Koneksi lama: mark tetap"], size=12.5, color=QUIET)
    s.rect(1200, 930, 360, 164, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    s.text(1216, 960, "Fail-static di router", size=14, weight="bold")
    s.lines(1216, 986, ["Failover keras tetap berjalan", "walau controller mati:", "check-gateway rekursif +", "rute cadangan distance 2"], size=12.5, color=QUIET)
    s.arrow([(1455, 886), (1455, 920), (430, 920), (430, 930)], color="#EF6C00", marker="arO")
    s.arrow([(810, 1012), (840, 1012)], color="#EF6C00", dash="7 5", marker="arO")
    s.arrow([(1005, 1094), (1005, 1116), (1588, 1116), (1588, 100), (920, 100), (920, 110)], color="#EF6C00", dash="7 5", marker="arO")
    s.text(1575, 1110, "kontrol: tulis pemetaan bucket ke router", size=12, color="#EF6C00", anchor="end")

    # L6 eval
    s.band(20, 1124, 1560, 150, "L6 · EVALUASI")
    s.box(50, 1140, 760, 120, "ex", "Performance Evaluation",
          ["Throughput/goodput · latency p95 · jitter · loss · availability",
           "Waktu deteksi · waktu perpindahan · Kendall τ peringkat · perpindahan ISP per jam",
           "Pembanding P0–P7 (§11), unit analisis = episode degradasi"])
    s.rect(840, 1140, 720, 120, fill=CAT["rc"][0], stroke=CAT["rc"][1], sw=2.2)
    s.text(856, 1166, "Kontribusi yang diharapkan", size=15, weight="bold")
    s.lines(856, 1192, ["RC1  D1 menurunkan perpindahan tak perlu tanpa memperlambat deteksi",
                        "RC2  D2 menurunkan perubahan aturan & gangguan sesi, QoS ≥ PCC statis",
                        "RC3  Atribusi kontribusi tiap komponen lewat ablasi"], size=12.5, color=INK, lh=20)
    s.arrow([(810, 1200), (840, 1200)], color="#2E7D32", marker="arG")

    legend_block(s, 1296)
    s.save("/home/claude/diagrams/D3_proposed.svg")


# =====================================================================
# DIAGRAM 4 — ROUTING CONTROL FLOW
# =====================================================================
def diamond(s, cx, cy, w, h, cat, lines_):
    fill, stroke = CAT[cat]
    s.add(f"<polygon points='{cx-w/2},{cy} {cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2}' fill='{fill}' stroke='{stroke}' stroke-width='1.8'/>")
    n = len(lines_)
    for i, t in enumerate(lines_):
        s.text(cx, cy + 5 + (i - (n - 1) / 2) * 17, t, size=12.5, weight="bold", anchor="middle")


def d4():
    s = SVG(1600, 1290)
    s.title("Diagram 4 — Routing Control and Decision Flow",
            "Satu siklus keputusan (tiap T_d) mengubah hanya pemetaan bucket PCC; jalur paket dan failover keras tetap di router")
    s.rect(20, 92, 1010, 1060, fill="#FFFBF5", stroke="#FFCC80", sw=1.3, rx=14, dash="6 4")
    s.text(40, 120, "DECISION + CONTROL PLANE (controller, out-of-band)", size=14, weight="bold", color="#E65100")
    s.rect(1050, 92, 530, 1060, fill="#F7F9FA", stroke="#CFD8DC", sw=1.3, rx=14, dash="6 4")
    s.text(1070, 120, "DATA PLANE (RouterOS v7, per koneksi)", size=14, weight="bold", color="#546E7A")

    X, W = 80, 420
    cx = X + W / 2
    s.box(X, 140, W, 56, "ex", "Mulai siklus T_d (mis. 10 s, dikalibrasi)", [], center=True)
    s.arrow([(cx, 196), (cx, 220)])
    s.box(X, 220, W, 70, "dev", "Baca keluaran ALQI", ["state & A_i(t) untuk ISP-A, ISP-B, ISP-C"], center=True)
    s.arrow([(cx, 290), (cx, 312)])
    diamond(s, cx, 362, 260, 100, "ad", ["State", "ISP i?"])
    # three branches
    br = [("NORMAL", "e_i = 1", 560), ("DEGRADED", "e_i = ε (→ b_min)", 680), ("DOWN", "e_i = 0 (keluar matriks)", 800)]
    for lab, val, yy in br:
        pass
    s.box(560, 316, 420, 92, "dev", "Tetapkan kelayakan e_i",
          ["NORMAL → 1 · DEGRADED → ε (dapat b_min)", "DOWN → 0 (tidak ikut SAW)"])
    s.arrow([(cx + 130, 362), (560, 362)])
    s.arrow([(770, 408), (770, 430), (cx, 430), (cx, 446)])
    s.box(X, 446, W, 72, "ad", "SAW: hitung V_i untuk ISP dengan e_i > 0", ["normalisasi N-c, bobot w_j"], center=True)
    s.arrow([(cx, 518), (cx, 540)])
    diamond(s, cx, 600, 320, 120, "dev", ["|ΔV| > δ atau", "state berubah?"])
    s.tag(cx + 120, 548, "G5")
    s.box(620, 566, 360, 68, "ex", "Pertahankan alokasi", ["tidak ada penulisan ke router"], center=True)
    s.arrow([(cx + 160, 600), (620, 600)])
    s.text(cx + 175, 590, "tidak", size=12, color=QUIET)
    s.arrow([(cx, 660), (cx, 690)])
    s.text(cx + 10, 680, "ya", size=12, color=QUIET)
    s.box(X, 690, W, 100, "dev", "Hitung alokasi bucket (D2)",
          ["T_i ∝ e_i · V_i · C_i", "b_i = clip(round(20·T_i), b_min, b_max)", "sisa pembulatan: largest remainder"])
    s.arrow([(cx, 790), (cx, 812)])
    s.box(X, 812, W, 72, "dev", "Reassignment minimum", ["bandingkan dengan pemetaan sekarang;", "pilih bucket yang harus pindah saja"])
    s.arrow([(cx, 884), (cx, 904)])
    diamond(s, cx, 954, 300, 100, "dev", ["Change budget", "terpenuhi?"])
    s.box(620, 922, 360, 64, "ex", "Tunda ke siklus berikut", ["catat alasan di log audit"], center=True)
    s.arrow([(cx + 150, 954), (620, 954)])
    s.text(cx + 165, 944, "tidak", size=12, color=QUIET)
    s.arrow([(cx, 1004), (cx, 1030)])
    s.text(cx + 10, 1022, "ya", size=12, color=QUIET)
    s.box(X, 1030, W, 100, "ex", "Terapkan via API-SSL",
          ["snapshot → set new-connection-mark", "untuk bucket terpilih → verify (print)", "gagal → rollback ke snapshot"])
    s.tag(X + W - 60, 1036, "G6")

    # data plane lane
    RX, RW = 1080, 470
    rcx = RX + RW / 2
    s.box(RX, 150, RW, 66, "ex", "Koneksi baru dari client", ["chain prerouting, connection-state=new"], center=True)
    s.arrow([(rcx, 216), (rcx, 240)])
    s.rect(RX, 240, RW, 150, fill=CAT["ex"][0], stroke=CAT["ex"][1], sw=1.8)
    s.text(rcx, 266, "PCC both-addresses-and-ports:20/k", size=14, weight="bold", anchor="middle")
    s.text(rcx, 290, "k = 0 … 19  (20 aturan tetap, resolusi 5%)", size=12.5, color=QUIET, anchor="middle")
    s.rect(RX + 20, 304, RW - 40, 70, fill=CAT["dev"][0], stroke=CAT["dev"][1], sw=2)
    s.text(rcx, 330, "bucket k → new-connection-mark", size=13, weight="bold", anchor="middle")
    s.text(rcx, 354, "conn-A / conn-B / conn-C  (satu-satunya yang diubah)", size=12.5, anchor="middle")
    s.arrow([(rcx, 390), (rcx, 414)])
    s.box(RX, 414, RW, 66, "ex", "mark-routing: conn-X → to-ISP-X", ["aturan tetap, tidak pernah ditulis controller"], center=True)
    s.arrow([(rcx, 480), (rcx, 504)])
    s.box(RX, 504, RW, 96, "ex", "Routing table to-ISP-X",
          ["default via ISP-X, check-gateway rekursif ke IP publik", "cadangan distance 2 via ISP lain (failover keras)"], center=True)
    s.arrow([(rcx, 600), (rcx, 624)])
    s.box(RX, 624, RW, 66, "ex", "NAT masquerade → ether1 / ether2 / ether3", ["keluar ke ISP terpilih"], center=True)
    s.box(RX, 730, RW, 110, "ex", "Koneksi lama (sudah ber-mark)",
          ["conntrack mempertahankan connection-mark", "→ sesi berjalan tidak terputus oleh", "perubahan rasio; hanya koneksi baru terdampak"], center=True)
    s.box(RX, 870, RW, 110, "ex", "Fail-static",
          ["controller mati → pemetaan terakhir tetap;", "failover keras tetap ditangani", "routing table (tanpa controller)"], center=True)
    # control arrow
    s.arrow([(X + W, 1080), (1020, 1080), (1020, 340), (RX + 20, 340)], color="#EF6C00", dash="7 5", marker="arO")
    s.text(1012, 700, "tulis", size=12.5, color="#EF6C00", anchor="end")
    s.text(1012, 716, "bucket", size=12.5, color="#EF6C00", anchor="end")

    s.note(40, 1176, ["Keterangan: kelayakan (ALQI) dan preferensi (SAW) digabung sebagai e_i × V_i × C_i (pendekatan kombinasi). Ranking murni (semua koneksi ke ISP peringkat 1) tidak dipakai karena",
                      "mematikan load balancing; distribusi murni tidak dipakai karena tetap mengirim koneksi ke link DEGRADED. Nilai T_d, δ, ε, b_min, b_max, dan change budget dikalibrasi eksperimen."])
    legend_block(s, 1236, [("ex", "Existing"), ("ad", "Adaptasi"), ("dev", "Pengembangan"), ("gap", "Research gap"), ("data", "Aliran proses"), ("ctrl", "Aliran kontrol")])
    s.save("/home/claude/diagrams/D4_routing_control.svg")


# =====================================================================
# DIAGRAM 5 — GAP & NOVELTY
# =====================================================================
def d5():
    s = SVG(1600, 1180)
    s.title("Diagram 5 — Research Gap and Novelty Mapping",
            "Novelty bukan SAW, PCC, baseline, atau histeresis secara terpisah, melainkan tiga mekanisme integrasi (D1–D3) yang dapat diuji dengan ablasi")
    s.text(220, 112, "RESEARCH GAP (hipotesis)", size=14, weight="bold", color="#C62828", anchor="middle")
    s.text(800, 112, "KOMPONEN ARSITEKTUR", size=14, weight="bold", color="#37474F", anchor="middle")
    s.text(1390, 112, "KONTRIBUSI YANG DIBUKTIKAN", size=14, weight="bold", color="#2E7D32", anchor="middle")

    gaps = [("G1", "Pemantauan kualitas ISP", "celah praktik (bukan novelty)", 140),
            ("G2", "Metrik QoS tidak jadi masukan", "didukung untuk konteks PCC", 290),
            ("G3", "Kualitas relatif baseline ISP", "HIPOTESIS TERBUKA — cari bukti", 440),
            ("G4", "Keputusan multikriteria temporal", "didukung (G-N1, G-N2 repo)", 590),
            ("G5", "Ketidakstabilan keputusan", "kuat (data + Tournaire 2023)", 740),
            ("G6", "Algoritma → aturan routing", "kuat (arsip G-M2, G-E2)", 890)]
    for code, t, st, y in gaps:
        s.rect(40, y, 360, 100, fill=CAT["gap"][0], stroke=CAT["gap"][1], sw=2)
        s.tag(54, y + 12, code)
        s.text(104, y + 30, t, size=14, weight="bold")
        s.text(54, y + 68, st, size=12.5, color="#C62828")

    comps = {
        "l2ex": (470, 140, 300, 100, "ex", "Probe aktif + counter", ["kolektor existing"]),
        "l2ad": (790, 140, 330, 100, "ad", "Probe IP publik + counter 1 s", ["deteksi upstream"]),
        "l4ex": (470, 290, 300, 100, "ex", "SAW (V_i = Σ w_j r_ij)", ["penggabung linear"]),
        "l3ad": (790, 290, 330, 100, "ad", "Baseline median/MAD + Hampel", ["per ISP, per jam-hari"]),
        "l4ad": (470, 590, 650, 100, "ad", "Normalisasi acuan tetap N-c · bobot statis/entropy/hibrida γ", ["dari Vafaei 2021, entropy-SAW; diuji pada deret real-time"]),
        "d1": (470, 440, 650, 100, "dev", "D1 · Penilaian dua referensi", ["state ALQI relatif-baseline menggerbangi preferensi SAW absolut"]),
        "d3": (470, 740, 650, 100, "dev", "D3 · Stabilitas dua skala waktu", ["histeresis asimetris state + deadband δ + change budget; aturan A&B turun"]),
        "d2": (470, 890, 650, 100, "dev", "D2 · Pemetaan berbatas ke bucket PCC", ["b_min/b_max, largest remainder, reassignment minimum, fail-static"]),
    }
    for k, (x, y, w, h, c, t, b) in comps.items():
        s.box(x, y, w, h, c, t, b, tsize=14, bsize=12.5)
    s.text(800, 1022, "Existing di bawah tiap layer: PCC, mark, routing table, NAT, EWMA, histeresis dua ambang, TIPHON", size=12.5, color=QUIET, anchor="middle")

    R = "#E53935"
    s.arrow([(400, 190), (430, 190), (430, 130), (955, 130), (955, 140)], color=R, marker="arR")
    s.arrow([(400, 340), (470, 340)], color=R, marker="arR")
    s.arrow([(400, 462), (445, 462), (445, 280), (955, 280), (955, 290)], color=R, marker="arR")
    s.arrow([(400, 500), (470, 500)], color=R, marker="arR")
    s.arrow([(400, 640), (470, 640)], color=R, marker="arR")
    s.arrow([(400, 670), (430, 670), (430, 525), (470, 525)], color=R, marker="arR", dash="5 4")
    s.arrow([(400, 790), (470, 790)], color=R, marker="arR")
    s.arrow([(400, 940), (470, 940)], color=R, marker="arR")

    rcs = [("RC1", ["D1 menurunkan perpindahan tak perlu", "tanpa memperlambat deteksi degradasi", "Uji: P6 vs P3 (ALQI acuan absolut)"], 420),
           ("RC3", ["Atribusi kontribusi tiap komponen", "lewat ablasi P0–P6, effect size + CI", "Uji: model efek campuran, Holm"], 640),
           ("RC2", ["D2 menurunkan perubahan aturan dan", "gangguan sesi, QoS ≥ PCC statis", "Uji: P6 vs P5 (pemetaan naif), P0"], 860)]
    for code, ls, y in rcs:
        s.rect(1190, y, 380, 130, fill=CAT["rc"][0], stroke=CAT["rc"][1], sw=2.2)
        s.tag(1204, y + 12, code, cat="rc")
        s.lines(1204, y + 60, ls, size=12.5, color=INK, lh=19)
    G = "#2E7D32"
    s.arrow([(1120, 490), (1190, 490)], color=G, marker="arG")
    s.arrow([(1120, 925), (1190, 925)], color=G, marker="arG")
    s.arrow([(1120, 790), (1150, 790), (1150, 705), (1190, 705)], color=G, marker="arG")
    s.line([(1150, 490), (1150, 925)], color=G, sw=1.6, dash="4 4")

    s.note(40, 1060, ["Keterangan: panah merah = gap yang dijawab komponen; panah merah putus-putus = jawaban parsial. Panah hijau = komponen yang menjadi dasar kontribusi.",
                      "Klaim \"belum ada\" untuk D1–D3 hanya boleh ditulis setelah log pencarian lintas basis data (aturan repo); G3 wajib diverifikasi lebih dulu."])
    legend_block(s, 1126, [("ex", "Existing"), ("ad", "Adaptasi"), ("dev", "Pengembangan"), ("gap", "Research gap"), ("rc", "Kontribusi")])
    s.save("/home/claude/diagrams/D5_gap_novelty.svg")


for f in (d1, d2, d3, d4, d5):
    f()
print("ok")
