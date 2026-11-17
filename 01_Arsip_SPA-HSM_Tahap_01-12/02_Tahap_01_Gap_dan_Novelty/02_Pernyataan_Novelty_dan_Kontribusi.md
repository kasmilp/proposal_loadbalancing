# Tahap 1 — Pernyataan Novelty dan Kontribusi

**Dokumen:** `02_Pernyataan_Novelty_dan_Kontribusi.md`
**Status:** Draf kerja Tahap 1 — diperbarui 17 November 2026
**Fungsi:** Mengubah gap menjadi klaim kebaruan yang dapat dipertahankan.
**Prinsip bahasa:** gunakan **memodifikasi** sebagai kata kerja utama. Hindari
“merancang”, “menciptakan”, dan “membangun dari nol”.

---

## 1. Prinsip

Novelty bukan “metode yang belum pernah dipakai”. Novelty adalah **klaim bahwa
kemampuan baru dihasilkan melalui modifikasi**, disertai pembanding dan bukti.

Rumus yang dipakai:

> **Berbeda dari** [pembanding], **penelitian ini memodifikasi** [fungsi kontrol],
> **sehingga** [kemampuan/bukti baru yang sebelumnya tidak tersedia].

Yang dimodifikasi adalah **fungsi kontrol di atas kapabilitas PCC statis dan
conntrack yang tersedia pada platform**—bukan Starlink, bukan algoritma PCC, dan
bukan kontroler yang diklaim sudah beroperasi.

---

## 2. Novelty Statement

> Penelitian ini memodifikasi fungsi kontrol di atas kapabilitas PCC statis dan
> *connection tracking* yang tersedia pada platform. Kebaruan bukan pada “PCC
> dinamis”, melainkan pada **kebijakan alokasi *stock-flow aware*** yang
> mempertimbangkan stok koneksi lama dan aliran koneksi baru, serta pada
> **evaluasi trade-off stabilitas–kontinuitas** yang memisahkan flapping, RST,
> *effective load skew*, dan waktu rebalance. Mekanisme hasil modifikasi—SPA-HSM—
> belum ditemukan dalam literatur; karena itu, kebaruannya terletak pada
> modifikasi kebijakan kontrol dan bukti empirisnya.

---

## 3. Lima Klaim Kebaruan

### N1 — Modifikasi persepsi dan deteksi (pendukung)

**Klaim.** Penelitian ini memodifikasi cara controller mengamati kualitas ISP dan
mendeteksi degradasi: dari metrik mentah/ambang tunggal menjadi EWMA–SAW dengan
batas acuan tetap, dilanjutkan histeresis dua ambang dan *dwell*.

**Pembanding.** Studi PCC umumnya menetapkan rasio dari kapasitas atau metrik
tunggal (Amalia et al., 2022; Arfianita et al., 2024). Studi histeresis memakai
ambang, tetapi tidak menurunkannya dari durasi transien link (Tournaire et al.,
2023).

**Bukti.** Formalisasi $Q_i(t)$, tabel parameter, analisis aliasing, dan kurva
flapping–recovery.

**Kekuatan:** sedang. Ini fondasi, bukan novelty utama.

---

### N2 — Modifikasi alokasi menjadi *stock-flow aware* (utama)

**Klaim.** Penelitian ini memodifikasi kebijakan alokasi dari berbasis kualitas
saja menjadi kebijakan yang mempertimbangkan **stok koneksi lama** $S_i(t)$ dan
**aliran koneksi baru** $F_i(t)$.

**Pembanding.** Studi PCC dan *load balancing* umumnya menghitung rasio dari
kondisi link saat ini dan mengabaikan bahwa koneksi lama tetap menempati link yang
sedang memburuk (Kumar & Golash, 2009; Amalia et al., 2022; Nugroho et al., 2023).
Literatur SD-WAN/DRL mengalokasikan *flow* pada level *overlay*, bukan pada
granularitas koneksi PCC dan *conntrack* (Cruvellier et al., 2025; Giacometti et
al., 2025).

**Bukti.** Rumus koreksi stok:

