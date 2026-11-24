# Proposal Tesis S2 — Ruang Kerja

Repositori ini dipakai untuk menyusun proposal tesis Magister Teknik Informatika
(Universitas Hasanuddin) secara bertahap.

**Fokus aktif:** kajian arah penelitian **ALQI berbasis *Simple Additive Weighting*
(SAW)** — pembobotan dan normalisasi adaptif untuk penilaian kualitas link pada
jaringan heterogen **tri-link: 1 FO (IndiHome) + 2 Starlink LEO**. Lingkup
dipersempit dari sistem kontroler penuh (SPA-HSM) menjadi modul/fokus yang lebih
spesifik dan terukur.

> **Revisi topologi (18 Nov 2026):** topologi uji diubah dari *dual-ISP FO–LEO*
> menjadi **tri-link 1 FO + 2 Starlink** (setara ISP-A + ISP-B + ISP-C). Ini
> **menggantikan** keputusan lama K-01/D-14 (dual A+C). Konsekuensi & syarat ada di
> `01_Pembahasan_ALQI_SAW/00_README.md` §6.

## Struktur

| Folder | Isi | Status |
|---|---|---|
| `01_Arsip_SPA-HSM_Tahap_01-12/` | Alur kerja SPA-HSM: manajemen, gap/novelty, RQ, kerangka teori, metodologi, baseline, presentasi. | **Arsip** |
| `00_Arsip_Proposal_SPA-HSM/` | Materi lebih lama: draf Bab I–II, dokumen audit, PDF, jurnal, arsitektur, logo, panduan penulisan. | **Arsip** |
| `01_Pembahasan_ALQI_SAW/` | **Naskah aktif baru**: kelayakan, prior art, gap, parameter, bobot SAW, formulasi, SOTA, eksperimen, RQ/judul, kandidat referensi, analisis pra-penelitian. | **Aktif** |
| `02_Pembahasan_Final_Proposal/` | **Konsolidasi final**: struktur langkah penelitian (kelayakan gap/novelty S2), peta gap→klaim→bukti→syarat, gerbang keputusan, tahapan kerja per folder, draf Bab I–III (rencana). | **Aktif** |

## Isi `01_Pembahasan_ALQI_SAW/`

| Berkas | Isi |
|---|---|
| `00_README.md` | Indeks, konvensi label, ringkasan eksekutif |
| `00_Bahan_Pengamatan/` | Salinan `Proposal pcc- print.pdf` sebagai bahan pengamatan |
| `01_Kelayakan_dan_Prior_Art.md` | Putusan kelayakan + temuan prior art paten ALQI |
| `02_Research_Gap.md` | Gap berbasis bukti (G-N1, G-N2, G-W1, G-W2) |
| `03_Spesifikasi_Parameter.md` | Parameter QoS + batas acuan TIPHON/Y.1541 |
| `04_Analisis_Bobot_SAW.md` | Benefit/cost, normalisasi, pendekatan bobot |
| `05_Formulasi_ALQI_Adaptif.md` | Formulasi matematis statis → adaptif |
| `06_Matriks_State_of_the_Art.md` | Tabel pembanding + nilai kuantitatif |
| `07_Kebaruan_dan_Kontribusi.md` | Klaim kebaruan S2 + batas klaim |
| `08_Rancangan_Eksperimen.md` | Arsitektur, skenario, metrik, statistik |
| `09_Rumusan_Masalah_dan_Judul.md` | RQ versi "memodifikasi" + rekomendasi judul |
| `10_Kandidat_Referensi.csv` | Daftar referensi (sebagian perlu verifikasi) |
| `11_Rencana_Verifikasi_Lanjutan.md` | Pekerjaan literatur & teknis yang belum selesai |
| `12_Pengamatan_Proposal_Lama.md` | Audit naskah lama (temuan editorial/metodologis/klaim/referensi) |
| `13_Perbaikan_Proposal_Lama.md` | Usulan perbaikan konkret atas temuan audit |
| `14_Tahapan_Penelitian.md` | Roadmap tahap demi tahap (T0–T10) + gate & jadwal |
| `15_Arsitektur_Sistem.md` | Arsitektur tri-link: diagram, kontrak antarmuka, state machine, deployment |
| `16_Arsitektur_Jaringan_MikroTik.md` | Desain jaringan Multi-WAN 3 ISP: PCC, failover, LAN, RouterOS v7 |
| `17_Uji_Kelayakan_dan_Risiko_Penguji.md` | Uji kelayakan dari sudut penguji (skor ±70; syarat B1–B6) |
| `18_B1_Lingkup_dan_Pernyataan_Kebaruan.md` | B1: lingkup (Varian C) + pernyataan kebaruan |
| `arsitektur/` | Skrip & gambar arsitektur (`arsitektur_ALQI_SAW.*`, `arsitektur_jaringan_mikrotik.*`) |

