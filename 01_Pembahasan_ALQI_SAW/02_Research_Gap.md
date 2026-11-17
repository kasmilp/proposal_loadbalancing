# 02 — Research Gap

**Status:** Draf kerja
**Fungsi:** Menetapkan *apa yang belum terjawab* pada arah ALQI–SAW, dengan bukti
literatur — bukan klaim "belum ada penelitian".
**Aturan bukti:** klaim "belum ada" hanya boleh setelah log pencarian dijalankan
(`11_Rencana_Verifikasi_Lanjutan.md`).

---

## 1. Cara Membaca Gap

Gap = **jarak antara kebutuhan terbukti dan kemampuan pendekatan yang ada**, ditulis
dengan pola:

> **Meskipun** [yang sudah diketahui], **belum ada** [yang belum],
> **sehingga** [konsekuensi yang dapat diukur].

Jenis gap: **G-E** *evidence*, **G-M** *method*, **G-I** *integration*, **G-C**
*context*. Prioritas diberikan pada **G-M dan G-E** (G-I saja paling rentan dinilai
"hanya kombinasi").

---

## 2. Bukti Pencarian yang Sudah Ada **[FAKTA]**

Dari arsip `01_Arsip_SPA-HSM_Tahap_01-12/09_Verifikasi_dan_Pencarian/01_Log_Pencarian_Gap.md`
(OpenAlex, judul+abstrak, 2015–2026, 12 Nov 2026):

| Kode | Query | Hits | Catatan |
|---|---|---:|---|
| S5f | `(MCDM OR SAW) AND "network selection"` | 82 | Dominan *seleksi* jaringan, bukan skor kualitas link untuk alokasi WAN |
| S1g | `"per connection classifier" AND (hysteresis OR dwell OR "quality score")` | **0** | Irisan kosong |
| S1f | `"per connection classifier" AND (adaptive OR dynamic OR quality)` | 34 | Dominan implementasi PCC statis |

**[FAKTA tambahan — pencarian 17 Nov 2026]** Melalui OpenAlex ditemukan kandidat yang
belum masuk korpus:
- *Multi-criteria handover management using entropy-based SAW method for SDN-based 5G
  small cells* — Wireless Networks, 2021, `10.1007/s11276-021-02625-y`
- *Context-oriented performance evaluation of network selection algorithms in 5G
  heterogeneous networks* — JNCA, 2022, `10.1016/j.jnca.2022.103358`
- *A Modified CRITIC Method…* — Symmetry, 2021, `10.3390/sym13060973`
- *Determination of Objective Weights… (MEREC)* — Symmetry, 2021, `10.3390/sym13040525`
- *A Comprehensive Review of the Novel Weighting Methods for MCDM* — Information, 2023,
  `10.3390/info14050285`

Status: **kandidat, metadata & teks penuh belum diverifikasi.**

---

## 3. Peta Gap

### G-N1 — Teknik normalisasi SAW belum diuji pada deret metrik link real-time

**Yang sudah diketahui.** Teknik normalisasi memengaruhi peringkat akhir SAW secara
signifikan (Vafaei et al., 2021 **[FAKTA, ada di korpus]**).

**Yang belum ada.** Pengujian Vafaei dilakukan pada **dataset MCDM statis**. Belum ada
studi yang menguji **stabilitas temporal** teknik normalisasi ketika metrik datang
sebagai **deret waktu** yang bising dan mengandung outlier (mis. lonjakan delay saat
handover LEO).

**Konsekuensi.** Normalisasi *min–max* dengan batas yang bergeser tiap siklus membuat
skor **tidak komparabel antar-waktu**; keputusan kontrol menjadi tidak konsisten.
Tanpa pengujian, desainer sistem tidak punya dasar memilih teknik normalisasi.

**Jenis:** G-M utama. **Tingkat keyakinan:** tinggi.

---

### G-N2 — Pembobotan objektif/adaptif belum dievaluasi pada penilaian kualitas link WAN FO–LEO skala kecil

**Yang sudah diketahui.** Pembobotan objektif (entropy, CRITIC, MEREC) mapan di MCDM
(`10.3390/sym13060973`; `10.3390/sym13040525` **[FAKTA kandidat]**). *Entropy-based
SAW* telah dipakai untuk handover 5G (`10.1007/s11276-021-02625-y` **[FAKTA
kandidat]**).

