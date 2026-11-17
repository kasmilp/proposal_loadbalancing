# 12 — Pengamatan atas `Proposal pcc- print.pdf`

**Status:** Draf kerja (audit)
**Fungsi:** Menjadikan naskah lama `Proposal pcc- print.pdf` sebagai **objek
pengamatan**, mendokumentasikan isinya dan menemukan kelemahan yang harus diperbaiki.
**Berkas bahan:** `00_Bahan_Pengamatan/Proposal pcc- print.pdf` (salinan; asli tetap di
`00_Arsip_Proposal_SPA-HSM/`).

**Konvensi label:** **[FAKTA]** = isi naskah apa adanya · **[ANALISIS]** = penilaian
kritis · **[USULAN]** = tindakan perbaikan.

---

## 1. Identitas Berkas **[FAKTA]**

| Item | Isi |
|---|---|
| Judul | *Pengembangan Adaptive Link Quality Index (ALQI) Berbasis Simple Additive Weighting (SAW) Dengan Hysteresis Asimetris Untuk Penyesuaian Rasio Dinamis (Studi Kasus Implementasi Per Connection Classifier PCC Pada Router Mikrotik)* |
| Penulis | Kasmil Papalia — D082252011 |
| Program | Magister Teknik Informatika, Universitas Hasanuddin, 2026 |
| Jumlah halaman | 38 (PDF); isi naskah ≈ 32 halaman |
| Struktur | Bab I Pendahuluan (1.1–1.7), Bab II Metodologi (2.1–2.7), Daftar Pustaka, Lampiran (State of the Art) |
| Tabel | 9 (menurut Daftar Tabel) |
| Gambar | 11 (menurut Daftar Gambar) |
| Rujukan | 21 entri |

---

## 2. Inventaris Isi **[FAKTA]**

| Bagian | Hal. PDF | Muatan |
|---|---:|---|
| Sampul, pengesahan, daftar isi/tabel/gambar | 1–6 | — |
| 1.1 Latar Belakang | 7–9 | FO vs LEO; PCC statis; usulan ALQI; histeresis |
| 1.2 Tinjauan Pustaka 1.2.1–1.2.10 | 9–15 | QoS, FO/LEO, MikroTik, PCC, perbandingan LB, MCDM, SAW, histeresis, integrasi ALQI |
| 1.3 Rumusan Masalah | 15 | *"Bagaimana merancang dan mengimplementasikan ALQI…"* |
| 1.4 Hipotesis | 15 | H1 (flapping turun), H2 (QoS agregat naik) |
| 1.5–1.7 Tujuan, Manfaat, Batasan | 15–17 | 4 tujuan; 2 manfaat; 7 batasan |
| 2.1–2.2 Jenis, Waktu, Lokasi | 18–19 | R&D + kuasi-eksperimental; NDLC; lokasi Desa Waeura, Buru, Maluku |
| 2.3 Tahapan NDLC | 20–21 | Analysis→Design→Prototyping→Implementation→Monitoring→Management |
| 2.4 Perangkat | 21–22 | RB1100AHx4, Starlink, PC, RouterOS 7.22.2, Python 3.11.9 |
| 2.5 Perancangan Sistem | 23–28 | Arsitektur, DB, rumus SAW, histeresis, formulasi rasio, flowchart |
| 2.6 Skenario Percobaan | 28–29 | Variabel; 3 skenario A/B/C; pengujian terkendali `tc/netem` |
| 2.7 Analisis Data | 29–31 | Deskriptif, normalitas, uji hipotesis, flapping, stratifikasi |
| Daftar Pustaka | 32–33 | 21 rujukan |
| Lampiran — State of the Art | 34–36 | 12 baris ringkasan + tabel peneliti |
| Lampiran — tabel peneliti | 37–38 | 21 entri |

**Inti teknis [FAKTA]:** 4 metrik QoS → normalisasi cost/benefit → skor SAW →
gerbang histeresis 2-state → rasio PCC proporsional → disuntik ke MikroTik via
*Controller* eksternal.

---

## 3. Pengamatan Editorial **[ANALISIS]**

