# 16 — Arsitektur Jaringan MikroTik Multi-WAN (3 ISP)

**Status:** Draf desain (siap dikembangkan ke implementasi)
**Fungsi:** Merancang arsitektur jaringan MikroTik dengan **3 koneksi ISP
(Multi-WAN)**, load balancing **PCC**, **failover**, dan distribusi **LAN**.
**Acuan:** `15_Arsitektur_Sistem.md`, `08_Rancangan_Eksperimen.md`,
`00_README.md` §6, serta kolektor `collector.py`.
**Target:** RouterOS **v7** (RB1100AHx4).

**Konvensi:** **[FAKTA]** · **[ANALISIS]** · **[USULAN]**.

---

## 1. Pemetaan Interface & Identitas ISP **[FAKTA]**

Nama interface **tidak diubah** dan **ketiga ISP dipertahankan**:

| # | Interface | ISP | Teknologi | Peran |
|---|---|---|---|---|
| 1 | **`ether1-ISP-A`** | ISP A | Starlink (LEO) | WAN-1 |
| 2 | **`ether2-ISP-B`** | ISP B | Starlink (LEO) | WAN-2 |
| 3 | **`ether3-ISP-C`** | ISP C | **Fiber Optic (FO)** | WAN-3 |
| 4 | `ether4`+ (LAN) | — | — | Distribusi LAN (bridge) |

Pemetaan ini **identik** dengan `PROBE_INTERFACES` pada kolektor:
`ether1-ISP-A,ether2-ISP-B,ether3-ISP-C`.

---

## 2. Asumsi Kapasitas (TIDAK diasumsikan sama) 🔴

**[USULAN]** Bobot load balancing **wajib** diturunkan dari kapasitas nyata, bukan
diasumsikan sama. Isi tabel berikut dari kontrak/ukur:

| Link | Interface | Kapasitas kontrak | Kapasitas terukur (baseline) | Bobot relatif |
|---|---|---|---|---|
| ISP A | `ether1-ISP-A` | `<isi>` | `<isi>` | `<isi>` |
| ISP B | `ether2-ISP-B` | `<isi>` | `<isi>` | `<isi>` |
| ISP C | `ether3-ISP-C` | `<isi>` | `<isi>` | `<isi>` |

**Contoh ilustratif (bukan asumsi):** bila kapasitas A : B : C = **2 : 1 : 1**,
maka pembagian bucket PCC menjadi 2/4 : 1/4 : 1/4 (lihat §6.4).

**[ANALISIS]** Karena Starlink bersifat stokastik (lihat `03_Spesifikasi_Parameter.md`),
"kapasitas" yang dipakai sebaiknya **kapasitas efektif** dari baseline
(`analyze_baseline.py`), bukan angka iklan.

---

## 3. Diagram Arsitektur

**Gambar:** `arsitektur/arsitektur_jaringan_mikrotik.png` (vektor: `.svg`);
skrip: `arsitektur/arsitektur_jaringan_mikrotik.py`.

```
   [ISP A Starlink]        [ISP B Starlink]        [ISP C Fiber Optic]
          │                        │                        │
    ether1-ISP-A             ether2-ISP-B             ether3-ISP-C
          └───────────┬────────────┴────────────┬───────────┘
                      ▼                         ▼
        ┌───────────────────────────────────────────────────────┐
        │            MikroTik RB1100AHx4 · RouterOS v7          │
        │  ┌─────────────────────────────────────────────────┐  │
        │  │ (1) Mangle: PCC classifier + connection mark    │  │
        │  │ (2) Routing mark → to-ISP-A / to-ISP-B / to-ISP-C│ │
        │  │ (3) Failover: check-gateway + netwatch          │  │
        │  │ (4) NAT masquerade per WAN                      │  │
        │  └─────────────────────────────────────────────────┘  │
        └───────────────────────────┬───────────────────────────┘
                                    │ LAN (bridge-LAN)
                                    ▼
                          ┌──────────────────┐        ┌───────────────┐
                          │   Switch LAN      │───────►│ Access Point  │
                          └────────┬─────────┘        └──────┬────────┘
                                   │                          │
                             [Client kabel]             [Client Wi-Fi]

   Server Controller (API-SSL) ──► mengatur rasio PCC & verifikasi aturan
```

**Kode warna:** **biru** = jalur WAN · **kuning** = routing/load balancing ·
**merah** = failover · **ungu** = distribusi LAN · **hijau** = client ·
**abu** = kontrol eksternal.

---

