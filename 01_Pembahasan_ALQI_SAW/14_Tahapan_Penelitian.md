# 14 — Tahapan Penelitian (Roadmap)

**Status:** Draf kerja (rencana)
**Fungsi:** Menyusun langkah penelitian **tahap demi tahap** untuk arah ALQI–SAW
sehingga setiap tahap punya masukan, aktivitas, luaran, dan **kriteria lulus** yang
jelas.
**Acuan:** `01`–`13` pada folder ini, serta arsip
`01_Arsip_SPA-HSM_Tahap_01-12/` (baseline, statistik, protokol).

**Konvensi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]** (sama seperti `00_README.md`).

---

## 1. Prinsip Penyusunan

1. **Bertahap dengan gerbang (gate).** Tahap tidak dilanjutkan sebelum kriteria lulus
   tahap sebelumnya terpenuhi.
2. **Bukti dulu, klaim kemudian.** Klaim kebaruan baru ditulis setelah tahap
   verifikasi literatur (`T1`) dan uji offline (`T6`) memberi bukti.
3. **Risiko menurun ke pelanggan.** Eksperimen disusun berlapis: **L0 (data)** →
   **L1 (offline)** → **L2 (staging)** → **L3 (lapangan, opsional)**.
4. **Setiap parameter diberi angka.** Tidak boleh ada simbol tanpa nilai (temuan
   M7/M13 di `12_Pengamatan_Proposal_Lama.md`).
5. **Satu konvensi.** Simbol $Q_i(t)$, topologi **tri-link (1 FO + 2 LEO)**, skenario
   perlakuan A/B/D/F/G/H, kondisi N/T/S/R/K, penomoran tabel (`13` §7).

---

## 2. Peta Tahapan (Ringkasan)

| Tahap | Nama | Luaran utama | Kriteria lulus | Estimasi |
|---|---|---|---|---:|
| **T0** | Pembekuan lingkup & keputusan | Catatan keputusan terkunci | Semua item D-1…D-6 punya nilai | 3–5 hari |
| **T1** | Studi literatur & verifikasi prior art | Register referensi + log pencarian | ≥ 15 SOTA inti terverifikasi; prior art ALQI ditangani | 2–3 mgg |
| **T2** | Spesifikasi parameter & instrumen | Spesifikasi parameter & prosedur | Tiap variabel punya satuan+alat+prosedur | 1 mgg |
| **T3** | Akuisisi & konsolidasi data (L0) | Dataset bersih + label episode | Lolos sanity check (rentang, missing, sampling) | 1–2 mgg |
| **T4** | Formalisasi & perancangan | Spesifikasi teknis + diagram | Cukup rinci untuk diimplementasikan | 1–2 mgg |
| **T5** | Implementasi prototipe | Artefak perangkat lunak + tes | Unit test lulus; skoring ≤ 1 s; deterministik | 2–3 mgg |
| **T6** | Eksperimen L1 — offline/replay | Tabel & grafik hasil | Hipotesis kerja dapat dievaluasi | 2 mgg |
| **T7** | Eksperimen L2 — staging | Dataset staging + hasil | Efek gerbang terukur; tanpa artefak | 2–3 mgg |
| **T8** | Eksperimen L3 — lapangan (opsional) | Data lapangan | Izin lengkap; tanpa gangguan pelanggan | 2–4 mgg |
| **T9** | Analisis statistik & pembuktian | Bab analisis + bukti | Primary outcome terjawab; effect size ada | 2 mgg |
| **T10** | Penulisan & seminar | Naskah + slide | Konsistensi naskah; checklist `13` §10 | 3–4 mgg |
| | | | **Total** | **± 18–24 mgg** |

**Gerbang (gate):** G0 setelah T1 · G1 setelah T5 · G2 setelah T7 · G3 setelah T9.

---

## 3. Rincian Tahap

### T0 — Pembekuan Lingkup & Keputusan

