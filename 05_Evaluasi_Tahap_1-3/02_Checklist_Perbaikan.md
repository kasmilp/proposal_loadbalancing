# Checklist Perbaikan Sebelum Tahap 4

**Dokumen:** `02_Checklist_Perbaikan.md`
**Fungsi:** Daftar kerja yang dapat dicentang, bukan sekadar catatan.
**Aturan:** Tahap 4 baru dimulai setelah semua item **BLOCKING** selesai.
**Status 12-11-2026:** B-01 s.d. B-04 selesai. P-01 s.d. P-05 dikerjakan paralel
dengan Tahap 4.

---

## A. BLOCKING — harus selesai sebelum Tahap 4

### [x] B-01 — Satukan ambang recovery latency

**Masalah:** H1 menetapkan ≤ 60 detik; H2 mengizinkan +30 detik dari simetris.
Dua ambang ini dapat bertabrakan.

**Langkah:**
1. Tetapkan satu batas global $R_{max} = 90$ detik (atau nilai lain yang disetujui).
2. Ubah H1: "recovery latency p95 ≤ 90 detik".
3. Ubah H2: "selisih recovery latency p95 asimetris−simetris ≤ 30 detik **dan**
   keduanya ≤ 90 detik".
4. Catat perubahan di `01_Manajemen_Proposal/01_Log_Keputusan.md`.

**Kriteria selesai:** tidak ada dua ambang recovery yang saling bertentangan di
dokumen Tahap 2 dan Tahap 3.

**Perkiraan:** 30 menit.

---

### [x] B-02 — Tetapkan kriteria primer H3a

**Masalah:** H3a menuntut non-inferioritas **dan** RST absolut < 1%; keduanya bisa
saling meniadakan.

**Langkah:**
1. Tetapkan **kriteria primer**: non-inferioritas vs baseline statis, margin +0,5 pp.
2. Tetapkan **kriteria sekunder**: RST absolut < 1% sebagai target deskriptif.
3. Tulis aturan keputusan: jika primer lolos tetapi sekunder gagal, hasil disebut
   "non-inferior, target absolut belum tercapai".
4. Perbarui H3a dan tabel keputusan.

**Kriteria selesai:** satu hipotesis tidak lagi memiliki dua syarat lulus yang
setara.

**Perkiraan:** 30 menit.

---

### [x] B-03 — Kunci jumlah skenario (D-02)

**Pilihan:**

| Opsi | Skenario | Konsekuensi |
|---|---|---|
| Minimum | A, B, D, F | H2 hanya bukti parsial; H4 tetap bisa |
| Penuh | A–F | H2 dan H4 penuh; waktu dan data ±50% lebih banyak |

**Rekomendasi:** **A–F** jika akses lokasi dan waktu memungkinkan; jika tidak,
**A, B, D, F** dengan catatan keterbatasan H2.

**Langkah:**
1. Konsultasikan dengan pembimbing.
2. Catat keputusan dan alasannya di log.
3. Sesuaikan jadwal Tahap 4.

**Kriteria selesai:** satu jumlah skenario dikunci dan tidak berubah saat analisis.

---

### [x] B-04 — Kunci baseline praktisi (D-03)

**Pilihan:** `netwatch` failover / weighted ECMP / keduanya.

**Rekomendasi:** `netwatch` failover, karena paling dekat dengan praktik RT/RW Net
dan tersedia di RouterOS.

**Langkah:**
1. Tentukan konfigurasi baseline (rasio, probe, ambang failover).
2. Dokumentasikan agar dapat direplikasi.
3. Catat di log.

**Kriteria selesai:** baseline punya konfigurasi tertulis dan alasan pemilihan.

---

## B. PARALEL — dikerjakan bersamaan dengan Tahap 4

### [ ] P-01 — Jalankan log pencarian gap (K-01)

**Langkah:**
1. Jalankan string S1–S7 di `04_Tahap_03_Kerangka_Teori/04_Audit_Referensi_dan_Rencana_Pencarian.md`.
2. Catat tanggal, basis data, string, jumlah hit, jumlah lolos.
3. Simpan tangkapan layar atau ekspor CSV.
4. Perbarui §6 peta gap dengan hasil.

**Kriteria selesai:** klaim "belum ditemukan" punya log yang dapat ditunjukkan.

**Perkiraan:** 1–2 hari.

---

### [ ] P-02 — Tambah 3–5 referensi internasional PCC/adaptive LB (K-02)

**Target topik:**
- adaptive/dynamic load balancing pada multi-WAN
- SD-WAN multipath atau traffic steering
- policy-based routing dengan umpan balik kualitas

