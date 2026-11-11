# Tahap 4 — Jadwal, Risiko, dan Etika

**Dokumen:** `05_Jadwal_Risiko_dan_Etika.md`
**Status:** Draf kerja Tahap 4
**Fungsi:** Memastikan penelitian dapat dijalankan tanpa membahayakan jaringan
produksi dan selesai dalam waktu yang realistis.

---

## 1. Jadwal Indikatif

Total: **20 minggu** (di luar waktu tunggu seminar dan revisi).

| Minggu | Aktivitas | Luaran |
|---:|---|---|
| 1–2 | Finalisasi desain, kontrak antarmuka, `MockAdapter` | Spesifikasi dan mock |
| 3–4 | Pilot 24–48 jam, kalibrasi instrumen, uji RST | Laporan pilot |
| 5–6 | Replay staging A–G | Dataset staging |
| 7 | Perbaikan parameter berdasarkan pilot | Parameter final |
| 8–13 | Kampanye lapangan (6 minggu) | Dataset lapangan |
| 14 | Pembersihan dan audit data | Dataset bersih |
| 15–17 | Analisis statistik dan robustness | Tabel hasil |
| 18–19 | Penulisan Bab IV–V | Draf hasil |
| 20 | Konsolidasi, cek format, reproduksibilitas | Naskah siap seminar |

### 1.1 Milestone

| Milestone | Kriteria |
|---|---|
| M1 — Instrumen siap | Pilot lulus 7 uji kalibrasi |
| M2 — Staging selesai | 20 replay per kondisi |
| M3 — Lapangan selesai | ≥ 10 episode lapangan per kondisi |
| M4 — Analisis selesai | Semua hipotesis terjawab dengan CI |
| M5 — Naskah siap | Format, sitasi, dan lampiran lengkap |

### 1.2 Penyangga

Sediakan **2 minggu penyangga** untuk:

- cuaca buruk berkepanjangan,
- gangguan Starlink,
- perbaikan data,
- revisi pembimbing.

Jika penyangga habis, turunkan cakupan ke A, B, D, F dan catat sebagai
penyimpangan (bukan mengubah hasil).

---

## 2. Manajemen Risiko

| ID | Risiko | Peluang | Dampak | Mitigasi |
|---|---|:---:|:---:|---|
| R1 | Cuaca buruk berkepanjangan | Tinggi | Sedang | Blok waktu, perpanjang kampanye, replay staging |
| R2 | Starlink outage saat run | Sedang | Tinggi | Pause, tandai run, ulangi |
| R3 | Perubahan paket/firmware ISP | Sedang | Tinggi | Catat versi, uji ulang baseline |
| R4 | Controller mati | Sedang | Tinggi | Fail-static, watchdog, UPS |
| R5 | API RouterOS gagal/limit | Sedang | Sedang | Backoff, retry, queue lokal |
| R6 | Data hilang/korup | Rendah | Tinggi | Buffer lokal, checksum, backup harian |
| R7 | Conntrack tidak sesuai asumsi | Sedang | Tinggi | Pilot RST, verifikasi manual |
| R8 | Episode kurang | Tinggi | Sedang | Replay staging, perpanjang, laporkan presisi |
| R9 | Intervensi operator | Sedang | Sedang | Log, otomatisasi, protokol run |
| R10 | Etika/izin terlambat | Rendah | Tinggi | Urus izin sebelum pilot |
| R11 | Beban probe mengganggu pelanggan | Sedang | Sedang | Probe ringan, jam rendah, monitor keluhan |
| R12 | Konflik jadwal pembimbing | Sedang | Rendah | Jadwal tetap, laporan mingguan |

**Aturan eskalasi:** risiko R2, R4, R6, dan R10 menghentikan run sampai
ditangani. Risiko lain dicatat dan dilanjutkan dengan catatan.

---

## 3. Keselamatan Operasional

### 3.1 Fail-static

Jika controller mati, koneksi API putus, atau keputusan tidak valid:

1. Router tetap memakai konfigurasi terakhir yang valid.
2. Watchdog memeriksa heartbeat setiap 5 detik.
3. Jika heartbeat hilang > 30 detik, sistem menulis status `FAIL_STATIC` dan
   berhenti mengubah aturan.
4. Operator diberi notifikasi.

### 3.2 Backup dan rollback

Sebelum setiap run:

1. Ekspor konfigurasi RouterOS (`/export`).
2. Simpan daftar aturan mangle dan routing.
3. Catat checkpoint ID.
4. Uji rollback pada staging.

