# Tahap 2 — Rumusan Masalah dan Tujuan

**Dokumen:** `01_Rumusan_Masalah_dan_Tujuan.md`
**Status:** Draf kerja Tahap 2
**Arah penelitian:** Opsi D — SPA-HSM + metrik gabungan SIWG
**Fungsi:** Menerjemahkan gap Tahap 1 menjadi pertanyaan payung, sub-pertanyaan,
dan tujuan yang saling memetakan satu-satu.

---

## 1. Pertanyaan Penelitian Payung

> Sejauh mana **SPA-HSM** — *state machine* yang memadukan skor kualitas
> multi-kriteria, penghalusan EWMA, histeresis asimetris sadar-transien, dan
> `AFFINITY_LOCK` — mampu mengendalikan **trade-off antara stabilitas keputusan
> dan kontinuitas sesi** pada WAN dual-ISP FO–LEO, dan bagaimana kontribusi
> masing-masing komponen serta parameter *dwell* membentuk *frontier* trade-off
> tersebut?

Pertanyaan payung ini sengaja menyebut **trade-off**, bukan sekadar "peningkatan
kinerja". Alasannya: setiap mekanisme yang menstabilkan keputusan berpotensi
memperlambat pemulihan, dan setiap perubahan rasio berpotensi mengganggu sesi.
Yang dinilai bukan salah satu sisi, melainkan posisi sistem pada kurva trade-off.

---

## 2. Sub-Pertanyaan Penelitian

| Kode | Pertanyaan | Gap | Sifat |
|---|---|---|---|
| **RQ1** | Bagaimana merumuskan skor kualitas $Q_i(t)$ dari metrik QoS dengan normalisasi berbatas tetap dan bobot statis, lalu memetakannya menjadi proporsi PCC diskret yang memenuhi $\sum b_i = N$ serta batas $b_{min}$ dan $b_{max}$? | G-M2 | Formalisasi |
| **RQ2** | Bagaimana merancang aturan *dwell* histeresis asimetris yang diturunkan dari durasi transien LEO terukur, dan bagaimana aturan itu menggeser trade-off antara *flapping rate* dan *recovery latency*? | G-M1 | Metodologis |
| **RQ3** | Seberapa besar `AFFINITY_LOCK` menurunkan gangguan sesi TCP — diukur sebagai RST *rate* dan proporsi aliran terganggu — dan bagaimana interaksinya dengan bentuk histeresis? | G-E1 | Empiris |
| **RQ4** | Bagaimana kinerja gabungan SPA-HSM diukur dengan *Session-Impact-Weighted Goodput* (SIWG), dan seberapa besar kontribusi tiap komponen berdasarkan ablasi pada konteks FO–LEO? | G-I1, G-C1 | Empiris/komparatif |
| **RQ5** | Apakah *Algorithm Core* memenuhi kontrak antarmuka dan menghasilkan keputusan identik ketika dijalankan pada dua adapter berbeda? | G-C2 | Rekayasa |

**Aturan:** tidak ada sub-pertanyaan yang hanya bisa dijawab "ya/tidak". Setiap
RQ harus menghasilkan angka, model, atau artefak yang dapat diperiksa.

---

## 3. Tujuan Penelitian

### Tujuan umum

Mengembangkan dan mengevaluasi SPA-HSM sebagai mekanisme kendali proporsi PCC
yang menjaga stabilitas keputusan sekaligus kontinuitas sesi pada WAN heterogen
FO–LEO, serta menghasilkan panduan parameter yang dapat dipakai praktisi.

### Tujuan khusus

| Kode | Tujuan | Menjawab | Luaran terukur |
|---|---|---|---|
| **T1** | Merumuskan $Q_i(t)$ berbasis EWMA–SAW dengan normalisasi berbatas tetap, serta pemetaan formal $Q_i(t) \rightarrow$ bucket PCC. | RQ1 | Rumus, tabel parameter, contoh perhitungan, uji granularitas |
| **T2** | Merancang aturan *dwell* $k_{down}, k_{up}$ yang diturunkan dari durasi transien LEO, dan menganalisis pengaruhnya terhadap flapping dan recovery latency. | RQ2 | Turunan aturan, kurva trade-off, analisis sensitivitas |
| **T3** | Mengimplementasikan `AFFINITY_LOCK` dan mengukur dampaknya terhadap RST rate serta proporsi aliran terganggu. | RQ3 | Mekanisme teknis, data RST, uji non-inferioritas |
| **T4** | Mengevaluasi kontribusi histeresis dan affinity secara terpisah dan bersama melalui ablasi, menggunakan SIWG sebagai ukuran gabungan. | RQ4 | Dataset ablasi, effect size, peringkat SIWG |
| **T5** | Menguji kontrak *Abstract Allocation Interface* dan portabilitas *Algorithm Core* melalui *mock adapter* dan adapter kedua. | RQ5 | Uji konformitas, bukti keputusan identik |

