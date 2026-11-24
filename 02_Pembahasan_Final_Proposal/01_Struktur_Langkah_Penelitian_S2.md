# 01 — Struktur Langkah Penelitian (Kelayakan Gap & Novelty S2)

**Status:** Draf kerja — acuan utama penyusunan proposal final.
**Fungsi:** Menjelaskan **struktur langkah penelitian** yang harus diambil agar
gap penelitian dan novelty memiliki **kelayakan strata S2 (tesis)** — dengan
tolok ukur eksplisit dan gerbang keputusan.
**Basis:** `17_Uji_Kelayakan_dan_Risiko_Penguji.md` (B1–B6, P1–P5),
`18_B1_Lingkup_dan_Pernyataan_Kebaruan.md` (Varian C, K-A…K-E),
`19_Analisis_Pra_Penelitian.md` (temuan aktual), `02_Research_Gap.md`,
`07_Kebaruan_dan_Kontribusi.md`, `14_Tahapan_Penelitian.md`.
**Konvensi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]**.

---

## 1. Tesis S2: Standar Kelayakan

**[ANALISIS]** "Layak S2" dalam konteks ini didefinisikan sebagai kemampuan
menjawab lima pertanyaan inti penguji (`17` §1) dengan bukti:

| # | Pertanyaan penguji | Bukti yang harus ada |
|---|---|---|
| Q1 | Apa kebaruan dalam satu kalimat? | Pernyataan kebaruan tunggal (B1) |
| Q2 | Apa celahnya nyata & terverifikasi? | Log pencarian + gap berbasis bukti (V-1…V-8) |
| Q3 | Apakah metode menjawab pertanyaan? | RQ ↔ hipotesis ↔ metode ↔ metrik konsisten |
| Q4 | Apakah hasilnya dapat dipercaya? | Baseline cukup, ground truth non-sirkular, statistik berpower (B2–B4) |
| Q5 | Apa batas klaim? | Daftar "tidak diklaim" + sitasi prior art (B6) |

**Rantai kelayakan (dirangkai berurutan):**

```
GAP (berbasis bukti) → KLAIM (terukur & tidak overclaim) → BUKTI (data + eksperimen)
→ SYARAT BLOCKING (B1–B6) → GERBANG (G0–G3) → NASKAH FINAL
```

Jika satu mata rantai putus, kelayakan turun. Titik putus paling umum di tesis
S2: **klaim tanpa bukti** dan **gap tanpa verifikasi**.

---

## 2. Peta Gap → Klaim → Bukti (master)

| Gap | Klaim (kontribusi) | Bukti yang diperlukan | Syarat | Tahap |
|---|---|---|---|---|
| G-N1: perbandingan normalisasi pada deret metrik real-time tri-link belum ada | K-A (studi komparatif terkontrol) + K-C (normalisasi berbatas acuan tetap) | V-1/V-4 (pencarian lintas basis data); V-3 (teks penuh entropy-SAW 2021); dataset tri-link nyata | B2, B3 | T1 → T3 → T6 |
| G-N2: bobot adaptif vs statis belum diuji atributif | K-B (pembobotan hibrida γ) + K-D (dekomposisi) | V-4/V-5; uji ablasi (P1) | B4, B5 | T1 → T6 → T9 |
| G-W1: stabilitas temporal / rank reversal belum diukur pada SAW | K-B/K-D (stabilitas) | V-5; metrik rank reversal, chattering | B4 | T1 → T6 |
| G-W2: dekomposisi kontribusi normalisasi vs bobot | K-D | Ablasi normalisasi × pembobotan | B4 | T6 |
| G-M3/G-E1: dampak alokasi/sesi belum diukur | K-E (bukti penerapan: ELS, flapping, RST) | Instrumentasi stok S_i & F_i; snapshot 17 Nov; L2 staging | B2, P4 | T3 → T7 |

**Kunci [ANALISIS]:** K-A…K-D adalah **klaim utama** (metode + empiris);
K-E adalah **penguat** (penerapan) — menutup A-2/A-3 tanpa melebar ke kontroler
penuh.

---

## 3. Struktur Langkah Penelitian (T0–T10)

Setiap tahap: **masukan → aktivitas → luaran → kriteria lulus → menutup syarat**.
Kriteria lulus ditulis **terukur** agar gerbang objektif.

### T0 — Kunci Keputusan (D-1…D-7, D-21)
- **Masukan:** `18` (B1), `19` (pra-penelitian), `09`.
- **Aktivitas:** kunci D-1…D-6; **D-7 ditunda** sampai uji independensi (T3);
  tegaskan Varian C; pilih judul (`18` §10).
