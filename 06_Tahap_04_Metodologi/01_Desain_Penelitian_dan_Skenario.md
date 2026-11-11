# Tahap 4 — Desain Penelitian dan Skenario

**Dokumen:** `01_Desain_Penelitian_dan_Skenario.md`
**Status:** Draf kerja Tahap 4
**Fungsi:** Menetapkan desain evaluasi yang menjawab H1–H5 secara terukur.
**Keputusan terkunci:** 6 skenario (A–F) + baseline praktisi G; baseline G =
`netwatch` failover.

---

## 1. Pendekatan Penelitian

Penelitian ini memakai dua lapis evaluasi:

| Lapis | Tujuan | Lingkungan | Kekuatan |
|---|---|---|---|
| **Staging** | Inferensi kausal dan replikasi | `tc netem` + *trace replay* + `MockAdapter` | Kondisi terkendali, dapat diulang |
| **Lapangan** | Validitas eksternal | Jaringan RT/RW Net produksi | Kondisi nyata, beban pelanggan riil |

Alasannya: data lapangan mengandung *confounder* (cuaca, jam sibuk, perubahan ISP)
yang tidak dapat dikendalikan sepenuhnya. Klaim kausal utama dibuat di staging;
lapangan dipakai untuk menguji apakah arah efek tetap sama pada kondisi nyata.

Pendekatan umum: **Research and Development (R&D)** untuk membangun artefak,
dipadukan **kuasi-eksperimen** untuk mengevaluasi. Randomisasi penuh tidak
diklaim karena kondisi lapangan tidak dapat diacak sepenuhnya.

---

## 2. Lokasi dan Topologi

**Rencana lokasi:** RT/RW Net di Desa Waeura, Kecamatan Waplau, Kabupaten Buru,
Maluku (konfirmasi akses: D-06).

| Komponen | Spesifikasi | Peran |
|---|---|---|
| WAN1 | FO IndiHome | Link terestrial |
| WAN2 | Starlink (LEO) | Link non-stasioner |
| Router | MikroTik RB1100AHx4 | Agregasi, PCC, conntrack |
| Switch | 24 port | Distribusi pelanggan |
| Controller | Server terpisah di jalur manajemen | Algorithm Core + probe + collector |

Controller ditempatkan di jalur manajemen agar pengambilan keputusan tidak
membebani *data plane*. Jika controller gagal, router kembali ke konfigurasi
statis terakhir (*fail-static*).

---

## 3. Kondisi Eksperimen

### 3.1 Tabel kondisi

| Kondisi | Histeresis | $k_{up}$ | Affinity | Peran |
|---|---|:---:|---|---|
| **A** | Tidak ada (rasio statis 50:50) | — | — | Baseline statis |
| **B** | Tidak ada (rasio dinamis) | — | Off | *Dynamic naive* |
| **C** | Simetris | 20 | Off | Isolasi bentuk histeresis |
| **D** | Asimetris | 60 | Off | Isolasi asimetri waktu |
| **E** | Simetris | 20 | On | Affinity pada simetris |
| **F** | Asimetris | 60 | On | **SPA-HSM (usulan)** |
| **G** | Tidak ada ($k$ tidak berlaku) | — | — | Baseline praktisi `netwatch` |

Parameter yang sama untuk semua kondisi kecuali yang disebut:

| Parameter | Nilai | Catatan |
|---|---|---|
| $T_s$ | 1 detik | Skala skoring |
| $\alpha$ | 0,20 | $N_{eff} \approx 9$ sampel |
| $\theta_{low}$ | 0,60 | Ambang degradasi |
| $\theta_{high}$ | 0,80 | Ambang pemulihan |
| $k_{down}$ | 20 | 20 detik > transien 15 detik + margin |
| $N$ | 20 bucket | Granularitas PCC |
| $b_{min}$ / $b_{max}$ | 3 / 17 | 15% dan 85% dari $N$ |
| $T_{max}$ | 10 menit | Evaluasi ulang paksa |

### 3.2 Mengapa bukan faktorial 3×2 penuh

Enam kondisi A–F membentuk **faktorial 2×2** (simetris/asimetris × affinity
off/on) ditambah **dua pembanding**:

- A = baseline statis,
- B = *dynamic naive* (tanpa histeresis, tanpa affinity),
- G = baseline praktisi.

Kombinasi "tanpa histeresis + affinity on" **tidak** dijalankan. Konsekuensinya,
interaksi antara ketiadaan histeresis dan affinity tidak dapat diuji. Ini dicatat
sebagai keterbatasan, bukan diklaim sebagai faktorial penuh 3×2.

**Alasan:** menambah satu kondisi lagi (8 total) menambah beban lapangan sekitar
15% tanpa menjawab hipotesis utama. H1–H4 tidak memerlukan sel tersebut.

---

## 4. Perbandingan Kunci

| Hipotesis | Perbandingan | Pertanyaan |
|---|---|---|
| H1 | B vs C; B vs D | Apakah histeresis menekan flapping? (affinity off) |
| H2 | C vs D; E vs F | Apakah asimetri waktu memperbaiki trade-off? |
| H3a | C vs E; D vs F; F vs A | Apakah affinity menjaga sesi? |
| H3b | F vs A; F vs G | Apakah kinerja agregat meningkat? |
| H4 | F vs semua kondisi | Apakah SIWG tertinggi? |
| H5 | Dua adapter | Apakah inti portabel? |

Perbandingan H2 dilakukan dua kali (dengan affinity off dan on) untuk menguji
apakah efek asimetri konsisten, bukan bergantung pada satu kondisi.

