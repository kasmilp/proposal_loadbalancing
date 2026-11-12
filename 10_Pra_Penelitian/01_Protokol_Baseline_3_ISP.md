# Protokol Baseline 3 ISP (Read-Only)

**Status:** Draf pra-penelitian
**Tujuan:** Mengumpulkan baseline observasional pada tiga ISP tanpa mengubah
konfigurasi apa pun.
**Akun:** Group `read` — hanya monitoring, tanpa hak modifikasi.

---

## 1. Posisi Kegiatan Ini

| Aspek | Baseline read-only | Eksperimen SPA-HSM |
|---|---|---|
| Sifat | Observasional | Intervensi |
| Akun | `read` | Akun terpisah dengan hak tulis terbatas |
| Tujuan | Baseline, kalibrasi, validasi instrumen | Uji H1–H4, ablasi |
| Mengubah aturan | **Tidak** | Ya, pada jendela terkontrol |
| Klaim yang didukung | Gap, parameter, kelayakan | Kontribusi sistem |

**Penting:** akun read-only **tidak dapat** membuktikan klaim kontribusi SPA-HSM
(H1–H4), karena klaim tersebut memerlukan perubahan rasio PCC. Yang dapat
dibuktikan dengan akun ini adalah baseline, kualitas pengukuran, dan kelayakan
topologi.

---

## 2. Topologi

| Interface | ISP | Teknologi | Peran awal |
|---|---|---|---|
| ether1 | ISP-A | Starlink (LEO) | Kandidat link formal |
| ether2 | ISP-B | Starlink (LEO) | Kandidat link formal / pembanding |
| ether3 | ISP-C | Fiber Optic | Kandidat link formal |

**Catatan:** proposal saat ini masih berkunci pada **dual-ISP FO–LEO**. Penggunaan
tiga ISP adalah perubahan lingkup yang harus diputuskan setelah baseline (lihat
`02_Matriks_Keputusan_Topologi.md`).

---

## 3. Konfigurasi Akun Read-Only

### 3.1 Group

Buat group `monitor-read` dengan policy minimal:

```
/api
/read
/test
/winbox
```

Jangan berikan:

```
/write
/policy
/sensitive
/reboot
/ftp
/ssh
/romon
```

**Catatan:** policy `read` tetap dapat membaca informasi sistem. Batasi akses
dengan *source address* dan gunakan API-SSL.

### 3.2 Verifikasi read-only

| Uji | Perintah | Hasil yang diharapkan |
|---|---|---|
| Baca resource | `GET /rest/system/resource` | 200 OK |
| Baca interface | `GET /rest/interface` | 200 OK |
| Baca route | `GET /rest/ip/route` | 200 OK |
| Baca mangle | `GET /rest/ip/firewall/mangle` | 200 OK |
| Tulis (uji negatif) | `POST /rest/ip/firewall/mangle` | **403 Forbidden** |
| Hapus (uji negatif) | `DELETE /rest/ip/firewall/mangle/<id>` | **403 Forbidden** |

Jika uji tulis berhasil, hentikan kegiatan dan perbaiki group sebelum melanjutkan.

---

## 4. Metrik dan Instrumen

| Metrik | Sumber | Interval | Catatan |
|---|---|---|---|
| RTT, jitter, loss | Probe per WAN | 1 detik | Gunakan *routing mark* per WAN |
| Throughput/goodput | `iperf3`/HTTP | 10 menit | Bergantian, jangan paralel |
| Utilisasi | SNMP `ifHCInOctets`/`ifHCOutOctets` | 10 detik | Per interface |
| Error/discard | SNMP | 10 detik | Indikator tambahan |
| Telemetri Starlink | gRPC dish (jika tersedia) | 1 detik | Dua dish, dua vantage |
| Cuaca | Stasiun/BMKG | 10 menit | Kovariat |
| Log API | Controller | Setiap request | Untuk audit read-only |

**Aturan probe:** probe ke ISP-A, ISP-B, dan ISP-C harus memakai *routing mark*
masing-masing. Tanpa ini, probe hanya mengukur jalur default.

---

## 5. Endpoint REST yang Dipakai

Contoh (sesuaikan dengan versi RouterOS):

```
GET /rest/system/resource
GET /rest/interface
GET /rest/ip/address
GET /rest/ip/route
GET /rest/ip/firewall/mangle
GET /rest/ip/firewall/connection
GET /rest/interface/ether1
GET /rest/tool/netwatch
```

**Larangan:** jangan memakai `POST`, `PATCH`, `PUT`, atau `DELETE` selama baseline.

---

## 6. Durasi dan Jendela

| Tahap | Durasi | Cakupan |
|---|---:|---|
| Pilot akun dan probe | 1 hari | Verifikasi read-only dan routing probe |
| Baseline utama | 7–14 hari | 24 jam penuh, termasuk jam sibuk dan hujan |
| Validasi ulang | 1–2 hari | Setelah perubahan firmware/ISP |

Setiap hari dicatat: tanggal, cuaca, kejadian khusus, dan intervensi operator
(jika ada).

---

## 7. Analisis Baseline

1. Distribusi RTT, jitter, loss, dan throughput per ISP.
2. Frekuensi dan durasi episode degradasi.
3. Periodisitas 15 detik pada kedua Starlink.
4. Korelasi antar-Starlink: apakah keduanya mengalami transien bersamaan?
5. Pola harian dan pengaruh hujan.
6. Stabilitas API dan kelengkapan data.

**Luaran:** laporan baseline + rekomendasi topologi formal.

---

## 8. Kriteria Keputusan Setelah Baseline

| Pertanyaan | Ambang indikatif | Implikasi |
|---|---|---|
| API stabil | ≥ 99% request sukses | Layak untuk controller |
| Data lengkap | ≥ 95% sampel | Layak dianalisis |
| Episode cukup | ≥ 5 episode/hari total | Layak untuk kampanye |
| Dua Starlink independen | Korelasi transien < 0,7 | Tri-ISP layak dipertimbangkan |
| Waktu tersedia | ≥ 16 minggu | Tri-ISP realistis |

Jika dua Starlink sangat berkorelasi, tri-ISP tidak menambah informasi banyak;
dual-ISP lebih rasional.

---

## 9. Etika dan Keselamatan

- Read-only tidak mengubah layanan pelanggan.
- Tidak menangkap payload.
- Anonimisasi data.
- Pemberitahuan ke pemilik jaringan.
- Simpan kredensial di tempat aman; jangan commit ke repositori.

---

## 10. Checklist

- [ ] Group `monitor-read` dibuat.
- [ ] Uji tulis negatif menghasilkan 403.
- [ ] API-SSL aktif dan source address dibatasi.
- [ ] Probe per WAN memakai routing mark.
- [ ] NTP tersinkron.
- [ ] Disk dan buffer cukup.
- [ ] Skema data disiapkan.
- [ ] Baseline 7–14 hari dijalankan.
- [ ] Laporan baseline disusun.
- [ ] Keputusan dual vs tri dicatat di log.
