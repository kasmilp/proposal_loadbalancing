# Matriks Keputusan Topologi: Dual-ISP vs Tri-ISP

**Status:** Menunggu data baseline
**Konteks:** Tersedia tiga ISP: ISP-A Starlink, ISP-B Starlink, ISP-C FO.
**Keputusan yang harus diambil:** topologi formal untuk eksperimen tesis.

---

## 1. Pilihan

### Opsi 1 — Dual-ISP formal (ISP-A + ISP-C)

- ISP-B dimonitor sebagai **kontrol eksternal** dan cadangan, tidak masuk klaim.
- Sesuai dengan keputusan K-01 dan seluruh Bab I–III yang sudah disusun.
- Tidak perlu menulis ulang lingkup, skenario, atau hipotesis.

### Opsi 2 — Tri-ISP formal (ISP-A + ISP-B + ISP-C)

- Dua LEO + satu FO; klaim diperluas menjadi WAN multi-ISP heterogen.
- Novelty konteks lebih tinggi, tetapi desain, skenario, dan analisis harus direvisi.
- Membutuhkan justifikasi bahwa dua Starlink memberikan informasi yang tidak
  redundan (independensi transien).

### Opsi 3 — Dual-ISP formal + Tri-ISP sebagai validasi eksternal

- Eksperimen utama: A + C (sesuai proposal).
- Validasi: ulangi subset skenario pada A + B + C untuk melihat apakah arah efek
  bertahan.
- Klaim utama tetap dual-ISP; tri-ISP dilaporkan sebagai robustness check.

---

## 2. Perbandingan

| Aspek | Dual-ISP (A+C) | Tri-ISP (A+B+C) |
|---|---|---|
| Kesesuaian dengan proposal sekarang | **Tinggi** | Rendah; perlu revisi besar |
| Kekuatan novelty konteks | Sedang | **Tinggi** |
| Kompleksitas state machine | 2 link, 4 kombinasi state | 3 link, 8 kombinasi state |
| Tabel rasio | Sederhana | Perlu tabel 8 state |
| Bucket mapping | 2 link, mudah | 3 link, perlu batas baru |
| Jumlah skenario | 6 + G | 6 + G (tetapi perbandingan lebih kaya) |
| Ukuran sampel | 30 episode/kondisi | 30 episode/kondisi, tetapi lebih mahal |
| Waktu kampanye | 6 minggu | 8–10 minggu |
| Risiko data | Sedang | Tinggi |
| Klaim generalisasi | Terbatas dual-ISP | Lebih luas, tetapi harus dibuktikan |
| Beban analisis | Sedang | Tinggi |
| Kesesuaian dengan akun read-only | Baik untuk baseline | Baik untuk baseline |

---

## 3. Dampak Jika Memilih Tri-ISP

Jika tri-ISP dipilih, hal-hal berikut **wajib** direvisi:

1. **K-01** di log keputusan: dari dual-ISP menjadi tri-ISP.
2. **Judul dan Bab I**: "dual-ISP" menjadi "multi-ISP" atau "tri-ISP".
3. **Batasan**: klaim generalisasi berubah; satu FO + dua LEO bukan semua WAN.
4. **State machine**: 3 link, 8 kombinasi state; tabel rasio diperluas.
5. **Bucket mapping**: $N=20$ dibagi tiga link; tetapkan $b_{min}$ dan $b_{max}$
   baru (mis. 2 dan 14) dan uji kelayakan.
6. **Skenario**: A–G tetap, tetapi baseline G harus menangani tiga WAN.
7. **Hipotesis**: semua frasa "dual-ISP" diganti; H2/H3a dibandingkan pada tiga link.
8. **Ukuran sampel**: episode per kondisi tetap, tetapi kampanye lebih panjang.
9. **Analisis**: model harus mengakomodasi tiga link dan korelasi antar-LEO.
10. **Etika/risiko**: dua Starlink berarti dua titik gangguan dan dua set telemetri.

---

## 4. Dampak Jika Memilih Dual-ISP

1. ISP-B tetap dimonitor, tetapi **tidak** masuk klaim formal.
2. Jelaskan di batasan: "ISP-B tidak diuji sebagai bagian dari perlakuan; hanya
   digunakan sebagai pembanding konteks/cadangan."
3. Tidak ada perubahan besar pada Bab I–III.
4. Waktu dan risiko lebih terkendali.
5. Tri-ISP dapat diusulkan sebagai **penelitian lanjutan**, bukan klaim tesis.

---

## 5. Rekomendasi

**Rekomendasi utama: Opsi 3.**

- Eksperimen formal tetap **dual-ISP A+C** agar proposal tidak perlu ditulis ulang.
- ISP-B dimonitor sejak baseline dan dipakai untuk **validasi eksternal** pada
  subset skenario.
- Jika baseline menunjukkan dua Starlink **independen** dan waktu mencukupi,
  tri-ISP dapat dinaikkan menjadi kontribusi tambahan — tetapi keputusan itu
  diambil setelah data, bukan sekarang.

**Alasan:** novelty tesis saat ini sudah bertumpu pada aturan *dwell*, pemetaan
bucket, dan SIWG, bukan pada jumlah ISP. Menambah ISP menaikkan kompleksitas
tanpa otomatis menaikkan kualitas klaim.

---

## 6. Gerbang Keputusan Setelah Baseline

| Kriteria | Ambang | Keputusan |
|---|---|---|
| Korelasi transien A–B | < 0,7 | Tri-ISP informatif |
| Episode total/hari | ≥ 5 | Data cukup |
| API stabil | ≥ 99% | Layak |
| Waktu tersedia | ≥ 16 minggu | Tri-ISP realistis |
| Risiko operasional | Rendah–sedang | Layak |

Jika salah satu gagal, pilih **dual-ISP** dan laporkan ISP-B sebagai konteks.

---

## 7. Yang Harus Dicatat

- [ ] Jalankan baseline read-only 7–14 hari pada tiga ISP.
- [ ] Hitung korelasi transien A–B.
- [ ] Hitung frekuensi episode per ISP.
- [ ] Nilai stabilitas API dan kelengkapan data.
- [ ] Putuskan Opsi 1/2/3 di log keputusan.
- [ ] Perbarui Bab I–III hanya setelah keputusan.
