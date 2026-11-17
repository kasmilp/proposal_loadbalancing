# 13 — Perbaikan atas `Proposal pcc- print.pdf`

**Status:** Draf kerja (usulan perbaikan)
**Fungsi:** Memberikan perbaikan konkret atas temuan di `12_Pengamatan_Proposal_Lama.md`,
agar naskah lama dapat dipakai kembali sebagai basis yang bersih.

**Prinsip [USULAN]:** perbaiki **tanpa mengubah rancangan inti** — cukup konsistensi
logika, ketepatan rumus, kejelasan klaim, dan kerapian penulisan.

---

## 1. Perbaikan Editorial (E1–E12)

| Kode | Sebelum | Sesudah |
|---|---|---|
| E1 | "Tabel 5. Bobot Ilustratif throughput" (isinya data metrik) | "Tabel 5. Data ilustratif metrik QoS per jalur" |
| E2 | Badan: "Tabel 4"/"Tabel 5" untuk perangkat | "Tabel 2. Spesifikasi Perangkat Keras" / "Tabel 3. Spesifikasi Perangkat Lunak" |
| E3 | $s_i = w_D r_D + w_J r_J + r_{PL} + w_T r_T$ | $s_i = w_D r_{D,i} + w_J r_{J,i} + \mathbf{w_{PL}}\, r_{PL,i} + w_T r_{T,i}$ |
| E4 | $W_T = 020$ | $w_T = 0{,}20$ |
| E5 | Gambar 4 & 5 sama-sama "Diagram Integrasi ALQI" | Gambar 4 = "Posisi histeresis dalam alur keputusan"; Gambar 5 = "Diagram integrasi $Q_i(t)$" |
| E6 | Gambar 10 bertajuk arsitektur padahal di subbab histeresis | Gambar 10 = "Diagram keadaan (state machine) histeresis" |
| E7 | Lampiran "Tabel 12" | "Tabel 10" (lanjutkan penomoran) |
| E8 | `�550 km` | "≈550 km" |
| E9 | "di ataranya" | "di antaranya" |
| E10 | Placeholder `[isi …]` | Isi nilai sebenarnya (mis. paket IndiHome, SQLite) |
| E11 | Tabel 7 "Skenario Percobaan" (isinya variabel) | "Tabel 7. Variabel penelitian" |
| E12 | Jadwal "3 bulan" untuk seluruh NDLC | Jadwal 6 bulan, atau nyatakan 3 bulan hanya untuk pengujian |

---

## 2. Perbaikan Rumus **[USULAN]**

### 2.1 Normalisasi (tetap, dengan catatan)
Cost (delay, jitter, loss): $r_{ij} = \dfrac{\min_k(x_{kj})}{x_{ij}}$ ·
Benefit (throughput): $r_{ij} = \dfrac{x_{ij}}{\max_k(x_{kj})}$

**Catatan [ANALISIS]:** bentuk $\min/\max$ yang bergeser tiap siklus membuat skor
tidak komparabel antar-waktu. Alternatif: normalisasi berbatas acuan tetap (TIPHON/
Y.1541). Lihat `04_Analisis_Bobot_SAW.md`.

### 2.2 Skor SAW (diperbaiki)
$$s_i = \sum_{j \in \{D,J,PL,T\}} w_j\, r_{ij}, \qquad \sum_j w_j = 1$$

### 2.3 Rasio PCC — beri batas
Sebelum: $R_{FO} = \dfrac{Q_{FO}}{Q_{FO}+Q_{LEO}} \times 100\%$ (tanpa batas)

Sesudah:
$$R_{FO} = \mathrm{clip}\!\left(\frac{Q_{FO}}{Q_{FO}+Q_{LEO}} \times 100\%,\; R_{\min},\; R_{\max}\right),\quad
R_{\min}=15\%,\; R_{\max}=85\%$$

**[ANALISIS]** Rasio juga sebaiknya mempertimbangkan **kapasitas/kontrak** tiap jalur,
bukan hanya skor kualitas — jika tidak, link dengan kualitas tinggi tetapi kapasitas
kecil bisa kelebihan beban.

---

## 3. Perbaikan Inkonsistensi Histeresis (M14) 🔴

**Masalah:** naskah menyatakan histeresis di tiga tempat yang berbeda.

**Keputusan [USULAN]: tetapkan satu alur, lalu selaraskan ketiga tempat.**

**Alur yang dipilih:**

```
metrik mentah → EWMA (penghalusan) → normalisasi (batas tetap) → SAW → Q_i(t)
      → gerbang histeresis (pada Q_i(t)) → keputusan rasio
```

**Perbaikan redaksi:**

