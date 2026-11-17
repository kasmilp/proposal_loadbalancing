# Presentasi Proposal Tesis

**Berkas utama:** `Proposal_Tesis_SPA-HSM.pptx`
**Jumlah slide:** 20
**Rasio:** 16:9
**Catatan pembicara:** tersedia di setiap slide

## Susunan

| Slide | Isi |
|---:|---|
| 1 | Judul |
| 2 | Agenda |
| 3 | Latar belakang FO–LEO–PCC (PCC = aktuator) |
| 4 | Masalah: flapping, gangguan sesi, stok menumpuk |
| 5 | Research gap: G-M3 dan G-E2 |
| 6 | Novelty: stock-flow, preservasi sesi, SIWG+ELS |
| 7 | Pertanyaan penelitian (6 RQ) |
| 8 | Tujuan & hipotesis (termasuk H3c) |
| 9 | Kerangka teori & tiga proposisi |
| 10 | Arsitektur tiga lapis |
| 11 | Formalisasi inti + rumus stock-flow |
| 12 | Desain eksperimen A–H |
| 13 | Metrik & instrumen (ELS/TTR/retention) |
| 14 | Rencana analisis (H3c) |
| 15 | Baseline awal 2,2 jam + snapshot stok |
| 16 | Kontribusi |
| 17 | Jadwal 22 minggu |
| 18 | Risiko, keselamatan, etika |
| 19 | Batasan |
| 20 | Penutup |

## Cara Membangun Ulang

```bash
pip install python-pptx
python build_pptx.py
```

Skrip akan menimpa `Proposal_Tesis_SPA-HSM.pptx`.

## Cara Mengekspor Preview

Buka di PowerPoint, lalu:

- **File → Export → PDF**, atau
- **File → Save As → PNG**.

Untuk pemeriksaan cepat di Windows, folder `preview/` dapat dibuat dengan
COM automation (tidak disimpan di Git).

## Catatan Presentasi

- Durasi target: **15–20 menit**.
- Slide inti: **5 (gap), 6 (novelty), 9 (teori), 11 (formalisasi), 12 (desain), 15 (baseline)**.
- Jangan mengklaim 15 detik dari baseline RTT. Klaim tersebut dikunci dari
  literatur: Garcia et al. (2025); Hammer et al. (2024); Mohan et al. (2024).
- Baseline 2,2 jam adalah pilot, bukan baseline final.
- Topologi formal: **dual-ISP A+C**; ISP-B sebagai validasi eksternal.
- Novelty utama: **alokasi stock-flow aware + preservasi sesi**, bukan “PCC dinamis”.
- Kondisi H (*stock-aware*) dan H3c wajib disebut saat membahas metode.
- Stok koneksi: snapshot 17 Nov menunjukkan 15.914 koneksi; ini bukti awal,
  bukan hasil eksperimen.

## Berkas

| Berkas | Fungsi |
|---|---|
| `Proposal_Tesis_SPA-HSM.pptx` | Deck presentasi |
| `build_pptx.py` | Skrip pembuat deck |
| `preview/` | Hasil ekspor PNG (lokal, tidak di-commit) |
