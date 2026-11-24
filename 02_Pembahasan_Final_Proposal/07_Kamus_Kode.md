# 07 — Kamus Kode (Kode Indeks & Daftar Rujukannya)

**Status:** Rujukan tetap — jangan menambah kode baru di sini; kode baru lahir di dokumen asalnya lalu didaftarkan di sini.
**Fungsi:** Menjelaskan **arti, isi, status, dan rujukan** setiap kode indeks yang dipakai di seluruh ruang kerja (`01_Pembahasan_ALQI_SAW/`, `02_Pembahasan_Final_Proposal/`, dan arsip) — **lengkap di satu berkas** agar pembaca tidak perlu bolak-balik antar dokumen.
**Cara pakai:** baca §1 untuk aturan penamaan dan kode yang sering tertukar, lalu cari kodenya di §2–§15 sesuai awalan hurufnya.
**Konvensi label isi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]** (sama dengan dokumen lain).

> **Aturan dokumen ini:** setiap baris kode menyebutkan **isi (ringkas) + rujukan** (dokumen §bagian). Isi di sini adalah **ringkasan**; kalimat lengkap dan alasan tetap ada di dokumen asal — jangan menjadikan kamus ini sebagai pengganti dokumen sumber.

---

## 1. Cara Membaca: Awalan Kode & Peringatan Tabrakan

### 1.1 Awalan kode (berlaku di seluruh ruang kerja)

| Awalan | Kelompok | Arti | Rujukan aturan |
|---|---|---|---|
| **T0–T10** | Tahap | Tahap penelitian berurutan (T = *tahap*) | `01` §3 (folder 02), `01_Pembahasan_ALQI_SAW/14` §2 |
| **G0, G1, G2, G3, G-S2** | Gerbang (*gate*) | Syarat lulus antar-tahap; G-S2 = gerbang akhir kelayakan S2 | `01` §4 (folder 02) |
| **B1–B6** | Syarat *blocking* | Wajib ditutup sebelum seminar | `01_Pembahasan_ALQI_SAW/17` §7 |
| **P1–P5** | Perbaikan penting (*non-blocking*) | Wajib dikerjakan, tapi tidak menahan seminar | `01_Pembahasan_ALQI_SAW/17` §8 |
| **K-A…K-E** | Klaim/kontribusi | Kontribusi ilmiah yang diklaim (A–E) | `01_Pembahasan_ALQI_SAW/18` §7 |
| **G-N, G-W** | Gap (aktif) | *Research gap* versi baru (N = normalisasi/bobot, W = waktu/stabilitas) | `01_Pembahasan_ALQI_SAW/02` §3 |
| **G-M, G-E, G-I, G-C** | Gap (arsip) | *Research gap* versi lama (M=method, E=evidence, I=integration, C=context) | Arsip `02_Tahap_01_Gap_dan_Novelty/01` §3 |
| **D-1…D-7, D-21** | Keputusan (aktif) | Keputusan penelitian yang harus dikunci | `01_Pembahasan_ALQI_SAW/11` §4, `18` §3 |
| **D-01…D-20** | Keputusan (arsip) | Log keputusan arsip; **hanya D-14 yang masih dirujuk** | Arsip `01_Manajemen_Proposal/01_Log_Keputusan.md` |
| **V-1…V-8** | Verifikasi literatur | Pekerjaan pencarian lintas basis data | `01_Pembahasan_ALQI_SAW/11` §1 |
| **PA-1…PA-3** | Verifikasi prior art | Penanganan paten US 9,674,720 B2 | `01_Pembahasan_ALQI_SAW/11` §2 |
| **T-1…T-6** | Verifikasi teknis | Pekerjaan teknis/data (T-6 = uji independensi) | `01_Pembahasan_ALQI_SAW/11` §3 |
| **A-1…A-3, B-1…B-5, C-1…C-4, D-1…D-4, E-1…E-3** | Kekurangan temuan penguji | Kode **kekurangan** pada `17` §4 — *bukan* keputusan D | `01_Pembahasan_ALQI_SAW/17` §4 |
| **M1–M20, E1–E12, K1–K6, B1–B8** | Temuan audit naskah lama | M=metodologis, E=editorial, K=klaim, B=bibliografi | `01_Pembahasan_ALQI_SAW/12` §3–§6 |
| **A–H** | Perlakuan eksperimen | Bentuk fungsi kontrol yang dibandingkan | `01_Pembahasan_ALQI_SAW/08` §4a |
| **N, T, S, R, K** | Kondisi degradasi | Pola kondisi yang diamati | `01_Pembahasan_ALQI_SAW/08` §4b |
| **ISP-A, ISP-B, ISP-C** | Link | Tiga jalur uji (dua LEO + satu FO) | `01_Pembahasan_ALQI_SAW/00_README` §6 |
| **S0–S7** | State machine | Delapan kombinasi status tri-link | `01_Pembahasan_ALQI_SAW/15` §8 |
| **N-a…N-d** | Normalisasi | Empat teknik normalisasi SAW | `01_Pembahasan_ALQI_SAW/04` §2 |
| **P1–P12** | Parameter | Dua belas parameter teknis QoS/alokasi | `01_Pembahasan_ALQI_SAW/03` §2–§3 |
| **Q1–Q5** | Pertanyaan penguji | Lima pertanyaan inti sidang | `01_Pembahasan_ALQI_SAW/17` §1, `02` §1 |
| **L0–L3** | Lapisan uji | Data → offline → staging → lapangan | `01_Pembahasan_ALQI_SAW/08` §3 |
| **RQ1–RQ6 / H1–H5** | Rumusan & hipotesis | Sub-pertanyaan penelitian dan hipotesis (arsip + `09`) | Arsip `03_Tahap_02_Rumusan_Masalah/01`, `01_Pembahasan_ALQI_SAW/09` §2 |
| **K-01…K-07** | Konstanta keputusan (arsip) | Keputusan yang dianggap tetap di naskah lama | Arsip `01_Manajemen_Proposal/01_Log_Keputusan.md` |
| **S-1…S-7** | Syarat kelayakan (arsip aktif) | Syarat sebelum Bab I dikunci | `01_Pembahasan_ALQI_SAW/01` §4 |
| **W1–W6** | Gelombang kerja | Pengelompokan tahap per folder | `06_Tahapan_Per_Folder` §3 |
| **E-3** | Penanda penutup | Lihat peringatan §1.2 no. 4 | `01` §3 (T0), `17` §4E |

