# Kebijakan Tier Referensi

**Dokumen:** `01_Kebijakan_Tier_Referensi.md`
**Fungsi:** Memisahkan referensi yang layak menjadi *state of the art* (SOTA) dari
referensi yang hanya layak masuk daftar pustaka/konteks.
**Dasar:** Tidak semua publikasi punya bobot yang sama. Menempatkan jurnal
bereputasi rendah sebagai SOTA melemahkan novelty, meskipun jurnal itu berguna
sebagai konteks.

---

## 1. Definisi Tier

| Tier | Kriteria | Boleh menjadi SOTA? | Peran |
|---|---|---|---|
| **T1** | Publikasi internasional peer-review kuat (IEEE, ACM, Elsevier, Springer, Nature), standar resmi, atau karya seminal | **Ya** | Pembanding utama, dasar gap, dasar metode |
| **T2** | Prosiding peer-review, preprint arXiv, jurnal nasional terakreditasi, atau jurnal internasional cakupan terbatas | **Bersyarat** | Pendukung; hanya jika tidak ada T1 yang setara, dan wajib dilabeli |
| **T3** | Jurnal lokal bereputasi rendah, dokumentasi vendor, non-peer-review, artikel tangential | **Tidak** | Konteks implementasi, definisi teknis, latar belakang lokal |

**Catatan penting:** "T3" bukan berarti "buruk" atau "tidak boleh dipakai".
Banyak studi T3 sangat berharga untuk menunjukkan realitas RT/RW Net. Yang dilarang
adalah **menjadikannya satu-satunya dasar klaim state of the art atau gap**.

---

## 2. Aturan Pemakaian

1. **Setiap komponen SOTA minimal 2 referensi T1.**
   Komponen: QoS/pengukuran, FO/LEO, PCC/load balancing, MCDM/EWMA/histeresis,
   arsitektur kontrol, kontinuitas sesi.
2. **Klaim gap tidak boleh bersandar hanya pada T3.**
   Jika semua bukti "belum ada" berasal dari T3, gap belum terbukti.
3. **T2 hanya boleh menjadi SOTA pendukung** dan harus disandingkan dengan T1.
4. **T3 dipakai untuk konteks, bukan perbandingan kinerja.**
   Contoh: "Pada jaringan RT/RW Net lokal, PCC diimplementasikan dengan rasio
   statis (Nugroho et al., 2023)" — boleh. "PCC adalah state of the art karena
   (Nugroho et al., 2023)" — tidak boleh.
5. **Dokumentasi vendor bukan SOTA.**
   MikroTik (n.d.) dipakai untuk menjelaskan mekanisme, bukan untuk mengklaim
   keunggulan.
6. **Preprint harus dilabeli.**
   Ullah et al. (2025) adalah arXiv; jika sudah terbit, ganti ke versi final.
7. **Setiap referensi T3 yang dipakai sebagai konteks wajib punya alasan tertulis.**

---

## 3. Klasifikasi 38 Referensi

**Legenda peran:** SOTA = pembanding state of the art; Pendukung = SOTA pendukung;
Konteks = daftar pustaka/konteks; Metode = standar, buku, atau alat statistik.

