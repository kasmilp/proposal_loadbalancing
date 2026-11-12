# Diagnostik Akses API Monitoring

**Tanggal:** 12 November 2026
**Endpoint:** `[host]:[port]` (dirahasiakan)
**Akun:** group read-only (kredensial tidak disimpan)
**Tujuan:** Memastikan akun monitoring dapat membaca data melalui API/REST.

> **Pembaruan:** akses **berhasil** melalui port 6187 dengan TLS legacy
> (`minimum_version=TLSv1`, cipher `ALL:@SECLEVEL=0`, `OP_LEGACY_SERVER_CONNECT`).
> Negosiasi akhir: **TLS 1.2 + ADH-AES256-SHA256** (anonymous cipher).
> Snapshot lengkap ada di `04_Snapshot_ReadOnly_12Nov2026.md`.
> Bagian di bawah adalah riwayat diagnosis awal.

---

## 1. Ringkasan

| Uji | Hasil |
|---|---|
| TCP connect ke port monitoring | **Berhasil** |
| REST via HTTPS | Gagal: TLS handshake timeout |
| REST via HTTP | Gagal: read timeout |
| RouterOS API plain | Gagal: timeout |
| RouterOS API SSL | Gagal: timeout |
| Kirim sentence `/login` mentah | Tidak ada respons |
| Port 80 | Tertutup |
| Port 443 | Terbuka, tetapi bukan HTTPS/HTTP standar |
| Port 8291 (Winbox) | Tertutup dari luar |
| Port 8728/8729 (API/API-SSL) | Tertutup dari luar |

**Kesimpulan:** port monitoring menerima koneksi TCP, tetapi tidak merespons
protokol REST maupun RouterOS API. Kemungkinan besar port tersebut diteruskan ke
**Winbox (8291)**, ke layanan yang memerlukan tunnel/handshake khusus, atau
layanan API/REST tidak aktif.

**Penting:** tidak ada operasi tulis yang dicoba. Tidak ada konfigurasi yang
diubah.

---

## 2. Kemungkinan Penyebab

1. **Port 38291 diteruskan ke Winbox 8291**, bukan ke API 8728/8729.
2. **Service API/REST tidak aktif** di `/ip/service`.
3. **API hanya mendengarkan di address tertentu** (mis. localhost/LAN), bukan
   di interface WAN.
4. **Akses memerlukan tunnel/VPN** sebelum port tujuan dapat dijangkau.
5. **Group user tidak memiliki policy `api`/`rest-api`** — biasanya menghasilkan
   error autentikasi, bukan timeout, tetapi tetap perlu dicek.
6. **Port forwarding NAT mengarah ke perangkat lain** atau service di belakang
   proxy yang tidak meneruskan data.

---

## 2A. Uji Endpoint Kedua (port 6187)

Endpoint kedua diuji dengan akun yang sama. Hasilnya:

| Uji | Hasil |
|---|---|
| Resolusi DNS | Sempat gagal, lalu mengarah ke `103.186.31.198` |
| TCP ke IP:6187 | **Berhasil** |
| TCP via hostname:6187 | Tidak konsisten |
| TLS 1.0/1.1/1.2 (cipher default) | Gagal: `handshake_failure` |
| TLS legacy + `ALL:@SECLEVEL=0` | **Berhasil** (TLS 1.2, ADH-AES256-SHA256) |
| API plaintext (sentence `/login`) | Menerima 7 byte: `15 00 00 00 02 02 16` |
| Sentence API berikutnya | Tidak ada respons |
| REST HTTP/HTTPS | Tidak merespons |

**Interpretasi:** port 6187 adalah **API-SSL** yang hanya menawarkan cipher
*anonymous Diffie-Hellman* (ADH). Client modern menolak cipher ini secara default,
sehingga handshake gagal. Dengan cipher legacy diaktifkan, koneksi berhasil.
Ini **tidak aman** untuk produksi karena tidak ada autentikasi sertifikat.
Solusi: pasang sertifikat yang valid, nonaktifkan ADH, atau akses melalui VPN.

