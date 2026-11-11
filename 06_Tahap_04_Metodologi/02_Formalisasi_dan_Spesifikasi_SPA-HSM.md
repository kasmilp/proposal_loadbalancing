# Tahap 4 — Formalisasi dan Spesifikasi SPA-HSM

**Dokumen:** `02_Formalisasi_dan_Spesifikasi_SPA-HSM.md`
**Status:** Draf kerja Tahap 4
**Fungsi:** Menyediakan formalisasi yang cukup untuk diimplementasikan dan diuji.
**Aturan:** Semua simbol didefinisikan; tidak ada rumus yang hanya berupa gambar.

---

## 1. Notasi

| Simbol | Arti | Satuan/rentang |
|---|---|---|
| $i$ | Indeks link, $i \in \{1,2\}$ | — |
| $t$ | Waktu diskret, $t = k T_s$ | detik |
| $T_s$ | Interval sampling | 1 detik |
| $x_{ij}(t)$ | Metrik mentah $j$ pada link $i$ | sesuai metrik |
| $E_{ij}(t)$ | Nilai EWMA metrik $j$ | sesuai metrik |
| $r_{ij}(t)$ | Nilai ternormalisasi kriteria $j$ | $[0,1]$ |
| $w_j$ | Bobot kriteria $j$ | $\sum w_j = 1$ |
| $Q_i(t)$ | Skor kualitas link $i$ | $[0,1]$ |
| $s_i(t)$ | State link $i$ | STABLE/DEGRADED |
| $H_i(t)$ | Faktor headroom link $i$ | $[0,1]$ |
| $W_i(t)$ | Proporsi target link $i$ | $[0,1]$, $\sum W_i = 1$ |
| $b_i(t)$ | Jumlah bucket link $i$ | integer |
| $N$ | Total bucket | 20 |
| $\lambda$ | Bobot biaya sesi pada SIWG | $[0,1]$ |

---

## 2. Sampling dan EWMA

Metrik dasar: *throughput* ($j=1$), *delay* ($j=2$), *jitter* ($j=3$), *loss* ($j=4$).

$$E_{ij}(t) = \alpha \, x_{ij}(t) + (1-\alpha) \, E_{ij}(t-1)$$

dengan $\alpha = 0{,}20$. *Effective window*:

$$N_{eff} \approx \frac{2}{\alpha} - 1 = \frac{2}{0{,}2} - 1 = 9 \text{ sampel}$$

**Catatan aliasing.** $T_s = 1$ detik memberi 15 sampel per siklus transien
15 detik, sehingga bentuk transien masih terobservasi. Jika $T_s \ge 5$ detik,
transien dapat ter-*alias* dan aturan *dwell* kehilangan dasar.

---

## 3. Skor Kualitas Berbasis SAW

### 3.1 Normalisasi berbatas tetap

Atribut *benefit* (*throughput*):

$$r_{ij}(t) = \frac{E_{ij}(t) - x_j^{min}}{x_j^{max} - x_j^{min}}$$

Atribut *cost* (*delay*, *jitter*, *loss*):

$$r_{ij}(t) = \frac{x_j^{max} - E_{ij}(t)}{x_j^{max} - x_j^{min}}$$

Nilai dibatasi ke $[0,1]$; jika penyebut $=0$, gunakan $\varepsilon = 10^{-6}$.

### 3.2 Batas acuan

| Kriteria | Arah | $x^{min}$ | $x^{max}$ | Dasar |
|---|---|---:|---:|---|
| Throughput | Benefit | 0 Mbps | 100 Mbps | Kapasitas acuan |
| Delay | Cost | 0 ms | 150 ms | ITU-T G.114 |
| Jitter | Cost | 0 ms | 30 ms | TIPHON |
| Loss | Cost | 0% | 5% | TIPHON |

Batas ini **tetap** dan tidak dihitung ulang dari statistik antar-link setiap
siklus. Tujuannya menjaga $Q_i(t)$ komparabel antar-waktu.

### 3.3 Bobot dan skor

| Kriteria | Bobot $w_j$ | Alasan |
|---|---:|---|
| Throughput | 0,35 | Kapasitas efektif |
| Delay | 0,30 | Sensitif untuk layanan interaktif |
| Jitter | 0,15 | Penting untuk VoIP/video |
| Loss | 0,20 | Merusak TCP |

$$Q_i(t) = \sum_{j=1}^{4} w_j \, r_{ij}(t), \qquad Q_i \in [0,1]$$

Bobot dikalibrasi di awal dan diuji sensitivitasnya ($\pm 0{,}05$ per kriteria).
Bobot **tidak** dipelajari secara *online*.

---

## 4. State Machine Histeresis

### 4.1 Transisi

| Dari | Ke | Kondisi |
|---|---|---|
| STABLE | DEGRADED | $Q_i(t) < \theta_{low}$ selama $k_{down}$ sampel berturut-turut |
| DEGRADED | STABLE | $Q_i(t) > \theta_{high}$ selama $k_{up}$ sampel berturut-turut |