- **Tujuan:** mengunci keputusan yang membatasi seluruh pekerjaan, agar tidak berubah
  tanpa jejak (kebiasaan baik dari arsip `01_Log_Keputusan.md`).
- **Masukan:** `01_Kelayakan_dan_Prior_Art.md`, `07_Kebaruan_dan_Kontribusi.md`,
  `09_Rumusan_Masalah_dan_Judul.md`, `11_Rencana_Verifikasi_Lanjutan.md`.
- **Aktivitas:** mengisi keputusan **D-1…D-6** (`11` §4): varian lingkup (A/B/C),
  nama istilah, skema bobot, normalisasi default, primary outcome, keterlibatan
  lapangan.
- **Luaran:** tabel keputusan terkunci + tanggal + alasan.
- **Kriteria lulus:**
  - [ ] Varian lingkup dipilih (A = luas, B = skoring, C = tengah).
  - [ ] Istilah ditetapkan (ganti ALQI / pertahankan + prior art).
  - [ ] Skema bobot & normalisasi default ditetapkan.
  - [ ] Primary outcome + *smallest effect of interest* ditetapkan.
- **Alat:** dokumen keputusan (Markdown).
- **Risiko:** lingkup melebar → mitigasi: batasi pada luaran T0.
- **Estimasi:** 3–5 hari.

---

### T1 — Studi Literatur & Verifikasi Prior Art

- **Tujuan:** menutup klaim gap dengan bukti **dan** menangani prior art ALQI.
- **Masukan:** `02_Research_Gap.md`, `06_Matriks_State_of_the_Art.md`,
  `10_Kandidat_Referensi.csv`.
- **Aktivitas:**
  - V-1…V-8 (`11` §1): pencarian di Scopus/IEEE/ACM/ScienceDirect (bukan hanya
    OpenAlex), verifikasi DOI, baca teks penuh kandidat kunci.
  - PA-1…PA-3 (`11` §2): salin & bahas **US 9,674,720 B2** sebagai *related prior art*.
  - Snowballing dari 10 paper inti.
- **Luaran:** register referensi final + log pencarian (tanggal, string, hit) + draf
  subbab "posisi penelitian".
- **Kriteria lulus:**
  - [ ] ≥ 15 referensi SOTA inti terverifikasi (T1).
  - [ ] Semua klaim "belum ada" ditulis dengan frasa **"berdasarkan pencarian pada …"**.
  - [ ] Prior art ALQI disitasi & dibedakan.
  - [ ] Setiap klaim di Bab II punya entri sumber (adopsi tabel klaim arsip).
- **Alat:** Scopus/IEEE Xplore/ACM DL/ScienceDirect/OpenAlex, Zotero/Mendeley.
- **Risiko:** ada studi adaptif terlewat → mitigasi: minimal 2 kombinasi string + snowballing.

---

### T2 — Spesifikasi Parameter & Instrumen

- **Tujuan:** memastikan semua variabel terukur dan dapat direplikasi.
- **Masukan:** `03_Spesifikasi_Parameter.md`, `04_Analisis_Bobot_SAW.md`.
- **Aktivitas:**
  - Tetapkan **topologi tri-link**: `ether1-ISP-A` = Starlink LEO-1,
    `ether2-ISP-B` = Starlink LEO-2, `ether3-ISP-C` = FO IndiHome (`00_README.md` §6).
  - Finalisasi parameter (P1–P12), satuan, rentang acuan (TIPHON/Y.1541/G.114).
  - Definisi operasional: **flapping** (flap/jam, jendela $W$), **ELS**,
    *time-to-rebalance*, **RST flow**, *share error*.
  - Prosedur sampling & sinkronisasi waktu; protokol anonimisasi data.
