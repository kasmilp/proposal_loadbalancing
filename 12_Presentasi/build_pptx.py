#!/usr/bin/env python3
"""Membangun deck proposal tesis SPA-HSM (16:9)."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

# ---------- Palet ----------
NAVY = RGBColor(0x0B, 0x25, 0x45)
TEAL = RGBColor(0x13, 0xA8, 0x9E)
ORANGE = RGBColor(0xF2, 0xA5, 0x41)
LIGHT = RGBColor(0xF5, 0xF7, 0xFA)
GRAY = RGBColor(0x5A, 0x6B, 0x7B)
MID = RGBColor(0xD9, 0xE2, 0xEC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x1B, 0x1B, 0x1B)
RED = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x2E, 0x7D, 0x32)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def rect(slide, left, top, width, height, fill, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08):
    shp = slide.shapes.add_shape(shape, Inches(left), Inches(top), Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    shp.text_frame.text = ""
    return shp


def text(slide, value, left, top, width, height, size=18, bold=False, color=DARK,
         font="Arial", align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = value
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    return box


def bullets(slide, items, left, top, width, height, size=17, color=DARK,
            bullet_char="•", space=7):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    first = True
    for item in items:
        level = 0
        if isinstance(item, tuple):
            item, level = item
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        prefix = bullet_char + " " if bullet_char and level == 0 else ("– " if level else "")
        p.text = prefix + item
        p.level = level
        p.space_after = Pt(space)
        for run in p.runs:
            run.font.size = Pt(size - (2 if level else 0))
            run.font.color.rgb = color if level == 0 else GRAY
            run.font.name = "Arial"
    return box


def title_bar(slide, title, kicker=None):
    rect(slide, 0, 0, 13.333, 1.02, NAVY, shape=MSO_SHAPE.RECTANGLE)
    rect(slide, 0, 1.02, 13.333, 0.055, TEAL, shape=MSO_SHAPE.RECTANGLE)
    if kicker:
        text(slide, kicker.upper(), 0.55, 0.16, 10.5, 0.25, 10, True, TEAL)
        text(slide, title, 0.55, 0.38, 12.2, 0.55, 25, True, WHITE)
    else:
        text(slide, title, 0.55, 0.30, 12.2, 0.55, 26, True, WHITE)


def footer(slide, page, note="Proposal Tesis — SPA-HSM"):
    text(slide, note, 0.55, 7.12, 8.5, 0.22, 9, False, GRAY)
    text(slide, str(page), 12.25, 7.12, 0.55, 0.22, 9, False, GRAY, align=PP_ALIGN.RIGHT)


def add_notes(slide, content):
    slide.notes_slide.notes_text_frame.text = content


def table(slide, rows, left, top, width, height, col_widths=None, font_size=11,
          header_fill=NAVY, first_col_bold=False):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(left), Inches(top),
                                   Inches(width), Inches(height))
    tbl = shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = Inches(w)
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = tbl.cell(r, c)
            cell.text = str(value)
            cell.margin_left = Inches(0.06)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = header_fill
            else:
                cell.fill.fore_color.rgb = WHITE if r % 2 else LIGHT
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
                for run in p.runs:
                    run.font.size = Pt(font_size)
                    run.font.name = "Arial"
                    run.font.color.rgb = WHITE if r == 0 else DARK
                    run.font.bold = (r == 0) or (first_col_bold and c == 0)
    return tbl


def arrow_right(slide, left, top, width=0.28, height=0.22, color=TEAL):
    shp = rect(slide, left, top, width, height, color, shape=MSO_SHAPE.RIGHT_ARROW, radius=0)
    return shp


def new_slide():
    return prs.slides.add_slide(BLANK)


# =====================================================================
# 1. TITLE
# =====================================================================
s = new_slide()
rect(s, 0, 0, 13.333, 7.5, NAVY, shape=MSO_SHAPE.RECTANGLE)
rect(s, 0, 0, 0.18, 7.5, TEAL, shape=MSO_SHAPE.RECTANGLE)
rect(s, 10.7, 0.0, 2.633, 7.5, RGBColor(0x10, 0x30, 0x55), shape=MSO_SHAPE.RECTANGLE)
text(s, "PROPOSAL TESIS MAGISTER", 0.85, 0.85, 9.8, 0.3, 12, True, TEAL)
text(s, "SPA-HSM", 0.85, 1.35, 9.6, 0.9, 46, True, WHITE)
text(s, "Kendali Proporsi Aliran Adaptif dan Sadar-Sesi\npada WAN Heterogen Fiber Optic–LEO",
     0.85, 2.30, 9.8, 1.15, 25, True, WHITE)
text(s, "Studi Kasus Jaringan RT/RW Net Dual-ISP", 0.85, 3.55, 9.8, 0.35, 15, False, MID, italic=True)
rect(s, 0.85, 4.18, 2.2, 0.05, ORANGE, shape=MSO_SHAPE.RECTANGLE)
text(s, "Kasmil Papalia  •  D082252011", 0.85, 4.45, 9.8, 0.32, 15, True, WHITE)
text(s, "Magister Teknik Informatika  •  Universitas Hasanuddin", 0.85, 4.85, 9.8, 0.30, 13, False, MID)
text(s, "14 November 2026", 0.85, 5.25, 9.8, 0.30, 12, False, GRAY)

# Ornamen kanan
for i, (label, color) in enumerate([("EWMA", TEAL), ("SAW", TEAL), ("HISTERESIS", ORANGE), ("AFFINITY", ORANGE)]):
    rect(s, 10.95, 1.55 + i * 1.05, 1.75, 0.62, color, radius=0.25)
    text(s, label, 10.95, 1.66 + i * 1.05, 1.75, 0.28, 10, True, WHITE, align=PP_ALIGN.CENTER)
rect(s, 10.95, 5.75, 1.75, 0.62, RGBColor(0x1B, 0x4D, 0x7A), radius=0.25)
text(s, "SIWG", 10.95, 5.86, 1.75, 0.28, 10, True, WHITE, align=PP_ALIGN.CENTER)
add_notes(s, "Perkenalkan judul, fokus pada SPA-HSM dan WAN FO–LEO. Tegaskan bahwa MikroTik adalah adapter, bukan objek penelitian.")

# =====================================================================
# 2. AGENDA
# =====================================================================
s = new_slide()
title_bar(s, "Agenda", "Alur presentasi")
items = [
    ("01", "Latar belakang & masalah"),
    ("02", "Gap & novelty"),
    ("03", "Pertanyaan & hipotesis"),
    ("04", "Kerangka teori & SPA-HSM"),
    ("05", "Metodologi & evaluasi"),
    ("06", "Baseline awal"),
    ("07", "Kontribusi & jadwal"),
    ("08", "Risiko, batasan & penutup"),
]
for i, (num, label) in enumerate(items):
    col = 0 if i < 4 else 1
    row = i % 4
    x = 0.85 + col * 6.1
    y = 1.55 + row * 1.18
    rect(s, x, y, 0.58, 0.58, TEAL if i % 2 == 0 else ORANGE, shape=MSO_SHAPE.OVAL)
    text(s, num, x, y + 0.12, 0.58, 0.32, 14, True, WHITE, align=PP_ALIGN.CENTER)
    text(s, label, x + 0.78, y + 0.10, 5.0, 0.38, 17, False, DARK)
footer(s, 2)
add_notes(s, "Deck mengikuti alur proposal: masalah, gap, novelty, teori, metode, baseline, lalu kontribusi dan jadwal.")

# =====================================================================
# 3. LATAR BELAKANG
# =====================================================================
s = new_slide()
title_bar(s, "Latar Belakang", "Mengapa FO–LEO dan PCC")
cols = [
    ("FO Terestrial", "Latensi rendah, kapasitas tinggi", [
        "Kualitas operasional tidak konstan",
        "Kepadatan pelanggan & gangguan akses",
        "Degradasi berskala menit–jam",
    ], TEAL),
    ("Starlink LEO", "Jangkauan luas, dinamis", [
        "Variabilitas throughput & latensi tinggi",
        "Rain fade dan outage",
        "Transien rekonfigurasi ~15 detik (literatur)",
    ], ORANGE),
    ("PCC RouterOS", "Konsisten per sesi", [
        "Connection mark + routing mark",
        "Sesi lama bertahan di conntrack",
        "Rasio umumnya statis",
    ], NAVY),
]
for i, (head, sub, body, color) in enumerate(cols):
    x = 0.6 + i * 4.15
    rect(s, x, 1.40, 3.85, 4.55, WHITE, line=MID)
    rect(s, x, 1.40, 3.85, 0.12, color, shape=MSO_SHAPE.RECTANGLE)
    text(s, head, x + 0.22, 1.65, 3.4, 0.32, 18, True, color)
    text(s, sub, x + 0.22, 2.00, 3.4, 0.28, 11, False, GRAY, italic=True)
    bullets(s, body, x + 0.22, 2.45, 3.4, 2.3, 12, DARK, space=8)
    impl = ["→ perlu skor multi-kriteria", "→ perlu histeresis & dwell", "→ perlu rasio adaptif"][i]
    text(s, impl, x + 0.22, 5.05, 3.4, 0.28, 10, True, color)
rect(s, 0.6, 6.15, 12.13, 0.62, NAVY, radius=0.12)
text(s, "Tantangan: rasio statis tidak merespons degradasi; pembaruan naif memicu flapping dan gangguan sesi.",
     0.8, 6.30, 11.7, 0.30, 13, True, WHITE)
footer(s, 3)
add_notes(s, "Tegaskan dua skala waktu: FO lambat, LEO cepat. PCC menjaga sesi tetapi rasionya statis. Inilah titik masalah.")

# =====================================================================
# 4. MASALAH
# =====================================================================
s = new_slide()
title_bar(s, "Masalah Penelitian", "Tiga kegagalan mekanisme statis")
problems = [
    ("01", "Flapping", "Derau metrik dan transien LEO membuat rasio berubah bolak-balik bila diperbarui setiap siklus.", ORANGE),
    ("02", "Gangguan sesi", "Perubahan aturan PCC dapat memengaruhi sesi TCP: reordering, retransmisi, hingga RST.", RED),
    ("03", "Parameter ad hoc", "Dwell histeresis tidak diturunkan dari durasi transien; dampaknya ke sesi tidak diukur.", TEAL),
]
for i, (num, head, body, color) in enumerate(problems):
    x = 0.7 + i * 4.2
    rect(s, x, 1.55, 3.85, 3.55, WHITE, line=MID)
    rect(s, x, 1.55, 0.12, 3.55, color, shape=MSO_SHAPE.RECTANGLE)
    text(s, num, x + 0.25, 1.72, 0.7, 0.4, 24, True, color)
    text(s, head, x + 0.95, 1.78, 2.7, 0.35, 19, True, DARK)
    text(s, body, x + 0.28, 2.35, 3.25, 1.9, 13, False, GRAY)
    ind = ["Indikator: flapping rate", "Indikator: RST flow", "Indikator: recovery & parameter"][i]
    text(s, ind, x + 0.28, 4.55, 3.25, 0.25, 9, True, color)
rect(s, 0.7, 5.45, 11.95, 1.05, LIGHT, line=MID)
text(s, "Akibat", 0.95, 5.60, 1.4, 0.30, 12, True, NAVY)
text(s, "Alokasi tidak sadar-kondisi → QoS agregat turun, sesi berisiko, dan praktisi tidak punya dasar kuantitatif memilih parameter.",
     2.15, 5.58, 10.2, 0.70, 13, False, DARK)
footer(s, 4)
add_notes(s, "Tiga masalah ini yang harus dijawab bersama, bukan terpisah. Flapping dan gangguan sesi adalah dua sisi dari trade-off yang sama.")

# =====================================================================
# 5. GAP
# =====================================================================
s = new_slide()
title_bar(s, "Research Gap", "Apa yang belum tersedia")
rows = [
    ["Gap", "Kondisi literatur", "Yang belum ada"],
    ["G-M1", "Histeresis dipakai di cloud/handover", "Dwell tidak diturunkan dari transien LEO terukur"],
    ["G-M2", "SAW menghasilkan skor kontinu", "Pemetaan formal skor → bucket PCC diskret"],
    ["G-E1", "PCC mengklaim menjaga sesi", "Dampak perubahan rasio ke RST belum diukur"],
    ["G-C1", "PCC diuji pada ISP homogen/lab", "Evaluasi lapangan dual-ISP FO–LEO"],
]
table(s, rows, 0.65, 1.35, 12.0, 3.2, col_widths=[1.1, 5.2, 5.7], font_size=12)
rect(s, 0.65, 4.85, 12.0, 0.75, NAVY, radius=0.12)
text(s, "Pencarian OpenAlex 2015–2026: PCC × histeresis/dwell = 0 hit; PCC × preservasi sesi = 2 studi lokal tanpa RST.",
     0.85, 5.02, 11.6, 0.40, 12, True, WHITE)
text(s, "Posisi: bukan menciptakan MCDM/EWMA/histeresis baru, tetapi menyatukan dan mengukur trade-off-nya.",
     0.65, 5.95, 12.0, 0.35, 13, False, GRAY, italic=True)
footer(s, 5)
add_notes(s, "Gap utama ada di G-M1 dan G-E1. G-I1 integrasi hanya payung. Sebutkan pencarian OpenAlex sebagai bukti awal, bukan klaim universal.")

# =====================================================================
# 6. NOVELTY
# =====================================================================
s = new_slide()
title_bar(s, "Novelty", "Tiga kontribusi yang diklaim")
cards = [
    ("N1", "Dwell sadar-transien", "k_down·T_s > T_tr + m\nT_tr ≈ 15 detik (literatur)\nmenekan flapping tanpa recovery berlebih.", TEAL),
    ("N2", "Formalisasi skor → bucket", "Σb_i = N; b_min ≤ b_i ≤ b_max\nmenjembatani Q_i kontinu dan PCC diskret.", ORANGE),
    ("N3", "SIWG + ablasi", "Mengukur trade-off stabilitas–kontinuitas\nlewat flapping, RST, goodput, latensi.", NAVY),
]
for i, (num, head, body, color) in enumerate(cards):
    x = 0.65 + i * 4.25
    rect(s, x, 1.45, 3.95, 3.9, WHITE, line=MID)
    rect(s, x, 1.45, 3.95, 0.10, color, shape=MSO_SHAPE.RECTANGLE)
    text(s, num, x + 0.25, 1.65, 0.8, 0.4, 22, True, color)
    text(s, head, x + 0.95, 1.70, 2.7, 0.55, 16, True, DARK)
    text(s, body, x + 0.28, 2.45, 3.35, 2.0, 12, False, GRAY)
    bukti = ["Bukti: kurva flapping–recovery", "Bukti: uji 10.000 kombinasi skor", "Bukti: ablasi A–G + SIWG"][i]
    text(s, bukti, x + 0.28, 4.55, 3.35, 0.25, 9, True, color)
rect(s, 0.65, 5.65, 12.0, 0.62, LIGHT, line=MID)
text(s, "Integrasi EWMA + SAW + histeresis + affinity adalah payung sistem, bukan novelty tunggal.",
     0.85, 5.80, 11.6, 0.30, 12, True, NAVY)
footer(s, 6)
add_notes(s, "Urutan klaim: N1 aturan desain, N2 formalisasi, N3 bukti empiris. Hindari klaim metode dasar baru.")

# =====================================================================
# 7. PERTANYAAN PENELITIAN
# =====================================================================
s = new_slide()
title_bar(s, "Pertanyaan Penelitian", "Satu payung, lima sub-pertanyaan")
text(s, "Sejauh mana SPA-HSM mengendalikan trade-off stabilitas keputusan dan kontinuitas sesi pada WAN FO–LEO?",
     0.65, 1.30, 12.0, 0.60, 15, True, NAVY)
rqs = [
    ("RQ1", "Bagaimana merumuskan Q_i(t) dan memetakannya ke bucket PCC?"),
    ("RQ2", "Bagaimana aturan dwell sadar-transien menggeser flapping vs recovery?"),
    ("RQ3", "Seberapa besar AFFINITY_LOCK menurunkan RST dan gangguan aliran?"),
    ("RQ4", "Bagaimana SIWG dan ablasi menunjukkan kontribusi tiap komponen?"),
    ("RQ5", "Apakah Algorithm Core memenuhi kontrak dan portabel di dua adapter?"),
]
for i, (code, body) in enumerate(rqs):
    y = 2.10 + i * 0.92
    rect(s, 0.65, y, 0.75, 0.55, TEAL if i % 2 == 0 else ORANGE, radius=0.25)
    text(s, code, 0.65, y + 0.11, 0.75, 0.28, 11, True, WHITE, align=PP_ALIGN.CENTER)
    text(s, body, 1.65, y + 0.03, 10.9, 0.50, 14, False, DARK)
footer(s, 7)
add_notes(s, "RQ2 dan RQ3 adalah inti novelty. RQ5 validasi rekayasa, bukan klaim portabilitas multi-vendor.")

# =====================================================================
# 8. TUJUAN & HIPOTESIS
# =====================================================================
s = new_slide()
title_bar(s, "Tujuan & Hipotesis", "Apa yang diuji dan dengan ambang apa")
text(s, "Tujuan", 0.65, 1.30, 3.2, 0.30, 15, True, TEAL)
tujuan = [
    "Formalisasi Q_i(t) dan bucket PCC.",
    "Aturan dwell sadar-transien.",
    "Implementasi dan pengukuran AFFINITY_LOCK.",
    "Ablasi + SIWG.",
    "Uji kontrak dan portabilitas inti.",
]
bullets(s, tujuan, 0.65, 1.70, 3.55, 3.6, 12, DARK, space=9)
text(s, "Hipotesis", 4.55, 1.30, 3.2, 0.30, 15, True, TEAL)
rows = [
    ["ID", "Klaim", "Ambang"],
    ["H1", "Histeresis menekan flapping", "IRR < 0,5; recovery p95 ≤ 90 s"],
    ["H2", "Asimetri memperbaiki trade-off", "IRR < 0,7; Δrecovery ≤ 30 s"],
    ["H3a", "Affinity menjaga sesi", "Non-inferior +0,5 pp; sekunder <1%"],
    ["H3b", "Kinerja agregat naik", "Goodput ≥1,10×; latency ≤0,85×"],
    ["H4", "SIWG lebih tinggi", "Rasio ≥1,15; CI >1,00"],
    ["H5", "Inti portabel", "100% keputusan identik"],
]
table(s, rows, 4.55, 1.70, 8.1, 4.5, col_widths=[0.75, 3.15, 4.2], font_size=10)
text(s, "Catatan: ambang final dikalibrasi setelah pilot; definisi operasional dikunci sebelum data.",
     4.55, 6.35, 8.1, 0.30, 10, False, GRAY, italic=True)
footer(s, 8)
add_notes(s, "Jangan membaca semua baris. Tekankan H1/H2 untuk stabilitas, H3a untuk sesi, H4 untuk trade-off gabungan.")

# =====================================================================
# 9. KERANGKA TEORI
# =====================================================================
s = new_slide()
title_bar(s, "Kerangka Teori", "Dari degradasi link ke SIWG")
stages = [
    ("Degradasi\nlink", "FO/LEO"),
    ("Metrik\nQoS", "delay, jitter,\nloss, throughput"),
    ("EWMA", "α = 0,20"),
    ("Q_i(t)", "SAW,\nbatas tetap"),
    ("Histeresis", "θ, k_down,\nk_up"),
    ("Bucket\nPCC", "N = 20"),
    ("Flapping &\nsesi", "RST, goodput"),
    ("SIWG", "trade-off"),
]
x = 0.55
for i, (head, sub) in enumerate(stages):
    color = TEAL if i in (2, 3) else (ORANGE if i in (4, 5) else NAVY)
    rect(s, x, 1.65, 1.40, 1.55, WHITE, line=MID)
    rect(s, x, 1.65, 1.40, 0.08, color, shape=MSO_SHAPE.RECTANGLE)
    text(s, head, x + 0.08, 1.82, 1.24, 0.52, 11, True, DARK, align=PP_ALIGN.CENTER)
    text(s, sub, x + 0.06, 2.38, 1.28, 0.60, 8, False, GRAY, align=PP_ALIGN.CENTER)
    if i < len(stages) - 1:
        arrow_right(s, x + 1.44, 2.28, 0.20, 0.18, color)
    x += 1.60
text(s, "Transien ~15 detik: Garcia et al. (2025); Hammer et al. (2024); Mohan et al. (2024).  Histeresis: Tournaire et al. (2023); Alhabo et al. (2017).",
     0.65, 3.55, 12.0, 0.45, 10, False, GRAY, italic=True)
rect(s, 0.65, 4.20, 12.0, 1.85, LIGHT, line=MID)
text(s, "Dua proposisi yang diuji", 0.85, 4.38, 5.0, 0.30, 13, True, NAVY)
bullets(s, [
    "P1 — Memilih k_down·T_s > T_tr + m mencegah transien periodik memicu DEGRADED berulang, dengan biaya detection delay.",
    "P2 — Untuk θ tetap, menaikkan k_up menurunkan flapping tetapi menaikkan recovery latency; pasangan ini membentuk frontier trade-off.",
    "Implikasi — empat komponen diuji bersama; efek tidak dapat diatribusikan jika dipisah.",
], 0.85, 4.72, 11.5, 1.2, 10.5, DARK, space=5)
footer(s, 9)
add_notes(s, "Rantai ini menjelaskan mengapa komponen tidak bisa dinilai terpisah. P1 dan P2 adalah proposisi desain yang diuji, bukan teorema formal.")

# =====================================================================
# 10. ARSITEKTUR
# =====================================================================
s = new_slide()
title_bar(s, "Arsitektur SPA-HSM", "Tiga lapis + bidang pengukuran dan evaluasi")
# Kiri
rect(s, 0.55, 1.45, 2.55, 4.65, WHITE, line=MID)
text(s, "Measurement", 0.75, 1.62, 2.2, 0.30, 13, True, TEAL)
text(s, "Field", 0.75, 1.95, 2.2, 0.25, 10, False, GRAY)
bullets(s, ["Probe per WAN", "SNMP counter", "Starlink telemetry", "Cuaca"], 0.75, 2.35, 2.15, 2.6, 11, DARK, space=6)
# Tengah: tiga lapis
layers = [
    ("Algorithm Core", "EWMA  •  SAW  •  State machine  •  Ratio mapper", NAVY, 1.45, 1.25),
    ("Abstract Allocation Interface", "read_metrics  •  set_ratio  •  set_affinity  •  verify  •  rollback", TEAL, 3.05, 1.10),
    ("Platform Adapter", "MikroTikAdapter (PCC, conntrack)  •  MockAdapter (unit test)", ORANGE, 4.50, 1.10),
]
for head, body, color, y, h in layers:
    rect(s, 3.45, y, 6.0, h, color, radius=0.12)
    text(s, head, 3.68, y + 0.12, 5.6, 0.30, 15, True, WHITE)
    text(s, body, 3.68, y + 0.48, 5.55, 0.55, 10, False, WHITE)
# Panah vertikal antar lapis
for y in (2.72, 4.18):
    rect(s, 6.25, y, 0.28, 0.30, WHITE, shape=MSO_SHAPE.DOWN_ARROW, radius=0)
# Kanan
rect(s, 9.85, 1.45, 2.9, 4.65, WHITE, line=MID)
text(s, "Evaluation", 10.05, 1.62, 2.5, 0.30, 13, True, ORANGE)
text(s, "& Ablation", 10.05, 1.92, 2.5, 0.25, 10, False, GRAY)
bullets(s, ["Skenario A–G", "Flapping", "RST flow", "Goodput", "Latency p95", "SIWG"], 10.05, 2.32, 2.45, 2.9, 11, DARK, space=5)
text(s, "Inti tidak mengimpor API vendor.", 9.85, 6.25, 2.9, 0.30, 10, True, NAVY, align=PP_ALIGN.CENTER)
footer(s, 10)
add_notes(s, "Tiga lapis memisahkan keputusan, kontrak, dan eksekusi. MockAdapter memungkinkan uji tanpa menyentuh produksi.")

# =====================================================================
# 11. FORMALISASI
# =====================================================================
s = new_slide()
title_bar(s, "Formalisasi Inti", "Rumus yang dieksekusi")
# Kiri
rect(s, 0.55, 1.35, 6.05, 2.55, WHITE, line=MID)
text(s, "Skor kualitas", 0.75, 1.50, 5.6, 0.30, 13, True, TEAL)
text(s, "E_i(t) = α·x_i(t) + (1−α)·E_i(t−1)", 0.75, 1.88, 5.6, 0.30, 13, False, DARK, font="Consolas")
text(s, "Q_i(t) = Σ_j w_j · r_ij(t),   Q_i ∈ [0,1]", 0.75, 2.28, 5.6, 0.30, 13, False, DARK, font="Consolas")
text(s, "α = 0,20  •  N_eff ≈ 9  •  w = (0,35; 0,30; 0,15; 0,20)", 0.75, 2.72, 5.6, 0.30, 11, False, GRAY)
text(s, "Normalisasi berbatas tetap: throughput (benefit), delay/jitter/loss (cost).", 0.75, 3.10, 5.6, 0.55, 10, False, GRAY)
# Kanan
rect(s, 6.85, 1.35, 5.95, 2.55, WHITE, line=MID)
text(s, "Histeresis & rasio", 7.05, 1.50, 5.5, 0.30, 13, True, ORANGE)
text(s, "STABLE → DEGRADED: Q < θ_low selama k_down", 7.05, 1.88, 5.5, 0.30, 11, False, DARK)
text(s, "DEGRADED → STABLE: Q > θ_high selama k_up", 7.05, 2.20, 5.5, 0.30, 11, False, DARK)
text(s, "k_down·T_s > T_tr + m   (T_tr ≈ 15 s)", 7.05, 2.56, 5.5, 0.30, 12, True, NAVY, font="Consolas")
text(s, "T_s = 1 s; k_down = 20; k_up = 20/60; θ = 0,60/0,80", 7.05, 2.94, 5.5, 0.30, 10, False, GRAY)
text(s, "W_i = Q_i·H_i / Σ Q_k·H_k;  b_i = round(N·W_i)", 7.05, 3.30, 5.5, 0.30, 11, False, DARK, font="Consolas")
# Bawah
rect(s, 0.55, 4.20, 12.25, 1.95, LIGHT, line=MID)
text(s, "Mengapa ini bukan sekadar integrasi", 0.75, 4.36, 11.8, 0.30, 13, True, NAVY)
bullets(s, [
    "N1: parameter dwell diturunkan dari durasi transien, bukan dipilih ad hoc.",
    "N2: skor kontinu dipetakan ke bucket integer dengan jaminan Σb_i = N dan batas b_min/b_max.",
    "N3: SIWG dan ablasi memisahkan kontribusi histeresis vs preservasi sesi.",
    "Ukuran keberhasilan: flapping turun, recovery ≤ R_max, dan SIWG naik.",
], 0.75, 4.74, 11.5, 1.2, 10.5, DARK, space=5)
footer(s, 11)
add_notes(s, "Tunjukkan dua blok: skor kualitas dan keputusan. Tekankan aturan dwell sebagai kontribusi N1 dan bucket mapping sebagai N2.")

# =====================================================================
# 12. DESAIN EKSPERIMEN
# =====================================================================
s = new_slide()
title_bar(s, "Desain Eksperimen", "Tujuh kondisi, faktorial 2×2 + pembanding")
rows = [
    ["Kondisi", "Histeresis", "k_up", "Affinity", "Peran"],
    ["A", "Tidak ada (statis 50:50)", "—", "—", "Baseline statis"],
    ["B", "Tidak ada (dinamis)", "—", "Off", "Dynamic naive"],
    ["C", "Simetris", "20", "Off", "Isolasi bentuk"],
    ["D", "Asimetris", "60", "Off", "Isolasi asimetri"],
    ["E", "Simetris", "20", "On", "Affinity pada simetris"],
    ["F", "Asimetris", "60", "On", "SPA-HSM (usulan)"],
    ["G", "Tidak ada", "—", "—", "Baseline netwatch"],
]
table(s, rows, 0.65, 1.35, 7.4, 3.8, col_widths=[0.9, 2.9, 0.8, 0.9, 1.9], font_size=10)
text(s, "Perbandingan kunci", 8.4, 1.35, 4.2, 0.30, 13, True, TEAL)
bullets(s, [
    "H1: B vs C; B vs D.",
    "H2: C vs D; E vs F.",
    "H3a: C vs E; D vs F; F vs A.",
    "H3b: F vs A; F vs G.",
    "H4: F vs semua kondisi.",
], 8.4, 1.72, 4.3, 2.3, 11, DARK, space=6)
rect(s, 8.4, 4.10, 4.3, 1.55, LIGHT, line=MID)
text(s, "Kontrol", 8.58, 4.24, 3.9, 0.25, 11, True, NAVY)
text(s, "Latin square 7×7; washout 10 menit; dua jendela waktu; 30 episode/kondisi; dual-ISP A+C, B validasi.",
     8.58, 4.56, 3.95, 1.0, 9, False, GRAY)
text(s, "Staging: tc netem + trace replay + MockAdapter.  Lapangan: RT/RW Net produksi.",
     0.65, 5.55, 12.0, 0.55, 11, False, GRAY)
footer(s, 12)
add_notes(s, "Jelaskan bahwa A–F bukan 3×2 penuh. H1 memakai B vs C/D karena affinity off, agar terisolasi.")

# =====================================================================
# 13. METRIK & INSTRUMEN
# =====================================================================
s = new_slide()
title_bar(s, "Metrik & Instrumen", "Diukur, bukan diasumsikan")
rows = [
    ["Metrik", "Definisi", "Instrumen"],
    ["Flapping rate", "Flap per jam", "Log controller"],
    ["Recovery latency", "Awal episode → STABLE (p95)", "Log state"],
    ["RST flow", "% aliran TCP dengan ≥1 RST", "tcpdump/Wireshark"],
    ["Goodput", "Byte aplikasi / durasi", "iperf3 / HTTP"],
    ["Latency p95", "RTT probe per WAN", "Router /ping per interface"],
    ["SIWG", "G_eff × (1 − λ·RST_flow)", "Dihitung per episode"],
]
table(s, rows, 0.65, 1.35, 8.0, 3.9, col_widths=[1.7, 3.0, 3.3], font_size=10)
rect(s, 8.95, 1.35, 3.85, 2.35, NAVY, radius=0.12)
text(s, "SIWG", 9.15, 1.52, 3.4, 0.30, 15, True, WHITE)
text(s, "SIWG = G_eff × (1 − λ·RST_flow)", 9.15, 1.90, 3.4, 0.30, 11, False, WHITE, font="Consolas")
text(s, "λ = 1 primer; sensitivitas 0,25 / 0,5 / 1,0", 9.15, 2.28, 3.4, 0.30, 9, False, MID)
text(s, "Membuat biaya gangguan sesi eksplisit.", 9.15, 2.70, 3.4, 0.55, 9, False, MID)
rect(s, 8.95, 4.00, 3.85, 1.25, LIGHT, line=MID)
text(s, "Prinsip", 9.15, 4.14, 3.4, 0.25, 11, True, ORANGE)
text(s, "RST diukur di luar router. Probe per WAN memakai routing mark/interface eksplisit.",
     9.15, 4.46, 3.45, 0.65, 9, False, GRAY)
text(s, "Kalibrasi pilot 24–48 jam: SNMP vs probe vs capture; uji RST terkontrol; fail-static; rollback <60 detik.",
     0.65, 5.65, 12.0, 0.55, 10, False, GRAY, italic=True)
footer(s, 13)
add_notes(s, "Tekankan RST flow dan goodput, bukan hanya throughput router. SIWG adalah alat pembanding internal, bukan standar industri.")

# =====================================================================
# 14. ANALISIS
# =====================================================================
s = new_slide()
title_bar(s, "Rencana Analisis", "Model sesuai jenis data")
text(s, "Outcome", 0.65, 1.35, 3.0, 0.30, 13, True, TEAL)
bullets(s, [
    "Primer: flapping, RST flow, goodput, SIWG.",
    "Sekunder: recovery p95, RST packet, latensi p95, jitter, loss, overhead.",
    "Effect size: IRR, Cohen's d, Cliff's δ.",
], 0.65, 1.72, 3.5, 1.7, 10, DARK, space=6)
rect(s, 0.65, 3.35, 3.45, 1.15, LIGHT, line=MID)
text(s, "Unit analisis", 0.82, 3.48, 3.1, 0.25, 10, True, NAVY)
text(s, "Episode degradasi / jam / aliran — bukan setiap sampel 1 detik.", 0.82, 3.78, 3.1, 0.60, 9, False, GRAY)
rows = [
    ["Hipotesis", "Model", "Efek"],
    ["H1, H2", "Negative binomial campuran + offset jam", "IRR + 95% CI"],
    ["H3a", "Logistik/beta campuran + bootstrap", "Selisih pp + CI"],
    ["H3b", "LMM log(goodput), log(latency p95)", "Rasio + CI"],
    ["H4", "LMM SIWG + sensitivitas λ", "Rasio + CI"],
    ["H5", "Uji konformitas + exact match", "% identik"],
]
table(s, rows, 4.35, 1.35, 8.25, 3.25, col_widths=[1.1, 4.4, 2.75], font_size=10)
rect(s, 4.35, 4.95, 8.25, 1.25, LIGHT, line=MID)
text(s, "Kekuatan & keputusan", 4.55, 5.08, 7.8, 0.25, 11, True, NAVY)
text(s, "30–40 episode/kondisi; Holm–Bonferroni; effect size + 95% CI; data hilang dilaporkan, bukan diimputasi.",
     4.55, 5.40, 7.8, 0.60, 9, False, GRAY)
footer(s, 14)
add_notes(s, "Hindari t-test sebagai default. Tekankan unit analisis dan koreksi multiplisitas.")

# =====================================================================
# 15. BASELINE
# =====================================================================
s = new_slide()
title_bar(s, "Baseline Awal 2,2 Jam", "Pilot read-only, 13 November 2026")
rows = [
    ["WAN", "Jitter", "RTT p95", "Loss", "Episode"],
    ["Starlink A", "7,0 ms", "89–102 ms", "0,17–0,24%", "35–53"],
    ["Starlink B", "7,6–7,8 ms", "99–114 ms", "0,27–0,30%", "51–84"],
    ["FO C", "0,3 ms", "46,7 ms", "0–0,03%", "0–1"],
]
table(s, rows, 0.65, 1.40, 6.9, 2.0, col_widths=[1.7, 1.3, 1.5, 1.3, 1.1], font_size=10)
# Chart
chart_data = CategoryChartData()
chart_data.categories = ["Starlink A", "Starlink B", "FO C"]
chart_data.add_series("Jitter RTT (ms)", (7.0, 7.7, 0.3))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7.9), Inches(1.30),
                        Inches(4.9), Inches(2.5), chart_data)
chart = gf.chart
chart.has_legend = False
chart.has_title = True
chart.chart_title.text_frame.text = "Jitter RTT (ms)"
chart.chart_title.text_frame.paragraphs[0].font.size = Pt(11)
chart.chart_title.text_frame.paragraphs[0].font.bold = True
plot = chart.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = "0.0"
plot.data_labels.font.size = Pt(9)
plot.series[0].format.fill.solid()
plot.series[0].format.fill.fore_color.rgb = TEAL
chart.category_axis.tick_labels.font.size = Pt(9)
chart.value_axis.tick_labels.font.size = Pt(8)
chart.value_axis.maximum_scale = 9
text(s, "Temuan", 0.65, 3.70, 12.0, 0.30, 13, True, TEAL)
bullets(s, [
    "Heterogenitas nyata: jitter Starlink ~7 ms vs FO ~0,3 ms; episode pendek Starlink jauh lebih sering.",
    "Dua Starlink berkorelasi: residual r = 0,68–0,70; A–C dan B–C ≈ 0.",
    "Implikasi: dual-ISP formal A+C; ISP-B sebagai validasi eksternal, bukan link formal ketiga.",
    "Baseline 2,2 jam cukup untuk pilot; belum mewakili jam sibuk, hujan, dan variasi harian.",
], 0.65, 4.00, 12.0, 1.7, 10.5, DARK, space=4)
rect(s, 0.65, 5.85, 12.1, 0.62, LIGHT, line=MID)
text(s, "Catatan: klaim transien ~15 detik dikunci dari literatur (Garcia 2025; Hammer 2024; Mohan 2024). Baseline RTT belum mengonfirmasi siklus 15 detik; perlu throughput 1 detik.",
     0.85, 5.94, 11.7, 0.45, 9, False, GRAY, italic=True)
footer(s, 15)
add_notes(s, "Jangan mengklaim 15 detik dari baseline RTT. Klaim itu dari literatur. Baseline menunjukkan heterogenitas dan korelasi A–B yang tinggi.")

# =====================================================================
# 16. KONTRIBUSI
# =====================================================================
s = new_slide()
title_bar(s, "Kontribusi yang Diharapkan", "Teoretis, metodologis, praktis")
cols = [
    ("Teoretis", ["Trade-off stabilitas–kontinuitas sebagai masalah kendali.", "Aturan dwell yang menghubungkan T_s, T_tr, dan k_down.", "Frontier parameter, bukan satu titik optimal."], TEAL),
    ("Metodologis", ["Pemetaan formal skor kontinu → bucket PCC.", "SIWG sebagai ukuran gabungan.", "Ablasi 2×2 + pembanding untuk atribusi komponen."], ORANGE),
    ("Praktis", ["Panduan parameter untuk RT/RW Net.", "Fail-static dan rollback.", "Kontrak antarmuka yang dapat direplikasi."], NAVY),
]
for i, (head, body, color) in enumerate(cols):
    x = 0.65 + i * 4.2
    rect(s, x, 1.45, 3.9, 3.8, WHITE, line=MID)
    rect(s, x, 1.45, 3.9, 0.12, color, shape=MSO_SHAPE.RECTANGLE)
    text(s, head, x + 0.25, 1.65, 3.4, 0.35, 17, True, color)
    bullets(s, body, x + 0.25, 2.15, 3.4, 2.8, 11, DARK, space=8)
rect(s, 0.65, 5.60, 12.0, 0.65, NAVY, radius=0.12)
text(s, "Kontribusi utama: N1 + N3. N2 dan K5 adalah pendukung. Integrasi bukan klaim tunggal.",
     0.85, 5.76, 11.6, 0.30, 12, True, WHITE)
footer(s, 16)
add_notes(s, "Jangan mengklaim metode MCDM/EWMA/histeresis baru. Klaim pada aturan desain dan bukti empiris.")

# =====================================================================
# 17. JADWAL
# =====================================================================
s = new_slide()
title_bar(s, "Jadwal Penelitian", "20 minggu + penyangga")
phases = [
    ("Minggu 1–2", ["Desain & kontrak", "MockAdapter", "Finalisasi parameter"], TEAL),
    ("Minggu 3–4", ["Pilot 24–48 jam", "Kalibrasi probe/SNMP", "Uji RST & rollback"], TEAL),
    ("Minggu 5–6", ["tc netem", "Trace replay", "20 replay/kondisi"], ORANGE),
    ("Minggu 7–13", ["7 kondisi A–G", "Latin square", "30 episode/kondisi"], ORANGE),
    ("Minggu 14–17", ["NB/LMM/beta", "Holm + effect size", "Robustness"], NAVY),
    ("Minggu 18–20", ["Bab IV–V", "Format & sitasi", "Naskah siap"], NAVY),
]
for i, (weeks, body, color) in enumerate(phases):
    x = 0.55 + i * 2.12
    rect(s, x, 1.55, 1.95, 2.5, WHITE, line=MID)
    rect(s, x, 1.55, 1.95, 0.45, color, radius=0.08)
    text(s, weeks, x, 1.63, 1.95, 0.28, 9, True, WHITE, align=PP_ALIGN.CENTER)
    bullets(s, body, x + 0.12, 2.18, 1.72, 1.7, 8.5, DARK, space=3)
rect(s, 0.55, 4.45, 12.1, 0.10, MID, shape=MSO_SHAPE.RECTANGLE)
for i in range(6):
    rect(s, 0.85 + i * 2.12, 4.37, 0.22, 0.22, TEAL if i < 2 else (ORANGE if i < 4 else NAVY), shape=MSO_SHAPE.OVAL)
text(s, "Penyangga 2 minggu untuk cuaca, gangguan Starlink, dan revisi. Jika habis: turunkan ke A, B, D, F dan catat sebagai penyimpangan.",
     0.65, 5.15, 12.0, 0.60, 11, False, GRAY)
rect(s, 0.65, 5.95, 12.0, 0.55, LIGHT, line=MID)
text(s, "Milestone: M1 instrumen siap • M2 staging selesai • M3 lapangan selesai • M4 analisis selesai • M5 naskah siap",
     0.85, 6.10, 11.6, 0.30, 10, True, NAVY)
footer(s, 17)
add_notes(s, "Jadwal realistis 20 minggu. Sebutkan penyangga dan fallback 4 skenario.")

# =====================================================================
# 18. RISIKO & ETIKA
# =====================================================================
s = new_slide()
title_bar(s, "Risiko, Keselamatan & Etika", "Jaringan produksi harus aman")
text(s, "Risiko utama", 0.65, 1.35, 5.5, 0.30, 13, True, RED)
bullets(s, [
    "Cuaca buruk / hujan → blok waktu, perpanjang, replay staging.",
    "Starlink outage → pause, tandai run, ulangi.",
    "Perubahan ISP/firmware → catat versi, uji ulang baseline.",
    "Controller mati → fail-static, watchdog, UPS.",
    "Data hilang → buffer lokal, checksum, backup harian.",
], 0.65, 1.72, 5.8, 3.3, 10, DARK, space=7)
text(s, "Etika & keselamatan", 6.75, 1.35, 5.5, 0.30, 13, True, TEAL)
bullets(s, [
    "Izin pemilik RT/RW Net + pemberitahuan pelanggan.",
    "Anonimisasi; tidak menangkap payload.",
    "Perubahan besar hanya pada jam rendah.",
    "Rollback teruji <60 detik.",
    "Hentikan run jika pelanggan terganggu.",
], 6.75, 1.72, 5.8, 3.3, 10, DARK, space=7)
# Protokol run ringkas
run_steps = [
    ("Sebelum run", "Cuaca, backup, NTP,\ncheckpoint konfigurasi", TEAL),
    ("Saat run", "Urutan Latin square,\nalarm, log intervensi", ORANGE),
    ("Setelah run", "Ekspor, checksum,\nrollback, backup", NAVY),
]
for i, (head, body, color) in enumerate(run_steps):
    x = 0.65 + i * 4.12
    rect(s, x, 3.60, 3.90, 1.30, WHITE, line=MID)
    rect(s, x, 3.60, 0.10, 1.30, color, shape=MSO_SHAPE.RECTANGLE)
    text(s, head, x + 0.25, 3.72, 3.4, 0.28, 11, True, color)
    text(s, body, x + 0.25, 4.04, 3.4, 0.75, 9, False, GRAY)
rect(s, 0.65, 5.30, 12.0, 0.95, NAVY, radius=0.12)
text(s, "Prinsip: pelanggan tidak boleh menanggung risiko lebih besar daripada manfaat pengujian.",
     0.85, 5.48, 11.6, 0.30, 12, True, WHITE)
text(s, "Read-only untuk baseline; akun tulis terpisah dan terbatas untuk intervensi.",
     0.85, 5.86, 11.6, 0.30, 10, False, MID)
footer(s, 18)
add_notes(s, "Tegaskan fail-static dan rollback. Baseline read-only, intervensi dengan akun terpisah.")

# =====================================================================
# 19. BATASAN
# =====================================================================
s = new_slide()
title_bar(s, "Batasan Penelitian", "Klaim yang tidak dibuat")
bullets(s, [
    "Dual-ISP FO–LEO; tidak mengklaim generalisasi >2 ISP.",
    "Starlink sebagai kasus acuan upper bound transien.",
    "Bobot SAW statis; bukan pembelajaran bobot.",
    "MikroTik sebagai adapter; hanya satu adapter nyata + mock.",
    "Satu lokasi RT/RW Net; bukan skala enterprise.",
    "QoS, bukan QoE; persepsi pengguna tidak diukur.",
    "Stabilitas empiris; bukan pembuktian formal control loop.",
    "Desain 2×2 + pembanding; interaksi none×affinity tidak diuji.",
], 0.65, 1.45, 12.0, 4.9, 14, DARK, space=12)
rect(s, 0.65, 6.15, 12.0, 0.55, LIGHT, line=MID)
text(s, "Klaim dijaga sejajar dengan bukti: aturan desain + bukti empiris, bukan metode dasar baru.",
     0.85, 6.30, 11.6, 0.30, 11, True, NAVY)
footer(s, 19)
add_notes(s, "Batasan ini sengaja disebut di awal agar ekspektasi penguji realistis.")

# =====================================================================
# 20. PENUTUP
# =====================================================================
s = new_slide()
rect(s, 0, 0, 13.333, 7.5, NAVY, shape=MSO_SHAPE.RECTANGLE)
rect(s, 0, 0, 0.18, 7.5, TEAL, shape=MSO_SHAPE.RECTANGLE)
text(s, "Tiga hal yang perlu diingat", 0.85, 0.85, 11.5, 0.35, 13, True, TEAL)
text(s, "1.  Masalahnya adalah trade-off stabilitas–kontinuitas, bukan sekadar throughput.",
     0.85, 1.50, 11.6, 0.55, 21, True, WHITE)
text(s, "2.  Kebaruan ada pada aturan dwell, pemetaan bucket, dan SIWG + ablasi.",
     0.85, 2.35, 11.6, 0.55, 21, True, WHITE)
text(s, "3.  Baseline awal mendukung dual-ISP A+C; ISP-B menjadi validasi eksternal.",
     0.85, 3.20, 11.6, 0.55, 21, True, WHITE)
rect(s, 0.85, 4.25, 2.0, 0.06, ORANGE, shape=MSO_SHAPE.RECTANGLE)
text(s, "Terima kasih", 0.85, 4.65, 8.0, 0.75, 38, True, WHITE)
text(s, "Diskusi dan pertanyaan", 0.85, 5.45, 8.0, 0.35, 16, False, MID)
text(s, "Kasmil Papalia  •  D082252011  •  Magister Teknik Informatika Unhas",
     0.85, 6.25, 11.5, 0.30, 11, False, GRAY)
footer(s, 20, "")
add_notes(s, "Tutup dengan tiga pesan: masalah trade-off, novelty aturan desain, dan keputusan topologi berbasis baseline.")

# ---------- Simpan ----------
out = "12_Presentasi/Proposal_Tesis_SPA-HSM.pptx"
prs.save(out)
print(f"Tersimpan: {out}")
print(f"Jumlah slide: {len(prs.slides)}")
