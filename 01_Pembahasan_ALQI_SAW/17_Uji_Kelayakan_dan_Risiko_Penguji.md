# 17 — Uji Kelayakan dan Risiko Penguji

**Tanggal:** 18 November 2026
**Status:** Draf kerja (penilaian internal)
**Fungsi:** Menilai kelayakan sistem ALQI–SAW dari **sudut pandang penguji sidang**,
mendaftar kekurangan, dan menetapkan syarat perbaikan.
**Sifat:** Penilaian internal atas kesiapan naskah — **bukan** keputusan resmi penguji.
**Objek yang dinilai:** `01`–`16` (khususnya `05` formulasi, `07` kebaruan,
`08` rancangan eksperimen, `15` arsitektur sistem, `16` jaringan Multi-WAN).
**Konvensi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]**.

---

## 1. Cara Penilaian

Penguji pada dasarnya menguji lima hal:

| # | Pertanyaan inti | Yang diuji |
|---|---|---|
| Q1 | Apa **kebaruan**-nya dalam satu kalimat? | Orisinalitas |
| Q2 | Apa **celah**-nya nyata & terverifikasi? | Ketajaman masalah |
| Q3 | Apakah **metode** mampu menjawab pertanyaan? | Kekuatan metodologis |
| Q4 | Apakah **hasilnya dapat dipercaya**? | Validitas & statistik |
| Q5 | Apa **batas klaim**-nya? | Kejujuran ilmiah |

---

## 2. Ringkasan Sistem yang Dinilai

**[FAKTA]** Sistem = **indeks kualitas link berbasis SAW** $Q_i(t)$
(EWMA → normalisasi berbatas acuan tetap → bobot hibrida $\gamma$) + **gerbang
histeresis** + ditargetkan pada **tri-link** (`ether3-ISP-C` FO + `ether1-ISP-A`
dan `ether2-ISP-B` Starlink), memakai kolektor `collector.py` yang sudah ada,
dengan **rasio PCC** sebagai aktuator.

---

## 3. Skor Kelayakan

| Aspek | Bobot | Skor | Catatan |
|---|---:|---:|---|
| Kejelasan masalah | 10% | 88 | Nyata & terukur |
| **Kebaruan** | 20% | **60** | Tipis, positioning terbelah, prior art |
| Metode (SAW/bobot/normalisasi) | 15% | 68 | Adaptivitas & batas acuan belum terbukti |
| Data & validitas | 15% | 62 | Baseline 2,2 jam; korelasi; ground truth |
| Desain & statistik | 15% | 70 | Kerangka ada, power/primary belum |
| Kelayakan teknis | 10% | 85 | Kolektor & perangkat tersedia |
| Arsitektur & implementasi | 5% | 78 | Kuantisasi bucket, semantik failover |
| Klaim, etika, legal | 10% | 62 | Overclaim + ToS + izin |
| **Agregat** | **100%** | **± 70** | |

**Ambang internal:** ≥85 layak (revisi minor) · 75–84 layak (perbaikan terarah) ·
**65–74 perlu revisi mayor** · <65 belum layak.

**[ANALISIS]** Skor turun dari **±74** (penilaian awal, `00_README` §3) menjadi
**±70** setelah diuji dengan kacamata penguji.

---

## 4. Kekurangan

### A. Kebaruan (paling rawan) 🔴

| Kode | Kekurangan | Mengapa diserang | Dasar |
|---|---|---|---|
| **A-1** | **Kebaruan menyusut** menjadi "studi komparatif normalisasi × pembobotan" | *"Studi komparatif bukan kontribusi algoritmik."* | `07`; entropy-SAW sudah ada (2021) |
| **A-2** | **Arah mundur**: novelty terkuat (*stock-flow* + preservasi sesi) dilepas | *"Mengapa meninggalkan yang paling kuat?"* | `00_README` ↔ `07` |
| **A-3** | **Positioning terbelah**: dokumen bilang novelty = skoring, tetapi tri-link + state S4 + ELS = novelty alokasi | *"Kontribusinya skoring atau alokasi?"* | `00_README` §6 ↔ `08` §8 |

### B. Metode