| Lokasi | Sebelum (ringkas) | Sesudah (ringkas) |
|---|---|---|
| 1.2.10 | "histeresis diterapkan pada deret **metrik mentah**, bukan pada skor ALQI" | "histeresis asimetris bekerja pada **deret skor $Q_i(t)$** setelah penghalusan EWMA, sebelum keputusan rasio" |
| 2.5.4 | histeresis pada $ALQI_i(t)$ | konsisten: histeresis pada $Q_i(t)$ |
| 2.5.6 | langkah 3 histeresis, langkah 4 hitung SAW | urutkan ulang: **hitung $Q_i(t)$** → **evaluasi histeresis** → **keputusan rasio** |

**Catatan [ANALISIS]:** penghalusan derau bisa dilakukan di dua titik (metrik mentah
atau skor). Yang penting **satu pilihan** dan dinyatakan eksplisit. Jika ingin
menghaluskan derau pada sumbernya, letakkan EWMA pada metrik mentah **dan** histeresis
pada skor — tetapi **jangan** menyebut histeresis bekerja pada metrik mentah.

---

## 4. Perbaikan Rumusan Masalah & Hipotesis **[USULAN]**

Acuan lengkap: `09_Rumusan_Masalah_dan_Judul.md`.

**RQ lama → RQ baru (ringkas):**

> *Sebelum:* "Bagaimana **merancang dan mengimplementasikan** ALQI … untuk
> mengevaluasi … kemudian mengintegrasikan … untuk meningkatkan QoS agregat dan
> mengurangi flapping …?"

> *Sesudah:* "Bagaimana **memodifikasi fungsi penilaian kualitas link** pada PCC
> statis menjadi skor komposit berbasis SAW dengan **normalisasi berbatas acuan tetap**
> dan **pembobotan adaptif**, sehingga QoS agregat meningkat dan flapping menurun
> dibandingkan PCC statis dan varian tanpa gerbang?"

**Hipotesis (operasional):**

| Sebelum | Sesudah |
|---|---|
| H1: histeresis menurunkan flapping | H1: histeresis asimetris **menurunkan laju flapping (flap/jam, jendela $W$=5 menit) tanpa melampaui batas *recovery latency*** |
| H2: QoS agregat lebih tinggi | H2: alokasi berbasis $Q_i(t)$ menghasilkan **goodput lebih tinggi dan delay p95 lebih rendah pada episode degradasi** dibanding rasio statis |
| — | H3 (baru): kontribusi histeresis **dapat dipisahkan** dari kontribusi skor multi-kriteria (ablasi) |

---

## 5. Perbaikan Desain Eksperimen (M5, M6, M11, M20)

| Sebelum | Sesudah |
|---|---|
| 3 skenario A/B/C | Tambah ablasi: **A** statis, **B** tanpa histeresis, **D** histeresis simetris, **F** asimetris, **G** baseline praktisi, **H** (opsional) stock-aware |
| Tanpa metrik sesi | Tambah **RST flow rate**, *session retention*, **ELS**, *time-to-rebalance* |
| Cuaca hanya dicatat | Tambah **pemblokan/pengacakan urutan** run + stratifikasi |
| Tanpa metrik konvergensi | Tambah ***allocation convergence time*** dan ***share error*** |
| Uji langsung produksi | Tambah **L1 offline (replay dataset)** + **L2 staging (`tc/netem`)** sebelum lapangan |

---

## 6. Perbaikan Rencana Statistik (M3, M4, M18, M19)

| Sebelum | Sesudah |
|---|---|
| Uji-t sampel independen | **Mixed-effects / GEE** untuk data berulang; **Poisson/negative binomial** untuk cacah flapping |
| "Skenario berurutan diperlakukan sebagai sampel independen" | Satuan analisis = **episode atau jam**, dengan koreksi autokorelasi |
| Tanpa power analysis | Tetapkan **primary outcome** + *smallest effect of interest*; hitung/simulasi power |
| Efek size opsional | **Wajib**: effect size + 95% CI + koreksi **Holm** |

---

## 7. Perbaikan Penomoran Tabel & Gambar (E1–E12)

**Usulan [USULAN]:** satu skema penomoran berurutan tanpa lompatan, dan setiap rujukan
di badan **harus** cocok dengan Daftar Tabel/Gambar.

| Tabel | Isi baru |
|---|---|
| 1 | Jadwal penelitian (6 bulan) |
| 2 | Spesifikasi perangkat keras |
| 3 | Spesifikasi perangkat lunak |
| 4 | Rancangan skema basis data |
| 5 | Data ilustratif metrik QoS per jalur |
| 6 | Hasil perhitungan ilustratif (normalisasi, $s_i$, $Q_i$) |
| 7 | Variabel penelitian |
| 8 | Skenario pengujian (dengan pembanding) |
| 9 | Pemetaan hipotesis → uji statistik |
| 10 | Ringkasan State of the Art |

