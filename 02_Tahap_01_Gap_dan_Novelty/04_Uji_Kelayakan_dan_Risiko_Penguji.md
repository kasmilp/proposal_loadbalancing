# Tahap 1 — Uji Kelayakan dan Risiko Penguji

**Dokumen:** `04_Uji_Kelayakan_dan_Risiko_Penguji.md`
**Status:** Draf kerja Tahap 1
**Fungsi:** Menguji apakah novelty layak dan menyiapkan jawaban atas keberatan penguji.

---

## 1. Lima Uji Kelayakan Novelty

| Uji | Pertanyaan | Hasil | Catatan |
|---|---|---|---|
| **U1 — Pembeda** | Apa yang berbeda dari studi terdekat? | Lulus | Beda pada aturan dwell sadar-transien + pengukuran RST, bukan pada metode dasar |
| **U2 — Falsifiabilitas** | Hasil seperti apa yang akan membuktikan klaim ini salah? | Lulus | Jika RST dengan affinity tidak lebih rendah, atau flapping tidak turun, klaim gugur |
| **U3 — Ketersediaan bukti** | Apakah data untuk membuktikan tersedia? | Sebagian | Perlu pilot untuk memastikan telemetri Starlink dan akses lokasi |
| **U4 — Kelayakan waktu** | Apakah selesai dalam 4–6 bulan? | Lulus bersyarat | Bergantung jumlah skenario; minimum A, B, D, F |
| **U5 — Etika dan keselamatan** | Apakah aman pada jaringan produksi? | Lulus bersyarat | Perlu izin, fail-static, rollback, jam rendah risiko |

**Putusan:** **GO bersyarat**. Dua syarat yang harus dipenuhi sebelum Tahap 4:
1. pilot 24–48 jam membuktikan instrumen dan mekanisme RST dapat diukur;
2. jumlah skenario dikunci agar jadwal realistis.

---

## 2. Dua Belas Keberatan Penguji dan Jawaban

### Keberatan 1 — "Ini hanya integrasi metode yang sudah ada."

**Jawaban.** Betul bahwa metode dasarnya bukan hal baru, dan proposal tidak
mengklaim itu. Kontribusi yang diklaim adalah (a) aturan penurunan parameter
histeresis dari durasi transien LEO, dan (b) bukti ablasi yang memisahkan
flapping dari gangguan sesi. Keduanya belum tersedia di literatur. Jika penguji
tetap menilai kurang, Opsi A (batas analitis flapping) disiapkan sebagai penguatan.

---

### Keberatan 2 — "Mengapa harus histeresis? Mengapa bukan kontrol PID atau pembelajaran?"

**Jawaban.** Tiga alasan: (1) histeresis hanya membutuhkan dua ambang dan satu
counter, sehingga cocok untuk perangkat kelas SOHO dan siklus detik; (2) perilakunya
dapat dijelaskan dan diaudit, berbeda dari model *black-box*; (3) literatur
menunjukkan ambang ganda cukup untuk mencegah osilasi pada sistem berkapasitas
adaptif (Tournaire et al., 2023). Pembelajaran mesin tidak dikecualikan sebagai
pengembangan lanjutan, tetapi menambah kebutuhan data dan komputasi yang berada di
luar lingkup.

---

### Keberatan 3 — "Kalau PCC sudah menjaga sesi, apa gunanya affinity lock?"

**Jawaban.** Itu justru hipotesis yang diuji, bukan asumsi. Jika PCC memang sudah
menjaga sesi, H2a akan menunjukkan non-inferioritas, dan itu tetap merupakan
kontribusi: klaim praktisi menjadi terverifikasi. Yang tidak boleh terjadi adalah
mengklaim manfaat tanpa mengukur.

---

### Keberatan 4 — "Skenario tanpa affinity dibuat gagal secara sengaja."

**Jawaban.** Perlakuan "tanpa affinity" didefinisikan teknis sebagai *selective
conntrack flush* setelah aturan baru diterapkan, dan risiko perlakuannya dijelaskan.
Uji pilot akan membandingkan dua varian tanpa affinity (tanpa flush dan dengan flush)
agar efek perlakuan dapat dipisahkan dari efek kebetulan.

---

### Keberatan 5 — "Empat skenario terlalu sedikit / terlalu banyak."

**Jawaban.** Desain minimum A, B, D, F sudah cukup untuk mengisolasi:
B→D mengubah bentuk histeresis; D→F mengubah affinity. Dengan keputusan
6 skenario (A–F), desain yang dipakai adalah **faktorial 2×2** (simetris/asimetris
× affinity off/on) ditambah **dua pembanding** (A statis dan B dynamic naive) serta
**satu baseline praktisi** (G). Interaksi "tanpa histeresis × affinity" tidak diuji;
ini diakui sebagai keterbatasan, bukan diklaim sebagai faktorial penuh 3×2.

---

