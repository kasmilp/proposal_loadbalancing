# Pembahasan Baru — ALQI Berbasis SAW

**Status:** Draf kajian awal (belum naskah resmi)
**Fungsi:** Menampung seluruh analisis arah penelitian baru — *Adaptive Link Quality
Index* (ALQI) berbasis *Simple Additive Weighting* (SAW) — sebagai respons atas
penilaian bahwa cakupan **SPA-HSM terlalu luas** untuk diterapkan sebagai sistem
kontroler penuh.
**Latar:** Seluruh alur kerja SPA-HSM (folder 01–12 lama) telah dipindahkan ke
`01_Arsip_SPA-HSM_Tahap_01-12/` dan bersifat **arsip, bukan naskah aktif**.

---

## 1. Cara Membaca

Setiap dokumen di folder ini menyatakan asal pernyataan dengan label:

| Label | Arti |
|---|---|
| **[FAKTA]** | Berasal dari sumber/korpus yang dapat dilacak (standar, jurnal, paten, data repo) |
| **[ANALISIS]** | Penalaran kritis peneliti atas fakta, bukan pernyataan sumber |
| **[USULAN]** | Desain/keputusan penelitian yang diusulkan, belum divalidasi |

Aturan: **tidak ada klaim kebaruan tanpa bukti literatur**, dan klaim "belum ada"
hanya boleh ditulis setelah log pencarian dijalankan (lihat `11_Rencana_Verifikasi_Lanjutan.md`).

---

## 2. Isi Folder

| Berkas | Isi |
|---|---|
| `00_README.md` | Indeks, status, ringkasan eksekutif |
| `00_Bahan_Pengamatan/` | Bahan mentah pengamatan — salinan `Proposal pcc- print.pdf` (naskah lama) |
| `01_Kelayakan_dan_Prior_Art.md` | Putusan kelayakan ALQI–SAW untuk S2 + temuan prior art paten |
| `02_Research_Gap.md` | Gap penelitian berbasis bukti (G-N1, G-N2, G-W1, G-W2) |
| `03_Spesifikasi_Parameter.md` | Parameter QoS teknis, satuan, rentang acuan, arah cost/benefit |
| `04_Analisis_Bobot_SAW.md` | Kriteria benefit/cost, opsi normalisasi, pendekatan bobot |
| `05_Formulasi_ALQI_Adaptif.md` | Formulasi matematis dari statis → adaptif |
| `06_Matriks_State_of_the_Art.md` | Tabel pembanding penelitian terdahulu + nilai kuantitatif |
| `07_Kebaruan_dan_Kontribusi.md` | Klaim kebaruan realistis untuk S2 + batas klaim |
| `08_Rancangan_Eksperimen.md` | Arsitektur, skenario, pembanding, metrik, statistik |
| `09_Rumusan_Masalah_dan_Judul.md` | RQ versi "memodifikasi" + rekomendasi judul |
| `10_Kandidat_Referensi.csv` | Daftar kandidat referensi (perlu verifikasi) |
| `11_Rencana_Verifikasi_Lanjutan.md` | Pekerjaan literatur & teknis yang belum selesai |
| `12_Pengamatan_Proposal_Lama.md` | **Audit** naskah lama: inventaris, temuan editorial/metodologis/klaim/referensi |
| `13_Perbaikan_Proposal_Lama.md` | **Usulan perbaikan** konkret atas temuan tersebut |
| `14_Tahapan_Penelitian.md` | **Roadmap** tahap demi tahap (T0–T10) + gate, jadwal, kriteria lulus |
| `15_Arsitektur_Sistem.md` | **Arsitektur** tri-link: diagram, lapisan, kontrak antarmuka, state machine, deployment |
| `16_Arsitektur_Jaringan_MikroTik.md` | **Desain jaringan Multi-WAN** (3 ISP): PCC, failover, LAN, konfigurasi RouterOS v7 |
| `arsitektur/` | Skrip & gambar: `arsitektur_ALQI_SAW.*` dan `arsitektur_jaringan_mikrotik.*` (`.png`/`.svg`) |

---

## 3. Ringkasan Eksekutif

**[ANALISIS]** Pengembangan ALQI berbasis SAW **layak bersyarat** sebagai fokus tesis
S2. Kelayakannya bergantung pada **pemindahan kebaruan** dari *"menggabungkan metrik
QoS"* (tidak baru) ke *"mekanisme pembobotan dan normalisasi yang adaptif serta
tervalidasi secara empiris"* (masih terbuka).

**Skor kelayakan sementara:**

| Aspek | Bobot | Skor |
|---|---:|---:|
| Ketajaman masalah | 15% | 82 |
| Research gap berbasis bukti | 20% | 68 |
| Kontribusi ilmiah S2 | 20% | 70 |
| Keterukuran parameter | 15% | 90 |
| Kelayakan teknis & ketersediaan data | 15% | 88 |
| Risiko klaim & prior art | 15% | 55 |
| **Agregat berbobot** | **100%** | **± 74** |

Ambang internal: ≥85 layak dengan revisi minor · 75–84 layak dengan perbaikan
terarah · 65–74 perlu revisi mayor · <65 belum layak.
**Putusan: GO dengan perbaikan terarah (penyempitan lingkup wajib).**

**Tiga temuan kunci:**

1. **[FAKTA]** Istilah **ALQI sudah memiliki prior art**: US Patent 9,674,720 B2
   (Crestron Electronics, 2017) mendefinisikan *Application Link Quality Indicator*
   dari banyak indikator QoS, termasuk "modified ALQI" dengan ambang jumlah kejadian.
   Nama dan gagasan dasarnya **tidak boleh diklaim sebagai kebaruan**.
