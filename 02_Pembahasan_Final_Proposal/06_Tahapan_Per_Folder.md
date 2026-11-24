# 06 — Tahapan Kerja per Folder (Peta Eksekusi)

**Status:** Draf kerja — rencana eksekusi berbasis folder.
**Fungsi:** Menerjemahkan tahapan penelitian **T0–T10** (`01_Struktur_Langkah_Penelitian_S2.md`)
dan roadmap `14_Tahapan_Penelitian.md` menjadi **urutan kerja konkret per folder di
repositori**: folder mana disentuh, berkas mana dibaca, berkas mana dibuat/diperbarui,
dan **kapan sebuah tahap boleh dianggap selesai**.
**Basis:** `00_README.md` §5–§8 (folder ini), `01_...`, `01_Pembahasan_ALQI_SAW/00_README.md`
+ `11`, `14`, `18`, `19`.
**Konvensi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]**.

> **Aturan induk (tidak berubah):** naskah final **hanya** ditulis di
> `02_Pembahasan_Final_Proposal/`; bahan analisis tetap di `01_Pembahasan_ALQI_SAW/`
> (folder ini **merujuk, tidak menyalin**); folder arsip **tidak diperbarui**.

---

## 1. Prinsip Pemetaan Folder

**[USULAN]** Setiap folder punya **satu peran** dan **satu arah aliran**:

```
ARSIP (rujukan beku)  →  01_Pembahasan_ALQI_SAW (analisis)  →  02_Pembahasan_Final_Proposal (naskah)
        ▲                             │                                   │
        └──── dibaca, tidak diubah ───┘          keputusan baru dicatat ───┘
                                                  di 01/ (analisis) lalu dirujuk
```

| Peran | Folder | Boleh diubah? | Yang dikerjakan di sini |
|---|---|---|---|
| **Arsip beku** | `00_Arsip_Proposal_SPA-HSM/`, `01_Arsip_SPA-HSM_Tahap_01-12/` | ❌ Tidak | Hanya dibaca sebagai sumber (dataset, statistik, protokol) |
| **Analisis aktif** | `01_Pembahasan_ALQI_SAW/` | ✅ Ya | Kajian, formulasi, spesifikasi, pra-penelitian, keputusan D-1…D-7 |
| **Naskah final** | `02_Pembahasan_Final_Proposal/` | ✅ Ya | Peta kerja, gerbang, draf Bab I–III, pra-registrasi |
| **Alat kerja** | `.venv/`, `01_Arsip_.../11_Kolektor_Baseline/*.py` | ✅ Hanya skrip data | Kolektor & analisis (jalan dari arsip, luaran ke `data/`) |

**Aturan aliran dokumen:** jika sebuah fakta/angka baru ditemukan saat menulis naskah,
**perbaiki dulu di `01_`**, lalu rujuk dari `02_` — jangan menyalin angka baru langsung
ke `02_` tanpa jejak di `01_`.

---

## 2. Peta Ringkas: Tahap → Folder → Berkas