Saat rollback:

1. Hentikan controller.
2. Impor konfigurasi checkpoint.
3. Verifikasi aturan dan rute.
4. Uji konektivitas.
5. Catat waktu rollback.

**Kriteria lulus:** rollback selesai < 60 detik dan konektivitas pulih.

### 3.3 Jendela perubahan

- Perubahan aturan besar hanya pada jam rendah (01.00–05.00).
- Pada jam sibuk, hanya perubahan yang dibatasi oleh `b_min`/`b_max`.
- Pemberitahuan ke pelanggan minimal 24 jam sebelum kampanye.

### 3.4 Batas beban

- Probe throughput maksimal setiap 10 menit.
- Ukuran probe kecil (64 byte) untuk RTT.
- Tidak menjalankan `iperf3` bersamaan pada dua WAN.
- Pantau suhu dan CPU router.

---

## 4. Etika Penelitian

| Aspek | Tindakan |
|---|---|
| Izin lokasi | Persetujuan tertulis pemilik RT/RW Net |
| Informasi pelanggan | Pemberitahuan tujuan dan jadwal |
| Privasi | Anonimisasi; tidak menangkap payload |
| Data | Hanya header dan counter; disimpan terenkripsi |
| Retensi | Data mentah disimpan maksimal 2 tahun |
| Publikasi | Tidak menampilkan identitas pelanggan |
| Persetujuan | Mengikuti kebijakan kampus dan pembimbing |
| Konflik kepentingan | Tidak ada; penelitian tidak disponsori vendor |

**Prinsip:** pelanggan tidak boleh menanggung risiko lebih besar daripada manfaat
pengujian. Jika terjadi gangguan, run dihentikan dan layanan dipulihkan lebih dulu.

---

## 5. Prosedur Run

### 5.1 Sebelum run

- [ ] Konfirmasi cuaca dan prakiraan.
- [ ] Pastikan controller, probe, dan capture aktif.
- [ ] Ekspor konfigurasi dan buat checkpoint.
- [ ] Verifikasi NTP dan ruang disk.
- [ ] Catat versi firmware dan paket ISP.
- [ ] Pastikan tidak ada intervensi operator terjadwal.

### 5.2 Saat run

- [ ] Jalankan urutan sesuai Latin square.
- [ ] Catat waktu mulai/selesai.
- [ ] Pantau dashboard dan alarm.
- [ ] Catat intervensi.
- [ ] Hentikan jika ada indikasi gangguan pelanggan.

### 5.3 Setelah run

- [ ] Hentikan capture dan ekspor data.
- [ ] Verifikasi checksum.
- [ ] Rollback ke konfigurasi awal.
- [ ] Catat catatan lapangan.
- [ ] Backup ke dua lokasi.

---

## 6. Rencana Kontingensi

| Skenario | Tindakan |
|---|---|
| 6 skenario tidak selesai | Turunkan ke A, B, D, F; catat sebagai penyimpangan |
| Starlink tidak stabil berminggu-minggu | Perpanjang atau ganti periode; jangan mengubah definisi |
| Data RST tidak terdeteksi | Validasi capture; jika tetap gagal, H3a dilaporkan tidak teruji |
| Telemetri dish tidak tersedia | Gunakan probe aktif; catat keterbatasan |
| Lokasi tidak dapat diakses | Cari lokasi setara; dokumentasikan perbedaan |
| Waktu analisis mepet | Prioritaskan H1, H3a, H4; H5 dilaporkan sebagai validasi |

---

## 7. Luaran Akhir Tahap 4

1. Bab III lengkap: desain, formalisasi, instrumen, analisis.
2. Protokol run yang dapat dijalankan operator lain.
3. Berkas konfigurasi baseline A dan G.
4. Skema data dan skrip analisis.
5. Tabel risiko, etika, dan jadwal.
6. Checklist kesiapan kampanye.

---

## 8. Kriteria Kesiapan Kampanye

- [ ] Pilot lulus 7 uji kalibrasi.
- [ ] Rollback teruji < 60 detik.
- [ ] Fail-static teruji.
- [ ] Izin lokasi dan pemberitahuan pelanggan selesai.
- [ ] Dataset staging tersedia.
- [ ] Rencana analisis dikunci.
- [ ] Enam skenario + baseline G terkonfigurasi.
- [ ] Log keputusan diperbarui.
