# Diagnostik Akses API Monitoring

**Tanggal:** 12 November 2026
**Endpoint:** `[host]:[port]` (dirahasiakan)
**Akun:** group read-only (kredensial tidak disimpan)
**Tujuan:** Memastikan akun monitoring dapat membaca data melalui API/REST.

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
