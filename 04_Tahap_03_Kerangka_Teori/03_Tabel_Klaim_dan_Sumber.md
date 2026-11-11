# Tahap 3 — Tabel Klaim dan Sumber

**Dokumen:** `03_Tabel_Klaim_dan_Sumber.md`
**Fungsi:** Audit setiap klaim faktual di Bab II: dari mana sumbernya, sekuat apa,
dan apa yang masih harus diverifikasi.
**Aturan:** Tidak ada klaim di naskah yang tidak muncul di tabel ini.

**Legenda status**
- **Siap** — sumber ada di korpus, metadata lengkap, klaim umum.
- **Verifikasi halaman** — sumber ada, tetapi angka/kutipan spesifik harus dicek.
- **Perlu sumber** — belum ada sumber yang memadai; jangan dipakai dulu.
- **Desain** — klaim penelitian ini, bukan klaim literatur.

---

## 1. Tabel Klaim

| ID | Klaim | Sumber | Jenis bukti | Kekuatan | Status | Tindakan |
|---|---|---|---|---|---|---|
| C01 | QoS direpresentasikan oleh delay, jitter, loss, throughput | Nanang et al. (2024) | Studi empiris/standar | Sedang | Siap | — |
| C02 | TIPHON mengklasifikasikan kualitas layanan | ETSI (2000) | Standar | Kuat | Siap | — |
| C03 | G.114 menetapkan batas one-way delay layanan interaktif | ITU-T (2003) | Standar | Kuat | Siap | Catat nilai batas yang dipakai |
| C04 | Y.1541 menetapkan objektif performa IP | ITU-T (2011) | Standar | Kuat | Siap | Catat kelas yang dipakai |
| C05 | RFC 2330 menyediakan kerangka metrik performa IP | Paxson et al. (1998) | Standar | Kuat | Siap | — |
| C06 | RFC 2544 menetapkan metodologi benchmarking | Bradner & McQuaid (1999) | Standar | Kuat | Siap | — |
| C07 | RFC 3550 mendefinisikan estimasi jitter | Schulzrinne et al. (2003) | Standar | Kuat | Siap | Tulis rumus yang dipakai |
| C08 | Kualitas FO dapat turun karena oversubscription/contention | Studi IndiHome GPON di korpus | Studi kasus | Sedang | Verifikasi halaman | Cek angka dan konteks |
| C09 | Starlink LEO ~550 km, latensi lebih rendah dari GEO, handover periodik | Ma et al. (2023); Mohan et al. (2024) | Pengukuran | Kuat | Siap | — |
| C10 | Starlink memiliki variabilitas dan outage lebih tinggi dari jaringan terestrial | Ma et al. (2023); Mohan et al. (2024) | Pengukuran | Kuat | Siap | — |
| C11 | Terdapat pola periodik sekitar 15 detik pada one-way delay | Garcia et al. (2025) | Pengukuran | Sedang–kuat | Verifikasi halaman | Cek durasi, arah, dan kondisi |
| C12 | Pola penurunan throughput berulang teramati pada edge router | Hammer et al. (2024); Mohan et al. (2024) | Pengukuran | Sedang–kuat | Verifikasi halaman | Cek apakah 15 detik eksplisit |
| C13 | Hujan menurunkan throughput Starlink | Boeckenholt et al. (2024); Ullah et al. (2025) | Pengukuran | Kuat | Siap | — |
| C14 | Angka 137→90 Mbps (downlink) dan 20,9→10,5 Mbps (uplink) saat hujan | Ullah et al. (2025) | Pengukuran | Sedang | Verifikasi halaman | **Wajib cek tabel asli** |
| C15 | PCC memakai mangle connection mark dan routing mark | MikroTik (n.d.) | Dokumentasi vendor | Kuat | Siap | Sertakan URL dan tanggal akses |
| C16 | PCC menjaga konsistensi sesi per koneksi | Kumar & Golash (2009); MikroTik (n.d.) | Konsep/dokumentasi | Kuat | Siap | — |
| C17 | PCC lebih stabil dari ECMP/NTH pada trafik stateful | Nugroho et al. (2023); Mirsal & Agtriadi (2026) | Studi komparatif | Sedang | Siap | Catat metodologi dan batasan |
| C18 | PCC pada dua/tiga ISP meningkatkan skor QoS | Amalia et al. (2022); Arfianita et al. (2024) | Studi empiris | Sedang | Siap | Sebutkan metrik dan angka |
| C19 | Studi PCC yang ada memakai rasio statis | Amalia et al. (2022); Arfianita et al. (2024); Nugroho et al. (2023); Putra & Anton (2024); Mirsal & Agtriadi (2026) | Sintesis | Kuat | Siap | Pastikan tidak ada studi adaptif yang terlewat |
| C20 | PCC + failover mengurangi dampak gangguan ISP | Putra & Anton (2024) | Studi lapangan | Sedang | Siap | — |
| C21 | SAW adalah penjumlahan linier berbobot | Wang & Kuo (2013); Vafaei et al. (2021) | Metode | Kuat | Siap | — |
| C22 | Teknik normalisasi memengaruhi peringkat SAW | Vafaei et al. (2021) | Eksperimen metode | Kuat | Siap | — |
| C23 | Normalisasi berbatas tetap menjaga komparabilitas antar-waktu | Penalaran desain + Vafaei et al. (2021) | Argumen | Sedang | Desain | Nyatakan sebagai pilihan desain, bukan temuan |
| C24 | EWMA dirumuskan $E_t = \alpha x_t + (1-\alpha)E_{t-1}$ | Roberts (1959) | Metode | Kuat | Siap | — |
| C25 | Effective window EWMA sekitar $2/\alpha - 1$ | Turunan dari formulasi EWMA | Matematis | Kuat | Desain | Tunjukkan turunannya di lampiran |
| C26 | Dua ambang mencegah osilasi keputusan | Tournaire et al. (2023) | Analisis/eksperimen | Kuat | Siap | — |
| C27 | Histeresis handover menyeimbangkan unnecessary handover dan failure | Alhabo et al. (2017) | Studi analitis | Kuat | Siap | — |
| C28 | Koneksi established mempertahankan connection mark | MikroTik (n.d.) | Dokumentasi vendor | Kuat | Siap | Uji di pilot, jangan hanya dokumentasi |
| C29 | TCP RST muncul saat state tidak konsisten | Eddy (2022) | Standar | Kuat | Siap | — |
| C30 | Selective conntrack flush adalah perlakuan "tanpa affinity" | Keputusan desain | Desain | — | Desain | Jelaskan risiko dan justifikasinya |
| C31 | Controller eksternal dapat menyuntikkan kebijakan ke perangkat | Ali et al. (2025); Wang & Kuo (2013) | Arsitektur | Sedang–kuat | Siap | — |
| C32 | Pola adapter memisahkan inti dari implementasi | Gamma et al. (1994) | Buku | Kuat | Siap | — |
| C33 | Load balancing cloud berbasis metaheuristik berbiaya komputasi tinggi | Komathi et al. (2024); Lilhore et al. (2025) | Studi | Sedang | Verifikasi halaman | Cek klaim overhead |
| C34 | Hub multi-ISP berbasis ANN membutuhkan komputasi berat | Ali et al. (2025) | Studi | Sedang | Verifikasi halaman | Jangan menyederhanakan berlebihan |
| C35 | SIWG = $G_{eff}(1-\lambda \cdot RST_{flow})$ | Definisi penelitian ini | Desain | — | Desain | Nyatakan sebagai metrik internal |
| C36 | Aturan $k_{down} T_s > T_{tr}+m$ mencegah flapping akibat transien | Proposisi 1 penelitian ini | Desain/analitis | Sedang | Desain | Uji dengan replay; jangan sebut teorema |
| C37 | QoS dan QoE adalah konsep berbeda | Literatur QoE di korpus | Konsep | Kuat | Verifikasi halaman | Pilih satu sumber QoE yang jelas |

