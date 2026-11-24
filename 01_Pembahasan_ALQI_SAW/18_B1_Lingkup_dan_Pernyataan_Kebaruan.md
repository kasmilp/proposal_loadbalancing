# 18 — B1: Keputusan Lingkup & Pernyataan Kebaruan

**Status:** Draf keputusan (menunggu persetujuan pembimbing)
**Fungsi:** Menutup syarat *blocking* **B1** pada `17_Uji_Kelayakan_dan_Risiko_Penguji.md`
§7 — yaitu (a) mengunci lingkup penelitian dan (b) menetapkan **satu kalimat
kebaruan** yang konsisten dengan seluruh dokumen.
**Menutup temuan:** A-1, A-2, A-3 (kebaruan & positioning) dan E-3 (lingkup belum dikunci).
**Konvensi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]**.

---

## 1. Masalah yang Harus Diselesaikan

**[ANALISIS]** Dokumen `01`–`17` memuat **dua klaim kebaruan yang bersaing**:

| Sumber | Klaim kebaruan |
|---|---|
| `07_Kebaruan_dan_Kontribusi.md` | Skoring adaptif: normalisasi berbatas tetap + pembobotan hibrida (K-A…K-D) |
| `00_README.md` §6, `08` §4, `15` §8 | Tri-link + state machine 8-state + ELS/alokasi |

Akibatnya, bila penguji bertanya *"kebaruannya apa?"*, jawabannya bisa dua arah.
B1 menetapkan **satu** jawaban dan menurunkannya ke seluruh dokumen.

---

## 2. Tiga Opsi Lingkup (rekap)

| Opsi | Isi | Menutup | Membuka risiko |
|---|---|---|---|
| **Varian A** | Luas: skoring + alokasi + sesi + controller (mendekati SPA-HSM) | A-2 | Cakupan & waktu (kembali ke masalah awal) |
| **Varian B** | Sempit: murni **skoring** komparatif | Waktu terjamin | **A-1** tetap: dinilai "aplikasi SAW" |
| **Varian C** | **Skoring adaptif sebagai mesin keputusan + bukti penerapan alokasi sadar-stok** | A-1, A-2, A-3, E-3 | Cakupan lebih besar dari B |

**[ANALISIS]** Varian A ditolak (kembali ke cakupan yang dinilai terlalu luas).
Varian B aman tetapi kebaruan paling tipis. **Varian C** mempertahankan dua kekuatan
sekaligus — skoring adaptif (metode) **dan** konsekuensi alokasi (bukti) — tanpa
membangun kontroler penuh.

---

## 3. Keputusan **[USULAN]**

> ### D-21 — Lingkup dikunci pada **Varian C**
>
> Penelitian **memodifikasi fungsi penilaian kualitas link** (skoring adaptif) dan
> **menguji konsekuensinya pada alokasi PCC** — bukan membangun sistem kontroler baru.
> Alokasi/sesi diuji **sebatas bukti penerapan**, bukan sebagai objek algoritmik
> tersendiri.

**Batas eksplisit Varian C:**

| Termasuk | Tidak termasuk |
|---|---|
| Indeks $Q_i(t)$ (EWMA → normalisasi → bobot γ) | Kontroler adaptif penuh |
| Gerbang histeresis (kestabilan keputusan) | Pembelajaran bobot (*self-tuning*) |
| Pemetaan $Q_i(t)$ → rasio/bucket PCC | Perubahan algoritma PCC |
| Pengukuran dampak alokasi (ELS, flapping, RST) | Klaim *control loop* formal |
| Tri-link FO + 2 LEO | Generalisasi > 3 link / multi-vendor |

---

## 4. Pernyataan Kebaruan (satu paragraf)

**[USULAN]** Teks siap pakai untuk Bab I (subbab "Kebaruan Penelitian"):

