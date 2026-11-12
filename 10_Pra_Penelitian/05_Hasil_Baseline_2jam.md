# Hasil Baseline 2,2 Jam — 13 November 2026

**Sumber:** `11_Kolektor_Baseline/data/baseline_rb1100ahx4_20261113_050431.jsonl`
**Rentang UTC:** 05:04:32 → 07:17:14
**Durasi:** 2,21 jam
**Record:** 19.706
**Probe:** 17.742 (6 seri: 3 WAN × 2 target)
**Mode:** read-only

---

## 1. Kualitas Data

| Item | Nilai |
|---|---|
| Sampel per seri | 2.957 |
| Median interval probe | 2,35 s |
| p95 interval | 3,85 s |
| Gap maksimum | 26–38 s |
| Error | 3 timeout (0,015%) |
| Cakupan waktu lokal (UTC+8) | ±13.04–15.17 |

**Penilaian:** kualitas data **baik** untuk pilot. Tiga timeout tidak memengaruhi analisis. Gap puluhan detik terjadi sesekali, mungkin saat API lambat.

---

## 2. Ringkasan per WAN

| Interface | Target | Loss | RTT median | RTT p95 | Jitter | Episode |
|---|---|---:|---:|---:|---:|---:|
| ether1-ISP-A (Starlink) | 1.1.1.1 | 0,24% | 47,5 ms | 89,1 ms | 7,0 ms | 35 |
| ether1-ISP-A (Starlink) | 8.8.8.8 | 0,17% | 61,0 ms | 101,8 ms | 6,8 ms | 53 |
| ether2-ISP-B (Starlink) | 1.1.1.1 | 0,30% | 50,4 ms | 98,6 ms | 7,6 ms | 51 |
| ether2-ISP-B (Starlink) | 8.8.8.8 | 0,27% | 63,4 ms | 113,8 ms | 7,8 ms | 84 |
| ether3-ISP-C (FO) | 1.1.1.1 | 0,03% | 46,3 ms | 46,7 ms | 0,36 ms | 1 |
| ether3-ISP-C (FO) | 8.8.8.8 | 0,00% | 46,4 ms | 46,7 ms | 0,27 ms | 0 |

Ambang episode: RTT > 100 ms atau loss > 1%.

---

## 3. Temuan Utama

### 3.1 Heterogenitas nyata antara Starlink dan FO

- Starlink: jitter 6,8–7,8 ms; RTT p95 89–114 ms.
- FO: jitter 0,27–0,36 ms; RTT p95 46,7 ms.
- Loss Starlink 0,17–0,30%; FO 0–0,03%.

Perbedaan satu orde besaran pada jitter mendukung premis penelitian: dua jalur
memiliki dinamika yang berbeda dan tidak boleh diperlakukan sama.

### 3.2 Starlink sering mengalami episode pendek

Dalam 2,2 jam:

- ISP-A: 35–53 episode, median 3,0–3,4 detik.
- ISP-B: 51–84 episode, median 4,7–6,7 detik.
- FO: 0–1 episode.

Ini bukti langsung bahwa Starlink menghasilkan degradasi singkat yang berulang,
persis kondisi yang ingin ditangani histeresis.

### 3.3 Dua Starlink saling berkorelasi

Korelasi residual RTT:

| Pasangan | Target 1.1.1.1 | Target 8.8.8.8 |
|---|---:|---:|
| ISP-A vs ISP-B | **0,683** | **0,704** |
| ISP-A vs FO | -0,037 | 0,008 |
| ISP-B vs FO | -0,016 | 0,018 |

Tumpang tindih episode (Jaccard): 0,296–0,392. Episode A yang punya pasangan B
dalam ±2 detik: 47–54%.

**Implikasi:** dua Starlink di lokasi yang sama tidak independen. Mereka berbagi
hujan, transien global, dan pola beban. FO independen.

### 3.4 Periodisitas 15 detik belum terkonfirmasi pada RTT

Analisis FFT pada RTT yang sudah di-*detrend* menunjukkan:

- periode dominan **≈28,8 detik**, bukan 15 detik;
- autokorelasi lag 15 detik **negatif** (-0,24 s.d. -0,30);
- autokorelasi indikator buruk pada lag 15 hanya 0,03–0,13;
- proporsi gap episode yang dekat 15 detik: 16–30%.

**Interpretasi:** sinyal 15 detik **tidak terlihat jelas pada RTT**. Literatur
(Garcia et al., 2025; Hammer et al., 2024; Mohan et al., 2024) melaporkan
penurunan *throughput* pada batas 15 detik, bukan necessarily RTT. Probe RTT
kecil mungkin tidak menangkap antrean/laju yang turun.

**Konsekuensi:** klaim “transien 15 detik” tidak boleh dipakai sebagai dasar
tunggal untuk menetapkan $k_{down}=20$ tanpa bukti tambahan. Perlu pengukuran
**throughput/interface counter 1 detik** untuk melihat siklus 15 detik.

---

## 4. Kesiapan Penelitian

| Aspek | Status |
|---|---|
| Koneksi read-only | Siap |
| Kualitas data | Baik untuk pilot |
| Heterogenitas FO–LEO | Terkonfirmasi |
| Episode pendek Starlink | Terkonfirmasi |
| Korelasi A–B | Terukur (0,68–0,70) |
| Periodisitas 15 detik | **Belum terkonfirmasi pada RTT** |
| Cakupan waktu | 2,2 jam, siang; belum jam sibuk/hujan |
| Baseline formal 7–14 hari | Belum |

**Putusan:** **boleh lanjut ke pilot dan kalibrasi parameter**, tetapi belum
cukup untuk klaim periodisitas 15 detik atau baseline final.

---

## 5. Keputusan Topologi

Berdasarkan korelasi A–B yang tinggi:

- **Dual-ISP formal A+C** tetap direkomendasikan.
- ISP-B dipakai sebagai **validasi eksternal/kontrol**, bukan link formal ketiga.
- Tri-ISP tidak dinaikkan menjadi klaim utama karena dua LEO tidak independen.

---

## 6. Langkah Berikutnya

1. **Perpanjang baseline** menjadi 7 hari, mencakup:
   - jam sibuk (19.00–23.00),
   - jam rendah (01.00–05.00),
   - minimal satu kejadian hujan.
2. **Tambahkan pengukuran throughput 1 detik** pada ketiga WAN selama 10–15
   menit untuk analisis 15 detik:
   - SNMP `ifHCInOctets`/`ifHCOutOctets` per 1 detik, atau
   - probe UDP/`iperf3` berulang.
3. **Kalibrasi parameter** dari data:
   - $\alpha$ dari varians RTT,
   - $\theta_{low}/\theta_{high}$ dari distribusi Q,
   - $k_{down}$ dari durasi episode nyata (bukan hanya asumsi 15 detik).
4. **Siapkan akun tulis terbatas** untuk pilot intervensi setelah staging lulus.
5. **Jangan ubah konfigurasi** sampai protokol pilot dan rollback siap.

---

## 7. Catatan Metodologis

- Episode dihitung dari probe RTT/loss, bukan dari $Q_i(t)$ penuh.
- Korelasi Pearson mengasumsikan hubungan linier.
- Data 2,2 jam tidak mewakili variasi harian dan cuaca.
- Hasil ini **observasional**, bukan bukti kausal.
