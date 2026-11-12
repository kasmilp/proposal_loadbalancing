# BAB I
# PENDAHULUAN

**Status:** Draf kerja — belum naskah final
**Judul kerja:** SPA-HSM: Kendali Proporsi Aliran Adaptif dan Sadar-Sesi pada
WAN Heterogen Fiber Optic–LEO
**Subjudul:** Studi Kasus Jaringan RT/RW Net Dual-ISP

---

## 1.1 Latar Belakang

Transformasi digital membuat ketersediaan koneksi dan kualitas layanan menjadi
dua syarat yang harus dipenuhi bersamaan. Jaringan yang hanya mengandalkan satu
penyedia layanan internet memiliki titik kegagalan tunggal; karena itu, arsitektur
multi-ISP lazim dipakai untuk meningkatkan ketersediaan dan memanfaatkan lebar
pita secara lebih baik (Ali et al., 2025). Ketika jalur yang digabungkan memiliki
karakteristik fisik berbeda—misalnya serat optik terestrial dan satelit orbit
rendah—pengelolaan agregasi menjadi lebih kompleks karena setiap jalur memiliki
pola degradasi yang tidak sama (Chen et al., 2025).

Jalur *Fiber Optic* (FO) secara arsitektural unggul dalam latensi rendah,
*throughput* tinggi, dan *packet loss* kecil karena mediumnya terlindung dari
gangguan atmosferik. Namun, kualitas FO dalam praktik operasional tidak identik
dengan kapasitas nominal. Kepadatan pelanggan dan gangguan pada jaringan akses
dapat membuat *throughput* aktual berada di bawah kapasitas nominal, terutama
pada jam sibuk (Safitri et al., 2016). Gejala ini bersifat operasional, bukan
keterbatasan fisik medium, sehingga kualitas FO perlu dievaluasi berkala dan tidak
dapat diasumsikan konstan.

Sebaliknya, satelit *Low Earth Orbit* (LEO) seperti Starlink menyediakan
konektivitas di wilayah yang sulit dijangkau infrastruktur terestrial, tetapi
kinerjanya bersifat stokastik. Pengukuran dari sisi pengguna menunjukkan
variabilitas *throughput* dan latensi yang jauh lebih besar daripada jaringan
terestrial, disertai kejadian *outage* yang relatif sering (Ma et al., 2023;
Mohan et al., 2024). Pada wilayah tropis, *rain fade* memperburuk kondisi;
curah hujan menjadi prediktor kuat penurunan *throughput* (Boeckenholt et al.,
2024; Ullah et al., 2025). Selain degradasi lambat akibat cuaca, terdapat transien
cepat akibat rekonfigurasi dan *handover*; karakterisasi *one-way delay*
melaporkan pola periodik sekitar 15 detik yang paling terdampak pada arah
*uplink* (Garcia et al., 2025), dan pola serupa teramati pada
*throughput* dari sisi *edge router* (Hammer et al., 2024).

Dengan demikian, jalur LEO mengandung dua lapis ketidakstabilan: degradasi lambat
berskala menit akibat cuaca dan transien cepat berskala detik akibat rekonfigurasi.
Perbedaan skala waktu ini penting karena mekanisme kendali yang terlalu reaktif
akan bereaksi terhadap transien, sedangkan mekanisme yang terlalu lambat akan
melewatkan degradasi nyata.

Untuk mendistribusikan beban pada jaringan multi-ISP, *Per Connection Classifier*
(PCC) pada RouterOS MikroTik banyak dipakai. PCC mengelompokkan trafik berdasarkan
atribut koneksi sehingga seluruh paket dalam satu sesi konsisten dialirkan melalui
*gateway* yang sama; sifat ini mengurangi risiko *packet reordering* yang merusak
kinerja TCP (Kumar & Golash, 2009; MikroTik, n.d.). Pada konteks jaringan lokal
dan dual-ISP di Indonesia, penerapan PCC dilaporkan meningkatkan *throughput* dan
menurunkan *delay* serta *jitter* (Amalia et al., 2022; Arfianita et al., 2024),
lebih stabil daripada ECMP dan Nth pada trafik *stateful* (Nugroho et al., 2023),
serta mengurangi dampak gangguan salah satu ISP ketika dipadukan dengan
*failover* (Putra & Anton, 2024; Mirsal & Agtriadi, 2026; Bustomi & Tahir, 2026).

