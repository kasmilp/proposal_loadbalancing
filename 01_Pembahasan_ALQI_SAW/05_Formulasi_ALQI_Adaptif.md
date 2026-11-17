# 05 — Formulasi ALQI Adaptif

**Status:** Draf kerja
**Fungsi:** Merumuskan indeks kualitas link dari bentuk statis (naskah lama) menjadi
bentuk adaptif yang dapat dipertanggungjawabkan.

**Catatan nama [USULAN]:** karena "ALQI" memiliki prior art (lihat
`01_Kelayakan_dan_Prior_Art.md`), simbol yang dipakai di sini adalah **$Q_i(t)$**
(skor kualitas link). Istilah "ALQI" hanya boleh muncul sebagai rujukan prior art.

---

## 1. Bentuk Statis (Naskah Lama) **[FAKTA]**

Naskah `Proposal pcc- print.pdf` memakai:

$$s_i = \sum_{j} w_j\, r_{ij}, \qquad \text{ALQI}_i = 100 \cdot s_i$$

dengan normalisasi cost $r = \min(x)/x$ dan benefit $r = x/\max(x)$, serta bobot
contoh $w_D = 0{,}30$, $w_J = 0{,}25$, $w_{PL} = 0{,}25$, $w_T = 0{,}20$.

**Verifikasi ulang contoh naskah [FAKTA]:**

| Jalur | Delay | Jitter | Loss | Throughput |
|---|---:|---:|---:|---:|
| FO | 25 ms | 3 ms | 0,5% | 45 Mbps |
| LEO | 45 ms | 12 ms | 1,2% | 80 Mbps |

- FO: $r_D = 1$, $r_J = 1$, $r_{PL} = 1$, $r_T = 45/80 = 0{,}5625$
  → $s = 0{,}30 + 0{,}25 + 0{,}25 + 0{,}1125 = 0{,}9125$ → **ALQI = 91,3**
- LEO: $r_D = 0{,}556$, $r_J = 0{,}25$, $r_{PL} = 0{,}417$, $r_T = 1$
  → $s = 0{,}167 + 0{,}0625 + 0{,}104 + 0{,}20 = 0{,}533$ → **ALQI = 53,3**

Perhitungan konsisten. **Masalah [ANALISIS]:** bobot statis → tidak ada yang
"adaptif"; dan min/max bergeser tiap siklus → tidak komparabel antar-waktu.

---

## 2. Bentuk Adaptif yang Diusulkan **[USULAN]**

$$
\boxed{\;Q_i(t) = 100 \sum_{j \in \{D, J, PL, B\}} w_j(t)\, \tilde r_{ij}(t)\;}
$$

dengan empat komponen:

### (1) Penghalusan deret metrik (EWMA)

$$\tilde x_{ij}(t) = \alpha\, x_{ij}(t) + (1-\alpha)\, \tilde x_{ij}(t-1), \qquad \alpha \in [0{,}10;\, 0{,}20]$$

**[FAKTA]** EWMA dari Roberts (1959). Jendela efektif $\approx 2/\alpha - 1$ sampel.

### (2) Normalisasi berbatas acuan tetap

Untuk **cost** (delay, jitter, loss):

$$\tilde r_{ij}(t) = \mathrm{clip}\!\left(\frac{x_{\mathrm{ref,max}} - \tilde x_{ij}(t)}{x_{\mathrm{ref,max}} - x_{\mathrm{ref,min}}},\, 0,\, 1\right)$$

Untuk **benefit** (throughput/headroom):

$$\tilde r_{ij}(t) = \mathrm{clip}\!\left(\frac{\tilde x_{ij}(t) - x_{\mathrm{ref,min}}}{x_{\mathrm{ref,max}} - x_{\mathrm{ref,min}}},\, 0,\, 1\right)$$

Batas acuan dari TIPHON/Y.1541 (lihat `03_Spesifikasi_Parameter.md`). Tujuannya:
**komparabilitas antar-waktu** (gap G-N1).

### (3) Bobot adaptif

$$w_j(t) = \gamma\, w_j^{\text{ahli}} + (1-\gamma)\, w_j^{\text{obj}}(t),
\qquad \sum_j w_j(t) = 1$$

$w_j^{\text{obj}}(t)$ dari Entropy/CRITIC atas jendela geser $N$ sampel
(lihat `04_Analisis_Bobot_SAW.md`).

### (4) Gerbang kestabilan (histeresis asimetris)

Keputusan (mis. peringkat link / alokasi) hanya berubah saat transisi status:

- masuk **TERDEGRADASI** bila $Q_i(t) < \theta_{\text{degradasi}}$ selama $k_{\text{down}}$ sampel berturut-turut;
- kembali **BAIK** bila $Q_i(t) > \theta_{\text{pemulihan}}$ selama $k_{\text{up}}$ sampel berturut-turut;
- zona antara dipertahankan status terakhir (*dead zone*).

**[FAKTA]** Ambang ganda mencegah osilasi; ambang identik menimbulkan osilasi
(Tournaire et al., 2023).

---

## 3. Mengapa Ini "Adaptif" secara Jujur **[ANALISIS]**

| Klaim adaptivitas | Valid? | Penjelasan |
|---|---|---|
| Bobot berubah dari data | **Ya** | $w_j^{\text{obj}}(t)$ dihitung dari jendela geser |
| Batas normalisasi menyesuaikan konteks | Opsional | Dapat disesuaikan per skenario; default tetap dari standar |
| Mengganti metode MCDM secara dinamis | **Tidak diklaim** | SAW tetap SAW |
| Pembelajaran bobot otomatis (self-tuning) | **Tidak diklaim** | Di luar lingkuptrya; jangan overclaim |

**[ANALISIS]** Klaim "adaptif" yang aman: *"bobot kriteria diperbarui berdasarkan
dispersi/kontras data pada jendela geser, dengan parameter $\gamma$ mengatur
keseimbangan antara prior ahli dan data."*

---

## 4. Parameter yang Perlu Dikunci **[USULAN]**

| Simbol | Arti | Nilai awal | Status |
|---|---|---:|---|
| $\alpha$ | Faktor EWMA | 0,10–0,20 | Uji sensitivitas |
| $N$ | Jendela update bobot | 30–60 sampel | Uji sensitivitas |
| $\gamma$ | Bobot hibrida | 0,5 | Uji {0; 0,25; 0,5; 0,75; 1} |
| $\theta_{\text{degradasi}}$ | Ambang masuk degradasi | peringkat $Q$ penentu | Turunkan dari data/pilot |
| $\theta_{\text{pemulihan}}$ | Ambang kembali baik | $> \theta_{\text{deg}}$ | Asimetri |
| $k_{\text{down}}, k_{\text{up}}$ | Dwell count | $k_{\text{up}} > k_{\text{down}}$ | Turunkan dari transien 15 dtk |
| $T_s$ | Interval polling | 1 detik | Perangkat |
| $W$ | Jendela flap | 5 menit | Uji 1/5/15 |

---

## 5. Kasus Uji Ilustratif **[USULAN]**

Bandingkan dua jalur (FO vs LEO) pada tiga kondisi:
1. **Normal** — kedua link sehat.
2. **Transien LEO** — jitter/loss melonjak singkat (pola 15 dtk).
3. **Degradasi FO sustained** — throughput turun bertahap (kongesti jam sibuk).

Harapan: $Q_i(t)$ mengikuti degradasi **sustained** tetapi **tidak** berkedip pada
transien singkat (berkat EWMA + gerbang). Target uji: rasio chattering, rank
reversal, dan korelasi $Q$ terhadap goodput.
