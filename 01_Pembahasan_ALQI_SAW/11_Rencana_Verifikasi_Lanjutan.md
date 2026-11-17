# 11 — Rencana Verifikasi Lanjutan

**Status:** Daftar kerja (belum dikerjakan)
**Fungsi:** Mencatat pekerjaan literatur dan teknis yang harus diselesaikan sebelum
klaim kebaruan ditulis di Bab I/II.

**Aturan [USULAN]:** klaim "belum ada" hanya boleh ditulis sebagai **"berdasarkan
pencarian pada [basis data] pada [tanggal], belum ditemukan …"**.

---

## 1. Verifikasi Literatur (prioritas tinggi)

| Kode | Pekerjaan | Tujuan | Status |
|---|---|---|---|
| V-1 | Jalankan pencarian di **Scopus, IEEE Xplore, ACM DL, ScienceDirect** (bukan hanya OpenAlex) | Menutup klaim gap | Belum |
| V-2 | Verifikasi metadata & DOI 5 kandidat di `10_Kandidat_Referensi.csv` (baris `belum diverifikasi`) | Sitasi sahih | Belum |
| V-3 | Baca **teks penuh** entropy-SAW (`10.1007/s11276-021-02625-y`) | Sumber diferensiasi — pastikan apa yang sudah/belum dilakukan | Belum |
| V-4 | Cari string spesifik: `("weighting" OR "normalization") AND ("link quality" OR "QoS scoring") AND ("real-time" OR streaming)` | Menutup G-N1/G-N2 | Belum |
| V-5 | Cari `("temporal stability" OR "rank reversal") AND "MCDM" AND ("time series" OR dynamic)` | Menutup G-W1 | Belum |
| V-6 | Verifikasi angka **ITU-T Y.1541 / G.114** ke teks standar | Sitasi angka benar | Belum |
| V-7 | Snowballing dari 10 paper inti | Referensi tambahan | Belum |
| V-8 | Cek retraksi & status predator venue kandidat | Kredibilitas | Belum |

**Bukti yang disimpan:** tanggal, basis data, string, jumlah hit, jumlah lolos,
alasan eksklusi (protokol PRISMA ringkas).

---

## 2. Verifikasi Prior Art **[prioritas tertinggi]**

| Kode | Pekerjaan | Tujuan |
|---|---|---|
| PA-1 | Salin abstrak & klaim utama **US 9,674,720 B2** sebagai related prior art | Menghindari overclaim nama ALQI |
| PA-2 | Cari paten/artikel lain dengan istilah "link quality index" + ambang | Memastikan tidak ada prior art lain |
| PA-3 | Putuskan: ganti istilah ALQI, atau pertahankan dengan sitasi + pembeda tegas | Kebersihan klaim |

---

## 3. Verifikasi Teknis & Data (prioritas sedang)

| Kode | Pekerjaan | Tujuan |
|---|---|---|
| T-1 | Inventaris isi dataset `11_Kolektor_Baseline/data/*.jsonl` (kolom, resolusi, durasi) | Memastikan L1 (offline) dapat dijalankan |
| T-2 | Cek ketersediaan **REST API tulis-terpisah** (akun write) di RB1100AHx4 (SNMP opsional) | Prasyarat adopsi |
| T-3 | Cek ketersediaan telemetri Starlink (gRPC dish) | Data throughput akurat |
| T-4 | Konfirmasi izin lokasi & kepatuhan ToS ISP | Kelayakan operasional |
| T-5 | Uji `tc/netem` di staging | Validasi internal |
| T-6 | **Uji independensi dua Starlink** (korelasi transien LEO-1–LEO-2; ambang < 0,7) | Kelayakan tri-link (`00_README.md` §6) |

---

## 4. Keputusan yang Harus Dikunci Sebelum Bab I

| Kode | Keputusan | Opsi | Rekomendasi |
|---|---|---|---|
| D-1 | Lingkup | Varian A (luas) / B (sempit/skoring) / C (tengah) | Lihat `07_...` & `09_...` |
| D-2 | Nama istilah | Ganti ALQI / pertahankan + sitasi prior art | Ganti atau batasi |
| D-3 | Skema bobot | Statis / objektif / hibrida | Hibrida |
| D-4 | Normalisasi default | N-a / N-b / **N-c** | N-c |
| D-5 | Primary outcome | Spearman ρ / stabilitas / AUC | Tetapkan satu |
| D-6 | Keterlibatan lapangan | Ya / tidak (cukup offline+staging) | Tergantung waktu |
| D-7 | **Topologi uji** | Dual-ISP (A+C) / **Tri-link 1 FO + 2 LEO (A+B+C)** / Dual + validasi tri | **Tri-link (revisi 18 Nov 2026)**; tunduk pada uji independensi T-6 |

---

## 5. Urutan Kerja yang Diusulkan **[USULAN]**

1. PA-1 → PA-3 (selesaikan isu prior art).
2. V-1 → V-3 (verifikasi literatur inti).
3. D-1 (kunci lingkup) → D-3, D-4, D-5.
4. T-1 (inventaris data) → jalankan **L1 offline** sebagai bukti konsep.
5. Tulis Bab I berdasarkan `09_Rumusan_Masalah_dan_Judul.md`.
6. T-2 → T-5 (siapkan staging) jika lingkup mencakup alokasi.

---

## 6. Yang **Tidak** Perlu Diulang dari Arsip **[ANALISIS]**

Banyak bahan arsip masih relevan dan **tidak** perlu dikerjakan ulang:
- batas acuan parameter (TIPHON/Y.1541) → sudah diekstrak, lihat `03_...`;
- dataset baseline 2,2 jam → sudah ada;
- desain statistik (effect size, Holm, bootstrap) → dapat diadopsi dari arsip
  `06_Tahap_04_Metodologi/04_Rencana_Analisis_Statistik.md`;
- kerangka penulisan klaim → adopsi tabel klaim arsip
  `04_Tahap_03_Kerangka_Teori/03_Tabel_Klaim_dan_Sumber.md` dengan status
  **[FAKTA]/[ANALISIS]/[USULAN]**.
