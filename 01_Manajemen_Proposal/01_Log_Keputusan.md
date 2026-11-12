# Log Keputusan Proposal

**Fungsi:** Mencatat keputusan lingkup agar tidak ada klaim yang bertentangan
antar-bab. Setiap perubahan harus diberi tanggal dan alasan.

---

## 1. Keputusan yang Sudah Dikunci (dari audit sebelumnya)

| Kode | Keputusan | Konsekuensi |
|---|---|---|
| K-01 | Topologi uji: dual-ISP FO IndiHome + LEO Starlink | Tidak boleh mengklaim generalisasi > 2 ISP |
| K-02 | Starlink sebagai kasus acuan *upper bound* transien | Parameter diturunkan dari transien LEO, lalu diuji pada degradasi FO |
| K-03 | Bobot SAW statis, dikalibrasi di awal | "Adaptif" hanya merujuk rasio, bukan pembelajaran bobot |
| K-04 | MikroTik = adapter/testbed, bukan objek | Judul dan kontribusi tidak menyebut pengembangan PCC MikroTik |
| K-05 | Nama payung: **SPA-HSM** | ALQI dan TLABA tidak dipakai sebagai nama sistem |
| K-06 | Satuan analisis: episode degradasi atau jam | Bukan setiap siklus polling |
| K-07 | Evaluasi kausal utama di staging; lapangan sebagai validasi eksternal | Mengurangi confounder cuaca dan beban |

---

## 2. Keputusan yang Masih Terbuka

| No | Keputusan | Pilihan | Rekomendasi | Status |
|---|---|---|---|---|
| D-01 | Arah penelitian | Lihat §3 | **Opsi D dikunci** | **Dikunci 12-11-2026** |
| D-02 | Jumlah skenario ablasi | 6 (A–F) / 4 minimum (A, B, D, F) | **6 skenario A–F** | **Dikunci 12-11-2026** |
| D-03 | Baseline praktisi | netwatch failover / weighted ECMP / keduanya | **netwatch failover** | **Dikunci 12-11-2026** |
| D-04 | Penguatan novelty | Opsi A (batas analitis) / Opsi B (metrik SIWG) / keduanya | **Opsi B diterima sebagai SIWG** | **Dikunci 12-11-2026** |
| D-05 | Telemetri Starlink | gRPC dish / probe aktif saja | Cek ketersediaan sebelum Tahap 4 | **Menunggu** |
| D-06 | Lokasi dan izin | Lokasi lama / lokasi baru | Konfirmasi akses | **Menunggu** |
| D-07 | Ambang RST | < 1% / non-inferior / selisih absolut | Primer non-inferior +0,5 pp; sekunder < 1% | **Dikunci 12-11-2026** |
| D-08 | Jumlah bucket N | 20 / 100 / lain | 20 untuk uji awal, uji sensitivitas | **Menunggu** |
| D-09 | State machine | 2 state / 3 state (+RECOVERING) | 2 state untuk versi inti | **Menunggu** |
| D-10 | Gaya sitasi | APA 7 / IEEE / gaya kampus | APA 7 sesuai draf | **Menunggu konfirmasi pedoman** |
| D-11 | Tier referensi | Terapkan T1/T2/T3 | T3 hanya untuk daftar pustaka/konteks | **Dikunci 12-11-2026** |
| D-12 | Target SOTA inti | 10 / 15 / 20 | Minimal 15 sebelum seminar | **Dikunci 12-11-2026** |
| D-13 | Referensi kontinuitas sesi | 0 / 4 / lebih | Minimal 4 (MPTCP/session continuity) | **Terlaksana 12-11-2026 (4 refs)** |

---

## 3. Opsi Arah Penelitian

### Opsi A — SPA-HSM penuh (rekomendasi)

Fokus: integrasi + aturan dwell sadar-transien + ablasi empiris.

- **Novelty:** sedang–tinggi (N2 + N3).
- **Risiko:** sedang. Sebagian besar bahan sudah ada.
- **Kelebihan:** realistis untuk S2, artefak jelas, evaluasi terukur.
- **Kekurangan:** tetap rentan tuduhan "integrasi" jika N2 tidak ditonjolkan.

### Opsi B — Fokus pada aturan dwell dan batas analitis

