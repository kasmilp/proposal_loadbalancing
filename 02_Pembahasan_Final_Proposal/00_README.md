# 02 — Pembahasan Final Proposal (S2)

**Status:** Folder baru — konsolidasi menuju naskah proposal final.
**Fungsi:** Menampung satu sumber kebenaran (*single source of truth*) untuk
penyusunan proposal tesis S2: peta gap → kontribusi → bukti → syarat kelayakan,
struktur langkah penelitian, gerbang keputusan, dan draf naskah (Bab I–III).
**Basis:** Seluruh dokumen aktif `01_Pembahasan_ALQI_SAW/` (01–19) dan arsip
`01_Arsip_SPA-HSM_Tahap_01-12/`.

---

## 1. Isi Folder

| Berkas | Isi | Status |
|---|---|---|
| `00_README.md` | Indeks, ringkasan eksekutif, status blocking | Aktif |
| `01_Struktur_Langkah_Penelitian_S2.md` | **Struktur langkah penelitian** agar gap/novelty layak S2: rantai kelayakan, peta gap→klaim→bukti→syarat, tahapan + gerbang, barometer S2, checklist | Aktif |
| `02_Draf_Bab_I.md` | *(rencana)* Draf Bab I: pendahuluan, RQ, tujuan, kebaruan, batasan | Belum |
| `03_Draf_Bab_II.md` | *(rencana)* Tinjauan pustaka + posisi penelitian | Belum |
| `04_Draf_Bab_III.md` | *(rencana)* Metodologi: desain, parameter, statistik, etika | Belum |
| `05_Registrasi_Rencana_Analisis.md` | *(rencana)* Pra-registrasi: primary outcome, SESOI, power, uji statistik | Belum |
| `06_Tahapan_Per_Folder.md` | **Peta eksekusi per folder**: tahap T0–T10 → folder → berkas → kriteria lulus, gelombang kerja, titik serah-terima | Aktif |
| `07_Kamus_Kode.md` | **Kamus kode lengkap**: arti + isi + status + rujukan untuk semua kode (T, G, B, P, K-A…K-E, G-, D-, V/PA/T, temuan `17`, audit `12`, perlakuan A–H, kondisi N/T/S/R/K, state S0–S7, parameter P1–P12, kode arsip) | Aktif |

**Aturan:** folder ini **hanya** menampung naskah final dan peta kerja. Bahan
analisis tetap di `01_Pembahasan_ALQI_SAW/`; dokumen di sini merujuk, tidak menyalin.

---

## 2. Ringkasan Eksekutif

**[ANALISIS]** Proposal berada pada status **LAYAK BERSYARAT** (skor ±70 → ±73
setelah B1). Agar gap/novelty **layak strata S2**, dibutuhkan rantai yang utuh:

```
GAP (G-N1/N2/W1/W2) → KLAIM (K-A…K-E) → BUKTI (V/PA/T) → SYARAT BLOCKING (B1–B6)
→ GERBANG (G0–G3) → NASKAH FINAL (Bab I–III)
```

Titik paling rawan menurut uji penguji (`17` §9):
1. 🔴 **Kebaruan tipis + positioning terbelah** → sudah ditutup sebagian oleh B1 (Varian C, K-E).
2. 🔴 **Korelasi dua Starlink 0,68–0,70** → **B3** tersisa; data terbaru (segmen 17–18 Nov) menunjukkan korelasi residual **0,384–0,393** (di bawah ambang), tetapi sesi 12 Nov masih 0,68–0,70 → **belum konklusif**.
3. 🔴 **Ground truth lemah + baseline 2,2 jam** → **B2/B3**: sekarang ada sesi 17–18 Nov (±19,9 jam, 174.352 probe) + throughput interface 10 s; prosedur formal pelabelan tetap perlu ditulis.

**Status syarat blocking hari ini:**

| Syarat | Isi | Status |
|---|---|---|
| B1 | Kunci lingkup + satu kalimat kebaruan | ✅ Usulan siap (`18`); ⏳ menunggu persetujuan pembimbing |
| B2 | Ground truth & prosedur validasi indeks (hindari sirkularitas) | ⏳ Sebagian: sesi 17–18 Nov (±19,9 jam) tersedia, episode FO kini teramati (18–20 episode), throughput interface 10 s tersedia sebagai GT non-sirkular (kriteria Q = probe RTT/jitter/loss). Prosedur pelabelan formal belum ditulis |
| B3 | Baseline ≥7 hari + uji independensi A–B → keputusan topologi | ⏳ Sebagian: uji per segmen kontinu selesai — residu A–B 0,384–0,393 (17–18 Nov, lolos <0,7) vs 0,683–0,704 (12 Nov, ambang). Baseline kontinu ≥7 hari belum |
| B4 | Primary outcome + SESOI + power/sample size | ❌ Belum |
| B5 | Justifikasi parameter (θ, k, N, batas normalisasi) | ❌ Belum |
| B6 | Tangani prior art ALQI + hapus overclaim | ⏳ Sebagian (`18` daftar "tidak diklaim"; sitasi US 9,674,720 B2 perlu di Bab II) |