Meskipun demikian, studi-studi tersebut menetapkan rasio pembagian secara
**statis** pada tahap konfigurasi. Rasio tidak dievaluasi ulang terhadap kondisi
link secara *real-time*. Ketika salah satu ISP terdegradasi—misalnya Starlink
mengalami transien atau FO mengalami penurunan kecepatan pada jam sibuk—router
tetap menyalurkan proporsi trafik sesuai rasio semula. Alokasi yang tidak
sadar-kondisi ini dapat menurunkan kualitas layanan agregat dan mengurangi
*throughput* efektif.

Pendekatan adaptif yang lebih baru, seperti *hub* konektivitas berbasis *Artificial
Neural Network* (ANN) dan *load balancing* cloud berbasis metaheuristik, menunjukkan
manfaat alokasi sadar-kondisi (Ali et al., 2025; Komathi et al., 2024; Lilhore et
al., 2025). Namun, pendekatan tersebut umumnya memerlukan pelatihan model dan
sumber daya komputasi yang lebih besar daripada aturan ambang sederhana, sehingga
kurang sesuai untuk perangkat kelas SOHO; selain itu, pendekatan tersebut tidak
secara eksplisit menjaga konsistensi sesi TCP. Di sisi lain, literatur MCDM menyediakan kerangka
skor multi-kriteria (Wang & Kuo, 2013; Vafaei et al., 2021), literatur kontrol
menyediakan histeresis untuk mencegah osilasi (Tournaire et al., 2023; Alhabo et
al., 2017), dan literatur Starlink menyediakan karakterisasi dinamika link (Ma et
al., 2023; Garcia et al., 2025). Namun, keempat elemen tersebut belum disatukan
dalam satu mekanisme yang mengendalikan proporsi PCC, menjaga sesi, dan dapat
diuji kontribusinya secara terpisah.

Tiga masalah muncul ketika pembaruan rasio dilakukan secara naif. **Pertama**,
metrik QoS mengandung derau dan transien; memperbarui rasio pada setiap siklus
*polling* dapat memicu *flapping*, yaitu perubahan aturan yang berbalik arah
secara berulang. **Kedua**, perubahan aturan PCC berpotensi memengaruhi sesi yang
sedang berjalan; tanpa mekanisme preservasi, koneksi TCP dapat mengalami
*reordering*, retransmisi, bahkan *reset*. **Ketiga**, parameter histeresis pada
praktik load balancing umumnya dipilih secara *ad hoc*, tidak diturunkan dari
durasi transien link, dan dampaknya terhadap sesi tidak diukur.

Berdasarkan uraian tersebut, penelitian ini mengusulkan *Session-Preserving
Asymmetric Hysteresis State Machine* (SPA-HSM), yaitu arsitektur kendali
lingkaran tertutup tiga lapis. Lapis *Algorithm Core* menghaluskan metrik dengan
*Exponentially Weighted Moving Average* (EWMA), menghitung skor kualitas link
dengan *Simple Additive Weighting* (SAW), menentukan status link melalui
histeresis asimetris, dan memetakan status/skor menjadi proporsi PCC diskret.
Lapis *Abstract Allocation Interface* menerjemahkan keputusan menjadi direktif
abstrak, termasuk `AFFINITY_LOCK` untuk menjaga sesi berjalan. Lapis *Platform
Adapter* menerjemahkan direktif menjadi aturan *mangle/routing* PCC pada RouterOS
MikroTik melalui REST API, dengan pembaruan yang dibatasi pada
`connection-state=new`.