- **Luaran:** dokumen spesifikasi parameter & instrumen.
- **Kriteria lulus:**
  - [ ] Tiap variabel: definisi + satuan + instrumen + prosedur.
  - [ ] Semua ambang & dwell punya angka ($\theta$ 60/80; $k$ 20/60; $W$=5 mnt).
  - [ ] Prosedur etika & anonimisasi disetujui.
- **Alat:** `collector.py` (librouteros API-SSL), `ping`/iPerf3, dokumentasi RouterOS.
- **Risiko:** instrumen tidak tersedia → mitigasi: fallback ke metrik terukur router.

---

### T3 — Akuisisi & Konsolidasi Data (L0)

- **Tujuan:** menyiapkan bahan uji offline yang bersih.
- **Masukan:** dataset baseline arsip (`11_Kolektor_Baseline/data/*.jsonl`),
  kolektor `collector.py`.
- **Aktivitas:**
  - Inventaris dataset (**2,2 jam**, 13 Nov 2026) **[FAKTA arsip]**.
  - **Uji independensi** dua Starlink (korelasi transien LEO-1–LEO-2; ambang < 0,7)
    sebagai prasyarat tri-link.
  - Ekstraksi & pembersihan metrik (delay, jitter, loss, throughput); cek missing.
  - **Pelabelan episode** (normal/transien/sustain) dan penyusunan *ground truth*
    (goodput).
  - Pembuatan **data sintetis** pola transien 15 dtk & degradasi bertahap untuk L1/L2.
- **Luaran:** dataset bersih + skema label + dokumentasi versi data.
- **Kriteria lulus:**
  - [ ] Sanity check lolos (rentang, outlier, resolusi sampling).
  - [ ] Label episode tersedia & konsisten.
  - [ ] Data teranonim (tanpa identitas pelanggan).
- **Alat:** Python (pandas/NumPy), `tc/netem` untuk replay.
- **Risiko:** episode degradasi asli jarang → mitigasi: data sintetis + staging.

---

### T4 — Formalisasi & Perancangan (Design)

- **Tujuan:** merumuskan indeks dan arsitektur secara lengkap.
- **Masukan:** `04_Analisis_Bobot_SAW.md`, `05_Formulasi_ALQI_Adaptif.md`,
  `08_Rancangan_Eksperimen.md`.
- **Aktivitas:**
  - Tetapkan satu alur baku (`13` §3):
    `metrik → EWMA → normalisasi (batas tetap) → SAW+bobot adaptif → $Q_i(t)$ → gerbang histeresis`.
  - Rumuskan rumus final (normalisasi, bobot entropy/CRITIC/hibrida, gerbang).
  - Rancang **state machine 3 link (8 kombinasi status)** dan **bucket mapping** $N$
    tiga link ($b_{\min}$/$b_{\max}$, mis. 2/14 untuk $N=20$).
  - Rancang spesifikasi antarmuka (read_metrics, compute, decide) + *mock adapter*.
  - Rancang skema basis data metrik (timestamp, link, metrik, $Q$, status, rasio).
- **Luaran:** spesifikasi teknis + diagram arsitektur & *state machine*.
- **Kriteria lulus:**
  - [ ] Tidak ada ambiguitas letak komponen (menutup temuan M14).
  - [ ] Semua rumus diberi definisi variabel & rentang.
  - [ ] Kontrak antarmuka lengkap.
- **Alat:** Markdown/diagram (draw.io/matplotlib).
- **Risiko:** desain terlalu luas → mitigasi: ikuti varian T0.

---

### T5 — Implementasi Prototipe (*Scoring Engine*)

- **Tujuan:** mewujudkan desain menjadi perangkat lunak yang dapat diuji.
- **Masukan:** luaran T4 + dataset T3.
- **Aktivitas:**
  - Implementasi modul: penghalusan, normalisasi, pembobotan (statis/objektif/hibrida),
    gerbang histeresis.
  - *Unit test* + uji determinisme (input sama → keluaran sama).
  - Instrumentasi logging untuk audit.