### 1.2 Kode yang mudah tertukar (peringatan wajib)

| Kode sama, arti beda | Konteks A | Konteks B | Cara membedakan |
|---|---|---|---|
| **A–H** | **Perlakuan** eksperimen (`08` §4a): A=statis, B=tanpa gerbang, D=simetris, F=asimetris, G=netwatch, H=stock-aware | **ISP-A/B/C** = link fisik (`00_README` §6); huruf **C dan E** tidak dipakai sebagai perlakuan | Kalau disertai kata "perlakuan/skenario" → A–H; kalau disertai "ISP/ether/link" → ISP |
| **B1–B6** | **Syarat blocking** (`17` §7) | **Temuan bibliografi** naskah lama (`12` §6) | Di `02_` dan `01_/17–19` → blocking; di `12`/`13` → bibliografi |
| **B-1…B-5** | **Kekurangan metode** (`17` §4B), ditulis dengan tanda hubung | Syarat blocking B1 (tanpa hubung) | Ada tanda hubung → temuan penguji |
| **D-1…D-7** | **Keputusan aktif** (`11` §4) | **Kekurangan desain/statistik** (`17` §4D) | `17` §4D juga memakai D-1…D-4; selalu tulis sumbernya (`17` §4D vs `11` §4) |
| **E-3** | **Kekurangan** "lingkup belum dikunci" (`17` §4E) | Penutup B1 di T0 (`01` §3) dan `17` §7 (kolom "Menutup" B1 = A-2, A-3, **E-3**) | Arti tunggal: "lingkup belum dikunci"; konteksnya berbeda |
| **G-M3 / G-E1** | **Gap arsip** versi lama | Gap aktif `G-N1/N2/W1/W2` | Di `02_` §4 tertulis "G-M3/G-E1" = rujukan ke gap arsip untuk K-E |
| **P1–P5** | **Perbaikan** (`17` §8) | **Parameter** P1–P12 (`03`) | Disertai nama perbaikan/parameter |
| **T1–T6** | **Tahap** penelitian (tanpa hubung) | **Verifikasi teknis** T-1…T-6 (dengan hubung) | Ada tanda hubung → pekerjaan teknis |
| **K1–K6** | **Temuan klaim** audit (`12` §5) | **K-A…K-E** kontribusi baru (`18` §7); **K-01…K-07** konstanta arsip | Format: `K1` = temuan; `K-A` = klaim; `K-01` = keputusan arsip |
| **V-1…V-8** | **Verifikasi literatur** aktif (`11` §1) | — | Jangan tertukar dengan "Varian A/B/C" |
| **S-1…S-7** | **Syarat kelayakan** (`01` §4) | **Kondisi S** (degradasi FO) di `08` §4b; **S0–S7** state machine | `S-1` = syarat; `S` tunggal = kondisi; `S0`–`S7` = state |

---

## 2. Tahap Penelitian (T0–T10)

Sumber utama: `02_Pembahasan_Final_Proposal/01_Struktur_Langkah_Penelitian_S2.md` §3, `01_Pembahasan_ALQI_SAW/14_Tahapan_Penelitian.md` §3. Pemetaan folder: `06_Tahapan_Per_Folder.md` §2.

| Kode | Nama tahap | Isi (ringkas) | Folder kerja | Syarat yang ditutup |
|---|---|---|---|---|
| **T0** | Kunci keputusan | Kunci D-1…D-6, tunda D-7, tegaskan Varian C, pilih judul | `02_/00`, `01_/11`, `01_/18` | **B1** |
| **T1** | Studi literatur & prior art | Jalankan V-1…V-8, PA-1…PA-3, snowballing ≥15 SOTA | `01_/` (01, 02, 06, 10, 11) | **B6**, **G0** |
| **T2** | Spesifikasi parameter & instrumen | Finalkan P1–P12 + sumber tiap angka, definisi operasional, prosedur sampling | `01_/03`, `01_/05` | **B5** |
| **T3** | Akuisisi & konsolidasi data (L0) | Baseline ≥7 hari, throughput 1 s, uji independensi A–B, pelabelan, data sintetis | `11_Kolektor_Baseline/` → `01_/19` | **B2** (parsial), **B3**, **D-7** |
| **T4** | Formalisasi & perancangan | Rumus final, state machine 8-state, bucket mapping, kontrak antarmuka | `01_/04, 05, 08, 15, 16` | Temuan **M14** |
| **T5** | Implementasi prototipe (*scoring engine*) | Modul EWMA/normalisasi/bobot/gerbang, unit test, determinisme | di luar repo naskah | **G1** |
| **T6** | Eksperimen L1 (offline/replay) | Semua kombinasi N × bobot, ablasi (P1), sensitivitas N (P3), resampling (P2) | luar repo → `02_` (hasil) | **B-1**, **D-3**, P2 |
| **T7** | Eksperimen L2 (staging) | Perlakuan A–H × kondisi N/T/S/R/K, injeksi `tc/netem`, demo rollback (P4) | luar repo → `01_/08, 15` | **G2**, P4 |
| **T8** | Eksperimen L3 (lapangan, opsional) | Mode pantau pasif, izin, ToS, fail-static/watchdog/rollback | luar repo → `01_/15` | P5 |
| **T9** | Analisis statistik & pembuktian | Mixed-effects/GEE, Poisson/NB, effect size + CI, Holm, bootstrap, pra-registrasi | `02_/05` | **B4**, **G3** |
| **T10** | Penulisan naskah & seminar | Bab I–III, deck, latihan tanya-jawab, uji penguji ≥75 | `02_/02, 03, 04` | **G-S2** |

**[ANALISIS]** T0–T4 dan T9–T10 dikerjakan **di dalam repo**; T5–T8 teknis dan hanya hasilnya yang masuk ke `01_`/`02_` (`06` §2).

---

## 3. Gerbang Keputusan (G0–G3, G-S2)

Sumber: `02_/01` §4; `01_Pembahasan_ALQI_SAW/14` §7.

