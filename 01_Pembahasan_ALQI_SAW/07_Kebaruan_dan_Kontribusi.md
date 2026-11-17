# 07 — Kebaruan dan Kontribusi Ilmiah

**Status:** Draf kerja
**Fungsi:** Menentukan aspek kebaruan yang **realistis** untuk tingkat S2 dan batas
klaimnya.

**Prinsip [USULAN]:**

> **Berbeda dari** [pembanding], **penelitian ini memodifikasi** [fungsi penilaian
> kualitas link], **sehingga** [kemampuan/bukti baru yang sebelumnya tidak tersedia].

Kata kerja: **memodifikasi**. Hindari "merancang", "menciptakan", "membangun dari nol".

---

## 1. Klaim Kebaruan (realistis untuk S2)

| Kode | Klaim | Dibanding siapa | Bukti yang dihasilkan | Kekuatan |
|---|---|---|---|---|
| **K-A** | **Studi komparatif terkontrol** teknik normalisasi (N-a/N-b/N-c) dan skema pembobotan (statis, entropy, CRITIC, MEREC, hibrida) untuk indeks kualitas link pada **deret metrik real-time FO–LEO** | Vafaei et al. (dataset statis); entropy-SAW (domain seluler 5G) | Matriks kinerja + uji sensitivitas + effect size | **Tinggi** |
| **K-B** | **Mekanisme pembobotan hibrida adaptif** $w(t) = \gamma w^{\text{ahli}} + (1-\gamma) w^{\text{obj}}(t)$ dengan **gerbang kestabilan** | Studi bobot statis; studi bobot objektif tanpa analisis stabilitas | Kurva trade-off akurasi ↔ stabilitas ($\gamma$) | Tinggi |
| **K-C** | **Normalisasi berbatas acuan tetap** (TIPHON/Y.1541) untuk menjaga **komparabilitas temporal** indeks | Min–max dengan batas bergeser | Uji *rank reversal* & stabilitas indeks | Sedang–tinggi |
| **K-D** | **Dekomposisi kontribusi** normalisasi vs pembobotan terhadap kinerja indeks | Studi yang melaporkan "sistem lebih baik" tanpa atribusi | Analisis ablasi 2×2 (normalisasi × bobot) | Sedang–tinggi |

**Kontribusi utama: K-A + K-B.** Pendukung: K-C, K-D.

---

## 2. Yang **bukan** kebaruan **[USULAN]**

| Tidak diklaim | Alasan |
|---|---|
| Metode MCDM baru | SAW sudah mapan |
| "Pertama memakai SAW" | Sudah umum di network selection |
| "Pertama memakai bobot objektif pada SAW" | Entropy-SAW sudah ada (5G, 2021) |
| Istilah/konsep ALQI | Prior art paten US 9,674,720 B2 (2017) |
| Sistem kontroler penuh | Lingkup dipersempit ke modul penilaian |
| Kontrol loop formal | Tidak dibuktikan secara matematis |
| Generalisasi > 2 ISP / multi-vendor | Di luar lingkup |
| QoE / kepuasan pengguna | Yang diukur QoS |

---

## 3. Batas Klaim **[USULAN]**

- Konteks: **dual-ISP FO–LEO**, satu lokasi skala kecil (RT/RW Net).
- Data: **deret metrik 1 detik** dari kolektor *read-only*; validasi internal di
  staging, eksternal di lapangan (jika memungkinkan).
- Bobot: **hibrida** dengan prior ahli dari literatur/pilot; **bukan** pembelajaran
  otomatis (*self-tuning*).
- Istilah ALQI: hanya sebagai prior art yang dibedakan.
- Klaim "belum ada" diganti **"belum dievaluasi pada konteks X dengan metrik Y"**.

---

## 4. Dua Varian Lingkup **[USULAN]**

### Varian Sempit (paling aman untuk S2)
Fokus **hanya modul penilaian kualitas link** ($Q_i(t)$): normalisasi + pembobotan
adaptif + stabilitas temporal. Tidak menyentuh alokasi PCC.
- **Kelebihan:** waktu terjamin; eksperimen dapat sepenuhnya offline/staging.
- **Kekurangan:** melepas novelty kebijakan alokasi.

### Varian Tengah (rekomendasi bila ingin lebih kuat)
Modul penilaian **+** kebijakan alokasi sadar-stok (menambah RQ tentang stok koneksi
lama). Novelty utama tetap pada penilaian, dengan alokasi sebagai bukti penerapan.
- **Kelebihan:** kontribusi lebih berisi; ada jalur ke publikasi.
- **Kekurangan:** cakupan lebih luas → risiko jadwal.

---

## 5. Kalimat Novelty (siap tulis di Bab I) **[USULAN]**

> *"Berbeda dari studi PCC yang menetapkan rasio secara statis dan dari studi
> normalisasi MCDM yang diuji pada dataset statis, penelitian ini **memodifikasi
> fungsi penilaian kualitas link** pada jaringan dual-WAN FO–LEO menjadi skor
> komposit berbasis SAW dengan **normalisasi berbatas acuan tetap** dan **pembobotan
> hibrida adaptif**, lalu **membuktikan secara komparatif** teknik mana yang
> menghasilkan indeks paling akurat sekaligus paling stabil secara temporal."*

---

## 6. Peta Kontribusi

| Kode | Kontribusi | Jenis | Gap | Bukti |
|---|---|---|---|---|
| K-A | Studi komparatif normalisasi × pembobotan | Empiris | G-N1 | Matriks kinerja, effect size |
| K-B | Pembobotan hibrida adaptif + gerbang | Metode | G-N2 | Kurva trade-off $\gamma$ |
| K-C | Normalisasi berbatas acuan tetap | Desain | G-N1 | Uji rank reversal |
| K-D | Dekomposisi kontribusi | Metode | G-W2 | Ablasi 2×2 |
