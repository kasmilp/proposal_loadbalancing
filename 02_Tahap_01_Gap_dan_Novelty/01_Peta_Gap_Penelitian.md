# Tahap 1 — Peta Gap Penelitian

**Dokumen:** `01_Peta_Gap_Penelitian.md`
**Status:** Draf kerja Tahap 1
**Fungsi:** Menetapkan *apa yang belum terjawab* sebelum menulis Bab I.
**Aturan:** Setiap gap harus punya bukti literatur, bukan hanya klaim "belum ada penelitian".

---

## 1. Cara Membaca Dokumen Ini

Gap penelitian bukan "topik yang belum pernah diteliti". Gap adalah **jarak antara
kebutuhan yang terbukti dan kemampuan pendekatan yang ada**. Karena itu setiap gap
di bawah ini ditulis dengan pola:

> **Meskipun** [apa yang sudah diketahui], **belum ada** [apa yang belum],
> **sehingga** [konsekuensi yang dapat diobservasi].

Gap yang tidak dapat menghasilkan konsekuensi yang dapat diukur biasanya hanya
celah topik, bukan celah penelitian.

---

## 2. Empat Jenis Gap yang Dipakai

| Kode | Jenis | Pertanyaan kunci | Bukti yang dibutuhkan |
|---|---|---|---|
| G-E | *Evidence gap* | Apakah fenomena yang diklaim benar-benar terukur? | Data pengukuran atau studi empiris sebelumnya |
| G-M | *Method gap* | Apakah metode yang ada mampu menangani kondisi ini? | Analisis keterbatasan metode + kasus yang gagal |
| G-I | *Integration gap* | Apakah komponen yang sudah ada pernah disatukan dan diuji bersama? | Matriks SOTA yang menunjukkan kombinasi kosong |
| G-C | *Context gap* | Apakah temuan berlaku pada konteks yang berbeda? | Perbedaan konteks: topologi, skala, iklim, perangkat |

Gap jenis **G-I saja** paling rentan dinilai "hanya kombinasi". Karena itu penelitian
ini harus bersandar pada **G-M dan G-E** sebagai gap utama, dan memakai G-I/G-C
sebagai pendukung posisi.

---

## 3. Peta Gap

### G-E1 — Dampak perubahan aturan PCC terhadap integritas sesi belum diukur

**Yang sudah diketahui.** PCC mempertahankan *connection mark* pada tabel
*conntrack*; pembaruan aturan yang hanya menyasar `connection-state=new` tidak
otomatis menghapus sesi lama (MikroTik, n.d.; Kumar dan Golash, 2009). Studi PCC
yang ada melaporkan QoS agregat seperti *throughput*, *delay*, *jitter*, dan
*packet loss* (Amalia et al., 2022; Arfianita et al., 2024; Nugroho et al., 2023).

**Yang belum ada.** Tidak ditemukan studi yang mengukur **TCP RST rate** atau
tingkat gangguan sesi sebagai akibat langsung dari perubahan rasio PCC, apalagi
yang membandingkan perlakuan *dengan* dan *tanpa* preservasi sesi secara terkontrol.

**Konsekuensi.** Klaim "session-preserving" pada literatur load balancing praktis
masih berupa asumsi desain. Tanpa pengukuran, tidak dapat dibedakan apakah
perlindungan sesi benar-benar bekerja atau hanya kebetulan karena beban uji rendah.

**Jenis:** G-E utama, diperkuat G-M.
**Tingkat keyakinan:** tinggi — dapat diverifikasi pada pilot 24–48 jam.

---

### G-E2 — Akumulasi stok koneksi lama di link yang memburuk belum diukur

**Yang sudah diketahui.** PCC bersifat *session-oriented*: koneksi lama
mempertahankan *connection mark* dan jalurnya, sedangkan perubahan aturan terutama
memengaruhi koneksi baru (MikroTik, n.d.).

