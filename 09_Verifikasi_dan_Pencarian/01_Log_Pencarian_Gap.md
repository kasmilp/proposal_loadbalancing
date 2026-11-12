# Log Pencarian Gap (P-01)

**Tanggal pencarian:** 12 November 2026
**Basis data:** OpenAlex API (`title_and_abstract.search`)
**Batasan:** publikasi 2015–2026, pencarian pada judul dan abstrak
**Tujuan:** Menguji klaim "belum ditemukan studi" pada Tahap 1.

---

## 1. Ringkasan Eksekutif

| Temuan | Bukti |
|---|---|
| PCC + histeresis/dwell/skor kualitas | **0 hit** |
| PCC + sesi/conntrack/connection tracking | **2 hit**, keduanya lokal dan tidak mengukur preservasi sesi |
| PCC + adaptive/dynamic/quality | 34 hit, dominan implementasi statis |
| Starlink + handover/throughput/OWD | 285 hit, dominan pengukuran, bukan mekanisme alokasi |
| MPTCP + load balancing/multihoming | 137 hit, relevan untuk P-03 |
| SD-WAN + multipath/steering/LB | 75 hit, dominan arsitektur/DRL |

**Kesimpulan sementara:** irisan **PCC × histeresis/dwell** kosong, dan irisan
**PCC × preservasi sesi terukur** hanya berisi dua studi lokal yang tidak mengukur
RST. Gap Tahap 1 **terverifikasi secara tentatif** pada OpenAlex.

---

## 2. Tabel Pencarian

| Kode | Query | Hits | Hasil relevan | Catatan saring |
|---|---|---:|---|---|
| S1f | `"per connection classifier" AND (adaptive OR dynamic OR quality)` | 34 | Implementasi PCC lokal; tidak ada skor kualitas adaptif | Dominan jurnal nasional |
| S1g | `"per connection classifier" AND (hysteresis OR dwell OR "quality score")` | **0** | — | **Irisan kosong** |
| S1h | `"per connection classifier" AND (session OR conntrack OR "connection tracking")` | 2 | PCC RB1100 (2023); PBR + failover (2026) | Tidak mengukur RST/preservasi |
| S2f | `("load balancing" OR "network selection") AND (hysteresis OR dwell OR threshold)` | 1.111 | Handover LTE, threshold SDN, cloud LB | Tidak ada PCC + FO–LEO |
| S3f | `Starlink AND (handover OR throughput OR "one-way delay")` | 285 | Ma 2023; Garcia 2025; StarTCP 2024; Vivisecting 2025 | Pengukuran/transport, bukan alokasi PCC |
| S4f | `(MPTCP OR "session continuity" OR conntrack) AND (multihoming OR failover OR "load balancing")` | 189 | MPTCP load balancer (2016, 2017) | Load balancer server, bukan PCC |
| S4g | `MPTCP AND ("load balancing" OR multihoming)` | 137 | Inventory MPTCP scheduler (2024); optimal scheduler (2017) | Kandidat P-03 |
| S5f | `(MCDM OR SAW) AND "network selection"` | 82 | Modified-SAW untuk seleksi jaringan | Seleksi, bukan proporsi PCC |
| S6f | `"SD-WAN" AND (multipath OR "traffic steering" OR "load balancing")` | 75 | SD-WAN LB overview (2020); DRL steering (2025) | Arsitektur, bukan PCC/sesi |
| S7f | `(Starlink OR LEO) AND ("rain fade" OR rain OR weather) AND (throughput OR latency)` | 132 | Ullah 2025; WetLinks 2024; tropical rain 2025 | Deskriptif |

**Catatan metodologis:** query memakai sintaks boolean OpenAlex. Hit count adalah
jumlah karya yang cocok pada judul/abstrak, bukan jumlah yang lolos penyaringan
teks penuh.

---

## 3. Interpretasi

### 3.1 Irisan yang kosong

Query S1g menghasilkan **0 hit**. Artinya, pada korpus OpenAlex 2015–2026, tidak
ada karya yang secara eksplisit menggabungkan PCC dengan histeresis, *dwell*, atau
skor kualitas pada judul/abstrak. Ini mendukung klaim bahwa **aturan dwell
sadar-transien untuk PCC belum tersedia**.

### 3.2 Irisan yang hampir kosong

Query S1h menghasilkan 2 hit, keduanya:
- implementasi PCC pada MikroTik RB1100 (2023),
- analisis PBR dan failover pada dual-WAN (2026).

