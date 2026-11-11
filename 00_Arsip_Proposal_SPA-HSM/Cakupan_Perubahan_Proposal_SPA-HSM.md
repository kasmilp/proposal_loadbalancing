# Cakupan Perubahan Proposal Tesis

## SPA-HSM untuk Kendali Proporsi Aliran Adaptif pada WAN Heterogen

**Dokumen sumber:** Audit konsistensi Bab I–II proposal tesis  
**Tanggal:** 6 November 2026  
**Status:** Draf kerja revisi — bukan naskah proposal final  
**Penulis:** Kasmil Papalia (D082252011)  
**Program:** Magister Teknik Informatika, Universitas Hasanuddin

> Dokumen ini merangkum keputusan lingkup, temuan audit, perubahan yang diperlukan, prioritas, dan kriteria penerimaan. Fungsinya sebagai *change scope* dan checklist revisi sebelum seminar.

---

## 1. Tujuan dan Cara Pakai

Dokumen ini dipakai untuk:

1. mengunci keputusan lingkup agar Bab I dan Bab II tidak saling bertentangan;
2. memetakan setiap temuan audit ke perubahan konkret;
3. memberi urutan prioritas revisi sebelum seminar dan sebelum pengujian lapangan;
4. menjadi dasar diskusi dengan pembimbing.

Cara pakai: selesaikan **P0** sebelum seminar, **P1** sebelum pengujian lapangan, dan **P2** saat penyempurnaan naskah.

---

## 2. Keputusan Lingkup yang Ditetapkan

| No | Keputusan | Konsekuensi yang harus tercermin di proposal |
|---|---|---|
| K-01 | Sistem diuji pada topologi **dual-ISP: FO IndiHome dan LEO Starlink**. | Tidak boleh mengklaim generalisasi ke lebih dari dua ISP atau ke semua WAN heterogen. Batasan ini harus eksplisit di 1.7 dan di akhir Bab II. |
| K-02 | Starlink LEO dipakai sebagai **kasus acuan (upper bound)** untuk merancang parameter histeresis karena fluktuasinya berskala detik. | Starlink bukan satu-satunya target penerapan. Parameter harus diturunkan dari karakteristik transien Starlink (mis. siklus sekitar 15 detik), lalu diuji apakah tetap masuk akal untuk degradasi FO yang lebih lambat. |
| K-03 | Bobot kriteria SAW **tidak self-tuning**; dikalibrasi statis di awal. | Harus ada protokol kalibrasi, nilai bobot terdokumentasi, dan analisis sensitivitas. Klaim “adaptif” hanya boleh merujuk pada rasio alokasi, bukan pada pembelajaran bobot. |
| K-04 | MikroTik/RouterOS adalah **platform adapter/testbed eksekutor data plane**, bukan objek algoritma. | Judul, abstrak, tujuan, dan kontribusi tidak boleh memberi kesan bahwa penelitian mengembangkan PCC MikroTik. Independensi platform harus diuji lewat kontrak antarmuka dan mock adapter, atau klaimnya diturunkan menjadi “dirancang agar portabel”. |

**Implikasi judul:** frasa “Studi Kasus Implementasi PCC pada Router MikroTik” perlu dipertimbangkan ulang. Jika MikroTik bukan objek, judul sebaiknya menonjolkan SPA-HSM dan WAN heterogen, dengan MikroTik disebut sebagai testbed di subjudul atau abstrak.

---

## 3. Glosarium dan Penyelarasan Nama

Proposal saat ini memakai beberapa nama yang berpotensi saling tumpang tindih. Tetapkan satu nama payung dan satu nama komponen.