> **Kebaruan penelitian ini.** Berbeda dari studi PCC yang menetapkan rasio secara
> statis dan dari studi pembobotan MCDM yang diuji pada dataset statis, penelitian ini
> **memodifikasi fungsi penilaian kualitas link** pada jaringan tri-link heterogen
> (satu fiber optik dan dua satelit LEO) menjadi skor komposit berbasis *Simple
> Additive Weighting* dengan **normalisasi berbatas acuan tetap** dan **pembobotan
> hibrida adaptif** yang diatur parameter γ, lalu **membuktikan secara komparatif dan
> atributif** — melalui ablasi normalisasi × pembobotan serta pengukuran dampaknya
> pada rasio PCC (ELS, flapping, RST) — teknik mana yang menghasilkan indeks paling
> **akurat sekaligus paling stabil secara temporal**. Penelitian ini tidak mengklaim
> metode MCDM baru, tidak mengklaim istilah ALQI, dan tidak mengklaim dukungan
> multi-vendor.

**Versi 30 detik (lisan):**
> "Kami tidak menciptakan metode baru. Kami memodifikasi cara menilai kualitas link —
> normalisasi berbatas tetap plus bobot adaptif — dan membuktikan lewat ablasi teknik
> mana yang paling akurat dan paling stabil, termasuk dampaknya pada pembagian trafik
> PCC di jaringan satu FO + dua Starlink."

---

## 5. Kalimat Kebaruan Tunggal (untuk slide judul)

**[USULAN]**
> *"Penelitian ini memodifikasi penilaian kualitas link berbasis SAW agar stabil secara
> temporal dan membuktikan dampaknya pada alokasi PCC di jaringan 1 FO + 2 LEO —
> bukan menciptakan metode MCDM baru."*

**Uji satu kalimat:**

| Kriteria | Terpenuhi? |
|---|---|
| Menyebut **objek** yang dimodifikasi | ✅ penilaian kualitas link (SAW) |
| Menyebut **pembanding** | ✅ PCC statis; studi normalisasi pada dataset statis |
| Menyebut **bukti** | ✅ ablasi + pengukuran dampak alokasi |
| Menyebut **batas** | ✅ bukan metode baru |

---

## 6. Novelty Statement (format templat)

**[USULAN]**
> **Berbeda dari** [pembanding], **penelitian ini memodifikasi** [fungsi penilaian
> kualitas link], **sehingga** [kemampuan/bukti baru yang sebelumnya tidak tersedia].

Diisi:

| Unsur | Isi |
|---|---|
| Pembanding | (a) PCC rasio statis; (b) Vafaei dkk. (normalisasi pada dataset statis); (c) entropy-SAW 5G (tanpa uji stabilitas temporal) |
| Yang dimodifikasi | Fungsi penilaian kualitas link: normalisasi berbatas acuan tetap + pembobotan hibrida adaptif |
| Kemampuan/bukti baru | Bukti komparatif + atributif teknik mana yang akurat **dan** stabil, serta dampaknya pada rasio PCC (ELS, flapping, RST) |

---

## 7. Peta Kontribusi (setelah B1)

| Kode | Kontribusi | Jenis | Gap | Peran |
|---|---|---|---|---|
| **K-A** | Studi komparatif terkontrol normalisasi × pembobotan pada deret metrik real-time tri-link | Empiris | G-N1 | **Utama** |
| **K-B** | Pembobotan hibrida adaptif $w(t)=\gamma w^{\text{ahli}}+(1-\gamma)w^{\text{obj}}(t)$ + gerbang kestabilan | Metode | G-N2 | **Utama** |
| **K-C** | Normalisasi berbatas acuan tetap untuk komparabilitas temporal | Desain | G-N1 | Pendukung |
| **K-D** | Dekomposisi kontribusi normalisasi vs bobot | Metode | G-W2 | Pendukung |
| **K-E** | Bukti penerapan: dampak $Q_i(t)$ pada alokasi PCC (ELS, flapping, RST) | Empiris | G-M3/G-E1 | **Penguat** (bukan klaim utama) |

**[ANALISIS]** K-E inilah yang menjawab A-2 (tidak melepas konteks stok/sesi) **tanpa**
menjadikannya klaim algoritmik — sehingga positioning tidak terbelah (A-3).

