# Roadmap Tahapan Proposal Tesis S2

**Judul kerja:** Kendali Proporsi Aliran Adaptif dan Sadar-Sesi pada WAN Heterogen FO–LEO
**Kandidat sistem:** SPA-HSM (*Session-Preserving Asymmetric Hysteresis State Machine*)
**Program:** Magister Teknik Informatika, Universitas Hasanuddin
**Status:** Kerangka kerja — diperbarui 12 November 2026
**Progres:** Tahap 0–5 selesai; draf Bab III tersedia. Berikutnya: konsolidasi Bab I–II dan naskah penuh.

---

## 1. Prinsip Penyusunan

Proposal S2 yang kuat bukan yang paling banyak memakai metode, tetapi yang paling
jelas menjawab tiga pertanyaan:

1. **Apa yang belum terjawab?** (gap)
2. **Mengapa cara yang ada belum menjawabnya?** (kegagalan pendekatan sebelumnya)
3. **Apa bukti baru yang akan dihasilkan?** (novelty dan kontribusi)

Karena itu urutan tahapan di bawah ini sengaja menempatkan **gap dan novelty
sebelum penulisan Bab I**. Bab I ditulis setelah posisi penelitian dikunci, bukan
sebelumnya.

---

## 2. Peta Tahapan

| Tahap | Nama | Durasi indikatif | Luaran utama | Gerbang lulus |
|---|---|---|---|---|
| 0 | Konsolidasi dan keputusan arah | 3–5 hari | Folder kerja, log keputusan, satu nama payung | Tidak ada dua istilah yang bersaing |
| 1 | Peta gap dan pernyataan novelty | 1–2 minggu | Peta gap, matriks SOTA, novelty statement, uji kelayakan | Gap dapat dinyatakan dalam satu paragraf dan novelty lulus 5 uji |
| 2 | Rumusan masalah, tujuan, hipotesis | 3–5 hari | RQ, tujuan, hipotesis operasional | Setiap tujuan menjawab satu RQ; setiap hipotesis punya metrik dan uji |
| 3 | Kerangka teori dan state of the art | 2 minggu | Bab II, taksonomi, 35–50 referensi | Setiap klaim faktual bersitasi; tidak ada klaim "belum ada" tanpa bukti |
| 3.5 | Evaluasi dan perbaikan | 2–3 hari | Laporan evaluasi, kebijakan tier, checklist | Tidak ada ambang bertabrakan; SOTA inti ≥ 15; log pencarian ada |
| 4 | Metodologi dan desain evaluasi | 2 minggu | Bab III, desain faktorial, rencana statistik | Setiap faktor terisolasi; ada baseline praktisi |
| 5 | Instrumen, etika, manajemen risiko | 1 minggu | Tabel instrumen, prosedur rollback, tabel risiko | Ada uji pilot dan jalur gagal-aman |
| 6 | Penulisan naskah proposal | 2 minggu | Draf lengkap Bab I–III + lampiran | Konsisten istilah, nomor, sitasi, format kampus |
| 7 | Uji kelayakan internal dan simulasi seminar | 1 minggu | Berkas pertanyaan penguji + revisi | Tidak ada pertanyaan novelty yang belum terjawab |
| 8 | Seminar proposal dan revisi | 2–4 minggu | Naskah final + matriks revisi | Semua catatan penguji terpetakan |

Total indikatif: **10–13 minggu** kerja efektif, di luar waktu tunggu jadwal seminar.

---

## 3. Rincian Tiap Tahap

### Tahap 0 — Konsolidasi dan keputusan arah

**Tujuan:** memastikan hanya ada satu objek penelitian, satu nama payung, dan satu
lingkup yang tidak berubah di tengah jalan.

**Aktivitas**
- Memindahkan seluruh materi lama ke `00_Arsip_Proposal_SPA-HSM/`.
- Menetapkan nama payung (SPA-HSM) dan menghapus istilah pesaing (ALQI, TLABA).
- Menetapkan posisi MikroTik: *testbed/adapter*, bukan objek algoritma.
- Menetapkan topologi: dual-ISP FO–LEO, satu lokasi lapangan.

