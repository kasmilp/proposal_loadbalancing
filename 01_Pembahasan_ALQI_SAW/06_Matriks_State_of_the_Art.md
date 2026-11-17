# 06 — Matriks State of the Art

**Status:** Draf kerja
**Fungsi:** Membandingkan penelitian terdahulu untuk membuktikan adanya kesenjangan,
dengan nilai kuantitatif yang dapat dipertanggungjawabkan.

**Sumber:** arsip `01_Arsip_SPA-HSM_Tahap_01-12/02_Tahap_01_Gap_dan_Novelty/03_Matriks_State_of_the_Art.md`
dan `04_Tahap_03_Kerangka_Teori/05_Register_Referensi.csv` **[FAKTA]**; baris **✱** =
kandidat hasil pencarian OpenAlex 17 Nov 2026 **[perlu verifikasi]**.

**Penomoran:** tabel di bawah menjadi **Tabel 10** pada skema penomoran proposal
(lihat `13_Perbaikan_Proposal_Lama.md` §7).

---

## 1. Tabel Perbandingan Penelitian Terdahulu (Tabel 10)

| # | Penulis, Tahun (DOI) | Metode | Parameter | Hasil kuantitatif | Keterbatasan | Peluang pengembangan |
|---|---|---|---|---|---|---|
| 1 | Amalia et al., 2022 (`10.1016/j.procs.2022.12.116`) | PCC + failover, NDLC, evaluasi TIPHON | delay, jitter, loss, throughput | QoS **3,75** (sibuk), **4,00** (normal); kepuasan 0,4→0,89 | Rasio **statis**; ISP homogen | Skor/pembobotan dinamis |
| 2 | Arfianita et al., 2024 (`10.31763/iota.v4i4.810`) | PCC 3 ISP, GNS3 | throughput, delay, jitter, loss | **+9,32 Mbps**; **−43,54 ms**; **−74,17 ms**; loss 0% | Lab; tanpa skenario degradasi | Uji pada link memburuk |
| 3 | Nugroho et al., 2023 (`10.23887/janapati.v12i1.55894`) | PCC vs ECMP vs NTH | QoS agregat | PCC unggul konsistensi sesi | Statis; tanpa skor komposit | Metrik terpadu |
| 4 | Putra & Anton, 2024 (`10.31326/jisa.v7i1.2022`) | PCC + failover lapangan | QoS agregat | Mengurangi dampak gangguan ISP | Rasio statis | Mekanisme adaptif |
| 5 | Mirsal & Agtriadi, 2026 (`10.37339/e-komtek.v10i1.3170`) | PCC vs Queue Tree | throughput, latency, loss | PCC unggul agregasi kapasitas | Statis | Mekanisme adaptif |
| 6 | Ali et al., 2025 (`10.1109/ACCESS.2025.3529486`) | Hub multi-ISP **ANN** | latency, rate, kongesti, biaya | efisiensi alokasi **±17%** | Butuh training; tak jalan di SOHO; tak transparan | Skoring ringan & auditable |
| 7 | Vafaei et al., 2021 (`10.1016/j.procs.2022.01.156`) | **Studi normalisasi** SAW | dataset MCDM | Normalisasi **mengubah peringkat** signifikan | Dataset **statis**; tanpa deret waktu/outlier | **G-N1**: normalisasi pada data streaming |
| 8 | Wang & Kuo, 2013 (`10.1109/SURV.2012.010912.00044`) | Tutorial MCDM network selection | utility, MADM, fuzzy | MADM paling sesuai untuk seleksi | Domain seluler; bukan rasio WAN | Terjemahkan ke skor link WAN |
| 9 | Tournaire et al., 2023 (`10.1145/3603532`) | Ambang optimal + histeresis | threshold, queue | Ambang identik → **osilasi**; histeresis mencegah | Domain cloud, bukan jaringan | Gerbang kestabilan indeks |
| 10 | Ullah et al., 2025 (`10.1109/vtc2025-spring65109.2025.11174614`) | Pengukuran rain fade | throughput | DL **137→90,2**; UL **20,9→10,5** Mbps | Deskriptif | Masukan bobot kontekstual |
| 11 | Garcia et al., 2025 (`10.1145/3748749.3749090`) | Karakterisasi OWD | one-way delay | Siklus rekonfigurasi **15 detik** | Pengukuran; tanpa mitigasi | Sumber transien untuk uji stabilitas |
| 12 | Hammer et al., 2024 (`10.1145/3697253.3697273`) | Pengukuran edge router | throughput, reordering | Penurunan throughput pada batas 15 dtk | Tanpa kebijakan alokasi | Dampak pada keputusan real-time |
| 13 | Ma et al., 2023 (`10.1109/INFOCOM53939.2023.10228912`) | Pengukuran end-user | throughput, latency, outage | Variabilitas & outage tinggi | Deskriptif-observasional | Mitigasi berbasis pengukuran |
| 14 | Chen et al., 2025 (`10.1016/j.eng.2025.05.012`) | Tinjauan integrasi satelit–terestrial 6G | arsitektur, QoS | Peta tantangan integrasi TN–NTN | Tinjauan konseptual; tanpa mekanisme skoring | Konteks tri-link (1 FO + 2 LEO) & batas klaim |
| 15 | Ji et al., 2026 (`10.1016/j.icte.2026.03.001`) | Tinjauan inter-satellite link LEO | link, handover | Teknologi & aplikasi ISL | Tinjauan; bukan alokasi multi-WAN | Konteks dinamika LEO |
| 16 | Cruvellier et al., 2025 (`10.1109/globecom59602.2025.11432107`) | **DRL** load balancing SD-WAN | goodput | **+48,94%** pada bandwidth asimetris | Simulasi; butuh pembelajaran | Pembanding "berat" |
| 17 ✱ | Wireless Networks, 2021 (`10.1007/s11276-021-02625-y`) | **Entropy + SAW** untuk handover SDN-5G | kriteria handover | (perlu verifikasi) | Domain 5G seluler; bukan skor link WAN 1 FO + 2 LEO | **Pembanding langsung** — sumber diferensiasi |
| 18 ✱ | JNCA, 2022 (`10.1016/j.jnca.2022.103358`) | Evaluasi kontekstual algoritma seleksi | multi-kriteria | (perlu verifikasi) | Fokus seleksi, bukan stabilitas indeks temporal | Kerangka evaluasi indeks |
| 19 ✱ | Symmetry, 2021 (`10.3390/sym13060973`) | Pembobotan objektif **CRITIC** (modifikasi) | kriteria MCDM | Perbaikan metode CRITIC | Domain umum | Kandidat mekanisme bobot |
| 20 ✱ | Symmetry, 2021 (`10.3390/sym13040525`) | Pembobotan objektif **MEREC** | kriteria MCDM | Efek penghapusan kriteria | Domain umum | Kandidat pembanding bobot |
| 21 ✱ | Information, 2023 (`10.3390/info14050285`) | Tinjauan metode bobot MCDM | — | Peta metode subjektif/objektif/hibrida | Tinjauan umum | Landasan Bab II |