| Kode | Setelah tahap | Pertanyaan kunci | Jika gagal |
|---|---|---|---|
| **G0** | T1 | Gap & prior art tertangani? (menutup **B6**) | Perluas pencarian; ganti sudut kebaruan |
| **G1** | T5 | Prototipe berjalan & deterministik? | Perbaiki; turunkan cakupan fitur |
| **G2** | T7 | Efek gerbang terukur di staging? | Perbaiki parameter; ulang ulangan |
| **G3** | T9 | Primary outcome terjawab? | Turunkan klaim; laporkan non-inferioritas |
| **G-S2** | T10 | B1–B6 tertutup & skor uji penguji ≥75? | Tunda seminar; tutup syarat tersisa |

**Aturan kunci [USULAN]:** tidak ada klaim kebaruan di naskah final sebelum **G0** dan **B3** lolos; tidak ada klaim "lebih stabil/akurat" sebelum **B4**; **D-7** tidak dikunci sebelum uji independensi A–B selesai.

---

## 4. Syarat Blocking (B1–B6)

Sumber: `01_Pembahasan_ALQI_SAW/17_Uji_Kelayakan_dan_Risiko_Penguji.md` §7 (kolom "Menutup"), `01_/18` (B1), `02_/00` §2 (status hari ini).

| Kode | Syarat (lengkap) | Menutup kekurangan | Bukti yang dihasilkan | Status (21 Nov 2026) |
|---|---|---|---|---|
| **B1** | Kunci lingkup + satu kalimat kebaruan | **A-2**, **A-3**, **E-3** | Halaman "lingkup & kebaruan" 1 paragraf (`18` §4–§5) | ✅ Usulan siap (`18`); ⏳ menunggu persetujuan pembimbing |
| **B2** | Tetapkan **ground truth** & metrik validasi indeks; hindari sirkularitas (throughput tidak boleh menjadi kriteria Q sekaligus GT) | **B-5**, **C-3** | Definisi operasional + prosedur pelabelan | ⏳ Sebagian (sesi 17–18 Nov, episode FO teramati); prosedur formal belum ditulis |
| **B3** | Baseline **≥7 hari** + **uji independensi A–B** → putuskan tri-link atau fallback dual | **C-1**, **C-2** | Laporan korelasi per segmen + keputusan **D-7** | ⏳ Sebagian (residu A–B 0,384–0,393 pada 17–18 Nov; 0,683–0,704 pada 12 Nov) |
| **B4** | **Primary outcome + SESOI + power/sample size** + pra-registrasi | **D-1**, **D-2** | Bagian rencana statistik (`02_/05`) | ❌ Belum |
| **B5** | **Justifikasi parameter** (θ, k, N, batas normalisasi) | **B-2**, **B-3** | Tabel parameter + sumber tiap nilai | ❌ Belum |
| **B6** | Tangani **prior art ALQI** + hapus overclaim ("bebas osilasi", "upper bound") | **B-4** | Sitasi US 9,674,720 B2 di Bab II + daftar "tidak diklaim" | ⏳ Sebagian (`18` §8 sudah; sitasi Bab II belum) |

**Putusan [ANALISIS]:** sistem **LAYAK BERSYARAT** hanya jika B1–B6 ditutup (`17` §6).

---

## 5. Perbaikan Penting Non-Blocking (P1–P5)

Sumber: `01_Pembahasan_ALQI_SAW/17` §8.

| Kode | Perbaikan | Menutup kekurangan | Melekat pada tahap |
|---|---|---|---|
| **P1** | Uji ablasi **bobot statis vs adaptif** | **B-1** | T6 |
| **P2** | Kebijakan **resampling 2 s → 1 s** + analisis aliasing 15 s | **C-4** | T3/T6 |
| **P3** | Uji sensitivitas **jumlah bucket N** | **D-3** | T6 |
| **P4** | Tunjukkan **fail-static/rollback** berjalan | **D-4** | T7 |
| **P5** | Siapkan **izin + tinjauan ToS** dua Starlink | **E-1**, **E-2** | T8 |

---

## 6. Klaim & Kontribusi (K-A…K-E)

Sumber: `01_Pembahasan_ALQI_SAW/18_B1_Lingkup_dan_Pernyataan_Kebaruan.md` §7 (versi final setelah B1) dan `01_/07` §1–§6 (versi awal, K-A…K-D).

| Kode | Kontribusi | Jenis | Gap yang dijawab | Peran | Bukti |
|---|---|---|---|---|---|
| **K-A** | **Studi komparatif terkontrol** teknik normalisasi (N-a/N-b/N-c) × skema pembobotan (statis/sama-rata/entropy/CRITIC/MEREC/hibrida) pada deret metrik real-time tri-link | Empiris | **G-N1** | **Utama** | Matriks kinerja + effect size |
| **K-B** | **Pembobotan hibrida adaptif** $w(t)=\gamma w^{\text{ahli}}+(1-\gamma)w^{\text{obj}}(t)$ + gerbang kestabilan | Metode | **G-N2** | **Utama** | Kurva trade-off akurasi ↔ stabilitas ($\gamma$) |
| **K-C** | **Normalisasi berbatas acuan tetap** untuk komparabilitas temporal | Desain | **G-N1** | Pendukung | Uji *rank reversal* & stabilitas indeks |
| **K-D** | **Dekomposisi kontribusi** normalisasi vs pembobotan | Metode | **G-W2** | Pendukung | Ablasi 2×2 |
| **K-E** | **Bukti penerapan**: dampak $Q_i(t)$ pada alokasi PCC (ELS, flapping, RST) | Empiris | **G-M3/G-E1** (gap arsip) | **Penguat** (bukan klaim utama) | Instrumentasi stok $S_i$/$F_i$, L2 staging |

**[ANALISIS]** K-A dan K-B adalah klaim utama; K-E menjawab **A-2** (tidak melepas konteks stok/sesi) tanpa menjadikannya klaim algoritmik, sehingga positioning tidak terbelah (**A-3**) — `18` §7.

---

## 7. Gap Penelitian Aktif (G-N1, G-N2, G-W1, G-W2)

