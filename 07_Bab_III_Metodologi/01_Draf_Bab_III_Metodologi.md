# BAB III
# METODOLOGI PENELITIAN

**Status:** Draf kerja — belum naskah final
**Dasar:** `06_Tahap_04_Metodologi/`
**Catatan:** Angka parameter dan ambang bersifat provisional sampai pilot selesai.
Setiap perubahan dicatat di `01_Manajemen_Proposal/01_Log_Keputusan.md`.

---

## 3.1 Jenis dan Pendekatan Penelitian

Penelitian ini menggunakan pendekatan **Research and Development (R&D)** yang
dipadukan dengan **desain kuasi-eksperimental**. Pendekatan R&D dipilih karena
luaran utama bukan temuan deskriptif, melainkan artefak berupa SPA-HSM yang
dirancang, diimplementasikan, dan diuji. Desain kuasi-eksperimental dipilih karena
pengujian dilakukan pada jaringan produksi yang melayani pelanggan, sehingga
cuaca, beban, dan kebijakan ISP tidak dapat dikendalikan sepenuhnya.

Evaluasi dilakukan pada dua lapis:

| Lapis | Tujuan | Lingkungan | Peran inferensi |
|---|---|---|---|
| **Staging** | Inferensi kausal dan replikasi | `tc netem`, *trace replay*, `MockAdapter` | Klaim sebab-akibat utama |
| **Lapangan** | Validitas eksternal | Jaringan RT/RW Net produksi | Validasi arah efek |

Pemisahan ini disengaja. Data lapangan mengandung *confounder* yang tidak dapat
diacak; staging menyediakan kondisi terkendali untuk menguji mekanisme. Klaim
kausal tidak dibuat dari lapangan saja, dan klaim generalisasi tidak dibuat dari
staging saja.

Tahapan penelitian disusun sebagai siklus rekayasa, bukan sebagai penerapan
NDLC yang kaku:

1. analisis kebutuhan dan studi literatur;
2. perancangan arsitektur dan formalisasi algoritma;
3. implementasi *Algorithm Core*, kontrak antarmuka, dan adapter;
4. pilot dan kalibrasi instrumen;
5. pengujian staging;
6. kampanye lapangan;
7. analisis dan pelaporan.

---

## 3.2 Lokasi dan Topologi Penelitian

Penelitian dilaksanakan pada usaha penyedia layanan internet skala rumah tangga
(RT/RW Net) di Desa Waeura, Kecamatan Waplau, Kabupaten Buru, Provinsi Maluku.
Lokasi ini dipilih karena memiliki dua jalur WAN heterogen yang menjadi objek
penelitian, yaitu FO IndiHome dan satelit LEO Starlink, serta telah beroperasi
secara komersial sehingga memiliki pola trafik pelanggan riil.

| Komponen | Spesifikasi | Peran |
|---|---|---|
| WAN1 | FO IndiHome | Link terestrial |
| WAN2 | Starlink (LEO) | Link non-stasioner |
| Router | MikroTik RB1100AHx4 | Agregasi, PCC, *conntrack* |
| Switch | 24 port | Distribusi pelanggan |
| Controller | Server terpisah di jalur manajemen | *Algorithm Core*, probe, kolektor |

Controller ditempatkan pada jalur manajemen agar pengambilan keputusan tidak
membebani *data plane* router. Jika controller gagal, router kembali ke
konfigurasi statis terakhir (*fail-static*).

Pemilihan lokasi didasari tiga pertimbangan: (1) topologi secara alami
merepresentasikan kombinasi FO–LEO; (2) sebagai jaringan komersial, pola trafik
pelanggan tidak dapat direplikasi secara akurat di simulasi murni; (3) Kabupaten
Buru sebagai wilayah kepulauan merepresentasikan kondisi Indonesia timur tempat
kombinasi FO dan LEO semakin umum.

**Batas klaim:** hasil tidak digeneralisasi ke skala *enterprise* atau ke topologi
dengan lebih dari dua ISP.