| No | Citekey | Venue/jenis | Tier | Peran | SOTA? | Catatan |
|---:|---|---|:---:|---|:---:|---|
| 1 | ali2025 | IEEE Access | T1 | SOTA | Ya | Internasional, cakupan luas |
| 2 | alhabo2017 | Springer WPC | T1 | SOTA | Ya | Lengkapi metadata penulis |
| 3 | amalia2022 | Procedia CS | T2 | Pendukung | Bersyarat | Baseline PCC dual-ISP; prosiding |
| 4 | arfianita2024 | IOTA Journal | T2 | Pendukung | Bersyarat | Verifikasi indeksasi |
| 5 | boeckenholt2024 | ITG Conference | T2 | Pendukung | Bersyarat | Prosiding; tanpa DOI |
| 6 | bradner1999 | RFC 2544 | T1 | Metode | Tidak | Standar |
| 7 | bustomi2026 | EDUMATIC | T3 | Konteks | Tidak | Jurnal lokal |
| 8 | chen2025 | Engineering (Elsevier) | T1 | SOTA | Ya | Review 6G |
| 9 | cohen1988 | Buku | T1 | Metode | Tidak | Effect size |
| 10 | eddy2022 | RFC 9293 | T1 | Metode | Tidak | TCP |
| 11 | efron1993 | Buku | T1 | Metode | Tidak | Bootstrap |
| 12 | etsi2000 | ETSI TS | T1 | Metode | Tidak | Standar QoS |
| 13 | gamma1994 | Buku | T1 | SOTA konsep | Ya | Pola adapter |
| 14 | garcia2025 | ACM LEO-NET | T1 | SOTA | Ya | Starlink OWD |
| 15 | hammer2024 | ACM LEO-NET | T1 | SOTA | Ya | Starlink edge |
| 16 | holm1979 | Scandinavian J. Stat. | T1 | Metode | Tidak | Koreksi multiplisitas |
| 17 | itut2003 | ITU-T G.114 | T1 | Metode | Tidak | Standar delay |
| 18 | itut2011 | ITU-T Y.1541 | T1 | Metode | Tidak | Standar performa |
| 19 | ji2026 | ICT Express | T1 | SOTA | Ya | Verifikasi DOI/keberadaan |
| 20 | komathi2024 | IJECE | T2 | Pendukung | Bersyarat | Cloud LB; verifikasi indeksasi |
| 21 | kumar2009 | IEEE COMSNETS | T1 | SOTA | Ya | Flow-aware LB |
| 22 | liang1986 | Biometrika | T1 | Metode | Tidak | GEE |
| 23 | lilhore2025 | Scientific Reports | T1 | SOTA | Ya | Cloud LB pembanding |
| 24 | ma2023 | IEEE INFOCOM | T1 | SOTA | Ya | Starlink measurement |
| 25 | mccullagh1989 | Buku | T1 | Metode | Tidak | GLM |
| 26 | mikrotik | Dokumentasi vendor | T3 | Konteks teknis | Tidak | Bukan peer-review |
| 27 | mirsal2026 | Jurnal E-Komtek | T3 | Konteks | Tidak | Jurnal lokal |
| 28 | mohan2024 | ACM WWW | T1 | SOTA | Ya | Starlink multifaceted |
| 29 | nanang2024 | IEEE ICCIT | T2 | Pendukung | Bersyarat | Prosiding |
| 30 | nugroho2023 | JANAPATI | T3 | Konteks | Tidak | Jurnal lokal |
| 31 | paxson1998 | RFC 2330 | T1 | Metode | Tidak | Metrik IP |
| 32 | putra2024 | JISA | T3 | Konteks | Tidak | Jurnal lokal |
| 33 | roberts1959 | Technometrics | T1 | SOTA metode | Ya | EWMA seminal |
| 34 | schulzrinne2003 | RFC 3550 | T1 | Metode | Tidak | Jitter |
| 35 | tournaire2023 | ACM TOMEPCS | T1 | SOTA | Ya | Histeresis/ambang |
| 36 | ullah2025 | arXiv | T2 | Pendukung | Bersyarat | Preprint; angka wajib dicek |
| 37 | vafaei2021 | Procedia CS | T2 | Pendukung | Bersyarat | SAW/normalisasi |
| 38 | wang2013 | IEEE COMST | T1 | SOTA | Ya | MCDM network selection |

---

## 4. Rekapitulasi

| Kelompok | Jumlah | Keterangan |
|---|---:|---|
| SOTA inti empiris/arsitektur (T1) | 12 | ali2025, alhabo2017, chen2025, garcia2025, hammer2024, ji2026, kumar2009, lilhore2025, ma2023, mohan2024, tournaire2023, wang2013 |
| Konsep/metode seminal (T1) | 2 | gamma1994, roberts1959 |
| SOTA pendukung (T2) | 7 | amalia2022, arfianita2024, boeckenholt2024, komathi2024, nanang2024, ullah2025, vafaei2021 |
| Konteks/bibliografi (T3) | 5 | bustomi2026, mikrotik, mirsal2026, nugroho2023, putra2024 |
| Standar dan metode (T1) | 12 | RFC, ITU-T, ETSI, buku statistik |
| **Total** | **38** | |

**Catatan angka:** dari 14 entri T1 yang tampak sebagai "SOTA", hanya **12** yang
merupakan studi empiris/arsitektur yang dapat dipakai sebagai pembanding kinerja.
`gamma1994` dan `roberts1959` adalah kontribusi konsep/metode, bukan studi empiris.

---

## 5. Komposisi Ideal untuk Proposal S2