Kebaruan penelitian ini bukan pada penemuan metode MCDM, EWMA, atau histeresis
yang baru. Kebaruannya terletak pada tiga hal: (1) **aturan *dwell* sadar-transien**
yang menghubungkan interval sampling, durasi transien LEO, dan jumlah sampel
berturut-turut; (2) **formalisasi pemetaan skor kualitas kontinu menjadi proporsi
PCC diskret** dengan jaminan jumlah bucket dan batas alokasi; serta (3) **metrik
*Session-Impact-Weighted Goodput* (SIWG)** dan bukti ablasi yang memisahkan
kontribusi histeresis dan preservasi sesi. Dengan posisi ini, penelitian tidak
mengklaim menggantikan metode yang ada, tetapi menawarkan kerangka rekayasa yang
dapat direplikasi dan dievaluasi.

Ruang lingkup penelitian dibatasi pada topologi dual-ISP FO–LEO, Starlink sebagai
kasus acuan *upper bound* untuk transien, bobot SAW statis yang dikalibrasi di
awal, dan MikroTik sebagai *platform adapter*. Hasil penelitian diharapkan menjadi
pedoman parameter dan bukti empiris bagi pengelola jaringan skala kecil-menengah,
bukan solusi *enterprise* yang menggantikan SD-WAN komersial.

---

## 1.2 Rumusan Masalah

Berdasarkan latar belakang tersebut, pertanyaan penelitian payung adalah:

> Sejauh mana SPA-HSM—yang memadukan skor kualitas multi-kriteria, penghalusan
> EWMA, histeresis asimetris sadar-transien, dan `AFFINITY_LOCK`—mampu
> mengendalikan trade-off antara stabilitas keputusan dan kontinuitas sesi pada
> WAN dual-ISP FO–LEO, dan bagaimana kontribusi masing-masing komponen serta
> parameter *dwell* membentuk *frontier* trade-off tersebut?

Pertanyaan payung tersebut dijabarkan menjadi lima sub-pertanyaan:

1. Bagaimana merumuskan skor kualitas $Q_i(t)$ dari metrik QoS dengan normalisasi
   berbatas tetap dan bobot statis, lalu memetakannya menjadi proporsi PCC diskret
   yang memenuhi jumlah bucket dan batas alokasi?
2. Bagaimana merancang aturan *dwell* histeresis asimetris yang diturunkan dari
   durasi transien LEO, dan bagaimana aturan itu menggeser trade-off antara
   *flapping rate* dan *recovery latency*?
3. Seberapa besar `AFFINITY_LOCK` menurunkan gangguan sesi TCP—diukur sebagai RST
   *rate* dan proporsi aliran terganggu—dan bagaimana interaksinya dengan bentuk
   histeresis?
4. Bagaimana kinerja gabungan SPA-HSM diukur dengan SIWG, dan seberapa besar
   kontribusi tiap komponen berdasarkan ablasi pada konteks FO–LEO?
5. Apakah *Algorithm Core* memenuhi kontrak antarmuka dan menghasilkan keputusan
   identik ketika dijalankan pada dua adapter berbeda?

---

## 1.3 Tujuan Penelitian

Tujuan umum penelitian ini adalah mengembangkan dan mengevaluasi SPA-HSM sebagai
mekanisme kendali proporsi PCC yang menjaga stabilitas keputusan sekaligus
kontinuitas sesi pada WAN heterogen FO–LEO, serta menghasilkan panduan parameter
yang dapat dipakai praktisi.

Tujuan khusus:

1. merumuskan $Q_i(t)$ berbasis EWMA–SAW dengan normalisasi berbatas tetap, serta
   pemetaan formal dari skor ke bucket PCC;
2. merancang aturan *dwell* yang diturunkan dari durasi transien LEO dan
   menganalisis pengaruhnya terhadap *flapping* dan *recovery latency*;