---

## 3.3 Variabel dan Definisi Operasional

### 3.3.1 Variabel

| Jenis | Variabel | Skala/operasionalisasi |
|---|---|---|
| Bebas | Kondisi eksperimen (A–G) | Kategorik |
| Bebas | Mode histeresis | none / symmetric / asymmetric |
| Bebas | Status affinity | off / on |
| Terikat | *Flapping rate* | flap per jam |
| Terikat | *Recovery latency* | detik; p50 dan p95 |
| Terikat | RST *flow* | persentase aliran TCP terganggu |
| Terikat | *Goodput* | Mbps byte aplikasi |
| Terikat | Latensi *end-to-end* | ms; p95 |
| Terikat | SIWG | Mbps setara |
| Kontrol | $T_s$, $\alpha$, $\theta$, $k$, $N$ | Tetap antar-kondisi |
| Kontrol | Perangkat dan firmware | Dicatat dan dikunci |
| *Confounder* | Cuaca, jam sibuk, beban pelanggan, perubahan ISP | Dicatat sebagai kovariat |

### 3.3.2 Definisi operasional

**Episode degradasi.** Periode yang dimulai saat $Q_i(t) < \theta_{low}$ selama
$k_{down}$ sampel berturut-turut dan berakhir saat $Q_i(t) > \theta_{high}$
selama $k_{up}$ sampel berturut-turut.

**Effective PCC rule change.** Perubahan jumlah bucket PCC pada minimal satu link.
Perubahan target rasio yang tidak mengubah alokasi bucket tidak dihitung.

**Flap.** *Effective rule change* yang diikuti perubahan arah sebaliknya dalam
jendela $W = 5$ menit. *Flapping rate* adalah jumlah flap per jam.

**Recovery latency.** Waktu dari sampel pertama $Q_i < \theta_{low}$ sampai state
kembali `STABLE`, yaitu $Q_i > \theta_{high}$ selama $k_{up}$ sampel berturut-turut.

**RST flow.** Proporsi aliran TCP yang menerima minimal satu paket RST selama
episode, diukur pada *vantage point* LAN. Nilai proporsi berada pada $[0,1]$ dan
dilaporkan sebagai persentase $\text{RST}_{flow}\%$.

**Goodput.** Byte tingkat aplikasi yang berhasil diterima dibagi durasi episode,
tidak termasuk retransmisi.

**SIWG.** *Session-Impact-Weighted Goodput*:

$$\text{SIWG} = G_{eff} \times (1 - \lambda \cdot \text{RST}_{flow})$$

dengan $\lambda = 1$ sebagai nilai primer dan analisis sensitivitas
$\lambda \in \{0{,}25;\ 0{,}5;\ 1{,}0\}$.

---

## 3.4 Desain Eksperimen dan Skenario

### 3.4.1 Kondisi eksperimen

| Kondisi | Histeresis | $k_{up}$ | Affinity | Peran |
|---|---|:---:|---|---|
| A | Tidak ada (statis 50:50) | — | — | Baseline statis |
| B | Tidak ada (dinamis) | — | Off | *Dynamic naive* |
| C | Simetris | 20 | Off | Isolasi bentuk histeresis |
| D | Asimetris | 60 | Off | Isolasi asimetri waktu |
| E | Simetris | 20 | On | Affinity pada simetris |
| F | Asimetris | 60 | On | **SPA-HSM (usulan)** |
| G | Tidak ada | — | — | Baseline praktisi `netwatch` |

Enam kondisi pertama membentuk **faktorial 2×2** (simetris/asimetris × affinity
off/on) ditambah dua pembanding (A dan B) serta satu baseline praktisi (G).
Kombinasi "tanpa histeresis + affinity on" tidak dijalankan; interaksi tersebut
diakui sebagai keterbatasan.

Parameter yang dipertahankan sama:

| Parameter | Nilai |
|---|---:|
| $T_s$ | 1 detik |
| $\alpha$ | 0,20 |
| $\theta_{low}$ | 0,60 |
| $\theta_{high}$ | 0,80 |
| $k_{down}$ | 20 |
| $k_{up}$ simetris / asimetris | 20 / 60 |
| $N$ | 20 bucket |
| $b_{min}$ / $b_{max}$ | 3 / 17 |
| $T_{max}$ | 10 menit |

### 3.4.2 Perbandingan kunci

| Hipotesis | Perbandingan | Faktor yang berubah |
|---|---|---|
| H1 | B vs C; B vs D | Kehadiran histeresis (affinity off) |
| H2 | C vs D; E vs F | Simetris vs asimetris |
| H3a | C vs E; D vs F; F vs A | Affinity (histeresis tetap) |
| H3b | F vs A; F vs G | Sistem usulan vs baseline |
| H4 | F vs semua kondisi | Efek gabungan |
| H5 | Dua adapter | Platform |

H1 sengaja hanya membandingkan B dengan C dan D karena ketiganya memakai affinity
off. Membandingkan B dengan E/F akan mengubah dua faktor sekaligus dan hasilnya
dilaporkan sebagai efek gabungan untuk H4.

### 3.4.3 Urutan, counterbalancing, dan washout

Urutan kondisi diatur dengan **Latin square** 7×7 dan diulang 3–4 blok. Setiap
kondisi diuji pada dua jendela waktu: jam sibuk (19.00–23.00) dan jam rendah
(01.00–05.00). Antar-kondisi diberi washout minimal 10 menit, diikuti verifikasi
bahwa tidak ada aturan atau entri *conntrack* yang tersisa.

### 3.4.4 Ukuran sampel

| Tahap | Unit | Target |
|---|---|---:|
| Staging | Episode | 20 per kondisi |
| Lapangan | Episode | ≥ 10 per kondisi |
| Total | Episode | 30 per kondisi |

Dengan 7 kondisi, target total sekitar 210 episode. Untuk uji dua sisi
$\alpha=0{,}05$, *power* 0,80, dan $d=0{,}5$, dibutuhkan sekitar 34 episode per
kelompok; target 30–40 adalah kompromi dengan keterbatasan lapangan. *Power* final
dihitung setelah pilot menggunakan estimasi ICC.

---

## 3.5 Formalisasi SPA-HSM

### 3.5.1 Sampling dan EWMA

Metrik dasar: *throughput*, *delay*, *jitter*, dan *loss*. Penghalusan:

$$E_{ij}(t) = \alpha x_{ij}(t) + (1-\alpha) E_{ij}(t-1)$$

dengan $\alpha=0{,}20$ dan *effective window* $N_{eff} \approx 2/\alpha - 1 = 9$
sampel. Dengan $T_s=1$ detik, satu siklus transien 15 detik tercakup oleh 15
sampel, sehingga bentuk transien masih terobservasi.

### 3.5.2 Skor kualitas berbasis SAW

Normalisasi memakai batas acuan tetap:

$$r_{ij} = \frac{E_{ij} - x_j^{min}}{x_j^{max} - x_j^{min}} \quad \text{(benefit)}$$

$$r_{ij} = \frac{x_j^{max} - E_{ij}}{x_j^{max} - x_j^{min}} \quad \text{(cost)}$$

| Kriteria | Arah | $x^{min}$ | $x^{max}$ | Bobot |
|---|---|---:|---:|---:|
| Throughput | Benefit | 0 Mbps | 100 Mbps | 0,35 |
| Delay | Cost | 0 ms | 150 ms | 0,30 |
| Jitter | Cost | 0 ms | 30 ms | 0,15 |
| Loss | Cost | 0% | 5% | 0,20 |

$$Q_i(t) = \sum_{j=1}^{4} w_j r_{ij}(t) \in [0,1]$$

