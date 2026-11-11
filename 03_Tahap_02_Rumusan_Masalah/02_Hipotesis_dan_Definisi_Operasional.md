# Tahap 2 — Hipotesis dan Definisi Operasional

**Dokumen:** `02_Hipotesis_dan_Definisi_Operasional.md`
**Status:** Draf kerja Tahap 2
**Fungsi:** Menetapkan hipotesis yang dapat diuji, definisi operasional yang sama
untuk semua skenario, dan aturan keputusan statistik.

**Penting:** ambang numerik di bawah ini adalah **ambang awal**. Nilai final
ditetapkan setelah pilot 24–48 jam dan dicatat di log keputusan. Yang tidak boleh
berubah setelah data dikumpulkan adalah **arah** dan **definisi operasional**.

---

## 1. Definisi Operasional

Semua definisi ini berlaku identik untuk skenario A–F dan baseline.

### 1.1 Episode degradasi

Periode yang dimulai saat $Q_i(t) < \theta_{low}$ selama $k_{down}$ sampel
berturut-turut dan berakhir saat $Q_i(t) > \theta_{high}$ selama $k_{up}$ sampel
berturut-turut. Satu episode dihitung satu observasi.

**Mengapa:** mencegah *pseudoreplication* akibat memperlakukan setiap sampel
deret waktu sebagai observasi independen.

### 1.2 *Effective PCC rule change*

Perubahan jumlah bucket PCC pada minimal satu link. Perubahan target rasio yang
tidak mengubah alokasi bucket **tidak** dihitung, karena tidak memengaruhi
koneksi baru.

### 1.3 *Flap*

*Effective PCC rule change* yang diikuti perubahan arah sebaliknya dalam jendela
pengamatan $W = 5$ menit. Satu pasangan perubahan dihitung satu flap.

**Flapping rate** = jumlah flap per jam pengamatan.

### 1.4 *Recovery latency*

Waktu dari sampel pertama $Q_i < \theta_{low}$ (awal episode) sampai state kembali
`STABLE`, yaitu $Q_i > \theta_{high}$ selama $k_{up}$ sampel berturut-turut.
Dilaporkan sebagai p50 dan p95 per skenario.

### 1.5 TCP RST rate

Dua ukuran, keduanya dilaporkan:

$$\text{RST}_{packet}\% = \frac{\text{jumlah paket TCP RST}}{\text{jumlah paket TCP}} \times 100\%$$

$$\text{RST}_{flow} = \frac{\text{jumlah aliran TCP dengan} \geq 1 \text{ RST}}{\text{jumlah aliran TCP}} \in [0,1]$$

$$\text{RST}_{flow}\% = 100 \times \text{RST}_{flow}$$

Untuk pelaporan digunakan $\text{RST}_{flow}\%$; untuk perhitungan SIWG digunakan
proporsi $\text{RST}_{flow}$.

Diukur pada *vantage point* controller/LAN capture, bukan hanya di router.

### 1.6 Goodput

Byte tingkat aplikasi yang berhasil diterima selama episode dibagi durasi episode,
tidak termasuk retransmisi. Diukur dengan `iperf3` dan probe HTTP berukuran tetap.

### 1.7 Latensi end-to-end

RTT probe aktif per WAN; dilaporkan p50, p95, p99. Bukan latensi antrean router.

### 1.8 *Session-Impact-Weighted Goodput* (SIWG)

Metrik gabungan yang mendiskon goodput dengan biaya gangguan sesi:

$$\text{SIWG} = G_{eff} \times (1 - \lambda \cdot \text{RST}_{flow})$$

dengan:
- $G_{eff}$ = goodput efektif episode (Mbps),
- $\text{RST}_{flow}$ = proporsi aliran terganggu (0–1),
- $\lambda \in [0,1]$ = bobot biaya sesi; nilai default $\lambda = 1$.

**Interpretasi:** satu aliran yang terganggu dianggap kehilangan seluruh
kontribusinya pada episode tersebut. Ini asumsi konservatif yang mudah diaudit.
Analisis sensitivitas dilakukan untuk $\lambda \in \{0{,}25;\ 0{,}5;\ 1{,}0\}$.

**Mengapa bukan metrik baru yang rumit:** SIWG hanya memerlukan dua besaran yang
sudah diukur (goodput dan RST flow). Tidak ada parameter tersembunyi selain
$\lambda$ yang diuji sensitivitasnya.