Sumber: `01_Pembahasan_ALQI_SAW/02_Research_Gap.md` §3 dan §5. Pola penulisan: *"Meskipun …, belum ada …, sehingga …"* (`02` §1).

| Kode | Isi gap | Jenis | Kekuatan novelty | Peran |
|---|---|---|---|---|
| **G-N1** | Teknik **normalisasi SAW** belum diuji pada deret metrik link **real-time** yang bising (Vafaei et al. 2021 hanya dataset statis) | G-M (method) | **Tinggi** | Kontribusi utama (K-A, K-C) |
| **G-N2** | **Pembobotan objektif/hibrida** belum dievaluasi pada penilaian kualitas link WAN heterogen (1 FO + 2 LEO) skala kecil + hubungan akurasi ↔ stabilitas | G-M | **Tinggi** | Kontribusi utama (K-B, K-D) |
| **G-W1** | **Stabilitas indeks komposit** belum diukur terhadap transien periodik LEO | G-E/G-M | Sedang–tinggi | Pendukung |
| **G-W2** | **Dekomposisi kontribusi** normalisasi vs pembobotan belum dilakukan | G-M | Sedang–tinggi | Pendukung |

**Bukan gap [USULAN]:** "belum ada yang memakai SAW untuk jaringan", "belum ada bobot objektif pada SAW", "ALQI istilah baru", "menggantikan SD-WAN" (`02` §4).

---

## 8. Gap Arsip (G-E1, G-E2, G-M1, G-M2, G-M3, G-I1, G-C1, G-C2)

Sumber: arsip `01_Arsip_SPA-HSM_Tahap_01-12/02_Tahap_01_Gap_dan_Novelty/01_Peta_Gap_Penelitian.md` §3 dan §7. **Status:** arsip; hanya **G-M3/G-E1** yang masih dirujuk aktif (melalui **K-E**, `02_/00` §4).

| Kode | Isi gap | Jenis | Status dalam arah baru |
|---|---|---|---|
| **G-E1** | Dampak perubahan aturan PCC terhadap **integritas sesi** (RST) belum diukur | Evidence | Dirujuk oleh **K-E** (RST) |
| **G-E2** | **Akumulasi stok koneksi lama** di link yang memburuk belum diukur | Evidence | Tidak dipakai sebagai klaim utama |
| **G-M1** | Histeresis tidak **diturunkan dari dinamika link LEO** | Method | Menjadi dasar **P1**/parameter $k$ (`03` §5) |
| **G-M2** | Konversi skor kontinu → **bucket PCC diskret** belum diformalkan | Method | Menjadi **P3**/state machine (`15` §9) |
| **G-M3** | Kebijakan alokasi belum **stock-flow aware** ($S_i$, $F_i$) | Method | Dijawab **K-E** (penguat) |
| **G-I1** | Empat komponen belum disatukan dalam satu loop | Integration | Diakui **bukan** novelty tunggal |
| **G-C1** | Studi PCC dominan statis/homogen/lab | Context | Validitas eksternal (L3) |
| **G-C2** | Portabilitas platform belum diuji | Context | Di luar lingkup Varian C |

---

## 9. Keputusan Penelitian (D-1…D-7, D-21)

Sumber: `01_Pembahasan_ALQI_SAW/11_Rencana_Verifikasi_Lanjutan.md` §4 (D-1…D-7), `18` §3 (D-21), `19` §7 (status terkini). **Arti singkat:** D = *decision*.

| Kode | Keputusan | Opsi | Rekomendasi / status |
|---|---|---|---|
| **D-1** | **Lingkup** | Varian A (luas) / B (skoring saja) / C (tengah) | **C** — lihat **D-21** |
| **D-2** | **Nama istilah** | Ganti ALQI / pertahankan + sitasi prior art | Ganti/batasi; simbol $Q_i(t)$ (`05` catatan nama) |
| **D-3** | **Skema bobot** | Statis / objektif / hibrida | **Hibrida** ($\gamma$) |
| **D-4** | **Normalisasi default** | N-a / N-b / **N-c** | **N-c** (batas acuan tetap) |
| **D-5** | **Primary outcome** | Spearman ρ / stabilitas / AUC | Tetapkan **satu** (terkait **B4**) |
| **D-6** | **Keterlibatan lapangan** | Ya / tidak (cukup offline + staging) | Tergantung waktu & izin (terkait **P5**) |
| **D-7** | **Topologi uji** | Dual-ISP (A+C) / **Tri-link 1 FO + 2 LEO (A+B+C)** / Dual + validasi tri | **Ditunda** sampai **B3**/T-6 selesai (`19` §7.1) |
| **D-21** | **Kunci lingkup = Varian C** (diusulkan) | — | Skoring adaptif + bukti penerapan alokasi; **menutup B1** (`18` §3) |

**Varian lingkup (dipakai oleh D-1/D-21):**

| Varian | Isi | Konsekuensi |
|---|---|---|
| **Varian A** | Luas: skoring + alokasi + sesi + kontroler | Kembali ke cakupan SPA-HSM (ditolak) |
| **Varian B** | Sempit: murni skoring komparatif | Waktu aman; kebaruan paling tipis (**A-1** tetap) |
| **Varian C** | Skoring adaptif + bukti penerapan alokasi sadar-stok | **Dipilih** (menutup A-1/A-2/A-3/E-3) |

---

## 10. Pekerjaan Verifikasi (V, PA, T-)

Sumber: `01_Pembahasan_ALQI_SAW/11_Rencana_Verifikasi_Lanjutan.md` §1–§3.

### 10.1 Verifikasi literatur (V-1…V-8)

| Kode | Pekerjaan | Menutup |
|---|---|---|
| **V-1** | Pencarian di Scopus, IEEE Xplore, ACM DL, ScienceDirect (bukan hanya OpenAlex) | Klaim gap |
| **V-2** | Verifikasi metadata & DOI 5 kandidat di `10_Kandidat_Referensi.csv` | Sitasi sahih |
| **V-3** | Baca **teks penuh** entropy-SAW `10.1007/s11276-021-02625-y` | Diferensiasi dari K-B |
| **V-4** | String `("weighting" OR "normalization") AND ("link quality" OR "QoS scoring") AND ("real-time" OR streaming)` | G-N1/G-N2 |
| **V-5** | String `("temporal stability" OR "rank reversal") AND "MCDM" AND ("time series" OR dynamic)` | G-W1 |
| **V-6** | Verifikasi angka ITU-T Y.1541 / G.114 ke teks standar | **B5** |
| **V-7** | Snowballing 10 paper inti | ≥15 SOTA (**G0**) |
| **V-8** | Cek retraksi & predator venue | Kredibilitas |