- **Luaran:** artefak perangkat lunak + dokumentasi + laporan tes.
- **Kriteria lulus:**
  - [ ] Unit test lulus.
  - [ ] Waktu skoring ≤ 1 detik per siklus.
  - [ ] Deterministik (uji ulang menghasilkan keluaran identik).
  - [ ] Berjalan pada data nyata tanpa error.
- **Alat:** Python 3.11, Git, virtualenv.
- **Risiko:** bug pembobotan → mitigasi: test case contoh (FO 91,3 / LEO 53,3 pada
  bobot lama sebagai *golden test*).

---

### T6 — Eksperimen L1 (Offline / Replay)

- **Tujuan:** validasi konstruk indeks dan **perbandingan normalisasi × pembobotan**.
- **Masukan:** prototipe T5 + dataset T3.
- **Aktivitas:**
  - Jalankan seluruh kombinasi (N-a/N-b/N-c) × (statis/sama-rata/entropy/CRITIC/MEREC/hibrida).
  - Hitung metrik: Spearman $\rho$, *rank reversal*, *chattering rate*, AUC.
  - Analisis sensitivitas ($\gamma$, $\alpha$, $N$).
- **Luaran:** tabel & grafik hasil (siap masuk Bab hasil).
- **Kriteria lulus:**
  - [ ] Kesenjangan terukur antar-metode terlihat jelas.
  - [ ] Teridentifikasi satu konfigurasi terbaik (akurasi vs stabilitas).
  - [ ] Hasil dapat direproduksi dari skrip.
- **Alat:** pustaka statistik Python (scipy/statsmodels), plotting.
- **Risiko:** hasil tidak konklusif → mitigasi: perluas grid sensitivitas.

---

### T7 — Eksperimen L2 (Staging Terkendali)

