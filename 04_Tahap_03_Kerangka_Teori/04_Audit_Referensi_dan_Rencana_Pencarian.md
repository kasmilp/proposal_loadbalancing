# Tahap 3 — Audit Referensi dan Rencana Pencarian

**Dokumen:** `04_Audit_Referensi_dan_Rencana_Pencarian.md`
**Fungsi:** Memastikan korpus cukup, mutakhir, dan dapat ditelusuri; menutup klaim
"belum ada penelitian" dengan bukti pencarian.

---

## 1. Inventaris Korpus

| Folder | Berkas | Dipakai di Bab II | Catatan |
|---|---:|---:|---|
| `01_QoS_dan_Pengukuran` | 6 | 3 | Standar TIPHON + QoS RT/RW Net |
| `02_FO_IndiHome_dan_Optik` | 4 | 2 | Bukti operasional FO |
| `03_LEO_Starlink_dan_Satelit` | 26 | 8 | Inti dinamika LEO |
| `04_PCC_MikroTik_dan_Load_Balancing` | 15 | 7 | Inti baseline |
| `05_MCDM_SAW_EWMA_dan_Histeresis` | 7 | 3 | Metode |
| `06_SDN_dan_Arsitektur_Kontrol` | 14 | 3 | Arsitektur |
| `07_QoE_dan_Aplikasi` | 2 | 1 | Batas QoS vs QoE |
| `08_Cloud_dan_Load_Balancing_Umum` | 6 | 2 | Pembanding |
| `09_Referensi_Umum_dan_Lainnya` | 9 | 0 | Sebagian besar di luar fokus |
| **Total** | **89** | **29** | |

Korpus memadai untuk Bab II, tetapi **belum** memadai untuk klaim gap yang
sistematis. Dua area masih tipis: (a) kontinuitas sesi/MPTCP dan (b) metode
statistik untuk data jaringan.

---

## 2. Status Metadata

| Kelompok | Jumlah | Status | Tindakan |
|---|---:|---|---|
| Referensi dengan DOI lengkap | 24 | Siap | Verifikasi DOI resolve |
| Referensi tanpa DOI/tahun | 5 | Perlu dilengkapi | Cari via Crossref/Google Scholar |
| Standar (RFC, ITU, ETSI) | 7 | Siap | Cantumkan nomor standar |
| Dokumentasi vendor | 1 | Siap | Cantumkan tanggal akses |
| Buku metode | 4 | Siap | Cantumkan edisi |

**Masalah metadata yang ditemukan:**

1. `references.bib` memiliki entri tanpa tahun dan tanpa penulis lengkap.
2. Banyak nama berkas berupa terjemahan Indonesia, bukan judul asli.
3. Versi `annotated` dan versi utama sering berdampingan; jangan sitasi keduanya.
4. Beberapa DOI di daftar lama belum diuji resolve.
5. Ada paper yang venue-nya perlu dipastikan (mis. Ji et al., 2026).

---

## 3. Duplikat dan Versi Ganda

Gunakan **versi utama** (bukan `annotated`, bukan terjemahan) untuk sitasi.

| Topik | Versi utama | Duplikat/terjemahan |
|---|---|---|
| Amalia et al. (2022) | `pcc.pdf` | `[2022] Amalia...pdf` |
| Arfianita et al. (2024) | `[2024] Arfianita...pdf` | `10 Implementation...pdf` |
| Nugroho et al. (2023) | `21 Quality Analysis...pdf` | `Nugroho...annotated.pdf` |
| Garcia et al. (2025) | `Garcia...annotated.pdf` | `8 Karakterisasi...pdf` |
| Hammer et al. (2024) | `[2024] Hammer...pdf` | `Hammer...annotated.pdf` |
| Mohan et al. (2024) | `starlink.pdf` | `9A Multifaceted...pdf`, `Mohan...annotated.pdf` |
| Ullah et al. (2025) | `Ullah...annotated.pdf` | `7 Dampak Cuaca...pdf` |
| Tournaire et al. (2023) | `[2023] Tournaire...annotated.pdf` | `17Komputasi...pdf` |
| Vafaei et al. (2021) | `Vafaei...pdf` | `14 Menilai...pdf` (2 salinan) |
| Ali et al. (2025) | `[2025] Ali...pdf` | `Ali...annotated.pdf` |
| Mirsal & Agtriadi (2026) | `[2026] Mirsal...pdf` | `[2026] PCC vs QoS...pdf` |