### 10.2 Prior art (PA-1…PA-3)

| Kode | Pekerjaan | Menutup |
|---|---|---|
| **PA-1** | Salin abstrak & klaim utama **US 9,674,720 B2** (Crestron, 2017) sebagai *related prior art* | **B6** |
| **PA-2** | Cari paten/artikel lain "link quality index" + ambang | **B6** |
| **PA-3** | Putuskan: ganti istilah ALQI / pertahankan + sitasi + pembeda | **B6**, **D-2** |

### 10.3 Verifikasi teknis & data (T-1…T-6)

| Kode | Pekerjaan | Menutup |
|---|---|---|
| **T-1** | Inventaris isi `data/*.jsonl` (kolom, resolusi, durasi) | Kesiapan L1 |
| **T-2** | Cek REST API akun **write** terpisah (SNMP opsional) | Prasyarat adopsi |
| **T-3** | Cek telemetri Starlink (gRPC dish) | Ground truth throughput (**B2**) |
| **T-4** | Konfirmasi izin lokasi & ToS ISP | **P5** |
| **T-5** | Uji `tc/netem` di staging | L2 |
| **T-6** | **Uji independensi dua Starlink** (ambang korelasi < 0,7) | **B3**, **D-7** |

---

## 11. Kekurangan dari Uji Penguji (A, B-, C-, D-, E-)

Sumber: `01_Pembahasan_ALQI_SAW/17_Uji_Kelayakan_dan_Risiko_Penguji.md` §4. **Penting:** kode berhuruf tunggal dengan tanda hubung = **kekurangan**, bukan keputusan.

| Kode | Kekurangan | Mengapa diserang | Ditutup oleh |
|---|---|---|---|
| **A-1** | Kebaruan menyusut menjadi "studi komparatif" | "Studi komparatif bukan kontribusi algoritmik" | **B1** (K-B sebagai metode) |
| **A-2** | Arah mundur: novelty *stock-flow* + sesi dilepas | "Mengapa meninggalkan yang paling kuat?" | **B1** (K-E) |
| **A-3** | Positioning terbelah: skoring atau alokasi? | "Kontribusinya yang mana?" | **B1**, **D-21** |
| **B-1** | "Adaptif" belum terbukti adaptif ($\gamma$ tetap) | "Bedanya dengan EWMA biasa?" | **P1** |
| **B-2** | Batas normalisasi dipinjam dari TIPHON/Y.1541 | "Batas acuan arbitrer" | **B5** |
| **B-3** | Parameter belum bersumber (θ, k, W, N) | "Dari mana angka-angka ini?" | **B5** |
| **B-4** | Prior art ALQI (US 9,674,720 B2) | "Menyerupai prior art" | **B6** |
| **B-5** | Sirkularitas: throughput sebagai kriteria Q **dan** ground truth | "Indeks dinilai dengan metrik sendiri" | **B2** |
| **C-1** | Baseline 2,2 jam (protokol minta 7–14 hari) | "Tidak cukup untuk distribusi" | **B3** |
| **C-2** | Dua Starlink berkorelasi 0,68–0,70 (ambang < 0,7) | "Hanya ~2 sumber independen" | **B3** |
| **C-3** | Ground truth lemah (goodput hanya proksi) | "Bagaimana membuktikan Q benar?" | **B2** |
| **C-4** | Resolusi temporal: probe 2 s vs $T_s$ 1 s; transien 15 s ter-alias | "Indeks mengukur artefak sampling?" | **P2** |
| **D-1** | Belum ada power analysis / SESOI | "Berapa episode? Kalau tidak signifikan?" | **B4** |
| **D-2** | Banyak kombinasi (3 normalisasi × 6 bobot) → p-hacking | "Berapa hipotesis primer?" | **B4** |
| **D-3** | Kuantisasi bucket N=20 → langkah 5% | "Apakah selisih 5% berarti?" | **P3** |
| **D-4** | Failover PCC tak menyelamatkan sesi lama | "Klaim 'tanpa mengorbankan stabilitas' di mana?" | **P4** |
| **E-1** | Dua Starlink residensial untuk jaringan komersial (ToS + biaya) | Etika & relevansi RT/RW Net | **P5** |
| **E-2** | Data pelanggan, izin, anonimisasi belum ada bukti | Syarat operasional | **P5** |
| **E-3** | Lingkup belum dikunci (Varian A/B/C terbuka) | "Apa lingkup final Anda?" | **B1**, **D-21** |

---

## 12. Temuan Audit Naskah Lama (M, E, K, B)

Sumber: `01_Pembahasan_ALQI_SAW/12_Pengamatan_Proposal_Lama.md` §3–§6; perbaikan: `13_Perbaikan_Proposal_Lama.md` §1–§9. **Berlaku hanya di `12`/`13`** — jangan dicampur dengan kode aktif.

### 12.1 Metodologis (M1–M20) — `12` §4

