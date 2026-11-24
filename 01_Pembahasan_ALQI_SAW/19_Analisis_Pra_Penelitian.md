# 19 — Analisis Pra-Penelitian

**Status:** Dokumen konsolidasi (hasil aktual, 12–19 Nov 2026)
**Fungsi:** Merangkum seluruh hasil kegiatan **pra-penelitian** — lingkungan uji,
akses API, dataset baseline, temuan statistik, dan implikasi — menjadi satu
rujukan untuk gerbang keputusan (T0/T2/T3) dan penulisan Bab I–III.
**Acuan:** `01`–`18` pada folder ini; arsip
`01_Arsip_SPA-HSM_Tahap_01-12/10_Pra_Penelitian/` (protokol, matriks topologi,
diagnostik API, snapshot, hasil baseline) dan `11_Kolektor_Baseline/` (kolektor,
dataset, laporan, log).

**Konvensi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]** (sama seperti `00_README.md`).

---

## 1. Ringkasan Eksekutif

**[ANALISIS]** Kegiatan pra-penelitian **mencapai tujuan utamanya**: (1) akses
read-only ke router **terbukti berfungsi**, (2) dataset baseline **terkumpul**
(2,2 jam pada 13 Nov + **baseline ±5 hari 13–18 Nov** + snapshot 17 Nov), dan
(3) temuan kunci **mempersempit** pilihan desain. Tiga temuan yang paling
berpengaruh:

1. **[FAKTA]** Heterogenitas FO–LEO terkonfirmasi: jitter FO **0,27–0,37 ms**
   vs LEO **5,8–6,2 ms**; RTT p95 FO **46,4–47,5 ms** vs LEO **62–77 ms**
   (pilot 2,2 jam: 89–114 ms); loss FO **0–0,43%** vs LEO **0,27–0,43%** —
   satu orde besaran pada jitter tetap bertahan pada data 5 hari.
2. **[FAKTA]** Dua Starlink co-located **berkorelasi campuran**: korelasi
   Pearson RTT A–B = **0,74** (target 1.1.1.1) dan **0,522** (target 8.8.8.8)
   pada basis 5 hari — satu di atas, satu di bawah ambang 0,7. Keputusan tri-link
   **tetap belum aman** tanpa analisis lanjutan (residual/throughput).
3. **[FAKTA]** **Episode degradasi kini juga muncul pada FO** (18–20 episode,
   median durasi 7,4–10,3 s) di jendela 5 hari — berbeda dari pilot 2,2 jam
   (0–1 episode). Ini memperkaya pelabelan ground truth, tetapi menuntut
   kehati-hatian pada ambang episode.

**Putusan [USULAN]:** lanjut ke **T0 (kunci keputusan)** dan persiapkan **T2/T3**
(spesifikasi + akuisisi data lanjutan). Keputusan **D-7 (tri-link)** ditunda
sampai **uji independensi lanjutan** (residual & throughput 1 detik) selesai.

---

## 2. Inventaris Aset Pra-Penelitian

