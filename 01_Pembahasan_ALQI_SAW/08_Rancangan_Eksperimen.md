# 08 — Rancangan Eksperimen

**Status:** Draf kerja
**Fungsi:** Menyusun arsitektur sistem dan skenario pengujian untuk membandingkan
indeks kualitas link berbasis SAW dengan pendekatan pembanding.

---

## 1. Arsitektur Sistem **[USULAN]**

```
┌────────────────────┐   delay/jitter/loss/throughput   ┌────────────────────────┐
│  Metric Collector  │ ───────────────────────────────► │   Scoring Engine       │
│  (SNMP/API + probe)│                                  │  EWMA → normalisasi →  │
│  read-only         │                                  │  bobot adaptif → Q_i(t)│
└────────────────────┘                                  └───────────┬────────────┘
         │                                                          │
         ▼                                                          ▼
┌────────────────────┐                                  ┌────────────────────────┐
│ Log metrik (JSONL) │                                  │ Gerbang histeresis +   │
│ + conntrack        │ ◄──────── audit ──────────────── │ keputusan (opsional)   │
└────────────────────┘                                  └────────────────────────┘
```

- **Kolektor:** sudah tersedia di arsip `11_Kolektor_Baseline/collector.py`
  (mode *read-only*, API terpisah) **[FAKTA]**.
- **Router:** MikroTik RB1100AHx4, RouterOS 7.22.2 — diposisikan sebagai **adapter/
  testbed**, bukan objek penelitian **[FAKTA arsip]**.
- **Jalur:** FO IndiHome (WAN1) + Starlink LEO (WAN2).
- **Server Controller:** layanan terpisah (Python 3.11), dapat dijalankan di staging.

**Prinsip risiko [USULAN]:** eksperimen kausal utama dilakukan **offline (replay
dataset)** dan **staging (`tc/netem`)**; lapangan hanya untuk validasi eksternal.

---

## 2. Variabel

| Jenis | Variabel | Level |
|---|---|---|
| **Bebas 1** | Teknik normalisasi | N-a (linear max), N-b (min–max), N-c (batas acuan tetap) |
| **Bebas 2** | Skema pembobotan | statis-ahli, sama-rata, entropy, CRITIC, MEREC, hibrida($\gamma$) |
| **Terikat 1** | Akurasi indeks | Korelasi Spearman $Q$ vs *ground truth* goodput/utility |
| **Terikat 2** | Stabilitas indeks | Std $Q$, laju *chattering*, jumlah *rank reversal* |
| **Terikat 3** | Deteksi degradasi | AUC/ROC terhadap label episode |
| **Terikat 4** | Biaya komputasi | Waktu skoring per siklus (s) |
| **Kontrol** | Interval polling, $N$, $\alpha$, batas share | tetap antar-perlakuan |

**Ground truth [USULAN]:** label episode degradasi (dari data lapangan/log) dan
goodput terukur; untuk data sintetis, label berasal dari pola yang disuntikkan.

---

## 3. Bertingkat (Layered) **[USULAN]**

| Tingkat | Tujuan | Cara | Risiko ke pelanggan |
|---|---|---|---|
| **L1 — Offline (replay)** | Validasi konstruk indeks | Replay dataset baseline JSONL + sintesis transien | **Nol** |
| **L2 — Staging terkendali** | Validasi internal (kausal) | `tc/netem` meniru 2 pola degradasi; ulangan 30–64× | Nol (lab) |
| **L3 — Lapangan (opsional)** | Validasi eksternal | Mode pantau pasif; jam rendah risiko + izin | Rendah |

**[FAKTA]** Aset L1 sudah tersedia: dataset baseline `baseline_rb1100ahx4_*.jsonl`
(termasuk rekaman **2,2 jam**, 13 Nov 2026) di arsip `11_Kolektor_Baseline/data/`.

---

## 4. Skenario Pengujian **[USULAN]**

