# 08 — Rancangan Eksperimen

**Status:** Draf kerja
**Fungsi:** Menyusun arsitektur sistem dan skenario pengujian untuk membandingkan
indeks kualitas link berbasis SAW dengan pendekatan pembanding.

---

## 1. Arsitektur Sistem **[USULAN]**

```
┌────────────────────┐   delay/jitter/loss/throughput   ┌────────────────────────┐
│  Kolektor          │ ───────────────────────────────► │   Scoring Engine       │
│  collector.py      │                                  │  EWMA → normalisasi →  │
│  read-only → JSONL │                                  │  bobot adaptif → Q_i(t)│
└────────────────────┘                                  └───────────┬────────────┘
         │                                                          │
         ▼                                                          ▼
┌────────────────────┐                                  ┌────────────────────────┐
│ Log metrik (JSONL) │                                  │ Gerbang histeresis +   │
│ + conntrack        │ ◄──────── audit ──────────────── │ keputusan (opsional)   │
└────────────────────┘                                  └────────────────────────┘
```

- **Kolektor:** `11_Kolektor_Baseline/collector.py` — read-only, `librouteros` API-SSL,
  `/print` + `/ping interface=` (probe di router) → JSONL **[FAKTA]**.
- **Router:** MikroTik RB1100AHx4, RouterOS 7.22.2 — diposisikan sebagai **adapter/
  testbed**, bukan objek penelitian **[FAKTA arsip]**.
- **Jalur (tri-link, sesuai kolektor):** `ether1-ISP-A` = Starlink LEO-1;
  `ether2-ISP-B` = Starlink LEO-2; `ether3-ISP-C` = FO IndiHome.
- **Server Controller:** layanan terpisah (Python 3.11), dapat dijalankan di staging.

**Konsekuensi tri-link [USULAN]** (dari arsip `02_Matriks_Keputusan_Topologi.md` §3):

- **State machine:** 3 link → **8 kombinasi status** (bukan 4).
- **Bucket mapping:** $N$ slot dibagi tiga link; tetapkan $b_{\min}$/$b_{\max}$ baru
  (mis. 2 dan 14 untuk $N=20$) + uji kelayakan.
- **Analisis:** model harus mengakomodasi **korelasi antar-LEO** (lihat §7).
- **Uji independensi:** korelasi transien LEO-1–LEO-2 wajib dilaporkan; ambang
  informatif arsip **< 0,7**.

**Prinsip risiko [USULAN]:** eksperimen kausal utama dilakukan **offline (replay
dataset)** dan **staging (`tc/netem`)**; lapangan hanya untuk validasi eksternal.

---

## 2. Variabel (Tabel 7)

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

## 4. Skenario Pengujian (Tabel 8) **[USULAN]**

Desain dibagi **dua dimensi ortogonal** — selaras `13_Perbaikan_Proposal_Lama.md` §5
dan sub-RQ4 pada `09_Rumusan_Masalah_dan_Judul.md`.

**(a) Perlakuan sistem** (level variabel bebas = bentuk fungsi kontrol). Kode perlakuan
**A/B/D/F/G/H** **berbeda** dari kode ISP (**ISP-A/ISP-B/ISP-C**) — jangan tertukar.

| Kode | Perlakuan | Peran | Kode di `13` §5 |
|---|---|---|---|
| A | PCC statis (rasio tetap) | Baseline utama | A |
| B | Skor $Q_i(t)$ **tanpa histeresis** | Mengisolasi efek gerbang | B |
| D | Histeresis **simetris** | Pembanding bentuk gerbang | D |
| F | Histeresis **asimetris** (sistem usulan) | Sistem yang diusulkan | F |
| G | Baseline praktisi (mis. netwatch failover) | Jangkar praktik | G |
| H | Alokasi sadar-stok (*opsional*) | Isolasi kontribusi stok | H |

**(b) Kondisi / pola degradasi** (variabel yang diamati, bukan dimanipulasi penuh)