Parameter: $\theta_{low}=0{,}60$, $\theta_{high}=0{,}80$, $k_{down}=20$,
$k_{up}=20$ (simetris) atau $60$ (asimetris).

### 4.2 Aturan dwell sadar-transien

Dengan transien dominan $T_{tr} \approx 15$ detik dan margin $m = T_s = 1$ detik:

$$k_{down} \cdot T_s = 20 > 15 + 1 = 16$$

Karena itu $k_{down}=20$ mencegah transien 15 detik memicu `DEGRADED` berulang.
*Detection delay* maksimum adalah 20 detik, masih jauh lebih pendek daripada
degradasi FO yang berskala menit.

### 4.3 Evaluasi ulang paksa

Setiap $T_{max} = 10$ menit, sistem mengevaluasi ulang rasio meskipun tidak ada
transisi. Perubahan hanya diterapkan jika:

1. selisih proporsi target dan aktif > 10 poin persentase, **dan**
2. kondisi bertahan ≥ 5 menit.

Mekanisme ini menangani degradasi lambat yang tidak melewati ambang, tanpa
mengubah definisi transisi utama.

### 4.4 Inisialisasi

Setelah *warm-up* 60 detik, sistem menghitung $Q_i$ dan menetapkan rasio awal
berdasarkan $Q_i H_i$. Tanpa inisialisasi, sistem dapat bertahan pada 50:50
meskipun salah satu link jauh lebih baik.

---

## 5. Kebijakan Rasio

### 5.1 Headroom

$$H_i(t) = \max\left(\varepsilon, \; 1 - u_i(t)\right)$$

dengan $u_i(t)$ adalah utilisasi link dari SNMP. Jika SNMP tidak tersedia,
$H_i = 1$ dan statusnya dicatat sebagai *degraded mode*.

### 5.2 Rasio saat kedua link STABLE

$$W_i(t) = \frac{Q_i(t) H_i(t)}{\sum_{k} Q_k(t) H_k(t)}$$

### 5.3 Rasio saat salah satu DEGRADED

| FO | LEO | $W_{FO}$ | $W_{LEO}$ |
|---|---|---:|---:|
| STABLE | STABLE | $QH$-based | $QH$-based |
| DEGRADED | STABLE | 0,15 | 0,85 |
| STABLE | DEGRADED | 0,85 | 0,15 |
| DEGRADED | DEGRADED | 0,50 | 0,50 |

**Override keselamatan:** jika satu link benar-benar *down* (bukan sekadar
DEGRADED), seluruh trafik dialihkan ke link yang hidup, meskipun melampaui
$b_{max}$. Ini adalah jalur *failover*, bukan operasi normal, dan dicatat terpisah.

### 5.4 Pemetaan ke bucket

```
input: W[1..2], N, b_min, b_max
1. b_i = round(N * W_i)
2. clamp b_i ke [b_min, b_max]
3. selisih = N - sum(b_i)
4. jika selisih > 0:
       tambahkan 1 ke link dengan sisa pecahan terbesar yang belum b_max
       ulangi sampai selisih = 0
5. jika selisih < 0:
       kurangi 1 dari link dengan sisa pecahan terkecil yang belum b_min
       ulangi sampai selisih = 0
6. jika langkah 4/5 tidak mungkin:
       fallback ke pembagian merata dan catat error
7. kembalikan b
```

**Jaminan:** $\sum b_i = N$ dan $b_{min} \le b_i \le b_{max}$ selama
$2 b_{min} \le N \le 2 b_{max}$.

**Contoh.** $N=20$, $b_{min}=3$, $b_{max}=17$.

| $W$ | $N W$ | Awal | Setelah koreksi |
|---|---:|---:|---|
| 0,766 | 15,33 | 15 | 15 |
| 0,234 | 4,67 | 5 | 5 |

Jika $W = (0{,}879;\ 0{,}121)$: $b = (18;2)$ → clamp menjadi $(17;3)$, jumlah 20.

---

## 6. Contoh Perhitungan Skor

Asumsikan nilai sudah dihaluskan EWMA.

| Metrik | FO | LEO |
|---|---:|---:|
| Throughput | 90 Mbps | 50 Mbps |
| Delay | 10 ms | 40 ms |
| Jitter | 2 ms | 8 ms |
| Loss | 0% | 1% |

Normalisasi:

| Kriteria | $r_{FO}$ | $r_{LEO}$ | Bobot |
|---|---:|---:|---:|
| Throughput | 0,900 | 0,500 | 0,35 |
| Delay | 0,933 | 0,733 | 0,30 |
| Jitter | 0,933 | 0,733 | 0,15 |
| Loss | 1,000 | 0,800 | 0,20 |