3. mengimplementasikan `AFFINITY_LOCK` dan mengukur dampaknya terhadap RST *rate*
   serta proporsi aliran terganggu;
4. mengevaluasi kontribusi histeresis dan affinity secara terpisah dan bersama
   melalui ablasi, menggunakan SIWG sebagai ukuran gabungan;
5. menguji kontrak *Abstract Allocation Interface* dan portabilitas *Algorithm
   Core* melalui *mock adapter* dan adapter kedua.

---

## 1.4 Hipotesis Penelitian

Hipotesis nol ($H_0$) untuk setiap hipotesis menyatakan tidak terdapat perbedaan
yang signifikan antara kondisi yang dibandingkan. Hipotesis kerja dirumuskan
sebagai berikut.

**H1 — Histeresis menekan flapping.** SPA-HSM dengan histeresis (simetris atau
asimetris) menurunkan *flapping rate* minimal 50% dibanding varian tanpa
histeresis, tanpa membuat *recovery latency* p95 melebihi 90 detik pada
$T_s = 1$ detik.

**H2 — Asimetri waktu memperbaiki trade-off.** Histeresis asimetris menurunkan
*flapping rate* minimal 30% dibanding histeresis simetris pada ambang yang sama,
dengan kenaikan *recovery latency* p95 tidak lebih dari 30 detik dan keduanya
tetap ≤ 90 detik.

**H3a — Affinity lock menjaga integritas sesi.** `AFFINITY_LOCK` menurunkan
$\text{RST}_{flow}$ dibanding varian tanpa affinity, dan tidak inferior terhadap
baseline PCC statis dengan margin 0,5 poin persentase. Nilai absolut
$\text{RST}_{flow}\%$ di bawah 1% dilaporkan sebagai kriteria sekunder.

**H3b — Kinerja agregat meningkat saat degradasi.** Pada episode degradasi,
SPA-HSM meningkatkan *goodput* minimal 10% dan menurunkan latensi p95 minimal 15%
dibanding PCC statis, serta tidak inferior terhadap baseline praktisi.

**H4 — SIWG SPA-HSM lebih tinggi.** SIWG SPA-HSM lebih tinggi minimal 15%
dibanding baseline terbaik, dengan interval kepercayaan yang konsisten pada
analisis sensitivitas $\lambda$.

**H5 — Portabilitas inti algoritma.** *Algorithm Core* lulus seluruh uji
konformitas kontrak dan menghasilkan urutan keputusan yang identik pada dua
adapter untuk dataset *replay* yang sama.

---

## 1.5 Manfaat Penelitian

### 1.5.1 Manfaat teoretis

Penelitian ini diharapkan memperkaya literatur *load balancing* adaptif dengan
menyatukan empat elemen yang selama ini dikaji terpisah: skor kualitas
multi-kriteria, penghalusan deret waktu, histeresis asimetris, dan preservasi
sesi. Kontribusi teoretis utamanya adalah rumusan trade-off stabilitas–kontinuitas
sebagai masalah kendali, serta aturan *dwell* yang menghubungkan parameter kendali
dengan karakteristik transien link.

### 1.5.2 Manfaat praktis

1. Bagi pengelola RT/RW Net, penelitian ini menawarkan mekanisme penyesuaian
   proporsi beban yang berjalan otomatis dan dapat dikembalikan ke konfigurasi
   statis ketika controller gagal.
2. Bagi organisasi di wilayah dengan keterbatasan infrastruktur terestrial,
   kombinasi FO dan satelit LEO dapat dikelola tanpa ketergantungan pada solusi
   *proprietary*.
3. Bagi peneliti dan praktisi, arsitektur tiga lapis dan kontrak antarmuka
   menyediakan kerangka yang dapat direplikasi pada platform lain.
4. Bagi industri, hasil penelitian berpotensi menjadi masukan untuk pengembangan
   fitur *adaptive WAN* pada perangkat kelas SOHO.

---