| Istilah | Usulan makna | Tindakan |
|---|---|---|
| **SPA-HSM** | *Session-Preserving Asymmetric Hysteresis State Machine* — nama sistem/algoritma yang diusulkan. | Jadikan nama utama di judul, rumusan masalah, tujuan, dan hipotesis. |
| **Q_i(t)** | Skor kualitas kontinu link ke-i pada waktu t, hasil EWMA + SAW, rentang 0–1. | Gunakan konsisten; jangan berganti-ganti dengan “ALQI” tanpa definisi. |
| **ALQI** | Nama lama untuk skor kualitas komposit. | Jika dipertahankan, definisikan sebagai “nama lain Q_i(t)” dan pakai hanya di satu tempat. Jika tidak, hapus. |
| **TLABA** | Nama algoritma di rumusan masalah lama (utilisasi, kapasitas, demand, bucket). | Hapus, atau jadikan modul alokasi terpisah dengan definisi formal. Jangan biarkan muncul hanya di 1.3. |
| **AFFINITY_LOCK** | Direktif abstrak yang menahan sesi lama pada jalur awalnya. | Definisikan sebagai bagian dari *Abstract Allocation Interface*. |
| **Effective PCC rule change** | Perubahan aturan mangle/routing yang memengaruhi alokasi *new flows*. | Jadikan definisi operasional “flapping” agar Skenario B–F sebanding. |

---

## 4. Ringkasan Temuan Audit

### 4.1 Yang sudah kuat

- Alur masalah → celah → solusi → hipotesis jelas dan mudah diikuti.
- Rancangan ablasi A–D adalah pendekatan yang tepat untuk membedah komponen.
- Batasan masalah jujur: MikroTik hanya testbed, bobot SAW statis, Starlink sebagai batas atas.
- Pemisahan tiga lapis (*Algorithm Core*, *Abstract Interface*, *Platform Adapter*) masuk akal secara rekayasa.

### 4.2 Temuan kritis

1. **Ablasi tidak mengisolasi komponen.** Skenario D berbeda dari C pada dua faktor sekaligus: histeresis asimetris dan perlindungan sesi.
2. **Klaim session disruption belum dibuktikan.** Perlu mekanisme teknis yang jelas, bukan asumsi bahwa perubahan aturan PCC otomatis mereset sesi.
3. **Konversi skor kontinu → rasio diskret belum dirumuskan.** Jumlah state, fungsi Q_i → W, jumlah bucket, dan tabel transisi belum ada.
4. **Ketegangan logika histeresis asimetris.** *Downscale* cepat bisa memicu DEGRADED berulang pada lonjakan 15 detik jika k_down lebih pendek dari durasi lonjakan.
5. **Hipotesis belum sepenuhnya terukur.** H2 memuat dua klaim; “mendekati nol” tidak punya ambang; definisi flapping antar-skenario tidak sebanding.

### 4.3 Temuan penting

6. **Analisis statistik tidak cocok dengan desain data.** Empat skenario tidak boleh diuji dengan t-test berulang; data deret waktu berkorelasi; flapping adalah data cacah.
7. **Confounder lapangan.** Cuaca, jam sibuk, dan urutan run berbeda antar-skenario; perlu randomisasi/counterbalancing atau evaluasi utama di staging.
8. **Baseline pembanding belum ada.** B dan C adalah rancangan sendiri, bukan algoritma terpublikasi.
9. **Klaim platform-independent belum diuji.** Hanya ada satu adapter (MikroTik).
10. **Dasar pengukuran SAW kurang spesifik.** Normalisasi, cost/benefit, kalibrasi bobot, dan cara probing belum dijelaskan.
11. **Tinjauan pustaka belum ada.** Klaim 15 detik, rain fade, bufferbloat FO, dan “upaya terdahulu” belum bersitasi.

### 4.4 Temuan minor

- Judul menonjolkan MikroTik, bertentangan dengan K-04.
- Tahap NDLC “Management” diisi analisis statistik, bukan manajemen jaringan.
- Heading 2.5 menempel di akhir paragraf 2.4.
- Keselamatan operasional dan etika pelanggan belum dibahas.
- Keterbatasan satu pasang ISP terhadap klaim “WAN heterogen” belum eksplisit.

---

## 5. Cakupan Perubahan per Area

### 5.1 Judul, abstrak, dan posisi MikroTik

**Masalah:** judul memberi kesan MikroTik adalah objek penelitian, sedangkan 1.6 menyatakan sebaliknya.