- **Luaran:** tabel keputusan terkunci + tanggal + alasan.
- **Kriteria lulus:** semua D bernilai; D-7 berlabel "tertunda ↔ B3".
- **Menutup:** B1 (final), E-3.

### T1 — Studi Literatur & Verifikasi Prior Art
- **Aktivitas:** V-1…V-8; PA-1…PA-3; snowballing 10 paper inti.
- **Luaran:** register referensi final + log pencarian (tanggal, string, hit) +
  draf "posisi penelitian".
- **Kriteria lulus:** ≥15 SOTA inti terverifikasi; prior art ALQI disitasi &
  dibedakan (B6); semua klaim "belum ada" memakai frasa "berdasarkan pencarian pada…".
- **Menutup:** B6; gerbang G0.

### T2 — Spesifikasi Parameter & Instrumen
- **Aktivitas:** finalisasi P1–P12 + satuan + rentang acuan; **tabel sumber tiap
  nilai** (B5); definisi operasional flapping/ELS/time-to-rebalance/RST;
  prosedur sampling & sinkronisasi; anonimisasi.
- **Luaran:** dokumen spesifikasi parameter & instrumen.
- **Kriteria lulus:** tiap variabel punya definisi+satuan+instrumen+prosedur;
  **setiap angka (θ, k, W, N, batas normalisasi) punya sumber/justifikasi**.
- **Menutup:** B5.

### T3 — Akuisisi & Konsolidasi Data (L0)
- **Aktivitas:**
  - Perpanjang **baseline kontinu ≥7 hari** (jam sibuk 19.00–23.00, jam rendah
    01.00–05.00, minimal satu hujan) — catatan: sesi 17–18 Nov sudah ±19,9 jam
    kontinu, tetapi berhenti 18 Nov 06:11 UTC dan ada celah ke 12 Nov.
  - **Pengukuran throughput 1 detik** pada 3 WAN (untuk B3 & analisis aliasing).
  - **Uji independensi A–B per segmen kontinu** (residual RTT + throughput +
    Jaccard + episode match) → putuskan **D-7**. Jangan menginterpolasi lintas
    celah (lihat `19` 4.4A).
  - Instrumentasi stok koneksi S_i (30 s per connection mark) & laju F_i.
  - Pelabelan episode + ground truth goodput (B2) — prosedur formal + antarmuka
    label (episode FO kini teramati: 18–20 episode, median 7–10 s).
  - Data sintetis: transien 15 detik & degradasi bertahap (untuk L1/L2).
- **Luaran:** dataset bersih + label + dokumentasi versi + laporan korelasi.
- **Kriteria lulus:** sanity check lolos; label konsisten; data teranonim;
  laporan korelasi A–B per segmen selesai.
- **Menutup:** B2 (parsial), B3, C-1, C-2, C-4, T-1…T-6.

### T4 — Formalisasi & Perancangan
- **Aktivitas:** rumus final (normalisasi N-c, bobot γ, gerbang histeresis);
  state machine 3-link 8-state; bucket mapping N=20 (b_min/b_max); kontrak
  antarmuka; skema basis data.
- **Luaran:** spesifikasi teknis + diagram.
- **Kriteria lulus:** tanpa ambiguitas letak komponen; semua rumus berdefinisi +
  rentang.
- **Menutup:** temuan M14.

### T5 — Implementasi Prototipe (Scoring Engine)
- **Aktivitas:** modul EWMA/normalisasi/bobot/gerbang; unit test; determinisme;
  instrumentasi log.
- **Kriteria lulus:** unit test lulus; skoring ≤1 s/siklus; deterministik;
  golden test (FO 91,3 / LEO 53,3 pada bobot lama).
- **Menutup:** gerbang G1.

### T6 — Eksperimen L1 (Offline/Replay)
- **Aktivitas:**
  - Seluruh kombinasi (N-a/N-b/N-c) × (statis/sama-rata/entropy/CRITIC/MEREC/
    hibrida).
  - Metrik: Spearman ρ, rank reversal, chattering, AUC.
  - **Ablasi pembobotan (P1)**; **sensitivitas N (P3)**; **resampling 2 s→1 s
    & analisis aliasing (P2)**; sensitivitas γ, α, N.
- **Luaran:** tabel & grafik hasil (siap Bab hasil).
- **Kriteria lulus:** kesenjangan antar-metode terlihat; satu konfigurasi terbaik
  teridentifikasi (akurasi × stabilitas); dapat direproduksi.
- **Menutup:** B-1, D-3, C-4.