Batas tetap dipilih agar $Q_i(t)$ komparabel antar-waktu dan tidak berubah skala
ketika kondisi link lain berubah (Vafaei et al., 2021). Bobot ditetapkan statis
dan diuji sensitivitasnya; pembelajaran bobot berada di luar lingkup.

### 3.5.3 State machine histeresis

| Transisi | Kondisi |
|---|---|
| STABLE → DEGRADED | $Q_i < \theta_{low}$ selama $k_{down}$ sampel |
| DEGRADED → STABLE | $Q_i > \theta_{high}$ selama $k_{up}$ sampel |

Aturan *dwell* sadar-transien:

$$k_{down} T_s > T_{tr} + m$$

Dengan $T_{tr} \approx 15$ detik dan $m = 1$ detik, $k_{down}=20$ memenuhi
$20 > 16$. *Detection delay* maksimum 20 detik, masih lebih pendek daripada
degradasi FO yang berskala menit. Asimetri waktu diimplementasikan dengan
$k_{up}=60$ pada varian asimetris, sedangkan $\theta$ dipertahankan sama.

### 3.5.4 Kebijakan rasio dan pemetaan bucket

Headroom dihitung dari utilisasi SNMP:

$$H_i(t) = \max(\varepsilon, 1 - u_i(t))$$

Saat kedua link `STABLE`:

$$W_i(t) = \frac{Q_i(t) H_i(t)}{\sum_k Q_k(t) H_k(t)}$$

Saat salah satu `DEGRADED`, rasio mengikuti tabel state:

| FO | LEO | $W_{FO}$ | $W_{LEO}$ |
|---|---|---:|---:|
| STABLE | STABLE | $QH$-based | $QH$-based |
| DEGRADED | STABLE | 0,15 | 0,85 |
| STABLE | DEGRADED | 0,85 | 0,15 |
| DEGRADED | DEGRADED | 0,50 | 0,50 |

Pemetaan ke bucket:

1. $b_i = \text{round}(N W_i)$;
2. batasi $b_i \in [b_{min}, b_{max}]$;
3. sesuaikan jumlah agar $\sum b_i = N$ dengan metode sisa terbesar;
4. jika tidak layak, gunakan pembagian merata dan catat error.

Jika satu link benar-benar *down*, seluruh trafik dialihkan ke link hidup sebagai
*override* keselamatan, meskipun melampaui $b_{max}$.

### 3.5.5 Preservasi sesi dan `AFFINITY_LOCK`

Pada RouterOS, aturan PCC dievaluasi saat paket pertama koneksi diproses.
*Connection mark* disimpan pada tabel *conntrack* dan dipakai untuk paket
berikutnya (MikroTik, n.d.). Karena itu, pembaruan aturan yang hanya menyasar
`connection-state=new` dapat mempertahankan sesi lama.

| Direktif | Perilaku |
|---|---|
| `set_affinity(true)` | Aturan baru hanya untuk koneksi baru; conntrack lama tidak disentuh |
| `set_affinity(false)` | Aturan baru diterapkan, lalu entri conntrack terkait di-*flush* selektif |
| `rollback(checkpoint)` | Kembalikan aturan sebelumnya |

Perlakuan "tanpa affinity" didefinisikan sebagai *selective conntrack flush*
setelah perubahan bucket. Ini perlakuan yang disengaja dan berisiko; risikonya
dicatat, dan efeknya diukur, bukan diasumsikan.

### 3.5.6 Arsitektur tiga lapis dan kontrak antarmuka

| Lapis | Isi | Tanggung jawab |
|---|---|---|
| *Algorithm Core* | EWMA, SAW, state machine, kebijakan rasio | Menghasilkan keputusan |
| *Abstract Allocation Interface* | `read_metrics`, `set_ratio`, `set_affinity`, `get_state`, `verify`, `rollback` | Kontrak yang dapat diuji |
| *Platform Adapter* | `MikroTikAdapter`, `MockAdapter` | Eksekusi dan verifikasi |