## 1.6 Batasan Masalah

Agar penelitian tetap fokus dan hasilnya terukur, ditetapkan batasan berikut.

1. Sistem diuji pada topologi dual-ISP (FO IndiHome dan LEO Starlink) dan tidak
   divalidasi pada topologi dengan lebih dari dua ISP.
2. Starlink dipakai sebagai kasus acuan *upper bound* untuk transien; generalisasi
   ke semua jenis WAN non-stasioner tidak diklaim.
3. Bobot kriteria SAW ditetapkan statis berdasarkan kalibrasi awal, bukan hasil
   pembelajaran otomatis. Analisis sensitivitas dilakukan, tetapi penyesuaian
   bobot *real-time* berada di luar cakupan.
4. MikroTik/RouterOS berperan sebagai *platform adapter* dan *testbed eksekutor*,
   bukan objek algoritma. Penelitian hanya memvalidasi satu adapter nyata dan
   menggunakan *mock adapter* untuk uji kontrak; generalisasi multi-vendor tidak
   diklaim.
5. Implementasi dan pengujian dilakukan pada satu lokasi RT/RW Net; hasil belum
   tentu tergeneralisasi pada skala *enterprise*.
6. Penelitian berfokus pada mekanisme penyesuaian proporsi PCC dan tidak membahas
   aspek keamanan komunikasi antara controller dan router secara mendalam.
7. Alokasi rasio berbasis kualitas $Q_i(t)$ dan *headroom* sederhana; optimasi
   kapasitas formal dan alokasi multi-*objective* yang lebih kompleks berada di
   luar cakupan.
8. Penelitian mengukur QoS, bukan QoE; persepsi pengguna dan aplikasi spesifik
   tidak diukur secara langsung.
9. Stabilitas sistem dievaluasi secara empiris melalui ablasi dan analisis
   statistik, bukan melalui pembuktian formal kestabilan *control loop*.
10. Desain ablasi adalah faktorial 2×2 (simetris/asimetris × affinity off/on)
    ditambah pembanding statis, *dynamic naive*, dan baseline praktisi. Kombinasi
    "tanpa histeresis + affinity on" tidak diuji, sehingga interaksi tersebut
    tidak diklaim.
11. Hasil tidak dimaksudkan untuk menggantikan solusi SD-WAN komersial skala
    *enterprise*; kontribusinya adalah kerangka adaptif yang ringan, terbuka, dan
    dapat direplikasi pada skala kecil-menengah.

---

## 1.7 Definisi Istilah

| Istilah | Definisi |
|---|---|
| **SPA-HSM** | *Session-Preserving Asymmetric Hysteresis State Machine*, arsitektur kendali tiga lapis yang diusulkan |
| **$Q_i(t)$** | Skor kualitas link $i$ pada waktu $t$, hasil EWMA–SAW, rentang 0–1 |
| **Episode degradasi** | Periode ketika $Q_i < \theta_{low}$ selama $k_{down}$ sampel dan berakhir saat $Q_i > \theta_{high}$ selama $k_{up}$ sampel |
| **Flap** | Perubahan aturan PCC efektif yang diikuti perubahan arah sebaliknya dalam jendela 5 menit |
| **Flapping rate** | Jumlah flap per jam pengamatan |
| **Effective rule change** | Perubahan jumlah bucket PCC pada minimal satu link |
| **Recovery latency** | Waktu dari awal episode sampai state kembali `STABLE` |
| **RST flow** | Proporsi aliran TCP yang menerima minimal satu RST; dilaporkan sebagai persentase |
| **SIWG** | *Session-Impact-Weighted Goodput*, goodput efektif yang didiskon oleh proporsi aliran terganggu |
| **`AFFINITY_LOCK`** | Direktif yang menahan sesi berjalan pada jalur awalnya; hanya koneksi baru mengikuti rasio baru |
| **Baseline G** | PCC statis 50:50 dengan `netwatch`/health-check failover |
