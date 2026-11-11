# Tahap 4 — Rencana Analisis Statistik

**Dokumen:** `04_Rencana_Analisis_Statistik.md`
**Status:** Draf kerja Tahap 4
**Fungsi:** Menetapkan uji, model, dan aturan keputusan sebelum data dikumpulkan.
**Prinsip:** Rencana ini dikunci sebelum analisis. Perubahan setelah melihat data
dicatat sebagai penyimpangan protokol.

---

## 1. Outcome

### 1.1 Primary outcome

| Outcome | Hipotesis | Satuan | Alasan |
|---|---|---|---|
| Flapping rate | H1, H2 | flap/jam | Inti stabilitas keputusan |
| RST flow | H3a | % aliran | Inti kontinuitas sesi |
| Goodput | H3b | Mbps | Kinerja efektif |
| SIWG | H4 | Mbps setara | Trade-off gabungan |

### 1.2 Secondary outcome

| Outcome | Kegunaan |
|---|---|
| Recovery latency p95 | Kendala operasional |
| RST packet | Validasi silang RST flow |
| Latency p95, jitter, loss | Kualitas layanan |
| Retransmisi | Beban transport |
| Overhead CPU/API | Kelayakan perangkat |
| Fairness antar-link | Keseimbangan alokasi |
| Jumlah rule change | Validasi flapping |

### 1.3 Outcome yang **bukan** klaim

QoE, kepuasan pengguna, penghematan biaya, dan generalisasi multi-vendor tidak
diukur dan tidak diklaim.

---

## 2. Unit Analisis

| Analisis | Unit | Alasan |
|---|---|---|
| Flapping | Jam pengamatan per run | Data cacat; menghindari pseudoreplication |
| Recovery | Episode degradasi | Satu kejadian = satu observasi |
| RST | Aliran TCP (flow) | Persentase aliran lebih bermakna daripada paket |
| Goodput | Episode degradasi | Kinerja selama kondisi yang diuji |
| SIWG | Episode degradasi | Metrik gabungan per episode |
| H5 | Urutan keputusan | Uji kesamaan, bukan statistik inferensial |

**Larangan:** memperlakukan setiap sampel 1 detik sebagai observasi independen.

---

## 3. Statistik Deskriptif

Untuk setiap kondisi:

- $n$ episode, durasi total, jumlah rule change.
- Median, IQR, p95 untuk goodput, latency, recovery.
- RST flow: proporsi + 95% CI Wilson.
- Flapping: total flap dan rate per jam + 95% CI Poisson.
- Visual: boxplot per kondisi, ECDF goodput, time series episode.

Semua grafik menyertakan jumlah observasi dan interval kepercayaan.

---

## 4. Model per Hipotesis

### H1 dan H2 — Flapping

Model utama:

```
flaps ~ scenario + offset(log(hours)) + (1 | block/day) + (1 | run)
family = negative binomial
```

- Estimasi: IRR per skenario vs pembanding.
- 95% CI: profil likelihood atau *bootstrap*.
- Jika overdispersi rendah: Poisson; jika *zero-inflated*: ZINB dan laporkan
  perbandingan AIC.
- Uji pendukung: Kruskal–Wallis + Dunn dengan koreksi Holm.

**H1:** kontras B vs C, B vs D, B vs E, B vs F.
**H2:** kontras C vs D dan E vs F.

### Recovery latency

- Model linier campuran pada $\log(\text{recovery})$:

```
log(recovery) ~ scenario + (1 | day) + (1 | run)
```

- p95 diestimasi dengan *bootstrap* (10.000 resampel).
- Jika asumsi normalitas gagal: regresi kuantil atau *bootstrap* median.

### H3a — RST flow

Dua pendekatan, keduanya dilaporkan:

1. **Level aliran:** regresi logistik campuran

```
disrupted ~ scenario + (1 | run)
family = binomial
```

2. **Level episode:** regresi beta pada proporsi aliran terganggu

```
rst_flow ~ scenario + (1 | day)
family = beta
```

**Non-inferioritas:** *bootstrap* 10.000 resampel untuk selisih F−A; margin
+0,5 pp. Kriteria primer:
- F−D < 0 (95% CI tidak memuat 0),
- batas atas 95% CI F−A ≤ +0,5 pp.

**Sekunder:** RST flow F < 1% (dilaporkan, bukan syarat lulus).

### H3b — Goodput dan latency

```
log(goodput) ~ scenario + severity + (1 | day) + (1 | run)
log(latency_p95) ~ scenario + severity + (1 | day) + (1 | run)
```

- Rasio antar-kondisi dari *estimated marginal means*.
- 95% CI dengan *bootstrap* atau *parametric bootstrap*.
- Effect size: Cohen's $d$ atau Cliff's $\delta$.

Kriteria:
- goodput F/A ≥ 1,10 (batas bawah CI > 1,00),
- latency p95 F/A ≤ 0,85 (batas atas CI < 1,00),
- non-inferior vs G dengan margin yang ditetapkan setelah pilot.

### H4 — SIWG

```
siwg ~ scenario + severity + (1 | day) + (1 | run)
```