**Perubahan:**
- Ubah judul agar fokus pada SPA-HSM dan kendali proporsi aliran pada WAN heterogen.
- Pindahkan MikroTik ke subjudul/abstrak sebagai testbed.
- Tambahkan satu paragraf di 1.6 yang menyatakan kontribusi algoritmik dan independensi platform.
- Jika klaim independensi tidak diuji, tulis “dirancang portabel” bukan “terbukti portabel”.

**Kriteria penerimaan:** judul, abstrak, 1.6, 2.3, dan kesimpulan memakai posisi MikroTik yang sama.

### 5.2 Rumusan masalah dan tujuan

**Masalah:** 1.3 memakai TLABA dengan utilisasi/kapasitas/demand, tetapi Bab II memakai SPA-HSM berbasis Q_i(t) dan histeresis.

**Perubahan:**
- Tetapkan satu payung: SPA-HSM.
- Pecah rumusan masalah menjadi 2–3 pertanyaan yang dapat dijawab:
  1. Bagaimana merumuskan Q_i(t) dari metrik QoS dengan normalisasi dan bobot statis?
  2. Bagaimana merancang state machine histeresis asimetris yang menekan flapping tanpa memperlambat pemulihan?
  3. Bagaimana memetakan state/Q_i(t) ke rasio PCC diskret yang menjaga sesi dan meningkatkan goodput?
  4. Seberapa besar efek masing-masing komponen berdasarkan ablasi?
- Selaraskan tujuan dengan pertanyaan tersebut.
- Hapus TLABA atau definisikan sebagai modul alokasi terpisah.

**Kriteria penerimaan:** tidak ada istilah algoritma yang muncul hanya di satu subbab; setiap tujuan menjawab satu rumusan masalah.

### 5.3 Hipotesis

**Masalah:** H2 menggabungkan dua klaim; “mendekati nol” tidak terukur; flapping B vs C vs D tidak sebanding.

**Perubahan:**
- **H1:** Histeresis asimetris menurunkan *effective PCC rule change per jam* dibanding tanpa histeresis dan histeresis simetris, tanpa melewati batas *recovery latency* yang ditetapkan.
- **H2a:** *Affinity lock* menurunkan TCP RST rate dibanding tanpa affinity, dengan ambang mis. < 1% atau non-inferior terhadap baseline statis.
- **H2b:** Sistem usulan meningkatkan goodput dan menurunkan latensi end-to-end dibanding PCC statis pada episode degradasi.
- **H3 (opsional):** *Algorithm core* lulus uji kesesuaian antarmuka dengan mock adapter dan menghasilkan keputusan identik di dua adapter.
- Definisikan flapping secara operasional: jumlah perubahan aturan PCC efektif per jam; perubahan yang berbalik dalam jendela W tetap dihitung sebagai satu flap.
- Ganti “mendekati nol” dengan ambang numerik dan interval kepercayaan.

**Kriteria penerimaan:** setiap hipotesis punya variabel, metrik, uji, ambang, dan arah yang jelas.

### 5.4 Kerangka metodologi dan NDLC

**Masalah:** “Management” diisi analisis statistik; ini bukan makna manajemen jaringan.

**Perubahan:**
- Pertahankan NDLC untuk pengembangan sistem.
- Pindahkan analisis statistik ke tahap *Monitoring/Evaluation*.
- Tambahkan tahap *Evaluation* eksplisit, atau nyatakan bahwa NDLC dipakai untuk rekayasa dan kuasi-eksperimen dipakai untuk evaluasi.
- Buat tabel pemetaan: tahap NDLC → aktivitas → luaran → alat.

**Kriteria penerimaan:** tidak ada kategori aktivitas yang salah tempat; setiap tahap punya luaran yang dapat diperiksa.

### 5.5 Arsitektur tiga lapis dan kontrak antarmuka

**Masalah:** pemisahan tiga lapis bagus, tetapi kontrak *Abstract Allocation Interface* belum didefinisikan.

**Perubahan:**
- Definisikan kontrak antarmuka: input (Q_i, state, ratio target), output (direktif), operasi (`SET_RATIO`, `AFFINITY_LOCK`, `ROLLBACK`), idempotensi, versi, dan penanganan error.
- Definisikan adapter API: read metrics, apply rules, verify state, rollback.
- Tambahkan *sequence diagram* dari metric poll → decision → directive → adapter → verification.
- Sediakan satu mock adapter untuk pengujian tanpa router.