---

## 3. Barometer Kelayakan S2

**[ANALISIS]** Definisi operasional "layak S2" yang dipakai folder ini:

| Kriteria | Ambang | Bukti |
|---|---|---|
| Kebaruan | ≠ sekadar aplikasi SAW; ada elemen **metodologis/empiris** baru | K-A…K-E; novel statement |
| Gap terverifikasi | Semua klaim "belum ada" dengan log pencarian | V-1…V-8, PA-1…PA-3 |
| Metode menjawab RQ | RQ ↔ hipotesis ↔ metode ↔ metrik konsisten | Bab I–III |
| Bukti empiris yang dapat dipercaya | Baseline cukup, ground truth non-sirkular, statistik berpower | B2, B3, B4 |
| Kejujuran klaim | Batas klaim eksplisit; tidak overclaim | B6 |
| Skor agregat | ≥ 75 (ambang internal uji penguji) | `17` |
| Semua syarat blocking | B1–B6 tertutup | Checklist §7 |

**Strata S2:** kontribusi minimal **satu** dari: (a) metode/teknik baru yang
terverifikasi secara empiris, (b) studi komparatif terkontrol yang menghasilkan
rekomendasi berbasis bukti, (c) penerapan yang menghasilkan temuan baru yang
dapat digeneralisasi dalam batas. Varian C memenuhi (a)+(b) dengan K-E sebagai
penguat penerapan.

---

## 4. Peta Gap → Klaim → Bukti → Syarat (tabel master)

| Gap | Klaim (kontribusi) | Bukti yang diperlukan | Syarat blocking | Tahap |
|---|---|---|---|---|
| G-N1 (normalisasi belum dibandingkan pada deret real-time tri-link) | K-A studi komparatif terkontrol; K-C normalisasi berbatas tetap | V-1/V-4 pencarian; V-3 teks penuh entropy-SAW (2021); dataset tri-link nyata | B2 (ground truth), B3 (baseline) | T1 → T3 → T6 |
| G-N2 (bobot adaptif vs statis belum diuji atributif) | K-B pembobotan hibrida γ + K-D dekomposisi | V-4/V-5; uji ablasi (P1) | B4 (power), B5 (parameter) | T1 → T6 → T9 |
| G-W1 (stabilitas temporal/rank reversal belum diukur pada SAW) | K-B/K-D (stabilitas) | V-5; metrik rank reversal, chattering | B4 | T1 → T6 |
| G-W2 (dekomposisi kontribusi) | K-D | Ablasi normalisasi × bobot | B4 | T6 |
| G-M3/G-E1 (dampak alokasi/sesi) | K-E bukti penerapan (ELS, flapping, RST) | Instrumentasi stok S_i & F_i; snapshot 17 Nov; L2 staging | B2, D-4 (P4) | T3 → T7 |

**Hubungan kunci:** B2+B3 mendukung G-N1; B4+B5 mendukung G-N2/G-W1/G-W2;
B6 melindungi seluruh klaim dari prior art (US 9,674,720 B2, entropy-SAW 2021).

---

## 5. Struktur Langkah Penelitian (T0–T10, versi final)

**Prinsip:** setiap tahap = masukan → aktivitas → luaran → **kriteria lulus**
(terukur) → terkait syarat blocking. Ini mengikuti `14_Tahapan_Penelitian.md`,
dirapikan dengan status B1–B6.

### T0 — Kunci Keputusan (D-1…D-7, D-21)
- **Masukan:** `18` (B1), `19` (pra-penelitian), `09`.
- **Aktivitas:** kunci D-1…D-6; **D-7 ditunda** sampai uji independensi (T3);
  tegaskan Varian C; pilih judul (`18` §10).
- **Luaran:** tabel keputusan terkunci + tanggal.
- **Kriteria lulus:** semua D bernilai; D-7 berlabel "tertunda ↔ B3".
- **Menutup:** B1 (final), E-3.