| Tahap | Folder utama | Berkas masuk (dibaca) | Berkas keluar (dibuat/diperbarui) | Syarat ditutup |
|---|---|---|---|---|
| **T0** Kunci keputusan | `02_` (+ `01_`) | `01_/18`, `01_/19`, `01_/09`, `01_/11` §4 | `02_/00_README.md` §7; tabel keputusan di `01_/11` §4 | **B1** |
| **T1** Literatur & prior art | `01_` | `01_/02`, `01_/06`, `01_/10`, `01_/11` §1–2, `01_/01` | `01_/06`, `01_/10`, `01_/11` (status V/PA) + **berkas log pencarian baru** di `01_/` | **B6**, **G0** |
| **T2** Parameter & instrumen | `01_` | `01_/03`, `01_/04`, `01_/05`, `01_/08`, `01_/19` §7.3 | `01_/03` (tabel sumber nilai), `01_/05` (definisi operasional) | **B5** |
| **T3** Akuisisi data (L0) | `01_Arsip_.../11_Kolektor_Baseline/` → `01_/19` | `collector.py`, `analyze_*.py`, `data/*.jsonl` | data baru di `data/`, laporan di `01_/19` | **B2** (parsial), **B3**, **D-7** |
| **T4** Formalisasi & desain | `01_` | `01_/04`, `01_/05`, `01_/08`, `01_/15`, `01_/16` | `01_/05`, `01_/15`, `01_/16`, `arsitektur/` | temuan M14 |
| **T5** Prototipe | *(di luar repo naskah)* | luaran T4 + dataset T3 | artefak kode + laporan tes (repo terpisah/di luar arsip) | **G1** |
| **T6** Eksperimen L1 | *(luar repo)* → `01_/` | prototipe T5, dataset T3 | tabel hasil di `02_/` (Bab hasil) + ringkasan di `01_/19` | B-1, D-3, P2 |
| **T7** Eksperimen L2 | *(luar repo)* → `01_/` | prototipe, staging | ringkasan di `01_/08`, `01_/15` | **G2**, P4 |
| **T8** Eksperimen L3 (opsional) | *(luar repo)* → `01_/` | izin, protokol | catatan insiden/rollback di `01_/15` | P5 |
| **T9** Analisis statistik | `02_` (+ `01_/`) | `01_/08`, arsip `06_Tahap_04_Metodologi/04_Rencana_Analisis_Statistik.md` | `02_/05_Registrasi_Rencana_Analisis.md` (sebelum T6), bab analisis | **B4**, **G3** |
| **T10** Naskah & seminar | `02_` | `01_/06`, `01_/09`, `01_/18`, `01_/08`, luaran T1–T5 | `02_/02_Draf_Bab_I.md`, `03_`, `04_`, `00_README.md` §7 | **G-S2** |

**[ANALISIS]** Yang dikerjakan **di dalam repo** adalah T0–T4 dan T9–T10; T5–T8
bersifat **teknis/eksperimental** dan hanya **hasilnya** yang masuk ke `01_`/`02_`.

---

## 3. Urutan Eksekusi (Gelombang)

**[USULAN]** T0–T10 tidak dijalankan berurutan kaku; pekerjaan disusun per **gelombang**
agar baseline (T3) bisa berjalan paralel dengan literatur (T1).

| Gelombang | Tahap | Folder yang disentuh | Keluaran gelombang | Gerbang keluar |
|---|---|---|---|---|
| **W1 — Kunci** | T0 | `02_/00`, `01_/11`, `01_/18` | Keputusan D-1…D-6 terkunci; D-7 ditunda | **B1** disetujui pembimbing |
| **W2 — Verifikasi** (paralel) | T1, T2, T3-awal | `01_/` (06, 10, 11, 03, 05, 19) + `11_Kolektor_Baseline/` | Log pencarian, tabel parameter, uji independensi A–B | **B6**, **B5**, **G0**, **D-7** |
| **W3 — Desain & bangun** | T4, T5 | `01_/` (05, 15, 16, arsitektur/) | Spesifikasi teknis + prototipe deterministik | **G1** |
| **W4 — Eksperimen** | T6, T7, (T8) | luar repo → `01_/` | Tabel hasil L1/L2 | **G2** |
| **W5 — Bukti** | T9 | `02_/05` | Primary outcome + effect size + CI | **G3**, **B4** |
| **W6 — Naskah** | T10 | `02_/` (02, 03, 04, 00) | Bab I–III + deck | **G-S2** (skor ≥75) |

**[FAKTA]** Syarat **B2** (ground truth + prosedur pelabelan) melewati **dua** gelombang:
bahan di T3 (W2) dan prosedur formal ditulis di T2/T9 — karena itu B2 dicentang
**setelah** `02_/05` ada, bukan setelah T3.

---

## 4. Rincian per Folder

### 4.1 `02_Pembahasan_Final_Proposal/` (naskah final)

