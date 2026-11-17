# Tahap 2 — Rumusan Masalah dan Tujuan

**Dokumen:** `01_Rumusan_Masalah_dan_Tujuan.md`
**Status:** Draf kerja Tahap 2 — diperbarui 17 November 2026
**Arah penelitian:** Modifikasi fungsi kontrol + alokasi *stock-flow aware* + SIWG
**Fungsi:** Menerjemahkan gap Tahap 1 menjadi pertanyaan payung, sub-pertanyaan,
dan tujuan yang saling memetakan satu-satu.

---

## 1. Pertanyaan Penelitian Payung

> Bagaimana mekanisme kontrol adaptif pada WAN heterogen FO–LEO dapat
> **memodifikasi cara mengamati kualitas ISP, mendeteksi degradasi, menghitung
> ulang persentase alokasi koneksi baru dengan mempertimbangkan stok koneksi lama,
> dan mempertahankan koneksi yang telah terbentuk**, sehingga trade-off antara
> stabilitas keputusan, kontinuitas sesi, dan kinerja agregat dapat dikendalikan?

Pertanyaan ini sengaja menyebut **modifikasi fungsi kontrol**, bukan “merancang
kontroler” atau “PCC dinamis”. Yang dimodifikasi adalah kebijakan yang menentukan
kapan dan seberapa besar alokasi koneksi baru diubah, dengan tetap menghormati
koneksi lama yang tidak dapat dipindahkan.

---

## 2. Sub-Pertanyaan Penelitian

| Kode | Pertanyaan | Gap | Sifat |
|---|---|---|---|
| **RQ1** | Bagaimana memodifikasi persepsi kualitas menjadi $Q_i(t)$ berbasis EWMA–SAW dan memetakannya ke bucket PCC diskret? | G-M2 | Formalisasi |
| **RQ2** | Bagaimana memodifikasi deteksi degradasi dengan histeresis asimetris dan *dwell* yang diturunkan dari durasi transien LEO? | G-M1 | Metodologis |
| **RQ3** | Bagaimana memodifikasi perlakuan sesi sehingga koneksi lama dipertahankan dan koneksi baru diarahkan tanpa pemutusan paksa? | G-E2 | Metodologis/empiris |
| **RQ4** | Bagaimana memodifikasi kebijakan alokasi agar mempertimbangkan stok koneksi lama $S_i(t)$ dan aliran koneksi baru $F_i(t)$, dan seberapa besar pengaruhnya terhadap *effective load skew* dan *time-to-rebalance*? | **G-M3** | **Utama** |
| **RQ5** | Seberapa besar modifikasi tersebut menurunkan flapping dan RST serta meningkatkan SIWG berdasarkan ablasi A–H pada konteks FO–LEO? | G-E1, G-I1, G-C1 | Empiris/komparatif |
| **RQ6** | Apakah mekanisme hasil modifikasi memenuhi kontrak antarmuka dan menghasilkan keputusan identik pada dua adapter? | G-C2 | Rekayasa |

**Aturan:** tidak ada sub-pertanyaan yang hanya bisa dijawab “ya/tidak”. Setiap
RQ harus menghasilkan angka, model, atau artefak yang dapat diperiksa.

---

## 3. Tujuan Penelitian

### Tujuan umum

Memodifikasi fungsi kontrol di atas kapabilitas PCC statis dan *conntrack* yang
tersedia pada platform, sehingga mekanisme hasil modifikasi—SPA-HSM—dapat
mengelola trade-off stabilitas keputusan, kontinuitas sesi, dan kinerja agregat
pada WAN heterogen FO–LEO.

### Tujuan khusus

| Kode | Tujuan | Menjawab | Luaran terukur |
|---|---|---|---|
| **T1** | Memodifikasi persepsi kualitas: $Q_i(t)$ berbasis EWMA–SAW dan pemetaan ke bucket PCC. | RQ1 | Rumus, tabel parameter, uji granularitas |
| **T2** | Memodifikasi deteksi degradasi: histeresis dua ambang + *dwell* sadar-transien. | RQ2 | Aturan *dwell*, kurva trade-off |
| **T3** | Memodifikasi perlakuan sesi: preservasi koneksi lama dan pengarahan koneksi baru. | RQ3 | Mekanisme, RST flow, session retention |
| **T4** | **Memodifikasi kebijakan alokasi menjadi *stock-flow aware*** dengan $S_i(t)$, $F_i(t)$, dan koreksi $\kappa$. | **RQ4** | Rumus $W_i$, ELS, time-to-rebalance |
| **T5** | Mengevaluasi kontribusi modifikasi melalui ablasi A–H dan SIWG. | RQ5 | Dataset, effect size, peringkat SIWG |
| **T6** | Menguji kontrak *Abstract Allocation Interface* dan portabilitas inti. | RQ6 | Uji konformitas, keputusan identik |