| Kelompok | Target | Saat ini | Kekurangan |
|---|---:|---:|---:|
| SOTA inti (T1) | 15–18 | 12 | 3–6 |
| SOTA pendukung (T2) | 5–8 | 7 | cukup |
| Konteks/bibliografi (T3) | 8–12 | 5 | 3–7 |
| Metode/standar | 10–15 | 14 | cukup |
| **Total** | **40–50** | **38** | 2–12 |

---

## 6. Komponen SOTA Paling Lemah

| Komponen | T1 | T2 | Status |
|---|---:|---:|---|
| QoS dan pengukuran | 6 (standar) | 1 | Cukup, tetapi standar bukan pembanding empiris |
| FO dan LEO | 6 | 2 | **Kuat** |
| PCC dan load balancing | **1** | 2 | **Lemah** |
| MCDM/EWMA/histeresis | 4 | 1 | Cukup |
| Arsitektur kontrol | 2 | 0 | Cukup |
| Kontinuitas sesi/MPTCP | **0** | 0 | **Kosong** |

**Dua lubang utama:**

1. **PCC/adaptive load balancing internasional.** Hanya Kumar dan Golash (2009)
   yang T1. Perlu 3–5 referensi 2018–2026 tentang adaptive load balancing,
   SD-WAN multipath, atau traffic steering.
2. **Kontinuitas sesi/MPTCP.** Nol referensi. Padahal H3a adalah hipotesis inti.
   Perlu 3–4 referensi tentang MPTCP, connection migration, atau session
   continuity.

---

## 7. Daftar "Jangan Dijadikan SOTA"

Referensi berikut **tetap dipakai**, tetapi hanya untuk konteks/definisi:

| Referensi | Boleh dipakai untuk | Tidak boleh dipakai untuk |
|---|---|---|
| Nugroho et al. (2023) | Konteks PCC di jaringan lokal | Klaim state of the art PCC global |
| Mirsal & Agtriadi (2026) | Konteks perbandingan PCC vs Queue Tree | Dasar gap utama |
| Putra & Anton (2024) | Konteks failover lapangan | Klaim keunggulan metode |
| Bustomi & Tahir (2026) | Konteks PCC dual-ISP lokal | Pembanding internasional |
| MikroTik (n.d.) | Mekanisme mangle/conntrack | Klaim keunggulan atau gap |

**Kalimat yang benar:**
> "Pada implementasi RT/RW Net lokal, PCC umumnya dikonfigurasi dengan rasio
> statis (Nugroho et al., 2023; Putra & Anton, 2024)."

**Kalimat yang salah:**
> "State of the art PCC adalah rasio statis (Nugroho et al., 2023)."

---

## 8. Konsekuensi bagi Tahap 4

1. Tabel SOTA di Bab II harus memisahkan kolom "SOTA inti" dan "konteks".
2. Bab III boleh memakai studi T3 untuk justifikasi konteks lokasi, bukan untuk
   memilih metode.
3. Sebelum seminar, targetkan minimal **15 SOTA inti** dan **4 referensi
   kontinuitas sesi**.
4. Setiap penambahan referensi T3 setelah ini harus dicatat alasannya di register.

---

## 9. Keputusan yang Diusulkan

| Kode | Keputusan | Status |
|---|---|---|
| D-11 | Terapkan tiering T1/T2/T3; T3 hanya untuk daftar pustaka/konteks | **Dikunci 12-11-2026** |
| D-12 | Target minimal 15 SOTA inti sebelum seminar | **Dikunci 12-11-2026** |
| D-13 | Tambah minimal 4 referensi kontinuitas sesi/MPTCP | **Menunggu eksekusi** |

---

## 10. Pembaruan Setelah P-02/P-03 (12-11-2026)

| Kelompok | Sebelum | Sesudah |
|---|---:|---:|
| SOTA inti (T1) | 12 | **17** |
| SOTA pendukung (T2) | 7 | **10** |
| Register total | 38 | **48** |

**Komponen PCC** kini memiliki 4 referensi T1:
Kumar & Golash (2009), Shahid et al. (2020), Cruvellier et al. (2025), dan
Giacometti et al. (2025). Ditambah Rajagopalan (2020) sebagai T2.

**Kontinuitas sesi** kini memiliki:
- T1: Duchene & Bonaventure (2017); Naimi et al. (2024).
- T2: Liénardy & Donnet (2016); Jiang et al. (2024).

**Catatan:** Naimi et al. (2024) baru tersedia pada level judul; klaim dibatasi
pada topik. Dua kandidat belum dipakai: Mokhtar et al. (2021) dan Choi et al.
(2017). P-05 (audit sitasi) masih harus dijalankan.
