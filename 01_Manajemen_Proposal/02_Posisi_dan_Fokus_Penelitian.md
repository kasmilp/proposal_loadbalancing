# Posisi dan Fokus Penelitian

**Status:** Dokumen kanonik — rujukan seluruh 01–12
**Prinsip bahasa:** kata kerja utama adalah **memodifikasi**. Hindari
“merancang”, “menciptakan”, dan “membangun dari nol” untuk menjelaskan
kontribusi penelitian.

---

## 1. Pernyataan Posisi

Penelitian ini **memodifikasi fungsi kontrol** yang dibangun di atas **kapabilitas
dasar platform**—PCC statis, *connection tracking*, dan monitoring—yang tersedia
pada RouterOS. Modifikasi dilakukan pada cara mekanisme tersebut mengamati kualitas
ISP, mendeteksi degradasi, menghitung ulang persentase alokasi koneksi baru,
membentuk koneksi baru, dan memperlakukan koneksi lama. Mekanisme hasil
modifikasi—SPA-HSM—belum ditemukan dalam literatur; karena itu, kebaruannya
terletak pada **modifikasi kebijakan kontrol**, bukan pada keberadaan mekanisme
dasar.

Penelitian ini **tidak** memodifikasi teknologi Starlink, **tidak** mengubah
algoritma PCC, **tidak** menyusun mekanisme dari nol, dan **tidak** mengklaim
bahwa kontroler adaptif yang identik sudah beroperasi. Yang tersedia adalah
kapabilitas platform yang menjadi titik tolak modifikasi.

---

## 2. Tiga Lapis yang Harus Dibedakan

| Lapis | Status | Isi |
|---|---|---|
| **Kapabilitas dasar platform** | Tersedia pada platform | PCC statis, *conntrack*, monitoring |
| **Fungsi kontrol yang dimodifikasi** | **Objek penelitian** | Pengamatan, deteksi, alokasi, perlakuan sesi, evaluasi |
| **Mekanisme hasil modifikasi** | Baru, belum ditemukan yang identik | SPA-HSM |

Kalimat kunci:

> “Penelitian ini memodifikasi fungsi kontrol di atas kapabilitas PCC statis dan
> conntrack yang tersedia pada platform. Mekanisme hasil modifikasi—SPA-HSM—belum
> ditemukan dalam literatur; karena itu, kebaruannya terletak pada modifikasi
> kebijakan kontrol, bukan pada keberadaan mekanisme dasar, dan bukan pada klaim
> bahwa kontroler tersebut sudah beroperasi sebelumnya.”

---

## 3. Apa yang Dimodifikasi dan Apa yang Tidak

| Lapis | Kapabilitas awal | Modifikasi | Bukti |
|---|---|---|---|
| Persepsi | Metrik mentah/ambang tunggal | EWMA + SAW + batas acuan tetap | Stabilitas $Q_i(t)$ |
| Deteksi | Ambang tunggal | Histeresis dua ambang + *dwell* | Flapping, recovery |
| Alokasi | Rasio statis/berbasis kualitas saja | Alokasi *stock-flow aware* | ELS, time-to-rebalance |
| Sesi | Preservasi *conntrack* implisit | Batasan *affinity* eksplisit | RST, session retention |
| Evaluasi | QoS agregat | SIWG + ELS + RST | Trade-off stabilitas–kontinuitas |

Yang **tidak** dimodifikasi:

- teknologi Starlink dan karakteristik propagasinya;
- mekanisme internal PCC dan *connection tracking* RouterOS;
- MikroTik sebagai platform;
- topologi dual-ISP FO–LEO sebagai lingkungan uji.

---

## 4. Loop Adaptasi yang Dimodifikasi

1. **Observation** — membaca kualitas ISP: throughput, delay, jitter, loss,
   utilisasi.
2. **Degradation detection** — memisahkan transien dari degradasi sustained
   melalui histeresis dan *dwell*.
3. **Evaluation** — menilai kualitas link sekaligus **stok koneksi lama** dan
   **aliran koneksi baru**.
4. **Recomputation** — menghitung ulang persentase alokasi untuk koneksi baru.
5. **New-connection formation** — menerapkan persentase baru pada koneksi baru.
6. **Old-connection preservation** — membiarkan koneksi lama tetap pada jalurnya,
   tanpa pemutusan paksa.

Novelty bukan pada “PCC dinamis”, tetapi pada **hubungan antar-langkah** dan
**objek yang dipertimbangkan pada langkah 3–4**.

---

## 5. Formalisasi Stock-Flow

| Simbol | Arti |
|---|---|
| $S_i(t)$ | Stok koneksi lama yang masih aktif di link $i$ |
| $F_i(t)$ | Laju koneksi baru yang dialokasikan ke link $i$ |
| $L_i(t)$ | Pangsa beban efektif: $(S_i+F_i)/\sum_k(S_k+F_k)$ |
| $T_i(t)$ | Target kualitas: $Q_iH_i/\sum_k Q_kH_k$ |
| $W_i(t)$ | Persentase alokasi untuk koneksi baru |

Modifikasi kebijakan alokasi:

$$W_i(t)=\text{clip}\left(T_i(t)+\kappa\left(T_i(t)-\frac{S_i(t)}{\sum_k S_k(t)}\right),\;W_{\min},\;W_{\max}\right)$$

Makna:

