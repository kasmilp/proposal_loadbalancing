# Arsitektur Sistem SPA-HSM dan Pemetaan Kontribusi

Folder ini memuat diagram arsitektur sistem SPA-HSM beserta penandaan kontribusi
penelitian (K1–K4) pada setiap lapisan.

## Berkas

| Berkas | Keterangan |
|---|---|
| `arsitektur_spahsm_kontribusi.png` | Diagram siap pakai untuk dokumen (220 dpi) |
| `arsitektur_spahsm_kontribusi.svg` | Versi vektor, dapat diperbesar tanpa pecah |
| `arsitektur_spahsm_kontribusi.py` | Skrip pembuat diagram (matplotlib) |

Menjalankan ulang:

```bash
python arsitektur/arsitektur_spahsm_kontribusi.py
```

## Tiga lapis inti

1. **Algorithm Core** — EWMA smoother, SAW scorer, *asymmetric hysteresis state
   machine*, dan pemetaan status/skor ke target rasio PCC.
2. **Abstract Allocation Interface (Kontrak)** — `read_metrics()`, `set_ratio()`,
   `set_affinity()`, `get_state()`, `verify()`, `rollback()`, serta direktif
   `AFFINITY_LOCK`.
3. **Platform Adapter / Execution** — `MikroTikAdapter` (PCC *mangle/routing*,
   *conntrack*, `connection-state=new`) dan `MockAdapter` untuk uji kontrak.

## Dua bidang pendukung

- **Bidang Pengukuran** — probe RTT/jitter/packet loss/goodput, SNMP, dan
  telemetri RouterOS sebagai masukan bagi Algorithm Core.
- **Bidang Evaluasi & Ablasi** — *scenario runner*, *metric collector*, dan uji
  statistik; mengatur mode histeresis (none/simetris/asimetris) serta
  *affinity lock* (on/off).

## Pemetaan kontribusi ke lapisan

| Kode | Kontribusi | Lapisan penanda | Komponen kunci | Bukti/artefak |
|---|---|---|---|---|
| **K1** | Formulasi SPA-HSM yang menyatukan EWMA, SAW, histeresis asimetris, dan preservasi sesi | Lapis 1 dan Lapis 2 | EWMA smoother, SAW scorer, *state machine*, `AFFINITY_LOCK` | Tabel parameter dan skor, pseudocode, hasil ablasi |
| **K2** | Arsitektur tiga lapis dengan kontrak antarmuka yang dapat diuji | Batas Lapis 1–2–3 | `Abstract Allocation Interface`, `MockAdapter`, `verify()`, `rollback()` | Uji konformitas antarmuka, H3 |
| **K3** | Evaluasi ablasi yang memisahkan kontribusi histeresis dan *affinity lock* | Bidang evaluasi (mengontrol Lapis 1 dan 2) | Faktorial 3 × 2, skenario A–H | Tabel skenario, metrik, analisis |
| **K4** | Bukti empiris pada jaringan FO–LEO skala RT/RW Net | Bidang pengukuran dan Lapis 3 | Probe, SNMP, `MikroTikAdapter`, data lapangan | Data *staging* dan lapangan, Bab II 2.1 dan 2.5 |

## Catatan pembacaan

- **K1** melekat pada jalur keputusan: EWMA dan SAW di Lapis 1, sedangkan
  preservasi sesi diwujudkan sebagai flag `AFFINITY_LOCK` di Lapis 2.
- **K2** adalah kontribusi pada batas antarmuka, sehingga ditandai di antara
  Lapis 1, 2, dan 3.
- **K3** bukan lapisan *runtime*, melainkan bidang lintas lapis yang mengatur
  mode histeresis dan status *affinity* lalu mengukur akibatnya.
- **K4** adalah kontribusi pada bukti empiris, sehingga ditandai di bidang
  pengukuran, adapter MikroTik, dan jaringan produksi.