### T1 — Studi Literatur & Verifikasi Prior Art
- **Aktivitas:** V-1…V-8; PA-1…PA-3; snowballing 10 paper inti.
- **Luaran:** register referensi final + log pencarian + draf "posisi penelitian".
- **Kriteria lulus:** ≥15 SOTA inti terverifikasi; prior art ALQI disitasi &
  dibedakan (B6); semua klaim "belum ada" memakai frasa "berdasarkan pencarian pada…".
- **Menutup:** B6, G0.

### T2 — Spesifikasi Parameter & Instrumen
- **Aktivitas:** finalisasi P1–P12 + satuan + rentang acuan; **tabel sumber tiap
  nilai** (B5); definisi operasional flapping/ELS/time-to-rebalance/RST;
  prosedur sampling & sinkronisasi; anonimisasi.
- **Luaran:** dokumen spesifikasi parameter & instrumen.
- **Kriteria lulus:** tiap variabel punya definisi+satuan+instrumen+prosedur;
  **setiap angka (θ, k, W, N, batas normalisasi) punya sumber/justifikasi**.
- **Menutup:** B5.

### T3 — Akuisisi & Konsolidasi Data (L0)
- **Aktivitas:** perpanjang **baseline ≥7 hari** (jam sibuk 19.00–23.00, jam
  rendah 01.00–05.00, minimal satu hujan); **pengukuran throughput 1 detik**
  pada 3 WAN (untuk B3 & aliasing); **uji independensi A–B** pada metrik RTT +
  throughput; instrumentasi stok S_i & laju F_i; pelabelan episode + ground truth
  goodput (B2); data sintetis transien 15 s & degradasi bertahap.
- **Luaran:** dataset bersih + label + dokumentasi versi + laporan korelasi.
- **Kriteria lulus:** sanity check lolos; label konsisten; data teranonim;
  **laporan korelasi A–B selesai → putuskan D-7** (tri-link vs Opsi 3).
- **Menutup:** B2 (parsial), B3, C-1/C-2/C-4, T-1…T-6.

### T4 — Formalisasi & Perancangan
- **Aktivitas:** rumus final (normalisasi N-c, bobot γ, gerbang histeresis);
  state machine 3-link 8-state; bucket mapping N=20 (b_min/b_max); kontrak
  antarmuka; skema basis data.
- **Luaran:** spesifikasi teknis + diagram.
- **Kriteria lulus:** tanpa ambiguitas letak komponen; semua rumus berdefinisi
  + rentang.
- **Menutup:** M14.

### T5 — Implementasi Prototipe (Scoring Engine)
- **Aktivitas:** modul EWMA/normalisasi/bobot/gerbang; unit test; determinisme;
  instrumentasi log.
- **Kriteria lulus:** unit test lulus; skoring ≤1 s/siklus; deterministik;
  golden test (FO 91,3 / LEO 53,3).
- **Menutup:** G1.

### T6 — Eksperimen L1 (Offline/Replay)
- **Aktivitas:** seluruh kombinasi (N-a/N-b/N-c) × (statis/sama-rata/entropy/
  CRITIC/MEREC/hibrida); metrik Spearman ρ, rank reversal, chattering, AUC;
  **ablasi pembobotan (P1)**; **sensitivitas N (P3)**; **resampling 2 s→1 s &
  analisis aliasing (P2)**; sensitivitas γ, α, N.
- **Luaran:** tabel & grafik hasil (siap Bab hasil).
- **Kriteria lulus:** kesenjangan antar-metode terlihat; satu konfigurasi terbaik
  teridentifikasi (akurasi × stabilitas); dapat direproduksi.
- **Menutup:** B-1, D-3, C-4 (P2).

### T7 — Eksperimen L2 (Staging Terkendali)
- **Aktivitas:** perlakuan A/B/D/F/G/H × kondisi N/T/S/R/K; injeksi tc/netem;
  ulangan 30–64× counterbalanced; ukur flapping, recovery latency, ELS,
  time-to-rebalance, RST flow; **demo fail-static/rollback (P4)**.
- **Kriteria lulus:** efek gerbang (B vs D vs F) terukur & signifikan arah;
  tanpa artefak; protokol dapat diulang.
- **Menutup:** D-4 (P4), G2.

### T8 — Eksperimen L3 (Lapangan, Opsional)
- **Aktivitas:** izin pemilik + pemberitahuan pelanggan + **tinjauan ToS dua
  Starlink (P5)**; mode pantau pasif → aktivasi bertahap; fail-static/watchdog/
  rollback.
- **Kriteria lulus:** izin & kepatuhan lengkap; tanpa gangguan pelanggan;
  rollback terbukti.
- **Menutup:** E-1/E-2 (P5). *(Klaim tetap sah tanpa L3.)*

