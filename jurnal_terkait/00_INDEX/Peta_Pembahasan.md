# Peta Pembahasan Jurnal

Gunakan tabel ini untuk memilih folder literatur berdasarkan subbab proposal. Urutan folder mengikuti alur Bab I–II, bukan abjad.

| Folder | Fokus | Relevansi Bab I | Relevansi Bab II | Kata kunci |
|---|---|---|---|---|
| `01_QoS_dan_Pengukuran` | QoS, pengukuran, standar | 1.2.1 Konsep QoS; 1.1 Latar belakang | 2.7 Pengukuran dan instrumen; 2.8 Analisis data | delay, jitter, packet loss, throughput, TIPHON, RT/RW Net |
| `02_FO_IndiHome_dan_Optik` | FO, IndiHome, GPON, RoF, PON | 1.1 Latar belakang; 1.2.2 Karakteristik FO | 2.1 Lokasi dan topologi; 2.6 Skenario | IndiHome, FTTH, GPON, MSAN, RoF, WDM-PON |
| `03_LEO_Starlink_dan_Satelit` | Starlink, LEO, satelit-terestrial | 1.1 Latar belakang; 1.2.2; 1.2.10 Celah | 2.6 Skenario; 2.7 Metrik; 2.9 Risiko cuaca | Starlink, one-way delay, rain fade, LEO, handover, satelit-terestrial |
| `04_PCC_MikroTik_dan_Load_Balancing` | PCC, ECMP, NTH, failover | 1.2.3 PCC; 1.2.4 Load balancing adaptif; 1.3 Rumusan masalah | 2.4.4 Pemetaan rasio; 2.5 Perangkat; 2.6 Baseline | PCC, ECMP, NTH, failover, MikroTik, RouterOS, bucket |
| `05_MCDM_SAW_EWMA_dan_Histeresis` | SAW, normalisasi, EWMA, histeresis | 1.2.5 MCDM/SAW; 1.2.6 EWMA; 1.2.7 Histeresis | 2.4.1 EWMA; 2.4.2 Skor SAW; 2.4.3 State machine | SAW, normalisasi, EWMA, hysteresis, threshold, dwell |
| `06_SDN_dan_Arsitektur_Kontrol` | SDN, OpenFlow, controller, SD-WAN | 1.2.9 Arsitektur tiga lapis; 1.2.10 Celah | 2.3 Arsitektur; 2.4 Algorithm Core; 2.11 Reproduksibilitas | SDN, OpenFlow, multi-controller, SD-WAN, policy routing |
| `07_QoE_dan_Aplikasi` | QoE dan aplikasi | 1.2.1 (pembeda QoS vs QoE); 1.7 Batasan | 2.9 Etika dan batasan pengukuran | QoE, video on demand, aplikasi |
| `08_Cloud_dan_Load_Balancing_Umum` | Cloud load balancing, data center | 1.2.4 Pendekatan terkait; 1.2.10 Celah | 2.2 Tahapan; 2.10 Jadwal (pembanding) | cloud, data center, ACO, WWO, load balancing |
| `09_Referensi_Umum_dan_Lainnya` | Referensi umum dan artikel tangential | 1.2.10 Celah; Lampiran A | 2.2 Tahapan; 2.11 Artefak | standar, kebijakan, IoT, orbit, UX |

## Alur Membaca yang Disarankan

1. **Untuk latar belakang dan celah:** mulai dari `03_LEO_Starlink_dan_Satelit`, lalu `04_PCC_MikroTik_dan_Load_Balancing`, `01_QoS_dan_Pengukuran`, dan `06_SDN_dan_Arsitektur_Kontrol`.
2. **Untuk metode:** `05_MCDM_SAW_EWMA_dan_Histeresis` (SAW, EWMA, histeresis), `04_PCC_MikroTik_dan_Load_Balancing` (pemetaan bucket), dan `06_SDN_dan_Arsitektur_Kontrol` (arsitektur tiga lapis).
3. **Untuk evaluasi:** `01_QoS_dan_Pengukuran` (metrik), `03_LEO_Starlink_dan_Satelit` (dinamika LEO dan cuaca), serta `04_PCC_MikroTik_dan_Load_Balancing` (baseline PCC).
4. **Untuk batasan dan etika:** `07_QoE_dan_Aplikasi` (QoS vs QoE) dan `09_Referensi_Umum_dan_Lainnya` (konteks kebijakan).

## Catatan

- Versi `annotated` berguna untuk melihat catatan/highlight, tetapi untuk sitasi gunakan versi utama.
- Beberapa artikel Indonesia adalah terjemahan/versi paralel dari artikel Inggris; lihat `Duplikat_Versi.md`.
- Jika suatu subbab belum memiliki sumber yang cukup, tambahkan ke `00_INDEX/unduhan_baru.csv` atau catat di `Daftar_Jurnal.md`.
