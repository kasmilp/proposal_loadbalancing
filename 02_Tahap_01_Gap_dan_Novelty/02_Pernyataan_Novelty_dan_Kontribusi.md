# Tahap 1 — Pernyataan Novelty dan Kontribusi

**Dokumen:** `02_Pernyataan_Novelty_dan_Kontribusi.md`
**Status:** Draf kerja Tahap 1
**Fungsi:** Mengubah gap menjadi klaim kebaruan yang dapat dipertahankan.

---

## 1. Prinsip

Novelty bukan "metode yang belum pernah dipakai". Novelty adalah **klaim bahwa
pengetahuan atau kemampuan baru akan dihasilkan**, disertai pembanding dan bukti.

Rumus yang dipakai:

> **Berbeda dari** [pembanding], **penelitian ini** [apa yang dilakukan],
> **sehingga** [kemampuan/bukti baru yang sebelumnya tidak tersedia].

Setiap klaim di bawah ini harus lolos rumus tersebut.

---

## 2. Novelty Statement (Satu Paragraf)

> Penelitian ini tidak mengklaim menemukan metode MCDM, EWMA, atau histeresis yang
> baru. Kebaruannya terletak pada **pengendalian trade-off antara stabilitas
> keputusan dan kontinuitas sesi** pada WAN heterogen FO–LEO: parameter histeresis
> diturunkan dari durasi transien LEO yang terukur, skor kualitas kontinu
> dipetakan secara formal ke proporsi PCC diskret, dan dampaknya terhadap flapping
> serta integritas sesi TCP dipisahkan melalui ablasi faktorial. Dengan demikian,
> penelitian ini menghasilkan **aturan perancangan dan bukti empiris** yang belum
> tersedia, bukan sekadar penggabungan empat komponen yang sudah dikenal.

---

## 3. Empat Klaim Kebaruan

### N1 — Kontribusi konseptual: stabilitas–kontinuitas sebagai satu masalah kendali

**Klaim.** Flapping dan gangguan sesi diperlakukan sebagai dua kendala yang
diselesaikan bersama, bukan dua masalah terpisah.

**Pembanding.** Studi PCC yang ada mengoptimalkan QoS agregat dan mengasumsikan
konsistensi sesi otomatis terjaga (Amalia et al., 2022; Arfianita et al., 2024;
Nugroho et al., 2023). Studi histeresis mengoptimalkan osilasi keputusan tanpa
memodelkan dampak sesi (Tournaire et al., 2023).

**Bukti yang dihasilkan.** Rumusan kendali dengan dua batasan: laju perubahan
aturan efektif dan laju gangguan sesi, serta analisis *trade-off* antara keduanya.

**Kekuatan:** tinggi, karena mengubah cara masalah dirumuskan.

---

### N2 — Kontribusi metodologis: aturan dwell yang sadar-transien LEO

**Klaim.** Parameter histeresis tidak ditetapkan *ad hoc*, tetapi diturunkan dari
hubungan antara interval sampling, durasi transien, dan jumlah sampel berturut-turut.

**Pembanding.** Parameter histeresis pada literatur *auto-scaling* dipilih
berdasarkan simulasi beban, bukan karakteristik fisik link (Tournaire et al., 2023).
Studi Starlink mengarakterisasi transien sekitar 15 detik, tetapi tidak
menerjemahkannya menjadi parameter kendali (Garcia et al., 2025; Hammer et al., 2024;
Mohan et al., 2024).

**Bukti yang dihasilkan.** Aturan `k_down × T_s > durasi transien` (dengan margin),
tabel parameter yang dapat dikalibrasi, dan analisis aliasing.

**Kekuatan:** tinggi, karena dapat diuji secara analitis dan eksperimental.

**Catatan penting.** Ini adalah klaim paling kuat dan paling mudah dipertahankan.
Letakkan di depan saat seminar.

---

### N3 — Kontribusi empiris: ablasi yang memisahkan bentuk histeresis dan preservasi sesi