| Aset | Lokasi | Status |
|---|---|---|
| Kolektor read-only (`collector.py`, librouteros API-SSL) | `11_Kolektor_Baseline/` | Berfungsi **[FAKTA]** |
| Dataset baseline **2,2 jam** (13 Nov 2026 WITA = 12 Nov 21:04–23:17 UTC, 19.706 record) | `11_Kolektor_Baseline/data/` | Siap untuk L1 offline **[FAKTA]** |
| Dataset **sesi 17–18 Nov 2026** (10:18 UTC 17 Nov → 06:11 UTC 18 Nov, ±19,9 jam kontinu, 174.352 probe; `baseline_rb1100ahx4_20261117_181759.jsonl`) | `11_Kolektor_Baseline/data/` | Siap; segmen kontinu terpanjang **[FAKTA]** |
| Laporan gabungan `report_20261119_140603.*` | `11_Kolektor_Baseline/` | ⚠️ **Cakupan tidak kontinu**: hanya 12, 17, 18 Nov; `n=466k` mencakup interpolasi hari kosong 13–16 Nov → **tidak boleh dipakai sebagai "baseline 5 hari"** **[ANALISIS]** |
| Laporan **uji independensi per segmen** (`uji_independensi_AB_segmen.md`) | `11_Kolektor_Baseline/data/` | Selesai 19 Nov **[FAKTA]** |
| Dataset **snapshot/interface 17 Nov 2026** (2 sesi) | `11_Kolektor_Baseline/data/` | Siap; durasi pendek **[FAKTA]** |
| Laporan baseline & periodisitas | `11_Kolektor_Baseline/report_*.md`, `data/*.periodicity.md` | Selesai 13 Nov **[FAKTA]** |
| Diagnostik akses API (12 Nov) | `10_Pra_Penelitian/03_...md` | Selesai **[FAKTA]** |
| Snapshot read-only router (12 Nov) | `10_Pra_Penelitian/04_...md` | Selesai **[FAKTA]** |
| Protokol baseline & matriks keputusan topologi | `10_Pra_Penelitian/01_...md`, `02_...md` | Selesai **[FAKTA]** |
| Skrip analisis (`analyze_baseline.py`, `analyze_periodicity.py`, `uji_independensi_segmen.py`, `analisis_file_tertentu.py`) | `11_Kolektor_Baseline/` | Selesai **[FAKTA]** |

---

## 3. Lingkungan Uji (Fakta Operasional)

### 3.1 Router dan koneksi

| Item | Nilai | Sumber |
|---|---|---|
| Model | MikroTik **RB1100AHx4** | snapshot 12 Nov **[FAKTA]** |
| RouterOS | **7.22.2** (stable) | snapshot 12 Nov **[FAKTA]** |
| CPU load | ±18% | snapshot 12 Nov **[FAKTA]** |
| Memori bebas | ±800 MB dari 1 GB | snapshot 12 Nov **[FAKTA]** |
| Akses API | API-SSL port eksternal **6187 → 8729**, TLS 1.2, cipher **ADH-AES256-SHA256** (anonymous, tanpa sertifikat) | diagnostik 12 Nov **[FAKTA]** |
| Akun | group `read` dengan `!write`, `!policy` → terverifikasi read-only | snapshot 12 Nov **[FAKTA]** |

### 3.2 Topologi tri-link (aktif di router)

| Link | Interface | ISP | Teknologi | Alamat privat |
|---|---|---|---|---|
| L-A | `ether1-ISP-A` | ISP-A | Starlink LEO-1 | 192.168.1.76/24 (DHCP) |
| L-B | `ether2-ISP-B` | ISP-B | Starlink LEO-2 | 192.168.2.160/24 (DHCP) |
| L-C | `ether3-ISP-C` | ISP-C | FO IndiHome | 192.168.3.2/24 (DHCP) |

**[FAKTA]** PCC 3-link **sudah terpasang aktif**: mangle `mark-connection` dengan
classifier `both-addresses-and-ports:3/0|3/1|3/2` → tabel routing `VIA ISP 1/2/3`
→ `mark-routing`. Secara teknis, tri-link **sudah siap** diuji (snapshot 12 Nov).

**[FAKTA]** Ada **tiga default route aktif dengan distance 1** di tabel `main`
(static + DHCP dynamic, ECMP). **[ANALISIS]** Trafik yang tidak ter-mark dapat
mengalami perilaku routing tidak pasti/asymmetric — perlu diaudit sebelum
eksperimen (lihat §5).

### 3.3 Netwatch

**[FAKTA]** Tidak ada entri `netwatch` — baseline praktisi **G** (netwatch failover)
belum dikonfigurasi. **[ANALISIS]** Ini justru sesuai rencana: G dibuat pada tahap
intervensi, bukan saat baseline.

---

## 4. Temuan Statistik Baseline (13 Nov 2026)