## 4. Fungsi Setiap Komponen **[USULAN]**

| Komponen | Fungsi |
|---|---|
| `ether1-ISP-A`, `ether2-ISP-B` | Terminasi WAN Starlink (DHCP dari dish) |
| `ether3-ISP-C` | Terminasi WAN Fiber Optic (PPPoE/statik) |
| **Mangle PCC** | Klasifikasi koneksi (PCC) → *connection mark* per ISP |
| **Routing mark** | Mengarahkan *connection mark* ke *routing table* ISP terkait |
| **Routing table** (`to-ISP-A/B/C`) | Tabel rute per ISP (RouterOS v7 wajib deklarasi) |
| **Failover** | Rute cadangan + `check-gateway`/`netwatch` saat ISP gagal |
| **NAT masquerade** | Menerjemahkan alamat LAN per `out-interface` WAN |
| **bridge-LAN** | Menyatukan port LAN; titik masuk distribusi |
| **Switch LAN** | Distribusi ke port kabel |
| **Access Point (AP)** | Distribusi Wi-Fi ke client |
| **Client** | Pengguna akhir (kabel & Wi-Fi) |
| **Server Controller** | (penelitian) menyuntik rasio PCC via API-SSL |

---

## 5. Alur Perjalanan Trafik (Client → Internet)

**[USULAN]** Tahapan per paket/koneksi:

1. **Client** mengirim paket ke gateway (bridge-LAN) di MikroTik.
2. Paket masuk **chain `prerouting`** dengan `in-interface = bridge-LAN`.
3. **PCC** (`per-connection-classifier`) menetapkan **bucket** untuk koneksi baru
   → menulis **`connection-mark`** (mis. `conn-A`).
4. Untuk paket berikutnya dari koneksi yang **sama**, *connection mark* dipertahankan
   → seluruh paket satu sesi konsisten ke satu ISP (mencegah *reordering*).
5. *Connection mark* dipetakan ke **routing mark** (`to-ISP-X`) → masuk **routing table**
   ISP terkait.
6. **Default route** di tabel itu mengarah ke gateway ISP → keluar via
   `ether1/2/3` (sesuai mark).
7. **NAT masquerade** pada `out-interface` WAN menerjemahkan IP privat LAN.
8. Paket keluar ke internet melalui ISP terpilih; balasan kembali lewat jalur yang
   sama (karena *conntrack* per koneksi).

**Saat failover:**

9. Bila ISP (mis. A) gagal, tanda pada rute `to-ISP-A` menjadi *unreachable*;
   rute **cadangan** (`distance` lebih besar) diaktifkan.
10. **Koneksi lama** yang sudah di-mark ke ISP-A **tetap** mencoba jalur mati hingga
    *timeout* (inilah masalah *session disruption* yang dianalisis penelitian);
    **koneksi baru** mengikuti jalur alternatif.

---

## 6. Desain Multi-WAN

### 6.1 Interface list & alamat **[USULAN]**

```routeros
/interface ethernet
set [ find default-name=ether1 ] name=ether1-ISP-A comment="ISP A - Starlink"
set [ find default-name=ether2 ] name=ether2-ISP-B comment="ISP B - Starlink"
set [ find default-name=ether3 ] name=ether3-ISP-C comment="ISP C - Fiber Optic"

/interface list
add name=WAN
add name=LAN
/interface list member
add list=WAN interface=ether1-ISP-A
add list=WAN interface=ether2-ISP-B
add list=WAN interface=ether3-ISP-C
add list=LAN interface=bridge-LAN

# Starlink: DHCP client
/ip dhcp-client
add interface=ether1-ISP-A disabled=no comment="ISP A DHCP"
add interface=ether2-ISP-B disabled=no comment="ISP B DHCP"
# FO IndiHome: PPPoE (atau statik). Contoh PPPoE:
# /interface pppoe-client add name=pppoe-ISP-C interface=ether3-ISP-C user=<u> password=<p> \
#     disabled=no add-default-route=no use-peer-dns=yes
```

*(IP gateway tiap ISP: catat hasil DHCP/PPPoE untuk dipakai di rute §6.3.)*

### 6.2 Routing table per ISP (RouterOS v7) **[USULAN]**

```routeros
/routing table
add name=to-ISP-A fib
add name=to-ISP-B fib
add name=to-ISP-C fib
```

### 6.3 Rute default per ISP + failover **[USULAN]**