**Luaran:** `01_Log_Keputusan.md` terisi.

**Gerbang lulus:** tidak ada dua istilah atau dua lingkup yang saling bertentangan
di dokumen mana pun.

---

### Tahap 1 — Peta gap dan pernyataan novelty

**Tujuan:** menghasilkan gap yang spesifik, terverifikasi, dan novelty yang bukan
sekadar "kombinasi metode".

**Aktivitas**
- Menyusun matriks state of the art pada tujuh dimensi.
- Memisahkan empat jenis gap: *evidence, method, integration, context*.
- Menulis satu paragraf gap statement dan tiga klaim novelty.
- Menguji novelty dengan lima pertanyaan kelayakan.
- Menyiapkan jawaban atas keberatan penguji: "ini hanya integrasi".

**Luaran:** empat dokumen di `02_Tahap_01_Gap_dan_Novelty/`.

**Gerbang lulus:**
- Gap dapat dijelaskan dalam 60 detik tanpa membaca slide.
- Novelty punya pembanding eksplisit dan bukti yang akan dihasilkan.
- Ada minimal satu kontribusi yang bukan sekadar penggabungan.

---

### Tahap 2 — Rumusan masalah, tujuan, hipotesis

**Tujuan:** menerjemahkan gap menjadi pertanyaan yang dapat dijawab dan hipotesis
yang dapat diuji.

**Aktivitas**
- Menulis 1 pertanyaan payung + 3–4 sub-pertanyaan.
- Menyusun tujuan yang satu-satu memetakan ke sub-pertanyaan.
- Menulis hipotesis dengan variabel, metrik, uji, ambang, dan arah.
- Menetapkan definisi operasional: *flap*, *effective rule change*, RST rate,
  goodput, episode degradasi.

**Gerbang lulus:** tidak ada tujuan tanpa RQ, tidak ada hipotesis tanpa ambang
numerik, dan tidak ada metrik yang definisinya berubah antar-skenario.

---

### Tahap 3 — Kerangka teori dan state of the art

**Tujuan:** membangun dasar teori yang cukup untuk membenarkan setiap pilihan desain.

**Aktivitas**
- Taksonomi: QoS, PCC/ECMP/NTH, MCDM/SAW, EWMA, histeresis, conntrack,
  SD-WAN, Starlink, pola adapter.
- Menyusun tabel "klaim → sumber → kekuatan bukti".
- Menulis sintesis, bukan ringkasan per paper.
- Menutup celah sitasi pada klaim 15 detik, rain fade, dan bufferbloat FO.

**Gerbang lulus:** 35–50 referensi relevan; setiap klaim faktual punya sitasi;
tidak ada referensi yang hanya muncul di daftar pustaka.

---

### Tahap 4 — Metodologi dan desain evaluasi

**Tujuan:** memastikan hasil penelitian dapat dipercaya dan direplikasi.

**Aktivitas**
- Menetapkan desain faktorial (histeresis × affinity) dan baseline praktisi.
- Menyusun urutan run acak/counterbalanced, washout, dan blok waktu.
- Menetapkan *primary* dan *secondary outcome*.
- Memilih uji statistik yang sesuai: mixed-effects/GEE, Poisson/NB, bootstrap.
- Menetapkan jumlah replikasi dan *minimum detectable effect*.
- Memisahkan evaluasi kausal di staging dan validasi di lapangan.

**Gerbang lulus:** setiap perbandingan mengubah satu faktor; tidak ada t-test
sebagai default; ada justifikasi jumlah run.

---

### Tahap 5 — Instrumen, etika, dan manajemen risiko

**Tujuan:** memastikan pengukuran valid dan eksperimen aman pada jaringan produksi.

