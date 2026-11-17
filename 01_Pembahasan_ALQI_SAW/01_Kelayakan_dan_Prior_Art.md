# 01 — Kelayakan dan Prior Art

**Status:** Draf kerja
**Fungsi:** Menilai apakah ALQI berbasis SAW layak menjadi fokus tesis S2, sekaligus
memetakan prior art yang membatasi klaim.

---

## 1. Objek yang Dinilai

**[FAKTA]** Naskah awal `Proposal pcc- print.pdf` (38 hlm) berjudul *"Pengembangan
Adaptive Link Quality Index (ALQI) Berbasis Simple Additive Weighting (SAW) Dengan
Hysteresis Asimetris Untuk Penyesuaian Rasio Dinamis (Studi Kasus Implementasi Per
Connection Classifier PCC Pada Router Mikrotik)"*. Intinya:

- empat metrik QoS (delay, jitter, packet loss, throughput) → skor komposit **ALQI**;
- skor dihitung dengan **SAW** (bobot statis, contoh 0,30/0,25/0,25/0,20);
- skor digerbangi **histeresis asimetris** (state BAIK/TERDEGRADASI);
- hasil → **rasio PCC dinamis** yang disuntik ke MikroTik via *Server Controller*;
- diuji **kuasi-eksperimental** di jaringan produksi RT/RW Net (FO + Starlink);
- H1: histeresis menurunkan flapping; H2: ALQI menaikkan QoS agregat.

---

## 2. Prior Art yang Harus Dihadapi

### 2.1 **[FAKTA]** Paten ALQI

Berkas arsip `00_Arsip_Proposal_SPA-HSM/jurnal_terkait/00_INDEX/peryataan ALQI.pdf`
bukan artikel jurnal, melainkan **US Patent 9,674,720 B2** (Crestron Electronics,
terbit 6 Juni 2017), *"Wireless Communication Link Debugging"*. Abstraknya:

> *"One or more nodes … substantially continuously monitor a plurality of quality of
> service (QoS) communication indicators and generate a first **application link
> quality indicator (ALQI)** based on a first subset of the plurality of QoS
> communication indicators according to a first time period. The node can then
> **modify the first ALQI** with a second subset of the plurality of QoS communication
> indicators only when a first predetermined **threshold number of occurrences** of the
> second subset … has occurred … to form a first **modified ALQI**."*

**Konsekuensi [ANALISIS]:**

| Aspek | Dampak |
|---|---|
| Akronim **ALQI** | Sudah dipakai pihak lain → jangan diklaim sebagai kebaruan istilah |
| Gagasan "indeks dari banyak indikator QoS" | Prior art (2017) → bukan kebaruan |
| "modified ALQI" dengan **ambang jumlah kejadian** | Sangat dekat dengan gagasan *dwell*/histeresis → harus dibedakan eksplisit |

**Tindakan [USULAN]:**
1. Istilah ALQI **tidak** dipakai sebagai klaim; gunakan simbol $Q_i(t)$ (skor
   kualitas link) atau nama generik lain.
2. Jika istilah tetap dipakai, wajib disitasi sebagai *related prior art* dan
   dibedakan secara tegas.
3. Konsisten dengan keputusan arsip **K-05** (ALQI tidak dipakai sebagai nama sistem).

### 2.2 **[FAKTA]** SAW dan MCDM untuk seleksi jaringan

Wang & Kuo (2013) — tutorial MCDM *network selection* di jaringan nirkabel
heterogen — menempatkan SAW sebagai salah satu pendekatan yang mapan. Studi
*entropy-based SAW* untuk handover SDN–5G (Wireless Networks, 2021,
`10.1007/s11276-021-02625-y`) memperlihatkan pembobotan objektif pada SAW **sudah
ada**. Karena itu: **[ANALISIS]** klaim "pertama memakai SAW / bobot objektif untuk
skor kualitas link" **tidak dapat dipertahankan**.

### 2.3 **[FAKTA]** Normalisasi mengubah hasil

Vafaei et al. (2021) membuktikan teknik normalisasi **mengubah peringkat akhir SAW
secara signifikan** — tetapi pada **dataset MCDM statis**. Ini justru dasar gap
(lihat `02_Research_Gap.md`, G-N1).