---

## 3. Checklist di Winbox

Jalankan di terminal RouterOS:

### 3.1 Service

```routeros
/ip/service print
```

Cek:

- `api` (8728) — enabled?
- `api-ssl` (8729) — enabled?
- `www` (80) / `www-ssl` (443) — enabled?
- `available-from` — apakah membatasi ke LAN?

### 3.2 NAT port forwarding

```routeros
/ip/firewall/nat print detail where dst-port~"38291"
```

Cek `to-addresses` dan `to-ports`. Jika `to-ports=8291`, itu Winbox, bukan API.

### 3.3 Firewall input

```routeros
/ip/firewall/filter print detail where chain=input
```

Pastikan koneksi dari IP controller diizinkan ke port API/REST.

### 3.4 Group dan user

```routeros
/user/group print detail where name="monitor-read"
/user print detail where name="monitoring123"
```

Policy minimal untuk REST/API:

```
api
read
test
```

Jika memakai REST di RouterOS 7, pastikan juga service `www-ssl` aktif dan
policy yang diperlukan tersedia pada versi tersebut.

### 3.5 Alamat dan DNS

```routeros
/ip/cloud print
/ip/dns print
```

Pastikan DDNS menunjuk ke router yang benar.

### 3.6 Versi RouterOS dan port 6187

```routeros
/system/resource print
/ip/service print
/ip/firewall/nat print detail where dst-port~"6187"
```

- Jika versi **6.x**: API-SSL lama mungkin memakai TLS 1.0/cipher yang tidak
  didukung OpenSSL modern. Opsi: upgrade ke v7, atau gunakan API plaintext
  **hanya melalui VPN/SSH tunnel**.
- Jika versi **7.x**: pastikan `api-ssl` aktif, sertifikat valid, dan coba REST
  melalui `www-ssl`.
- Pastikan `to-ports=8729`. Jika `to-ports=8291`, itu Winbox, bukan API-SSL.

---

## 4. Tindakan Keamanan

1. **Ganti password** akun monitoring; password saat ini terlalu lemah.
2. Batasi `address` user ke IP controller.
3. Jangan membuka API/REST langsung ke WAN; gunakan VPN/WireGuard/SSH tunnel.
4. Gunakan **API-SSL** atau **REST via HTTPS**, bukan API plaintext.
5. Pisahkan akun:
   - `monitor-read` untuk baseline,
   - `controller-write` untuk intervensi, dengan hak terbatas dan logging.
6. Jangan menaruh kredensial di repositori atau skrip yang di-commit.

---

## 5. Alternatif Jika API Tetap Tidak Tersedia

| Kebutuhan | Alternatif |
|---|---|
| Counter interface | SNMP v2c/v3 read-only |
| RTT/jitter/loss | Probe aktif dari controller |
| Throughput | `iperf3`/HTTP probe |
| Telemetri Starlink | gRPC dish / aplikasi resmi |
| Konfigurasi | Ekspor `/export` manual dari Winbox |

Baseline tetap dapat dijalankan tanpa API, tetapi koleksi data menjadi kurang
otomatis.

---

## 6. Langkah Berikutnya

- [ ] Cek `/ip/service print` dan NAT rule 38291.
- [ ] Perbaiki port forward ke API/REST yang benar.
- [ ] Verifikasi read-only dengan uji tulis negatif (harus 403).
- [ ] Jalankan baseline 7–14 hari.
- [ ] Setelah baseline, putuskan dual vs tri-ISP.

---

## 7. Catatan Topologi

Karena ISP-A dan ISP-B adalah dua akun Starlink terpisah di **lokasi yang sama**,
keduanya kemungkinan mengalami:
- hujan yang sama,
- transien rekonfigurasi global 15 detik yang sama,
- pola beban lokal yang sama.

Jika korelasi transien tinggi, ISP-B tidak menambah banyak informasi independen.
Ini memperkuat rekomendasi **dual-ISP formal (A+C)** dengan ISP-B sebagai
validasi eksternal, bukan sebagai link formal ketiga.