Inti tidak boleh mengimpor API vendor secara langsung. Adapter bertanggung jawab
atas penerjemahan, verifikasi, dan rollback. Klaim yang diajukan adalah "dirancang
portabel dan diuji melalui kontrak", bukan "terbukti portabel di semua vendor".

### 3.5.7 Pseudocode

```
init:
    warmup(60s)
    Q = compute_quality(read_metrics())
    apply_ratio(bucket_map(ratio_policy(Q)))

loop every Ts:
    m = read_metrics()
    E = ewma(m, alpha)
    Q = saw(E, weights, fixed_bounds)
    update_state(Q, theta_low, theta_high, k_down, k_up)
    W = ratio_policy(states, Q, headroom)
    b = bucket_map(W, N, b_min, b_max)
    if b != current_bucket:
        if affinity_on:
            set_ratio(b)
        else:
            set_ratio(b)
            flush_affected(b)
        log_rule_change(b)
    if now - last_force_eval > T_max:
        force_eval()
```

---

## 3.6 Instrumen dan Prosedur Pengukuran

### 3.6.1 Instrumen

| Metrik | Alat | Vantage point | Interval |
|---|---|---|---|
| RTT, jitter, loss | Probe ICMP/TCP | Controller, per WAN | 1 detik |
| Throughput | `iperf3` / HTTP | Endpoint uji | 10 menit |
| Goodput | `iperf3` / HTTP | Endpoint uji | Per episode |
| Utilisasi | SNMP `ifHCInOctets` | Router | 10 detik |
| Skor dan state | *Algorithm Core* | Controller | 1 detik |
| RST dan retransmisi | `tcpdump`/Wireshark | LAN capture | Kontinu |
| Telemetri Starlink | gRPC dish (jika tersedia) | Dish | 1 detik |
| Cuaca | Stasiun cuaca/BMKG | Lokasi | 10 menit |

Probe per WAN wajib memakai *routing mark* eksplisit agar tidak mengikuti jalur
default. Capture hanya menyimpan header, bukan payload.

### 3.6.2 Kalibrasi pilot

Pilot 24–48 jam dilakukan sebelum kampanye. Kriteria lulus:

1. selisih throughput SNMP vs probe < 10%;
2. probe benar-benar melewati WAN yang dituju;
3. RST terkontrol terdeteksi;
4. selisih jam antar-perangkat < 100 ms;
5. penurunan throughput akibat probe < 2%;
6. *fail-static* berfungsi saat controller dimatikan;
7. rollback selesai < 60 detik.

Jika salah satu gagal, kampanye tidak dimulai.

### 3.6.3 Perhitungan SIWG

Untuk setiap episode:

$$G_{eff} = \frac{\text{byte aplikasi}}{\text{durasi}}$$