**Yang belum ada.** Belum ada studi yang mengukur **distribusi koneksi lama** pada
setiap link setelah degradasi, apalagi yang menghubungkannya dengan pangsa beban
efektif. Studi PCC yang ada melaporkan QoS agregat atau RST, tetapi tidak
melaporkan berapa banyak koneksi yang masih “tertahan” di link yang sedang buruk.

**Konsekuensi.** Controller dapat mengira telah menggeser trafik karena rasio
koneksi baru berubah, padahal beban efektif pada link yang memburuk masih tinggi
akibat stok koneksi lama. Tanpa metrik ini, klaim “adaptif” tidak dapat dibuktikan.

**Jenis:** G-E, diperkuat G-M.
**Tingkat keyakinan:** tinggi — dapat diukur dari tabel *conntrack* per
*connection mark*.

---

### G-M1 — Histeresis pada literatur kontrol tidak diturunkan dari dinamika link LEO

**Yang sudah diketahui.** Histeresis dua ambang mencegah osilasi keputusan, dan
ambang yang identik antara aktivasi dan deaktivasi terbukti menimbulkan osilasi
pada sistem berkapasitas adaptif (Tournaire et al., 2023). Karakterisasi Starlink
menunjukkan pola periodik sekitar 15 detik pada *one-way delay* dan *throughput*
(Garcia et al., 2025; Hammer et al., 2024; Mohan et al., 2024).

**Yang belum ada.** Belum ada aturan perancangan *dwell count* dan ambang histeresis
yang **diturunkan dari durasi transien terukur** pada link LEO. Literatur histeresis
berada di domain *cloud auto-scaling* dan sistem kendali umum, bukan pada pemilihan
jalur WAN dengan derau non-stasioner dan transien periodik.

**Konsekuensi.** Parameter histeresis pada praktik load balancing dipilih secara
*ad hoc*. Jika `k_down × T_s` lebih pendek daripada durasi transien, sistem dapat
masuk `DEGRADED` berulang pada setiap siklus 15 detik — persis kegagalan yang ingin
dicegah. Sebaliknya, jika terlalu panjang, pemulihan menjadi lambat.

**Jenis:** G-M utama.
**Tingkat keyakinan:** tinggi — dapat diuji dengan analisis aliasing dan replay trace.

---

### G-M2 — Konversi skor kualitas kontinu menjadi proporsi PCC diskret belum diformalkan

**Yang sudah diketahui.** SAW menghasilkan skor kontinu dari kriteria
*benefit/cost* (Vafaei et al., 2021; Wang dan Kuo, 2013). PCC mengeksekusi
pembagian berbasis *bucket* yang bersifat diskret (MikroTik, n.d.).

**Yang belum ada.** Belum ada pemetaan eksplisit dari skor kualitas multi-kriteria
ke **jumlah bucket integer** dengan batas bawah/atas, penanganan sisa pembulatan,
dan jaminan bahwa perubahan skor kecil tidak selalu mengubah aturan efektif.

**Konsekuensi.** Dua sistem dapat memakai skor kualitas yang sama tetapi menghasilkan
perilaku *flapping* yang berbeda hanya karena granularitas bucket. Tanpa formalisasi,
hasil antar-penelitian tidak dapat dibandingkan.

**Jenis:** G-M.
**Tingkat keyakinan:** sedang–tinggi.

---

### G-M3 — Kebijakan alokasi belum mempertimbangkan stok koneksi lama dan aliran koneksi baru

**Yang sudah diketahui.** Literatur *load balancing* menghitung alokasi dari
kondisi link saat ini (Kumar & Golash, 2009; Amalia et al., 2022; Nugroho et al.,
2023). Literatur SD-WAN/DRL mengalokasikan *flow* pada level *overlay* (Cruvellier
et al., 2025; Giacometti et al., 2025).

**Yang belum ada.** Belum ada kebijakan alokasi pada level PCC yang secara
eksplisit memisahkan **stok koneksi lama** $S_i(t)$ dan **aliran koneksi baru**
$F_i(t)$, lalu menghitung persentase koneksi baru berdasarkan keduanya.