---

## 3. Putusan Kelayakan

### 3.1 Yang membuat layak **[ANALISIS]**

1. Masalah nyata dan terukur: jaringan **tri-link (1 FO + 2 Starlink LEO)** dengan
   dua *jenis* sumber degradasi (kongesti operasional pada FO; transien/rain fade
   pada LEO) — dengan catatan korelasi antar-LEO harus diuji (lihat `00_README.md` §6).
2. Parameter punya batas acuan baku (TIPHON/Y.1541/G.114) → dapat diukur.
3. Aset teknis tersedia: router RB1100AHx4, **dua Starlink + FO IndiHome**, kolektor
   baseline, dataset 2,2 jam → eksperimen offline & staging mungkin.
4. Celah metode yang jelas: normalisasi & pembobotan **belum diuji pada deret metrik
   link real-time yang bising** (bukan dataset statis).

### 3.2 Yang membuat berisiko **[ANALISIS]**

1. Nama ALQI = prior art.
2. Jika novelty = "integrasi", akan dinilai inkremental (lihat matriks SOTA: kolom
   "skor multi-kriteria" sudah ramai).
3. Klaim "belum ada" belum diverifikasi lintas basis data (baru OpenAlex).
4. Bila tetap mempertahankan "controller eksternal penuh", cakupan kembali luas —
   bertentangan dengan alasan penyempitan.

### 3.3 Skor per aspek

| Aspek | Bobot | Skor | Alasan singkat |
|---|---:|---:|---|
| Ketajaman masalah | 15% | 82 | Nyata, tetapi "skor kualitas" saja terlalu umum |
| Research gap berbasis bukti | 20% | 68 | Gap metode perlu bukti pencarian lanjutan |
| Kontribusi ilmiah S2 | 20% | 70 | Layak bila berupa studi komparatif + validasi |
| Keterukuran parameter | 15% | 90 | Batas acuan standar tersedia |
| Kelayakan teknis & data | 15% | 88 | Perangkat + dataset baseline 2,2 jam tersedia |
| Risiko klaim & prior art | 15% | 55 | Paten ALQI; klaim "belum ada" belum diverifikasi |
| **Agregat** | **100%** | **± 74** | |

**Putusan [ANALISIS]: LAYAK BERSYARAT (GO dengan penyempitan lingkup).**

---

## 4. Syarat Kelayakan (harus dipenuhi sebelum Bab I dikunci)

| Kode | Syarat | Bukti pemenuhan |
|---|---|---|
| S-1 | Kebaruan dipindah ke **mekanisme pembobotan/normalisasi adaptif**, bukan integrasi | Pernyataan novelty di `07_Kebaruan_dan_Kontribusi.md` |
| S-2 | Istilah ALQI ditangani sebagai prior art atau diganti | Draf Bab II menyitasi US 9,674,720 B2 |
| S-3 | Lingkup dipilih secara eksplisit (Varian A/B/C) — idealnya modul penilaian kualitas link | RQ & varian di `09_Rumusan_Masalah_dan_Judul.md`; desain di `08_Rancangan_Eksperimen.md` |
| S-4 | Ada pembanding eksplisit (statis, sama-rata, entropy-SAW, metrik tunggal) | `08_Rancangan_Eksperimen.md` |
| S-5 | Klaim "belum ada" diganti "belum dievaluasi pada konteks X" | `02_Research_Gap.md` |
| S-6 | Log pencarian lintas basis data dijalankan | `11_Rencana_Verifikasi_Lanjutan.md` |
| S-7 | Topologi tri-link (1 FO + 2 LEO) dengan **uji independensi antar-Starlink** dan analisis korelasi | `00_README.md` §6; `08` §1 |

---

## 5. Batas Klaim **[USULAN]**

- **Bukan** metode MCDM baru.
- **Bukan** "pertama memakai SAW" atau "pertama memakai bobot objektif".
- **Bukan** kebaruan istilah ALQI.
- Generalisasi dibatasi: **tri-link 1 FO + 2 LEO** (bukan semua WAN), satu lokasi
  skala kecil, QoS ≠ QoE.
- Bobot SAW: jika tetap statis, jangan menyebut sistem "adaptif" tanpa penjelasan.
