# Verifikasi Klaim (P-04)

**Tanggal:** 12 November 2026
**Metode:** ekstraksi teks PDF dengan PyMuPDF, pencarian per halaman
**Cakupan:** 7 klaim berstatus "verifikasi halaman" pada
`04_Tahap_03_Kerangka_Teori/03_Tabel_Klaim_dan_Sumber.md`

---

## 1. Ringkasan

| Status | Jumlah | Klaim |
|---|---:|---|
| **Terverifikasi** | 4 | C11, C12, C14, C37 |
| **Tidak terverifikasi** | 1 | C08 |
| **Inferensi, bukan klaim langsung** | 2 | C33, C34 |
| **Total** | **7** | |

**Implikasi:** empat klaim bisa langsung dipakai; satu klaim harus diubah; dua
klaim harus dilunakkan menjadi penalaran desain, bukan pernyataan literatur.

---

## 2. Rincian Verifikasi

### C11 — Pola periodik 15 detik pada Starlink

**Sumber:** Garcia, Sundberg, & Brunstrom (2025), *A Detailed Characterization of
Starlink One-way Delay*, LEO-NET 2025.

**Lokasi:** halaman 1 (abstrak dan pendahuluan).

**Kutipan:**
> "By measuring both uplink and downlink paths, the study uncovers significant
> differences in scheduling behavior, with uplink delays more affected by
> Starlink's periodic 15-second reconfiguration cycles."

> "Starlink uses a 15 second reconfiguration interval."

**Status:** **Terverifikasi.**
**Catatan:** klaim "paling terdampak pada arah uplink" juga didukung. Klaim
"aliasing" didukung: penulis menyebut interval pengukuran yang terlalu kasar dapat
menimbulkan aliasing.

---

### C12 — Pola penurunan throughput pada batas interval 15 detik

**Sumber 1:** Hammer, Addanki, Franke, & Schmid (2024), *Starlink Performance
through the Edge Router Lens*, LEO-NET 2024.

**Lokasi:** halaman 1 (abstrak).

**Kutipan:**
> "Starlink has been shown to exhibit a periodic pattern with a characteristic
> throughput drop on the boundaries of 15s intervals."

**Sumber 2:** Mohan et al. (2024), *A Multifaceted Look at Starlink Performance*,
WWW 2024.

**Lokasi:** halaman 1–2.

**Kutipan:**
> "…globally synchronized '15-second reconfiguration intervals' of the satellite
> links that cause substantial latency and throughput variations."

> "…Starlink performs network reconfigurations every 15 s, leading to noticeable
> latency and throughput degradations at sub-second granularity."

**Status:** **Terverifikasi.**
**Catatan:** Hammer menyatakan penyebabnya di *core network*, bukan *edge router*.
Ini memperkuat argumen bahwa transien tidak dapat dihilangkan dari sisi pengguna.

---

### C14 — Angka penurunan throughput saat hujan

**Sumber:** Ullah, Heikkinen, Uitto, Anttonen, & Mikhaylov (2025), *Impact of
Weather on Satellite Communication: Evaluating Starlink Resilience*.

**Lokasi:** halaman 5.

**Kutipan:**
> "One can observe the median downlink throughput drops from 137 Mbps to 90.2 Mbps
> during the rain. Similarly, the median uplink declined from 20.9 Mbps to
> 10.5 Mbps."

**Konteks:** pengukuran di Oulu, Finlandia; intensitas hujan hingga 12,5 mm/jam.

**Status:** **Terverifikasi.**
**Koreksi:** angka downlink adalah **90,2 Mbps**, bukan 90 Mbps. Perbarui Bab II.
**Catatan tambahan:** abstrak melaporkan penurunan median uplink 52,27% dan
downlink 37,84%. Versi terbit: IEEE VTC 2025 Spring,
DOI `10.1109/vtc2025-spring65109.2025.11174614`.

---

### C37 — QoS dan QoE adalah konsep berbeda

**Sumber:** Wang, Pérez Aguilar, Díaz Zayas, Corrales Madueño, Zhang, Hao, & Yu
(2023), *A general QoE assessment framework for applications and services*,
Computer Networks 225, 109641.

**Lokasi:** halaman 1 (pendahuluan).

