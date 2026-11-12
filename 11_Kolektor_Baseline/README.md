# Kolektor Baseline Read-Only

Kolektor untuk pra-penelitian pada RouterOS dengan akun **read-only**. Skrip ini
hanya memanggil endpoint `/print` dan `/ping` (test); tidak ada operasi
`add`, `set`, `remove`, `disable`, atau `enable`.

## Berkas

| Berkas | Fungsi |
|---|---|
| `collector.py` | Kolektor JSONL: resource, interface, route, mangle, NAT, service, group, netwatch, probe |
| `analyze_baseline.py` | Analisis: loss, RTT, jitter, periodisitas, korelasi, episode, throughput |
| `analyze_periodicity.py` | Analisis lanjutan: FFT periode dominan, ACF residual, korelasi dan tumpang tindih episode |
| `config.example.env` | Contoh konfigurasi; salin menjadi `.env` |
| `data/` | Output JSONL (di-ignore Git) |
| `logs/` | Log kolektor (di-ignore Git) |

## Instalasi

```bash
cd 11_Kolektor_Baseline
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install librouteros
```

Untuk analisis periodisitas lanjutan:

```bash
pip install numpy
```

Salin konfigurasi:

```bash
copy config.example.env .env      # Windows
cp config.example.env .env        # Linux/macOS
```

Isi `.env`:

```env
ROS_HOST=...
ROS_PORT=6187
ROS_USER=...
ROS_PASS=...
PROBE_INTERFACES=ether1-ISP-A,ether2-ISP-B,ether3-ISP-C
PROBE_TARGETS=1.1.1.1,8.8.8.8
DURATION=7d
```

**Jangan commit `.env`.** Folder `data/` dan `logs/` juga di-ignore.

## Uji Cepat

Ambil satu snapshot tanpa ping:

```bash
python collector.py --once --no-probe
```

Dengan ping per WAN (dijalankan **di router** melalui `/ping interface=...`):

```bash
python collector.py --once
```

Jika berhasil, akan muncul path data dan log di akhir.

## Jalankan Baseline

```bash
python collector.py --duration 7d
```

Atau tanpa batas (hentikan dengan Ctrl+C):

```bash
python collector.py
```

Interval default:

| Data | Interval |
|---|---:|
| Resource | 10 s |
| Interface | 10 s |
| Route | 60 s |
| Mangle | 60 s |
| NAT | 300 s |
| Service/group | 3600 s |
| Probe | 2 s |

Ubah lewat `.env`.

## Analisis

```bash
python analyze_baseline.py
```

Atau pilih file/folder:

```bash
python analyze_baseline.py --data-dir data --glob "baseline_*.jsonl"
```

Ambang episode:

```bash
python analyze_baseline.py --rtt-threshold 100 --loss-threshold 1
```

Luaran:

- `report_<timestamp>.md`
- `report_<timestamp>.json`

### Analisis periodisitas lanjutan

```bash
python analyze_periodicity.py data/baseline_*.jsonl
```

Luaran: file `*.periodicity.md` di folder `data/`.

Isi: periode dominan (FFT), ACF residual lag 15 detik, autokorelasi indikator
buruk, korelasi antar-WAN, Jaccard episode, dan kecocokan episode ±2 detik.

Isi laporan:

1. ringkasan probe per WAN,
2. periodisitas (autokorelasi lag 1–60 detik),
3. korelasi antar-interface,
4. episode degradasi sederhana,
5. throughput dari delta counter interface,
6. snapshot route/mangle/service.

## Skema Data

Satu baris JSON per observasi:

```json
{
  "ts_utc": "2026-11-13T01:23:45+00:00",
  "site": "rt-rw-net-buru",
  "router": "rb1100ahx4",
  "kind": "probe",
  "data": {
    "interface": "ether1-ISP-A",
    "target": "1.1.1.1",
    "success": true,
    "rtt_ms": 45.793,
    "packet_loss": "0",
    "sent": 1,
    "received": 1
  }
}
```

`kind`: `meta`, `resource`, `identity`, `interface`, `ethernet`, `address`,
`route`, `mangle`, `nat`, `service`, `group`, `netwatch`, `probe`, `error`.

## Keamanan

1. Gunakan akun **read-only** (`read` group, tanpa `write`/`policy`).
2. Jangan membuka API/REST ke WAN; gunakan VPN/tunnel.
3. Ganti password default; simpan di pengelola sandi.
4. Batasi `address` user ke IP kolektor.
5. API-SSL saat ini memakai cipher ADH tanpa sertifikat; sebaiknya pasang
   sertifikat valid atau akses melalui VPN.
6. Skrip ini tidak menangkap payload dan tidak menyimpan kredensial.

## Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `handshake_failure` | Cipher ADH tidak didukung default | Skrip sudah memakai `ALL:@SECLEVEL=0` + `OP_LEGACY_SERVER_CONNECT` |
| `TimeoutError` | Koneksi/jaringan lambat | Naikkan timeout atau cek tunnel |
| `TrapError unknown parameter` | Versi RouterOS berbeda | Gunakan parameter yang didukung; `/ping interface=` sudah diuji |
| Data probe kosong | `/ping` tidak diizinkan | Pastikan group punya policy `test` |
| Koneksi tabel timeout | Tabel conntrack besar | Biarkan `--connections` nonaktif |

## Batasan

- Episode dihitung dari sampel probe, bukan dari $Q_i(t)$ penuh.
- Periodisitas bergantung pada interval probe dan kualitas timestamp.
- Korelasi Pearson mengasumsikan hubungan linier.
- Data ini observasional; tidak ada klaim kausal.