**Kriteria penerimaan:** ada tabel spesifikasi antarmuka; core tidak mengimpor API vendor secara langsung.

### 5.6 Formalisasi SPA-HSM

**Masalah:** belum ada rumus EWMA, normalisasi SAW, Q_i(t), transisi state, dan pemetaan Q_i → W.

**Perubahan:** tambahkan subbab “Formalisasi” yang memuat:

- **Sampling:** interval T_s; justifikasi terhadap transien Starlink (~15 detik). Hindari aliasing; jika T_s = 5 detik dan k_down = 3, jendela keputusan = 15 detik — sama dengan periode gangguan.
- **EWMA:** `E_i(t) = α x_i(t) + (1-α) E_i(t-1)`, dengan α dan *effective window* `N_eff ≈ 2/α - 1`.
- **Normalisasi SAW:** gunakan batas acuan tetap (TIPHON/ITU-T), bukan min/max antar-link setiap siklus. Contoh cost: `r = (x_max - x)/(x_max - x_min)`; benefit: `r = (x - x_min)/(x_max - x_min)`. Tangani `0/0` dengan ε.
- **Skor:** `Q_i(t) = Σ_j w_j r_ij(t)`, `Σ w_j = 1`, `Q_i ∈ [0,1]`.
- **State machine:** state `STABLE` dan `DEGRADED` (opsional `RECOVERING`). Transisi:
  - `STABLE → DEGRADED` jika `Q_i(t) < θ_low` selama `k_down` sampel berturut-turut.
  - `DEGRADED → STABLE` jika `Q_i(t) > θ_high` selama `k_up` sampel berturut-turut.
  - Syarat: `θ_high > θ_low` dan `k_up ≫ k_down`.
- **Pemetaan rasio:** `W_i = Q_i / Σ Q_j` (kualitas saja) atau `W_i = Q_i H_i / Σ Q_j H_j` (dengan headroom H_i, lebih disarankan). Petakan ke bucket integer: `b_i = round(N W_i)`, `Σ b_i = N`, dengan `b_min` dan `b_max`.
- **Tabel transisi:** state gabungan (STABLE/STABLE, FO DEGRADED, LEO DEGRADED, BOTH DEGRADED) → rasio target.
- **Inisialisasi:** hitung rasio awal dari Q_i setelah warm-up; jangan menunggu transisi pertama.
- **Batas waktu:** evaluasi ulang minimal setiap T_max agar degradasi lambat tidak tertahan di zona mati.

**Kriteria penerimaan:** semua simbol didefinisikan; ada contoh perhitungan; ada tabel parameter dan tabel transisi; tidak ada rumus yang hanya berupa gambar tanpa keterangan.

### 5.7 Desain ablasi

**Masalah:** D vs C mengubah dua faktor sekaligus.

**Perubahan:** gunakan desain faktorial 3 × 2:

- Faktor 1: histeresis — none / symmetric / asymmetric.
- Faktor 2: affinity lock — off / on.

Skenario:

| Skenario | Histeresis | Affinity | Peran |
|---|---|---|---|
| A | Tidak ada (statis 50:50) | — | Baseline |
| B | None | Off | Dynamic naive |
| C | Symmetric | Off | Isolasi bentuk histeresis |
| D | Asymmetric | Off | Isolasi asimetri |
| E | Symmetric | On | Affinity pada simetris |
| F | Asymmetric | On | **Proposed SPA-HSM** |

Jika waktu terbatas, minimum A, B, D, F; tetapi klaim kontribusi *affinity* dan *asimetri* tidak bisa dipisahkan sepenuhnya.

Tambahkan satu baseline praktisi: PCC + `netwatch`/health-check failover atau weighted ECMP berbasis monitoring.

**Kriteria penerimaan:** setiap perbandingan mengubah satu faktor; ada tabel faktor dan urutan run yang diacak/counterbalanced.

### 5.8 Baseline pembanding

