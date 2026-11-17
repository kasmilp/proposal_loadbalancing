# 04 — Analisis Bobot SAW

**Status:** Draf kerja
**Fungsi:** Menilai kelayakan SAW menggabungkan parameter QoS, menetapkan
kriteria benefit/cost, membandingkan teknik normalisasi, dan memilih pendekatan
penentuan bobot yang dapat dipertanggungjawabkan secara ilmiah.

---

## 1. Kriteria Benefit dan Cost **[FAKTA + ANALISIS]**

**[FAKTA]** SAW adalah penjumlahan linier berbobot atas nilai ternormalisasi
(Wang & Kuo, 2013; Vafaei et al., 2021).

| Kriteria | Jenis | Alasan |
|---|---|---|
| Delay (P1) | **Cost** | Makin kecil makin baik |
| Jitter (P3) | **Cost** | Makin kecil makin baik |
| Packet loss (P4) | **Cost** | Makin kecil makin baik |
| Throughput / headroom (P5/P6) | **Benefit** | Makin besar makin baik |
| Utilisasi (P7) | Cost | Makin kecil makin baik (cadangan) |

**[ANALISIS]** Komposisi 3 cost : 1 benefit inilah penyebab pada contoh naskah lama
FO unggul meski throughput LEO lebih tinggi (bobot cost kumulatif 0,80). Ini **bukan
salah**, tetapi harus dijelaskan sebagai konsekuensi bobot — bukan kejutan.

---

## 2. Opsi Normalisasi

**Rumus baku [FAKTA]:**

| Kode | Rumus | Rentang |
|---|---|---|
| N-a | benefit $r = x/x_{\max}$ · cost $r = x_{\min}/x$ (dipakai naskah lama) | (0,1] |
| N-b | $r = (x - x_{\min})/(x_{\max} - x_{\min})$ | [0,1] |
| N-c | Batas acuan tetap: $r = \mathrm{clip}\!\left(\dfrac{x - x_{\mathrm{ref,min}}}{x_{\mathrm{ref,max}} - x_{\mathrm{ref,min}}}, 0, 1\right)$ (cost dibalik) | [0,1] |
| N-d | Vektor/sum: $r = x/\sqrt{\sum x^2}$ atau $x/\sum x$ | variatif |

**Perbandingan [ANALISIS]:**

| Kode | Kelebihan | Risiko | Komparabilitas antar-waktu |
|---|---|---|---|
| N-a | Sederhana, cepat | Sensitif outlier; $x_{\min}=0$ → bagi nol | Sedang (tergantung $x_{\max}$) |
| N-b | Rentang [0,1] seragam | **Batas bergeser tiap siklus** | **Rendah** |
| N-c | Stabil & interpretabel | Perlu justifikasi batas acuan | **Tinggi** |
| N-d | Relatif terhadap populasi | Kehilangan interpretasi 0–1 | Sedang |

**[FAKTA]** Vafaei et al. (2021) membuktikan pilihan normalisasi **mengubah peringkat
akhir secara signifikan** — diuji pada **dataset statis**.

**Keputusan [USULAN]:**
- **Default:** **N-c** dengan batas acuan dari TIPHON/Y.1541 (lihat
  `03_Spesifikasi_Parameter.md`).
- **Pembanding uji:** **N-a** dan **N-b**.
- **Metrik penilaian:** *rank reversal* dan stabilitas temporal indeks (lihat
  `08_Rancangan_Eksperimen.md`).

Rasional: pada sistem kontrol, indeks harus **komparabel antar-waktu**; N-b yang
batasnya bergeser tiap siklus membuat skor yang sama bisa punya arti berbeda di dua
waktu.

---

## 3. Pendekatan Penentuan Bobot

### 3.1 Peta metode **[FAKTA literatur; kandidat perlu verifikasi]**