- **Tujuan:** validasi internal kausal (sebab-akibat) dengan pola degradasi terkendali.
- **Masukan:** luaran T5–T6; lingkungan staging.
- **Aktivitas:**
  - Susun **perlakuan sistem** (A/B/D/F/G/H) × **kondisi** (N/T/S/R/K) (`08` §4).
  - Injeksi pola via `tc/netem` (transien 15 dtk, degradasi bertahap).
  - Ulangan 30–64×, urutan diacak/*counterbalanced*, diblok per jam.
  - Ukur: flapping, *recovery latency*, ELS, *time-to-rebalance*, RST flow.
- **Luaran:** dataset staging + hasil efek perlakuan.
- **Kriteria lulus:**
  - [ ] Efek gerbang (B vs D vs F) terukur & signifikan arah.
  - [ ] Tidak ada artefak (mis. *reordering* tak wajar).
  - [ ] Protokol dapat diulang.
- **Alat:** staging Linux, `tc/netem`, skrip otomasi.
- **Risiko:** lingkungan tidak representatif → mitigasi: kalibrasi dengan data lapangan.

---

### T8 — Eksperimen L3 (Lapangan, Opsional)

- **Tujuan:** validasi eksternal pada jaringan produksi nyata.
- **Masukan:** freeze prototipe; izin bertulis; prosedur rollback.
- **Aktivitas:**
  - Izin pemilik RT/RW Net + pemberitahuan pelanggan; kepatuhan ToS ISP.
  - Mulai dari **mode pantau pasif**, lalu aktivasi bertahap.
  - *Fail-static*, *watchdog*, snapshot & rollback; jam rendah risiko.
- **Luaran:** data lapangan + catatan insiden + log rollback (bila ada).
- **Kriteria lulus:**
  - [ ] Izin & kepatuhan lengkap.
  - [ ] Tidak ada gangguan terukur bagi pelanggan.
  - [ ] Prosedur rollback terbukti berjalan.
- **Alat:** RB1100AHx4, **dua Starlink + 1 FO**, akun API tulis terpisah, UPS.
- **Risiko:** cuaca/izin → mitigasi: buffer 2–3 minggu; klaim tetap sah tanpa L3.

---

### T9 — Analisis Statistik & Pembuktian

- **Tujuan:** menjawab hipotesis secara sahih dan atributif.
- **Masukan:** data T6–T8.
- **Aktivitas:**
  - Satuan analisis = **episode/jam** (bukan tiap siklus) — menutup M4/M6.
  - Uji: **mixed-effects/GEE**, **Poisson/negative binomial** (cacah flapping),
    ANOVA/Kruskal–Wallis + post hoc.
  - **Effect size + 95% CI**, koreksi **Holm**, **bootstrap**.
  - Analisis dekomposisi (normalisasi vs bobot vs gerbang) untuk H3.
- **Luaran:** bab analisis + tabel efek + visualisasi.
- **Kriteria lulus:**
  - [ ] Primary outcome terjawab dengan effect size & CI.
  - [ ] Kontribusi komponen dapat diatribusikan (ablasi).
  - [ ] Analisis sensitivitas dilaporkan sebagai eksplorasi (bukan konfirmatori).
- **Alat:** statsmodels, R (opsional).
- **Risiko:** p-hacking → mitigasi: pra-registrasi rencana analisis.

---

### T10 — Penulisan Naskah & Seminar

- **Tujuan:** menyusun naskah proposal/tesis dan bahan seminar.
- **Masukan:** semua luaran T0–T9.
- **Aktivitas:**
  - Bab I (latar belakang, RQ, tujuan, hipotesis, batasan) — dari `09`.
  - Bab II (tinjauan pustaka + posisi) — dari `06`, `T1`.
  - Bab III (metodologi) — dari `08`, `T4`.
  - Lampiran historis: terapkan checklist `13` §10 pada naskah lama.
  - Deck presentasi + latihan tanya-jawab.
- **Luaran:** naskah + slide + artefak.
- **Kriteria lulus:**
  - [ ] Konsistensi RQ ↔ hipotesis ↔ metode ↔ luaran.
  - [ ] Semua sitasi ↔ daftar pustaka konsisten.
  - [ ] Batas klaim dinyatakan eksplisit.
- **Alat:** LaTeX/Word + pedoman penulisan kampus.
- **Risiko:** waktu menipis → mitigasi: turunkan ke Varian B (skoring saja).

---

## 4. Peta Tahap ↔ Bab Naskah

| Tahap | Bab I | Bab II | Bab III | Hasil |
|---|:--:|:--:|:--:|:--:|
| T0 Keputusan | ● | ○ | ○ | ○ |
| T1 Literatur | ◐ | ● | ○ | ○ |
| T2 Parameter | ○ | ◐ | ● | ○ |
| T3 Data | ○ | ○ | ● | ● |
| T4 Desain | ○ | ○ | ● | ○ |
| T5 Implementasi | ○ | ○ | ● | ◐ |
| T6–T8 Eksperimen | ○ | ○ | ● | ● |
| T9 Analisis | ○ | ○ | ◐ | ● |
| T10 Penulisan | ● | ● | ● | ● |

*(● utama · ◐ sebagian · ○ tidak langsung)*

---

## 5. Peta Tahap ↔ NDLC (kesinambungan dengan naskah lama)

| NDLC (naskah lama) | Tahap baru |
|---|---|
| Analysis | T0–T2 |
| Design | T4 (dan T3 untuk data) |
| Simulation Prototyping | T5–T6 |
| Implementation | T7 (staging) → T8 (lapangan) |
| Monitoring | T7–T8 |
| Management | T9–T10 |

**[ANALISIS]** Pemetaan ini mempertahankan kerangka NDLC yang sudah dipakai naskah
lama, tetapi **memisahkan** validasi offline/staging dari lapangan — perbaikan atas
temuan M9 (`12_Pengamatan_Proposal_Lama.md`).

---

## 6. Jadwal (Minggu Relatif)

| Minggu | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| T0 | █ | █ | | | | | | | | | | | | | | | | | | |
| T1 | | █ | █ | █ | | | | | | | | | | | | | | | | |
| T2 | | | | █ | █ | | | | | | | | | | | | | | | |
| T3 | | | | | █ | █ | | | | | | | | | | | | | | |
| T4 | | | | | | █ | █ | | | | | | | | | | | | | |
| T5 | | | | | | | | █ | █ | █ | | | | | | | | | | |
| T6 | | | | | | | | | | █ | █ | | | | | | | | | |
| T7 | | | | | | | | | | | █ | █ | █ | | | | | | | |
| T8 | | | | | | | | | | | | | | █ | █ | █ | | | | |
| T9 | | | | | | | | | | | | | | | | | █ | █ | | |
| T10 | | | | | | | | | | | | | | | | | | | █ | █ |

**Catatan [USULAN]:** T8 hanya dijalankan bila izin & cuaca memungkinkan; tanpa T8,
total menjadi ± 16 minggu.

---

## 7. Gerbang Keputusan (Gate)

| Gate | Setelah | Pertanyaan kunci | Jika gagal |
|---|---|---|---|
| **G0** | T1 | Apakah gap & prior art sudah tertangani? | Perluas pencarian; mungkin ganti sudut kebaruan |
| **G1** | T5 | Apakah prototipe berjalan & deterministik? | Perbaiki; turunkan cakupan fitur |
| **G2** | T7 | Apakah efek gerbang terukur di staging? | Perbaiki parameter; ulang ulangan |
| **G3** | T9 | Apakah primary outcome terjawab? | Turunkan klaim; laporkan non-inferioritas |

---

## 8. Risiko Utama & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Lingkup melebar | Jadwal meleset | Kunci Varian di T0; turunkan ke Varian B bila perlu |
| Prior art ALQI | Klaim gugur | Tangani di T1; ganti istilah |
| Episode degradasi langka | Data kurang | Data sintetis + staging (L2) |
| Izin lokasi/ToS | L3 batal | Klaim tetap sah tanpa L3 |
| Hasil tidak konklusif | Kebaruan lemah | Perluas sensitivitas; fokus studi komparatif |
| Bug pembobotan | Hasil salah | Golden test + unit test (T5) |
| **Dua Starlink berkorelasi** | Tri-link tidak menambah informasi | Uji independensi (T3, T-6); fallback ke dual-ISP + validasi tri |

---

## 9. Definition of Done (ringkas)

Sebuah tahap **selesai** bila: (1) seluruh kriteria lulus dicentang, (2) luaran
tersimpan & berversi, (3) keputusan yang diambil dicatat, dan (4) gate terkait (bila
ada) dinyatakan lolos.

---

## 10. Checklist Progres

- [ ] T0 — Lingkup & keputusan dikunci
- [ ] T1 — Literatur & prior art terverifikasi (G0)
- [ ] T2 — Spesifikasi parameter & instrumen
- [ ] T3 — Dataset L0 siap
- [ ] T4 — Formalisasi & perancangan
- [ ] T5 — Prototipe lulus tes (G1)
- [ ] T6 — Eksperimen L1 selesai
- [ ] T7 — Eksperimen L2 selesai (G2)
- [ ] T8 — Eksperimen L3 (opsional)
- [ ] T9 — Analisis & pembuktian (G3)
- [ ] T10 — Naskah & seminar

---

## 11. Langkah Berikutnya (tindakan langsung)

1. Jalankan **T0** — pilih Varian lingkup (A/B/C) dan isi keputusan D-1…D-6 di `11` §4.
2. Jalankan **T1** — verifikasi literatur lintas basis data + prior art (`11` §1–2).
3. Setelah G0 lolos, mulai **T2** dan **T3** (spesifikasi + data).