**Masalah:** B–F adalah rancangan sendiri; tidak ada pembanding yang dikenal praktisi.

**Perubahan:**
- Tambahkan PCC + health-check/netwatch failover sebagai baseline praktisi.
- Opsional: weighted ECMP berbasis monitoring, atau static capacity-proportional.
- Jelaskan konfigurasi baseline dan sitasi.

**Kriteria penerimaan:** baseline punya konfigurasi terdokumentasi dan alasan pemilihan.

### 5.9 Pengukuran dan instrumen

**Masalah:** SNMP/API saja tidak menghasilkan delay/jitter/loss end-to-end; throughput ambigu; probing membebani link.

**Perubahan:**
- **Probe per WAN:** ICMP/TCP/HTTP dari controller atau LAN probe dengan source routing/routing mark.
- **SNMP:** `ifHCInOctets`/`ifHCOutOctets` untuk carried throughput dan utilisasi; `ifInErrors`/`ifOutDiscards` sebagai indikator tambahan.
- **Starlink telemetry:** gRPC dish metrics (latency, drop rate, obstruction) jika tersedia; jika tidak, probe aktif.
- **Wireshark:** RST rate dan retransmisi TCP untuk validasi H2a.
- **Throughput:** bedakan carried throughput, achievable throughput, dan goodput. Untuk ALQI/Q_i, gunakan headroom atau achievable throughput, bukan carried throughput.
- **Jitter:** rumus RFC 3550 atau standar deviasi RTT; **loss:** sequence gap; laporkan p50/p95/p99, bukan hanya rata-rata.
- **Sampling:** T_s untuk skoring; probe throughput aktif dengan frekuensi rendah (mis. 5–15 menit) agar tidak mengganggu kuota.
- **Kalibrasi:** bandingkan SNMP vs probe vs Wireshark pada pilot 24–48 jam.

**Kriteria penerimaan:** tabel instrumen (metrik, alat, vantage point, rumus, interval); ada data pilot.

### 5.10 Analisis statistik

**Masalah:** t-test berulang, autokorelasi, data cacah, dan confounder.

**Perubahan:**
- Tetapkan **primary outcome** (goodput, p95 latency, RST rate, flapping count) dan **secondary outcome** (jitter, loss, recovery latency, overhead).
- Unit analisis: episode degradasi atau jam/hari, bukan setiap siklus polling.
- Uji: ANOVA/Kruskal–Wallis + post hoc (Tukey/Dunn, koreksi Holm/Bonferroni); mixed-effects/GEE untuk data deret waktu; Poisson/negative binomial untuk flapping; bootstrap/permutation untuk distribusi non-normal.
- Laporkan effect size (Cohen's d, Cliff's delta, incidence rate ratio) dan 95% CI.
- Rancang urutan run secara acak/counterbalanced; beri washout; blok berdasarkan cuaca/jam.
- Evaluasi kausal utama di staging dengan trace replay/tc netem; lapangan sebagai validasi eksternal.
- Lakukan power analysis atau tetapkan minimum detectable effect, jumlah replikasi, dan durasi per skenario.
- Catat confounder: firmware Starlink, perubahan paket ISP, beban pelanggan, cuaca, daya listrik.

**Kriteria penerimaan:** ada tabel hipotesis–uji–asumsi–effect size; tidak ada t-test sebagai default; ada justifikasi jumlah run.

### 5.11 Mekanisme session preservation

**Masalah:** klaim “tanpa perlindungan sesi” bisa menjadi strawman; RST belum dibuktikan.

**Perubahan:**
- Jelaskan aturan PCC di RouterOS: mangle `connection-state=new` memberi mark; koneksi lama mempertahankan conntrack mark.
- Definisikan secara teknis apa yang berbeda di Skenario B/C “tanpa affinity”: apakah menghapus filter `new`, mengubah routing untuk semua paket, atau flush conntrack. Jika flush conntrack, sebut sebagai perlakuan yang disengaja dan jelaskan risikonya.
- Jelaskan jalur timbulnya RST: perubahan gateway mid-flow, NAT/conntrack mismatch, atau reordering.
- Lakukan pilot staging dengan iperf3/TCP flow untuk membuktikan mekanisme, bukan mengasumsikannya.
- Sitasi dokumentasi MikroTik dan literatur connection tracking.