---

## 2. Matriks Dimensi (● eksplisit · ◐ sebagian · ○ tidak)

| No | Studi | D1 skor multi-kriteria | D2 penghalusan deret | D3 histeresis/ambang ganda | D4 normalisasi berbatas tetap | **D5 bobot adaptif/objektif** | D6 konteks tri-link |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 1–5 | Studi PCC (Amalia, Arfianita, Nugroho, Putra, Mirsal) | ○ | ○ | ○ | ○ | ○ | ○ |
| 6 | Ali et al. (ANN hub) | ◐ | ○ | ○ | ○ | ○ | ◐ |
| 7 | Vafaei et al. (normalisasi) | ● | ○ | ○ | ○ | ○ | ○ |
| 9 | Tournaire et al. (histeresis) | ○ | ◐ | ● | ○ | ○ | ○ |
| 10–13 | Starlink/LEO (Ullah, Garcia, Hammer, Ma) | ○ | ○ | ○ | ○ | ○ | ◐ |
| 14–15 | Tinjauan satelit 6G (Chen, Ji) | ○ | ○ | ○ | ○ | ○ | ◐ |
| 16 | SD-WAN DRL (Cruvellier) | ◐ | ○ | ○ | ○ | ◐ | ○ |
| 17 ✱ | Entropy-SAW (5G) | ● | ○ | ○ | ○ | ● | ○ |
| — | **Arah penelitian ini** | ● | ● | ◐ | ● | ● | ● |

---

## 3. Bukti Kuantitatif Adanya Kesenjangan **[ANALISIS]**

Dari **21 entri** pada Tabel 10:

- **12 entri** tidak memakai skor komposit multi-kriteria sama sekali — baris **1–5**
  (PCC/load balancing rasio statis), **10–13** (pengukuran Starlink/LEO), **14–15**
  (tinjauan satelit 6G), dan **16** (DRL SD-WAN).
- **1 entri** memakai **pembobotan objektif pada SAW** (baris **17**), tetapi di
  **domain seluler 5G**, bukan tri-link (1 FO + 2 LEO), dan **tidak mengukur stabilitas
  temporal indeks**.
- **1 entri** mengkaji **normalisasi** (baris **7**), tetapi pada **dataset statis**,
  bukan deret metrik bising.
- **0 entri** mengombinasikan **(a) normalisasi berbatas acuan tetap + (b) bobot
  adaptif/hibrida + (c) konteks tri-link (1 FO + 2 LEO) + (d) evaluasi stabilitas temporal**.

**Angka inilah yang dipakai sebagai bukti kesenjangan** — bukan klaim "belum ada".

---

## 4. Celah Matriks yang Harus Diakui **[ANALISIS]**

| Keterbatasan | Dampak | Mitigasi |
|---|---|---|
| Penilaian ●/◐ bersifat kualitatif | Bisa diperdebatkan penguji | Sertakan alasan singkat per sel di lampiran |
| Korpus belum sistematis (baru OpenAlex) | Risiko bias seleksi | Jalankan protokol pencarian lintas basis data |
| 5 baris ✱ belum diverifikasi | Klaim melemah | Verifikasi DOI + teks penuh sebelum sitasi |
| Studi non-Inggris/Indonesia mungkin terlewat | Klaim "belum ada" melemah | Gunakan frasa "berdasarkan pencarian pada …" |