Setiap gambar diberi judul unik dan diletakkan pada subbab yang sesuai isinya.

---

## 8. Perbaikan Bibliografi (B1–B8)

| Kode | Perbaikan |
|---|---|
| B1 | Selaraskan tahun Amalia → **2022** di seluruh naskah |
| B2 | Selaraskan atribusi penulis rain-fade → **Boeckenholt et al. (2024)**; verifikasi posisi "Lanfer" |
| B3 | Verifikasi penulis makalah "Efficient flow-aware dynamic link load balancing" (DOI `10.1109/COMSNETS.2009.4808841`); **jangan** memakai "Kandula" jika citekey "Kumar & Golash" |
| B4 | Ganti entri "LEO-NET, 2024" → **Hammer et al. (2024)** |
| B5 | Selaraskan Vafaei → **2021** (Prosedia vol. 199) |
| B6 | Tambahkan **Chen et al. (2025)** dan **Ji et al. (2026)** ke Daftar Pustaka & SOTA |
| B7 | Lengkapi halaman/DOI yang kosong (mis. Nugroho, 2023) |
| B8 | Hapus duplikasi sitasi "(X)(X)" pada tabel Lampiran |

**Rujukan metadata yang sudah terverifikasi** ada di arsip
`01_Arsip_SPA-HSM_Tahap_01-12/04_Tahap_03_Kerangka_Teori/05_Register_Referensi.csv` —
pakai sebagai sumber tunggal kebenaran sitasi.

---

## 9. Perbaikan Klaim & Kebaruan (K1–K6)

| Kode | Perbaikan |
|---|---|
| K1 | Ganti istilah **ALQI** → sebut "skor kualitas $Q_i(t)$"; jika tetap dipakai, sitasi **US 9,674,720 B2** dan bedakan |
| K2 | Hapus "belum ditemukan …" → ganti menjadi "berdasarkan pencarian pada [basis data], belum ditemukan …" setelah log dijalankan |
| K3 | Ubah kebaruan utama dari "integrasi" → **"mekanisme penilaian (normalisasi + pembobotan adaptif) + bukti komparatif"** |
| K4 | Ganti "**upper bound**" → "**kasus stres**" |
| K5 | Ganti "21 rujukan terindeks" → "21 rujukan" atau verifikasi status indeks masing-masing |
| K6 | Ganti "bukan hasil optimasi" → justifikasi parameter (standar/pilot/grid search) + analisis sensitivitas |

---

## 10. Checklist Perbaikan **[USULAN]**

**A. Konsistensi logika (wajib)**
- [ ] Letak histeresis diselaraskan (M14) — 1.2.10, 2.5.4, 2.5.6
- [ ] Rumus $s_i$ diperbaiki (E3) & $w_T$ diperbaiki (E4)
- [ ] Rumus rasio diberi batas $R_{\min}/R_{\max}$ (M15)
- [ ] RQ & hipotesis diubah ke gaya "memodifikasi" (M1, M2)
- [ ] Definisi operasional flapping (M12), dwell $k$, interval polling (M13)

**B. Keterukuran & statistik (wajib)**
- [ ] Rencana statistik diganti (M3, M4, M18, M19)
- [ ] Ablasi skenario ditambah (M5)
- [ ] Metrik RST/konvergensi ditambah (M6, M20)

**C. Klaim & kebaruan (wajib)**
- [ ] Istilah ALQI ditangani sebagai prior art (K1)
- [ ] Klaim "belum ada" diberi bukti pencarian (K2)
- [ ] "upper bound" → "kasus stres" (K4)

**D. Kerapian (penting)**
- [ ] Penomoran tabel/gambar (E1–E12)
- [ ] Bibliografi (B1–B8)
- [ ] Placeholder diisi (E10)

**E. Tambahan wajib untuk kelayakan**
- [ ] Bagian **etika/izin** (M10)
- [ ] **Staging + rollback + fail-static** (M9)
- [ ] **Pengacakan/blok** (M11)

---

## 11. Catatan Penutup **[ANALISIS]**

Perbaikan di atas **tidak mengubah rancangan inti** naskah lama. Yang berubah hanya
(1) konsistensi letak komponen, (2) ketepatan rumus, (3) kejelasan klaim, dan
(4) kerapian penyajian. Setelah checklist §10 selesai, naskah lama dapat dipakai
sebagai **lampiran historis** atau **basis penulisan Bab I–III** pada arah baru
(`00_README.md`).