### Keberatan 6 — "Kenapa Starlink? Kenapa tidak 4G/5G saja?"

**Jawaban.** Starlink dipilih karena transiennya paling ekstrem dan terukur
(~15 detik), sehingga menjadi *upper bound* untuk pengujian. Jika mekanisme mampu
menstabilkan link dengan transien tercepat, ia memiliki margin untuk link yang
lebih lambat. Generalisasi ke 4G/5G tidak diklaim, tetapi diuji sebagai arah lanjutan.

---

### Keberatan 7 — "Data lapangan terlalu bising; hasil tidak valid."

**Jawaban.** Evaluasi kausal utama dilakukan di staging dengan *trace replay* dan
`tc netem`, sehingga kondisi dapat dikendalikan dan diulang. Lapangan dipakai
sebagai validasi eksternal, bukan satu-satunya sumber inferensi kausal. Urutan run
diacak/counterbalanced dan diblok berdasarkan jam dan cuaca.

---

### Keberatan 8 — "Mengapa memakai t-test?"

**Jawaban.** Tidak memakai t-test sebagai default. Data deret waktu berkorelasi,
flapping adalah data cacat, dan unit analisisnya episode/jam. Rencana: mixed-effects
atau GEE untuk data berulang, Poisson/negative binomial untuk flapping,
ANOVA/Kruskal–Wallis + post hoc untuk perbandingan antar-skenario, dan bootstrap
untuk distribusi non-normal. Setiap hasil disertai effect size dan 95% CI.

---

### Keberatan 9 — "Klaim portabilitas tidak didukung."

**Jawaban.** Klaim yang diajukan adalah "dirancang portabel dan diuji melalui
kontrak antarmuka", bukan "terbukti portabel di semua vendor". Bukti yang
disediakan: spesifikasi antarmuka, mock adapter, dan perbandingan keputusan pada
dua adapter. Generalisasi multi-vendor dinyatakan sebagai keterbatasan.

---

### Keberatan 10 — "Mengapa bobot SAW statis? Bukankah itu tidak adaptif?"

**Jawaban.** "Adaptif" merujuk pada rasio alokasi, bukan pada pembelajaran bobot.
Bobot statis dipilih agar keputusan dapat diaudit dan hasil dapat direplikasi.
Protokol kalibrasi dan analisis sensitivitas disediakan; pembelajaran bobot
dinyatakan di luar lingkup.

---

### Keberatan 11 — "Apa dampak praktisnya bagi RT/RW Net?"

**Jawaban.** Tiga dampak: (1) panduan parameter yang dapat dipakai ulang;
(2) mekanisme yang tetap kembali ke konfigurasi statis saat controller gagal;
(3) artefak yang dapat direplikasi tanpa lisensi proprietary. Klaim dampak
ekonomi tidak dibuat karena tidak diukur.

---

### Keberatan 12 — "Apa yang terjadi jika controller mati?"

**Jawaban.** Sistem memakai *fail-static*: konfigurasi terakhir yang valid tetap
berlaku, watchdog memantau koneksi, dan prosedur rollback diuji sebelum run.
Skenario kegagalan controller dimasukkan sebagai bagian dari manajemen risiko,
bukan diabaikan.

---

## 3. Kriteria Go / No-Go

| Kriteria | Ambang | Status |
|---|---|---|
| Gap utama dapat dinyatakan dalam satu paragraf | Ya | Terpenuhi |
| Novelty punya minimal satu kontribusi non-integrasi | Ya | Terpenuhi (N2, N3) |
| Ada pembanding eksplisit | Ya | Terpenuhi |
| Instrumen RST dapat diuji | Pilot 24–48 jam | Belum |
| Akses lokasi dan izin | Tertulis | Belum |
| Jumlah skenario realistis | ≤ 6 atau minimum 4 | Belum diputuskan |
| Pembimbing menyetujui arah | Ya | Belum |

**Status keseluruhan:** **GO bersyarat** — lanjut ke Tahap 2, sambil menutup tiga
syarat yang belum.

---

## 4. Keputusan yang Dibutuhkan Sebelum Tahap 2

1. **Arah topik:** lanjut SPA-HSM, atau pertajam menjadi salah satu varian
   (lihat `01_Log_Keputusan.md`).
2. **Jumlah skenario:** 6 (A–F) atau minimum 4 (A, B, D, F).
3. **Penguatan novelty:** ambil Opsi B (metrik gabungan) sekarang, atau tunda.
4. **Baseline praktisi:** netwatch failover, weighted ECMP, atau keduanya.
5. **Telemetri Starlink:** apakah data dish tersedia dan diizinkan.
6. **Lokasi dan izin:** apakah lokasi RT/RW Net yang sama masih dapat diakses.

Keputusan ini dicatat di `01_Manajemen_Proposal/01_Log_Keputusan.md` agar tidak
berubah tanpa jejak.
