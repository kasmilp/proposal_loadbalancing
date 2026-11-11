# Evaluasi Tahap 1–3

**Dokumen:** `00_Laporan_Evaluasi.md`
**Tanggal:** 12 November 2026
**Fungsi:** Menilai mutu pekerjaan Tahap 1–3 sebelum masuk Tahap 4.
**Sikap evaluasi:** Kritis, bukan memuji. Tujuannya menemukan masalah sebelum penguji.

---

## 1. Skor Ringkas

| Aspek | Skor | Alasan |
|---|:---:|---|
| Kelengkapan struktur | 5/5 | Gap → RQ → tujuan → hipotesis → teori → uji tersambung |
| Konsistensi istilah | 4/5 | Satu nama payung, tetapi beberapa definisi masih ganda |
| Ketajaman gap | 3/5 | Gap masuk akal, **belum diverifikasi pencarian sistematis** |
| Kekuatan novelty | 3,5/5 | Dua proposisi kuat; sisanya masih integrasi |
| Kualitas bukti/SOTA | 2,5/5 | PCC bertumpu pada jurnal lokal; perlu referensi internasional |
| Keterukuran hipotesis | 3,5/5 | Sudah ada ambang, tetapi H1–H2 dan H3a saling bertabrakan |
| Kelayakan eksekusi | 3/5 | Skenario dan baseline belum dikunci |
| **Rata-rata** | **3,5/5** | **Siap bersyarat untuk Tahap 4** |

**Putusan:** **LANJUT BERSYARAT.** Ada 4 masalah yang harus ditutup sebelum atau
bersamaan dengan Tahap 4. Tidak ada masalah yang membatalkan arah penelitian.

---

## 2. Yang Sudah Kuat

1. **Rantai alinyemen lengkap.** Gap → RQ → tujuan → hipotesis → metrik → uji
   bisa ditelusuri tanpa lompatan. Ini jarang ada di proposal awal.
2. **Lingkup jujur.** MikroTik sebagai adapter, Starlink sebagai *upper bound*,
   bobot SAW statis, dan QoE di luar cakupan — semuanya konsisten.
3. **Dua proposisi teoretis.** Aturan dwell sadar-transien dan frontier trade-off
   memberi tulang punggung yang bukan sekadar integrasi.
4. **SIWG sebagai satu angka.** Memudahkan komunikasi trade-off stabilitas–
   kontinuitas tanpa menambah banyak parameter.
5. **Budaya audit.** Tabel klaim–sumber dan register referensi sudah ada sebelum
   naskah final. Ini yang biasanya baru dibuat saat revisi.

---

## 3. Temuan Kritis

### K-01 — Klaim gap belum diverifikasi

**Lokasi:** `02_Tahap_01_Gap_dan_Novelty/01_Peta_Gap_Penelitian.md` §6;
`04_Tahap_03_Kerangka_Teori/04_Audit_Referensi_dan_Rencana_Pencarian.md` §5.

**Masalah:** Gap masih dinyatakan berdasarkan korpus yang sudah ada (89 berkas),
bukan hasil pencarian sistematis. Kalimat "belum ditemukan studi" belum punya log
pencarian, jumlah hit, dan kriteria eksklusi.

**Dampak:** Penguji dapat mematahkan novelty hanya dengan menunjukkan satu paper
yang terlewat.

**Perbaikan:** Jalankan 7 string pencarian, simpan log, dan perbarui §6 peta gap.
Jangan menulis "belum ada" di naskah sebelum log ini ada.

---

### K-02 — SOTA PCC bertumpu pada jurnal lokal

**Lokasi:** `04_Tahap_03_Kerangka_Teori/01_Draf_Bab_II_Kerangka_Teori.md` §2.4.

**Masalah:** Dari 7 studi PCC yang dipakai, 5–6 berasal dari jurnal/kepanitiaan
lokal (JANAPATI, JISA, E-Komtek, EDUMATIC, IOTA). Hanya Kumar dan Golash (2009)
yang merupakan publikasi internasional. Untuk klaim "state of the art", ini lemah.