---

## 2. Ringkasan Status

| Status | Jumlah | Tindakan |
|---|---:|---|
| Siap | 25 | Bisa langsung dipakai |
| Verifikasi halaman | 7 | Cek PDF dan catat halaman |
| Perlu sumber | 0 | — |
| Desain | 5 | Nyatakan sebagai klaim penelitian, bukan literatur |
| **Total** | **37** | |

---

## 3. Lima Klaim Paling Berisiko

Urutan berdasarkan dampak jika salah:

1. **C14 — angka rain fade 137→90 Mbps.** Jika angka berbeda, kredibilitas
   seluruh latar belakang turun. Wajib buka tabel asli Ullah et al. (2025).
2. **C11 — periode 15 detik.** Ini dasar Proposisi 1. Jika yang dimaksud 15 detik
   adalah interval *handover* dan bukan periodisitas delay, aturan dwell harus
   dirumuskan ulang.
3. **C19 — "semua studi PCC memakai rasio statis".** Jika ada satu studi adaptif
   yang terlewat, klaim gap runtuh. Jalankan pencarian di
   `04_Audit_Referensi_dan_Rencana_Pencarian.md`.
4. **C28 — conntrack mempertahankan mark.** Dokumentasi vendor bukan bukti empiris.
   Uji pada pilot dan laporkan hasilnya.
5. **C17 — PCC lebih stabil dari ECMP/NTH.** Bergantung pada beban dan metodologi;
   jangan generalisasi ke semua kondisi.

---

## 4. Aturan Penulisan Klaim

| Situasi | Kalimat yang benar | Kalimat yang salah |
|---|---|---|
| Sumber kuat | "PCC mempertahankan mark per koneksi (MikroTik, n.d.)." | "PCC selalu menjaga sesi." |
| Sumber sedang | "Studi X melaporkan penurunan throughput ..." | "Starlink selalu turun saat hujan." |
| Angka belum dicek | "sekitar 15 detik **[verifikasi]**" | "tepat 15 detik" |
| Klaim sendiri | "Penelitian ini merumuskan ..." | "Telah terbukti bahwa ..." |
| Gap | "Belum ditemukan studi yang ..." | "Belum ada penelitian di dunia." |

---

## 5. Yang Harus Dilakukan Sebelum Naskah Final

- [ ] Buka 9 PDF berstatus "Verifikasi halaman" dan catat nomor halaman.
- [ ] Perbarui tabel ini dengan halaman/DOI.
- [ ] Hapus penanda **[verifikasi]** dari Bab II setelah dicek.
- [ ] Pastikan setiap sitasi di Bab II ada di daftar rujukan, dan sebaliknya.
- [ ] Jalankan pemeriksaan silang otomatis (sitasi ↔ daftar pustaka).