**Batas klaim:** SIWG adalah alat pembanding internal, bukan standar industri.
Jangan mengklaim validitas eksternal di luar korpus penelitian ini.

### 1.9 *Baseline* praktisi

PCC dengan `netwatch`/health-check failover: jika probe gagal, rute dialihkan.
Rasio tetap; tidak ada histeresis multi-ambang dan tidak ada affinity eksplisit.

### 1.10 Peta Skenario yang Dirujuk

| Skenario | Histeresis | Affinity | Peran |
|---|---|---|---|
| A | Tidak ada (rasio statis) | — | Baseline statis |
| B | Tidak ada (rasio dinamis) | Off | *Dynamic naive* |
| C | Simetris | Off | Isolasi bentuk histeresis |
| D | Asimetris | Off | Isolasi asimetri waktu |
| E | Simetris | On | Affinity pada simetris |
| F | Asimetris | On | **SPA-HSM (usulan)** |
| G | — | — | Baseline praktisi (`netwatch`) |

Perbandingan kunci: **B→D** (efek histeresis), **C→D** (efek asimetri),
**D→F** (efek affinity), **A→F** (efek total), **G→F** (efek vs praktik).


---

## 2. Hipotesis

**Batas global.** Untuk semua skenario, *recovery latency* p95 tidak boleh melebihi
$R_{max} = 90$ detik pada $T_s = 1$ detik. Batas ini berlaku sebagai kendala
operasional, bukan sebagai klaim bahwa 90 detik selalu dapat diterima.

### H1 — Histeresis menekan flapping

**Pernyataan.** SPA-HSM dengan histeresis (simetris atau asimetris) menurunkan
*flapping rate* minimal **50%** dibanding varian tanpa histeresis, tanpa membuat
*recovery latency* p95 melebihi **90 detik** pada $T_s = 1$ detik.

- **Variabel bebas:** mode histeresis (none / symmetric / asymmetric).
- **Variabel terikat:** flapping rate (flap/jam); recovery latency p95 (detik).
- **Isolasi:** H1 membandingkan B vs C dan B vs D, yaitu kondisi dengan affinity
  off, agar efek histeresis tidak bercampur dengan efek affinity.
- **Arah:** flapping turun; recovery tetap di bawah batas.
- **Uji:** model *negative binomial* campuran dengan *offset* jam pengamatan;
  faktor tetap = skenario, efek acak = hari/run. Laporkan *incidence rate ratio* (IRR).
- **Uji pendukung:** Kruskal–Wallis + Dunn dengan koreksi Holm.
- **Diterima jika:** IRR < 0,5; 95% CI tidak memuat 1; p95 recovery ≤ 90 detik.

---

### H2 — Asimetri waktu memperbaiki trade-off

**Pernyataan.** Histeresis asimetris ($k_{up} \gg k_{down}$) menurunkan
*flapping rate* minimal **30%** dibanding histeresis simetris pada $\theta$ yang
sama, dengan kenaikan *recovery latency* p95 **tidak lebih dari 30 detik** dan
keduanya tetap **≤ 90 detik**.

- **Perbandingan:** skenario D (asimetris) vs C (simetris), hanya $k_{up}$ yang berbeda.
- **Uji:** sama dengan H1; ditambah uji non-inferioritas dengan margin 30 detik.
- **Diterima jika:** IRR < 0,7; 95% CI tidak memuat 1; selisih p95 recovery ≤ 30 detik
  (batas atas 95% CI ≤ 30 detik); p95 recovery kedua skenario ≤ 90 detik.

**Catatan desain.** Karena enam skenario A–F dijalankan, H2 diuji penuh. Jika salah
satu run gagal dan C tidak tersedia, H2 dilaporkan sebagai *bukti parsial* dengan
perbandingan D vs B, bukan sebagai bukti penuh.

---

### H3a — Affinity lock menjaga integritas sesi

**Pernyataan.** `AFFINITY_LOCK` menurunkan $\text{RST}_{flow}$ dibanding varian
tanpa affinity, dan **tidak inferior** terhadap baseline PCC statis dengan margin
**0,5 poin persentase**. Keduanya adalah **dua komponen kriteria primer**. Nilai
absolut $\text{RST}_{flow}\%$ di bawah **1%** dilaporkan sebagai **kriteria sekunder**.