### T7 — Eksperimen L2 (Staging Terkendali)
- **Aktivitas:** perlakuan A/B/D/F/G/H × kondisi N/T/S/R/K; injeksi tc/netem;
  ulangan 30–64× counterbalanced; ukur flapping, recovery latency, ELS,
  time-to-rebalance, RST flow; **demo fail-static/rollback (P4)**.
- **Kriteria lulus:** efek gerbang (B vs D vs F) terukur & signifikan arah;
  tanpa artefak; protokol dapat diulang.
- **Menutup:** D-4; gerbang G2.

### T8 — Eksperimen L3 (Lapangan, Opsional)
- **Aktivitas:** izin pemilik + pemberitahuan pelanggan + **tinjauan ToS dua
  Starlink (P5)**; mode pantau pasif → aktivasi bertahap; fail-static/watchdog/
  rollback.
- **Kriteria lulus:** izin & kepatuhan lengkap; tanpa gangguan pelanggan;
  rollback terbukti.
- **Menutup:** E-1/E-2. *(Klaim tetap sah tanpa L3.)*

### T9 — Analisis Statistik & Pembuktian
- **Aktivitas:** satuan analisis episode/jam; mixed-effects/GEE; Poisson/negative
  binomial untuk flapping; ANOVA/Kruskal–Wallis + post hoc; **effect size + 95%
  CI; Holm; bootstrap**; dekomposisi (H3); **pra-registrasi rencana analisis
  (B4)** sebelum T6.
- **Kriteria lulus:** primary outcome terjawab dengan effect size & CI;
  kontribusi komponen dapat diatribusikan (ablasi); sensitivitas dilaporkan
  sebagai eksplorasi.
- **Menutup:** B4, D-1, D-2; gerbang G3.

### T10 — Penulisan Naskah & Seminar
- **Aktivitas:** Bab I (dari `09` + `18`), Bab II (dari `06` + T1), Bab III
  (dari `08` + T2–T5); checklist `13` §10; deck + latihan tanya-jawab.
- **Kriteria lulus:** konsistensi RQ↔hipotesis↔metode↔luaran; sitasi konsisten;
  batas klaim eksplisit; **skor uji penguji ≥75**.
- **Menutup:** seluruh syarat untuk seminar.

---

## 4. Gerbang & Logika "Apakah Sudah Layak?"

| Gate | Setelah | Pertanyaan kunci | Jika gagal |
|---|---|---|---|
| G0 | T1 | Gap & prior art tertangani? (B6) | Perluas pencarian; ganti sudut kebaruan |
| G1 | T5 | Prototipe berjalan & deterministik? | Perbaiki; turunkan cakupan fitur |
| G2 | T7 | Efek gerbang terukur di staging? | Perbaiki parameter; ulang ulangan |
| G3 | T9 | Primary outcome terjawab? | Turunkan klaim; laporkan non-inferioritas |
| **G-S2** | T10 | B1–B6 semua tertutup & skor ≥75? | Tunda seminar; tutup syarat tersisa |

**Aturan kunci [USULAN]:**
- **Tidak boleh ada klaim kebaruan di naskah final** sebelum G0 (B6) dan B3 lolos.
- **Tidak boleh mengklaim "lebih stabil/akurat"** sebelum B4 (power/SESOI)
  terdefinisi.
- **Keputusan topologi (D-7)** tidak boleh dikunci sebelum B3 (uji independensi
  A–B) selesai.

---

## 5. Menutup Syarat Blocking (B1–B6) — Cara & Bukti

| Syarat | Cara menutup | Bukti | Kapan |
|---|---|---|---|
| **B1** | Kunci Varian C + satu kalimat kebaruan + persetujuan pembimbing | `18`; paragraf novelty di Bab I | T0 |
| **B2** | Definisikan ground truth (goodput + label episode), prosedur pelabelan, hindari sirkularitas (throughput tidak boleh menjadi kriteria Q sekaligus GT) | Dokumen definisi operasional; protokol pelabelan | T2/T3 |
| **B3** | Baseline ≥7 hari + uji independensi A–B (korelasi residual RTT & throughput; ambang <0,7) → keputusan D-7 | Laporan korelasi; keputusan topologi | T3 |
| **B4** | Primary outcome tunggal + SESOI + power/sample size + pra-registrasi rencana analisis | `05_Registrasi_Rencana_Analisis.md` | T2/T9 |
| **B5** | Tabel parameter: tiap nilai (θ, k, W, N, batas normalisasi) bersumber (TIPHON/Y.1541/G.114, kalibrasi data, literatur) | Tabel parameter di Bab III | T2 |
| **B6** | Sitasi US 9,674,720 B2 + entropy-SAW (2021); hapus overclaim ("bebas osilasi", "upper bound"); daftar "tidak diklaim" | Bab II + `18` §8 | T1/T10 |