**Kriteria selesai:** komponen PCC memiliki minimal 3 referensi T1, bukan 1.

**Perkiraan:** 1 hari.

---

### [ ] P-03 — Tambah 4 referensi kontinuitas sesi/MPTCP (D-13)

**Target topik:**
- MPTCP dan connection migration
- session continuity pada multi-homing
- dampak perubahan jalur terhadap TCP

**Kriteria selesai:** H3a punya landasan teori, bukan hanya dokumentasi vendor.

**Perkiraan:** 1 hari.

---

### [ ] P-04 — Verifikasi 7 klaim berstatus "halaman" (M-04)

**Daftar:**
- C08 — oversubscription FO
- C11 — periode 15 detik
- C12 — pola throughput edge router
- C14 — angka 137→90 Mbps dan 20,9→10,5 Mbps
- C33 — overhead cloud LB
- C34 — beban ANN hub
- C37 — QoS vs QoE

**Kriteria selesai:** setiap klaim punya nomor halaman atau diturunkan kekuatannya.

**Perkiraan:** 4–6 jam.

---

### [ ] P-05 — Audit silang sitasi ↔ daftar pustaka (M-06)

**Langkah:**
1. Ekstrak semua sitasi dari Bab II.
2. Cocokkan dengan `05_Register_Referensi.csv`.
3. Tandai sitasi tanpa entri dan entri tanpa sitasi.

**Kriteria selesai:** tidak ada sitasi yatim atau referensi menganggur.

**Perkiraan:** 2 jam.

---

## C. PEMBERSIHAN — sebelum naskah final

| ID | Item | Tindakan | Status |
|---|---|---|---|
| C-01 | §2.1 "Posisi Bab II" bersifat meta | Ganti menjadi "Kerangka Umum" | [ ] |
| C-02 | "Flapping rate" vs "flap per jam" | Definisikan sekali di 2.7, gunakan konsisten | [ ] |
| C-03 | RQ5 ditandai opsional | Tulis "lima sub-RQ, RQ5 opsional" di semua tempat | [ ] |
| C-04 | `AFFINITY_LOCK` vs "affinity lock" | Kode untuk teknis, prosa untuk narasi | [ ] |
| C-05 | Penanda **[verifikasi]** | Hanya di dokumen kerja, hilang di naskah | [ ] |
| C-06 | Gaya sitasi (D-10) | Konfirmasi manual ke pedoman kampus | [ ] |
| C-07 | Referensi T3 | Pastikan hanya dipakai untuk konteks | [ ] |

---

## D. PEMBARUAN DOKUMEN

- [ ] `01_Manajemen_Proposal/01_Log_Keputusan.md`: catat B-01 s.d. B-04.
- [ ] `03_Tahap_02_Rumusan_Masalah/02_Hipotesis_dan_Definisi_Operasional.md`: perbarui H1, H2, H3a.
- [ ] `05_Evaluasi_Tahap_1-3/01_Kebijakan_Tier_Referensi.md`: perbarui jumlah setelah P-02/P-03.
- [ ] `README.md`: status Tahap 4 setelah dimulai.

---

## E. Definisi Selesai Evaluasi

Evaluasi dianggap selesai jika:

- [ ] Tidak ada ambang yang bertabrakan.
- [ ] Jumlah skenario dan baseline dikunci.
- [ ] Log pencarian gap tersedia.
- [ ] Komponen PCC punya minimal 3 referensi T1.
- [ ] Kontinuitas sesi punya minimal 4 referensi.
- [ ] 7 klaim berstatus "halaman" sudah diverifikasi atau diturunkan.
- [ ] Semua keputusan tercatat di log.

---

## F. Urutan Eksekusi yang Disarankan

```
Hari 1  : B-01, B-02 (perbaikan ambang)          → 1 jam
Hari 1  : B-03, B-04 (keputusan skenario)        → diskusi pembimbing
Hari 2  : P-03 (MPTCP) + P-02 (PCC internasional) → 1 hari
Hari 3  : P-01 (log pencarian)                    → 1 hari
Hari 4  : P-04 (verifikasi klaim)                 → setengah hari
Hari 5  : P-05 (audit silang) + C-01 s.d. C-07    → setengah hari
Hari 6  : Tahap 4 dimulai
```

Jika waktu sangat terbatas: kerjakan **B-01, B-02, B-03, B-04** lebih dulu,
lalu mulai Tahap 4 sambil mengerjakan P-01 s.d. P-05 secara paralel.