```routeros
# Rute utama tiap ISP (distance 1) dengan cek gateway
/ip route
add dst-address=0.0.0.0/0 gateway=<GW-A> routing-table=to-ISP-A \
    check-gateway=ping distance=1 comment="default-A"
add dst-address=0.0.0.0/0 gateway=<GW-B> routing-table=to-ISP-B \
    check-gateway=ping distance=1 comment="default-B"
add dst-address=0.0.0.0/0 gateway=<GW-C> routing-table=to-ISP-C \
    check-gateway=ping distance=1 comment="default-C"
```

### 6.4 Mangle PCC (inti load balancing) **[USULAN]**

**Pemetaan bucket → ISP.** Ambil $N$ bucket, lalu alokasikan **berurutan** sesuai
bobot (§2). Contoh **bobot 2:1:1** → $N=4$:

| Bucket PCC | ISP | Interface |
|---|---|---|
| `4/0`, `4/1` | ISP A | `ether1-ISP-A` |
| `4/2` | ISP B | `ether2-ISP-B` |
| `4/3` | ISP C | `ether3-ISP-C` |

```routeros
/ip firewall mangle
# --- Tandai koneksi sesuai bucket ---
add chain=prerouting in-interface-list=LAN dst-address-type=!local \
    per-connection-classifier=both-addresses-and-ports:4/0 \
    action=mark-connection new-connection-mark=conn-A passthrough=yes comment="PCC 4/0 -> A"
add chain=prerouting in-interface-list=LAN dst-address-type=!local \
    per-connection-classifier=both-addresses-and-ports:4/1 \
    action=mark-connection new-connection-mark=conn-A passthrough=yes comment="PCC 4/1 -> A"
add chain=prerouting in-interface-list=LAN dst-address-type=!local \
    per-connection-classifier=both-addresses-and-ports:4/2 \
    action=mark-connection new-connection-mark=conn-B passthrough=yes comment="PCC 4/2 -> B"
add chain=prerouting in-interface-list=LAN dst-address-type=!local \
    per-connection-classifier=both-addresses-and-ports:4/3 \
    action=mark-connection new-connection-mark=conn-C passthrough=yes comment="PCC 4/3 -> C"

# --- Peta connection mark -> routing mark ---
add chain=prerouting connection-mark=conn-A action=mark-routing \
    new-routing-mark=to-ISP-A passthrough=no
add chain=prerouting connection-mark=conn-B action=mark-routing \
    new-routing-mark=to-ISP-B passthrough=no
add chain=prerouting connection-mark=conn-C action=mark-routing \
    new-routing-mark=to-ISP-C passthrough=no
```

**[ANALISIS] Aturan penting:**
- `dst-address-type=!local` mencegah trafik ke router sendiri ikut ter-PCC.
- Gunakan `in-interface-list=LAN` agar hanya trafik *forwarded* yang di-PCC.
- **Bucket menentukan resolusi rasio.** $N=20$ → langkah **5%**; $N=100$ → **1%**.
  Ini batas granularitas untuk kontrol dinamis (§9).
- PCC menjaga konsistensi sesi (semua paket satu koneksi ke satu ISP) — menghindari
  *packet reordering* yang merusak TCP.

### 6.5 NAT masquerade per WAN **[USULAN]**

```routeros
/ip firewall nat
add chain=srcnat out-interface-list=WAN action=masquerade comment="NAT per WAN"
```

---

## 7. Mekanisme Failover

| Lapisan | Metode | Perilaku |
|---|---|---|
| **Rute** | `check-gateway=ping` + `distance` | Jika gateway utama tak terjawab, rute cadangan (distance lebih besar) aktif |
| **Interface** | `/tool netwatch` | Menandai ISP mati/hidup; menjalankan skrip |
| **Opsi lanjut** | **Rute rekursif** (scope/target-scope) | Cek keterjangkauan ke IP publik, bukan hanya gateway lokal |

**Contoh netwatch + skrip penanda:**

```routeros
/tool netwatch
add host=<GW-A> interval=10s timeout=1s \
    down-script="/ip route disable [find comment=\"default-A\"]" \
    up-script="/ip route enable [find comment=\"default-A\"]" comment="watch A"
```

**[ANALISIS] Batas failover berbasis rute:** ia **tidak menyelamatkan koneksi lama**
yang sudah di-mark ke ISP mati. Koneksi tersebut akan *timeout* — inilah *session
disruption* yang menjadi objek penelitian (lihat `07_Kebaruan_dan_Kontribusi.md`).
Karena itu, mekanisme PCC + failover ini adalah **baseline/aktuator**, bukan
kontribusi algoritmik.