$$W_i(t)=\text{clip}\left(T_i(t)+\kappa\left(T_i(t)-\frac{S_i(t)}{\sum_k S_k(t)}\right),\;W_{\min},\;W_{\max}\right)$$

serta metrik *effective load skew* (ELS) dan *time-to-rebalance*.

**Kekuatan:** tinggi. Ini klaim paling utama.

---

### N3 — Modifikasi perlakuan sesi (utama)

**Klaim.** Penelitian ini memodifikasi cara controller memperlakukan sesi: koneksi
lama dipertahankan pada jalurnya, sedangkan koneksi baru diarahkan berdasarkan
persentase terbaru. Preservasi sesi diperlakukan sebagai **batasan** dalam
keputusan alokasi, bukan sebagai efek samping.

**Pembanding.** Implementasi PCC praktis memanfaatkan *conntrack* secara implisit
(MikroTik, n.d.). Literatur MPTCP menangani kontinuitas di level transport
(Duchene & Bonaventure, 2017; Jiang et al., 2024), bukan di level kebijakan
alokasi koneksi pada router.

**Bukti.** Definisi teknis `AFFINITY_LOCK`, pengukuran RST *flow*, *session
retention rate*, dan perbandingan dengan perlakuan *flush* selektif.

**Kekuatan:** tinggi. Ini yang membedakan penelitian dari “PCC dinamis”.

---

### N4 — Modifikasi evaluasi (pendukung)

**Klaim.** Penelitian ini memodifikasi evaluasi dari QoS agregat menjadi
SIWG + ELS + *time-to-rebalance* + *session retention*.

**Pembanding.** Studi PCC melaporkan throughput/delay/jitter/loss agregat
(Amalia et al., 2022; Arfianita et al., 2024). Studi yang mengklaim preservasi
sesi tidak mengukur RST atau stok koneksi lama.

**Bukti.** Rumus SIWG, ELS, time-to-rebalance, RST flow, dan analisis sensitivitas
$\lambda$.

**Kekuatan:** sedang. Ini alat ukur, bukan novelty utama.

---

### N5 — Modifikasi kontrak antarmuka (rekayasa)

**Klaim.** Penelitian ini memodifikasi cara logika keputusan dipisahkan dari
eksekusi melalui kontrak antarmuka yang dapat diuji dengan *mock adapter*.

**Pembanding.** Implementasi PCC praktis tertanam pada konfigurasi vendor
(MikroTik, n.d.; Putra & Anton, 2024).

**Bukti.** Spesifikasi antarmuka, *mock adapter*, uji konformitas, dan bukti
keputusan identik pada dua adapter.

**Kekuatan:** sedang. Kontribusi pendukung; jangan mengklaim portabilitas
multi-vendor.

---

## 4. Mengapa Ini Bukan Sekadar Integrasi

| Keberatan | Jawaban |
|---|---|
| “Tinggal menempelkan EWMA, SAW, histeresis, dan PCC.” | Modifikasi mengubah **kopling** antar-komponen: stok koneksi lama masuk ke keputusan alokasi, dan preservasi sesi menjadi batasan. Ini bukan penempelan. |
| “PCC sudah menangani sesi.” | PCC mempertahankan koneksi lama, tetapi justru itu yang menimbulkan **penumpukan stok** di link yang memburuk. Penelitian ini memodifikasi kebijakan untuk mengelolanya. |
| “Histeresis sudah lama ada.” | Histeresis di sini dipakai untuk memisahkan transien dari degradasi sustained dan dihubungkan dengan perhitungan alokasi. |
| “SAW sudah biasa.” | SAW adalah lapisan penyeragam skor, bukan klaim. Klaimnya ada pada kebijakan alokasi dan evaluasi. |
| “Tidak ada metode baru.” | Benar. Klaimnya adalah **modifikasi kebijakan kontrol + bukti empiris**, bukan metode dasar baru. |
| “Ini hanya PCC dinamis.” | PCC adalah aktuator. Yang dimodifikasi adalah fungsi kontrol yang menentukan kapan dan seberapa besar alokasi koneksi baru diubah. |

---

## 5. Peta Kontribusi

