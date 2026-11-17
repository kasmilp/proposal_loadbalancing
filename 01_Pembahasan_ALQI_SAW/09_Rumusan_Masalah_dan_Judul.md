# 09 — Rumusan Masalah dan Judul

**Status:** Draf kerja
**Fungsi:** Menggantikan rumusan masalah naskah lama dengan rumusan bergaya
**"memodifikasi"** agar layak sebagai penelitian S2.

---

## 1. Rumusan Masalah Lama dan Kelemahannya **[FAKTA + ANALISIS]**

**RQ lama [FAKTA]:**
> *"Bagaimana merancang dan mengimplementasikan ALQI berbasis SAW dengan histeresis
> asimetris untuk mengevaluasi kualitas jalur WAN heterogen FO dan LEO Starlink
> berdasarkan delay, jitter, packet loss, dan throughput, kemudian mengintegrasikan
> hasil evaluasi tersebut ke dalam PCC dinamis pada MikroTik melalui server Controller
> eksternal untuk meningkatkan QoS agregat dan mengurangi frekuensi flapping
> dibandingkan PCC statis konvensional?"*

| # | Kelemahan | Konsekuensi |
|---|---|---|
| 1 | Kata kerja **"merancang dan mengimplementasikan"** | Bahasa rekayasa, bukan kontribusi pengetahuan |
| 2 | Tiga kata kerja sekaligus (mengevaluasi + mengintegrasikan + meningkatkan) | Tidak dapat dijawab oleh satu penelitian dengan satu metode |
| 3 | Nama **ALQI** (prior art paten) | Dianggap klaim istilah |
| 4 | "Meningkatkan QoS agregat" tanpa satuan/pembanding | Tidak falsifiabel |
| 5 | Pembanding hanya "PCC statis" | Tidak memisahkan kontribusi komponen |
| 6 | Cakupan controller penuh | Terlalu luas untuk S2 |

**Prinsip perbaikan:** templat *"Berbeda dari …, penelitian ini memodifikasi …,
sehingga …"* dengan lima unsur: **(a) fungsi yang dimodifikasi, (b) pembanding,
(c) mekanisme, (d) luaran terukur, (e) satuan analisis.**

---

## 2. Rumusan Masalah Baru **[USULAN]**

### RQ Payung
> **Bagaimana memodifikasi fungsi kontrol alokasi koneksi pada PCC statis — dari
> ambang tunggal dan rasio tetap menjadi penilaian kualitas link multi-kriteria (SAW)
> yang digerbangi histeresis asimetris — pada jaringan dual-WAN heterogen FO–LEO,
> sehingga QoS agregat meningkat dan frekuensi flapping menurun dibandingkan PCC
> statis dan varian tanpa gerbang?**

### Sub-RQ

| Kode | Sub-RQ | Pembanding | Luaran terukur |
|---|---|---|---|
| **RQ1 — Persepsi** | Bagaimana memodifikasi penilaian kualitas link dari metrik mentah menjadi skor komposit ternormalisasi (SAW) sehingga peringkat link **komparabel antar-waktu** dan tahan derau? | Normalisasi min–max vs batas acuan tetap | $Q_i(t)$ + indeks stabilitas (std, *rank reversal*) |
| **RQ2 — Deteksi** | Bagaimana memodifikasi deteksi degradasi dari ambang tunggal menjadi **histeresis dua ambang + dwell** yang diturunkan dari durasi transien terukur, sehingga flapping turun **tanpa** memperlambat pemulihan? | Ambang tunggal; histeresis simetris | Flapping/jam, *recovery latency*, kurva trade-off |
| **RQ3 — Alokasi** | Bagaimana memodifikasi kebijakan alokasi dari rasio tetap menjadi pemetaan skor kontinu → proporsi PCC diskret dengan batas min–maks, sehingga alokasi mengikuti kondisi link tanpa *overload/starvation*? | Rasio statis | Distribusi rasio, langkah kuantisasi, ELS |
| **RQ4 — Bukti** | Seberapa besar modifikasi pada RQ1–RQ3 menurunkan flapping dan menaikkan QoS agregat, serta **komponen mana** yang menyumbang perubahan itu? | PCC statis (A), tanpa histeresis (B), simetris (D) | Effect size + 95% CI per episode/jam |