---

## 4. Matriks Alinyemen

| Gap | RQ | Tujuan | Hipotesis | Metrik utama | Bab |
|---|---|---|---|---|---|
| G-M2 | RQ1 | T1 | — (formalisasi) | Galat pemetaan bucket, stabilitas granularitas | I, II |
| G-M1 | RQ2 | T2 | H1, H2 | Flapping rate, recovery latency p95 | I, II |
| G-E1 | RQ3 | T3 | H3a | RST rate, flow disruption ratio | I, II |
| G-I1, G-C1 | RQ4 | T4 | H3b, H4 | Goodput, latency p95, SIWG | I, II |
| G-C2 | RQ5 | T5 | H5 | Kesesuaian antarmuka, identik/tidak | I, II |

**Uji konsistensi:** setiap RQ punya tepat satu tujuan; setiap tujuan punya
minimal satu hipotesis atau luaran formal; setiap hipotesis punya metrik dan uji
(di dokumen `02_Hipotesis_dan_Definisi_Operasional.md`).

---

## 5. Batas Pertanyaan (Agar Tidak Melebar)

| Hal yang tidak ditanyakan | Alasan |
|---|---|
| Apakah SPA-HSM lebih baik dari semua algoritma load balancing? | Tidak dapat diuji dengan satu penelitian |
| Apakah sistem dapat memprediksi degradasi sebelum terjadi? | Itu Opsi C, di luar lingkup |
| Apakah pengguna merasa lebih puas (QoE)? | Penelitian mengukur QoS, bukan persepsi |
| Apakah metode ini optimal secara global? | Tidak ada klaim optimalitas; yang dicari adalah perbaikan terukur |
| Apakah bobot SAW sebaiknya dipelajari otomatis? | Bobot statis adalah keputusan lingkup (K-03) |
| Apakah sistem bekerja pada semua vendor? | Hanya satu adapter nyata + mock (K-04) |

---

## 6. Kriteria Jawaban yang Memuaskan

| RQ | Jawaban dianggap memuaskan jika |
|---|---|
| RQ1 | Semua simbol terdefinisi; pemetaan menghasilkan $\sum b_i = N$ untuk 10.000 kombinasi skor uji; tidak ada pelanggaran $b_{min}/b_{max}$ |
| RQ2 | Ada aturan eksplisit yang menghubungkan $T_s$, durasi transien, dan $k_{down}$; kurva trade-off dihasilkan dari minimal 3 set parameter |
| RQ3 | RST diukur, bukan diasumsikan; ada interval kepercayaan; perlakuan "tanpa affinity" didefinisikan teknis |
| RQ4 | Ada effect size dan 95% CI; SIWG dihitung dengan analisis sensitivitas $\lambda$ |
| RQ5 | Ada matriks uji konformitas dan perbandingan urutan keputusan |

---

## 7. Rumusan Masalah untuk Naskah (Versi Ringkas)

Versi ini yang akan dipakai di Bab I:

> Pengelolaan proporsi trafik PCC pada WAN heterogen FO–LEO masih bertumpu pada
> rasio statis yang tidak merespons degradasi link secara *real-time*. Pembaruan
> rasio secara naif menimbulkan flapping dan berpotensi mengganggu sesi TCP,
> sedangkan parameter histeresis yang ada tidak diturunkan dari dinamika transien
> LEO dan dampaknya terhadap sesi tidak diukur. Penelitian ini merumuskan dan
> mengevaluasi SPA-HSM untuk mengendalikan trade-off stabilitas–kontinuitas–kinerja,
> serta mengukur kontribusi masing-masing komponennya melalui ablasi.

---

## 8. Yang Dibutuhkan Sebelum Tahap 3

- [ ] Konfirmasi pembimbing atas lima sub-RQ (terutama RQ5, yang bersifat opsional).
- [ ] Penetapan jumlah skenario (D-02) karena memengaruhi kekuatan H2 dan H4.
- [ ] Konfirmasi ketersediaan data untuk RQ3 dan RQ4 (pilot).
- [ ] Persetujuan penggunaan SIWG sebagai metrik tambahan (D-04).
