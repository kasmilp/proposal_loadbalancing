# Snapshot Read-Only Router — 12 November 2026

**Status:** Berhasil terhubung dengan akun monitoring read-only.
**Endpoint:** `[host]:6187` → API-SSL (dirahasiakan).
**Kredensial:** tidak disimpan di repo.
**Perubahan konfigurasi:** **tidak ada**.

---

## 1. Metode Koneksi

| Item | Nilai |
|---|---|
| Protokol | RouterOS API-SSL |
| Port eksternal | 6187 → 8729 |
| TLS | TLS 1.2 |
| Cipher | `ADH-AES256-SHA256` (anonymous, tanpa sertifikat) |
| Verifikasi sertifikat | Tidak ada (karena cipher ADH) |
| Library | `librouteros` + SSLContext legacy |

**Catatan keamanan:** cipher `ADH` berarti tidak ada autentikasi sertifikat.
Koneksi rentan *man-in-the-middle*. Ini harus diperbaiki sebelum dipakai untuk
intervensi.

---

## 2. Perangkat

| Item | Nilai |
|---|---|
| Model | RB1100AHx4 |
| RouterOS | 7.22.2 (stable) |
| Uptime saat snapshot | ±6 jam |
| CPU load | 18% |
| Memori bebas | ±800 MB dari 1 GB |

---

## 3. Interface WAN

| Interface | ISP | Status | Alamat privat |
|---|---|---|---|
| ether1-ISP-A | Starlink A | **Running** | 192.168.1.76/24 |
| ether2-ISP-B | Starlink B | **Running** | 192.168.2.160/24 |
| ether3-ISP-C | FO | **Running** | 192.168.3.2/24 |

Interface lain: bridge hotspot, dua tunnel OVPN, loopback, dan ether4–13.
Tidak ada interface WAN yang disabled.

---

## 4. Routing

### 4.1 Tabel utama

Ditemukan **tiga default route aktif** di tabel `main`:

| Gateway | Distance | Status |
|---|---:|---|
| ether1-ISP-A | 1 | active |
| ether2-ISP-B | 1 | active |
| ether3-ISP-C | 1 | active |

Selain itu ada duplikat distance 2 dan 3 untuk ISP-B/ISP-C.

**Masalah:** beberapa default route aktif dengan distance sama di tabel `main`
membuat perilaku routing untuk trafik yang tidak ter-mark menjadi tidak pasti.
Bisa menyebabkan asymmetric routing atau fallback yang tidak diinginkan.

### 4.2 Tabel PCC

Terdapat tabel terpisah:

- `VIA ISP 1` → default via ether1
- `VIA ISP 2` → default via ether2
- `VIA ISP 3` → default via ether3

Ini bagian yang dipakai PCC. Bagian ini **benar** secara struktur.

---

## 5. PCC dan Mangle

Jumlah aturan mangle: **23**.

| Rantai | Fungsi | Status |
|---|---|---|
| `prerouting` | `mark-connection` PCC 3 arah | Aktif |
| `prerouting` | `mark-routing` ke VIA ISP 1/2/3 | Aktif |
| `input` | Mark koneksi untuk trafik router | Aktif |
| `output` | Mark routing untuk trafik router | Aktif |
| `prerouting` | Aturan classifier 4/3 | **Disabled** |

Classifier yang dipakai:

```
both-addresses-and-ports:3/0  -> ISP-A
both-addresses-and-ports:3/1  -> ISP-B
both-addresses-and-ports:3/2  -> ISP-C
```

**Kesimpulan:** PCC 3-link sudah terpasang dan aktif. Ini berarti topologi
tri-ISP secara teknis **sudah siap** untuk diuji.

**Yang perlu diaudit:** urutan aturan, `passthrough`, dan apakah aturan
`DNS-ICMP` menimpa mark PCC untuk trafik tertentu.

---

## 6. NAT dan Layanan

- NAT didominasi aturan hotspot.
- Tidak terlihat aturan port-forward 6187 di NAT; akses kemungkinan melalui
  tunnel OVPN, bukan NAT langsung.
- Banyak layanan aktif dengan `address` kosong (terbuka ke semua interface):
  `ftp`, `telnet`, `www`, `winbox`, `api`, `api-ssl`, `ssh`, `snmp`.
- Banyak layanan bernama `detnet` dan `ppp` pada port acak. Perlu diaudit apakah
  ini layanan yang dikenal.

**Risiko:** permukaan serangan sangat lebar. FTP, telnet, dan HTTP polos tidak
perlu terbuka.

---

## 7. Group Read-Only

Policy group `read`:

```
local,telnet,ssh,read,test,winbox,web,sensitive,api,romon,rest-api,
!ftp,!reboot,!write,!policy,!password,!sniff
```

**Kesimpulan:** `!write` dan `!policy` menegaskan akun ini **benar-benar
read-only**. Tidak ada operasi tulis yang dicoba.

**Catatan:** `sensitive` dan `romon` tidak diperlukan untuk monitoring dan
sebaiknya dihapus. `telnet` dan `ssh` juga tidak perlu jika hanya API.

---

## 8. Netwatch

Tidak ada entri `netwatch`. Artinya baseline praktisi G (netwatch failover)
**belum dikonfigurasi**. Ini harus dibuat pada tahap intervensi, bukan sekarang.

---

## 9. Temuan Prioritas

| Prioritas | Temuan | Tindakan |
|---|---|---|
| **Kritis** | Layanan terbuka ke semua interface | Batasi ke VPN/IP manajemen; matikan ftp/telnet/www |
| **Kritis** | API-SSL memakai cipher ADH tanpa sertifikat | Pasang sertifikat, nonaktifkan ADH, atau akses via VPN |
| **Tinggi** | Password monitoring lemah | Ganti dan simpan di pengelola sandi |
| **Tinggi** | Default route ganda di tabel `main` | Audit dan rapikan |
| **Tinggi** | Layanan `detnet`/`ppp` port acak | Audit; matikan jika tidak dikenal |
| **Sedang** | Group `read` punya `sensitive`/`romon` | Hapus untuk least privilege |
| **Sedang** | Netwatch belum ada | Konfigurasi saat tahap intervensi |
| **Rendah** | `ip/firewall/connection` timeout | Gunakan SNMP/filter untuk baseline |

---

## 10. Implikasi untuk Penelitian

1. **Read-only baseline bisa dijalankan sekarang.** API berhasil; data interface,
   route, mangle, dan resource dapat dibaca.
2. **PCC 3-link sudah aktif.** Secara teknis, tri-ISP layak diuji.
3. **Dua Starlink satu lokasi** kemungkinan berkorelasi tinggi. Baseline harus
   mengukur korelasi transien sebelum memutuskan dual vs tri.
4. **Proposal saat ini dual-ISP.** Rekomendasi tetap: formal A+C, B sebagai
   validasi eksternal, sampai data baseline menunjukkan independensi.
5. **Akun tulis belum ada.** Intervensi H1–H4 memerlukan akun terpisah dengan
   hak tulis terbatas dan jendela terkontrol.

---

## 11. Berikutnya

- [ ] Ganti password monitoring.
- [ ] Batasi layanan dan hapus `sensitive`/`romon`.
- [ ] Audit default route ganda dan layanan `detnet`.
- [ ] Jalankan kolektor baseline read-only 7–14 hari.
- [ ] Ukur korelasi transien A–B.
- [ ] Putuskan dual vs tri.
- [ ] Buat akun `controller-write` setelah staging lulus.
