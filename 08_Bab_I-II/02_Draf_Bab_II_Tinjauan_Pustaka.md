# BAB II
# TINJAUAN PUSTAKA DAN KERANGKA TEORITIS

**Status:** Draf kerja — belum naskah final
**Dasar:** `04_Tahap_03_Kerangka_Teori/`
**Aturan:** Setiap klaim faktual merujuk sumber di `03_Tabel_Klaim_dan_Sumber.md`.
Verifikasi halaman terbaru ada di `09_Verifikasi_dan_Pencarian/02_Verifikasi_Klaim.md`.

---

## 2.1 Kerangka Umum

Bab II berfungsi untuk tiga hal: (1) mendefinisikan konsep yang dipakai, (2)
mensintesis temuan penelitian terdahulu menjadi kerangka yang utuh, dan (3)
menunjukkan celah yang menjadi dasar hipotesis. Bab ini **bukan** kumpulan
ringkasan per artikel. Setiap subbab diakhiri dengan "Implikasi desain" yang
menjelaskan konsekuensinya bagi SPA-HSM.

Kerangka teoritis penelitian ini bertumpu pada satu gagasan: keputusan alokasi
trafik selalu berada di antara dua kegagalan — **terlalu reaktif** (flapping dan
gangguan sesi) dan **terlalu lambat** (pemanfaatan link buruk dan pemulihan
tertunda). SPA-HSM diformulasikan sebagai mekanisme yang memilih titik operasi
pada kurva trade-off tersebut, bukan sebagai metode yang mengklaim unggul pada
semua metrik sekaligus.

---

## 2.2 Quality of Service dan Pengukurannya

QoS adalah kemampuan jaringan menyediakan jaminan performa bagi trafik yang
dilewatkannya. Literatur umumnya meringkasnya menjadi empat parameter: *delay*,
*jitter*, *packet loss*, dan *throughput* (Nanang et al., 2024). Keempatnya
cenderung terdegradasi bersamaan ketika terjadi gangguan, sehingga pemantauan
harus dilakukan pada kombinasi, bukan pada satu metrik saja.

Standar yang dipakai sebagai acuan adalah ETSI TIPHON untuk klasifikasi kualitas
layanan (ETSI, 2000), ITU-T G.114 untuk batas *one-way delay* layanan interaktif
(ITU-T, 2003), dan ITU-T Y.1541 untuk objektif performa jaringan berbasis IP
(ITU-T, 2011). Pada sisi pengukuran, RFC 2330 menyediakan kerangka metrik
performa IP (Paxson et al., 1998), RFC 2544 menetapkan metodologi *benchmarking*
perangkat (Bradner & McQuaid, 1999), dan RFC 3550 mendefinisikan estimasi *jitter*
untuk trafik *real-time* (Schulzrinne et al., 2003).

Dua pembedaan penting dipakai konsisten di seluruh penelitian:

1. **QoS bukan QoE.** QoS diukur melalui metrik teknis seperti *throughput*,
   *delay*, *jitter*, dan *packet loss*, sedangkan QoE melibatkan persepsi
   pengguna dan model aplikasi (Wang et al., 2023). Penelitian ini mengukur QoS
   dan tidak mengklaim kepuasan pengguna.
2. **Carried throughput bukan achievable throughput.** Throughput yang terukur di
   antarmuka mencakup trafik yang mungkin tertahan atau diulang. Untuk skor
   kualitas, digunakan *goodput* atau *headroom*, bukan sekadar laju antarmuka.

**Implikasi desain.** Skor $Q_i(t)$ memakai *throughput* sebagai atribut *benefit*
dan *delay*, *jitter*, serta *loss* sebagai atribut *cost*. Normalisasi harus
memakai batas acuan tetap agar skor dapat dibandingkan antar-waktu dan tidak
berubah skala ketika kondisi link lain berubah.

---

## 2.3 Heterogenitas FO dan LEO Starlink