$$\text{RST}_{flow} = \frac{\#\text{aliran terganggu}}{\#\text{aliran}} \in [0,1]$$

$$\text{SIWG} = G_{eff}(1 - \lambda \cdot \text{RST}_{flow})$$

Untuk pelaporan digunakan $\text{RST}_{flow}\% = 100 \times \text{RST}_{flow}$;
untuk SIWG digunakan proporsi.

Episode tanpa aliran TCP dikeluarkan dari H3a tetapi tetap masuk H3b.

### 3.6.4 Skema data

Data disimpan dalam dua tingkat: sampel skoring (1 detik) dan ringkasan episode.
Kolom wajib mencakup `timestamp`, `scenario`, `run_id`, `link_id`, metrik mentah,
`q_score`, `state`, `bucket`, `rule_change`, counter RST, `rain_mm`, `source`, dan
`notes`. Ringkasan episode mencakup `flaps`, `recovery_s`, `goodput_mbps`,
`latency_p95_ms`, `rst_flow_pct`, dan `siwg`.

---

## 3.7 Prosedur Pengujian

### 3.7.1 Sebelum run

1. Konfirmasi cuaca dan prakiraan.
2. Pastikan controller, probe, dan capture aktif.
3. Ekspor konfigurasi dan buat checkpoint.
4. Verifikasi NTP dan ruang disk.
5. Catat versi firmware dan paket ISP.

### 3.7.2 Saat run

1. Jalankan urutan sesuai Latin square.
2. Catat waktu mulai dan selesai.
3. Pantau dashboard dan alarm.
4. Catat setiap intervensi operator.
5. Hentikan run jika ada indikasi gangguan pelanggan.

### 3.7.3 Setelah run

1. Hentikan capture dan ekspor data.
2. Verifikasi checksum.
3. Rollback ke konfigurasi awal.
4. Catat catatan lapangan.
5. Backup ke dua lokasi.

### 3.7.4 Baseline A dan G

**A — PCC statis 50:50.** Rasio tetap, tanpa umpan balik kualitas.

**G — PCC + `netwatch`.** Pemeriksaan konektivitas setiap 10 detik; setelah tiga
kegagalan berturut-turut, *default route* diarahkan ke link yang aktif, dan
dikembalikan setelah link pulih selama 60 detik. Baseline ini tidak menyesuaikan
proporsi selama kedua link hidup.

### 3.7.5 Kegagalan dan rollback

Jika controller mati atau API putus, sistem masuk `FAIL_STATIC` dan mempertahankan
konfigurasi terakhir. Watchdog memeriksa heartbeat setiap 5 detik; jika hilang
lebih dari 30 detik, perubahan aturan dihentikan. Rollback dilakukan dengan
mengimpor checkpoint, memverifikasi aturan dan rute, lalu menguji konektivitas.

---

## 3.8 Analisis Data

### 3.8.1 Outcome

| Jenis | Outcome |
|---|---|
| Primer | *Flapping rate*, RST flow, *goodput*, SIWG |
| Sekunder | *Recovery latency* p95, RST packet, latensi p95, jitter, loss, overhead, fairness |

### 3.8.2 Unit analisis

Unit analisis adalah **episode degradasi** untuk recovery, goodput, RST, dan SIWG;
**jam pengamatan** untuk flapping; **aliran TCP** untuk RST flow. Sampel 1 detik
tidak diperlakukan sebagai observasi independen.

### 3.8.3 Model

| Hipotesis | Model | Efek yang dilaporkan |
|---|---|---|
| H1, H2 | *Negative binomial* campuran dengan *offset* jam | IRR + 95% CI |
| H3a | Logistik campuran level aliran; beta level episode | Selisih pp + 95% CI |
| H3b | LMM pada log(goodput) dan log(latency p95) | Rasio + 95% CI |
| H4 | LMM pada SIWG | Rasio + 95% CI |
| H5 | Uji konformitas dan kesamaan urutan | Persentase identik |

Efek acak: hari pengamatan dan run. Kovariat: tingkat keparahan degradasi dan
curah hujan. Diagnostik mencakup overdispersi, *zero-inflation*, normalitas
residual, dan autokorelasi.

### 3.8.4 Koreksi dan kekuatan uji

Koreksi **Holm–Bonferroni** diterapkan pada keluarga H1–H4. H5 dilaporkan
terpisah. *Power* final dihitung setelah pilot; jika target episode tidak
tercapai, hasil dilaporkan dengan interval kepercayaan dan presisi, bukan sebagai
"tidak ada efek".

### 3.8.5 Data hilang dan robustness

Tidak ada imputasi untuk outcome primer. Data hilang dilaporkan. Analisis
sensitivitas dilakukan tanpa episode hujan ekstrem, tanpa 60 detik pertama, dan
dengan nilai $\lambda$ berbeda untuk SIWG. Data staging dan lapangan dipisahkan
oleh variabel `source`.

### 3.8.6 Aturan keputusan

| Kondisi | Kesimpulan |
|---|---|
| p terkoreksi < α, effect size ≥ ambang, CI konsisten | Didukung |
| p < α tetapi effect size < ambang | Signifikan, tidak praktis |
| p ≥ α dengan CI lebar | Tidak konklusif |
| Arah berlawanan | Tidak didukung |
| Non-inferioritas terpenuhi | Non-inferior, bukan lebih baik |
| Primer lolos, sekunder gagal | Non-inferior, target absolut belum tercapai |

---

## 3.9 Etika dan Keselamatan Operasional

| Aspek | Tindakan |
|---|---|
| Izin | Persetujuan tertulis pemilik RT/RW Net |
| Pelanggan | Pemberitahuan tujuan dan jadwal minimal 24 jam |
| Privasi | Anonimisasi; tidak menangkap payload |
| Data | Header dan counter saja; disimpan terenkripsi |
| Retensi | Data mentah maksimal 2 tahun |
| Publikasi | Tidak menampilkan identitas pelanggan |
| Keselamatan | *Fail-static*, watchdog, backup, rollback teruji |
| Jendela perubahan | Perubahan besar hanya pada jam rendah |

Risiko utama dan mitigasinya:

| Risiko | Mitigasi |
|---|---|
| Cuaca buruk | Blok waktu, perpanjang kampanye, replay staging |
| Starlink outage | Pause, tandai run, ulangi |
| Perubahan ISP/firmware | Catat versi, uji ulang baseline |
| Controller mati | Fail-static, watchdog, UPS |
| Data hilang | Buffer lokal, checksum, backup harian |
| Episode kurang | Replay staging, laporkan presisi |
| Gangguan pelanggan | Probe ringan, jam rendah, hentikan run jika perlu |

---

## 3.10 Jadwal Penelitian

| Minggu | Aktivitas | Luaran |
|---:|---|---|
| 1–2 | Finalisasi desain dan kontrak antarmuka | Spesifikasi dan mock |
| 3–4 | Pilot dan kalibrasi | Laporan pilot |
| 5–6 | Replay staging | Dataset staging |
| 7 | Perbaikan parameter | Parameter final |
| 8–13 | Kampanye lapangan | Dataset lapangan |
| 14 | Pembersihan dan audit data | Dataset bersih |
| 15–17 | Analisis statistik | Tabel hasil |
| 18–19 | Penulisan Bab IV–V | Draf hasil |
| 20 | Konsolidasi dan format | Naskah siap seminar |

Sediakan penyangga 2 minggu untuk cuaca, gangguan, dan revisi. Jika penyangga
habis, cakupan diturunkan ke A, B, D, F dan dicatat sebagai penyimpangan.

---

## 3.11 Reproduksibilitas dan Artefak

| Artefak | Isi |
|---|---|
| Kode | *Algorithm Core*, adapter, mock, skrip analisis |
| Konfigurasi | Baseline A dan G, aturan PCC, parameter |
| Dataset | Skema sampel dan episode, metadata run |
| Log | Keputusan, intervensi, perubahan parameter |
| Analisis | Skrip R/Quarto dengan versi paket dan seed |
| Dokumentasi | README, protokol run, catatan rollback |

Repositori memakai struktur yang sama dengan folder kerja ini. Data mentah dan
informasi pelanggan tidak dipublikasikan; yang dipublikasikan adalah skema,
skrip, dan data teranonimisasi.

---

## 3.12 Batasan Metodologis

1. Tidak ada pembuktian formal kestabilan *control loop*; klaim stabilitas bersifat
   empiris.
2. Hanya satu adapter nyata (MikroTik); portabilitas diuji melalui kontrak, bukan
   lintas vendor.
3. Hanya dua ISP; generalisasi multi-ISP tidak diklaim.
4. Interaksi "tanpa histeresis × affinity" tidak diuji karena desain 2×2 + pembanding.
5. SIWG adalah metrik pembanding internal, bukan standar industri.
6. Data lapangan mengandung *confounder*; klaim kausal utama berasal dari staging.
7. QoE dan kepuasan pengguna tidak diukur.