| Berkas | Tahap yang menulis | Aksi | Kapan |
|---|---|---|---|
| `00_README.md` | T0, T10 | Perbarui §7 (checklist B/P/Naskah) setiap syarat tertutup | Setiap akhir gelombang |
| `01_Struktur_Langkah_Penelitian_S2.md` | acuan tetap | Perbarui hanya bila struktur T0–T10 berubah | Jarang |
| `02_Draf_Bab_I.md` | T10 (awal) | **Buat baru** — pendahuluan, RQ, tujuan, kebaruan, batasan (dari `01_/09` + `01_/18`) | Setelah B1 disetujui (W1) |
| `03_Draf_Bab_II.md` | T10 (setelah T1/G0) | **Buat baru** — tinjauan pustaka + posisi (dari `01_/06` + log T1 + PA-1) | Setelah **G0** |
| `04_Draf_Bab_III.md` | T10 (setelah T2/T4) | **Buat baru** — metodologi (dari `01_/08` + `01_/03` + `01_/05`) | Setelah **B5** |
| `05_Registrasi_Rencana_Analisis.md` | T9 (sebelum T6) | **Buat baru** — primary outcome, SESOI, power, uji statistik | Setelah **B4** ditetapkan (akhir W2) |
| `06_Tahapan_Per_Folder.md` | — | Dokumen ini (peta eksekusi) | ✅ |

**Kriteria selesai folder:** Bab I–III ada, checklist §7 `00_README.md` semua
tercentang, skor uji penguji ≥75.

### 4.2 `01_Pembahasan_ALQI_SAW/` (analisis aktif)

| Berkas | Tahap | Aksi | Kriteria lulus |
|---|---|---|---|
| `01_Kelayakan_dan_Prior_Art.md` | T1 | Perbarui hasil PA-1…PA-3 | Prior art disitasi & dibedakan |
| `02_Research_Gap.md` | T1 | Kunci gap (G-N1/N2/W1/W2) setelah log pencarian | Semua klaim "belum ada" bersumber |
| `03_Spesifikasi_Parameter.md` | T2 | Tambah **tabel sumber tiap nilai** (θ, k, W, N, batas normalisasi) | Setiap angka punya sumber (**B5**) |
| `04_Analisis_Bobot_SAW.md` | T2/T4 | Finalkan normalisasi N-c & skema bobot | Rumus berdefinisi + rentang |
| `05_Formulasi_ALQI_Adaptif.md` | T2/T4 | Definisi operasional flapping/ELS/time-to-rebalance/RST | Definisi + satuan + instrumen |
| `06_Matriks_State_of_the_Art.md` | T1 | Tambah ≥15 SOTA terverifikasi | **G0** |
| `07_Kebaruan_dan_Kontribusi.md` | T1/T10 | Selaraskan dengan B1 & daftar "tidak diklaim" | Tanpa overclaim |
| `08_Rancangan_Eksperimen.md` | T2/T4/T7 | Kunci skenario perlakuan × kondisi | Protokol dapat diulang |
| `09_Rumusan_Masalah_dan_Judul.md` | T0/T10 | Kunci judul (dari `18` §10) | Judul disetujui |
| `10_Kandidat_Referensi.csv` | T1 | Verifikasi DOI/metadata (V-2) | Register referensi final |
| `11_Rencana_Verifikasi_Lanjutan.md` | T0/T1 | Isi status V-1…V-8, PA-1…PA-3, T-1…T-6, D-1…D-7 | Semua baris berstatus |
| `12`–`13` (audit & perbaikan) | acuan tetap | Hanya dibaca (checklist `13` §10 dipakai di T10) | — |
| `14_Tahapan_Penelitian.md` | acuan tetap | Rujukan jadwal & risiko | — |
| `15_Arsitektur_Sistem.md` | T4/T7 | State machine 8-state, kontrak antarmuka | Tanpa ambiguitas (**M14**) |
| `16_Arsitektur_Jaringan_MikroTik.md` | T4 | Konfigurasi PCC tri-link | Konsisten dengan topologi |
| `17_Uji_Kelayakan_dan_Risiko_Penguji.md` | T10 | Perbarui skor setiap B tertutup | Skor ≥75 |
| `18_B1_Lingkup_dan_Pernyataan_Kebaruan.md` | T0 | Sinkronisasi §9 setelah persetujuan | **B1** final |
| `19_Analisis_Pra_Penelitian.md` | T3/T6/T7 | Tambah sesi data baru + laporan korelasi per segmen | Sanity check + D-7 |
| `arsitektur/` | T4 | Perbarui gambar/skrip diagram | Diagram sinkron dengan `15`/`16` |
| `00_Bahan_Pengamatan/` | — | Beku (naskah lama sebagai bahan) | — |