**Dampak:** Novelty dan gap bisa dinilai berdiri di atas literatur bereputasi
rendah. Penguji berhak mempertanyakan kualitas pembanding.

**Perbaikan:** Tambah 3–5 referensi internasional tentang *adaptive load
balancing*, *SD-WAN multipath*, atau *MPTCP*. Jurnal lokal tetap dipakai sebagai
**konteks implementasi RT/RW Net**, bukan sebagai SOTA. Lihat
`01_Kebijakan_Tier_Referensi.md`.

---

### K-03 — Ambang H1 dan H2 saling bertabrakan

**Lokasi:** `03_Tahap_02_Rumusan_Masalah/02_Hipotesis_dan_Definisi_Operasional.md`
H1 dan H2.

**Masalah:**
- H1: recovery latency p95 ≤ **60 detik**.
- H2: asimetris boleh lebih lambat **≤ 30 detik** dari simetris.

Jika simetris 50 detik, asimetris 80 detik masih lolos H2 tetapi gagal H1.
Satu skenario bisa "didukung" dan "tidak didukung" sekaligus.

**Perbaikan:** Tetapkan satu batas global, misal $R_{max} = 90$ detik, dipakai H1;
H2 memakai syarat tambahan selisih ≤ 30 detik. Tulis ulang H1: "recovery p95 ≤ 90
detik", bukan 60 detik. Catat perubahan di log keputusan.

---

### K-04 — H3a punya dua kriteria yang bisa saling meniadakan

**Lokasi:** H3a.

**Masalah:** H3a menuntut (a) non-inferior terhadap baseline statis dengan margin
0,5 pp **dan** (b) RST absolut < 1%. Jika baseline statis 1,2%, keduanya tidak
bisa terpenuhi sekaligus meskipun sistem lebih baik.

**Perbaikan:** Tentukan kriteria primer. Rekomendasi:
- **Primer:** non-inferioritas vs baseline (margin +0,5 pp).
- **Sekunder:** RST absolut < 1% sebagai target deskriptif, bukan syarat lulus.
Tulis aturan keputusan eksplisit agar tidak terjadi *post-hoc*.

---

## 4. Temuan Mayor

| ID | Temuan | Lokasi | Perbaikan |
|---|---|---|---|
| M-01 | Jumlah skenario (D-02) belum dikunci; H2 memerlukan C, H4 memerlukan ablasi penuh | Log keputusan | Putuskan 4 atau 6 skenario sebelum Tahap 4 |
| M-02 | Baseline praktisi (D-03) belum dikunci | Log keputusan | Pilih `netwatch` atau weighted ECMP |
| M-03 | SIWG bergantung pada $\lambda$ yang belum dijustifikasi | H4 | Tetapkan $\lambda=1$ sebagai primer + sensitivitas 0,25/0,5/1,0; jelaskan asal asumsi |
| M-04 | 7 klaim berstatus "verifikasi halaman", termasuk angka rain fade dan periode 15 detik | Tabel klaim | Buka PDF dan catat halaman sebelum naskah final |
| M-05 | Bab II §2.1 "Posisi Bab II" bersifat meta, bukan teori | Draf Bab II | Ganti menjadi "Kerangka Umum" atau pindahkan ke pengantar |
| M-06 | Referensi di Bab II (~30) belum dicocokkan satu-satu dengan register (38) | Register | Audit silang sitasi ↔ daftar pustaka |
| M-07 | Klaim C08 (FO oversubscription) bersandar pada satu studi kasus | Tabel klaim | Tambah sumber atau turunkan kekuatan klaim |

---

## 5. Temuan Minor