| Kelompok | Metode | Rujukan | Karakter |
|---|---|---|---|
| Subjektif | Ahli / AHP / BWM | Wang & Kuo (2013) | Stabil, dapat diaudit, tidak adaptif |
| Objektif | **Entropy** | Wireless Networks 2021 `10.1007/s11276-021-02625-y` | Bobot dari dispersi data |
| Objektif | **CRITIC** | Symmetry 2021 `10.3390/sym13060973`; 2025 `10.14710/jmasif.16.2.73143` | Bobot dari kontras + konflik antar-kriteria |
| Objektif | **MEREC** | Symmetry 2021 `10.3390/sym13040525` | Bobot dari efek penghapusan kriteria |
| Tinjauan | Review metode bobot MCDM | Information 2023 `10.3390/info14050285` | Landasan Bab II |
| Hibrida | $\gamma\,w^{\text{subj}} + (1-\gamma)\,w^{\text{obj}}$ | Sintesis [USULAN] | Menyeimbangkan stabilitas & adaptivitas |

### 3.2 Rumus bobot objektif **[FAKTA]**

**Entropy.** Untuk matriks ternormalisasi $p_{ij} = r_{ij}/\sum_i r_{ij}$:

$$e_j = -\frac{1}{\ln m}\sum_{i=1}^{m} p_{ij}\ln p_{ij}, \qquad
w_j^{\text{obj}} = \frac{1-e_j}{\sum_{k}(1-e_k)}$$

**CRITIC.** Dengan $\sigma_j$ simpangan baku kriteria $j$ dan $\rho_{jk}$ korelasi
antar-kriteria:

$$C_j = \sigma_j \sum_{k}(1-\rho_{jk}), \qquad w_j = \frac{C_j}{\sum_k C_k}$$

### 3.3 Analisis kelayakan tiap opsi **[ANALISIS]**

| Opsi | Kelebihan | Risiko | Verdict |
|---|---|---|---|
| Bobot statis (naskah lama) | Auditable, replikabel | Tidak "adaptif" → rapuh terhadap kritik | Pertahankan sebagai pembanding |
| Bobot objektif murni | Adaptif terhadap data | Bisa tidak stabil saat derau → *chattering* | Uji, jangan langsung dipakai |
| **Hibrida** | Menyeimbangkan stabilitas & adaptivitas | Perlu kalibrasi $\gamma$ | **Direkomendasikan** |

### 3.4 Aturan bobot adaptif **[USULAN]**

$$w_j(t) = \gamma\, w_j^{\text{ahli}} + (1-\gamma)\, w_j^{\text{obj}}(t), \qquad \gamma \in [0,1]$$

- $w^{\text{obj}}(t)$ dihitung dari **jendela geser** $N$ sampel (mis. $N = 30$–$60$).
- $\gamma$ diuji sensitivitas: $\gamma \in \{0, 0{,}25, 0{,}5, 0{,}75, 1\}$.
- Bobot dinormalisasi ulang agar $\sum_j w_j(t) = 1$.

---

## 4. Jebakan yang Harus Dihindari **[ANALISIS]**

| Jebakan | Contoh | Mitigasi |
|---|---|---|
| Istilah "adaptif" tanpa definisi | Bobot statis disebut adaptif | Definisikan adaptivitas pada **bobot** dan/atau **batas normalisasi** |
| *Double counting* | Headroom dipakai di skor **dan** dikalikan lagi | Pilih satu peran, atau nyatakan eksplisit |
| Bobot berubah tiap siklus → osilasi | $w(t)$ diperbarui setiap detik | Perbarui tiap $N$ sampel + gerbang histeresis |
| Normalisasi tanpa batas acuan | min–max bergeser | Gunakan N-c sebagai default |
| Klaim "lebih baik" tanpa ukuran | — | Bandingkan vs baseline + effect size |

---

## 5. Kesimpulan **[USULAN]**

SAW **layak** dipakai sebagai mesin penggabung karena komputasinya ringan dan
pemisahan cost/benefit-nya jelas — syarat untuk siklus kontrol berskala detik.
Namun **nilai ilmiah bukan terletak pada SAW-nya**, melainkan pada:
1. **teknik normalisasi** yang menjaga komparabilitas temporal (G-N1), dan
2. **skema pembobotan adaptif** yang akurat namun stabil (G-N2).