**Yang belum ada.** Belum ditemukan studi yang (i) menerapkan pembobotan objektif pada
**penilaian kualitas link WAN heterogen FO–LEO** dalam konteks **router kelas
SOHO/PCC**, dan (ii) mengukur **hubungan akurasi ↔ stabilitas** akibat bobot yang
diperbarui berkala.

**Konsekuensi.** Praktisi memakai bobot statis/ahli tanpa dasar empiris apakah bobot
objektif benar-benar menambah akurasi, atau justru menambah *chattering* indeks.

**Jenis:** G-M utama. **Tingkat keyakinan:** sedang–tinggi (perlu verifikasi lintas
basis data).

---

### G-W1 — Stabilitas indeks komposit belum diuji terhadap transien periodik LEO

**Yang sudah diketahui.** Starlink memiliki siklus rekonfigurasi **≈15 detik** yang
menurunkan delay/throughput secara periodik (Garcia et al., 2025; Hammer et al., 2024;
Mohan et al., 2024 **[FAKTA, ada di korpus]**). Histeresis dua ambang mencegah
osilasi keputusan (Tournaire et al., 2023 **[FAKTA]**).

**Yang belum ada.** Belum ada studi yang mengukur bagaimana **stabilitas indeks
komposit** berubah ketika bobot/normalisasi diperbarui berkala pada link dengan
transien periodik secepat itu.

**Konsekuensi.** Indeks dapat "berkedip" (*chattering*) tiap 15 detik; keputusan
alokasi jadi flapping. Tanpa pengukuran, klaim "indeks stabil" tak dapat dibuktikan.

**Jenis:** G-E/G-M. **Tingkat keyakinan:** sedang–tinggi.

---

### G-W2 — Dekomposisi kontribusi normalisasi vs pembobotan belum dilakukan

**Yang sudah diketahui.** Normalisasi dan pembobotan keduanya memengaruhi hasil SAW.

**Yang belum ada.** Belum ada studi yang **memisahkan kontribusi** masing-masing
(normalisasi saja, bobot saja, interaksi keduanya) terhadap kinerja indeks pada
konteks jaringan.

**Konsekuensi.** Klaim "sistem kami lebih baik" tidak dapat diatribusikan ke komponen
tertentu; hasil sulit direplikasi.

**Jenis:** G-M. **Tingkat keyakinan:** sedang–tinggi.

---

## 4. Bukan Gap Penelitian Ini **[USULAN]**

Agar tidak membangun *strawman*:

| Klaim yang harus dihindari | Alasan |
|---|---|
| "Belum ada yang memakai SAW untuk jaringan" | Salah; MCDM sudah lazim |
| "Belum ada yang memakai bobot objektif pada SAW" | Salah; entropy-SAW sudah ada (5G) |
| "Belum ada yang meneliti kualitas link" | Salah; literatur QoS sangat banyak |
| "ALQI adalah istilah/konsep baru" | Salah; ada paten 2017 (lihat `01_...`) |
| "Kami menggantikan SD-WAN" | Berlebihan; lingkupnya kecil-menengah |

---

## 5. Ringkasan Prioritas Gap

| Gap | Jenis | Kekuatan sebagai novelty | Peran |
|---|---|---|---|
| G-N1: normalisasi pada data streaming | Method | **Tinggi** | Kontribusi utama |
| G-N2: pembobotan objektif/hibrida pada FO–LEO | Method | **Tinggi** | Kontribusi utama |
| G-W1: stabilitas indeks vs transien LEO | Evidence/Method | Sedang–tinggi | Pendukung |
| G-W2: dekomposisi normalisasi × bobot | Method | Sedang–tinggi | Pendukung |

**Keputusan [USULAN]:** kebaruan utama bertumpu pada **G-N1 + G-N2**; G-W1 dan G-W2
menjadi pendukung yang memperkuat atribusi bukti.

---

## 6. Klaim Gap (Satu Paragraf)

> Meskipun teknik normalisasi dan pembobotan pada SAW telah terbukti memengaruhi hasil
> peringkat dan telah diterapkan pada seleksi jaringan seluler, pengujiannya masih
> bertumpu pada dataset statis atau domain seluler 5G — belum pada **deret metrik
> kualitas link real-time yang bising** pada **jaringan dual-WAN heterogen FO–LEO**
> dengan transien periodik. Akibatnya, belum diketahui teknik normalisasi dan skema
> pembobotan mana yang menghasilkan indeks yang **akurat sekaligus stabil secara
> temporal**, dan seberapa besar masing-masing komponen menyumbang kinerja tersebut.