**Konsekuensi.** Alokasi “dinamis” yang hanya berbasis kualitas saat ini dapat
gagal menurunkan beban efektif di link yang memburuk, karena koneksi lama tidak
ikut berpindah. Diperlukan kebijakan *stock-flow aware* dan metrik seperti
*effective load skew* serta *time-to-rebalance*.

**Jenis:** G-M utama.
**Tingkat keyakinan:** tinggi — dapat diuji dengan simulasi dan data *conntrack*.

---

### G-I1 — Empat komponen belum pernah disatukan dalam satu loop kendali

**Yang sudah diketahui.** Secara terpisah: MCDM/SAW untuk memilih jaringan
(Wang dan Kuo, 2013; Vafaei et al., 2021), EWMA untuk penghalusan deret waktu
(Roberts, 1959), histeresis untuk mencegah osilasi (Tournaire et al., 2023), dan
PCC untuk distribusi beban (Amalia et al., 2022; Arfianita et al., 2024).

**Yang belum ada.** Belum ada studi yang menyatukan keempatnya dalam satu *state
machine* yang (a) menghasilkan rasio PCC, (b) menahan flapping, dan (c) menjaga
sesi berjalan — lalu **memisahkan kontribusi tiap komponen melalui ablasi**.

**Konsekuensi.** Praktisi tidak punya bukti komponen mana yang benar-benar
menyumbang perbaikan. Tanpa ablasi, klaim manfaat sering kali merupakan efek
gabungan yang tidak dapat diatribusikan.

**Jenis:** G-I.
**Tingkat keyakinan:** tinggi, tetapi **belum cukup sebagai novelty tunggal**.

---

### G-C1 — Studi PCC dominan statis, homogen, dan laboratorium

**Yang sudah diketahui.** Studi PCC yang ada menetapkan rasio pada tahap
konfigurasi dan menguji topologi ISP homogen di laboratorium atau simulasi
(Amalia et al., 2022; Arfianita et al., 2024; Nugroho et al., 2023; Putra dan
Anton, 2024; Mirsal dan Agtriadi, 2026).

**Yang belum ada.** Belum ada evaluasi lapangan pada **dual-ISP FO–LEO** yang
menggabungkan link terestrial dan satelit, dengan pola degradasi berbeda:
operasional-komersial pada FO dan fisik-atmosferik pada LEO.

**Konsekuensi.** Temuan pada ISP homogen tidak otomatis berlaku ketika dua link
memiliki skala waktu degradasi yang berbeda satu orde besaran.

**Jenis:** G-C.
**Tingkat keyakinan:** tinggi untuk klaim konteks; perlu deskripsi lokasi yang jujur.

---

### G-C2 — Klaim portabilitas platform belum diuji

**Yang sudah diketahui.** Pola *adapter* memisahkan logika dari implementasi
(Gamma et al., 1994), dan arsitektur *offloading controller* lazim pada SDN
(Ali et al., 2025; Wang dan Kuo, 2013).

**Yang belum ada.** Studi load balancing praktis umumnya menempel pada satu vendor
dan tidak menyediakan kontrak antarmuka yang dapat diuji dengan *mock adapter*.

**Konsekuensi.** Algoritma sulit direplikasi dan hasilnya sulit dibandingkan
lintas platform.

**Jenis:** G-C, bersifat rekayasa.
**Tingkat keyakinan:** sedang — jangan mengklaim lebih dari "dirancang portabel".

---

## 4. Pernyataan Gap (Satu Paragraf)

> Meskipun PCC telah terbukti menjaga konsistensi sesi dibanding ECMP/NTH dan
> literatur telah menyediakan metode skor multi-kriteria serta mekanisme histeresis
> secara terpisah, belum ada studi yang (i) menurunkan parameter histeresis dari
> durasi transien link LEO yang terukur, (ii) memformalkan pemetaan skor kualitas
> kontinu menjadi proporsi PCC diskret, (iii) mengukur dampak perubahan rasio
> terhadap integritas sesi TCP, dan (iv) mempertimbangkan **stok koneksi lama**
> yang tetap menempati link yang memburuk dalam perhitungan alokasi. Akibatnya,
> controller dapat mengubah rasio koneksi baru tanpa menurunkan beban efektif pada
> link yang memburuk, dan praktisi tidak memiliki dasar kuantitatif untuk menilai
> apakah mekanisme adaptif benar-benar bekerja.