Sumber: `05_Hasil_Baseline_2jam.md`, `report_20261113_071809.md`,
`baseline_rb1100ahx4_20261113_050431.periodicity.md` **[FAKTA]**.

### 4.1 Kualitas data

| Item | Nilai |
|---|---|
| Durasi | 2,21 jam (UTC 05:04:32 → 07:17:14) |
| Record | 19.706 |
| Probe | 17.742 (6 seri: 3 WAN × 2 target) |
| Sampel per seri | 2.957 |
| Median interval probe | 2,35 s |
| p95 interval | 3,85 s |
| Gap maksimum | 26–38 s |
| Error | 3 timeout (0,015%) |

**[ANALISIS]** Kualitas baik untuk pilot. Gap puluhan detik sesekali terjadi
(kemungkinan API lambat); untuk pengukuran formal perlu dipantau.

### 4.2 Heterogenitas FO–LEO

| Interface | Target | Loss | RTT median | RTT p95 | Jitter | Episode |
|---|---:|---:|---:|---:|---:|---:|
| ether1-ISP-A (LEO) | 1.1.1.1 | 0,24% | 47,5 ms | 89,1 ms | 7,0 ms | 35 |
| ether1-ISP-A (LEO) | 8.8.8.8 | 0,17% | 61,0 ms | 101,8 ms | 6,8 ms | 53 |
| ether2-ISP-B (LEO) | 1.1.1.1 | 0,30% | 50,4 ms | 98,6 ms | 7,6 ms | 51 |
| ether2-ISP-B (LEO) | 8.8.8.8 | 0,27% | 63,4 ms | 113,8 ms | 7,8 ms | 84 |
| ether3-ISP-C (FO) | 1.1.1.1 | 0,03% | 46,3 ms | 46,7 ms | 0,36 ms | 1 |
| ether3-ISP-C (FO) | 8.8.8.8 | 0,00% | 46,4 ms | 46,7 ms | 0,27 ms | 0 |

(Ambang episode: RTT > 100 ms atau loss > 1%.)

**[ANALISIS]** Perbedaan satu orde besaran pada jitter dan episode 35–84 vs 0–1
mendukung premis penelitian: jalur memiliki dinamika berbeda dan **tidak boleh
diperlakukan sama**.

### 4.3 Episode pendek Starlink

- ISP-A: 35–53 episode, median durasi 3,0–3,4 detik.
- ISP-B: 51–84 episode, median durasi 4,7–6,7 detik.
- FO: 0–1 episode.

**[ANALISIS]** Bukti langsung bahwa LEO menghasilkan degradasi singkat berulang —
kondisi yang ingin ditangani histeresis ($k$, dwell).

### 4.4 Korelasi dua Starlink (kunci D-7)

Korelasi **residual** RTT (setelah detrend):

| Pasangan | Target 1.1.1.1 | Target 8.8.8.8 |
|---|---:|---:|
| ISP-A vs ISP-B | **0,683** | **0,704** |
| ISP-A vs FO | -0,037 | 0,008 |
| ISP-B vs FO | -0,016 | 0,018 |

Korelasi Pearson mentah (laporan): A–B **0,825 / 0,741**; A–FO ≈ -0,006–0,02;
B–FO ≈ -0,015–0,044. Tumpang tindih episode (Jaccard): 0,296–0,392; 47–54%
episode A punya pasangan B dalam ±2 detik.

**[ANALISIS]** Dua LEO di satu lokasi **tidak independen** pada sedi 2,2 jam
(12 Nov): residual 0,683–0,704 berada **tepat di ambang** 0,7; FO independen
terhadap keduanya. Hasil **sesi 17–18 Nov** berbeda (lihat 4.4A) → keputusan
tri-link harus ditunda sampai uji independensi segmen kontinu & throughput 1 s
selesai (lihat §7).

### 4.4A Uji independensi per segmen kontinu (19 Nov 2026, koreksi)