- jika stok lama di link $i$ melebihi target, alokasi koneksi baru dikurangi;
- jika stok lama di bawah target, alokasi koneksi baru ditambah;
- $\kappa$ mengatur agresivitas koreksi;
- $W_{\min}/W_{\max}$ mencegah *starvation* dan *overload*;
- histeresis menjaga agar koreksi tidak berbalik arah.

**Metrik baru:**

- **Effective Load Skew (ELS):** $\frac{1}{2}\sum_i |L_i-T_i|$; 0 = alokasi efektif sesuai target.
- **Time-to-rebalance:** waktu hingga ELS turun di bawah ambang setelah degradasi.
- **Session retention rate:** proporsi koneksi lama yang tetap di jalurnya.
- **RST flow:** memastikan preservasi tidak menimbulkan reset.

---

## 6. Klaim Novelty

| Kode | Klaim | Jenis |
|---|---|---|
| **N1** | Modifikasi fungsi observasi dan deteksi: kualitas multi-kriteria + histeresis *dwell* | Pendukung |
| **N2** | Modifikasi kebijakan alokasi menjadi **stock-flow aware**: mempertimbangkan stok koneksi lama dan aliran koneksi baru | **Utama** |
| **N3** | Modifikasi perlakuan sesi: koneksi lama dipertahankan, koneksi baru diarahkan | **Utama** |
| **N4** | Modifikasi evaluasi: SIWG + ELS + time-to-rebalance + session retention | Pendukung |

“PCC dinamis” **bukan** novelty utama. PCC adalah aktuator; yang dimodifikasi
adalah kebijakan controller yang mengendalikannya.

---

## 7. Kebijakan Bahasa

Gunakan:

- “memodifikasi fungsi kontrol di atas kapabilitas PCC statis”;
- “memodifikasi kebijakan alokasi”;
- “memodifikasi cara controller mengamati, memutuskan, dan mengalokasikan”;
- “mekanisme hasil modifikasi”;
- “kapabilitas dasar platform”.

Hindari:

- “merancang kontroler”;
- “menciptakan mekanisme”;
- “membangun dari nol”;
- “memodifikasi kontroler adaptif yang sudah berjalan” (overclaim);
- “mekanisme dasar yang sudah beroperasi pada controller”;
- “PCC dinamis” sebagai klaim utama.

---

## 8. Judul yang Dipakai

**Judul kerja:**

> Mekanisme Kontrol Adaptif untuk Alokasi Koneksi Sadar-Sesi pada Jaringan
> Heterogen FO–LEO

**Subjudul:**

> Implementasi dan Evaluasi pada Platform MikroTik PCC

Nama mekanisme: **SPA-HSM**. Nama ini adalah nama mekanisme hasil modifikasi,
bukan nama algoritma PCC.

---

## 9. Dampak ke Rumusan Masalah

Pertanyaan payung yang dipakai:

> Bagaimana mekanisme kontrol adaptif pada jaringan heterogen FO–LEO dapat
> mengamati kualitas dan degradasi ISP, menghitung ulang persentase alokasi
> koneksi baru dengan mempertimbangkan stok koneksi lama, dan mempertahankan
> koneksi yang telah terbentuk tanpa mengorbankan kinerja agregat?

Sub-RQ:

1. Bagaimana memodifikasi persepsi kualitas ISP agar stabil dan komparabel?
2. Bagaimana memodifikasi deteksi degradasi agar transien tidak memicu flapping?
3. Bagaimana memodifikasi alokasi agar mempertimbangkan stok koneksi lama dan aliran koneksi baru?
4. Seberapa besar modifikasi tersebut menurunkan ELS/time-to-rebalance tanpa menaikkan RST?
5. Apakah mekanisme hasil modifikasi memenuhi kontrak dan portabel di dua adapter?

---

## 10. Dampak ke Hipotesis

H1–H5 tetap. Tambahan:

**H3c — Stock-aware allocation.** Alokasi yang mempertimbangkan stok koneksi lama
menurunkan *effective load skew* dan *time-to-rebalance* dibanding alokasi berbasis
kualitas saja, tanpa menaikkan RST flow.

---

## 11. Dampak ke Eksperimen

Tambahkan satu kondisi:

| Kondisi | Alokasi | Histeresis | Affinity | Peran |
|---|---|---|---|---|
| F | Kualitas saja | Asimetris | On | Proposed tanpa stock |
| **H** | **Stock-aware** | **Asimetris** | **On** | **Proposed utama** |

Perbandingan **F vs H** mengisolasi kontribusi *stock-flow aware allocation*.

---

## 12. Batas Klaim

- Dual-ISP FO–LEO; bukan generalisasi >2 ISP.
- Starlink sebagai kasus acuan *upper bound* transien.
- Bobot SAW statis.
- Satu adapter nyata + mock; portabilitas diuji lewat kontrak.
- QoS, bukan QoE.
- Stabilitas empiris, bukan pembuktian formal *control loop*.
- Desain 2×2 + pembanding + H; bukan faktorial penuh 3×2.

---

## 13. Rujukan Dokumen

- Bab I–II: `08_Bab_I-II/`
- Bab III: `07_Bab_III_Metodologi/`
- Metodologi: `06_Tahap_04_Metodologi/`
- Gap/novelty: `02_Tahap_01_Gap_dan_Novelty/`
- RQ/hipotesis: `03_Tahap_02_Rumusan_Masalah/`
- Teori: `04_Tahap_03_Kerangka_Teori/`
- Baseline: `10_Pra_Penelitian/`
- Kolektor: `11_Kolektor_Baseline/`
- Presentasi: `12_Presentasi/`