Jalur *fiber optic* (FO) unggul pada latensi rendah, *throughput* tinggi, dan
*loss* rendah karena mediumnya terlindung dari gangguan atmosferik. Namun kualitas
operasional FO tidak identik dengan kapasitas nominal: kepadatan pelanggan dan
gangguan pada jaringan akses membuat *throughput* aktual dapat berada di bawah
kapasitas nominal, terutama pada jam sibuk (Safitri et al., 2016). Gejala ini
bersifat operasional, bukan keterbatasan fisik medium, sehingga kualitas FO
perlu dievaluasi berkala dan tidak dapat diasumsikan konstan.

Starlink beroperasi pada orbit rendah (sekitar 550 km) sehingga latensinya jauh
lebih rendah daripada satelit GEO, tetapi konsekuensinya jaringan harus melakukan
*handover* antar-satelit secara periodik. Pengukuran dari sisi pengguna menunjukkan
variabilitas *throughput* dan latensi yang jauh lebih besar daripada jaringan
terestrial, disertai *outage* yang relatif sering (Ma et al., 2023; Mohan et al.,
2024). Pada wilayah tropis, *rain fade* memperburuk kondisi; curah hujan
diidentifikasi sebagai prediktor terkuat penurunan *throughput* (Boeckenholt et
al., 2024), dengan penurunan *throughput downlink* median dari sekitar 137 Mbps
menjadi 90,2 Mbps dan *uplink* dari 20,9 Mbps menjadi 10,5 Mbps saat hujan
(Ullah et al., 2025, hlm. 5).

Yang paling relevan bagi penelitian ini adalah **dua skala waktu degradasi**:

| Skala | Penyebab | Orde waktu | Implikasi kendali |
|---|---|---|---|
| Lambat | Cuaca, kongesti, kebijakan ISP | Menit–jam | Perlu evaluasi ulang berkala dan *dead zone* |
| Cepat | *Handover*, rekonfigurasi, transien | Detik (~15 detik) | Perlu *dwell* yang lebih panjang dari transien |

Karakterisasi *one-way delay* melaporkan pola periodik sekitar 15 detik yang
paling terdampak pada arah *uplink* (Garcia et al., 2025), dan pola serupa
teramati sebagai penurunan *throughput* berulang pada batas interval 15 detik
(Hammer et al., 2024; Mohan et al., 2024).

**Implikasi desain.** Sampling harus cukup cepat untuk menangkap transien, tetapi
tidak boleh lebih cepat dari yang dapat direspons oleh aktuator. Parameter *dwell*
histeresis harus memperhitungkan durasi transien; jika tidak, sistem dapat
memasuki `DEGRADED` berulang pada setiap siklus transien.

---

## 2.4 PCC dan Load Balancing pada RouterOS

*Per Connection Classifier* (PCC) mengelompokkan trafik berdasarkan kombinasi
atribut koneksi, misalnya *source address*, *destination address*, dan *port*.
Seluruh paket dalam satu sesi konsisten dialirkan melalui *gateway* yang sama,
sehingga risiko *packet reordering* yang merusak kinerja TCP berkurang
(Kumar & Golash, 2009; MikroTik, n.d.).

Implementasi PCC pada RouterOS memakai aturan *mangle* untuk memberi *connection
mark* dan *routing mark*, yang kemudian dipakai tabel routing untuk memilih
*gateway*. Koneksi yang sudah terbentuk mempertahankan *connection mark* pada
tabel *connection tracking* (*conntrack*), sedangkan koneksi baru mengikuti aturan
yang berlaku saat paket pertama diproses (MikroTik, n.d.).

Perbandingan tiga metode pembagian beban yang tersedia pada RouterOS:

| Aspek | PCC | ECMP | NTH |
|---|---|---|---|
| Dasar pembagian | Atribut koneksi | Rute berbiaya sama | Urutan paket ke-n |
| Konsistensi sesi | Tinggi | Sedang | Rendah |
| Beban komputasi | Sedang | Rendah | Rendah |
| Risiko *reordering* | Rendah | Sedang | Tinggi |
| Kecocokan trafik *stateful* | Tinggi | Sedang | Rendah |