**[FAKTA]** Verifikasi cakupan asli menunjukkan data baseline **tidak kontinu
5 hari**: hanya ada 12 Nov (2,22 jam), 17 Nov 10:18–23:59 UTC, dan 18 Nov
00:00–06:11 UTC (17–18 Nov = **±19,9 jam kontinu**, 174.352 probe).
**Tidak ada data asli 13–16 Nov.** Laporan gabungan `report_20261119_140603.*`
memakai grid 1 detik penuh rentang start→end, sehingga `n=466k` mencakup
**interpolasi hari kosong** — korelasi 0,74/0,522 dari laporan itu **tidak
valid** sebagai "baseline 5 hari".

Korelasi A–B **per segmen kontinu** (resample 1 s hanya dalam segmen):

| Segmen (UTC) | Target | r residual | r mentah | Jaccard bad | Episode match | n |
|---|---|---:|---:|---:|---:|---:|
| 12 Nov 21:05–23:16 | 1.1.1.1 | 0,683 | 0,726 | 0,296 | 0,469 | 7.859 |
| 12 Nov 21:05–23:16 | 8.8.8.8 | 0,704 | 0,739 | 0,392 | 0,542 | 7.858 |
| 17 Nov 10:19 – 18 Nov 06:10 | 1.1.1.1 | **0,384** | 0,481 | 0,284 | 0,079 | 71.468 |
| 17 Nov 10:19 – 18 Nov 06:10 | 8.8.8.8 | **0,393** | 0,481 | 0,316 | 0,117 | 71.468 |

**[ANALISIS]**
- Sesi 17–18 Nov (n=71.468, ±19,9 jam): korelasi residual A–B **0,384–0,393
  < 0,7** dan episode match rendah (0,08–0,12) → indikasi **cukup independen**
  pada sesi ini. Ini lebih representatif dari pilot 2,2 jam (12 Nov).
- Sesi 12 Nov (pilot): 0,683–0,704 (ambang) → variabilitas antar-sesi nyata.
- **Kesimpulan D-7:** bukti **belum konklusif** (1 sesi lolos, 1 sesi ambang).
  **Wajib** memperpanjang baseline kontinu (≥7 hari) dan memakai metrik
  throughput 1 s untuk keputusan final. **Jangan** memakai laporan gabungan
  19 Nov sebagai dasar klaim korelasi.

### 4.5 Periodisitas 15 detik — tidak terkonfirmasi pada RTT

- Periode dominan (FFT, rentang 5–30 s): **≈28,8 detik**, bukan 15.
- Autokorelasi lag 15 detik (residual): **negatif** (-0,24 s.d. -0,30).
- Autokorelasi indikator buruk pada lag 15: hanya 0,03–0,13.
- Proporsi gap episode yang dekat 15 detik: 16–30%.

**[ANALISIS]** Literatur (Garcia et al., 2025; Hammer et al., 2024; Mohan et al.,
2024) melaporkan penurunan *throughput* pada batas ~15 detik, bukan RTT. Probe RTT
kecil mungkin tidak menangkap antrean/laju yang turun. **Konsekuensi:** klaim
"transien 15 detik" tidak boleh menjadi dasar tunggal untuk $k_{\text{down}}=20$;
perlu pengukuran **throughput/interface counter 1 detik**.

### 4.6 Throughput interface (pilot)

| Interface | RX mean | RX p95 | TX mean | TX p95 |
|---|---:|---:|---:|---:|
| ether1-ISP-A | 11,5 Mbps | 19,3 | 0,93 Mbps | 1,87 |
| ether2-ISP-B | 12,1 Mbps | 18,9 | 2,11 Mbps | 3,69 |
| ether3-ISP-C | 11,3 Mbps | 18,2 | 0,90 Mbps | 1,81 |
| Bridge - Hotspot | 4,3 Mbps | 7,0 | 27,9 Mbps | 37,4 |