| Kode | Lokasi | Masalah | Bukti | Dampak |
|---|---|---|---|---|
| E1 | Hal. 25 | Judul **"Tabel 5. Bobot Ilustratif throughput"** tidak cocok isinya | Isi = data metrik FO/LEO (delay/jitter/loss/throughput) | Membingungkan pembaca |
| E2 | Hal. 22 (2.4.1, 2.4.2) | Rujukan tabel di badan ≠ Daftar Tabel | Badan: "Tabel 4"/"Tabel 5"; Daftar: Tabel 2/3 | Penomoran tidak konsisten |
| E3 | Hal. 24 (2.5.3) | Rumus $s_i$ **tidak memberi bobot pada suku packet loss** | $s_i = w_D r_D + w_J r_J + r_{PL} + w_T r_T$ (tanpa $w_{PL}$) | Rumus salah secara matematis |
| E4 | Hal. 25 | `W_T = 020` (hilang koma) | seharusnya 0,20 | Kesalahan angka |
| E5 | Hal. 13–14 | **Gambar 4 & Gambar 5 bertajuk sama**: "Diagram Integrasi ALQI" | Daftar Gambar juga duplikat | Duplikasi judul |
| E6 | Hal. 23, 26 | Gambar 8 & Gambar 10 bertajuk hampir sama; Gambar 10 ditempatkan di subbab histeresis tetapi bertajuk "Arsitektur Sistem" | — | Gambar tidak sesuai konteks |
| E7 | Hal. 34 (Lampiran) | Menyebut **"Tabel 12"** padahal tidak ada Tabel 10–11 | — | Penomoran melompat |
| E8 | Hal. 10 (1.2.2) | Karakter rusak `�550 km` | seharusnya "≈550 km" | Kesalahan enkoding |
| E9 | Hal. 16 (1.5) | Salah ketik "di **ataranya**" | seharusnya "di antaranya" | Kesalahan ketik |
| E10 | Hal. 21–22 | Placeholder belum diisi: `[isi model, kapasitas paket IndiHome]`, `[isi, mis. SQLite / InfluxDB]` | — | Naskah belum lengkap |
| E11 | Hal. 28 (Tabel 7) | Judul "Skenario Percobaan" tetapi isi = variabel penelitian | — | Judul tidak cocok |
| E12 | Hal. 18-19 | "Tabel 1. Jadwal penelitian selama 3 bulan" tetapi tahap ditulis 3 bulan | konsisten; namun durasi 3 bulan tidak realistis untuk seluruh NDLC + analisis | Rencana waktu janggal |

---

## 4. Pengamatan Metodologis **[ANALISIS]** — inilah yang paling penting

| Kode | Lokasi | Masalah | Mengapa bermasalah |
|---|---|---|---|
| **M1** | 1.3 | RQ memuat **tiga kata kerja**: "merancang dan mengimplementasikan", "mengevaluasi", "mengintegrasikan … untuk meningkatkan" | Satu RQ tidak dapat dijawab oleh satu desain; sulit difalsifikasi |
| **M2** | 1.4 (H2) | "skor QoS agregat lebih tinggi" tanpa definisi operasional, satuan, atau selisih minimum | Tidak terukur / tidak falsifiabel |
| **M3** | 2.7.3 (Tabel 9) | Menggunakan **uji-t sampel independen** untuk data deret waktu berurutan | Melanggar asumsi independensi (autokorelasi); risiko galat Tipe I |
| **M4** | 2.7.3 | Menyatakan skenario berurutan **"diperlakukan sebagai sampel independen"** | Keliru secara statistik |
| **M5** | 2.6.2 | Hanya **3 skenario (A statis, B tanpa histeresis, C lengkap)** | Tidak ada ablasi → kontribusi komponen tidak dapat dipisahkan |
| **M6** | 2.7 | Tidak ada metrik **integritas sesi (RST)** | Klaim "tanpa mengorbankan stabilitas routing" tidak dibuktikan |
| **M7** | 2.5.4 | Ambang `Th_degradasi`/`Th_pemulihan` **tanpa nilai konkret** | Tidak dapat direplikasi |
| **M8** | 1.7 no. 3 / 1.2.7 | Bobot SAW **statis**, tetapi sistem disebut "adaptif" | Ambiguitas klaim |
| **M9** | 2.3.4 | Implementasi **langsung di jaringan produksi** tanpa validitas internal/staging formal | Risiko ke pelanggan; validitas internal lemah |
| **M10** | — | **Tidak ada bagian etika/izin** pemberitahuan pelanggan | Wajib untuk jaringan komersial |
| **M11** | 2.6.2 | Cuaca/beban hanya dicatat, tanpa pengacakan/pemblokan | Confounder tidak dikendalikan |
| **M12** | 2.7.4 | **"Flapping" tidak didefinisikan operasional** (jendela? arah? satuan?) | Tidak terukur |
| **M13** | 2.5.4 | Nilai **$k$ (dwell)** dan interval polling tidak disebut | Tidak dapat direplikasi |
| **M14** 🔴 | 1.2.10 vs 2.5.4 vs 2.5.6 | **Inkonsistensi tempat histeresis:** (a) 1.2.10 → histeresis pada **metrik mentah**; (b) 2.5.4 → histeresis pada **skor ALQI**; (c) 2.5.6 → histeresis dievaluasi **sebelum** SAW dihitung | Tiga pernyataan saling bertentangan; inti metode jadi kabur |
| **M15** | 2.5.5 | Rumus rasio $ALQI_{FO}/(ALQI_{FO}+ALQI_{LEO})$ **tanpa batas min/maks** | Rasio bisa ekstrem (mendekati 0/100%); risiko *starvation* |
| **M16** | 2.5.5 | Rasio proporsional terhadap **skor kualitas**, bukan **kapasitas/kontrak** ISP | Mengabaikan daya tampung nyata tiap jalur |
| **M17** | 1.1 | Klaim **"bebas osilasi"** tanpa bukti | Overclaim |
| **M18** | 2.7 | Tidak ada **power analysis**/penetapan *primary outcome* | Risiko *underpowered* & p-hacking |
| **M19** | 2.7.2 | Tetap merencanakan parametrik meski mengakui data cenderung *skewed* | Metode uji mungkin tidak sesuai |
| **M20** | 2.5.5 | Mengubah rasio hanya menyasar **koneksi baru**; tidak ada metrik konvergensi | Klaim "penyesuaian beban" tidak terjaga |