### Hipotesis

- **H1 (dari RQ2):** histeresis asimetris menurunkan laju flapping dibandingkan tanpa
  histeresis, **tanpa** melampaui batas *recovery latency*.
- **H2 (dari RQ3–RQ4):** alokasi berbasis $Q_i(t)$ menghasilkan QoS agregat lebih baik
  daripada rasio statis **pada episode degradasi**.
- **H3 (dari RQ4):** kontribusi histeresis dapat dipisahkan dari kontribusi skor
  multi-kriteria (ablasi), sehingga perbaikan **dapat diatribusikan**.

### Novelty Statement
> *"Berbeda dari studi PCC yang menetapkan rasio secara statis dan studi histeresis
> yang tidak diturunkan dari dinamika link, penelitian ini **memodifikasi fungsi
> kontrol PCC** menjadi penilaian kualitas multi-kriteria dengan gerbang histeresis
> asimetris, dan **membuktikan lewat ablasi** komponen mana yang menurunkan flapping
> dan menaikkan QoS agregat pada jaringan FO–LEO."*

---

## 3. Varian Lingkup

### Varian A — mempertahankan substansi lama (luas)
Gunakan §2 apa adanya.

### Varian B — sempit, hanya modul skoring (paling aman)
> *"Bagaimana memodifikasi fungsi **penilaian kualitas link** pada PCC statis — dari
> metrik tunggal menjadi skor komposit berbasis SAW dengan normalisasi berbatas acuan
> tetap — sehingga penilaian **stabil secara temporal dan komparabel** pada link
> heterogen FO–LEO, dibandingkan normalisasi min–max dan pembobotan statis?"*

Sub-RQ: (1) pilihan normalisasi; (2) skema bobot statis vs objektif vs hibrida;
(3) stabilitas temporal indeks; (4) bukti komparatif.

### Varian C — tengah (rekomendasi bila ingin lebih kuat)
RQ payung §2 **+ RQ5 stok koneksi**:
> *"Bagaimana memodifikasi kebijakan alokasi agar mempertimbangkan **stok koneksi
> lama** yang tetap menempati link yang memburuk, sehingga **beban efektif** menurun
> lebih cepat tanpa menaikkan RST?"*

---

## 4. Uji Kelayakan RQ

| Uji | Pertanyaan | Status §2 |
|---|---|---|
| Falsifiabilitas | Hasil apa yang membuktikan RQ salah? | Terpenuhi |
| Keterukuran | Semua variabel punya satuan & instrumen? | Terpenuhi |
| Keterbandingan | Ada pembanding eksplisit? | Terpenuhi (A, B, D) |
| Atribusi | Dapat dipisahkan per komponen? | Terpenuhi (H3) |
| Batas klaim | Lingkup dibatasi? | Perlu dinyatakan eksplisit |
| Kelayakan waktu | Selesai 4–6 bulan? | Bergantung varian |

**Hindari:** "merancang", "menciptakan", "membangun dari nol".
**Pakai:** "memodifikasi", "mengubah cara controller …", "menurunkan", "membuktikan".

---

## 5. Rekomendasi Judul **[USULAN]**

1. **(Komparatif — paling mudah dipertahankan)**
   *Perbandingan Teknik Normalisasi dan Pembobotan pada Simple Additive Weighting
   untuk Indeks Kualitas Link Multi-Kriteria pada Jaringan Dual-WAN Fiber Optik–LEO*

2. **(Orientasi pengembangan)**
   *Pengembangan Indeks Kualitas Link Adaptif Berbasis Simple Additive Weighting
   dengan Pembaruan Bobot Objektif untuk Penilaian Jalur WAN Heterogen FO–LEO*

3. **(Paling sempit, risiko rendah)**
   *Evaluasi Stabilitas Temporal Indeks Kualitas Link Berbasis SAW terhadap Pilihan
   Normalisasi dan Bobot pada Link dengan Transien Periodik*

**Catatan:** pada ketiga judul, **jangan** memakai "ALQI" sebagai klaim; sebut sebagai
$a_i(t)$/skor kualitas link. MikroTik disebut sebagai platform penerapan, bukan objek.
