# Matriks Konsistensi Bab I–III

**Dokumen:** `03_Matriks_Konsistensi_Bab_I-III.md`
**Fungsi:** Memastikan istilah, angka, dan klaim sama di tiga bab.
**Cara pakai:** Periksa tabel ini setiap kali salah satu bab diubah.

---

## 1. Istilah Baku

| Istilah | Bentuk baku | Jangan dipakai |
|---|---|---|
| Nama sistem | **SPA-HSM** | ALQI, TLABA |
| Skor kualitas | **$Q_i(t)$** | ALQI, skor kualitas link (tanpa simbol) |
| Metrik gabungan | **SIWG** | *session score*, *weighted QoS* |
| Perubahan aturan | ***effective PCC rule change*** | *rule change* (tanpa "effective") |
| Flap | **flap** (peristiwa), **flapping rate** (laju) | *flapping* untuk peristiwa tunggal |
| Episode | **episode degradasi** | *event*, *outage* (kecuali benar-benar outage) |
| Waktu pemulihan | ***recovery latency*** | *recovery time* |
| RST | **RST flow** (proporsi 0–1), **RST flow %** (persen) | mencampur proporsi dan persen |
| Direktif | **`AFFINITY_LOCK`** (kode), *affinity lock* (prosa) | *session lock* |
| Baseline | **baseline G** | “baseline H” (H = kondisi stock-aware) |
| Platform | **MikroTik sebagai adapter/testbed** | "PCC MikroTik" sebagai objek |
| Desain | **faktorial 2×2 + pembanding + H** | faktorial 3×2 penuh |
| Alokasi | ***stock-flow aware*** | “PCC dinamis” sebagai novelty |
| Stok koneksi | **$S_i(t)$** | “jumlah sesi” tanpa simbol |
| Aliran baru | **$F_i(t)$** | “trafik baru” tanpa pembeda |
| Beban efektif | **$L_i(t)$** | “rasio” tanpa konteks |
| Rebalance | **ELS**, **time-to-rebalance** | “load balance” tanpa metrik |
| Sesi lama | **session retention** | “session preservation” tanpa angka |

---

## 2. Angka Baku

| Parameter | Nilai | Muncul di |
|---|---:|---|
| $T_s$ | 1 detik | Bab I (implisit), II, III |
| $\alpha$ | 0,20 | Bab II, III |
| $\theta_{low}$ | 0,60 | Bab II, III |
| $\theta_{high}$ | 0,80 | Bab II, III |
| $k_{down}$ | 20 | Bab II, III |
| $k_{up}$ simetris | 20 | Bab III |
| $k_{up}$ asimetris | 60 | Bab III |
| $N$ | 20 bucket | Bab II, III |
| $b_{min}$ / $b_{max}$ | 3 / 17 | Bab III |
| $R_{max}$ | 90 detik | Bab I, II, III |
| $\lambda$ primer | 1,0 | Bab I, II, III |
| $\kappa$ | 0 / 0,5 / 1,0 | Bab III |
| $W_{\min}/W_{\max}$ | 0,15 / 0,85 | Bab III |
| Jumlah kondisi | 8 (A–H) | Bab I, III |
| Episode per kondisi | 30 | Bab III |
| Durasi kampanye | 22 minggu | Bab III |

**Pengecualian yang sah:** "60 detik" hanya boleh muncul sebagai waktu pemulihan
`netwatch` pada baseline G, bukan sebagai batas *recovery latency* H1/H2.

---

## 3. Peta Alinyemen Antar-Bab