Studi komparatif menempatkan PCC lebih unggul dalam konsistensi sesi dan
stabilitas koneksi aplikasi *stateful* dibanding ECMP dan NTH (Nugroho et al.,
2023; Mirsal & Agtriadi, 2026). Penerapan PCC pada dua dan tiga ISP juga
melaporkan perbaikan QoS berdasarkan TIPHON (Amalia et al., 2022; Arfianita et
al., 2024), serta pengurangan dampak gangguan ISP ketika dipadukan dengan
*failover* (Putra & Anton, 2024).

### 2.4.1 Posisi bukti: SOTA versus konteks

Studi PCC di atas penting sebagai bukti konteks implementasi di jaringan lokal
dan RT/RW Net, tetapi sebagian besar berasal dari jurnal/kepanitiaan nasional.
Dalam kerangka *state of the art*, posisinya perlu dibedakan:

| Kelompok | Contoh | Peran dalam Bab II |
|---|---|---|
| SOTA inti (T1) | Kumar & Golash (2009); Ali et al. (2025) | Pembanding internasional |
| SOTA pendukung (T2) | Amalia et al. (2022); Arfianita et al. (2024) | Prosiding/konteks terbatas |
| Konteks lokal (T3) | Nugroho et al. (2023); Putra & Anton (2024); Mirsal & Agtriadi (2026); Bustomi & Tahir (2026) | Praktik RT/RW Net, bukan dasar gap global |

Konsekuensinya, klaim "state of the art PCC" tidak boleh bersandar pada studi T3.
Komponen PCC masih memerlukan 3–5 referensi internasional tentang *adaptive load
balancing*, SD-WAN *multipath*, atau *traffic steering* (lihat P-02 pada
`05_Evaluasi_Tahap_1-3/02_Checklist_Perbaikan.md`).

Namun, seluruh studi tersebut menetapkan rasio pembagian secara **statis** pada
tahap konfigurasi. Rasio tidak dievaluasi ulang terhadap kondisi link secara
*real-time*; ketika salah satu ISP terdegradasi, router tetap menyalurkan proporsi
trafik sesuai rasio semula. Klaim ini berlaku baik untuk studi T1 maupun T3,
tetapi kekuatan buktinya berbeda.

### 2.4.2 Load balancing adaptif pada WAN

Literatur SD-WAN menunjukkan bahwa kebijakan *traffic engineering* statis mulai
ditinggalkan. Rajagopalan (2020) merangkum peran *load balancing* pada SD-WAN.
Cruvellier et al. (2025) menyatakan solusi SD-WAN saat ini masih bergantung pada
kebijakan *traffic engineering* statis dan mengusulkan *deep reinforcement
learning* untuk kebijakan adaptif; simulasi mereka melaporkan perbaikan 48,94%
pada lingkungan *bandwidth* asimetris. Giacometti et al. (2025) mengusulkan
*multi-agent reinforcement learning* untuk *traffic steering* guna mengurangi
gangguan layanan. Pada konteks satelit–terestrial, Shahid et al. (2020)
mengusulkan *load balancing* multi-RAT dengan *radio resource utilization ratio*
dan *adaptive threshold* untuk menentukan sel *overload*; algoritme tersebut juga
memperkirakan dampak pemindahan beban untuk menghindari aksi yang tidak perlu.

Studi-studi tersebut menunjukkan bahwa alokasi sadar-kondisi memang diperlukan.
Namun, mereka beroperasi pada level *overlay*, *flow steering*, atau sel/RAT,
bukan pada granularitas *bucket* PCC. Tidak ada yang membahas *conntrack*,
preservasi sesi TCP, atau eksekusi pada router kelas SOHO. *Adaptive threshold*
pada level sel/RAT juga belum diterjemahkan menjadi aturan *dwell* per koneksi.
Karena itu, pendekatan tersebut tidak dapat langsung dipakai sebagai pembanding
SPA-HSM, tetapi menjadi bukti bahwa masalah yang lebih umum—alokasi adaptif lintas
jalur—sedang aktif diteliti.

**Implikasi desain.** Pendekatan SD-WAN/DRL menunjukkan arah, tetapi tidak
menggantikan mekanisme ringan di level PCC. Penelitian ini mengambil posisi di
antara keduanya: adaptif seperti SD-WAN, tetapi cukup ringan dan sadar-sesi
seperti PCC.

