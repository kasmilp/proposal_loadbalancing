# Tahap 4 — Instrumen dan Prosedur Pengukuran

**Dokumen:** `03_Instrumen_dan_Prosedur_Pengukuran.md`
**Status:** Draf kerja Tahap 4
**Fungsi:** Memastikan setiap metrik diukur dengan alat, titik ukur, dan interval
yang sama pada semua kondisi.

---

## 1. Prinsip

1. **Satu metrik, satu definisi operasional.** Definisi tidak berubah antar-kondisi.
2. **Ukur di luar router.** RST dan goodput tidak boleh disimpulkan dari counter router.
3. **Pisahkan vantage point.** Probe per WAN, capture di LAN, telemetri dari dish.
4. **Kalibrasi sebelum kampanye.** Pilot 24–48 jam untuk mencocokkan SNMP, probe,
   dan capture.
5. **Jangan menangkap payload.** Hanya header dan counter.

---

## 2. Tabel Instrumen

| Metrik | Definisi | Alat | Vantage point | Interval |
|---|---|---|---|---|
| RTT | *Round-trip time* probe | ICMP/TCP probe | Controller, per WAN | 1 s |
| Jitter | Variasi RTT (RFC 3550) | Probe | Controller, per WAN | 1 s (dihitung 30 s) |
| Loss | Rasio probe hilang | Probe | Controller, per WAN | 1 s (agregat 30 s) |
| Throughput | Laju uji kapasitas | `iperf3` / HTTP | Endpoint uji | 10 menit |
| Goodput | Byte aplikasi / durasi | `iperf3`, HTTP | Endpoint uji | Per episode |
| Utilisasi | Pemakaian link | SNMP `ifHCInOctets`/`ifHCOutOctets` | Router | 10 s |
| Error/discard | Indikator tambahan | SNMP `ifInErrors`, `ifOutDiscards` | Router | 10 s |
| Skor $Q_i$ | SAW | Algorithm Core | Controller | 1 s |
| State | STABLE/DEGRADED | Algorithm Core | Controller | 1 s |
| Bucket | Alokasi PCC | Controller + RouterOS | Controller | Per perubahan |
| Rule change | Perubahan bucket efektif | Log controller | Controller | Per kejadian |
| RST packet | Paket TCP RST | `tcpdump`/Wireshark | LAN capture | Kontinu |
| RST flow | Aliran dengan ≥1 RST | Analisis capture | LAN capture | Per episode |
| Retransmisi | Paket TCP retransmit | `tcpdump`/Wireshark | LAN capture | Kontinu |
| Starlink telemetry | Latency, drop, obstruction | gRPC dish (jika tersedia) | Dish | 1 s |
| Cuaca | Curah hujan | Stasiun cuaca/BMKG | Lokasi | 10 menit |

---

## 3. Titik Ukur

```
        ┌──────────────┐
        │  Controller  │  probe per WAN, log keputusan, collector
        └──────┬───────┘
               │ manajemen
        ┌──────┴───────┐
        │   Router     │  SNMP, conntrack, mangle
        └──┬────────┬──┘
           │        │
        WAN1 FO   WAN2 LEO
           │        │
        ┌──┴────────┴──┐
        │  LAN capture │  tcpdump: RST, retransmisi
        └──────┬───────┘
               │
          Pelanggan / endpoint uji
```

**Aturan routing probe:** probe ke WAN1 dan WAN2 harus memakai *routing mark*
eksplisit agar tidak mengikuti jalur default. Tanpa ini, probe hanya mengukur
jalur yang sedang aktif.

---

## 4. Prosedur per Metrik

### 4.1 RTT, jitter, loss

1. Kirim probe 64 byte setiap 1 detik ke target tetap di tiap WAN.
2. Catat `timestamp, link, seq, rtt_ms, success`.
3. Hitung loss per 30 sampel.
4. Hitung jitter dengan rumus RFC 3550:

$$J = J + \frac{|D_{i-1,i}| - J}{16}$$

5. Simpan nilai mentah; agregasi dilakukan saat analisis, bukan saat pengukuran.

### 4.2 Throughput dan goodput

1. Jalankan `iperf3` 10 detik setiap 10 menit per WAN (bukan bersamaan, agar tidak
   saling mengganggu).
2. Catat byte aplikasi, bukan hanya byte TCP.
3. Goodput episode = total byte aplikasi / durasi episode.
4. Bedakan *carried*, *achievable*, dan *goodput*; hanya goodput dipakai untuk H3b.

### 4.3 RST dan integritas sesi

1. Capture di LAN dengan `tcpdump -s 96` (header saja).
2. Filter TCP; hitung paket dengan flag RST.
3. Identifikasi aliran dengan hash 5-tuple.
4. Hitung:

$$\text{RST}_{packet}\% = \frac{\#\text{RST}}{\#\text{TCP}} \times 100\%, \qquad
\text{RST}_{flow} = \frac{\#\text{flow dengan RST}}{\#\text{flow}} \in [0,1]$$

Untuk pelaporan digunakan $\text{RST}_{flow}\% = 100 \times \text{RST}_{flow}$;
untuk SIWG digunakan proporsi.

5. Catat RST yang terjadi dalam 30 detik setelah *rule change* sebagai
   "RST terkait perubahan" untuk analisis tambahan.

### 4.4 Starlink telemetry

1. Jika gRPC dish tersedia: ambil latency, drop rate, obstruction, uptime.
2. Jika tidak: gunakan probe aktif dan catat sebagai keterbatasan.
3. Jangan mengandalkan aplikasi konsumen untuk data riset.

### 4.5 Cuaca

1. Catat curah hujan per 10 menit dari stasiun terdekat.
2. Simpan sebagai kovariat, bukan sebagai variabel perlakuan.

---

## 5. Kalibrasi Pilot 24–48 Jam

| Langkah | Kriteria lulus |
|---|---|
| Bandingkan SNMP vs probe vs capture | Selisih throughput < 10% |
| Uji probe per WAN | Setiap probe benar-benar melewati WAN yang dituju |
| Uji RST detection | RST buatan (`tc`/reset terkontrol) terdeteksi |
| Uji timestamp | Selisih jam antar-perangkat < 100 ms (NTP) |
| Uji beban probe | Penurunan throughput < 2% |
| Uji fail-static | Controller dimatikan → konfigurasi terakhir tetap berlaku |
| Uji rollback | Konfigurasi kembali ke checkpoint dalam < 60 detik |

Jika salah satu gagal, kampanye tidak dimulai.

---

## 6. Perhitungan SIWG

Untuk setiap episode $e$:

$$G_{eff}(e) = \frac{\text{byte aplikasi}(e)}{\text{durasi}(e)}$$

$$\text{RST}_{flow}(e) = \frac{\#\text{flow terganggu}(e)}{\#\text{flow}(e)} \in [0,1]$$

$$\text{SIWG}(e) = G_{eff}(e) \times \left(1 - \lambda \cdot \text{RST}_{flow}(e)\right)$$

dengan $\lambda = 1$ sebagai primer. Analisis sensitivitas:
$\lambda \in \{0{,}25;\ 0{,}5;\ 1{,}0\}$. Untuk pelaporan, gunakan
$\text{RST}_{flow}\%$; untuk SIWG, gunakan proporsi.

**Aturan:** episode tanpa aliran TCP (mis. hanya UDP) dihitung terpisah dan
dikeluarkan dari H3a, tetapi tetap masuk H3b.

---

## 7. Skema Data

Satu baris per sampel skoring:

| Kolom | Tipe | Keterangan |
|---|---|---|
| `timestamp` | ISO 8601 | NTP tersinkron |
| `scenario` | string | A–G |
| `run_id` | string | blok + urutan |
| `link_id` | string | FO/LEO |
| `rtt_ms` | float | — |
| `jitter_ms` | float | — |
| `loss_pct` | float | — |
| `throughput_mbps` | float | — |
| `goodput_mbps` | float | — |
| `utilization` | float | 0–1 |
| `q_score` | float | 0–1 |
| `state` | string | STABLE/DEGRADED |
| `ratio_target` | float | — |
| `bucket` | int | — |
| `rule_change` | bool | — |
| `rst_count` | int | kumulatif per interval |
| `tcp_pkt_count` | int | — |
| `flow_count` | int | — |
| `disrupted_flows` | int | — |
| `rain_mm` | float | — |
| `source` | string | staging/field |
| `notes` | string | intervensi |

Satu baris per episode:

| Kolom | Tipe |
|---|---|
| `episode_id` | string |
| `scenario` | string |
| `start`, `end` | timestamp |
| `duration_s` | float |
| `flaps` | int |
| `recovery_s` | float |
| `goodput_mbps` | float |
| `latency_p95_ms` | float |
| `rst_flow_pct` | float |
| `siwg` | float |
| `source` | string |

---

## 8. Kontrol Mutu

| Pemeriksaan | Frekuensi | Tindakan jika gagal |
|---|---|---|
| Sinkronisasi waktu | Harian | Sinkronkan NTP, tandai data |
| Kelengkapan sampel | Harian | Isi celah atau tandai |
| Probe per WAN | Awal run | Perbaiki routing mark |
| Capture RST | Awal run | Uji RST terkontrol |
| Disk dan buffer | Harian | Bersihkan, arsipkan |
| Checksum berkas | Akhir run | Ulangi ekspor |
| Log intervensi | Setiap kejadian | Catat penyebab dan durasi |

---

## 9. Jebakan Pengukuran yang Harus Dihindari

1. **Mengukur throughput router, bukan goodput pengguna.** Hasil bisa tampak baik
   meskipun aplikasi menderita.
2. **Probe mengikuti jalur default.** Semua probe tampak mengukur WAN1.
3. **RST disimpulkan dari counter router.** Counter tidak menangkap RST ujung-ke-ujung.
4. **Throughput probe terlalu sering.** Mengganggu pengukuran dan kuota.
5. **Menggabungkan data staging dan lapangan tanpa penanda.** Confounder tidak
   dapat dipisahkan.
6. **Menganggap conntrack langsung terhapus saat aturan berubah.** Harus diuji.
7. **Mengabaikan jam sibuk.** Beban tidak setara antar-run.