**Catatan [FAKTA]:** data 2,2 jam & snapshot 17 Nov **belum** memenuhi B3
(butuh ≥7 hari) — lihat `19` §7.4.

---

## 6. Perbaikan Penting (P1–P5) — Langkah yang Melekat

| Kode | Perbaikan | Melekat pada | Menutup temuan |
|---|---|---|---|
| P1 | Ablasi bobot statis vs adaptif | T6 | B-1 |
| P2 | Resampling 2 s→1 s + analisis aliasing 15 s | T3/T6 | C-4 |
| P3 | Sensitivitas jumlah bucket N | T6 | D-3 |
| P4 | Demo fail-static/rollback | T7 | D-4 |
| P5 | Izin + tinjauan ToS dua Starlink | T8 | E-1, E-2 |

---

## 7. Barometer Kelayakan S2 (ringkas)

| Kriteria | Ambang | Status saat ini |
|---|---|---|
| Kebaruan | Bukan sekadar aplikasi SAW; ada elemen metodologis/empiris baru | ⏳ B1 siap; menunggu persetujuan |
| Gap terverifikasi | Log pencarian untuk semua klaim "belum ada" | ❌ V-1…V-8 belum jalan |
| Metode → RQ | Konsistensi penuh Bab I–III | ❌ Naskah belum ditulis |
| Bukti dapat dipercaya | Baseline ≥7 hari; GT non-sirkular; power | ⏳ B2/B3 sebagian: sesi 17–18 Nov (±19,9 jam) + throughput 10 s siap; baseline 7 hari & power belum |
| Kejujuran klaim | Batas eksplisit; sitasi prior art | ⏳ B6 sebagian |
| Skor agregat | ≥75 | ⚠️ ±73 (setelah B1) |
| Syarat blocking | B1–B6 semua tertutup | ❌ B2–B6 terbuka |

---

## 8. Checklist Progres (inti)

**Blocking:**
- [x] B1 — Usulan Varian C + kalimat kebaruan (`18`)
- [ ] B1 — Persetujuan pembimbing
- [ ] B2 — Ground truth + prosedur validasi indeks (sesi 17–18 Nov siap sebagai bahan)
- [ ] B3 — Baseline kontinu ≥7 hari + uji independensi per segmen (sementara: 0,384–0,393 pada 17–18 Nov; 0,683–0,704 pada 12 Nov) → D-7
- [ ] B4 — Primary outcome + SESOI + power (pra-registrasi)
- [ ] B5 — Tabel justifikasi parameter
- [ ] B6 — Sitasi US 9,674,720 B2 + hapus overclaim

**Penting:**
- [ ] P1 — Ablasi pembobotan (T6)
- [ ] P2 — Resampling & aliasing (T3/T6)
- [ ] P3 — Sensitivitas N (T6)
- [ ] P4 — Fail-static/rollback (T7)
- [ ] P5 — Izin & ToS (T8)

**Naskah:**
- [ ] Bab I — `02_Draf_Bab_I.md`
- [ ] Bab II — `03_Draf_Bab_II.md`
- [ ] Bab III — `04_Draf_Bab_III.md`
- [ ] Registrasi rencana analisis — `05_Registrasi_Rencana_Analisis.md`
- [ ] Uji penguji: skor ≥75

---

## 9. Urutan Kerja Minggu Ini (rekomendasi)

1. **B1 final** — minta persetujuan pembimbing atas Varian C & judul (`18`).
2. **T-6 diperluas (T3 awal)** — ukur **throughput 1 detik** 3 WAN
   (10–15 menit) → hitung ulang korelasi A–B → putuskan **D-7**.
3. **T1 (lanjut)** — V-1…V-3 + PA-1…PA-3 → tulis posisi penelitian.
4. **B4** — tetapkan primary outcome + SESOI + power sebelum eksperimen.
5. **B5** — susun tabel parameter + sumber nilai (kalibrasi dari `19` §7.3).
6. **T3 penuh** — baseline 7 hari (paralel dengan T1/T2).
7. Setelah B2–B6 jalan, mulai draf Bab I–III (T10 awal).

---

## 10. Lanjutan yang Disarankan

- Buat `02_Draf_Bab_I.md` (pendahuluan + RQ + kebaruan + batasan) setelah B1
  disetujui.
- Buat `05_Registrasi_Rencana_Analisis.md` setelah B4 ditetapkan.
- Perbarui `17` setiap syarat blocking tertutup (skor & putusan).