| Kode | Kondisi | Tujuan |
|---|---|---|
| A | Link normal (kedua sehat) | Baseline akurasi & stabilitas |
| B | **Transien LEO** (pola 15 dtk) | Uji ketahanan indeks terhadap lonjakan singkat |
| C | **Degradasi FO sustained** (kongesti bertahap) | Uji respons terhadap degradasi nyata |
| D | **Rain fade** (penurunan throughput) | Uji bobot kontekstual |
| E | Kombinasi B + C | Uji interaksi |

Masing-masing diulang dengan **counterbalancing** urutan dan diblok berdasarkan jam.

---

## 5. Pembanding **[USULAN]**

| Pembanding | Peran |
|---|---|
| Skor statis (naskah lama) | Baseline utama |
| Bobot sama-rata (1/4) | Baseline naif |
| **Entropy-SAW** (Wireless Networks, 2021) | Pembanding kuat — sumber diferensiasi |
| Metrik tunggal terbaik (mis. goodput saja) | *Lower bound* |
| $Q$ tanpa gerbang histeresis | Mengisolasi efek gerbang |

---

## 6. Metrik Evaluasi & Indikator Keberhasilan **[USULAN]**

| Metrik | Definisi | Ambang sukses usulan |
|---|---|---|
| Spearman $\rho$ ($Q$ vs goodput) | Keselarasan peringkat | $\geq 0{,}7$ (lebih baik dari baseline statis) |
| *Rank reversal count* | Pembalikan peringkat saat bobot diganggu ±20% | $\leq 10\%$ pasangan (metode Vafaei) |
| *Index chattering rate* | Perubahan $Q$ > ambang per satuan waktu | turun $\geq 30\%$ dengan gerbang |
| Deteksi episode (AUC) | Kemampuan menandai degradasi | $\text{AUC} \geq 0{,}85$ |
| Waktu skoring/siklus | Latensi komputasi | $\leq 1$ detik |
| *Recovery latency* | Waktu pemulihan setelah degradasi | $\leq$ batas target (mis. 90 dtk) |

---

## 7. Rencana Statistik **[USULAN]**

- **Perbandingan antar-metode:** ANOVA satu arah atau Kruskal–Wallis (bila tidak
  normal), dilanjutkan post hoc.
- **Effect size & 95% CI** untuk setiap perbandingan.
- **Koreksi Holm** untuk keluarga perbandingan (mencegah p-hacking).
- **Bootstrap** untuk distribusi non-normal.
- **Jangan** memakai uji-t sampel independen untuk data deret waktu berurutan
  (kelemahan naskah lama). Bila data berulang, pertimbangkan *mixed-effects*/GEE.
- Tetapkan **primary outcome** dan **smallest effect of interest** sebelum eksperimen.

---

## 8. Parameter Awal (perlu dikalibrasi) **[USULAN]**

| Parameter | Nilai awal | Catatan |
|---|---|---|
| Interval polling $T_s$ | 1 detik | Perangkat |
| $\alpha$ EWMA | 0,10–0,20 | Uji sensitivitas |
| Jendela bobot $N$ | 30–60 sampel | Uji sensitivitas |
| $\gamma$ hibrida | 0,5 | Uji {0; 0,25; 0,5; 0,75; 1} |
| Jendela flap $W$ | 5 menit | Uji 1/5/15 |
| Ulangan staging | 30–64 | Agar bertenaga |

---

## 9. Ancaman Validitas **[ANALISIS]**

| Ancaman | Jenis | Mitigasi |
|---|---|---|
| Cuaca & beban tak terkendali | Eksternal | Fokus kausal di staging; blok & stratifikasi |
| Overfitting bobot | Internal | Uji sensitivitas & rank reversal |
| Ground truth lemah | Konstruk | Pakai goodput + label episode |
| Sampling tidak sinkron | Internal | Tandai toleransi waktu sampling |
| Perubahan aturan mengganggu sesi | Eksternal | Mode pantau pasif pada fase awal |