**Klaim.** Penelitian ini menghasilkan bukti kuantitatif tentang kontribusi
masing-masing komponen terhadap flapping, TCP RST rate, goodput, dan latensi p95.

**Pembanding.** Studi PCC membandingkan metode secara statis (PCC vs ECMP vs NTH),
bukan mengablationkan komponen internal (Nugroho et al., 2023; Mirsal dan Agtriadi,
2026). Studi yang mengklaim preservasi sesi tidak mengukur RST.

**Bukti yang dihasilkan.** Desain faktorial 2×2 (simetris/asimetris × affinity
off/on) ditambah pembanding statis dan dynamic naive, dengan unit analisis episode
degradasi.

**Kekuatan:** tinggi, karena langsung menjawab G-E1.

**Prasyarat:** mekanisme "tanpa affinity" harus didefinisikan teknis dan tidak
dibuat gagal secara artifisial.

---

### N4 — Kontribusi rekayasa: kontrak antarmuka yang dapat diuji

**Klaim.** Logika keputusan dipisahkan dari eksekusi melalui kontrak abstrak,
sehingga dapat diuji dengan *mock adapter* sebelum menyentuh jaringan produksi.

**Pembanding.** Implementasi PCC praktis tertanam pada konfigurasi vendor dan
sulit direplikasi (MikroTik, n.d.; Putra dan Anton, 2024).

**Bukti yang dihasilkan.** Spesifikasi antarmuka, *mock adapter*, uji konformitas,
dan bukti keputusan identik pada dua adapter.

**Kekuatan:** sedang. Ini kontribusi pendukung, bukan novelty utama. Jangan
mengklaim "platform-independent" — gunakan "dirancang portabel dan diuji melalui
kontrak antarmuka".

---

## 4. Mengapa Ini Bukan Sekadar Integrasi

Keberatan yang paling mungkin muncul: *"Ini hanya menggabungkan EWMA, SAW,
histeresis, dan PCC."*

Jawaban yang harus disiapkan:

| Keberatan | Jawaban |
|---|---|
| "Tinggal menempelkan empat metode." | Yang baru bukan penempelannya, tetapi **aturan penurunan parameter** (N2) dan **pengukuran trade-off** (N1/N3). Tanpa N2, integrasi memang inkremental. |
| "Histeresis sudah lama ada." | Histeresis yang ada tidak diturunkan dari transien LEO dan tidak memperhitungkan biaya sesi. Asimetri waktu di sini berfungsi sebagai instrumen kendali, bukan sekadar ambang. |
| "SAW sudah biasa." | SAW dipakai sebagai penyeragam skor agar dapat dibandingkan antar-waktu; kontribusinya bukan pada SAW, melainkan pada pemetaan skor ke bucket diskret (G-M2). |
| "PCC sudah menangani sesi." | Itu asumsi yang justru diuji (G-E1). Jika benar, H2a akan menunjukkan non-inferioritas — hasil negatif yang tetap bernilai. |
| "Tidak ada metode baru." | Benar, dan itu bukan klaim. Klaimnya adalah **aturan desain + bukti empiris**. |

**Aturan presentasi:** sebut lebih dulu apa yang **bukan** klaim, lalu sebut
kontribusi yang diklaim. Ini menurunkan ekspektasi penguji dan meningkatkan
kredibilitas.

---

## 5. Peta Kontribusi

