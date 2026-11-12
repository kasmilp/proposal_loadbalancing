# Proposal Tesis S2 — Ruang Kerja

Repositori ini dipakai untuk menyusun proposal tesis Magister Teknik Informatika
(Universitas Hasanuddin) secara bertahap, dengan penekanan pada **research gap**
dan **novelty** yang dapat dipertahankan di depan penguji.

## Struktur

| Folder | Isi |
|---|---|
| `00_Arsip_Proposal_SPA-HSM/` | Seluruh materi lama: draf Bab I–II, dokumen audit, PDF, jurnal, arsitektur, logo, panduan penulisan. Dipertahankan sebagai rujukan, bukan naskah aktif. |
| `01_Manajemen_Proposal/` | Roadmap tahapan, log keputusan, dan kontrol progres. |
| `02_Tahap_01_Gap_dan_Novelty/` | Luaran Tahap 1: peta gap, pernyataan novelty, matriks state of the art, uji kelayakan. |
| `03_Tahap_02_Rumusan_Masalah/` | Luaran Tahap 2: pertanyaan penelitian, tujuan, hipotesis, definisi operasional, metrik SIWG. |
| `04_Tahap_03_Kerangka_Teori/` | Luaran Tahap 3: draf Bab II, peta teori, tabel klaim–sumber, audit referensi, register CSV. |
| `05_Evaluasi_Tahap_1-3/` | Evaluasi kritis, kebijakan tier referensi (SOTA vs daftar pustaka), checklist perbaikan. |
| `06_Tahap_04_Metodologi/` | Luaran Tahap 4: desain skenario, formalisasi, instrumen, rencana statistik, jadwal/risiko/etika. |
| `07_Bab_III_Metodologi/` | Draf Bab III, lampiran protokol pilot/rollback, matriks alinyemen metodologi. |
| `08_Bab_I-II/` | Draf Bab I–II konsolidasi, matriks konsistensi, daftar simbol, catatan penyusunan. |
| `09_Verifikasi_dan_Pencarian/` | Log pencarian gap (P-01), verifikasi 7 klaim (P-04), kandidat referensi baru. |
| `10_Pra_Penelitian/` | Protokol baseline 3 ISP read-only dan matriks keputusan dual vs tri-ISP. |
| `11_Kolektor_Baseline/` | Kolektor baseline read-only, analisis JSONL, konfigurasi contoh, dan README. |

## Aturan kerja

1. Naskah aktif **tidak** ditulis di folder arsip.
2. Setiap tahap punya luaran yang dapat diperiksa dan kriteria lulus.
3. Setiap klaim kebaruan harus bisa dijawab dengan: *apa yang baru, dibanding siapa,
   dan bukti apa yang akan dihasilkan.*
4. Keputusan lingkup dicatat di `01_Manajemen_Proposal/01_Log_Keputusan.md`
   agar tidak ada istilah atau klaim yang saling bertentangan antar-bab.

## Status

- [x] Tahap 0 — Konsolidasi dan pemindahan materi lama
- [x] Tahap 1 — Peta gap dan pernyataan novelty
- [x] Tahap 2 — Rumusan masalah, tujuan, hipotesis
- [x] Tahap 3 — Kerangka teori dan state of the art
- [x] Tahap 3.5 — Evaluasi dan perbaikan (blocking B-01 s.d. B-04 selesai)
- [x] Tahap 4 — Metodologi dan desain evaluasi
- [x] Tahap 5 — Instrumen, etika, manajemen risiko (dokumen; kalibrasi lapangan belum)
- [ ] Tahap 6 — Penulisan naskah proposal (draf Bab I–III selesai; P-01 s.d. P-04 selesai; abstrak dan daftar pustaka belum)
- [x] Baseline awal 2,2 jam dianalisis (bukan baseline final)
- [ ] Baseline final 7–14 hari + throughput 1 detik
- [ ] Tahap 7 — Uji kelayakan internal dan simulasi seminar
- [ ] Tahap 8 — Seminar proposal dan revisi