### T9 — Analisis Statistik & Pembuktian
- **Aktivitas:** satuan analisis episode/jam; mixed-effects/GEE; Poisson/negative
  binomial untuk flapping; ANOVA/Kruskal–Wallis + post hoc; **effect size + 95%
  CI; Holm; bootstrap**; dekomposisi (H3); **pra-registrasi rencana analisis
  (B4)** sebelum T6.
- **Kriteria lulus:** primary outcome terjawab dengan effect size & CI;
  kontribusi komponen dapat diatribusikan (ablasi); sensitivitas dilaporkan
  sebagai eksplorasi.
- **Menutup:** B4, D-1/D-2, G3.

### T10 — Penulisan Naskah & Seminar
- **Aktivitas:** Bab I (dari `09` + `18`), Bab II (dari `06` + T1), Bab III
  (dari `08` + T2–T5); checklist `13` §10; deck + latihan tanya-jawab.
- **Kriteria lulus:** konsistensi RQ↔hipotesis↔metode↔luaran; sitasi konsisten;
  batas klaim eksplisit; **skor uji penguji ≥75**.
- **Menutup:** seluruh syarat untuk seminar.

---

## 6. Gerbang & Logika "Apakah Sudah Layak?"

| Gate | Setelah | Pertanyaan kunci | Jika gagal |
|---|---|---|---|
| G0 | T1 | Gap & prior art tertangani? (B6) | Perluas pencarian; ganti sudut kebaruan |
| G1 | T5 | Prototipe berjalan & deterministik? | Perbaiki; turunkan cakupan fitur |
| G2 | T7 | Efek gerbang terukur di staging? | Perbaiki parameter; ulang ulangan |
| G3 | T9 | Primary outcome terjawab? | Turunkan klaim; laporkan non-inferioritas |
| **G-S2** | T10 | B1–B6 semua tertutup & skor ≥75? | Tunda seminar; tutup syarat tersisa |

**Aturan kunci [USULAN]:** **tidak boleh ada klaim kebaruan di naskah final**
sebelum G0 (B6) dan B3 lolos; **tidak boleh mengklaim "lebih stabil/akurat"**
sebelum B4 (power/SESOI) terdefinisi.

---

## 7. Checklist Progres (Final)

**Blocking:**
- [x] B1 — Usulan Varian C + satu kalimat kebaruan (`18`)
- [ ] B1 — **Persetujuan pembimbing** (Varian C & judul)
- [ ] B2 — Ground truth & prosedur validasi indeks
- [ ] B3 — Baseline ≥7 hari + uji independensi A–B → keputusan D-7
- [ ] B4 — Primary outcome + SESOI + power/sample size (pra-registrasi)
- [ ] B5 — Tabel justifikasi seluruh parameter
- [ ] B6 — Sitasi US 9,674,720 B2 di Bab II + hapus overclaim

**Penting:**
- [ ] P1 — Ablasi pembobotan statis vs adaptif (T6)
- [ ] P2 — Kebijakan resampling 2 s→1 s + analisis aliasing (T3/T6)
- [ ] P3 — Sensitivitas jumlah bucket N (T6)
- [ ] P4 — Demo fail-static/rollback (T7)
- [ ] P5 — Izin + tinjauan ToS (T8)

**Naskah:**
- [ ] Bab I (draf) — `02_Draf_Bab_I.md`
- [ ] Bab II (draf) — `03_Draf_Bab_II.md`
- [ ] Bab III (draf) — `04_Draf_Bab_III.md`
- [ ] Registrasi rencana analisis — `05_Registrasi_Rencana_Analisis.md`
- [ ] Uji penguji: skor ≥75

---

## 8. Urutan Kerja Disarankan (minggu ini)

1. **B1 final** — minta persetujuan pembimbing atas Varian C & judul (dari `18`).
2. **T-6 diperluas (T3 awal)** — jalankan pengukuran **throughput 1 detik**
   pada 3 WAN (10–15 menit) → hitung ulang korelasi A–B → putuskan **D-7**.
3. **T1 (lanjut)** — V-1…V-3 + PA-1…PA-3 (prior art & entropy-SAW) → tulis
   posisi penelitian.
4. **B4** — tetapkan primary outcome + SESOI + power (sebelum eksperimen).
5. **B5** — susun tabel parameter + sumber nilai (kalibrasi dari `19` §7.3).
6. **T3 penuh** — baseline 7 hari (bisa berjalan paralel dengan T1/T2).
7. Setelah B2–B6 jalan, mulai draf Bab I–III (T10 awal).