| Kode | Kontribusi | Jenis | Gap yang dijawab | Bukti |
|---|---|---|---|---|
| K1 | Formulasi SPA-HSM: EWMA + SAW + histeresis asimetris + affinity | Konseptual/artefak | G-I1 | Formalisasi, pseudocode, tabel parameter |
| K2 | Aturan dwell sadar-transien dan analisis aliasing | Metodologis | G-M1 | Turunan aturan, analisis sensitivitas, replay trace |
| K3 | Formalisasi pemetaan skor → bucket PCC | Metodologis | G-M2 | Rumus, contoh perhitungan, uji granularitas |
| K4 | Bukti ablasi terhadap flapping, RST, goodput, latensi | Empiris | G-E1, G-C1 | Dataset, uji statistik, effect size |
| K5 | Kontrak antarmuka + mock adapter | Rekayasa | G-C2 | Uji konformitas, H3 |
| K6 | Metrik *Session-Impact-Weighted Goodput* (SIWG) | Metrik/evaluasi | G-E1, G-I1 | Rumus, analisis sensitivitas λ, peringkat skenario |

**Kontribusi utama yang harus dipertahankan:** **K2 + K4**.
**Kontribusi pendukung:** K1, K3, K5.

---

## 6. Elevator Pitch (60 Detik)

> "PCC pada MikroTik membagi trafik dengan rasio statis. Ketika Starlink mengalami
> transien sekitar 15 detik, rasio statis tetap mengirim trafik ke jalur yang sedang
> buruk. Solusi naif — memperbarui rasio setiap siklus — menimbulkan flapping dan
> berpotensi mengganggu sesi TCP. Penelitian ini mengusulkan SPA-HSM: skor kualitas
> dihaluskan, histeresis asimetris dengan dwell yang diturunkan dari durasi transien,
> dan preservasi sesi melalui affinity lock. Yang baru bukan metode dasarnya, tetapi
> aturan penurunan parameter dan bukti ablasi yang memisahkan kontribusi flapping
> dan gangguan sesi pada WAN FO–LEO."

---

## 7. Batas Klaim

Hal-hal berikut **tidak** diklaim:

- Tidak mengklaim metode MCDM, EWMA, atau histeresis baru.
- Tidak mengklaim generalisasi ke lebih dari dua ISP.
- Tidak mengklaim portabilitas terbukti ke semua vendor.
- Tidak mengklaim menggantikan SD-WAN enterprise.
- Tidak mengklaim kestabilan formal *control loop*.
- Tidak mengklaim QoE atau kepuasan pengguna.

---

## 8. Opsi Penguatan Novelty (Jika Diperlukan)

Jika pembimbing menilai novelty masih lemah, ada dua penguatan yang masih
terjangkau:

### Opsi A — Tambahkan batas analitis flapping

Turunkan batas atas jumlah transisi state per jam sebagai fungsi dari `α`,
`θ_low`, `θ_high`, `k_down`, `k_up`, dan varians derau. Ini mengubah kontribusi
dari "eksperimental" menjadi "analitis + eksperimental".

- **Kelebihan:** novelty naik signifikan.
- **Risiko:** membutuhkan asumsi derau yang harus dipertahankan.
- **Kelayakan:** sedang; bisa dibatasi pada kasus derau Gaussian dan replay trace.

### Opsi B — Usulkan metrik gabungan *session-impact-weighted goodput*

Metrik yang memasukkan biaya gangguan sesi ke dalam goodput, sehingga dua strategi
dapat dibandingkan dengan satu angka.

- **Kelebihan:** mudah dikomunikasikan dan menonjolkan trade-off.
- **Risiko:** pembobotan bisa diperdebatkan; harus disertai analisis sensitivitas.
- **Kelayakan:** tinggi.

**Rekomendasi:** ambil **Opsi B** sebagai kontribusi tambahan, dan **Opsi A**
sebagai lampiran analitis jika waktu memungkinkan. Jangan menunda Tahap 2 hanya
untuk mengejar Opsi A.

**Keputusan 12-11-2026:** **Opsi B diadopsi** dan diberi nama SIWG
(*Session-Impact-Weighted Goodput*). Rumus, definisi operasional, dan hipotesisnya
berada di `03_Tahap_02_Rumusan_Masalah/02_Hipotesis_dan_Definisi_Operasional.md`.
Opsi A tetap menjadi cadangan jika penguji meminta kontribusi analitis tambahan.