**Kriteria penerimaan:** ada diagram mekanisme; RST diukur, bukan diklaim; tidak ada perlakuan yang dibuat gagal secara artifisial.

### 5.12 Keselamatan operasional dan etika

**Masalah:** eksperimen pada jaringan komersial; controller bisa mati; pelanggan bisa terganggu.

**Perubahan:**
- **Fail-safe:** jika controller mati/API putus, kembali ke PCC statis terakhir (fail-static), dengan watchdog dan systemd.
- **Rollback:** skrip restore config, backup sebelum run, verifikasi setelah injeksi.
- **Jadwal:** uji pada jam rendah risiko; beri notice ke pelanggan; siapkan maintenance window.
- **Etika:** persetujuan pemilik RT/RW Net; anonimisasi data pelanggan; tidak menangkap payload; patuhi kebijakan kampus.
- **Risiko:** tabel risiko (Starlink outage, hujan, listrik, perubahan ISP, CPU router, API failure) + mitigasi.

**Kriteria penerimaan:** ada bagian “Operational Safety and Ethics”; ada prosedur rollback yang diuji.

### 5.13 Tinjauan pustaka dan sitasi

**Masalah:** belum ada Bab Tinjauan Pustaka; beberapa klaim belum bersitasi.

**Perubahan:**
- Tambahkan bab/subbab tinjauan pustaka: QoS, PCC/ECMP/NTH, MCDM/SAW, EWMA, histeresis/state machine, adaptive load balancing, SD-WAN, dual-WAN, Starlink, platform independence/adapter pattern.
- Sitasi: MikroTik PCC/REST API, ETSI TIPHON, ITU-T G.114/Y.1541, RFC 3550/2330/2544, paper Starlink (Ma, Mohan, Garcia, Hammer), Tournaire, Vafaei.
- Buat *gap matrix*: penelitian terdahulu vs penelitian ini (skor kualitas, histeresis, affinity, platform independence, FO+LEO, field deployment).
- Audit setiap klaim → sumber; gunakan reference manager; pilih satu gaya sitasi (APA 7 atau IEEE).
- Target 35–50 referensi.

**Kriteria penerimaan:** setiap klaim faktual punya sitasi; tidak ada referensi yang hanya muncul di daftar; gaya konsisten.

### 5.14 Format dan konsistensi

**Masalah:** heading 2.5 menempel; penomoran tabel/gambar; rumus hilang; belum ada abstrak.

**Perubahan:**
- Pindahkan heading 2.5 ke paragraf baru.
- Tambahkan abstrak Indonesia dan Inggris + kata kunci.
- Tambahkan daftar simbol, singkatan, dan tabel parameter.
- Nomori rumus, tabel, dan gambar; pastikan semua dirujuk di teks.
- Perbaiki penomoran tabel/gambar yang duplikat.
- Tambahkan jadwal penelitian dan daftar pustaka.
- Konsisten: “MikroTik”, “histeresis”, “throughput”, “packet loss”.

**Kriteria penerimaan:** daftar isi/tabel/gambar akurat; tidak ada placeholder; format sesuai template kampus.

---

## 6. Matriks Cakupan Perubahan