**Aktivitas**
- Menyusun tabel instrumen: metrik, alat, *vantage point*, rumus, interval.
- Menetapkan probe per WAN, SNMP, telemetri Starlink, dan Wireshark.
- Menyiapkan *fail-static*, watchdog, backup, dan prosedur rollback yang diuji.
- Menyusun etika: izin pemilik, anonimisasi, larangan menangkap payload.
- Menyusun tabel risiko dan mitigasi.

**Gerbang lulus:** ada pilot 24–48 jam untuk kalibrasi instrumen; rollback
dibuktikan, bukan hanya ditulis.

---

### Tahap 6 — Penulisan naskah proposal

**Tujuan:** menghasilkan naskah yang konsisten dan sesuai template kampus.

**Aktivitas**
- Menulis Bab I–III dari dokumen tahap 1–5, bukan dari nol.
- Menambahkan abstrak Indonesia–Inggris, daftar simbol, daftar singkatan.
- Menomori rumus, tabel, gambar, dan memastikan semuanya dirujuk.
- Menyusun jadwal penelitian dan daftar pustaka.
- Audit konsistensi istilah dan angka.

**Gerbang lulus:** tidak ada placeholder; daftar isi/tabel/gambar akurat; format
sesuai `00_Arsip_Proposal_SPA-HSM/panduan_penulisan/`.

---

### Tahap 7 — Uji kelayakan internal dan simulasi seminar

**Tujuan:** menemukan kelemahan sebelum penguji menemukannya.

**Aktivitas**
- Menyusun 30 pertanyaan penguji dan jawabannya.
- Simulasi 20 menit + sesi tanya jawab.
- Meminta satu pembaca luar menilai kejelasan gap dan novelty.
- Menyiapkan slide: masalah → gap → novelty → metode → bukti yang dijanjikan.

**Gerbang lulus:** semua pertanyaan novelty, kelayakan, dan etika punya jawaban
ringkas yang didukung bukti.

---

### Tahap 8 — Seminar proposal dan revisi

**Tujuan:** lulus seminar dan mengunci lingkup untuk penelitian.

**Aktivitas**
- Seminar.
- Mencatat setiap catatan penguji ke matriks revisi.
- Memisahkan revisi wajib, opsional, dan di luar lingkup.
- Memperbarui log keputusan dan roadmap.

**Gerbang lulus:** semua catatan wajib tertutup dan disetujui pembimbing.

---

## 4. Titik Kendali Risiko

| Risiko | Tahap deteksi | Tindakan |
|---|---|---|
| Novelty dinilai hanya integrasi | 1 | Tambah kontribusi analitis/metrik, bukan hanya arsitektur |
| Gap "belum ada penelitian" tidak terbukti | 1, 3 | Dokumentasikan strategi pencarian dan hasil pencarian |
| Lingkup melebar (multi-ISP, multi-vendor, QoE) | 2 | Kunci batasan di log keputusan |
| Desain ablasi tidak mengisolasi faktor | 4 | Faktorial 2×2 + 2 pembanding + baseline praktisi |
| Data lapangan tidak cukup | 4, 5 | Evaluasi kausal di staging + replikasi |
| Klaim sesi tidak terbukti | 4, 5 | Ukur RST, jangan asumsikan |
| Etika/izin terlambat | 5 | Urus izin sebelum pilot |

---

## 5. Definisi Selesai

Proposal dinyatakan siap seminar jika:

- [ ] Satu nama payung dan satu lingkup, konsisten di seluruh dokumen.
- [ ] Gap statement dapat dinyatakan dalam satu paragraf.
- [ ] Novelty punya pembanding eksplisit dan minimal satu kontribusi non-integrasi.
- [ ] Setiap RQ punya tujuan, hipotesis, metrik, dan uji.
- [ ] Setiap faktor ablasi terisolasi.
- [ ] Ada baseline praktisi dan rencana statistik yang sesuai.
- [ ] Ada prosedur etika, rollback, dan fail-safe yang diuji.
- [ ] Tidak ada klaim tanpa sitasi atau bukti.