| Kode | Kekurangan | Mengapa diserang |
|---|---|---|
| **B-1** | **"Adaptif" belum terbukti adaptif** — $\gamma$ adalah hyperparameter tetap, bukan mekanisme belajar | *"Apa bedanya dengan EWMA biasa?"* |
| **B-2** | **Batas normalisasi dipinjam dari TIPHON/Y.1541** (untuk layanan tutur/IP), bukan throughput Starlink yang dinamis | *"Batas acuan Anda arbitrer."* |
| **B-3** | **Parameter belum bersumber** ($\theta$ 60/80; $k$ 20/60; $W$=5 mnt; $N$=20 = "nilai awal") | *"Dari mana angka-angka ini?"* |
| **B-4** | **Prior art ALQI** (US 9,674,720 B2), termasuk "modified ALQI dengan ambang kejadian" | *"Menyerupai prior art."* |
| **B-5** | **Sirkularitas**: throughput sebagai **kriteria $Q$** dan sebagai **ground truth** | *"Indeks dinilai dengan metrik yang Anda masukkan ke dalamnya."* |

### C. Data & Validitas

| Kode | Kekurangan | Mengapa diserang |
|---|---|---|
| **C-1** | **Baseline 2,2 jam** (13 Nov 2026); protokol arsip minta **7–14 hari** | *"Tidak cukup untuk korelasi/periodisitas/distribusi."* |
| **C-2** | 🔴 **Dua Starlink berkorelasi 0,68–0,70** (ambang arsip <0,7); ko-lokasi → rain fade & kontelasi sama | *"3 ISP, tetapi hanya ~2 sumber independen."* |
| **C-3** | **Ground truth lemah** (goodput hanya proksi) | *"Bagaimana membuktikan $Q_i(t)$ benar?"* |
| **C-4** | **Resolusi temporal**: probe 2 s vs $T_s$ 1 s; transien 15 s bisa **ter-alias** | *"Indeks mengukur artefak sampling?"* |

### D. Desain & Statistik

| Kode | Kekurangan | Mengapa diserang |
|---|---|---|
| **D-1** | **Belum ada power analysis / SESOI**; episode degradasi langka | *"Berapa episode & bagaimana jika tidak signifikan?"* |
| **D-2** | **Banyak kombinasi** (3 normalisasi × 6 bobot) → risiko **p-hacking** | *"Berapa hipotesis primer?"* |
| **D-3** | **Kuantisasi bucket** (N=20 → langkah 5%) | *"Apakah selisih 5% berarti?"* |
| **D-4** | **Failover PCC tak menyelamatkan sesi lama** | *"Klaim 'tanpa mengorbankan stabilitas' terbukti di mana?"* |

### E. Etika, Legal, Kelayakan

| Kode | Kekurangan | Mengapa diserang |
|---|---|---|
| **E-1** | **Dua Starlink residensial** untuk jaringan komersial → isu **ToS** + biaya ganda | Etika **dan** relevansi RT/RW Net |
| **E-2** | Data pelanggan, izin, anonimisasi belum ada bukti dokumen | Syarat kelayakan operasional |
| **E-3** | **Lingkup belum dikunci** (Varian A/B/C masih terbuka) | *"Apa lingkup final Anda?"* |

---

## 5. Dua Belas Pertanyaan Penguji & Kesiapan

| # | Pertanyaan | Kesiapan | Yang harus disiapkan |
|---|---|---|---|
| 1 | Apa kebaruan dalam 1 kalimat? | ⚠️ lemah | Satu kalimat + pembanding (B1) |
| 2 | Mengapa 2 Starlink tidak redundan? | ❌ | Uji independensi ≥7 hari (B3) |
| 3 | Apa ground truth kualitas link? | ❌ | Definisi + sumber label (B2) |
| 4 | Mengapa batas TIPHON cocok untuk Starlink? | ⚠️ | Justifikasi/alternatif (B5) |
| 5 | Bukti bobot adaptif > bobot statis? | ❌ | Uji ablasi pembobotan (P1) |
| 6 | Berapa episode & power? | ❌ | Power/sample size (B4) |
| 7 | Bagaimana cegah p-hacking? | ⚠️ | Primary outcome + Holm (ada) |
| 8 | Dampak kuantisasi 5%? | ⚠️ | Uji sensitivitas $N$ (P3) |
| 9 | Klaim "stabil" dibuktikan bagaimana? | ⚠️ | Metrik RST/retensi (P4) |
| 10 | Kepatuhan ToS dua Starlink? | ❌ | Izin/tinjauan ToS (P5) |
| 11 | Mengapa mundur dari *stock-flow*? | ❌ | Narasi konsisten (B1) |
| 12 | Apa batas klaim? | ✅ | `07` §3 |

---

## 6. Putusan

> ### **LAYAK BERSYARAT — GO dengan revisi mayor terarah.**
> Sistem layak sebagai tesis S2 **hanya jika** enam syarat *blocking* (B1–B6)
> ditutup. Tanpa itu, penguji berhak menilai **inkremental** dan menahan.