| Kode | Kontribusi | Jenis | Gap | Bukti |
|---|---|---|---|---|
| K1 | Modifikasi persepsi & deteksi: EWMA–SAW + histeresis *dwell* | Metodologis | G-M1 | Formalisasi, kurva trade-off |
| K2 | Modifikasi alokasi *stock-flow aware* | **Utama** | G-M3 | Rumus $W_i$, ELS, time-to-rebalance |
| K3 | Modifikasi perlakuan sesi: preservasi + koneksi baru | **Utama** | G-E2 | RST flow, session retention |
| K4 | Formalisasi pemetaan skor → bucket PCC | Pendukung | G-M2 | Rumus, uji granularitas |
| K5 | SIWG + ELS + time-to-rebalance | Pendukung | G-E1 | Rumus, sensitivitas $\lambda$ |
| K6 | Bukti ablasi A–H pada FO–LEO | **Utama** | G-E1, G-C1 | Dataset, effect size |
| K7 | Kontrak antarmuka + mock adapter | Rekayasa | G-C2 | Uji konformitas |

**Kontribusi utama:** **K2 + K3 + K6**.
**Pendukung:** K1, K4, K5, K7.

---

## 6. Elevator Pitch (60 Detik)

> “PCC pada MikroTik membagi koneksi baru dengan rasio statis. Koneksi lama tetap
> di jalurnya. Ketika Starlink memburuk, stok koneksi lama menumpuk di link yang
> sedang buruk, sementara koneksi baru tetap bisa diarahkan. Penelitian ini
> memodifikasi fungsi kontrol di atas kapabilitas PCC: mengamati kualitas,
> mendeteksi degradasi sustained, menghitung ulang persentase koneksi baru dengan
> mempertimbangkan stok koneksi lama, dan mempertahankan koneksi lama. Kebaruan
> bukan ‘PCC dinamis’, tetapi kebijakan *stock-flow aware* dan bukti empirisnya.”

---

## 7. Batas Klaim

Hal-hal berikut **tidak** diklaim:

- Tidak mengklaim memodifikasi Starlink.
- Tidak mengklaim mengubah algoritma PCC.
- Tidak mengklaim bahwa kontroler adaptif yang identik sudah beroperasi.
- Tidak mengklaim metode MCDM, EWMA, atau histeresis baru.
- Tidak mengklaim generalisasi ke lebih dari dua ISP.
- Tidak mengklaim portabilitas terbukti ke semua vendor.
- Tidak mengklaim menggantikan SD-WAN *enterprise*.
- Tidak mengklaim kestabilan formal *control loop*.
- Tidak mengklaim QoE atau kepuasan pengguna.

---

## 8. Opsi Penguatan

Jika pembimbing menilai novelty masih lemah:

### Opsi A — Batas analitis *stock-flow convergence*

Turunkan batas waktu rebalance atau syarat konvergensi ELS sebagai fungsi
$\kappa$, laju kedatangan koneksi, dan waktu *idle* conntrack.

- **Kelebihan:** novelty analitis naik.
- **Risiko:** membutuhkan asumsi laju kedatangan dan distribusi durasi sesi.
- **Kelayakan:** sedang.

### Opsi B — Perluas SIWG

Tambahkan komponen ELS atau *session retention* ke dalam SIWG.

- **Kelebihan:** satu angka untuk trade-off.
- **Risiko:** pembobotan perlu sensitivitas.
- **Kelayakan:** tinggi.

**Rekomendasi:** pertahankan SIWG sebagai metrik utama, tambahkan ELS dan
time-to-rebalance sebagai metrik terpisah. Opsi A menjadi lampiran analitis jika
waktu memungkinkan.

---

## 9. Catatan Pembaruan

- Dokumen ini menggantikan versi sebelumnya yang menekankan “aturan dwell” dan
  “pemetaan bucket” sebagai novelty utama.
- Novelty utama sekarang adalah **stock-flow aware allocation + session
  preservation**, dengan dukungan observasi/deteksi dan evaluasi.
- Istilah “PCC dinamis” tidak dipakai sebagai klaim utama.
