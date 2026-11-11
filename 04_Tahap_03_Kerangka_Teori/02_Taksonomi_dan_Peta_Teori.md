# Tahap 3 — Taksonomi dan Peta Teori

**Dokumen:** `02_Taksonomi_dan_Peta_Teori.md`
**Fungsi:** Menunjukkan asal setiap teori, perannya, dan batas penggunaannya.
**Guna:** Menjawab pertanyaan penguji: "Teori apa yang Anda pakai, dan mana yang
benar-benar baru?"

---

## 1. Empat Lapis Teori

| Lapis | Isi | Sifat | Sumber utama |
|---|---|---|---|
| **L1 — Fondasi** | QoS, pengukuran jaringan, karakteristik FO/LEO, TCP/conntrack | Diterima dari literatur | ETSI, ITU-T, RFC, Ma et al. (2023), Mohan et al. (2024) |
| **L2 — Metode** | PCC, MCDM/SAW, EWMA, histeresis | Diterima dan diadaptasi | MikroTik, Vafaei et al. (2021), Roberts (1959), Tournaire et al. (2023) |
| **L3 — Integrasi** | SPA-HSM, aturan dwell sadar-transien, pemetaan skor→bucket, SIWG | **Diformulasikan dalam penelitian ini** | Proposisi 1–2, definisi SIWG |
| **L4 — Evaluasi** | Ablasi faktorial, statistik campuran, effect size | Diterima dari metodologi | Cohen (1988), Holm (1979), Liang & Zeger (1986) |

**Aturan atribusi:** L1 dan L2 tidak diklaim sebagai kebaruan. L3 adalah klaim
utama. L4 adalah alat, bukan kontribusi.

---

## 2. Inventaris Teori

| Teori/konsep | Sumber | Peran dalam penelitian | Status |
|---|---|---|---|
| QoS empat parameter | Nanang et al. (2024); ETSI (2000) | Mendefinisikan metrik masukan | Diterima |
| Batas acuan QoS | ITU-T G.114; ITU-T Y.1541; TIPHON | Menetapkan $x^{min}, x^{max}$ normalisasi | Diterima |
| Pengukuran IP | RFC 2330/2544/3550 | Prosedur dan rumus metrik | Diterima |
| Dinamika LEO | Ma et al. (2023); Mohan et al. (2024); Garcia et al. (2025) | Menjelaskan transien dan variabilitas | Diterima |
| *Rain fade* | Ullah et al. (2025); Boeckenholt et al. (2024) | Menjelaskan degradasi lambat | Diterima |
| PCC dan conntrack | MikroTik (n.d.); Kumar & Golash (2009) | Mekanisme aktuator | Diterima |
| MCDM/SAW | Wang & Kuo (2013); Vafaei et al. (2021) | Skor kualitas multi-kriteria | Diterima |
| EWMA | Roberts (1959) | Penghalusan deret waktu | Diterima |
| Histeresis dua ambang | Tournaire et al. (2023); Alhabo et al. (2017) | Peredam osilasi keputusan | Diadaptasi |
| *Adapter pattern* | Gamma et al. (1994) | Pemisahan inti–platform | Diterima |
| *Offloading controller* | Ali et al. (2025); Wang & Kuo (2013) | Arsitektur kontrol eksternal | Diterima |
| **Aturan dwell sadar-transien** | **Proposisi 1 penelitian ini** | **Menurunkan $k_{down}$ dari $T_{tr}$** | **Baru (L3)** |
| **Pemetaan skor→bucket** | **Formalisasi penelitian ini** | **Menjembatani kontinu–diskret** | **Baru (L3)** |
| **SIWG** | **Definisi penelitian ini** | **Mengukur trade-off stabilitas–kontinuitas** | **Baru (L3)** |
| Statistik campuran | Liang & Zeger (1986); McCullagh & Nelder (1989) | Analisis data berulang/cacat | Diterima |
| *Effect size* dan koreksi | Cohen (1988); Holm (1979) | Pelaporan hasil | Diterima |

---

## 3. Konstruk, Variabel, dan Metrik

