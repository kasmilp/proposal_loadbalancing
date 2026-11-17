# 03 — Spesifikasi Parameter

**Status:** Draf kerja
**Fungsi:** Mendefinisikan parameter teknis yang relevan dan terukur untuk indeks
kualitas link, lengkap dengan satuan, rentang acuan, dan pengaruhnya.

**Sumber batas acuan [FAKTA]:**
- **TIPHON** — ETSI TR 101 329 V2.1.1 (1999). Nilai diekstrak langsung dari berkas
  `00_Arsip_Proposal_SPA-HSM/jurnal_terkait/01_QoS_dan_Pengukuran/TIPHON.pdf`.
- **ITU-T Y.1541 / G.114** — dari register referensi arsip; **angka perlu diverifikasi
  ke teks standar** sebelum disitasi resmi.
- **Starlink** — Ullah et al. (2025), hlm. 5; Garcia et al. (2025); Hammer et al.
  (2024); Mohan et al. (2024).

---

## 1. Tabel Batas Acuan (TIPHON) **[FAKTA]**

**Tabel 1a — Kelas QoS end-to-end TIPHON (ETSI TR 101 329, hal. 25)**

| | 4 (Best) | 3 (High) | 2 (Medium) | 1 (Low) |
|---|---|---|---|---|
| End-to-end delay | < 150 ms | < 250 ms | < 350 ms | < 450 ms |
| Kualitas tutur (setara kodek) | > G.711 | ≥ G.726 @32 kbit/s | ≥ GSM-FR | — |

*Catatan sumber: "All delay parameters represent an upper bound for 90% of the
connections".*

**Tabel 3 — Level degradasi jaringan (ETSI TR 101 329, hal. 26)**

| Kategori | Packet loss | Peak jitter |
|---|---|---|
| Perfect | 0% | 0 ms |
| Good | 3% | 75 ms |
| Medium | 15% | 125 ms |
| Poor | 25% | 225 ms |

*Nilai bersifat sementara ("provisional") menurut standar.*

---

## 2. Tabel Parameter **[FAKTA + USULAN]**

| # | Parameter | Definisi | Satuan | Rentang / nilai acuan | Jenis | Pengaruh pada kualitas koneksi | Instrumen |
|---|---|---|---|---|---|---|---|
| P1 | **One-way delay (OWD)** | Waktu tempuh paket satu arah | ms | TIPHON: <150/<250/<350/<450 ms (Kelas 4/3/2/1) | Cost | Menentukan kelayakan aplikasi interaktif (VoIP/video); >150 ms mulai terasa | Probe `/ping interface=` di router (ICMP) — `collector.py` |
| P2 | **RTT** | Round-trip time | ms | ≈ 2× OWD | Cost | Menggerakkan TCP throughput melalui BDP | ping / probe |
| P3 | **Jitter / IPDV** | Variasi delay antar-paket | ms | TIPHON degradasi: 0 / ≤75 / ≤125 / ≤225 ms | Cost | Merusak buffer real-time; memicu retransmisi | RFC 3550 (estimasi jitter) |
| P4 | **Packet loss ratio (IPLR)** | Rasio paket gagal sampai | % | TIPHON degradasi: 0/3/15/25%. Y.1541: 1×10⁻³ (Kelas 0–4), 1×10⁻⁵ (Kelas 6–7) | Cost | Menurunkan goodput; memicu congestion control | Probe `packet_loss` + delta counter interface |
| P5 | **Throughput / goodput** | Laju data efektif berhasil | Mbps | Starlink: DL **137 → 90,2** saat hujan; UL **20,9 → 10,5** (Ullah et al., 2025, hlm. 5) | **Benefit** | Kapasitas nyata; *carried ≠ achievable* | Delta counter interface (kolektor) + iperf3 |
| P6 | **Available bandwidth / headroom** | Sisa kapasitas yang dapat dipakai | Mbps | `max(0; 0,9·C − L)` (margin 10%) | Benefit | Menentukan apakah link dapat menampung koneksi baru | Turunan P5 + P7 |
| P7 | **Utilisasi link** | Pangsa kapasitas terpakai | % | 0–100% | Cost | Mencegah *overload*; dasar batas share 15–85% | Delta counter interface (kolektor) |
| P8 | **Frekuensi flapping** | Laju perubahan aturan yang berbalik arah | flap/jam | jendela W = 5 menit (uji sensitivitas 1/5/15) | Cost (output) | Metrik hasil keputusan, **bukan** input indeks | Log aturan/controller |