---

## 4. Matriks Alinyemen

| Gap | RQ | Tujuan | Hipotesis | Metrik utama | Bab |
|---|---|---|---|---|---|
| G-M2 | RQ1 | T1 | — (formalisasi) | Galat bucket, stabilitas granularitas | I, II |
| G-M1 | RQ2 | T2 | H1, H2 | Flapping, recovery p95 | I, II |
| G-E2 | RQ3 | T3 | H3a | RST flow, session retention | I, II |
| **G-M3** | **RQ4** | **T4** | **H3c** | **ELS, time-to-rebalance** | I, II |
| G-E1, G-I1, G-C1 | RQ5 | T5 | H3b, H4 | Goodput, latency, SIWG | I, II |
| G-C2 | RQ6 | T6 | H5 | Kesesuaian antarmuka | I, II |

**Uji konsistensi:** setiap RQ punya tepat satu tujuan; setiap tujuan punya
minimal satu hipotesis atau luaran formal; setiap hipotesis punya metrik dan uji.

---

## 5. Batas Pertanyaan

| Hal yang tidak ditanyakan | Alasan |
|---|---|
| Apakah SPA-HSM lebih baik dari semua algoritma *load balancing*? | Tidak dapat diuji dengan satu penelitian |
| Apakah sistem dapat memprediksi degradasi sebelum terjadi? | Di luar lingkup; mekanisme bersifat reaktif |
| Apakah pengguna merasa lebih puas (QoE)? | Penelitian mengukur QoS, bukan persepsi |
| Apakah metode ini optimal secara global? | Tidak ada klaim optimalitas |
| Apakah bobot SAW sebaiknya dipelajari otomatis? | Bobot statis (K-03) |
| Apakah sistem bekerja pada semua vendor? | Satu adapter nyata + mock (K-04) |
| Apakah koneksi lama dipindahkan paksa? | Tidak; preservasi sesi adalah batasan |

---

## 6. Kriteria Jawaban yang Memuaskan

| RQ | Jawaban dianggap memuaskan jika |
|---|---|
| RQ1 | Semua simbol terdefinisi; $\sum b_i=N$ untuk 10.000 kombinasi uji; tidak ada pelanggaran $b_{min}/b_{max}$ |
| RQ2 | Ada aturan eksplisit yang menghubungkan $T_s$, $T_{tr}$, dan $k_{down}$; kurva trade-off dihasilkan |
| RQ3 | Koneksi lama tetap; RST flow dan session retention terukur |
| RQ4 | ELS dan time-to-rebalance turun dibanding alokasi kualitas saja; $\kappa$ diuji sensitivitasnya |
| RQ5 | Ada effect size dan 95% CI; SIWG dihitung dengan sensitivitas $\lambda$ |
| RQ6 | Ada matriks konformitas dan perbandingan urutan keputusan |

---

## 7. Rumusan Masalah untuk Naskah

> Pengelolaan proporsi trafik PCC pada WAN heterogen FO–LEO masih bertumpu pada
> rasio statis yang tidak merespons degradasi link secara *real-time*. Pembaruan
> rasio secara naif menimbulkan flapping, dan karena PCC bersifat *session-oriented*,
> koneksi lama dapat menumpuk pada link yang sedang memburuk. Penelitian ini
> memodifikasi fungsi kontrol di atas kapabilitas PCC: mengamati kualitas ISP,
> mendeteksi degradasi sustained, menghitung ulang persentase koneksi baru dengan
> mempertimbangkan stok koneksi lama, dan mempertahankan koneksi yang telah
> terbentuk. Mekanisme hasil modifikasi dievaluasi melalui flapping, RST, goodput,
> latensi, ELS, time-to-rebalance, dan SIWG.

---

## 8. Yang Dibutuhkan Sebelum Tahap 3

- [ ] Konfirmasi pembimbing atas enam sub-RQ.
- [ ] Konfirmasi kondisi H (*stock-aware*) dan H3c.
- [ ] Konfirmasi ketersediaan data *conntrack* per *connection mark*.
- [ ] Konfirmasi judul kerja baru.
