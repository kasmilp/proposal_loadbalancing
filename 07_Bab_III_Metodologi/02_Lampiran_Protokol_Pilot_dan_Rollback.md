# Lampiran Protokol Pilot dan Rollback

**Dokumen:** `02_Lampiran_Protokol_Pilot_dan_Rollback.md`
**Fungsi:** Prosedur yang harus lulus sebelum kampanye lapangan dimulai.
**Prinsip:** Jika satu uji gagal, kampanye tidak dimulai.

---

## 1. Prasyarat

- [ ] Izin lokasi dan pemberitahuan pelanggan selesai.
- [ ] Controller, probe, dan capture terpasang.
- [ ] RouterOS dan firmware Starlink dicatat.
- [ ] Backup konfigurasi awal tersedia.
- [ ] NTP aktif pada router, controller, dan probe.
- [ ] `MockAdapter` lulus uji unit.
- [ ] Rencana analisis dikunci.

---

## 2. Tujuh Uji Kalibrasi

### T1 — Konsistensi throughput SNMP vs probe

**Tujuan:** memastikan SNMP dan probe mengukur hal yang sama.

**Langkah:**
1. Jalankan `iperf3` 60 detik pada WAN1.
2. Catat throughput `iperf3`.
3. Catat `ifHCOutOctets` sebelum dan sesudah.
4. Hitung throughput SNMP.
5. Ulangi pada WAN2.

**Lulus jika:** selisih < 10% pada kedua WAN.
**Gagal jika:** selisih ≥ 10% → periksa interval polling dan counter overflow.

---

### T2 — Probe benar-benar melewati WAN yang dituju

**Tujuan:** mencegah semua probe mengikuti jalur default.

**Langkah:**
1. Tandai probe WAN1 dengan `routing-mark=probe-fo`.
2. Tandai probe WAN2 dengan `routing-mark=probe-leo`.
3. Jalankan `traceroute` dari masing-masing mark.
4. Catat hop pertama dan alamat publik.

**Lulus jika:** hop pertama dan IP publik berbeda untuk kedua WAN.
**Gagal jika:** keduanya sama → perbaiki aturan routing mark.

---

### T3 — Deteksi RST terkontrol

**Tujuan:** memastikan capture melihat RST, bukan hanya counter router.

**Langkah:**
1. Buat aliran TCP uji di VLAN uji (bukan pelanggan).
2. Kirim RST terkontrol dengan Scapy ke salah satu ujung aliran.
3. Periksa capture `tcpdump`.
4. Hitung RST flow dan RST packet.

**Lulus jika:** RST terdeteksi di capture dan nilainya sesuai injeksi.
**Gagal jika:** tidak terdeteksi → periksa posisi capture, filter, dan checksum.

---

### T4 — Sinkronisasi waktu

**Langkah:**
1. Bandingkan waktu router, controller, probe, dan capture.
2. Catat offset.

**Lulus jika:** offset < 100 ms.
**Gagal jika:** ≥ 100 ms → perbaiki NTP sebelum kampanye.

---

### T5 — Beban probe

**Langkah:**
1. Ukur throughput tanpa probe.
2. Ukur throughput dengan probe 1 detik dan `iperf3` 10 menit.
3. Bandingkan.

**Lulus jika:** penurunan < 2%.
**Gagal jika:** ≥ 2% → kurangi frekuensi atau ukuran probe.

---

### T6 — Fail-static

**Langkah:**
1. Jalankan sistem pada kondisi F.
2. Matikan controller.
3. Tunggu 60 detik.
4. Periksa aturan PCC dan konektivitas.
5. Nyalakan controller dan periksa pemulihan.

**Lulus jika:** konfigurasi terakhir tetap berlaku dan konektivitas tidak terputus.
**Gagal jika:** aturan berubah atau konektivitas hilang → perbaiki watchdog.

---

### T7 — Rollback

**Langkah:**
1. Buat checkpoint.
2. Ubah aturan PCC secara terkontrol.
3. Jalankan rollback.
4. Ukur waktu dan verifikasi.

**Lulus jika:** rollback < 60 detik dan konfigurasi kembali identik.
**Gagal jika:** > 60 detik atau ada aturan tersisa → perbaiki prosedur.

---

## 3. Prosedur Rollback

### 3.1 Sebelum perubahan

```routeros
/export file=checkpoint-<run-id>
/system backup save name=backup-<run-id>
/ip firewall mangle print detail
/ip route print detail
/ip firewall connection print count-only
```

Simpan berkas ke controller dan satu lokasi cadangan.

### 3.2 Saat rollback

1. Hentikan controller.
2. Impor konfigurasi:

```routeros
/import file-name=checkpoint-<run-id>.rsc
```

3. Verifikasi aturan:

```routeros
/ip firewall mangle print
/ip route print
/tool netwatch print
```

4. Verifikasi konektivitas dari LAN.
5. Catat waktu rollback dan hasil verifikasi.

### 3.3 Setelah rollback

- [ ] Tidak ada aturan PCC eksperimen yang tersisa.
- [ ] Rute default kembali ke konfigurasi awal.
- [ ] Konektivitas pelanggan normal.
- [ ] Log rollback tersimpan.
- [ ] Controller dalam keadaan berhenti atau mode aman.

---

## 4. Uji Fail-Static

| Langkah | Aksi | Kriteria |
|---:|---|---|
| 1 | Jalankan kondisi F | Aturan aktif |
| 2 | Matikan controller | Tidak ada perubahan aturan |
| 3 | Tunggu 60 detik | Konektivitas stabil |
| 4 | Periksa log watchdog | Status `FAIL_STATIC` tercatat |
| 5 | Nyalakan controller | Sinkronisasi tanpa lonjakan aturan |

---

## 5. Formulir Kalibrasi

| Uji | Tanggal | Hasil | Lulus/Gagal | Catatan |
|---|---|---|---|---|
| T1 | | | | |
| T2 | | | | |
| T3 | | | | |
| T4 | | | | |
| T5 | | | | |
| T6 | | | | |
| T7 | | | | |

**Keputusan:** ☐ Lanjut kampanye ☐ Perbaiki dan ulangi

---

## 6. Formulir Log Run

| Field | Isi |
|---|---|
| Run ID | |
| Kondisi | A–G |
| Tanggal | |
| Jam mulai/selesai | |
| Cuaca/curah hujan | |
| Firmware/router | |
| Intervensi | |
| Episode teramati | |
| Catatan | |

---

## 7. Kriteria Henti Darurat

Hentikan run dan rollback segera jika:

1. pelanggan melaporkan gangguan luas;
2. router CPU > 90% selama > 5 menit;
3. suhu router melewati batas aman;
4. controller kehilangan heartbeat > 30 detik;
5. aturan PCC tidak dapat diverifikasi;
6. terjadi perubahan konfigurasi di luar kendali;
7. listrik padam.

Setelah henti darurat, tulis laporan insiden dan jangan lanjutkan sebelum
penyebabnya dipahami.

---

## 8. Checklist Kesiapan Kampanye

- [ ] T1–T7 lulus.
- [ ] Rollback teruji < 60 detik.
- [ ] Fail-static teruji.
- [ ] Izin dan pemberitahuan selesai.
- [ ] Dataset staging tersedia.
- [ ] Rencana analisis dikunci.
- [ ] Tujuh kondisi terkonfigurasi.
- [ ] Log keputusan diperbarui.
- [ ] Tim/operator memahami protokol.