| ID | Area | Perubahan yang diperlukan | Prioritas | Status | Kriteria penerimaan |
|---|---|---|---|---|---|
| C-01 | Judul & posisi MikroTik | Selaraskan judul dengan K-04; MikroTik sebagai testbed | P0 | Perlu keputusan | Judul, abstrak, 1.6 konsisten |
| C-02 | Rumusan masalah | Hapus/definisikan TLABA; fokus SPA-HSM | P0 | Perlu keputusan | Satu nama payung; tujuan selaras |
| C-03 | Hipotesis | Pecah H2; tambah H1/H2a/H2b/H3; ambang numerik | P0 | Rekomendasi audit | Setiap H punya metrik & uji |
| C-04 | Definisi flapping/RST | Definisi operasional & ambang | P0 | Rekomendasi audit | Definisi sama untuk B–F |
| C-05 | Formalisasi | EWMA, SAW, Q_i, W, bucket | P0 | Rekomendasi audit | Semua rumus & simbol ada |
| C-06 | Parameter histeresis | T_s, α, θ_low, θ_high, k_down, k_up | P0 | Perlu kalibrasi | Tabel parameter + justifikasi |
| C-07 | Tabel transisi | State gabungan → rasio | P0 | Rekomendasi audit | Tabel transisi lengkap |
| C-08 | Ablasi | Faktorial 3×2 (A–F) + baseline praktisi | P0 | Rekomendasi audit | Setiap faktor terisolasi |
| C-09 | Baseline | PCC + netwatch/health-check | P1 | Rekomendasi audit | Konfigurasi terdokumentasi |
| C-10 | Session preservation | Mekanisme teknis & pilot RST | P0 | Perlu keputusan | Diagram + data pilot |
| C-11 | Pengukuran | Probe per WAN, SNMP, Starlink telemetry | P0 | Rekomendasi audit | Tabel instrumen |
| C-12 | Statistik | ANOVA/KW + post hoc; mixed model; effect size | P0 | Rekomendasi audit | Analisis plan |
| C-13 | Confounder | Randomisasi/counterbalancing; staging replay | P1 | Rekomendasi audit | Protokol run |
| C-14 | Platform independence | Kontrak antarmuka + mock adapter | P1 | Perlu keputusan | Uji kesesuaian |
| C-15 | NDLC | Pindahkan analisis ke Evaluation | P2 | Rekomendasi audit | Tabel tahap benar |
| C-16 | Etika & fail-safe | Rollback, watchdog, consent | P0 | Rekomendasi audit | Prosedur diuji |
| C-17 | Tinjauan pustaka | Bab pustaka + gap matrix + sitasi | P0 | Rekomendasi audit | 35–50 refs |
| C-18 | Format | Heading, abstrak, nomor, placeholder | P2 | Rekomendasi audit | Checklist format |
| C-19 | Limitasi | Generalisasi dual-ISP | P1 | Rekomendasi audit | Ditulis di 1.7 |
| C-20 | Judul & abstrak | Kata kunci, kontribusi, posisi | P1 | Perlu keputusan | Selaras dengan isi |

---

## 7. Rencana Kerja Revisi

| Fase | Durasi indikatif | Aktivitas | Luaran |
|---|---|---|---|
| 0. Keputusan lingkup | 2–3 hari | Kunci nama payung, skenario, parameter, baseline | Dokumen scope disetujui |
| 1. Revisi Bab I–II | 1–2 minggu | Rumusan masalah, hipotesis, formalisasi, statistik, pengukuran | Draft 2 |
| 2. Pilot staging | 1–2 minggu | Mock adapter, mekanisme RST, kalibrasi parameter | Laporan pilot |
| 3. Pengujian lapangan | 4–6 minggu | Run A–F counterbalanced, pengumpulan data | Dataset |
| 4. Analisis & penulisan | 3–4 minggu | Statistik, effect size, pembahasan | Draft tesis |

Catatan: jadwal 3 bulan pada draft lama terlalu ketat jika memakai 6 skenario dan pilot RST. Pertimbangkan 4–6 bulan atau kurangi skenario ke minimum A, B, D, F.

---

## 8. Keputusan yang Masih Terbuka

1. **Nama payung:** SPA-HSM, ALQI, atau TLABA? Pilih satu.
2. **Cakupan alokasi:** apakah SPA-HSM hanya berbasis kualitas Q_i, atau juga kapasitas/headroom/utilisasi?
3. **Jumlah state dan rasio:** dua state (STABLE/DEGRADED) atau tambah RECOVERING? Rasio tiap state: 1:1, 2:1, 3:1?
4. **Jumlah bucket N:** 20, 100, atau nilai lain? Bagaimana pembulatan dan sisa bucket?
5. **Platform independence:** klaim atau sekadar design goal?
6. **Jumlah skenario:** 6 (A–F) atau minimum 4 (A, B, D, F)?
7. **Baseline praktisi:** netwatch failover, weighted ECMP, atau keduanya?
8. **Ambang RST:** < 1%, non-inferior, atau selisih absolut?
9. **H3:** perlu atau tidak?
10. **Data Starlink:** apakah telemetry dish tersedia dan diizinkan?
11. **Durasi dan jumlah replikasi:** berapa hari per skenario dan berapa episode degradasi minimum?
12. **Mekanisme “tanpa affinity”:** apa perlakuan teknisnya di RouterOS?