- **Perbandingan:** F (asimetris + affinity) vs D (asimetris tanpa affinity);
  F vs baseline statis A.
- **Uji:** regresi beta atau model logistik campuran pada level aliran;
  *bootstrap* 10.000 resampel untuk selisih proporsi.
- **Diterima (primer) jika:** selisih F−D < 0 (95% CI tidak memuat 0) **dan**
  batas atas 95% CI untuk F−A ≤ +0,5 pp.
- **Sekunder:** $\text{RST}_{flow}\% < 1\%$ dilaporkan sebagai target absolut.
  Jika primer lolos tetapi sekunder gagal, statusnya **"non-inferior, target
  absolut belum tercapai"** — bukan "didukung penuh".

---

### H3b — Kinerja agregat meningkat saat degradasi

**Pernyataan.** Pada episode degradasi, SPA-HSM meningkatkan *goodput* minimal
**10%** dan menurunkan latensi p95 minimal **15%** dibanding PCC statis, serta
**tidak inferior** terhadap baseline praktisi.

- **Uji:** model linier campuran pada level episode dengan kovariat tingkat
  keparahan degradasi; efek acak hari/run. Goodput ditransformasi log.
- **Uji pendukung:** ANOVA/Kruskal–Wallis + post hoc; *bootstrap* BCa untuk
  perbedaan median.
- **Diterima jika:** rasio goodput ≥ 1,10 (95% CI batas bawah > 1,00); rasio
  latensi p95 ≤ 0,85 (95% CI batas atas < 1,00); non-inferior vs baseline praktisi.
- **Effect size:** Cohen's d atau Cliff's delta dilaporkan, bukan hanya p-value.

---

### H4 — SIWG SPA-HSM lebih tinggi dari semua pembanding

**Pernyataan.** SIWG SPA-HSM lebih tinggi minimal **15%** dibanding baseline
terbaik (statis, tanpa histeresis, simetris, atau baseline praktisi).

- **Uji:** model linier campuran pada SIWG level episode; *bootstrap* untuk
  perbedaan dan interval kepercayaan.
- **Analisis sensitivitas:** ulangi untuk $\lambda \in \{0{,}25;\ 0{,}5;\ 1{,}0\}$.
- **Diterima jika:** rasio SIWG ≥ 1,15; 95% CI batas bawah > 1,00; arah tetap
  konsisten pada ketiga nilai $\lambda$.

**Mengapa hipotesis ini penting.** H3b hanya melihat kinerja; H4 menguji klaim
utama penelitian, yaitu bahwa stabilitas dan kontinuitas tidak boleh dikorbankan
satu sama lain.

---

### H5 — Portabilitas inti algoritma (validasi rekayasa)

**Pernyataan.** *Algorithm Core* lulus seluruh uji konformitas kontrak dan
menghasilkan urutan keputusan yang **identik** pada dua adapter (mock dan MikroTik)
untuk dataset *replay* yang sama.

- **Uji:** matriks konformitas (semua operasi: `read_metrics`, `set_ratio`,
  `set_affinity`, `get_state`, `verify`, `rollback`); perbandingan hash urutan
  keputusan.
- **Diterima jika:** 100% operasi sesuai kontrak dan 100% urutan keputusan identik.
- **Batas klaim:** ini bukan bukti portabilitas lintas vendor; hanya bukti bahwa
  inti tidak bergantung pada satu adapter.

---

## 3. Matriks Hipotesis–Uji–Ambang

| ID | Perbandingan | Metrik | Uji utama | Ambang diterima | Effect size |
|---|---|---|---|---|---|
| H1 | Hysteresis vs none | Flapping rate, recovery p95 | NB mixed model + KW/Dunn | IRR < 0,5; recovery p95 ≤ 90 s | IRR, 95% CI |
| H2 | Asymmetric vs symmetric | Flapping rate, recovery p95 | NB mixed + non-inferiority | IRR < 0,7; Δrecovery ≤ 30 s; keduanya ≤ 90 s | IRR, Δ dengan CI |
| H3a | Affinity vs no-affinity; vs statis | RST flow, RST packet | Beta/logistic mixed + bootstrap | Primer: F−D < 0; F−A ≤ +0,5 pp. Sekunder: < 1% | Selisih pp, 95% CI |
| H3b | SPA-HSM vs statis/praktisi | Goodput, latency p95 | LMM + bootstrap | Rasio ≥ 1,10; ≤ 0,85; non-inferior | d / Cliff's δ |
| H4 | SPA-HSM vs baseline terbaik | SIWG | LMM + bootstrap | Rasio ≥ 1,15; CI > 1,00 | d, 95% CI |
| H5 | Dua adapter | Urutan keputusan | Uji konformitas + exact match | 100% identik | — |