---

## 4. Literatur yang Masih Hilang

| Area | Mengapa penting | Prioritas | Rencana |
|---|---|---|---|
| MPTCP / multipath transport | Membingkai kontinuitas sesi dan alternatif PCC | Tinggi | Cari 3–5 paper 2018–2025 |
| SD-WAN multipath / traffic steering | Pembanding arsitektur | Tinggi | Cari 3 paper |
| Stabilitas sistem switching | Menopang Proposisi 1–2 | Sedang | Cari 2 paper teori kendali |
| Telemetri Starlink (API/gRPC) | Instrumen pengukuran | Tinggi | Dokumentasi resmi + paper |
| Metode statistik data jaringan | Menopang Bab III | Sedang | 2–3 paper/buku |
| Reproducible network experiment | Kredibilitas artefak | Sedang | 1–2 paper |
| Studi RT/RW Net Indonesia | Konteks lokal | Sedang | 2–3 paper |
| Fairness / capacity-aware allocation | Menopang $b_{min}/b_{max}$ | Rendah | 1–2 paper |
| QoE untuk membedakan QoS | Batas klaim | Rendah | 1 paper |

---

## 5. Protokol Pencarian

### 5.1 Basis data dan tanggal

| Basis data | Cakupan | Tanggal rencana |
|---|---|---|
| Scopus | Peer-reviewed internasional | Minggu 1 |
| IEEE Xplore | Jaringan, komunikasi | Minggu 1 |
| ACM Digital Library | Measurement, networking | Minggu 1 |
| ScienceDirect | Procedia, computer science | Minggu 2 |
| SpringerLink | LNCS, journal | Minggu 2 |
| arXiv | Preprint (Starlink, LEO) | Minggu 2 |
| Google Scholar | Snowballing | Minggu 2 |

### 5.2 String pencarian

| Kode | String | Tujuan |
|---|---|---|
| S1 | `("per connection classifier" OR "PCC") AND ("adaptive" OR "dynamic") AND ("MikroTik" OR "RouterOS")` | Menutup klaim C19 |
| S2 | `("load balancing") AND ("hysteresis" OR "dwell" OR "threshold") AND ("network" OR "link")` | Menutup G-M1 |
| S3 | `("Starlink" OR "LEO") AND ("handover" OR "one-way delay" OR "throughput") AND ("measurement" OR "characterization")` | Menopang C11–C14 |
| S4 | `("session continuity" OR "connection tracking" OR "conntrack" OR "MPTCP") AND ("load balancing" OR "failover")` | Menutup G-E1 |
| S5 | `("MCDM" OR "SAW" OR "simple additive weighting") AND ("network selection" OR "handover")` | Menopang C21–C23 |
| S6 | `("SD-WAN" OR "software-defined WAN") AND ("multipath" OR "traffic steering")` | Pembanding arsitektur |
| S7 | `("rain fade" OR "weather") AND ("Starlink" OR "LEO") AND ("throughput" OR "latency")` | Menopang C13–C14 |

Batasan waktu: 2015–2026, kecuali karya seminal (Roberts, 1959; Gamma et al.,
1994) dan standar.

### 5.3 Kriteria inklusi dan eksklusi

**Inklusi**
- Artikel peer-reviewed atau standar resmi.
- Bahasa Inggris atau Indonesia.
- Relevan pada minimal satu komponen: QoS, FO/LEO, PCC/LB, MCDM/EWMA/histeresis,
  arsitektur kontrol, atau kontinuitas sesi.
- Memiliki data, metode, atau kerangka yang dapat dipakai.