**[ANALISIS]** Beban jaringan nyata (RX ±11–12 Mbps per WAN; TX didominasi
layanan/hotspot) — berguna untuk menetapkan *ground truth* goodput dan kondisi
beban pada skenario.

---

## 5. Temuan Operasional & Keamanan (11aks 2026)

Dari `04_Snapshot_ReadOnly_12Nov2026.md` dan `03_Diagnostik_Akses_API.md` **[FAKTA]**:

| Prioritas | Temuan | Implikasi |
|---|---|---|
| **Kritis** | Layanan terbuka ke semua interface (`ftp`, `telnet`, `www`, `winbox`, `api`, `api-ssl`, `ssh`, `snmp`); banyak service `detnet`/`ppp` port acak | Permukaan serangan lebar; batasi ke VPN/IP manajemen; audit service tidak dikenal |
| **Kritis** | API-SSL memakai **cipher ADH tanpa sertifikat** (TLS 1.2, anonymous) | Rentan MITM; **aman untuk read-only**, tapi **tidak boleh** untuk akun tulis |
| **Tinggi** | Password monitoring lemah | Ganti; simpan di pengelola sandi; jangan di git |
| **Tinggi** | Tiga default route aktif distance 1 di tabel `main` | Audit; rapikan agar perilaku routing pasti |
| **Sedang** | Group `read` punya `sensitive`/`romon` (tidak perlu) | Hapus untuk *least privilege* |
| **Sedang** | `ip/firewall/connection` timeout | Gunakan filter/SNMP untuk stok koneksi |
| **Rendah** | `netwatch` belum ada | Konfigurasi hanya saat tahap intervensi |

**[ANALISIS]** Tidak ada operasi tulis yang dicoba dan tidak ada konfigurasi yang
diubah selama pra-penelitian — sesuai protokol.

---

## 6. Stok Koneksi (Snapshot 17 Nov 2026)

**[FAKTA]** Snapshot conntrack 17 Nov menunjukkan **15.914 koneksi** aktif:
ISP-A **5.669**, ISP-B **5.786**, ISP-C **3.711** (log kolektor 16:23/18:17 UTC;
sesi 18:17–19:01 sempat mengalami timeout baca `/system/resource` dan `/interface`).

**[ANALISIS]** Ini bukti awal bahwa **stok koneksi nyata dan tidak sepele**
(ribuan koneksi), sehingga relevansi logika sadar-stok (ELS, time-to-rebalance)
terdukung secara empiris. Namun: (1) ini snapshot sesaat, bukan deret waktu;
(2) stok per *connection mark* belum tercatat berkelanjutan; (3) laju koneksi baru
$F_i$ belum diukur. Jadi ini **bukan** hasil eksperimen, melainkan justifikasi
kebutuhan instrumentasi tambahan.

---

## 7. Implikasi untuk Keputusan (D-1…D-7) dan Tahapan

### 7.1 D-7 — Topologi uji (kritis)

| Bukti | Nilai (segmen kontinu) | Ambang arsip |
|---|---|---|
| Korelasi residual A–B — sesi 12 Nov (2,2 jam) | 0,683 / 0,704 | < 0,7 |
| Korelasi residual A–B — sesi 17–18 Nov (±19,9 jam) | **0,384 / 0,393** | < 0,7 |
| Korelasi mentah A–B — 17–18 Nov | 0,481 / 0,481 | — |
| Jaccard episode A–B — 17–18 Nov | 0,284–0,316 | — |
| Episode match A–B — 17–18 Nov | 0,079–0,117 | — |
| FO vs A/B (kedua sesi) | ≈ 0 | — |