Fokus: turunan parameter + batas atas flapping, dengan eksperimen lebih kecil.

- **Novelty:** tinggi (kontribusi analitis).
- **Risiko:** tinggi. Asumsi derau harus dipertahankan; butuh kemampuan analisis.
- **Kelebihan:** paling kuat secara teoritis.
- **Kekurangan:** beban pembuktian matematis besar; artefak rekayasa berkurang.

### Opsi C — Alokasi prediktif sadar-handover

Fokus: memanfaatkan pola periodik ~15 detik untuk memprediksi degradasi sebelum
terjadi, lalu mengalokasikan lebih awal.

- **Novelty:** sangat tinggi.
- **Risiko:** sangat tinggi. Prediktor bisa gagal; data pelatihan terbatas;
  waktu penelitian membengkak.
- **Kelebihan:** paling menarik secara ilmiah.
- **Kekurangan:** tidak disarankan untuk proposal S2 dengan batas waktu ketat.

### Opsi D — SPA-HSM + metrik gabungan (SIWG)

Fokus: Opsi A ditambah metrik *session-impact-weighted goodput*.

- **Novelty:** tinggi.
- **Risiko:** sedang.
- **Kelebihan:** satu angka untuk trade-off; mudah dikomunikasikan.
- **Kekurangan:** pembobotan perlu analisis sensitivitas.

**Rekomendasi:** **Opsi D**, yaitu Opsi A dengan tambahan metrik gabungan.
Jika waktu menipis, turunkan ke Opsi A tanpa kehilangan kerangka.

---

## 4. Format Pencatatan Perubahan

Setiap perubahan keputusan harus menambah baris:

| Tanggal | Kode | Keputusan lama | Keputusan baru | Alasan | Dampak |
|---|---|---|---|---|---|
| 12-11-2026 | — | — | Struktur kerja baru dan Tahap 1 disusun | Reorganisasi repo | Materi lama menjadi arsip |
| 12-11-2026 | D-01 | Belum ada | Opsi D: SPA-HSM + SIWG | Persetujuan mahasiswa | RQ, tujuan, hipotesis Tahap 2 disusun |
| 12-11-2026 | D-04 | Belum ada | Opsi B: SIWG diadopsi | Persetujuan mahasiswa | H4 dan definisi SIWG ditambahkan |
| 12-11-2026 | D-11 | Belum ada | Tier T1/T2/T3 diterapkan | Evaluasi kualitas referensi | Jurnal lokal hanya untuk konteks |
| 12-11-2026 | D-12 | Belum ada | Target SOTA inti ≥ 15 | Menjaga kualitas SOTA | Perlu 3–6 referensi T1 tambahan |
| 12-11-2026 | D-02 | Belum ada | 6 skenario A–F | Akses lokasi memungkinkan | H2 dan H4 diuji penuh |
| 12-11-2026 | D-03 | Belum ada | netwatch failover | Paling dekat praktik RT/RW Net | Baseline G dikonfigurasi |
| 12-11-2026 | D-07 | Belum ada | Primer non-inferior +0,5 pp; sekunder <1% | Menghindari kriteria ganda | H3a diperbarui |
| 12-11-2026 | B-01 | H1 60 s; H2 +30 s | Rmax global 90 s | Menghilangkan konflik ambang | H1/H2 diperbarui |
| 12-11-2026 | B-02 | Dua kriteria primer H3a | Non-inferior primer; <1% sekunder | Aturan keputusan jelas | H3a diperbarui |
| 12-11-2026 | D-13 | 0 referensi kontinuitas | 4 referensi masuk Bab II 2.8.1 | P-03 | H3a punya landasan teori |

---

## 5. Aturan Perubahan

1. Keputusan yang sudah dikunci hanya boleh diubah dengan persetujuan pembimbing.
2. Perubahan harus diperbarui serentak di: log ini, roadmap, dan dokumen tahap terkait.
3. Istilah yang sudah dihapus (ALQI, TLABA) tidak boleh muncul kembali tanpa
   keputusan tertulis.
4. Setiap klaim novelty baru harus melewati lima uji di
   `02_Tahap_01_Gap_dan_Novelty/04_Uji_Kelayakan_dan_Risiko_Penguji.md`.