---

## 4. Rencana Ukuran Sampel dan Kekuatan Uji

Angka ini **sementara** dan diperbarui setelah pilot.

1. **Unit analisis:** episode degradasi (bukan sampel polling).
2. **Kondisi:** 6 skenario (A–F) + baseline praktisi G = 7 kondisi.
3. **Target awal:** 30 episode per kondisi; prioritas analisis inti pada A, B, D, F.
   Total indikatif 210 episode; jika lapangan tidak mencukupi, kekurangan ditutup
   dengan *replay* staging dan dilaporkan terpisah.
4. **Justifikasi:** untuk uji dua sisi $\alpha = 0{,}05$, *power* 0,80, dan
   *minimum detectable effect* $d = 0{,}5$, dibutuhkan sekitar 34 episode per
   kelompok; 30–40 adalah kompromi dengan keterbatasan lapangan.
5. **Jika episode lapangan kurang:** lengkapi dengan *replay* staging terkontrol
   dan laporkan secara terpisah; jangan mencampur tanpa model yang mengakomodasi
   sumber data.
6. **Koreksi multiplisitas:** Holm–Bonferroni dalam satu keluarga hipotesis
   (H1–H4). H5 bersifat konfirmatori rekayasa dan dilaporkan terpisah.
7. **Efek acak:** hari pengamatan dan run, untuk mengakomodasi autokorelasi dan
   variasi cuaca.

---

## 5. Aturan Keputusan

| Kondisi | Kesimpulan |
|---|---|
| p < α terkoreksi **dan** effect size ≥ ambang **dan** CI konsisten | **Didukung** |
| p < α tetapi effect size < ambang | **Didukung secara statistik, tidak praktis** — laporkan apa adanya |
| p ≥ α tetapi CI lebar | **Tidak konklusif** — jangan klaim tidak ada efek |
| Arah berlawanan dengan hipotesis | **Tidak didukung** — laporkan dan analisis penyebab |
| Non-inferioritas terpenuhi | **Non-inferior** — bukan berarti lebih baik |
| Kriteria primer lolos, kriteria sekunder gagal | **Non-inferior, target absolut belum tercapai** — laporkan keduanya |

**Larangan:** tidak boleh mengubah ambang setelah melihat data. Perubahan harus
melalui log keputusan dan dijelaskan sebagai penyimpangan protokol.

---

## 6. Ancaman Validitas

| Ancaman | Dampak | Mitigasi |
|---|---|---|
| Cuaca berubah antar-run | Confounder utama | Blok waktu, acak urutan, catat curah hujan |
| Drift firmware/paket ISP | Perubahan baseline | Catat versi, uji perbaikan pada baseline |
| Carryover antar-skenario | Efek sisa | Washout minimal 2× durasi *dwell* maksimum |
| Efek instrumen | Probe membebani link | Probe frekuensi rendah, kalibrasi pilot |
| *Hawthorne*/intervensi operator | Bias | Protokol run otomatis, log intervensi |
| Episode sedikit | CI lebar | Replay staging + laporkan presisi |
| Kegagalan controller | Kehilangan data/risiko | Fail-static, watchdog, rollback teruji |

---

## 7. Ringkasan yang Akan Masuk Bab I

- **RQ payung:** trade-off stabilitas–kontinuitas–kinerja.
- **Lima sub-RQ** dan lima tujuan.
- **Enam hipotesis:** H1 flapping, H2 asimetri, H3a sesi, H3b kinerja, H4 SIWG,
  H5 portabilitas.
- **Satu metrik gabungan:** SIWG.
- **Satu aturan baru:** *dwell* sadar-transien.

Jika bagian ini kunci, Bab I dan Bab II tidak perlu ditulis ulang dari nol.
