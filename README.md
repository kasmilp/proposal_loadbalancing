# Proposal Tesis S2 — Ruang Kerja

Repositori ini dipakai untuk menyusun proposal tesis Magister Teknik Informatika
(Universitas Hasanuddin) secara bertahap.

**Fokus aktif:** kajian arah penelitian **ALQI berbasis *Simple Additive Weighting*
(SAW)** — pembobotan dan normalisasi adaptif untuk penilaian kualitas link pada
jaringan heterogen FO–LEO. Lingkup dipersempit dari sistem kontroler penuh (SPA-HSM)
menjadi modul/fokus yang lebih spesifik dan terukur.

## Struktur

| Folder | Isi | Status |
|---|---|---|
| `01_Arsip_SPA-HSM_Tahap_01-12/` | Alur kerja SPA-HSM: manajemen, gap/novelty, RQ, kerangka teori, metodologi, baseline, presentasi. | **Arsip** |
| `00_Arsip_Proposal_SPA-HSM/` | Materi lebih lama: draf Bab I–II, dokumen audit, PDF, jurnal, arsitektur, logo, panduan penulisan. | **Arsip** |
| `01_Pembahasan_ALQI_SAW/` | **Naskah aktif baru**: kelayakan, prior art, gap, parameter, bobot SAW, formulasi, SOTA, eksperimen, RQ/judul, kandidat referensi. | **Aktif** |

## Isi `01_Pembahasan_ALQI_SAW/`

| Berkas | Isi |
|---|---|
| `00_README.md` | Indeks, konvensi label, ringkasan eksekutif |
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
- [ ] Verifikasi literatur lintas basis data (lihat `11_...`)
- [ ] Kunci lingkup (Varian A/B/C) dan keputusan D-1 s.d. D-6
- [ ] Tulis Bab I + kerangka Bab III
