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
| 3 | Latar belakang FO–LEO–PCC |
| 4 | Masalah penelitian |
| 5 | Research gap |
| 6 | Novelty N1–N3 |
| 7 | Pertanyaan penelitian |
| 8 | Tujuan & hipotesis |
| 9 | Kerangka teori & dua proposisi |
| 10 | Arsitektur tiga lapis |
| 11 | Formalisasi inti |
| 12 | Desain eksperimen A–G |
| 13 | Metrik & instrumen |
| 14 | Rencana analisis |
| 15 | Baseline awal 2,2 jam |
| 16 | Kontribusi |
| 17 | Jadwal 20 minggu |
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
- Slide inti: **5 (gap), 6 (novelty), 9 (teori), 11 (formalisasi), 15 (baseline)**.
- Jangan mengklaim 15 detik dari baseline RTT. Klaim tersebut dikunci dari
  literatur: Garcia et al. (2025); Hammer et al. (2024); Mohan et al. (2024).
- Baseline 2,2 jam adalah pilot, bukan baseline final.
- Topologi formal: **dual-ISP A+C**; ISP-B sebagai validasi eksternal.

## Berkas

| Berkas | Fungsi |
|---|---|
| `Proposal_Tesis_SPA-HSM.pptx` | Deck presentasi |
| `build_pptx.py` | Skrip pembuat deck |
| `preview/` | Hasil ekspor PNG (lokal, tidak di-commit) |