2. **[FAKTA]** Batas acuan parameter tersedia dan terverifikasi: TIPHON
   (ETSI TR 101 329) dan ITU-T Y.1541/G.114.
3. **[FAKTA]** Aset data sudah ada: kolektor baseline *read-only* + dataset **2,2 jam**
   di arsip `11_Kolektor_Baseline/` — memungkinkan studi offline tanpa risiko ke
   pelanggan.

---

## 4. Hubungan dengan Arsip

| Arsip | Isi | Peran |
|---|---|---|
| `00_Arsip_Proposal_SPA-HSM/` | Materi lama (draf Bab I–II ALQI, PDF, jurnal, analisis kelayakan SPA-HSM) | Rujukan historis |
| `01_Arsip_SPA-HSM_Tahap_01-12/` | Alur kerja SPA-HSM: gap, novelty, RQ, teori, metodologi, baseline, presentasi | Rujukan historis |
| `01_Pembahasan_ALQI_SAW/` | **Naskah aktif baru** | Kajian arah penelitian ALQI–SAW |

**Aturan:** dokumen arsip tidak diperbarui. Perubahan arah dicatat di folder ini.

---

## 5. Sinkronisasi dengan `13_Perbaikan_Proposal_Lama.md`

Dokumen **01–11** telah diselaraskan dengan keputusan pada `13_Perbaikan_Proposal_Lama.md`
dan `12_Pengamatan_Proposal_Lama.md`:

| Item yang diselaraskan | Dokumen | Rujukan |
|---|---|---|
| Skenario eksperimen dipisah menjadi **perlakuan sistem (A/B/D/F/G/H)** × **kondisi degradasi (N/T/S/R/K)** | `08` §4–5 | `13` §5 |
| Nilai konkret ambang & dwell ($\theta$ 60/80, $k$ 20/60) | `05` §4, `08` §8 | `13` §10 (M7, M13) |
| Normalisasi: N-a sebagai rumus naskah lama, **N-c** sebagai default alur | `04` §2 | `13` §2.1, §3 |
| H2 dinyatakan kuantitatif (goodput, delay p95) | `09` §2 | `13` §4 |
| Simbol skor tunggal **$Q_i(t)$** (bukan ALQI/$a_i$) | `09` §5 | `13` §9 (K1) |
| Entri **Chen (2025)** & **Ji (2026)** ditambahkan | `06` §1, `10` CSV | `13` §8 (B6) |
| Penomoran tabel proposal (Tabel 7, 8, 10) | `06`, `08` | `13` §7 |
| Lingkup dinyatakan sebagai pilihan Varian A/B/C | `01` §4 | `13` §5, `09` §3 |

Catatan: `13` adalah dokumen perbaikan untuk **naskah lama**; `01`–`11` adalah kajian
arah **baru**. Keduanya kini memakai konvensi yang sama (simbol, skenario, parameter).

---

## 6. Topologi Uji — Revisi (18 Nov 2026)

**[USULAN] Topologi baru:** **tri-link 1 FO + 2 Starlink LEO** (menggantikan
dual-ISP FO–LEO). Pemetaan interface **selaras dengan kolektor baseline**
(`collector.py`, `PROBE_INTERFACES`):

| Link | Interface | ISP (kode) | Teknologi | Peran |
|---|---|---|---|---|
| L-A | `ether1-ISP-A` | ISP-A | **Starlink (LEO-1)** | Link uji |
| L-B | `ether2-ISP-B` | ISP-B | **Starlink (LEO-2)** | Link uji |
| L-C | `ether3-ISP-C` | ISP-C | **Fiber Optic (IndiHome)** | Link uji |

**[ANALISIS]** Penamaan dinormalkan memakai **kode ISP (A/B/C)** — sama dengan
`PROBE_INTERFACES=ether1-ISP-A,ether2-ISP-B,ether3-ISP-C`. Alias "WAN1/2/3" tidak
dipakai lagi agar tidak ada dua sistem label.

**Konsekuensi wajib (diadopsi dari arsip `02_Matriks_Keputusan_Topologi.md` §3):**

1. **K-01/D-14 digantikan** — klaim berubah dari dual-ISP menjadi **tri-link heterogen**.
2. **Judul & Bab I**: "dual-ISP" → "tri-link (1 FO + 2 LEO)".
3. **State machine**: 3 link → **8 kombinasi state**; tabel rasio diperluas.
4. **Bucket mapping**: $N$ dibagi tiga link; perlu $b_{\min}$/$b_{\max}$ baru
   (mis. 2 dan 14 untuk $N=20$) + uji kelayakan.
5. **Analisis**: model harus mengakomodasi **korelasi antar-LEO**.

**⚠️ Syarat ilmiah kritis [ANALISIS].** Dua Starlink berada di **satu lokasi**, sehingga
degradasi keduanya berpotensi **berkorelasi** (rain fade & kontelasi sama). Arsip
mencatat korelasi transien **A–B = 0,68–0,70**, sedangkan ambang kelayakan tri-ISP
di arsip adalah **< 0,7** — jadi nilainya **batas**. Karena itu:
- **Uji independensi transien A–B wajib dilaporkan** (T3/`11`);
- jika korelasi ≥ 0,7, tri-link tidak menambah informasi independen → turunkan ke
  dual-ISP + 2 Starlink sebagai validasi (Opsi 3 arsip);
- klaim "dua sumber degradasi berbeda" harus **dilunakkan** (bukan dua sumber
  independen, melainkan satu FO + dua LEO yang dapat berkorelasi).