**Kutipan:**
> "Traditionally Quality of Service (QoS) is the most widely used service quality
> metric, which can be used to assess the performance of telecommunication
> services by performing a series of technical measurements such as throughput,
> delay, jitter, error probability, packet loss, etc."

> "…QoE… user experience…"

**Status:** **Terverifikasi.**
**Tindakan:** tambahkan Wang et al. (2023) ke register dan Bab II 2.2.

---

### C08 — Oversubscription/contention pada FO IndiHome

**Sumber yang diperiksa:** Safitri, Munadi, & Walidainy (2016), *Analisis Kualitas
Jaringan Akses IndiHome untuk Teknologi GPON dan MSAN di STO Darussalam*,
KITEKTRO 1(3), 27–34.

**Lokasi:** halaman 1.

**Isi sumber:**
> "Penurunan kualitas jaringan disebabkan oleh gangguan pada jaringan tembaga
> maupun fiber optik…"

> "…dibedakan dengan jumlah pelanggan yang lebih banyak untuk satu daerah."

**Status:** **Tidak terverifikasi.**
**Masalah:** sumber ini membahas kualitas akses, SNR, redaman, dan Rx Power; **tidak
membahas** *oversubscription* atau *contention ratio*.
**Tindakan:** ganti klaim di Bab I menjadi "kepadatan pelanggan dan gangguan
jaringan akses" dengan sitasi Safitri et al. (2016), **atau** cari sumber baru
khusus oversubscription.

---

### C33 — Load balancing cloud metaheuristik berbiaya komputasi tinggi

**Sumber:** Komathi et al. (2024).

**Temuan:** artikel membahas metaheuristik (ACO) dan metrik *time of overhead*,
tetapi **tidak** menyatakan secara eksplisit bahwa metode tersebut "berbiaya
komputasi tinggi" dibanding PCC.

**Status:** **Inferensi, bukan klaim langsung.**
**Tindakan:** tulis sebagai penalaran desain: "pendekatan metaheuristik umumnya
memerlukan sumber daya komputasi dan data yang lebih besar daripada aturan ambang
sederhana", tanpa mengatribusikannya sebagai temuan Komathi et al.

---

### C34 — Hub multi-ISP berbasis ANN membutuhkan komputasi berat

**Sumber:** Ali et al. (2025).

**Temuan:** artikel menjelaskan model ANN untuk mengalokasikan *data rate* lintas
ISP, tetapi **tidak** melaporkan biaya komputasi secara eksplisit.

**Status:** **Inferensi, bukan klaim langsung.**
**Tindakan:** tulis sebagai alasan desain: "model ANN memerlukan pelatihan dan
sumber daya komputasi yang tidak dirancang untuk perangkat kelas SOHO", lalu
akui sebagai batasan lingkup, bukan temuan Ali et al.

---

## 3. Perubahan Naskah yang Diperlukan

| Lokasi | Sebelum | Sesudah |
|---|---|---|
| Bab I §1.1 | "Kebijakan oversubscription, contention ratio…" | "Kepadatan pelanggan dan gangguan jaringan akses…" (Safitri et al., 2016) |
| Bab II §2.3 | "137 Mbps menjadi 90 Mbps" | "137 Mbps menjadi 90,2 Mbps" |
| Bab II §2.3 | penanda **[verifikasi]** pada C11/C12/C14 | hapus setelah verifikasi |
| Bab II §2.2 | klaim QoS vs QoE tanpa sumber | tambah Wang et al. (2023) |
| Bab II §2.4 | "komputasi berat" untuk ANN/metaheuristik | "memerlukan sumber daya/data lebih besar" sebagai alasan desain |
| Tabel klaim | status C08/C33/C34 | perbarui sesuai §1 |

---

## 4. Bukti yang Disimpan

- Teks ekstrak PDF: `%TEMP%\opencode\pdftext\`
- Skrip ekstraksi: `%TEMP%\opencode\extract_pdfs.py`
- Skrip pencarian klaim: `%TEMP%\opencode\find_claims.py`, `find_more.py`
- Log pencarian: `01_Log_Pencarian_Gap.md`

**Catatan:** nomor halaman mengacu pada PDF yang diekstrak, bukan nomor halaman
jurnal. Saat menulis naskah, gunakan nomor halaman jurnal jika tersedia.