## Isi `02_Pembahasan_Final_Proposal/`

| Berkas | Isi |
|---|---|
| `00_README.md` | Indeks, ringkasan eksekutif, status blocking B1–B6, barometer S2, peta gap→klaim→bukti→syarat, checklist final |
| `01_Struktur_Langkah_Penelitian_S2.md` | **Struktur langkah penelitian** (T0–T10) + gerbang G0–G3/G-S2 + cara menutup B1–B6 + P1–P5 |
| `02_Draf_Bab_I.md` | *(rencana)* Draf Bab I |
| `03_Draf_Bab_II.md` | *(rencana)* Tinjauan pustaka + posisi |
| `04_Draf_Bab_III.md` | *(rencana)* Metodologi |
| `05_Registrasi_Rencana_Analisis.md` | *(rencana)* Pra-registrasi statistik |
| `06_Tahapan_Per_Folder.md` | **Tahapan kerja per folder**: T0–T10 → folder → berkas, gelombang kerja, serah-terima, gerbang |
| `07_Kamus_Kode.md` | **Kamus kode lengkap**: arti & rujukan semua kode (B1–B6, K-A…K-E, G-N/G-W, D-1…D-7, V/PA/T, perlakuan A–H, kondisi N/T/S/R/K, kode arsip) |

## Aturan kerja

1. **Naskah aktif tidak ditulis di folder arsip.** Arsip dipertahankan sebagai rujukan.
2. Labeli setiap pernyataan: **[FAKTA]** (sumber), **[ANALISIS]** (penalaran),
   **[USULAN]** (desain).
3. Klaim kebaruan harus bisa dijawab dengan: *apa yang baru, dibanding siapa, bukti apa.*
4. Klaim "belum ada" hanya boleh ditulis setelah log pencarian dijalankan, dengan
   frasa *"berdasarkan pencarian pada …"*.
5. Kata kerja kontribusi: **memodifikasi** — hindari "merancang/menciptakan/membangun
   dari nol".

## Status

- [x] Konsolidasi materi lama menjadi dua arsip
- [x] Analisis kelayakan awal ALQI–SAW
- [x] Identifikasi prior art (US 9,674,720 B2)
- [x] Spesifikasi parameter & batas acuan (TIPHON/Y.1541)
- [x] Analisis bobot SAW & formulasi adaptif
- [x] Matriks SOTA + rancangan eksperimen + RQ/judul
- [x] Audit & perbaikan naskah lama (`12`–`13`)
- [x] Roadmap tahapan penelitian (`14`)
- [x] Revisi topologi: tri-link 1 FO + 2 Starlink (18 Nov 2026)
- [x] Arsitektur sistem & jaringan Multi-WAN (`15`–`16`)
- [x] Uji kelayakan dari sudut pandang penguji (`17`) — skor ±70
- [ ] Verifikasi literatur lintas basis data (lihat `11_...`)
- [ ] Kunci lingkup (Varian A/B/C) dan keputusan D-1 s.d. D-6
- [ ] Tulis Bab I + kerangka Bab III