Tidak ada yang mengukur RST atau membandingkan perlakuan dengan/tanpa preservasi
sesi. Ini mendukung **G-E1**: klaim *session-preserving* belum diuji secara
kuantitatif.

### 3.3 Bidang yang ramai tetapi berbeda

- **Starlink/LEO** (S3f, S7f): banyak pengukuran, sedikit mekanisme alokasi.
- **MCDM/SAW** (S5f): banyak seleksi jaringan, bukan proporsi PCC.
- **SD-WAN/MPTCP** (S4g, S6f): banyak arsitektur dan load balancer server, bukan
  PCC pada router SOHO dengan preservasi conntrack.

---

## 4. Keterbatasan Pencarian

1. Hanya OpenAlex; Scopus, IEEE Xplore, dan ACM DL belum dijalankan manual.
2. Hanya judul dan abstrak; studi yang membahas topik ini di badan teks bisa
   terlewat.
3. Sintaks boolean dapat mengecualikan sinonim yang tidak dicantumkan.
4. Hit count besar (S2f, S4f) belum disaring teks penuh.
5. Tidak ada pencarian bahasa Indonesia yang sistematis.

**Konsekuensi:** klaim harus ditulis sebagai "berdasarkan pencarian pada OpenAlex
... belum ditemukan", bukan "belum ada penelitian di dunia".

---

## 5. Kandidat Referensi Baru

### 5.1 P-02 — PCC/adaptive load balancing internasional

| Kandidat | Venue/tahun | DOI | Peran |
|---|---|---|---|
| Multiple-level threshold load balancing in distributed SDN controllers | Computer Networks, 2021 | 10.1016/j.comnet.2021.108369 | Threshold/LB adaptif |
| An Overview of SD-WAN Load Balancing for WAN Connections | IEEE ICECA, 2020 | 10.1109/iceca49313.2020.9297574 | Arsitektur SD-WAN |
| Dynamic Load Balancing in SD-WAN with Deep Reinforcement Learning | IEEE Globecom, 2025 | 10.1109/globecom59602.2025.11432107 | Adaptive LB |
| A MARL Approach to Employ Intelligent Traffic Steering in SD-WAN | IEEE CSCN, 2025 | 10.1109/cscn67557.2025.11230744 | Traffic steering |

### 5.2 P-03 — MPTCP/kontinuitas sesi

| Kandidat | Venue/tahun | DOI | Peran |
|---|---|---|---|
| Making multipath TCP friendlier to load balancers and anycast | IEEE ICNP, 2017 | 10.1109/icnp.2017.8117545 | MPTCP + load balancer |
| Towards a Multipath TCP Aware Load Balancer | ACM ANRW, 2016 | 10.1145/2959424.2959426 | MPTCP + LB |
| Inventory of Load Balancing Parameters in MPTCP Schedulers | Computer Networks, 2024 | 10.1016/j.comnet.2024.110880 | Scheduler MPTCP |
| Optimal load balancing scheduler for MPTCP-based bandwidth aggregation | Computer Communications, 2017 | 10.1016/j.comcom.2017.08.018 | Multihoming |
| StarTCP: Handover-aware Transport Protocol for Starlink | ACM APNet, 2024 | 10.1145/3663408.3665803 | Handover LEO + transport |

**Status:** kandidat, **belum disitasi**. Baca teks penuh dan verifikasi klaim
sebelum memasukkannya ke Bab II.

**Pembaruan 12-11-2026:** 7 dari 9 kandidat sudah dimasukkan ke Bab II.
- P-02: Shahid et al. (2020), Cruvellier et al. (2025), Giacometti et al. (2025),
  Rajagopalan (2020).
- P-03: Liénardy & Donnet (2016), Duchene & Bonaventure (2017), Jiang et al.
  (2024), Naimi et al. (2024).
- Tetap kandidat: Mokhtar et al. (2021); Choi et al. (2017).

**Catatan versi:** Ullah et al. (2025) yang semula berupa arXiv telah terbit di
IEEE VTC2025-Spring dengan DOI `10.1109/vtc2025-spring65109.2025.11174614`.
Register sudah diperbarui ke versi terbit.

---

## 6. Tindakan Lanjutan

- [ ] Jalankan query yang sama di Scopus dan IEEE Xplore, catat hit.
- [ ] Saring 10 kandidat P-02/P-03 pada teks penuh.
- [ ] Tambahkan 3–5 referensi P-02 dan 4 referensi P-03 ke register.
- [ ] Perbarui §6 peta gap dengan hasil ini.
- [ ] Tulis klaim gap dengan frasa "berdasarkan pencarian pada OpenAlex".