**Implikasi desain.** PCC dipakai sebagai **aktuator**, bukan sebagai objek yang
dikembangkan. Yang diteliti adalah kebijakan yang menentukan rasio, bukan
implementasi PCC itu sendiri. Baseline praktisi yang dipakai adalah PCC dengan
`netwatch`/health-check *failover*, karena itu yang lazim tersedia bagi praktisi.

---

## 2.5 MCDM dan Simple Additive Weighting

MCDM mengevaluasi sejumlah alternatif berdasarkan lebih dari satu kriteria.
*Simple Additive Weighting* (SAW) menghasilkan skor melalui penjumlahan hasil kali
nilai kriteria yang telah dinormalisasi dengan bobotnya:

$$Q_i(t) = \sum_{j=1}^{m} w_j \, r_{ij}(t), \qquad \sum_j w_j = 1$$

dengan $r_{ij}$ adalah nilai ternormalisasi kriteria $j$ pada link $i$ dan $w_j$
bobot kriteria. Atribut *benefit* (mis. *throughput*) dinormalisasi naik, atribut
*cost* (mis. *delay*) dinormalisasi turun (Vafaei et al., 2021; Wang & Kuo, 2013).

Pemilihan teknik normalisasi terbukti memengaruhi peringkat akhir secara
signifikan (Vafaei et al., 2021). Karena itu, penelitian ini memakai **batas acuan
tetap** yang mengacu pada standar QoS, bukan nilai minimum/maksimum antar-link
pada setiap siklus:

$$r^{benefit}_{ij} = \frac{x_{ij} - x^{\min}_j}{x^{\max}_j - x^{\min}_j}, \qquad
r^{cost}_{ij} = \frac{x^{\max}_j - x_{ij}}{x^{\max}_j - x^{\min}_j}$$

dengan $x^{\min}_j$ dan $x^{\max}_j$ adalah batas acuan tetap, bukan statistik
antar-link. Penanganan $0/0$ memakai $\varepsilon = 10^{-6}$.

**Mengapa batas tetap.** Jika normalisasi memakai min–max antar-link setiap
siklus, skor satu link berubah ketika link lain berubah, sehingga $Q_i(t)$ tidak
lagi dapat dibandingkan antar-waktu dan keputusan menjadi tidak stabil. Batas
tetap mengorbankan adaptivitas skala demi komparabilitas dan stabilitas.

**Keterbatasan yang diakui.** SAW mengasumsikan kriteria saling independen;
*delay*, *jitter*, dan *loss* dapat berkorelasi. Asumsi ini dicatat sebagai
keterbatasan, bukan diabaikan. Bobot ditetapkan statis dan dikalibrasi di awal
(K-03), dengan analisis sensitivitas.

---

## 2.6 EWMA sebagai Penghalus Deret Waktu

Metrik jaringan mengandung derau dan lonjakan sesaat. Jika skor dihitung dari satu
sampel, keputusan dapat berubah karena anomali yang tidak bertahan lama. EWMA
adalah filter rekursif yang memberi bobot lebih besar pada sampel terbaru:

$$E_i(t) = \alpha \, x_i(t) + (1-\alpha) \, E_i(t-1), \qquad \alpha \in (0,1]$$

dengan $\alpha$ sebagai koefisien penghalusan (Roberts, 1959). Nilai $\alpha$ kecil
menghasilkan penghalusan lebih kuat dan *effective window* lebih panjang
($N_{eff} \approx 2/\alpha - 1$); nilai besar membuat filter lebih responsif.

EWMA dipilih karena ringan secara komputasi, hanya membutuhkan satu nilai state
per metrik, dan mudah dijelaskan kepada praktisi. Perannya adalah **pra-filter**
sebelum SAW dan histeresis. Kombinasi keduanya disengaja: EWMA meredam derau
berfrekuensi tinggi, sedangkan histeresis mencegah keputusan berbalik arah di
sekitar ambang. Keduanya tidak saling menggantikan.

