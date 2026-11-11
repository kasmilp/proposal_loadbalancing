# Daftar Simbol dan Singkatan

**Dokumen:** `04_Daftar_Simbol_dan_Singkatan.md`
**Fungsi:** Lampiran awal untuk naskah proposal; memastikan notasi konsisten.

---

## 1. Simbol

| Simbol | Arti | Satuan/rentang |
|---|---|---|
| $i$ | Indeks link, $i \in \{1,2\}$ | — |
| $t$ | Waktu diskret, $t=kT_s$ | detik |
| $T_s$ | Interval sampling | 1 detik |
| $x_{ij}(t)$ | Metrik mentah kriteria $j$ pada link $i$ | sesuai metrik |
| $E_{ij}(t)$ | Nilai EWMA metrik $j$ | sesuai metrik |
| $r_{ij}(t)$ | Nilai ternormalisasi kriteria $j$ | $[0,1]$ |
| $w_j$ | Bobot kriteria $j$ | $\sum w_j=1$ |
| $Q_i(t)$ | Skor kualitas link $i$ | $[0,1]$ |
| $H_i(t)$ | Faktor *headroom* link $i$ | $[0,1]$ |
| $u_i(t)$ | Utilisasi link $i$ | $[0,1]$ |
| $W_i(t)$ | Proporsi target link $i$ | $[0,1]$ |
| $b_i(t)$ | Jumlah bucket link $i$ | integer |
| $N$ | Total bucket PCC | 20 |
| $b_{min}, b_{max}$ | Batas bucket | 3, 17 |
| $\theta_{low}$ | Ambang degradasi | 0,60 |
| $\theta_{high}$ | Ambang pemulihan | 0,80 |
| $k_{down}$ | *Dwell* degradasi | 20 sampel |
| $k_{up}$ | *Dwell* pemulihan | 20/60 sampel |
| $T_{max}$ | Interval evaluasi ulang paksa | 10 menit |
| $T_{tr}$ | Durasi transien dominan | ≈15 detik |
| $\alpha$ | Koefisien EWMA | 0,20 |
| $N_{eff}$ | *Effective window* EWMA | ≈9 sampel |
| $\lambda$ | Bobot biaya sesi pada SIWG | $[0,1]$ |
| $G_{eff}$ | *Goodput* efektif episode | Mbps |
| $\text{RST}_{flow}$ | Proporsi aliran TCP terganggu | $[0,1]$ |
| $\text{RST}_{flow}\%$ | Persentase aliran terganggu | $[0,100]$ |
| SIWG | *Session-Impact-Weighted Goodput* | Mbps setara |
| $R_{max}$ | Batas *recovery latency* p95 | 90 detik |
| $F_{max}$ | Batas *flapping rate* (jika dipakai) | flap/jam |

---

## 2. Singkatan

| Singkatan | Kepanjangan |
|---|---|
| SPA-HSM | *Session-Preserving Asymmetric Hysteresis State Machine* |
| PCC | *Per Connection Classifier* |
| ECMP | *Equal-Cost Multi-Path* |
| NTH | *Nth* (metode pembagian RouterOS) |
| EWMA | *Exponentially Weighted Moving Average* |
| SAW | *Simple Additive Weighting* |
| MCDM | *Multi-Criteria Decision Making* |
| QoS | *Quality of Service* |
| QoE | *Quality of Experience* |
| FO | *Fiber Optic* |
| LEO | *Low Earth Orbit* |
| GEO | *Geostationary Earth Orbit* |
| RST | *Reset* (flag TCP) |
| SIWG | *Session-Impact-Weighted Goodput* |
| SNMP | *Simple Network Management Protocol* |
| API | *Application Programming Interface* |
| RT/RW Net | Rukun Tetangga/Rukun Warga Net (penyedia internet skala lingkungan) |
| NTP | *Network Time Protocol* |
| LMM | *Linear Mixed Model* |
| NB | *Negative Binomial* |
| GEE | *Generalized Estimating Equations* |
| GLM | *Generalized Linear Model* |
| CI | *Confidence Interval* |
| IRR | *Incidence Rate Ratio* |
| MDE | *Minimum Detectable Effect* |
| ICC | *Intraclass Correlation Coefficient* |

---

## 3. Aturan Notasi

1. Simbol matematis ditulis miring; nama fungsi dan kode ditulis monospace.
2. Subskrip $i$ untuk link, $j$ untuk kriteria, $t$ untuk waktu.
3. Proporsi ditulis 0–1; persentase diberi tanda $\%$.
4. `AFFINITY_LOCK` ditulis monospace karena merupakan nama direktif.
5. Jangan memakai simbol yang sama untuk dua makna berbeda.