| ID | Temuan | Perbaikan |
|---|---|---|
| m-01 | "Flapping rate" dan "flap per jam" dipakai bergantian | Definisikan sekali, gunakan konsisten |
| m-02 | "Lima sub-RQ" padahal RQ5 ditandai opsional | Sebut "lima sub-RQ, RQ5 opsional" |
| m-03 | Penomoran "lima hipotesis" sempat tidak sesuai jumlah (6) | Sudah diperbaiki; cek ulang saat menulis Bab I |
| m-04 | Istilah `AFFINITY_LOCK` (kode) dan "affinity lock" (prosa) bercampur | Pakai kode untuk teknis, prosa untuk narasi |
| m-05 | Tabel klaim memakai penanda **[verifikasi]** yang harus hilang di naskah final | Sisakan di dokumen kerja saja |

---

## 6. Evaluasi per Tahap

### Tahap 1 — Gap dan Novelty: 4/5

**Kuat:** pemisahan empat jenis gap; keberanian menyatakan G-I1 tidak cukup
sebagai novelty tunggal; matriks SOTA menunjukkan irisan kosong.

**Lemah:** verifikasi gap belum dijalankan; penilaian ●/◐ pada matriks masih
subjektif; klaim "belum ada" belum didukung log.

### Tahap 2 — Rumusan Masalah dan Hipotesis: 3,5/5

**Kuat:** RQ payung menyebut trade-off, bukan sekadar peningkatan; definisi
operasional flapping/RST/goodput jelas; SIWG sederhana dan dapat diaudit.

**Lemah:** konflik ambang H1–H2; H3a punya dua kriteria primer; H4 bergantung pada
λ; jumlah skenario belum dikunci.

### Tahap 3 — Kerangka Teori: 3/5

**Kuat:** sintesis, bukan ringkasan; dua proposisi; peta konstruk–variabel–hipotesis;
audit referensi sudah menyadari keterbatasan korpus.

**Lemah:** kualitas venue PCC; 7 klaim belum diverifikasi; literatur MPTCP dan
SD-WAN multipath belum ada; Bab II masih berupa draf, belum siap masuk naskah.

### Manajemen: 4/5

**Kuat:** roadmap, log keputusan, dan status jelas.

**Lemah:** D-02, D-03, D-05, D-06 belum dikunci; D-10 (gaya sitasi) belum
dikonfirmasi ke pedoman kampus.

---

## 7. Gerbang Sebelum Tahap 4

**Wajib (blocking):**
- [ ] K-03 diperbaiki: satu batas recovery global.
- [ ] K-04 diperbaiki: kriteria primer H3a ditetapkan.
- [ ] D-02 dikunci: 4 atau 6 skenario.
- [ ] D-03 dikunci: baseline praktisi.

**Dapat paralel dengan Tahap 4:**
- [ ] K-01: jalankan log pencarian.
- [ ] K-02: tambah 3–5 referensi internasional.
- [ ] M-04: verifikasi 7 klaim.
- [ ] M-06: audit silang sitasi.

**Tidak menghalangi Tahap 4, tetapi harus sebelum seminar:**
- [ ] M-05, m-01–m-05.
- [ ] D-10: konfirmasi gaya sitasi.

---

## 8. Rekomendasi Strategis

1. **Jangan menambah teori baru.** Yang kurang bukan teori, melainkan bukti
   kualitas referensi dan konsistensi ambang.
2. **Pindahkan jurnal lokal ke peran konteks.** Mereka berharga untuk menunjukkan
   realitas RT/RW Net, bukan untuk mengklaim state of the art.
3. **Perbaiki ambang sekarang.** Setelah data diambil, ambang tidak boleh diubah.
4. **Kunci skenario sekarang.** Ini menentukan bentuk Bab III dan beban kerja.
5. **Sisakan waktu untuk verifikasi halaman.** Ini pekerjaan membosankan yang
   paling sering menunda seminar.

---

## 9. Kesimpulan

Pekerjaan Tahap 1–3 sudah cukup untuk masuk Tahap 4 **setelah empat perbaikan
wajib**. Kekuatan utamanya adalah alinyemen dan kejujuran lingkup. Kelemahan
utamanya bukan ide, melainkan **kualitas bukti** dan **konsistensi ambang**.
Keduanya dapat diperbaiki tanpa mengubah arah penelitian.