**Implikasi desain.** $\alpha$ dan $T_s$ harus dipilih bersama. Jika $T_s$ terlalu
besar, transien 15 detik dapat ter-*alias*; jika terlalu kecil, beban pengukuran
dan sensitivitas terhadap derau meningkat.

---

## 2.7 Histeresis Asimetris dan State Machine

Histeresis menetapkan dua ambang berbeda untuk mengaktifkan dan menonaktifkan
suatu kondisi, sehingga terbentuk *dead zone* yang mencegah keputusan berbalik
arah akibat fluktuasi kecil. Pada histeresis **simetris**, ambang aktivasi dan
deaktivasi berjarak sama dari titik tengah. Pada histeresis **asimetris**, ambang
pemulihan lebih ketat daripada ambang degradasi.

Penetapan ambang ganda terbukti menghindari osilasi keputusan pada sistem
berkapasitas adaptif; osilasi muncul apabila ambang aktivasi dan deaktivasi
identik (Tournaire et al., 2023). Pada literatur *handover* seluler, histeresis
dipakai untuk menyeimbangkan *unnecessary handover* dan *handover failure*
(Alhabo et al., 2017) — trade-off yang strukturnya sama dengan flapping versus
recovery latency pada penelitian ini.

Penelitian ini membedakan dua bentuk asimetri:

| Bentuk | Definisi | Efek utama |
|---|---|---|
| Asimetri amplitudo | $\theta_{high} - \theta_{low}$ besar | Menjaga dari osilasi di sekitar ambang |
| Asimetri waktu | $k_{up} \gg k_{down}$ | Menahan pemulihan semu, memperlambat reaktivasi |

Ablasi Tahap 4 memfokuskan pada **asimetri waktu**: $\theta$ dipertahankan sama
antara varian simetris dan asimetris, sedangkan $k_{up}$ dibuat lebih panjang.

### 2.7.1 Formalisasi state machine

State per link: $s_i(t) \in \{\text{STABLE}, \text{DEGRADED}\}$.

| Transisi | Kondisi | Parameter |
|---|---|---|
| STABLE → DEGRADED | $Q_i(t) < \theta_{low}$ selama $k_{down}$ sampel berturut-turut | $\theta_{low}, k_{down}$ |
| DEGRADED → STABLE | $Q_i(t) > \theta_{high}$ selama $k_{up}$ sampel berturut-turut | $\theta_{high}, k_{up}$ |

Syarat: $\theta_{high} > \theta_{low}$ dan $k_{up} > k_{down}$. Evaluasi ulang
dipaksa minimal setiap $T_{max}$ agar degradasi lambat tidak tertahan di *dead
zone*.

### 2.7.2 Aturan dwell sadar-transien (kontribusi inti)

**Proposisi 1.** Jika periode transien dominan adalah $T_{tr}$ dan interval
sampling $T_s$, maka memilih

$$k_{down} \cdot T_s > T_{tr} + m$$

dengan margin $m \ge T_s$ mencegah transien periodik memicu transisi `DEGRADED`
berulang, dengan konsekuensi *detection delay* paling besar $k_{down} \cdot T_s$.

**Proposisi 2.** Untuk $\theta$ tetap, menaikkan $k_{up}$ menurunkan flapping
tetapi menaikkan *recovery latency*. Pasangan (flapping, recovery) membentuk
*frontier* monoton; tidak ada satu titik yang optimal untuk semua kendala, sehingga
titik operasi harus dipilih sesuai SLA.

Kedua proposisi ini bukan teorema formal. Keduanya adalah **pernyataan desain yang
dapat diuji** melalui *replay trace* dan eksperimen ablasi. Jika data menunjukkan
sebaliknya, proposisi direvisi.

**Implikasi desain.** Parameter histeresis tidak lagi dipilih *ad hoc*, tetapi
diturunkan dari karakteristik link dan kendala operasional. Ini yang membedakan
pendekatan penelitian ini dari studi PCC yang memakai rasio statis.

---

## 2.8 Preservasi Sesi dan Connection Tracking