| Kode | Masalah | Dampak | Perbaikan di `13` |
|---|---|---|---|
| **M1** | RQ memuat tiga kata kerja | Tidak falsifiabel | §4 (RQ "memodifikasi") |
| **M2** | H2 "QoS agregat lebih tinggi" tanpa definisi | Tidak terukur | §4 (H2 kuantitatif) |
| **M3** | Uji-t sampel independen untuk deret waktu | Galat Tipe I | §6 (mixed-effects/GEE) |
| **M4** | Skenario berurutan "sebagai sampel independen" | Keliru statistik | §6 (satuan = episode/jam) |
| **M5** | Hanya 3 skenario (A/B/C), tanpa ablasi | Kontribusi tak terpisah | §5 (A/B/D/F/G/H) |
| **M6** | Tidak ada metrik RST | Klaim stabilitas tak terbukti | §5 (RST flow) |
| **M7** | Ambang histeresis tanpa nilai konkret | Tidak dapat direplikasi | §10 (θ 60/80) |
| **M8** | Bobot statis disebut "adaptif" | Ambiguitas klaim | §4, `04` §3 |
| **M9** | Implementasi langsung di produksi | Validitas internal lemah | §5 (L1/L2 sebelum L3) |
| **M10** | Tidak ada etika/izin | Wajib untuk jaringan komersial | §10 (etika) |
| **M11** | Cuaca/beban hanya dicatat | Confounder | §5 (blok/pengacakan) |
| **M12** | "Flapping" tidak didefinisikan | Tidak terukur | §10 (definisi W=5 mnt) |
| **M13** | Nilai $k$ (dwell) & interval polling tidak disebut | Tidak dapat direplikasi | §10 ($k$ 20/60, $T_s$ 1 s) |
| **M14** 🔴 | Letak histeresis tidak konsisten (3 pernyataan) | Inti metode kabur | §3 (alur tunggal) |
| **M15** | Rasio PCC tanpa batas min/maks | Risiko starvation | §2.3 ($R$ 15–85%) |
| **M16** | Rasio berbasis skor, bukan kapasitas | Overload link kecil | §2.3 (kapasitas $C_i$) |
| **M17** | Klaim "bebas osilasi" | Overclaim | §9 (hapus) |
| **M18** | Tidak ada power/primary outcome | Underpowered | §6 |
| **M19** | Tetap parametrik meski data skewed | Uji tidak sesuai | §6 |
| **M20** | Hanya koneksi baru diubah; tanpa metrik konvergensi | Klaim beban tidak terjaga | §5 (ELS, time-to-rebalance) |

### 12.2 Editorial (E1–E12) — `12` §3

| Kode | Masalah | Lokasi | Perbaikan (`13` §1) |
|---|---|---|---|
| **E1** | Judul "Tabel 5. Bobot Ilustratif throughput" tidak cocok | Hal. 25 | Judul tabel diselaraskan |
| **E2** | Rujukan tabel di badan ≠ Daftar Tabel | Hal. 22 | Penomoran seragam (`13` §7) |
| **E3** | Rumus $s_i$ tidak memberi bobot pada packet loss | Hal. 24 | §2.2 ($w_{PL}$ masuk) |
| **E4** | `W_T = 020` (hilang koma) | Hal. 25 | 0,20 |
| **E5** | Gambar 4 & 5 bertajuk sama | Hal. 13–14 | Judul unik |
| **E6** | Gambar 8 & 10 bertajuk hampir sama; 10 salah subbab | Hal. 23, 26 | Dipindah |
| **E7** | Menyebut "Tabel 12" tanpa Tabel 10–11 | Hal. 34 | Penomoran ulang |
| **E8** | Karakter rusak `550 km` | Hal. 10 | ≈550 km |
| **E9** | Salah ketik "di ataranya" | Hal. 16 | "di antaranya" |
| **E10** | Placeholder belum diisi | Hal. 21–22 | Diisi |
| **E11** | Judul "Skenario Percobaan" ≠ isi (variabel) | Hal. 28 | Judul diselaraskan |
| **E12** | Jadwal 3 bulan tidak realistis | Hal. 18–19 | Jadwal 6 bulan |

### 12.3 Klaim (K1–K6) — `12` §5

| Kode | Masalah | Perbaikan (`13` §9) |
|---|---|---|
| **K1** | Istilah "ALQI" punya prior art (US 9,674,720 B2) | Ditangani sebagai prior art; simbol $Q_i(t)$ |
| **K2** | Klaim "belum ditemukan" tanpa log pencarian | Frasa "berdasarkan pencarian pada…" |
| **K3** | Kebaruan utama = "integrasi" | Diganti mekanisme penilaian + bukti |
| **K4** | Istilah "upper bound" Starlink | → "kasus stres" |
| **K5** | "21 rujukan terindeks" belum diverifikasi | → "21 rujukan" |
| **K6** | Bobot/ambang "bukan hasil optimasi" | Justifikasi + sensitivitas (**B5**) |

### 12.4 Bibliografi (B1–B8) — `12` §6

| Kode | Masalah | Perbaikan (`13` §8) |
|---|---|---|
| **B1** | Tahun Amalia tidak konsisten (2023 vs 2022) | Selaraskan ke 2022 |
| **B2** | Atribusi penulis rain-fade tertukar (Lanfer/Boeckenholt) | Boeckenholt et al. (2024) |
| **B3** | Citekey ≠ penulis (Kumar & Golash vs Kandula) | Verifikasi DOI `10.1109/COMSNETS.2009.4808841` |
| **B4** | "LEO-NET, 2024" dipakai sebagai penulis | → Hammer et al. (2024) |
| **B5** | Vafaei 2022 vs 2021 | → 2021 |
| **B6** | Chen (2025) & Ji (2026) tanpa entri | Tambahkan ke daftar pustaka |
| **B7** | Metadata tidak lengkap (Nugroho 2023) | Lengkapi halaman/DOI |
| **B8** | Sitasi ganda "(X)(X)" | Hapus duplikasi |

---

## 13. Kode Eksperimen & Arsitektur

### 13.1 Perlakuan sistem (A–H) — `01_/08` §4a

| Kode | Perlakuan | Peran |
|---|---|---|
| **A** | PCC statis (rasio tetap) | Baseline utama |
| **B** | Skor $Q_i(t)$ **tanpa histeresis** | Isolasi efek gerbang |
| **D** | Histeresis **simetris** | Pembanding bentuk gerbang |
| **F** | Histeresis **asimetris** (usulan) | Sistem yang diusulkan |
| **G** | Baseline praktisi (netwatch failover) | Jangkar praktik |
| **H** | Alokasi **sadar-stok** (opsional) | Isolasi kontribusi stok |
| ~~C, E~~ | **Tidak dipakai** sebagai perlakuan di `08`; huruf C/E hanya ada di arsip `03_Tahap_02.../02_Hipotesis` §1.11 (C=simetris, E=simetris+affinity) | Arsip: dihapus dari skema aktif |