**[ANALISIS]** Hasil **bervariasi antar-sesi**: pilot 12 Nov berada di ambang
(0,68–0,70); sesi panjang 17–18 Nov menunjukkan korelasi residual jauh di bawah
ambang (0,38–0,39) dengan episode match rendah. Laporan gabungan `report_20261119_140603.*`
(dengan interpolasi hari kosong 13–16 Nov) **tidak boleh dipakai** untuk
keputusan ini.
**[USULAN] Keputusan:** **tunda finalisasi D-7**. Jangan kunci tri-link maupun
fallback dual sebelum **baseline kontinu ≥7 hari + uji independensi throughput
1 detik** (T-6 diperluas) selesai. Sementara itu:
- tulis topologi sebagai **tri-link bersyarat** dengan fallback Opsi 3
  (dual-ISP A+C + B sebagai validasi eksternal);
- lunakkan klaim "dua sumber degradasi berbeda" → "satu FO + dua LEO yang dapat
  berkorelasi (terukur 0,38–0,70 bergantung sesi)".

### 7.2 D-1…D-6

**[ANALISIS]** Data pra-penelitian tidak mengubah rekomendasi yang ada:
D-1 Varian C (tengah), D-2 batasi istilah + sitasi prior art, D-3 bobot hibrida,
D-4 N-c, D-5 primary outcome (tetapkan satu), D-6 tergantung waktu & izin.
**[USULAN]** Kunci D-1…D-6 di T0; D-7 mengikuti uji independensi (T3).

### 7.3 Dampak ke parameter (kalibrasi)

| Parameter | Implikasi dari data |
|---|---|
| $k_{\text{down}}$ | **Tidak** boleh didasarkan semata pada "transien 15 detik" (belum terkonfirmasi). Kalibrasi dari durasi episode nyata (median 3–7 s; p95 perlu dihitung) |
| $\alpha$ EWMA | Kalibrasi dari varians RTT (autokorelasi lag 1 tinggi: 0,87–0,98) |
| $\theta_{\text{low}}/\theta_{\text{high}}$ | Kalibrasi dari distribusi $Q$ setelah normalisasi |
| $W$ (jendela flap) | Test 1/5/15; episode pendek sering → serasi |
| Interval probe | Median 2,35 s; target 1 s untuk throughput/interface |

### 7.4 Kesenjangan data vs kebutuhan eksperimen

| Kebutuhan (T2/T3) | Status | Rencana |
|---|---|---|
| RTT/jitter/loss per WAN | Tersedia (2,2 jam) | Perpanjang 7 hari + jam sibuk/hujan |
| Throughput 1 detik | **Belum** | SNMP `ifHCInOctets`/`ifHCOutOctets` per 1 s atau probe iperf3 10–15 menit |
| Stok koneksi $S_i$ per connection mark | **Belum** (baru snapshot 17 Nov) | Pembacaan ringan 30 s (bukan seluruh conntrack) |
| Laju koneksi baru $F_i$ | **Belum** | Log/agregat ringan |
| Ground truth goodput | **Belum** | iperf3/HTTP terukur saat L1/L2 |
| Telemetri Starlink (gRPC dish) | Belum dicek | T-3 |
| Data sintetis (transien 15 s, degradasi bertahap) | Belum dibuat | Generator untuk L1/L2 |
| Basline praktisi G | **Belum** | Konfigurasi netwatch saat intervensi |

---

## 8. Risiko & Mitigasi (tambahan berbasis data)

| Risiko | Bukti | Mitigasi |
|---|---|---|
| Dua LEO berkorelasi | Bervariasi antar-sesi: 0,683–0,704 (12 Nov, ambang) vs 0,384–0,393 (17–18 Nov, lolos); Jaccard 0,28–0,39 | Baseline kontinu ≥7 hari + uji independensi throughput 1 s; fallback Opsi 3; lunakkan klaim |
| **Interpolasi lintas celah (artefak laporan gabungan)** | `report_20261119_140603.*` memuat `n=466k` padahal data asli hanya 12/17/18 Nov → korelasi 0,74/0,522 tercemar | Selalu laporkan cakupan asli per tanggal; hitung korelasi **per segmen kontinu**; jangan pakai grid penuh lintas hari kosong |
| Transien 15 s tidak terlihat di RTT | Periode dominan 28,8 s; ACF15 negatif (pilot) | Ukur throughput 1 s sebelum menetapkan $k_{\text{down}}$ |
| Stok koneksi tidak terukur | Baru snapshot | Tambah instrumentasi 30 s di kolektor |
| API ADH tanpa sertifikat | Diagnostik 12 Nov | Jangan gunakan akun tulis lewat jalur ini; pasang sertifikat/VPN |
| Timeout baca (sesi 17 Nov) | 19:01:07, 19:01:17 | Pantau stabilitas API; retry + kualitas data dalam laporan |
| Layanan terbuka & password lemah | Snapshot 12 Nov | Batasi layanan, ganti password, least privilege sebelum intervensi |