**Berkas baru yang disarankan [USULAN]:**

| Berkas baru | Tahap | Isi |
|---|---|---|
| `20_Log_Pencarian_Literatur.md` | T1 | Tanggal, basis data, string, hit, lolos, alasan eksklusi (bukti V-1…V-8) |
| `21_Tabel_Justifikasi_Parameter.md` | T2 | Nilai × sumber × justifikasi (**B5**) |
| `22_Prosedur_Pelabelan_Ground_Truth.md` | T2/T3 | Definisi GT goodput, aturan label episode, anti-sirkularitas (**B2**) |

### 4.3 `01_Arsip_SPA-HSM_Tahap_01-12/` (arsip — baca saja)

| Subfolder | Dipakai pada tahap | Yang diambil |
|---|---|---|
| `11_Kolektor_Baseline/` | T3 | `collector.py`, `analyze_baseline.py`, `analyze_periodicity.py`, `data/*.jsonl` → **jalankan ulang**, luaran tetap di `data/` |
| `06_Tahap_04_Metodologi/` | T9 | `04_Rencana_Analisis_Statistik.md` (adopsi, bukan salin) |
| `04_Tahap_03_Kerangka_Teori/` | T10 | `03_Tabel_Klaim_dan_Sumber.md` (format tabel klaim) |
| `01_Manajemen_Proposal/` | T0 | Pola `01_Log_Keputusan.md` untuk mencatat D-1…D-7 |
| `09_Verifikasi_dan_Pencarian/` | T1 | Protokol pencarian sebelumnya (jangan diulang, cukup dilanjutkan) |
| `12_Presentasi/` | T10 | Deck lama sebagai dasar deck baru |
| `02`, `03`, `05`, `07`, `08`, `10` | rujukan | Dibaca bila relevan; **tidak diedit** |

**[ANALISIS]** Folder ini **tidak punya** tahap tulis. Satu-satunya aksi yang
diizinkan: **menjalankan** skrip kolektor/analisis (karena datanya di sini) dan
menyimpan luaran di `data/` + `logs/` (keduanya di-ignore Git).

### 4.4 `00_Arsip_Proposal_SPA-HSM/` (arsip — baca saja)

| Dipakai pada | Yang diambil |
|---|---|
| T1 | Referensi lama, jurnal, PDF untuk verifikasi ulang |
| T10 | Panduan penulisan kampus + draf lama sebagai pembanding (checklist `13` §10) |
| T0 | Riwayat keputusan lama (K-01/D-14 yang digantikan) |

---

## 5. Titik Serah-Antar Folder (handoff)

**[USULAN]** Agar tidak ada dokumen "menggantung", setiap serah terima punya
**kriteria bukti**:

| Dari | Ke | Yang diserahkan | Bukti serah terima |
|---|---|---|---|
| `01_/19` + `11_Kolektor_Baseline/` | `01_/03`, `01_/05` | Angka kalibrasi (korelasi, episode, throughput) | Laporan korelasi per segmen di `19` |
| `01_/06` + log T1 | `02_/03_Draf_Bab_II.md` | ≥15 SOTA + prior art | **G0** lolos |
| `01_/03` + `01_/05` | `02_/04_Draf_Bab_III.md` | Parameter & rumus final | **B5** tertutup |
| `01_/09` + `01_/18` | `02_/02_Draf_Bab_I.md` | RQ, judul, kalimat kebaruan | **B1** disetujui |
| Luaran T6/T7/T9 | `02_/05_...` + bab hasil | Primary outcome, effect size, CI | **B4** & **G3** |
| `01_/17` | `02_/00_README.md` §7 | Skor uji penguji | Skor ≥75 |

