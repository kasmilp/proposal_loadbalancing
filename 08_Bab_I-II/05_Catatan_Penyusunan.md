# Catatan Penyusunan Bab I–II

**Dokumen:** `05_Catatan_Penyusunan.md`
**Fungsi:** Mencatat apa yang berubah dari draf lama dan apa yang masih harus
diselesaikan.

---

## 1. Yang Berubah dari Draf Lama

| Aspek | Draf lama (arsip) | Draf baru |
|---|---|---|
| Judul | Menonjolkan PCC MikroTik | Menonjolkan SPA-HSM dan WAN FO–LEO |
| Nama algoritma | ALQI/TLABA bercampur | Hanya SPA-HSM |
| Jumlah skenario | 8 (A–H) | 7 kondisi (A–G) |
| Desain | Diklaim 3×2 | 2×2 + dua pembanding + baseline G |
| Batas recovery | 60 detik | 90 detik |
| H3a | Dua syarat setara | Primer non-inferior; sekunder <1% |
| Metrik gabungan | Belum ada | SIWG |
| Kualitas referensi | Campur | Tier T1/T2/T3; T3 hanya konteks |
| Bab II | Belum ada | Draf lengkap dengan peta teori |
| Bab III | Belum ada | Draf lengkap dengan formalisasi dan statistik |
| Posisi MikroTik | Ambigu | Adapter/testbed, bukan objek |

---

## 2. Kekuatan Draf Sekarang

1. Rantai RQ → tujuan → hipotesis → metrik → uji tersambung.
2. Tiga novelty eksplisit: aturan *dwell*, pemetaan bucket, SIWG + ablasi.
3. Angka dan istilah konsisten di Bab I–III.
4. Batas klaim jujur: satu adapter, dua ISP, QoS bukan QoE.
5. Ada rencana statistik dan protokol keselamatan.

---

## 3. Yang Masih Harus Diselesaikan

### Sebelum seminar

| Item | Kode | Dampak jika tertunda |
|---|---|---|
| Log pencarian gap | P-01 | Klaim "belum ditemukan" lemah |
| Referensi PCC internasional | P-02 | SOTA PCC dinilai tipis |
| Referensi MPTCP/kontinuitas sesi | P-03 | H3a tanpa landasan teori |
| Verifikasi 7 klaim halaman | P-04 | Angka bisa salah |
| Audit sitasi | P-05 | Sitasi yatim |
| Gaya sitasi | D-10 | Format tidak sesuai pedoman |
| Telemetri Starlink | D-05 | Instrumen perlu fallback |
| Izin lokasi | D-06 | Kampanye tidak bisa mulai |

### Setelah naskah tiga bab

1. Abstrak Indonesia dan Inggris + kata kunci.
2. Daftar isi, daftar tabel, daftar gambar.
3. Daftar pustaka final (APA 7, 35–50 referensi, ≥15 SOTA inti).
4. Lampiran: tabel parameter, tabel skenario, protokol pilot, kuesioner/izin.
5. Penomoran rumus, tabel, dan gambar.
6. Pemeriksaan format sesuai pedoman kampus.

---

## 4. Urutan Kerja yang Disarankan

```
1. P-01 + P-04        (verifikasi gap dan angka)
2. P-02 + P-03        (tambah referensi)
3. P-05 + D-10        (audit sitasi dan format)
4. Abstrak + daftar isi/tabel/gambar
5. Uji kelayakan internal (30 pertanyaan penguji)
6. Seminar proposal
```

---

## 5. Berkas Sumber

| Kebutuhan | Berkas |
|---|---|
| Gap dan novelty | `02_Tahap_01_Gap_dan_Novelty/` |
| RQ dan hipotesis | `03_Tahap_02_Rumusan_Masalah/` |
| Teori dan SOTA | `04_Tahap_03_Kerangka_Teori/` |
| Evaluasi dan tier referensi | `05_Evaluasi_Tahap_1-3/` |
| Metodologi | `06_Tahap_04_Metodologi/` |
| Bab III | `07_Bab_III_Metodologi/` |
| Bab I–II | `08_Bab_I-II/` |

---

## 6. Catatan Kecil

- P-04 selesai: klaim 15 detik, 137→90,2 Mbps, dan QoS/QoE sudah diverifikasi;
  penanda **[verifikasi]** dihapus dari Bab I–II.
- Angka rain fade tidak dimasukkan ke Bab I; di Bab II angka 90,2 Mbps dipakai
  dengan sitasi halaman 5.
- Klaim *oversubscription/contention* FO dihapus karena tidak didukung sumber;
  diganti dengan kepadatan pelanggan dan gangguan akses (Safitri et al., 2016).
- Klaim "komputasi berat" untuk ANN/metaheuristik dilunakkan menjadi alasan desain,
  bukan temuan literatur.
- Baseline G memakai waktu pemulihan `netwatch` 60 detik; ini berbeda dari
  $R_{max}=90$ detik untuk *recovery latency* SPA-HSM.
- Jika P-02 tidak menemukan cukup referensi T1, turunkan klaim SOTA PCC dan
  perkuat posisi pada konteks lokal, bukan menaikkan klaim.