---

## 9. Rekomendasi & Langkah Berikutnya

**[USULAN] Urutan kerja:**

1. **T0** — kunci D-1…D-6; tandai **D-7 sebagai tertunda** dengan kriteria
   lulus eksplisit (korelasi residual A–B < 0,7 pada throughput 1 s).
2. **T-6 diperluas (T3)** — jalankan **pengukuran throughput 1 detik** pada
   ketiga WAN (10–15 menit) dan hitung ulang korelasi transien A–B pada metrik
   throughput/laju, bukan hanya RTT. Putuskan D-7 setelahnya.
3. **T2** — finalisasi spesifikasi parameter dengan kalibrasi berbasis data (§7.3);
   tambah instrumentasi stok koneksi ($S_i$) dan laju ($F_i$).
4. **T3** — perpanjang baseline 7 hari (jam sibuk 19.00–23.00, jam rendah
   01.00–05.00, minimal satu hujan); ciptakan data sintetis untuk L1/L2.
5. **Keamanan** — sebelum intervensi: batasi layanan, ganti password, rapiikan
   default route ganda, sediakan akun `controller-write` terbatas lewat jalur
   aman (VPN/sertifikat).
6. **L1 offline** — segera dapat dijalankan dari dataset 2,2 jam (aset sudah ada).

**Klaim yang boleh ditulis sekarang (dengan bukti):**
- heterogenitas FO–LEO terukur (jitter/loss/RTT) — `05_Hasil_Baseline_2jam.md`
  dan `analisis_20261117_181759.md`;
- episode pendek berulang pada LEO — ibid.;
- stok koneksi nyata ±15,9 ribu (snapshot 17 Nov) — log kolektor;
- korelasi LEO co-located **bervariasi antar-sesi**: ambang pada 12 Nov
  (0,68–0,70), jauh di bawah ambang pada 17–18 Nov (0,38–0,39) —
  `uji_independensi_AB_segmen.md`;
- **tidak boleh** mengklaim periodisitas 15 detik pada RTT — periodicity report;
- **tidak boleh** mengklaim "baseline 5 hari" — data asli hanya segmen 12 & 17–18 Nov.

---

## 10. Checklist Progres Pra-Penelitian

- [x] Akses API read-only berhasil & terverifikasi (12 Nov)
- [x] Snapshot konfigurasi router (12 Nov)
- [x] Baseline 2,2 jam + laporan + analisis periodisitas (13 Nov)
- [x] Snapshot conntrack/stok (17 Nov)
- [x] Sesi 17–18 Nov (±19,9 jam) + analisis file (`analisis_20261117_181759.md`)
- [x] Uji independensi A–B per segmen kontinu (`uji_independensi_AB_segmen.md`)
- [x] Audit keamanan & temuan prioritas (12 Nov)
- [ ] Pengukuran throughput 1 detik pada 3 WAN
- [ ] Uji independensi A–B pada metrik throughput (putuskan D-7)
- [ ] Baseline formal kontinu 7 hari (jam sibuk, jam rendah, hujan)
- [ ] Instrumentasi stok $S_i$ dan laju $F_i$
- [ ] Data sintetis L1/L2
- [ ] Perbaikan keamanan sebelum intervensi
- [ ] Kunci D-1…D-6 (T0) dan D-7 (setelah uji independensi)