---

## 8. Yang **Tidak** Diklaim (daftar final)

| Tidak diklaim | Alasan |
|---|---|
| Metode MCDM baru | SAW sudah mapan |
| "Pertama memakai SAW / bobot objektif" | Entropy-SAW sudah ada |
| Istilah/konsep ALQI | Prior art US 9,674,720 B2 |
| Kontroler adaptif penuh | Lingkup dipersempit |
| Kontrol loop formal | Tidak dibuktikan |
| Generalisasi > 3 link / multi-vendor | Di luar lingkup |
| QoE / kepuasan pengguna | Yang diukur QoS |
| Dampak ekonomi | Tidak diukur |

---

## 9. Sinkronisasi Dokumen (wajib setelah B1 disetujui)

| Dokumen | Perubahan yang harus dilakukan |
|---|---|
| `00_README.md` | Tegaskan **Varian C** di ringkasan eksekutif; hapus frasa yang menyiratkan dua kebaruan |
| `07_Kebaruan_dan_Kontribusi.md` | Tambah **K-E**; samakan kalimat novelty dengan §4 dokumen ini |
| `09_Rumusan_Masalah_dan_Judul.md` | RQ payung & Varian B/C → selaras; tambah RQ bukti penerapan (K-E) |
| `08_Rancangan_Eksperimen.md` | Pastikan metrik ELS/flapping/RST tercantum sebagai bukti penerapan |
| `17_...` | Tandai **B1 = selesai**; skor kebaruan naik (lihat §11) |
| `11_...` | Catat D-21 di tabel keputusan |

---

## 10. Dampak pada Judul

**[USULAN]** Judul mengikuti Varian C:

1. **(Utama)**
   *"Modifikasi Penilaian Kualitas Link Berbasis Simple Additive Weighting dengan
   Normalisasi Berbatas Acuan Tetap dan Pembobotan Adaptif untuk Alokasi Trafik
   Multi-WAN pada Jaringan Fiber Optik–LEO"*
2. **(Alternatif, komparatif)**
   *"Perbandingan Teknik Normalisasi dan Pembobotan pada Indeks Kualitas Link Berbasis
   SAW serta Dampaknya pada Alokasi PCC di Jaringan Tri-link FO–LEO"*

**Hindari** judul yang memuat "ALQI" atau "Pengembangan sistem kontroler".

---

## 11. Dampak pada Skor Kelayakan

| Aspek | Sebelum B1 | Sesudah B1 | Alasan |
|---|---:|---:|---|
| Kebaruan | 60 | **72** | Positioning tunggal; K-E memulihkan konteks stok/sesi |
| Klaim & etika | 62 | 66 | Daftar "tidak diklaim" tegas |
| **Agregat** | **±70** | **±73** | Masih perlu B2–B6 |

---

## 12. Keputusan yang Menunggu Persetujuan

| # | Keputusan | Pilihan | Rekomendasi |
|---|---|---|---|
| 1 | Lingkup | A / **C** / B | **C** |
| 2 | Judul | Opsi 1 / Opsi 2 | **Opsi 1** |
| 3 | Apakah K-E (bukti alokasi) dimasukkan sebagai kontribusi | Ya / Tidak | **Ya** (penguat, bukan utama) |
| 4 | Istilah "ALQI" | Dihapus total / dipakai + sitasi prior art | **Dihapus dari klaim** |

---

## 13. Checklist B1

- [x] Rekap opsi lingkup A/B/C
- [x] Keputusan D-21 (Varian C) diusulkan
- [x] Pernyataan kebaruan satu paragraf
- [x] Kalimat kebaruan tunggal (slide)
- [x] Novelty statement templat terisi
- [x] Peta kontribusi K-A…K-E
- [x] Daftar "tidak diklaim"
- [ ] **Persetujuan pembimbing** atas Varian C & judul
- [ ] Sinkronisasi `00`, `07`, `08`, `09`, `11`, `17` (§9)