$$Q_{FO} = 0{,}935, \qquad Q_{LEO} = 0{,}665$$

Dengan utilisasi $u_{FO}=0{,}30$ dan $u_{LEO}=0{,}70$:

$$H_{FO}=0{,}70, \qquad H_{LEO}=0{,}30$$

$$W_{FO} = \frac{0{,}935 \times 0{,}70}{0{,}935 \times 0{,}70 + 0{,}665 \times 0{,}30}
= 0{,}766$$

$$W_{LEO} = 0{,}234 \quad\Rightarrow\quad b = (15;\ 5)$$

---

## 7. Preservasi Sesi dan `AFFINITY_LOCK`

| Direktif | Perilaku |
|---|---|
| `set_affinity(true)` | Aturan baru hanya berlaku untuk koneksi baru; conntrack lama tidak disentuh |
| `set_affinity(false)` | Aturan baru diterapkan, lalu entri conntrack yang terpengaruh di-*flush* selektif |
| `rollback(checkpoint)` | Kembalikan aturan sebelumnya; opsional flush entri baru |

**Definisi teknis "tanpa affinity":** setelah vektor bucket berubah, controller
menghapus entri conntrack yang *connection mark*-nya menunjuk ke bucket yang
berubah. Ini perlakuan yang disengaja dan berisiko; risikonya dicatat.

**Batas klaim:** preservasi sesi diuji, bukan diasumsikan. Jika RST tidak berbeda,
H3a dilaporkan tidak terdukung.

---

## 8. Kontrak Antarmuka

| Operasi | Input | Output | Idempoten | Error |
|---|---|:---:|---|
| `read_metrics(link_ids)` | daftar link | metrik + timestamp | Ya | `METRIC_UNAVAILABLE` |
| `get_state()` | — | state + $Q_i$ | Ya | — |
| `set_ratio(bucket_vector)` | vektor integer | ack + versi | Ya (vektor sama = no-op) | `INVALID_SUM`, `OUT_OF_BOUNDS` |
| `set_affinity(bool)` | boolean | ack | Ya | `UNSUPPORTED` |
| `verify(expected)` | vektor + state | boolean + diff | Ya | `VERIFY_TIMEOUT` |
| `rollback(checkpoint_id)` | id | ack | Ya | `CHECKPOINT_NOT_FOUND` |

**Aturan kontrak:** inti tidak boleh mengimpor API vendor secara langsung.
Adapter bertanggung jawab atas penerjemahan, verifikasi, dan rollback.

---

## 9. Pseudocode

```
init:
    warmup(60s)
    Q = compute_quality(read_metrics())
    apply_ratio(bucket_map(ratio_policy(Q)))

loop every Ts:
    m = read_metrics()
    E = ewma(m, alpha)
    Q = saw(E, weights, fixed_bounds)
    for i in links:
        update_state(i, Q[i], theta_low, theta_high, k_down, k_up)
    W = ratio_policy(states, Q, headroom)
    b = bucket_map(W, N, b_min, b_max)
    if b != current_bucket:
        if affinity_on:
            set_ratio(b)              # conntrack lama dipertahankan
        else:
            set_ratio(b)
            flush_affected(b)         # perlakuan tanpa affinity
        log_rule_change(b, timestamp)
    if now - last_force_eval > T_max:
        force_eval()
```

---

## 10. Kasus Tepi

| Kasus | Perilaku |
|---|---|
| Metrik hilang | Tahan state terakhir, catat `METRIC_UNAVAILABLE`, alarm |
| Kedua link DEGRADED | 50:50, evaluasi ulang lebih sering |
| Satu link down | 100% ke link hidup (override keselamatan) |
| Controller mati | *Fail-static*: konfigurasi terakhir tetap berlaku |
| $Q_i$ tidak valid (NaN) | Gunakan nilai EWMA terakhir; jika tidak ada, $Q_i=0$ |
| Normalisasi 0/0 | $\varepsilon = 10^{-6}$ |
| Bucket tidak layak | Fallback merata + catat error |

---

## 11. Tabel Parameter Final

| Parameter | Nilai | Justifikasi |
|---|---:|---|
| $T_s$ | 1 s | 15 sampel per transien |
| $\alpha$ | 0,20 | $N_{eff}=9$ |
| $\theta_{low}$ | 0,60 | Kalibrasi pilot |
| $\theta_{high}$ | 0,80 | *Dead zone* 0,20 |
| $k_{down}$ | 20 | $20 > 15+1$ |
| $k_{up}$ simetris | 20 | Simetri waktu |
| $k_{up}$ asimetris | 60 | Menahan pemulihan semu |
| $N$ | 20 | Granularitas 5% |
| $b_{min}$ | 3 | 15% |
| $b_{max}$ | 17 | 85% |
| $T_{max}$ | 10 menit | Degradasi lambat |
| $\lambda$ | 1,0 | Primer; sensitivitas 0,25/0,5/1,0 |
