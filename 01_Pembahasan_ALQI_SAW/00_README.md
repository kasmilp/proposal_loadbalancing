# Pembahasan Baru — ALQI Berbasis SAW

**Status:** Draf kajian awal (belum naskah resmi)
**Fungsi:** Menampung seluruh analisis arah penelitian baru — *Adaptive Link Quality
Index* (ALQI) berbasis *Simple Additive Weighting* (SAW) — sebagai respons atas
penilaian bahwa cakupan **SPA-HSM terlalu luas** untuk diterapkan sebagai sistem
kontroler penuh.
**Latar:** Seluruh alur kerja SPA-HSM (folder 01–12 lama) telah dipindahkan ke
`01_Arsip_SPA-HSM_Tahap_01-12/` dan bersifat **arsip, bukan naskah aktif**.

---

## 1. Cara Membaca

Setiap dokumen di folder ini menyatakan asal pernyataan dengan label:

| Label | Arti |
|---|---|
| **[FAKTA]** | Berasal dari sumber/korpus yang dapat dilacak (standar, jurnal, paten, data repo) |
| **[ANALISIS]** | Penalaran kritis peneliti atas fakta, bukan pernyataan sumber |
| **[USULAN]** | Desain/keputusan penelitian yang diusulkan, belum divalidasi |

Aturan: **tidak ada klaim kebaruan tanpa bukti literatur**, dan klaim "belum ada"
hanya boleh ditulis setelah log pencarian dijalankan (lihat `11_Rencana_Verifikasi_Lanjutan.md`).

---

## 2. Isi Folder

| Berkas | Isi |
|---|---|
| `00_README.md` | Indeks, status, ringkasan eksekutif |
| `01_Kelayakan_dan_Prior_Art.md` | Putusan kelayakan ALQI–SAW untuk S2 + temuan prior art paten |
| `02_Research_Gap.md` | Gap penelitian berbasis bukti (G-N1, G-N2, G-W1, G-W2) |
| `03_Spesifikasi_Parameter.md` | Parameter QoS teknis, satuan, rentang acuan, arah cost/benefit |
| `04_Analisis_Bobot_SAW.md` | Kriteria benefit/cost, opsi normalisasi, pendekatan bobot |
| `05_Formulasi_ALQI_Adaptif.md` | Formulasi matematis dari statis → adaptif |
| `06_Matriks_State_of_the_Art.md` | Tabel pembanding penelitian terdahulu + nilai kuantitatif |
| `07_Kebaruan_dan_Kontribusi.md` | Klaim kebaruan realistis untuk S2 + batas klaim |
| `08_Rancangan_Eksperimen.md` | Arsitektur, skenario, pembanding, metrik, statistik |
| `09_Rumusan_Masalah_dan_Judul.md` | RQ versi "memodifikasi" + rekomendasi judul |
| `10_Kandidat_Referensi.csv` | Daftar kandidat referensi (perlu verifikasi) |
| `11_Rencana_Verifikasi_Lanjutan.md` | Pekerjaan literatur & teknis yang belum selesai |

---

## 3. Ringkasan Eksekutif

**[ANALISIS]** Pengembangan ALQI berbasis SAW **layak bersyarat** sebagai fokus tesis
S2. Kelayakannya bergantung pada **pemindahan kebaruan** dari *"menggabungkan metrik
QoS"* (tidak baru) ke *"mekanisme pembobotan dan normalisasi yang adaptif serta
tervalidasi secara empiris"* (masih terbuka).

**Skor kelayakan sementara:**

| Aspek | Bobot | Skor |
|---|---:|---:|
| Ketajaman masalah | 15% | 82 |
| Research gap berbasis bukti | 20% | 68 |
| Kontribusi ilmiah S2 | 20% | 70 |
| Keterukuran parameter | 15% | 90 |
| Kelayakan teknis & ketersediaan data | 15% | 88 |
| Risiko klaim & prior art | 15% | 55 |
| **Agregat berbobot** | **100%** | **± 74** |

Ambang internal: ≥85 layak dengan revisi minor · 75–84 layak dengan perbaikan
terarah · 65–74 perlu revisi mayor · <65 belum layak.
**Putusan: GO dengan perbaikan terarah (penyempitan lingkup wajib).**

**Tiga temuan kunci:**

1. **[FAKTA]** Istilah **ALQI sudah memiliki prior art**: US Patent 9,674,720 B2
   (Crestron Electronics, 2017) mendefinisikan *Application Link Quality Indicator*
   dari banyak indikator QoS, termasuk "modified ALQI" dengan ambang jumlah kejadian.
   Nama dan gagasan dasarnya **tidak boleh diklaim sebagai kebaruan**.
2. **[FAKTA]** Batas acuan parameter tersedia dan terverifikasi: TIPHON
   (ETSI TR 101 329) dan ITU-T Y.1541/G.114.
3. **[FAKTA]** Aset data sudah ada: kolektor baseline *read-only* + dataset **2,2 jam**
   di arsip `11_Kolektor_Baseline/` — memungkinkan studi offline tanpa risiko ke
   pelanggan.

---

## 4. Hubungan dengan Arsip

| Arsip | Isi | Peran |
|---|---|---|
| `00_Arsip_Proposal_SPA-HSM/` | Materi lama (draf Bab I–II ALQI, PDF, jurnal, analisis kelayakan SPA-HSM) | Rujukan historis |
| `01_Arsip_SPA-HSM_Tahap_01-12/` | Alur kerja SPA-HSM: gap, novelty, RQ, teori, metodologi, baseline, presentasi | Rujukan historis |
| `01_Pembahasan_ALQI_SAW/` | **Naskah aktif baru** | Kajian arah penelitian ALQI–SAW |

**Aturan:** dokumen arsip tidak diperbarui. Perubahan arah dicatat di folder ini.
