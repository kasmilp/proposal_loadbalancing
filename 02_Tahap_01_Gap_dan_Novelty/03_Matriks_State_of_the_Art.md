# Tahap 1 — Matriks State of the Art

**Dokumen:** `03_Matriks_State_of_the_Art.md`
**Status:** Draf kerja Tahap 1
**Fungsi:** Menunjukkan secara visual di mana kombinasi penelitian ini belum terisi.

**Keterangan:** ● = ditangani secara eksplisit dan diuji · ◐ = disebut/sebagian ·
○ = tidak ditangani · — = tidak relevan.

---

## 1. Dimensi Pembanding

| Kode | Dimensi | Pertanyaan |
|---|---|---|
| D1 | Skor kualitas multi-kriteria | Apakah kualitas link dinilai dengan lebih dari satu metrik secara terpadu? |
| D2 | Penghalusan deret waktu | Apakah derau metrik dihaluskan sebelum keputusan? |
| D3 | Histeresis/ambang ganda | Apakah keputusan memakai dua ambang atau dwell untuk mencegah osilasi? |
| D4 | Preservasi sesi terukur | Apakah dampak keputusan terhadap sesi TCP diukur, bukan diasumsikan? |
| D5 | Proporsi PCC adaptif real-time | Apakah rasio PCC berubah berdasarkan kondisi link? |
| D6 | Konteks FO–LEO heterogen | Apakah menggabungkan link terestrial dan satelit LEO? |
| D7 | Validasi lapangan dual-ISP | Apakah diuji pada jaringan produksi, bukan hanya simulasi? |
| D8 | Portabilitas platform teruji | Apakah logika dipisahkan dan diuji lintas adapter? |

---

## 2. Matriks

| No | Studi | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | Amalia et al. (2022) — PCC + failover dual ISP | ○ | ○ | ○ | ○ | ◐ | ○ | ◐ | ○ |
| 2 | Arfianita et al. (2024) — PCC tiga ISP (GNS3) | ○ | ○ | ○ | ○ | ◐ | ○ | ○ | ○ |
| 3 | Nugroho et al. (2023) — PCC vs ECMP vs NTH | ○ | ○ | ○ | ◐ | ◐ | ○ | ○ | ○ |
| 4 | Putra & Anton (2024) — PCC + failover | ○ | ○ | ○ | ○ | ◐ | ○ | ◐ | ○ |
| 5 | Mirsal & Agtriadi (2026) — PCC vs Queue Tree | ○ | ○ | ○ | ○ | ◐ | ○ | ○ | ○ |
| 6 | Ali et al. (2025) — hub multi-ISP berbasis ANN | ◐ | ○ | ○ | ○ | ◐ | ◐ | ○ | ○ |
| 7 | Ma et al. (2023); Garcia et al. (2025); Hammer et al. (2024); Mohan et al. (2024) — karakterisasi Starlink | ○ | ○ | ○ | — | ○ | ◐ | ◐ | ○ |
| 8 | Ullah et al. (2025); Boeckenholt et al. (2024) — rain fade Starlink | ○ | ○ | ○ | — | ○ | ◐ | ◐ | ○ |
| 9 | Wang & Kuo (2013); Vafaei et al. (2021) — MCDM/SAW | ● | ○ | ○ | — | ○ | ○ | ○ | ○ |
| 10 | Tournaire et al. (2023) — ambang optimal histeresis | ○ | ◐ | ● | — | ○ | ○ | ○ | ○ |
| 11 | Komathi et al. (2024); Lilhore et al. (2025) — load balancing cloud | ◐ | ○ | ○ | ○ | ◐ | ○ | ○ | ○ |
| 12 | **SPA-HSM (usulan)** | ● | ● | ● | ● | ● | ● | ● | ◐ |

---

## 3. Cara Membaca Matriks

**Yang sudah ramai.** Kolom D5 (PCC) dan D1 (MCDM) sudah banyak diisi. Menambah
satu lagi studi PCC statis tidak menghasilkan novelty.

**Yang kosong dan saling terkait.**

1. **D3 + D4 belum pernah bertemu.** Histeresis dipelajari tanpa biaya sesi;
   preservasi sesi diklaim tanpa pengukuran. Titik temu keduanya kosong.
2. **D2 + D3 + D6 belum pernah bertemu.** Penghalusan dan histeresis dipelajari
   pada sistem umum, bukan pada transien LEO yang terukur.
3. **D7 + D6 hampir kosong.** Studi lapangan dual-ISP ada, tetapi tidak pada
   kombinasi FO–LEO.
4. **D8 kosong secara metodologis.** Portabilitas biasanya diklaim, bukan diuji.

**Kesimpulan matriks.** Sel yang benar-benar kosong dan dapat diisi dalam satu
penelitian adalah **D3 × D4 × D6**: histeresis yang sadar-transien, diukur
dampaknya terhadap sesi, pada konteks FO–LEO. Inilah irisan novelty yang dipakai.

---

## 4. Peta Posisi (Naratif)

Bayangkan dua sumbu:

- **Sumbu X:** kesadaran kondisi link (statis → adaptif berbasis pengukuran).
- **Sumbu Y:** kesadaran integritas sesi (diabaikan → diukur dan dijaga).

| Kuadran | Isi | Contoh |
|---|---|---|
| Kiri bawah | Statis, tidak sadar sesi | PCC konfigurasi tetap |
| Kanan bawah | Adaptif, tidak sadar sesi | ANN hub, load balancing cloud |
| Kiri atas | Sadar sesi, tetapi statis | PCC + conntrack, failover |
| **Kanan atas** | **Adaptif dan sadar sesi** | **Kosong → SPA-HSM** |

Posisi penelitian ini adalah kuadran kanan atas. Yang membuatnya bukan sekadar
"adaptif + conntrack" adalah **pengukuran** biaya sesi dan **aturan parameter**
yang mengikat keduanya.

---

## 5. Audit Referensi yang Harus Dilakukan

Matriks ini disusun dari korpus yang sudah ada di
`00_Arsip_Proposal_SPA-HSM/jurnal_terkait/`. Sebelum masuk Tahap 3:

| Pekerjaan | Alasan |
|---|---|
| Verifikasi metadata (tahun, venue, DOI) | Banyak berkas berupa PDF anotasi/terjemahan |
| Tambah minimal 10 referensi 2024–2026 | Memastikan posisi masih mutakhir |
| Cari studi "adaptive PCC" secara khusus | Menutup risiko klaim "belum ada" |
| Cari studi "session preservation + load balancing" | Menutup G-E1 |
| Cari studi "hysteresis + network selection" | Menutup G-M1 |
| Catat string pencarian dan jumlah hit | Bukti bahwa gap diverifikasi |

**Bukti yang harus disimpan:** tangkapan layar hasil pencarian, tanggal akses,
string, dan daftar judul yang diperiksa. Ini yang membedakan "gap" dari "saya
belum menemukannya".

---

## 6. Celah Matriks yang Harus Diakui

| Keterbatasan matriks | Dampak | Mitigasi |
|---|---|---|
| Penilaian ●/◐ bersifat kualitatif | Bisa diperdebatkan penguji | Sertakan alasan singkat per sel di lampiran |
| Korpus belum sistematis | Risiko bias seleksi | Jalankan protokol pencarian di §6 dokumen peta gap |
| Studi non-Inggris/Indonesia mungkin terlewat | Klaim "belum ada" melemah | Gunakan bahasa klaim yang hati-hati |
| D8 dinilai dari ada/tidaknya kontrak | Tidak mengukur kualitas | Jelaskan kriteria uji konformitas |