Pada RouterOS, aturan PCC dievaluasi ketika paket pertama suatu koneksi diproses.
Setelah koneksi terbentuk, *connection mark* disimpan pada tabel *conntrack* dan
dipakai untuk paket berikutnya. Perubahan aturan *mangle* tidak otomatis menghapus
*conntrack*; koneksi yang sudah ada umumnya mempertahankan *mark* awalnya
(MikroTik, n.d.). Karena itu, pembaruan rasio yang hanya menyasar
`connection-state=new` dapat membiarkan sesi lama tetap pada jalur semula. Sifat
inilah yang menjadi dasar mekanisme `AFFINITY_LOCK`.

Namun preservasi sesi tidak boleh diasumsikan tanpa pengujian. Perubahan *routing
mark*, penghapusan *conntrack*, atau perubahan *gateway* untuk paket yang sudah
berjalan dapat menyebabkan *reordering*, retransmisi, atau *reset*. Pada TCP,
*reset* dapat muncul ketika salah satu ujung menerima paket di luar jendela yang
diharapkan atau ketika *middlebox* kehilangan state (Eddy, 2022).

### 2.8.1 Kontinuitas sesi pada level transport

Masalah kontinuitas sesi juga dibahas pada literatur *Multipath TCP* (MPTCP).
Liénardy & Donnet (2016) menunjukkan bahwa *load balancer* stateless pada
*entry point* data center dapat meneruskan subflow ke server berbeda, sehingga
manfaat MPTCP hilang. Duchene & Bonaventure (2017) menunjukkan bahwa perubahan
kecil pada penanganan subflow awal membuat MPTCP kompatibel dengan *load balancer*
stateless, sekaligus mendukung agregasi *bandwidth* dan *fast handover*.

Pada konteks Starlink, Jiang et al. (2024) menemukan bahwa *handover* periodik
15 detik menyebabkan interupsi link dan *bursty loss* yang merusak kinerja TCP.
StarTCP menahan transmisi selama *handover* untuk menghindari sinyal kongesti
yang keliru. Naimi et al. (2024) menginventarisasi parameter *load balancing*
pada *scheduler* MPTCP.

Literatur ini menangani kontinuitas di level **transport**, bukan di level
keputusan proporsi PCC. MPTCP membutuhkan dukungan ujung-ke-ujung, sedangkan
SPA-HSM bekerja pada router dan harus menjaga sesi yang sudah ada tanpa mengubah
aplikasi. Karena itu, keduanya saling melengkapi, bukan saling menggantikan.

**Implikasi desain dan pengukuran.** (1) `AFFINITY_LOCK` diperlakukan sebagai
hipotesis, bukan jaminan. (2) TCP RST *rate* diukur pada *vantage point* di luar
router. (3) Perlakuan "tanpa affinity" didefinisikan teknis sebagai *selective
conntrack flush* setelah aturan baru diterapkan, agar perbandingan tidak menjadi
*strawman*. (4) Temuan MPTCP/StarTCP dipakai sebagai bukti bahwa gangguan sesi
nyata, tetapi solusi yang diuji tetap berada di level PCC.

---

## 2.9 Arsitektur Kontrol dan Pola Adapter

Pemisahan logika keputusan dari mekanisme eksekusi merupakan prinsip umum pada
sistem yang perlu diuji pada beberapa platform. Pola *adapter* memungkinkan satu
antarmuka abstrak diimplementasikan oleh beberapa platform tanpa mengubah inti
algoritma (Gamma et al., 1994). Pola ini menyerupai arsitektur *offloading
controller* pada SDN, di mana controller eksternal membaca kondisi jaringan,
menghitung kebijakan, lalu menyuntikkan aturan ke perangkat (Ali et al., 2025;
Wang & Kuo, 2013).

Pada penelitian ini, pemisahan diwujudkan dalam tiga lapis:

| Lapis | Isi | Tanggung jawab |
|---|---|---|
| *Algorithm Core* | EWMA, SAW, state machine, pemetaan rasio | Menghasilkan keputusan |
| *Abstract Allocation Interface* | `read_metrics`, `set_ratio`, `set_affinity`, `get_state`, `verify`, `rollback`, `AFFINITY_LOCK` | Kontrak yang dapat diuji |
| *Platform Adapter* | `MikroTikAdapter`, `MockAdapter` | Mengeksekusi direktif |