---

## 7. Syarat Blocking (wajib sebelum seminar)

| # | Syarat | Menutup | Bukti yang dihasilkan |
|---|---|---|---|
| **B1** | **Kunci lingkup + satu kalimat kebaruan** (Varian B murni skoring, atau C skoring+stok) | A-2, A-3, E-3 | Halaman "lingkup & kebaruan" 1 paragraf |
| **B2** | **Tetapkan ground truth** & metrik validasi indeks; hindari sirkularitas | B-5, C-3 | Definisi + prosedur pelabelan |
| **B3** | **Baseline ≥7 hari + uji independensi A–B** → putuskan tri-link atau fallback dual | C-1, C-2 | Laporan korelasi + keputusan topologi |
| **B4** | **Primary outcome + SESOI + power/sample size** | D-1, D-2 | Bagian rencana statistik |
| **B5** | **Justifikasi parameter** ($\theta$, $k$, $N$, batas normalisasi) | B-2, B-3 | Tabel parameter + sumber tiap nilai |
| **B6** | **Tangani prior art ALQI + hapus overclaim** | B-4 | Sitasi US 9,674,720 B2; hapus "bebas osilasi"/"upper bound" |

---

## 8. Perbaikan Penting (non-blocking)

| # | Perbaikan | Menutup |
|---|---|---|
| **P1** | Uji ablasi **bobot statis vs adaptif** | B-1 |
| **P2** | Kebijakan **resampling 2 s → 1 s** + analisis aliasing 15 s | C-4 |
| **P3** | Uji sensitivitas **jumlah bucket $N$** | D-3 |
| **P4** | Tunjukkan **fail-static/rollback** berjalan | D-4 |
| **P5** | Siapkan **izin + tinjauan ToS** dua Starlink | E-1, E-2 |

---

## 9. Tiga Risiko Terbesar

1. 🔴 **Kebaruan tipis + positioning terbelah** (A-1, A-2, A-3) → kesan "aplikasi SAW".
2. 🔴 **Korelasi dua Starlink 0,68–0,70** (C-2) → klaim "3 ISP" tanpa informasi independen.
3. 🔴 **Ground truth lemah + baseline 2,2 jam** (C-3, C-1) → hasil dianggap tidak dapat dipercaya.

---

## 10. Rekomendasi Arah

| Opsi | Isi | Kekuatan | Risiko |
|---|---|---|---|
| **Varian C (rekomendasi)** | Skoring adaptif **+** kontribusi stok/sesi sebagai bukti penerapan | Menutup A-2/A-3; kebaruan kembali kuat | Cakupan & waktu lebih besar |
| Varian B | Murni skoring (komparatif) | Waktu terjamin | Kebaruan paling tipis (A-1 tetap) |

**[ANALISIS]** **Varian C lebih layak di mata penguji** karena memulihkan kebaruan
yang diakui (*stock-flow*/sesi) tanpa kembali ke cakupan SPA-HSM penuh — **asalkan**
ground truth (B2) dan uji independensi (B3) ditutup lebih dulu.

---

## 11. Checklist Tindakan

**Blocking (sebelum seminar)**
- [ ] B1 — Kunci Varian & tulis 1 kalimat kebaruan
- [ ] B2 — Definisikan ground truth & prosedur validasi indeks
- [ ] B3 — Baseline ≥7 hari + uji independensi A–B → keputusan topologi
- [ ] B4 — Primary outcome + SESOI + power
- [ ] B5 — Justifikasi seluruh parameter (tabel sumber nilai)
- [ ] B6 — Tangani prior art ALQI + hapus overclaim

**Penting**
- [ ] P1 — Ablasi pembobotan
- [ ] P2 — Kebijakan resampling & analisis aliasing
- [ ] P3 — Sensitivitas $N$
- [ ] P4 — Demo fail-static/rollback
- [ ] P5 — Izin & ToS

---

## 12. Riwayat Penilaian

| Tanggal | Skor | Catatan |
|---|---:|---|
| (awal) | ± 74 | Penilaian kelayakan pertama (`00_README` §3) |
| **18-11-2026** | **± 70** | Uji ulang dari sudut pandang penguji (dokumen ini) |

**Aturan [USULAN]:** dokumen ini diperbarui setiap kali syarat blocking ditutup;
putusan berubah menjadi **LAYAK** bila seluruh B1–B6 selesai dan skor agregat ≥ 75.