---

## 5. Pengamatan Klaim & Kebaruan **[ANALISIS]**

| Kode | Lokasi | Masalah |
|---|---|---|
| K1 | Judul & 1.2.10 | Istilah **"ALQI"** memiliki prior art (US Patent 9,674,720 B2, Crestron 2017) |
| K2 | 1.2.10 | Klaim "belum ditemukan penelitian yang menggabungkan SAW + histeresis" **tanpa log pencarian** |
| K3 | 1.5 & 1.6.1 | Kebaruan utama = **"integrasi"** → rentan dinilai inkremental |
| K4 | 1.1 & 1.7 no. 2 | Istilah **"upper bound"** Starlink mudah disalahpahami |
| K5 | 2.3.1 | Menyebut **"21 rujukan terindeks"**, sebagian jurnal nasional/tanpa DOI |
| K6 | 1.7 no. 3–4 | Mengakui bobot & ambang "bukan hasil optimasi" → perlu justifikasi lebih kuat |

---

## 6. Pengamatan Referensi (Bibliografi) **[FAKTA]**

| Kode | Masalah | Bukti |
|---|---|---|
| B1 | Tahun tidak konsisten | SOTA menulis "Amalia dkk., **2023**"; daftar pustaka **2022** (hal. 34 vs 32) |
| B2 | Atribusi penulis tertukar | SOTA "**Lanfer** dkk., 2024" vs daftar pustaka "**Boeckenholt** et al., 2024"; Lampiran "E. Lanfer dkk." (hal. 35, 37) |
| B3 | Nama penulis ≠ citekey | Lampiran: "(**Kumar & Golash**, 2009) **S. Kandula dkk.**, *Efficient flow-aware dynamic link load balancing*" (hal. 37) |
| B4 | Venue dipakai sebagai penulis | Baris "**LEO-NET, 2024**" (hal. 35) |
| B5 | Tahun tidak konsisten | SOTA "Vafaei et al., **2022**" vs badan/daftar pustaka **2021** (hal. 36) |
| B6 | Sitasi tanpa entri SOTA | "Chen et al., 2025" dan "Ji et al., 2026" dipakai di Bab I tetapi tidak ada di Lampiran (hal. 7, 32) |
| B7 | Metadata tidak lengkap | Nugroho (2023) tanpa halaman/DOI di sebagian entri |
| B8 | Dialog sitasi berulang | Beberapa baris Lampiran menampilkan sitasi ganda seperti "(Ma et al., 2023)(Ma et al., 2023)" (hal. 37) |

---

## 7. Ringkasan: Layak Dipertahankan / Diganti / Dibuang **[USULAN]**

| Keputusan | Item |
|---|---|
| **Dipertahankan** | Problem statement (FO–LEO, PCC statis); struktur NDLC; pemilihan SAW; ide histeresis; tabel parameter & ambang (setelah diberi angka); contoh perhitungan |
| **Ditulis ulang** | RQ (M1); hipotesis (M2); rumus SAW (E3); rumus rasio+batas (M15); definisi flapping (M12); rencana statistik (M3–M4, M18–M19); urutan histeresis (M14) |
| **Diganti** | Nama "ALQI" (K1); istilah "upper bound" (K4) |
| **Ditambahkan** | Ablasi skenario (M5); metrik RST & konvergensi (M6, M20); nilai ambang & dwell (M7, M13); staging + rollback (M9); etika/izin (M10); pengacakan/pemblokan (M11) |
| **Dibuang** | Klaim "bebas osilasi" (M17); klaim "belum ada" tanpa bukti (K2) |
| **Dirapikan** | Seluruh penomoran tabel/gambar (E1–E12); seluruh entri bibliografi (B1–B8) |

---

## 8. Kesimpulan Pengamatan **[ANALISIS]**

Naskah lama **layak diselamatkan**, bukan dibuang. Kekuatannya: masalah nyata, alur
metodologis lengkap, dan contoh perhitungan yang konsisten. Kelemahan utamanya:
**(1) inkonsistensi letak histeresis (M14)** — ini cacat logika paling serius;
**(2) perencanaan statistik yang salah (M3–M4)**; **(3) ketiadaan ablasi (M5)**;
**(4) istilah ALQI sebagai prior art (K1)**; dan **(5) penomoran serta bibliografi yang
berantakan (E1–E12, B1–B8)**.

Perbaikan konkretnya ada di `13_Perbaikan_Proposal_Lama.md`.