---

## 6. Gerbang per Folder (kapan folder dianggap "selesai tahap")

| Gate | Folder yang harus berstatus selesai | Cek objektif | Jika gagal |
|---|---|---|---|
| **G0** | `01_/` (06, 10, 11, 01) | Log pencarian lengkap; prior art disitasi; ≥15 SOTA | Perluas pencarian; ganti sudut kebaruan |
| **G1** | luar repo (prototipe) | Unit test lulus; skoring ≤1 s; deterministik | Perbaiki; turunkan cakupan |
| **G2** | luar repo + `01_/08`, `01_/15` | Efek gerbang (B vs D vs F) terukur & signifikan arah | Perbaiki parameter; ulang ulangan |
| **G3** | `02_/05` | Primary outcome terjawab dengan effect size + CI | Turunkan klaim; laporkan non-inferioritas |
| **G-S2** | `02_/` (02, 03, 04, 00) | B1–B6 tertutup & skor ≥75 | Tunda seminar |

**Aturan kunci (dari `01_` §4, tidak berubah):** tidak ada klaim kebaruan di `02_/02`
sebelum **G0** dan **B3** lolos; tidak ada klaim "lebih stabil/akurat" sebelum **B4**;
**D-7** tidak dikunci sebelum uji independensi A–B (T3) selesai.

---

## 7. Urutan Kerja Praktis (minggu ini)

| # | Aksi | Folder / berkas | Menutup |
|---:|---|---|---|
| 1 | Minta persetujuan pembimbing atas Varian C & judul | `01_/18` §12 → `02_/00` §7 | **B1** final |
| 2 | Buat `20_Log_Pencarian_Literatur.md`; jalankan V-1…V-3 + PA-1…PA-3 | `01_/` (baru + `06`, `10`, `11`) | **B6**, menuju **G0** |
| 3 | Jalankan throughput 1 s pada 3 WAN → korelasi A–B → putuskan **D-7** | `11_Kolektor_Baseline/` → `01_/19` | **B3** (awal) |
| 4 | Tetapkan primary outcome + SESOI + power | `02_/05_Registrasi_Rencana_Analisis.md` | **B4** |
| 5 | Susun `21_Tabel_Justifikasi_Parameter.md` | `01_/` (baru + `03`) | **B5** |
| 6 | Tulis `22_Prosedur_Pelabelan_Ground_Truth.md` | `01_/` (baru) | **B2** |
| 7 | Mulai baseline ≥7 hari (paralel dengan #2–#6) | `11_Kolektor_Baseline/` → `01_/19` | **B3** penuh |
| 8 | Setelah B1 disetujui → buat `02_Draf_Bab_I.md` | `02_/` | menuju **G-S2** |

---

## 8. Checklist Progres per Folder

**`02_Pembahasan_Final_Proposal/`**
- [x] `00_README.md` — indeks & status
- [x] `01_Struktur_Langkah_Penelitian_S2.md`
- [x] `06_Tahapan_Per_Folder.md` — dokumen ini
- [ ] `02_Draf_Bab_I.md`
- [ ] `03_Draf_Bab_II.md`
- [ ] `04_Draf_Bab_III.md`
- [ ] `05_Registrasi_Rencana_Analisis.md`

**`01_Pembahasan_ALQI_SAW/`**
- [ ] `20_Log_Pencarian_Literatur.md` (T1)
- [ ] `21_Tabel_Justifikasi_Parameter.md` (T2)
- [ ] `22_Prosedur_Pelabelan_Ground_Truth.md` (T2/T3)
- [ ] `19` — sesi data ≥7 hari + laporan korelasi per segmen (T3)
- [ ] `11` §4 — D-1…D-7 terkunci (T0/T3)

**Arsip (baca saja)**
- [x] `11_Kolektor_Baseline/` — kolektor & analisis siap dipakai ulang
- [x] `06_Tahap_04_Metodologi/04_Rencana_Analisis_Statistik.md` — siap diadopsi di T9