| Kode | Kondisi | Tujuan |
|---|---|---|
| N | Normal (kedua link sehat) | Baseline akurasi & stabilitas |
| T | **Transien LEO** (pola 15 detik) | Ketahanan terhadap lonjakan singkat |
| S | **Degradasi FO bertahap** (kongesti) | Respons degradasi *sustained* |
| R | **Rain fade** (penurunan throughput) | Bobot kontekstual |
| K | Kombinasi T + S | Uji interaksi |

Setiap kombinasi perlakuan × kondisi diulang dengan **counterbalancing** urutan dan
diblok berdasarkan jam. Fokus utama (menguji H1–H3): **B vs D vs F** (efek gerbang) dan
**A vs F** (efek keseluruhan).

---

## 5. Pembanding **[USULAN]**

| Pembanding | Kode | Peran |
|---|---|---|
| PCC statis (naskah lama) | A | Baseline utama |
| $Q$ tanpa gerbang histeresis | B | Mengisolasi efek gerbang |
| Histeresis **simetris** | D | Pembanding bentuk gerbang (di `13` §5) |
| Baseline praktisi (netwatch failover) | G | Jangkar praktik (di `13` §5) |
| Alokasi sadar-stok | H | Isolasi kontribusi stok (opsional) |
| Bobot sama-rata (1/4) | — | Baseline naif |
| **Entropy-SAW** (Wireless Networks, 2021) | — | Pembanding kuat — sumber diferensiasi |
| Metrik tunggal terbaik (mis. goodput saja) | — | *Lower bound* |

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
- **Tiga link & korelasi antar-LEO:** model harus mengakomodasi tiga link dan korelasi
  LEO-1–LEO-2 (mis. random effect per link / struktur korelasi AR(1)); laporkan
  koefisien korelasi transien sebagai kovariat.

---

## 8. Parameter Awal (perlu dikalibrasi) **[USULAN]**

| Parameter | Nilai awal | Catatan |
|---|---|---|
| Interval polling $T_s$ | 1 detik | Perangkat |
| $\alpha$ EWMA | 0,10–0,20 | Uji sensitivitas |
| Jendela bobot $N$ | 30–60 sampel | Uji sensitivitas |
| $\gamma$ hibrida | 0,5 | Uji {0; 0,25; 0,5; 0,75; 1} |
| $\theta_{\text{degradasi}}$ | 60 (skala $Q$ 0–100) | Setara 0,60 skala 0–1; kalibrasi dari pilot |
| $\theta_{\text{pemulihan}}$ | 80 | $> \theta_{\text{degradasi}}$ → sumber asimetri |
| $k_{\text{down}}$ | 20 sampel | $k_{\text{down}}\cdot T_s \approx 20$ dtk $>$ transien 15 dtk |
| $k_{\text{up}}$ | 60 (asimetris) / 20 (simetris) | Asimetri waktu; uji sensitivitas |
| Jendela flap $W$ | 5 menit | Uji 1/5/15 |
| Ulangan staging | 30–64 | Agar bertenaga |

**[ANALISIS]** Nilai $\theta$ dan $k$ di atas **wajib diberi angka** (temuan M7/M13 di
`12_Pengamatan_Proposal_Lama.md`) agar dapat direplikasi — jangan dibiarkan sebagai
simbol tanpa nilai seperti pada naskah lama.

---

## 9. Ancaman Validitas **[ANALISIS]**

| Ancaman | Jenis | Mitigasi |
|---|---|---|
| Cuaca & beban tak terkendali | Eksternal | Fokus kausal di staging; blok & stratifikasi |
| Overfitting bobot | Internal | Uji sensitivitas & rank reversal |
| Ground truth lemah | Konstruk | Pakai goodput + label episode |
| Sampling tidak sinkron | Internal | Tandai toleransi waktu sampling |
| Perubahan aturan mengganggu sesi | Eksternal | Mode pantau pasif pada fase awal |
| **Dua Starlink berkorelasi (co-located)** | Eksternal/Konstruk | Uji independensi (< 0,7); laporkan korelasi A–B; fallback ke dual-ISP + validasi tri (Opsi 3 arsip) |