**Batas klaim.** Penelitian hanya memvalidasi satu adapter nyata (MikroTik) dan
memakai *mock adapter* untuk menguji kontrak. Klaim yang diajukan adalah "dirancang
portabel dan diuji melalui kontrak antarmuka", bukan "terbukti portabel di semua
vendor".

---

## 2.10 Sintesis Kerangka Teoritis

### 2.10.1 Rantai kausal

```
degradasi link (FO/LEO)
        │
        ▼
metrik QoS derau + transien
        │  sampling Ts
        ▼
EWMA (α) ──► Q_i(t) ──► histeresis (θ, k_down, k_up)
                              │
                              ▼
                     state s_i(t)
                              │
                              ▼
              rasio target W_i(t) ──► bucket b_i(t)
                              │
                              ▼
                 aturan PCC (new flows)
                    │                    │
                    ▼                    ▼
              flapping              sesi berjalan
                    │                    │
                    └────────┬───────────┘
                             ▼
                 goodput, latency, RST
                             │
                             ▼
                           SIWG
```

Rantai ini menjelaskan mengapa keempat komponen harus disatukan: perubahan pada
satu parameter ($\alpha$, $\theta$, $k$, $N$) merambat ke flapping, sesi, dan
kinerja. Tanpa model yang menyatukan, efek tidak dapat diatribusikan.

### 2.10.2 Rumusan masalah kendali

Penelitian ini memformulasikan pemilihan parameter sebagai masalah kendali
terbatas:

$$\max_{\alpha,\, \theta_{low},\, \theta_{high},\, k_{down},\, k_{up},\, N}
\quad \mathbb{E}[\text{SIWG}]$$

dengan kendala:

$$\text{FR} \le F_{max}, \qquad \text{RL}_{p95} \le R_{max}, \qquad
\sum_i b_i = N, \qquad b_{min} \le b_i \le b_{max}$$

dengan FR = *flapping rate*, RL = *recovery latency*, dan $N$ = jumlah bucket.

Rumusan ini bukan klaim optimasi global. Yang dicari adalah **titik operasi yang
layak** dan **frontier trade-off**-nya, bukan solusi optimal matematis.

### 2.10.3 Dari teori ke hipotesis

| Proposisi/teori | Hipotesis | Variabel yang diuji |
|---|---|---|
| Histeresis menekan osilasi (Tournaire et al., 2023) | H1 | Flapping, recovery |
| Asimetri waktu menahan pemulihan semu (Proposisi 2) | H2 | Flapping, recovery |
| Conntrack mempertahankan mark sesi lama (MikroTik, n.d.) | H3a | RST flow |
| Alokasi sadar-kondisi meningkatkan kinerja (Ali et al., 2025) | H3b | Goodput, latency |
| Trade-off stabilitas–kontinuitas–kinerja (Proposisi 1–2) | H4 | SIWG |
| Pemisahan inti–adapter (Gamma et al., 1994) | H5 | Urutan keputusan |

---

### 2.10.4 Metrik SIWG

Trade-off stabilitas–kontinuitas–kinerja perlu diringkas menjadi satu ukuran agar
skenario dapat dibandingkan. Penelitian ini mendefinisikan
*Session-Impact-Weighted Goodput* (SIWG):

$$\text{SIWG} = G_{eff} \times (1 - \lambda \cdot \text{RST}_{flow})$$

dengan $G_{eff}$ adalah *goodput* efektif episode, $\text{RST}_{flow} \in [0,1]$
adalah proporsi aliran TCP terganggu, dan $\lambda \in [0,1]$ adalah bobot biaya
sesi. Nilai primer $\lambda = 1$; analisis sensitivitas memakai
$\lambda \in \{0{,}25;\ 0{,}5;\ 1{,}0\}$.

SIWG bukan standar industri dan tidak menggantikan QoS. Metrik ini adalah alat
pembanding internal yang membuat biaya gangguan sesi eksplisit. Jika arah hasil
berubah pada nilai $\lambda$ yang berbeda, klaim diturunkan menjadi "bergantung
pada bobot biaya sesi", bukan "selalu lebih baik".