| Konstruk | Definisi konseptual | Variabel operasional | Metrik | Hipotesis |
|---|---|---|---|---|
| Kualitas link | Kondisi agregat link menurut QoS | $Q_i(t) \in [0,1]$ | Skor SAW | RQ1 |
| Derau metrik | Variasi cepat yang tidak bertahan | $\alpha$, $N_{eff}$ | Varians skor | RQ1 |
| Stabilitas keputusan | Kecenderungan keputusan berbalik arah | Mode histeresis, $k_{down}, k_{up}$ | Flapping rate | H1, H2 |
| Kecepatan pemulihan | Waktu kembali ke state stabil | $k_{up}$, $\theta_{high}$ | Recovery latency p95 | H1, H2 |
| Kontinuitas sesi | Kemampuan mempertahankan sesi berjalan | `AFFINITY_LOCK`, conntrack | RST flow/packet | H3a |
| Kinerja agregat | Laju dan kualitas data efektif | Rasio bucket | Goodput, latency p95 | H3b |
| Trade-off gabungan | Kinerja setelah dikurangi biaya gangguan sesi | $\lambda$, SIWG | SIWG | H4 |
| Portabilitas inti | Kemandirian logika dari platform | Kontrak antarmuka | % keputusan identik | H5 |

---

## 4. Peta Kausal

```
                 ┌──────────────────────────────┐
                 │  Kondisi fisik & operasional │
                 │  FO: kongesti/oversubscription│
                 │  LEO: cuaca + handover        │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │  Metrik QoS mentah            │
                 │  throughput, delay, jitter,   │
                 │  loss                         │
                 └──────────────┬───────────────┘
                                │ sampling Ts
                                ▼
                 ┌──────────────────────────────┐
                 │  EWMA (α)                     │
                 └──────────────┬───────────────┘
                                ▼
                 ┌──────────────────────────────┐
                 │  SAW (w, batas tetap)         │
                 │  Q_i(t)                       │
                 └──────────────┬───────────────┘
                                ▼
                 ┌──────────────────────────────┐
                 │  Histeresis (θ, k_down, k_up) │
                 │  state s_i(t)                 │
                 └──────────────┬───────────────┘
                                ▼
                 ┌──────────────────────────────┐
                 │  Rasio W_i(t) → bucket b_i(t) │
                 └──────────────┬───────────────┘
                                ▼
                 ┌──────────────────────────────┐
                 │  Aturan PCC (new flows)       │
                 └───────┬──────────────┬────────┘
                         │              │
                         ▼              ▼
                 ┌──────────────┐ ┌──────────────────┐
                 │  Flapping    │ │  Sesi berjalan    │
                 │  (aturan)    │ │  (conntrack/RST)  │
                 └───────┬──────┘ └────────┬─────────┘
                         └────────┬────────┘
                                  ▼
                 ┌──────────────────────────────┐
                 │  Goodput, latency p95, RST    │
                 └──────────────┬───────────────┘
                                ▼
                 ┌──────────────────────────────┐
                 │  SIWG                         │
                 └──────────────────────────────┘
```

**Pembacaan:** setiap kotak adalah konstruk yang diukur; setiap panah adalah
mekanisme yang diuji. Hipotesis H1–H2 menguji panah histeresis→flapping/recovery;
H3a menguji panah aturan→sesi; H3b menguji panah agregat; H4 menguji keseluruhan;
H5 menguji kemandirian inti dari adapter.

---

## 5. Batas Teori

| Batas | Konsekuensi |
|---|---|
| Tidak ada pembuktian formal kestabilan *control loop* | Klaim stabilitas bersifat empiris, bukan analitis |
| Tidak ada model prediktif transien | Sistem reaktif, bukan prediktif (Opsi C di luar lingkup) |
| Tidak ada pembelajaran bobot | "Adaptif" hanya pada rasio (K-03) |
| Tidak ada QoE | Tidak mengklaim kepuasan pengguna |
| Hanya satu adapter nyata | Portabilitas terbatas pada kontrak yang diuji |
| Hanya dua ISP | Tidak mengklaim generalisasi multi-ISP |
| Asumsi independensi kriteria SAW | Diakui sebagai keterbatasan |

---

## 6. Yang Benar-Benar Baru

Jika penguji bertanya "mana yang baru?", jawabannya hanya tiga:

1. **Aturan dwell sadar-transien** — menghubungkan $T_s$, $T_{tr}$, dan $k_{down}$
   secara eksplisit (Proposisi 1).
2. **Formalisasi pemetaan skor kontinu ke bucket PCC diskret** — dengan jaminan
   $\sum b_i = N$ dan batas $b_{min}/b_{max}$.
3. **SIWG dan bukti ablasi** — mengukur trade-off stabilitas–kontinuitas dalam satu
   angka, dengan pemisahan kontribusi komponen.

Selebihnya adalah teori yang dipinjam, diadaptasi, atau diintegrasikan. Menyebut
hal ini secara terbuka memperkuat kredibilitas, bukan melemahkannya.