| RQ | Bab I | Bab II | Bab III | Hipotesis |
|---|---|---|---|---|
| RQ1 | 1.2 butir 1 | 2.5, 2.10.2 | 3.5.1, 3.5.2, 3.5.4 | — |
| RQ2 | 1.2 butir 2 | 2.7, 2.10.3 | 3.5.3, 3.4.2 | H1, H2 |
| RQ3 | 1.2 butir 3 | 2.8, 2.8.1 | 3.5.5, 3.6 | H3a |
| **RQ4** | **1.2 butir 4** | **2.8.2, 2.11** | **3.5.4, 3.8** | **H3c** |
| RQ5 | 1.2 butir 5 | 2.10.4, 2.11 | 3.4, 3.6.3, 3.8 | H3b, H4 |
| RQ6 | 1.2 butir 6 | 2.9 | 3.5.6 | H5 |

---

## 4. Klaim yang Dilarang

| Klaim | Alasan | Ganti dengan |
|---|---|---|
| "PCC adalah state of the art" berdasarkan Nugroho/Mirsal/Putra | T3, jurnal lokal | "Pada konteks RT/RW Net, PCC..." |
| "Belum ada penelitian di dunia" | Tidak dapat dibuktikan | "Belum ditemukan studi yang..." + log pencarian |
| "PCC selalu merusak sesi" | Tidak terbukti | "Perubahan rasio berpotensi mengganggu sesi; hal ini diukur" |
| "Sistem terbukti portabel" | Hanya satu adapter nyata | "Dirancang portabel dan diuji melalui kontrak" |
| "Histeresis menjamin stabilitas" | Tidak ada bukti formal | "Histeresis menurunkan flapping secara empiris" |
| "SIWG adalah standar" | Metrik internal | "SIWG adalah alat pembanding internal" |
| "Faktorial 3×2" | Desain aktual 2×2 + pembanding + H | "Faktorial 2×2 + pembanding + H" |
| “PCC dinamis adalah novelty” | PCC hanya aktuator | "Novelty adalah alokasi *stock-flow aware*" |
| “Kontroler adaptif yang identik sudah beroperasi” | Tidak dapat dibuktikan | "Memodifikasi fungsi kontrol di atas kapabilitas platform" |
| “Merancang kontroler/Starlink/PCC” | Bukan objek penelitian | "Memodifikasi fungsi kontrol" |
| “Session preservation sudah selesai” | Koneksi lama bisa menumpuk | "Preservasi diukur melalui session retention dan ELS" |

---

## 5. Hasil Pemeriksaan

| Pemeriksaan | Status | Catatan |
|---|---|---|
| Satu nama sistem | Lulus | SPA-HSM saja |
| ALQI/TLABA tidak muncul | Lulus | Tidak ada di Bab I–III |
| Batas recovery konsisten | Lulus | 90 detik |
| RST proporsi vs persen | Lulus | Didefinisikan terpisah |
| Jumlah kondisi konsisten | Lulus | 8 kondisi A–H |
| Desain 2×2 + H konsisten | Lulus | Bab I, III, evaluasi |
| H1 mengisolasi affinity | Lulus | B vs C/D |
| H3a kriteria primer/sekunder | Lulus | Non-inferior primer |
| **H3c stock-flow** | Lulus | H vs F; ELS/TTR/RST/retention |
| **Stock-flow terms** | Lulus | S_i, F_i, L_i, κ, ELS, TTR |
| SIWG muncul di tiga bab | Lulus | Bab I, II, III |
| Klaim SOTA vs konteks | Sebagian | P-02 sudah; tambahan tetap terbuka |
| Klaim "belum ditemukan" | Sebagian | P-01 OpenAlex selesai; Scopus/IEEE belum |
| Angka rain fade/15 detik | Lulus | P-04 selesai (hlm. 5 / hlm. 1) |
| Gaya sitasi | Belum | D-10 |

---

## 6. Tindakan Berikutnya

1. Jalankan P-05 (audit sitasi) sebelum naskah final.
2. Tambah **P-06**: pencarian literatur *stock-flow/session-aware allocation*.
3. Konfirmasi D-10 (APA 7) ke pedoman kampus.
4. Kunci judul kerja baru dan perbarui abstrak.
5. Setelah itu, kunci naskah dan lanjut ke daftar isi/tabel/gambar.