- Kontras F vs kondisi terbaik.
- Rasio ≥ 1,15; batas bawah 95% CI > 1,00.
- Sensitivitas $\lambda \in \{0{,}25;\ 0{,}5;\ 1{,}0\}$.
- Jika arah berubah pada salah satu $\lambda$, klaim diturunkan menjadi
  "bergantung pada bobot biaya sesi".

### H5 — Portabilitas

- Matriks konformitas: 100% operasi lulus.
- Perbandingan urutan keputusan: hash identik untuk dataset *replay* yang sama.
- Tidak memakai uji signifikansi; ini uji kesamaan.

---

## 5. Kekuatan Uji dan Ukuran Sampel

1. **Pilot** menghasilkan estimasi ICC, varians, dan laju episode/hari.
2. **Target:** 30–40 episode per kondisi.
3. **Perhitungan awal:** dua sisi $\alpha=0{,}05$, *power* 0,80, $d=0{,}5$
   → sekitar 34 per kelompok.
4. **Koreksi Holm** menurunkan *power*; karena itu target 40 lebih aman.
5. **Power simulasi:** jalankan simulasi NB/LMM dengan parameter pilot untuk
   memastikan *minimum detectable effect* realistis.
6. **Jika target tidak tercapai:** laporkan CI dan presisi; jangan mengklaim
   hasil tidak konklusif sebagai "tidak ada efek".

---

## 6. Koreksi Multiplisitas

- Keluarga uji: H1, H2, H3a, H3b, H4.
- Gunakan **Holm–Bonferroni** dalam keluarga ini.
- H2 memiliki dua kontras (C–D, E–F); keduanya masuk keluarga yang sama.
- H5 dilaporkan terpisah sebagai validasi rekayasa.
- Laporkan p mentah dan p terkoreksi.

---

## 7. Data Hilang dan Pengecualian

| Situasi | Tindakan |
|---|---|
| Sampel hilang sesaat | Tandai, interpolasi hanya untuk visualisasi |
| Episode tidak lengkap | Keluarkan dari analisis episode, laporkan jumlahnya |
| Controller mati | Tandai run; analisis sensitivitas tanpa run tersebut |
| Intervensi operator | Catat; analisis dengan dan tanpa intervensi |
| Cuaca ekstrem | Blok terpisah; analisis sensitivitas |
| Data staging vs lapangan | Variabel `source`; jangan dicampur tanpa model |

**Prinsip:** tidak ada imputasi untuk outcome primer. Data hilang dilaporkan,
bukan disembunyikan.

---

## 8. Pemeriksaan Robustness

1. Ulangi analisis tanpa episode hujan ekstrem.
2. Ulangi tanpa 60 detik pertama setiap run (warm-up).
3. Ulangi dengan $\lambda$ berbeda untuk SIWG.
4. Ulangi dengan model Poisson jika NB tidak konvergen.
5. Ulangi dengan *cluster-robust standard error* di level hari.
6. Bandingkan hasil staging dan lapangan; laporkan perbedaan arah.

---

## 9. Diagnostik Model

| Pemeriksaan | Kriteria |
|---|---|
| Overdispersi | Rasio deviance/df; jika > 1,5 gunakan NB |
| Zero-inflation | Proporsi nol vs prediksi; jika jauh, ZINB |
| Normalitas residual | QQ-plot; jika gagal, transformasi/kuantil |
| Homoskedastisitas | Residual vs fitted |
| Pengaruh | Cook's distance; periksa outlier |
| Konvergensi | Singular fit, Hessian; sederhanakan efek acak |
| Autokorelasi | ACF residual; tambah struktur AR(1) jika perlu |

---

## 10. Template Pelaporan

| Hipotesis | Efek | Estimate | 95% CI | p terkoreksi | Effect size | Kesimpulan |
|---|---|---:|---|---:|---|---|
| H1 | IRR flapping C vs B | — | — | — | — | — |
| H2 | IRR flapping D vs C | — | — | — | — | — |
| H3a | Δ RST flow F−D | — | — | — | — | — |
| H3b | Rasio goodput F/A | — | — | — | — | — |
| H4 | Rasio SIWG F/best | — | — | — | — | — |

**Aturan narasi:**
- Sebut estimate, CI, dan arah, bukan hanya "signifikan".
- Jika CI lebar, tulis "tidak konklusif".
- Jika efek kecil, tulis "signifikan tetapi tidak praktis".

---

## 11. Perangkat Lunak

| Kebutuhan | Alat |
|---|---|
| Manipulasi data | R (`tidyverse`) atau Python (`pandas`) |
| Model campuran | R `lme4`, `glmmTMB`, `nlme` |
| Kontras | R `emmeans` |
| Bootstrap | R `boot`, `rsample` |
| Regresi kuantil | R `quantreg` |
| Visualisasi | `ggplot2` |
| Reproduksibilitas | R Markdown/Quarto + `renv` |

Semua skrip disimpan di repositori dengan versi paket dan seed.

---

## 12. Pra-registrasi dan Penyimpangan

1. Rencana ini dikunci sebelum kampanye lapangan.
2. Setiap perubahan dicatat di log keputusan dengan tanggal dan alasan.
3. Penyimpangan yang terjadi setelah melihat data dilaporkan di Bab IV.
4. Tidak boleh menghapus outcome atau mengubah ambang tanpa jejak.