**Catatan isolasi.** H1 hanya membandingkan B dengan C dan D karena ketiganya
memakai affinity off; dengan begitu efek histeresis terisolasi. Membandingkan B
dengan E/F akan mengubah dua faktor sekaligus (histeresis dan affinity), sehingga
hasilnya dilaporkan sebagai **efek gabungan** untuk H4, bukan sebagai uji H1.

---

## 5. Urutan Run dan Counterbalancing

### 5.1 Prinsip

Urutan run tidak boleh sistematis. Jika kondisi C selalu diuji pagi dan F selalu
malam, efek jam sibuk bercampur dengan efek perlakuan.

### 5.2 Rancangan urutan

- Gunakan **Latin square** 7×7 untuk tujuh kondisi (A–G).
- Setiap blok (satu siklus) memuat setiap kondisi satu kali.
- Ulangi 3–4 blok dengan rotasi berbeda.
- Di dalam blok, urutan hari diacak terkontrol (*balanced Latin square*).
- Blok dicatat dengan tanggal, cuaca, dan jam.

### 5.3 Washout

Antar-kondisi diberi jeda minimal **10 menit** untuk menghapus state conntrack
dan antrean. Untuk transisi yang mengubah mode affinity, lakukan:

1. hentikan controller,
2. pulihkan konfigurasi awal,
3. tunggu conntrack *idle timeout* atau flush terkontrol,
4. verifikasi tidak ada aturan tersisa,
5. mulai kondisi berikutnya.

### 5.4 Blok waktu

Setiap kondisi diuji pada minimal dua jendela:

- **jam sibuk** (19.00–23.00),
- **jam rendah** (01.00–05.00).

Tujuannya agar efek tidak bergantung pada satu pola beban.

---

## 6. Desain Staging

| Elemen | Rencana |
|---|---|
| Emulator | `tc netem` pada dua virtual link |
| Trace | Rekaman metrik lapangan (RTT, loss, throughput) |
| Adapter | `MockAdapter` untuk uji kontrak |
| Skenario | A–G, masing-masing 20 replay |
| Variasi | Trace bersih, berderau, transien 15 detik, degradasi lambat |
| Luaran | Dataset staging + kurva trade-off |

Staging dipakai untuk:

1. menguji mekanisme RST sebelum menyentuh produksi,
2. mengkalibrasi parameter,
3. menguji aliasing $T_s$,
4. mereplikasi kondisi yang jarang muncul di lapangan.

---

## 7. Desain Lapangan

| Elemen | Rencana |
|---|---|
| Durasi kampanye | 6 minggu |
| Cakupan | 7 kondisi, masing-masing ≥ 3 hari lapangan |
| Jendela | 2 jendela per hari (sibuk dan rendah) |
| Target episode | 30 per kondisi (lapangan + staging) |
| Notifikasi | Pemberitahuan ke pelanggan sebelum kampanye |
| Jam berisiko | Perubahan besar hanya pada jam rendah |

Jika episode lapangan kurang dari target, kekurangan ditutup dengan *replay*
staging. Sumber data dicatat dan dianalisis terpisah; tidak dicampur tanpa
variabel `source`.

---

## 8. Ukuran Sampel

| Tahap | Unit | Target | Catatan |
|---|---|---:|---|
| Staging | Episode | 20 per kondisi | Kondisi terkendali |
| Lapangan | Episode | ≥ 10 per kondisi | Validitas eksternal |
| Total | Episode | 30 per kondisi | 7 kondisi ≈ 210 episode |

Untuk uji dua sisi $\alpha=0{,}05$, *power* 0,80, dan $d=0{,}5$, dibutuhkan
sekitar 34 per kelompok. Target 30–40 adalah kompromi; *power* final dihitung
setelah pilot dengan mempertimbangkan ICC dan korelasi dalam blok.

---

## 9. Variabel dan Data yang Dicatat

| Kategori | Variabel |
|---|---|
| Manipulasi | kondisi, mode histeresis, $k_{up}$, affinity |
| Link | RTT, jitter, loss, throughput, goodput, utilisasi |
| Keputusan | $Q_i$, state, rasio target, bucket, rule change |
| Sesi | RST flow, RST packet, retransmisi, flow count |
| Lingkungan | cuaca, curah hujan, jam, suhu, daya |
| Operasional | versi firmware, paket ISP, intervensi operator |

---

## 10. Ancaman Validitas dan Mitigasi

| Ancaman | Dampak | Mitigasi |
|---|---|---|
| Cuaca antar-run | Confounder utama | Blok, acak, catat curah hujan |
| Jam sibuk | Beban tidak setara | Dua jendela per kondisi |
| Carryover conntrack | Efek sisa | Washout 10 menit + verifikasi |
| Drift ISP/firmware | Baseline berubah | Catat versi, uji ulang baseline |
| Episode sedikit | CI lebar | Replay staging + laporkan presisi |
| Intervensi operator | Bias | Log intervensi, otomatisasi run |
| Efek probe | Beban tambahan | Probe frekuensi rendah, kalibrasi |
| Controller gagal | Data hilang/risiko | Fail-static, buffer lokal, watchdog |

---

## 11. Luaran Tahap 4

1. Bab III yang memuat desain, formalisasi, instrumen, dan analisis.
2. Dataset staging dan lapangan dengan skema tetap.
3. Protokol run yang dapat dijalankan operator lain.
4. Tabel parameter dan tabel skenario yang siap masuk lampiran.
5. Berkas konfigurasi baseline A dan G yang terdokumentasi.