**Eksklusi**
- Opini tanpa data, blog tanpa dokumentasi.
- Studi yang tidak dapat dipetakan ke komponen mana pun.
- Duplikat/terjemahan dari artikel yang sudah ada.
- Predatory journal (cek DOAJ/Scopus).

### 5.4 Alur penyaringan (PRISMA ringkas)

```
Identifikasi   : jumlah hit per string          → catat di log
Penyaringan 1  : judul + abstrak                → buang tidak relevan
Penyaringan 2  : teks penuh                     → buang tanpa data/metode
Snowballing    : maju + mundur dari 10 paper inti
Final          : masuk daftar rujukan           → target 35–50
```

**Bukti yang disimpan:** tanggal, basis data, string, jumlah hit, jumlah lolos,
alasan eksklusi. Tanpa ini, klaim "belum ada penelitian" tidak dapat dipertahankan.

---

## 6. Komposisi Rujukan Target

| Kelompok | Target | Sudah ada | Kurang |
|---|---:|---:|---:|
| QoS dan pengukuran | 6 | 4 | 2 |
| FO dan LEO | 10 | 8 | 2 |
| PCC dan load balancing | 8 | 7 | 1 |
| MCDM/EWMA/histeresis | 6 | 4 | 2 |
| SDN dan arsitektur kontrol | 5 | 3 | 2 |
| Kontinuitas sesi/MPTCP | 4 | 0 | 4 |
| Metode dan statistik | 5 | 5 | 0 |
| Standar | 5 | 5 | 0 |
| Konteks/QoE | 2 | 1 | 1 |
| **Total** | **51** | **37** | **14** |

Target minimal 35–50; jumlah di atas memberi margin.

---

## 7. Gaya Sitasi dan Kebersihan Rujukan

- **Gaya:** APA 7 (sesuai draf lama dan daftar rujukan yang sudah ada).
- **Konfirmasi wajib:** buka `panduan_penulisan/Pedoman_Tugas_Akhir_Des23_FIX_Kirim.pdf`
  secara manual dan cocokkan gaya sitasi serta format daftar rujukan. PDF tidak
  dapat dibaca otomatis oleh alat ini.
- **Tier referensi:** ikuti `05_Evaluasi_Tahap_1-3/01_Kebijakan_Tier_Referensi.md`.
  Referensi T3 hanya untuk konteks, bukan SOTA.
- **Pemeriksaan DOI:** setiap DOI harus resolve ke halaman artikel.
- **Pemeriksaan retraksi:** cek Retraction Watch untuk paper 2020–2026.
- **Pemeriksaan predator:** pastikan venue terindeks Scopus/DOAJ.
- **Konsistensi nama:** gunakan nama keluarga + inisial, bukan nama lengkap.
- **Tahun:** gunakan tahun publikasi versi final, bukan tahun arXiv jika sudah terbit.

---

## 8. Rencana Kerja Audit

| Hari | Aktivitas | Luaran |
|---|---|---|
| 1 | Jalankan S1–S3, catat hit | Log pencarian |
| 2 | Jalankan S4–S7, saring judul/abstrak | Daftar kandidat |
| 3 | Baca teks penuh 15 kandidat | Daftar masuk/keluar |
| 4 | Verifikasi 7 klaim berstatus "halaman" | Tabel klaim diperbarui |
| 5 | Lengkapi metadata dan DOI | Register referensi final |
| 6 | Snowballing dari 10 paper inti | 5–10 referensi tambahan |
| 7 | Audit silang sitasi ↔ daftar pustaka | Laporan audit |

---

## 9. Kriteria Selesai Tahap 3

- [ ] Setiap klaim di Bab II punya entri di tabel klaim.
- [ ] Semua status "Verifikasi halaman" sudah dicek.
- [ ] Tidak ada klaim "belum ada" tanpa log pencarian.
- [ ] 35–50 referensi dengan metadata lengkap.
- [ ] Minimal 15 SOTA inti (T1) dan 4 referensi kontinuitas sesi.
- [ ] Gaya APA 7 konsisten.
- [ ] Tidak ada referensi yang hanya muncul di daftar pustaka.
- [ ] Daftar rujukan diformat dan siap dipindah ke naskah.