**Arsip (8 skenario A–H, `03_Tahap_02.../02_Hipotesis` §1.11):** A statis, B tanpa histeresis, C simetris, D asimetris, E simetris+affinity, F asimetris+affinity, G netwatch, H stock-flow aware. **Perbandingan kunci:** B→D, C→D, D→F, F→H, A→H, G→H.

### 13.2 Kondisi degradasi (N, T, S, R, K) — `01_/08` §4b

| Kode | Kondisi | Tujuan |
|---|---|---|
| **N** | Normal (semua link sehat) | Baseline akurasi & stabilitas |
| **T** | **Transien LEO** (pola ~15 detik) | Ketahanan lonjakan singkat |
| **S** | **Degradasi FO bertahap** (kongesti) | Respons degradasi *sustained* |
| **R** | **Rain fade** (throughput turun) | Bobot kontekstual |
| **K** | Kombinasi T + S | Uji interaksi |

### 13.3 Link & state machine — `01_/00_README` §6, `01_/15` §8

| Kode | Arti |
|---|---|
| **ISP-A** (`ether1-ISP-A`) | Starlink **LEO-1** |
| **ISP-B** (`ether2-ISP-B`) | Starlink **LEO-2** |
| **ISP-C** (`ether3-ISP-C`) | Fiber optik (**IndiHome**) |
| **S0** | B/B/B — semua sehat → rasio mengikuti $Q$ |
| **S1** | T/B/B — LEO-1 turun → alihkan dari A |
| **S2** | B/T/B — LEO-2 turun → alihkan dari B |
| **S3** | B/B/T — FO turun → alihkan dari C |
| **S4** | T/T/B — kedua LEO turun → prioritaskan FO (uji korelasi antar-LEO) |
| **S5** | T/B/T — LEO-1 + FO turun → prioritaskan LEO-2 |
| **S6** | B/T/T — LEO-2 + FO turun → prioritaskan LEO-1 |
| **S7** | T/T/T — semua turun → *fail-static* |

*(B = Baik, T = Terdegradasi; status ditentukan gerbang histeresis pada $Q_i(t)$.)*

### 13.4 Lapisan uji (L0–L3) — `01_/08` §3

| Kode | Lapisan | Risiko ke pelanggan |
|---|---|---|
| **L0** | Data (akuisisi/konsolidasi) | Nol |
| **L1** | Offline (replay dataset) | Nol |
| **L2** | Staging terkendali (`tc/netem`) | Nol (lab) |
| **L3** | Lapangan (opsional) | Rendah |

### 13.5 Teknik normalisasi (N-a…N-d) — `01_/04` §2

| Kode | Rumus | Komparabilitas temporal | Status |
|---|---|---|---|
| **N-a** | benefit $x/x_{\max}$, cost $x_{\min}/x$ (naskah lama) | Sedang | Pembanding |
| **N-b** | $(x-x_{\min})/(x_{\max}-x_{\min})$ | **Rendah** | Pembanding |
| **N-c** | Clip ke batas acuan tetap TIPHON/Y.1541 | **Tinggi** | **Default (D-4)** |
| **N-d** | Vektor/sum | Sedang | Tidak dipakai |

---

## 14. Parameter & Metrik Teknis (P1–P12)

Sumber: `01_Pembahasan_ALQI_SAW/03_Spesifikasi_Parameter.md` §2–§3.

| Kode | Parameter | Jenis | Catatan |
|---|---|---|---|
| **P1** | One-way delay (OWD) | Cost | TIPHON <150/<250/<350/<450 ms |
| **P2** | RTT | Cost | ≈ 2× OWD |
| **P3** | Jitter / IPDV | Cost | TIPHON 0/75/125/225 ms |
| **P4** | Packet loss ratio | Cost | Y.1541 1×10⁻³ / 1×10⁻⁵ |
| **P5** | Throughput / goodput | **Benefit** | Starlink hujan 137→90,2 Mbps |
| **P6** | Available bandwidth / headroom | Benefit | $0{,}9C - L$ |
| **P7** | Utilisasi link | Cost | Batas share 15–85% |
| **P8** | Frekuensi flapping | Output | **Jangan** dimasukkan ke indeks |
| **P9** | Pangsa beban efektif $L_i$ | Turunan | $(S_i+F_i)/\sum$ |
| **P10** | ELS (*effective load skew*) | Turunan | $0$ = sesuai target |
| **P11** | Time-to-rebalance | Turunan | Waktu ELS < ambang |
| **P12** | RST flow rate | Turunan | Biaya pemutusan sesi |

**Simbol & parameter formulasi** (`01_/05` §4): $\alpha$ (EWMA 0,10–0,20), $N$ (jendela bobot 30–60), $\gamma$ (hibrida 0,5), $\theta_{\text{deg}}$=60, $\theta_{\text{pemulih}}$=80, $k_{\text{down}}$=20, $k_{\text{up}}$=60, $T_s$=1 s, $W$=5 menit, $b_{\min}$=2, $b_{\max}$=14 ($N_{\text{bucket}}$=20).

**Metrik hasil & metrik arsip:**

| Kode/Nama | Arti | Rujukan |
|---|---|---|
| **ELS** | *Effective Load Skew* = $\tfrac12\sum\lvert L_i-T_i\rvert$ | `01_/03` §3 |
| **TTR** | *Time-to-rebalance* | `01_/03` §3 |
| **RST flow** | Rasio aliran TCP yang menerima ≥1 RST | `01_/03` §3 |
| **SIWG** (arsip) | *Session-Impact-Weighted Goodput* = $G_{eff}(1-\lambda\cdot \text{RST}_{flow})$; $\lambda=1$ default | Arsip `03_Tahap_02.../02_Hipotesis` §1.8 |
| **$S_i(t)$ / $F_i(t)$** | Stok koneksi lama / laju koneksi baru per link | Arsip `03_Tahap_02.../02_Hipotesis` §1.9 |

---

## 15. Rumusan Masalah, Hipotesis, dan Kode Pendukung Lain

### 15.1 RQ & hipotesis

