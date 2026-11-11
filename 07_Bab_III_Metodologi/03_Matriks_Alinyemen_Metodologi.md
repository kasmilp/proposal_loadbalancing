# Matriks Alinyemen Metodologi

**Dokumen:** `03_Matriks_Alinyemen_Metodologi.md`
**Fungsi:** Memastikan setiap pertanyaan penelitian punya jalur yang jelas menuju
instrumen, analisis, dan bukti.

---

## 1. RQ → Tujuan → Bagian Bab III → Bukti

| RQ | Tujuan | Bagian Bab III | Instrumen | Analisis | Bukti |
|---|---|---|---|---|---|
| RQ1 | T1 | 3.5.1, 3.5.2, 3.5.4 | Metrik QoS, SNMP, probe | Uji pemetaan bucket, sensitivitas bobot | Rumus, contoh hitung, tabel parameter |
| RQ2 | T2 | 3.5.3, 3.4.2 | Log state, log rule change | NB mixed, non-inferioritas | Kurva trade-off, IRR, recovery p95 |
| RQ3 | T3 | 3.5.5, 3.6.1 | Capture LAN, uji RST | Logistik/beta mixed, bootstrap | RST flow/packet, CI |
| RQ4 | T4 | 3.4, 3.6.3, 3.8 | Dataset episode | LMM, SIWG, sensitivitas λ | Rasio goodput, SIWG, effect size |
| RQ5 | T5 | 3.5.6 | `MockAdapter`, adapter kedua | Uji konformitas, hash keputusan | Matriks konformitas |

---

## 2. Hipotesis → Data → Uji → Kriteria

| Hipotesis | Data yang dibutuhkan | Uji | Kriteria lulus |
|---|---|---|---|
| H1 | Flap per jam; recovery per episode | NB mixed + KW/Dunn | IRR < 0,5; recovery p95 ≤ 90 s |
| H2 | Flap per jam; recovery C/D/E/F | NB mixed + non-inferioritas | IRR < 0,7; Δrecovery ≤ 30 s; keduanya ≤ 90 s |
| H3a | Flow TCP, RST, episode | Logistik/beta mixed + bootstrap | F−D < 0; F−A ≤ +0,5 pp; sekunder < 1% |
| H3b | Goodput, latency p95 per episode | LMM + bootstrap | Rasio ≥ 1,10; ≤ 0,85; non-inferior G |
| H4 | SIWG per episode | LMM + bootstrap | Rasio ≥ 1,15; CI > 1,00 |
| H5 | Urutan keputusan dua adapter | Konformitas + exact match | 100% identik |

---

## 3. Kondisi → Perbandingan → Hipotesis

| Kondisi | Peran | Perbandingan utama |
|---|---|---|
| A | Baseline statis | F vs A (H3b, H4) |
| B | Dynamic naive | B vs C/D (H1) |
| C | Simetris, affinity off | C vs D (H2); C vs E (H3a) |
| D | Asimetris, affinity off | D vs F (H3a); B vs D (H1) |
| E | Simetris, affinity on | E vs F (H2) |
| F | SPA-HSM | F vs A, F vs G, F vs semua (H3b, H4) |
| G | Baseline praktisi | F vs G (H3b, H4) |

---

## 4. Instrumen → Metrik → Hipotesis

| Instrumen | Metrik | Hipotesis |
|---|---|---|
| Probe per WAN | RTT, jitter, loss | H1, H2, H3b |
| SNMP | Utilisasi, error, discard | H3b, H4 |
| `iperf3`/HTTP | Throughput, goodput | H3b, H4 |
| Capture LAN | RST, retransmisi | H3a |
| Log controller | State, bucket, rule change | H1, H2, H4 |
| Telemetri Starlink | Latency, drop, obstruction | H1, H2 |
| Stasiun cuaca | Curah hujan | Kovariat |
| `MockAdapter` | Urutan keputusan | H5 |

---

## 5. Yang Masih Harus Dilengkapi

| Item | Status | Tindakan |
|---|---|---|
| Verifikasi 7 klaim literatur | Belum | P-04 |
| Log pencarian gap | Belum | P-01 |
| Referensi PCC internasional | Belum | P-02 |
| Referensi MPTCP/kontinuitas sesi | Belum | P-03 |
| Audit sitasi | Belum | P-05 |
| Izin lokasi | Belum | D-06 |
| Telemetri Starlink | Belum | D-05 |
| Gaya sitasi | Belum | D-10 |

---

## 6. Uji Konsistensi Cepat

Sebelum naskah final, jawab lima pertanyaan ini:

1. Apakah setiap RQ muncul di Bab I dan Bab III? **Ya.**
2. Apakah setiap hipotesis punya metrik dan uji? **Ya.**
3. Apakah setiap kondisi punya peran yang jelas? **Ya.**
4. Apakah setiap instrumen punya *vantage point*? **Ya.**
5. Apakah setiap klaim punya sumber atau status desain? **Sebagian; P-04 belum.**