Paragraf ini yang akan menjadi **inti 1.1 dan 1.2.10** pada naskah proposal.

---

## 5. Bukan Gap Penelitian Ini

Agar tidak membangun *strawman*, hal-hal berikut **tidak** diklaim sebagai gap:

| Klaim yang harus dihindari | Alasan |
|---|---|
| "Belum ada yang meneliti load balancing PCC" | Salah; banyak studi PCC |
| "Belum ada yang memakai SAW untuk jaringan" | Salah; MCDM sudah lazim |
| "Belum ada yang memakai histeresis" | Salah; histeresis sudah dipakai di cloud/kontrol |
| "PCC selalu merusak sesi" | Tidak terbukti; justru perlu diukur |
| "Metode kami menggantikan SD-WAN" | Berlebihan; lingkupnya kecil-menengah |

---

## 6. Rencana Verifikasi Gap

Gap di atas masih bersandar pada korpus yang sudah dikumpulkan. Sebelum Tahap 3,
lakukan verifikasi sistematis:

1. **Basis data:** Scopus, IEEE Xplore, ACM DL, ScienceDirect, Google Scholar.
2. **String pencarian inti:**
   - `("PCC" OR "per connection classifier") AND ("adaptive" OR "quality") AND ("MikroTik" OR "RouterOS")`
   - `("hysteresis") AND ("load balancing" OR "network selection") AND ("threshold" OR "dwell")`
   - `("Starlink" OR "LEO") AND ("handover" OR "throughput") AND ("load balancing" OR "multipath")`
   - `("session preservation" OR "connection tracking") AND ("load balancing" OR "failover")`
   - `("MCDM" OR "SAW") AND ("network selection") AND ("real-time")`
3. **Kriteria inklusi:** 2015–2026, bahasa Inggris/Indonesia, akses penuh, relevan
   pada salah satu dari empat komponen.
4. **Kriteria eksklusi:** opini tanpa data, studi murni teoritis tanpa evaluasi,
   konteks yang tidak dapat dipetakan.
5. **Luaran:** `04_Uji_Kelayakan_dan_Risiko_Penguji.md` diperbarui dengan hasil
   pencarian dan jumlah hit.

**Aturan bukti:** klaim "belum ada" hanya boleh ditulis setelah minimal dua
kombinasi string di atas dijalankan dan hasilnya didokumentasikan.

---

## 7. Ringkasan Prioritas Gap

| Gap | Jenis | Kekuatan sebagai novelty | Peran dalam proposal |
|---|---|---|---|
| G-M3: alokasi belum *stock-flow aware* | Method | **Tinggi** | **Kontribusi utama (H3c)** |
| G-E2: stok koneksi lama belum diukur | Evidence | **Tinggi** | **Kontribusi empiris utama (H3c)** |
| G-E1: RST/sesi belum diukur | Evidence | Tinggi | Pendukung (H3a) |
| G-M1: dwell histeresis tidak berbasis transien LEO | Method | Tinggi | Pendukung (H1/H2) |
| G-M2: skor kontinu → bucket diskret | Method | Sedang–tinggi | Formalisasi pendukung |
| G-I1: integrasi empat komponen | Integration | Sedang | Payung sistem, bukan novelty tunggal |
| G-C1: konteks FO–LEO lapangan | Context | Sedang | Validitas eksternal |
| G-C2: portabilitas platform | Context | Rendah–sedang | Rekayasa pendukung |

**Keputusan Tahap 1:** novelty utama bertumpu pada **G-M3 + G-E2**—
kebijakan alokasi *stock-flow aware* dan pengukuran stok koneksi lama. G-M1, G-E1,
dan G-M2 menjadi pendukung. Jika hanya G-I1 yang ditonjolkan, proposal berisiko
dinilai inkremental.