---

## 3. Parameter Turunan (terkait keputusan) **[USULAN]**

| Kode | Parameter | Rumus / Definisi | Peran |
|---|---|---|---|
| P9 | Pangsa beban efektif | $L_i = (S_i + F_i)/\sum_k(S_k+F_k)$ | Melihat alokasi nyata |
| P10 | *Effective Load Skew* (ELS) | $\tfrac12 \sum_i \lvert L_i - T_i \rvert$ | 0 = alokasi sesuai target |
| P11 | *Time-to-rebalance* | Waktu hingga ELS < ambang setelah degradasi | Kecepatan pemulihan |
| P12 | RST *flow rate* | Rasio koneksi TCP baru yang menerima ≥1 RST | Biaya pemutusan sesi |

*(P9–P12 hanya dipakai bila lingkup mencakup kebijakan alokasi; lihat `08_Rancangan_Eksperimen.md`.)*

---

## 4. Catatan Penggunaan **[ANALISIS]**

1. **Jangan masukkan P8 ke dalam indeks.** Flapping adalah *hasil* keputusan;
   memasukkannya sebagai kriteria menimbulkan *double counting*.
2. **Bedakan throughput jenis:** *carried throughput* (terukur di antarmuka) vs
   *achievable throughput*/*headroom*. Untuk skor kualitas, pakai **headroom/achievable**,
   bukan carried (catatan ini pernah muncul di dokumen arsip `Cakupan_Perubahan`).
3. **Empat kriteria inti** untuk indeks: **P1 (delay), P3 (jitter), P4 (loss),
   P5/P6 (throughput/headroom)**. **P7** dapat dipakai sebagai kriteria tambahan atau
   pembatas.
4. **Arah cost/benefit** menentukan rumus normalisasi (lihat `04_Analisis_Bobot_SAW.md`).
5. **Indeks dihitung per link** $i \in \{\text{ISP-A (ether1)},\ \text{ISP-B (ether2)},\ \text{ISP-C (ether3)}\}$
   (topologi tri-link, `00_README.md` §6). Normalisasi, bobot, dan gerbang diterapkan
   **per link**; korelasi antar-LEO dilaporkan sebagai kovariat, bukan diabaikan.

---

## 5. Temuan Starlink sebagai Konteks Transien **[FAKTA]**

| Temuan | Nilai | Sumber |
|---|---|---|
| Siklus rekonfigurasi antar-satelit | **≈15 detik** | Garcia et al. (2025) |
| Pola penurunan throughput pada batas interval | 15 detik | Hammer et al. (2024); Mohan et al. (2024) |
| Penurunan throughput saat hujan (downlink) | 137 → 90,2 Mbps | Ullah et al. (2025), hlm. 5 |
| Penurunan throughput saat hujan (uplink) | 20,9 → 10,5 Mbps | Ullah et al. (2025), hlm. 5 |
| Variabilitas & outage | lebih tinggi dari terestrial | Ma et al. (2023); Mohan et al. (2024) |

**[ANALISIS]** Nilai 15 detik adalah *skala waktu transien* yang harus diserap desain
indeks/gerbang — bukan klaim bahwa Starlink "lebih buruk" secara umum. Istilah
*"upper bound"* pada naskah lama sebaiknya diganti **"kasus stres"** agar tidak
disalahpahami. Karena topologi memakai **dua Starlink**, transien keduanya dapat
berkorelasi (arkip mencatat 0,68–0,70) — lihat `00_README.md` §6.