---

## 8. Distribusi Jaringan LAN

```routeros
/interface bridge
add name=bridge-LAN comment="LAN"
/interface bridge port
add bridge=bridge-LAN interface=ether4   # ke Switch LAN
add bridge=bridge-LAN interface=ether5   # (opsional) AP
/ip address
add address=192.168.88.1/24 interface=bridge-LAN
/ip pool
add name=dhcp-lan ranges=192.168.88.10-192.168.88.250
/ip dhcp-server
add interface=bridge-LAN address-pool=dhcp-lan name=dhcp-lan disabled=no
/ip dhcp-server network
add address=192.168.88.0/24 gateway=192.168.88.1 dns-server=192.168.88.1
```

- **Switch LAN** → distribusi ke client kabel.
- **Access Point (AP)** → SSID Wi-Fi → client nirkabel.
- Semua client berada di `bridge-LAN`; **tidak** ada trafik LAN-ke-LAN yang di-PCC.

---

## 9. Integrasi Controller (kontrol dinamis rasio) **[USULAN]**

- **Kontroler eksternal** (`15_Arsitektur_Sistem.md`) membaca metrik → menghitung
  $Q_i(t)$ → menentukan rasio → **menulis ulang pemetaan bucket** di mangle via
  **API-SSL** (akun *write* terpisah).
- Perubahan rasio = **regenerasi aturan mangle** (bucket → ISP), bukan sekadar ubah
  angka; karena itu jumlah bucket $N$ menentukan **resolusi** kendali.
- Setiap perubahan: **snapshot → apply → verify → rollback** (aman-ke-gagal).

```routeros
# Contoh kerangka (dijalankan controller, bukan manual):
# 1) baca Q_i(t)  -> 2) hitung alokasi bucket  -> 3) set aturan mangle
#    /ip/firewall/mangle/set  per-connection-classifier=both-addresses-and-ports:N/k
```

**[ANALISIS]** PCC bersifat **diskret per bucket**; alokasi kontinu dari SAW harus
**dikuantisasi**. Ini gap **G-M2** (pemetaan skor kontinu → proporsi diskret).

---

## 10. Pengujian & Validasi

| Uji | Cara | Harapan |
|---|---|---|
| Distribusi bucket | Buat banyak koneksi dari client; cek `connection-mark` | Proporsi mendekati bobot §2 |
| Konsistensi sesi | Unduhan besar; cek jalur stabil | Satu sesi tetap di satu ISP |
| Failover | Putus salah satu ISP | Koneksi baru pindah; waktu pemulihan terukur |
| NAT per WAN | `torch`/log di tiap `out-interface` | Trafik keluar sesuai ISP |
| Tidak ada PCC LAN | Ping antar-client LAN | Tidak ter-mark |
| Keamanan | Akun read/write terpisah | Baca boleh, tulis hanya akun intervensi |

---

## 11. Batasan & Pengembangan

| Batasan | Catatan |
|---|---|
| Bucket diskret | Resolusi rasio dibatasi $N$ (mis. 5% untuk $N=20$) |
| Failover ≠ preservasi sesi | Koneksi lama ke ISP mati akan timeout |
| Kapasitas Starlink stokastik | Bobot statis cepat usang ⇒ perlu bobot adaptif |
| Satu admin domain | Semua ISP jenuh bersama bila switch/upstream bermasalah |

**Pengembangan (sesuai penelitian):** rasio PCC dihitung **dinamis** dari skor
kualitas multi-kriteria ($Q_i(t)$) dengan bobot adaptif, dan perlakuan sesi
dipisahkan (koneksi lama vs baru) — lihat `00_README.md` §6 dan `15`.

---

## 12. Yang Perlu Diisi **[USULAN]**

- [ ] Kapasitas **nyata** tiap ISP (kolom §2) → menentukan bobot & jumlah bucket $N$.
- [ ] Mode akses ISP-C: **PPPoE** atau **statik**; catat gateway-nya.
- [ ] IP target `check-gateway`/netwatch (sebaiknya IP publik stabil, bukan gateway
      lokal, agar gangguan upstream terdeteksi).
- [ ] Jumlah bucket $N$ (20 vs 100) untuk keseimbangan resolusi vs beban CPU.
- [ ] Port LAN/AP aktual (`ether4`+ mana yang dipakai).
- [ ] Kebijakan: apakah AP di-bridge ke `bridge-LAN` atau tersegmentasi.