---

## 2.11 Posisi Penelitian

Literatur telah membahas secara terpisah: QoS dan pengukuran (Nanang et al., 2024;
ETSI, 2000), karakteristik FO/LEO (Ma et al., 2023; Garcia et al., 2025), PCC dan
varian *load balancing* (Kumar & Golash, 2009; Amalia et al., 2022; Arfianita et
al., 2024), MCDM/SAW (Vafaei et al., 2021; Wang & Kuo, 2013), serta histeresis
pada sistem adaptif (Tournaire et al., 2023; Alhabo et al., 2017). Namun, belum
ditemukan studi yang menyatukan keempatnya dalam satu *state machine* yang
mengendalikan proporsi PCC, menjaga sesi, dan dipisahkan dari vendor—lalu mengukur
kontribusi tiap komponen melalui ablasi.

Klaim "belum ditemukan" telah diuji melalui pencarian OpenAlex (P-01): irisan
PCC × histeresis/dwell menghasilkan 0 hit, sedangkan irisan PCC × preservasi sesi
menghasilkan 2 studi lokal yang tidak mengukur RST. Karena itu, klaim dapat dipakai
dengan frasa "berdasarkan pencarian pada OpenAlex", bukan sebagai klaim universal.
Pencarian Scopus dan IEEE Xplore masih diperlukan sebagai pelengkap.

Literatur *adaptive load balancing* di SD-WAN/DRL (Rajagopalan, 2020; Cruvellier
et al., 2025; Giacometti et al., 2025) dan literatur kontinuitas transport
(Liénardy & Donnet, 2016; Duchene & Bonaventure, 2017; Jiang et al., 2024; Naimi
et al., 2024) menunjukkan bahwa masalah stabilitas dan kontinuitas sudah diakui.
Namun, solusinya ditempatkan pada level *overlay* atau *transport*, bukan pada
keputusan proporsi PCC di router. Belum ada studi yang menempatkan skor kualitas,
*dwell* sadar-transien, preservasi *conntrack*, dan ablasi komponen dalam satu
loop kendali pada WAN FO–LEO.

Kebaruan penelitian ini terletak pada tiga hal:

1. **Aturan *dwell* sadar-transien** yang menghubungkan $T_s$, durasi transien
   LEO, dan $k_{down}$ (Proposisi 1).
2. **Formalisasi pemetaan skor kontinu ke bucket PCC diskret** dengan jaminan
   $\sum b_i = N$ dan batas $b_{min}/b_{max}$.
3. **SIWG dan bukti ablasi** yang memisahkan kontribusi histeresis dan preservasi
   sesi terhadap *flapping*, RST, *goodput*, dan latensi.

Integrasi empat komponen (EWMA, SAW, histeresis, *affinity*) adalah payung sistem,
bukan novelty tunggal. Penelitian ini juga tidak mengklaim metode MCDM, EWMA, atau
histeresis yang baru.

Dari sisi kualitas bukti, Bab II memakai kebijakan tier: referensi T1 untuk SOTA
inti, T2 sebagai pendukung, dan T3 hanya untuk konteks. Studi PCC lokal tetap
dipakai untuk menggambarkan praktik RT/RW Net, tetapi tidak dijadikan dasar klaim
*state of the art*. Target minimal 15 SOTA inti dan 4 referensi kontinuitas sesi
ditetapkan sebelum seminar.

---

## 2.12 Ringkasan Bab

1. QoS diukur dengan empat parameter dan standar acuan tetap; QoE tidak diukur.
2. FO dan LEO memiliki skala degradasi berbeda: menit–jam vs detik.
3. PCC adalah aktuator yang konsisten per sesi, tetapi rasionya statis.
4. SAW memerlukan normalisasi berbatas tetap agar skor komparabel.
5. EWMA menghaluskan derau; histeresis mencegah osilasi; keduanya berbeda peran.
6. Preservasi sesi harus diukur, bukan diasumsikan.
7. Arsitektur tiga lapis memungkinkan pengujian tanpa menyentuh produksi.
8. Kerangka teoritis menghasilkan dua proposisi yang dapat diuji dan enam hipotesis.