---

## 9. Checklist Revisi

- [ ] Judul dan abstrak selaras dengan K-04.
- [ ] Hanya satu nama algoritma yang dipakai.
- [ ] Rumusan masalah, tujuan, dan hipotesis saling menjawab.
- [ ] Semua simbol dan rumus EWMA/SAW/Q_i/W ada.
- [ ] Tabel parameter dan tabel transisi state tersedia.
- [ ] Skenario ablasi mengisolasi setiap faktor.
- [ ] Baseline praktisi didefinisikan.
- [ ] Definisi flapping, RST rate, dan goodput operasional.
- [ ] Instrumen pengukuran per WAN jelas.
- [ ] Rencana statistik + power analysis ada.
- [ ] Mekanisme session preservation dijelaskan teknis.
- [ ] Fail-safe, rollback, dan etika ada.
- [ ] Tinjauan pustaka dan sitasi lengkap.
- [ ] Format, penomoran, dan placeholder rapi.

---

## Lampiran A — Usulan Parameter SPA-HSM

| Simbol | Arti | Satuan | Nilai/rentang usulan | Cara menetapkan |
|---|---|---|---|---|
| T_s | Interval sampling | detik | 1–5 | ≤ 1/3 durasi transien; uji aliasing |
| α | Koefisien EWMA | — | 0,1–0,3 | Setara window 7–19 sampel; kalibrasi |
| θ_low | Ambang degradasi | skor 0–1 | 0,60–0,70 | Pilot; trade-off flapping vs respons |
| θ_high | Ambang pemulihan | skor 0–1 | 0,80–0,90 | Harus > θ_low |
| k_down | Dwell degradasi | sampel | 2–5 | Cepat, tapi > durasi spike |
| k_up | Dwell pemulihan | sampel | 10–30 | ≫ k_down; cegah recovery semu |
| N | Jumlah bucket PCC | — | 20–100 | Granularitas vs CPU router |
| b_min/b_max | Batas share | % | 15–85 | Availability & eksplorasi |
| W_i | Rasio target | % | Q-based atau Q×H | Keputusan desain |
| ε | Epsilon normalisasi | — | 10⁻⁶ | Hindari 0/0 |

---

## Lampiran B — Skenario Ablasi

| Skenario | Histeresis | Affinity lock | Tujuan |
|---|---|---|---|
| A | Tidak ada (statis 50:50) | — | Baseline |
| B | None | Off | Dynamic naive |
| C | Symmetric | Off | Isolasi bentuk histeresis |
| D | Asymmetric | Off | Isolasi asimetri |
| E | Symmetric | On | Affinity pada simetris |
| F | Asymmetric | On | Proposed SPA-HSM |
| G (opsional) | — | — | PCC + netwatch/health-check |

---

## Lampiran C — Hipotesis dan Uji

| ID | Hipotesis | Variabel | Uji | Kriteria |
|---|---|---|---|---|
| H1 | Histeresis asimetris menurunkan flapping vs none/symmetric | Effective PCC rule change/jam | Poisson/NB atau Kruskal–Wallis + post hoc | Signifikan, arah sesuai, recovery latency ≤ batas |
| H2a | Affinity lock menurunkan RST rate vs tanpa affinity | TCP RST rate | Proporsi/regresi; bootstrap | < 1% atau non-inferior |
| H2b | SPA-HSM meningkatkan goodput & latensi vs statis | Goodput, p95 latency | Mixed-effects/GEE; ANOVA/KW | Signifikan + effect size |
| H3 | Algorithm core portabel | Uji kesesuaian antarmuka | Mock adapter + dua adapter | Keputusan identik |