| Kode | Isi | Rujukan | Status |
|---|---|---|---|
| **RQ1–RQ4** | Persepsi → Deteksi → Alokasi → Bukti (sub-RQ arah baru) | `01_/09` §2 | Aktif |
| **RQ5** | Stok koneksi lama (*stock-flow*) | `01_/09` §3 (Varian C) | Aktif bila Varian C |
| **RQ1–RQ6** | RQ arsip (persepsi, deteksi, sesi, stock-flow, evaluasi, portabilitas) | Arsip `03_Tahap_02.../01_Rumusan` §2 | Arsip |
| **H1** | Histeresis asimetris menurunkan flapping tanpa melampaui batas *recovery latency* | `01_/09` §2 | Aktif |
| **H2** | Alokasi berbasis $Q_i(t)$ → goodput naik & delay p95 turun pada episode degradasi | `01_/09` §2 | Aktif |
| **H3** | Kontribusi histeresis dapat dipisahkan dari skor (ablasi) | `01_/09` §2 | Aktif |
| **H3a–H3c, H4, H5** | Hipotesis arsip (sesi, SIWG, antarmuka) | Arsip `03_Tahap_02.../02_Hipotesis` | Arsip |

### 15.2 Kode pendukung lain

| Kode | Arti | Rujukan |
|---|---|---|
| **Q1–Q5** | Lima pertanyaan penguji (kebaruan, gap, metode, kepercayaan hasil, batas klaim) | `01_/17` §1; `02_/01` §1 |
| **K-01…K-07** (arsip) | Konstanta keputusan naskah lama: K-01 dual-ISP (**digantikan** D-7), K-02 Starlink *upper bound*, K-03 bobot statis, K-04 MikroTik = testbed, K-05 nama SPA-HSM (ALQI/TLABA tidak dipakai), K-06 satuan analisis episode/jam, K-07 kausal utama di staging | Arsip `01_Manajemen_Proposal/01_Log_Keputusan.md` |
| **D-01…D-20** (arsip) | Log keputusan lama (arah, skenario, baseline, RST, bucket, sitasi, tier, topologi, judul…). **Yang masih dirujuk aktif:** hanya **D-14** (topologi dual A+C — kini **digantikan D-7**) | Arsip `01_Manajemen_Proposal/01_Log_Keputusan.md` |
| **N1–N4** (arsip) | Kontribusi naskah lama: N1 observasi/deteksi, N2 stock-flow aware, N3 perlakuan sesi, N4 evaluasi | Arsip `01_Manajemen_Proposal/02_Posisi_dan_Fokus_Penelitian.md` |
| **K1–K4** (arsip) | Kontribusi SPA-HSM: K1 formulasi, K2 arsitektur 3 lapis, K3 ablasi, K4 bukti empiris | `00_Arsip_Proposal_SPA-HSM/arsitektur/README.md` |
| **S-1…S-7** | Syarat kelayakan sebelum Bab I dikunci (novelty, istilah ALQI, lingkup, pembanding, frasa klaim, log pencarian, uji independensi) | `01_/01` §4 |
| **W1–W6** | Gelombang kerja per folder | `06_Tahapan_Per_Folder` §3 |
| **Tabel 7–10** | 7 = variabel, 8 = skenario, 9 = hipotesis→uji, 10 = SOTA | `01_/08` §2, §4; `01_/06` §1; `01_/13` §7 |
| **Berkas baru usulan** | `20_Log_Pencarian_Literatur` (V), `21_Tabel_Justifikasi_Parameter` (**B5**), `22_Prosedur_Pelabelan_Ground_Truth` (**B2**) | `06` §4.2 |

---

## 16. Rantai Rujukan Cepat (dari kode → dokumen)

| Kalau Anda membaca kode… | Buka dokumen… |
|---|---|
| **B1–B6** | `01_Pembahasan_ALQI_SAW/17` §7; status: `02_Pembahasan_Final_Proposal/00` §2 |
| **P1–P5** | `01_Pembahasan_ALQI_SAW/17` §8 |
| **A-, B-, C-, D-, E-** (kekurangan) | `01_Pembahasan_ALQI_SAW/17` §4 |
| **K-A…K-E** | `01_Pembahasan_ALQI_SAW/18` §7 |
| **G-N1/G-N2/G-W1/G-W2** | `01_Pembahasan_ALQI_SAW/02` §3 |
| **G-M/G-E/G-I/G-C** (arsip) | Arsip `02_Tahap_01_Gap_dan_Novelty/01_Peta_Gap_Penelitian.md` §3 |
| **D-1…D-7** | `01_Pembahasan_ALQI_SAW/11` §4; status D-7: `01_/19` §7.1 |
| **D-21** | `01_Pembahasan_ALQI_SAW/18` §3 |
| **V-, PA-, T-** | `01_Pembahasan_ALQI_SAW/11` §1–§3 |
| **M-, E-, K-, B-** (audit) | `01_Pembahasan_ALQI_SAW/12` §3–§6; perbaikan: `13` |
| **A–H** (perlakuan) | `01_Pembahasan_ALQI_SAW/08` §4a |
| **N/T/S/R/K** (kondisi) | `01_Pembahasan_ALQI_SAW/08` §4b |
| **S0–S7** | `01_Pembahasan_ALQI_SAW/15` §8 |
| **P1–P12** (parameter) | `01_Pembahasan_ALQI_SAW/03` §2–§3 |
| **N-a…N-d** | `01_Pembahasan_ALQI_SAW/04` §2 |
| **T0–T10, G0–G3, G-S2** | `02_Pembahasan_Final_Proposal/01` §3–§4 |
| **T0–T10 → folder** | `02_Pembahasan_Final_Proposal/06_Tahapan_Per_Folder.md` §2 |
| **K-01…K-07, D-01…D-20** (arsip) | Arsip `01_Manajemen_Proposal/01_Log_Keputusan.md` |

---

## 17. Pemeliharaan Dokumen

- Kode **baru** lahir di dokumen asalnya (mis. B7 lahir di `17`), lalu didaftarkan di sini.
- Kode yang **digantikan** diberi status *(digantikan)* dan tetap dicantumkan — jangan dihapus, karena masih muncul di arsip.
- Setiap kali kode diubah artinya, perbarui **§1.2 (kode yang mudah tertukar)** agar pembaca tidak salah paham.
- [ ] Periksa ulang §16 setiap akhir gelombang kerja (`06` §3).
