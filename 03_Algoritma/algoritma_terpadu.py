#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
algoritma_terpadu.py — SATU BERKAS berisi SELURUH algoritma yang dibahas di
repositori `proposal_loadbalancing`, ditambah SATU algoritma pembobotan baru
(TW-SAW) sebagai arah pengembangan.

Tujuan berkas ini
-----------------
Menjadi *single source of truth* untuk kode prototipe (tahap T4–T6 pada
`02_Pembahasan_Final_Proposal/01_Struktur_Langkah_Penelitian_S2.md`) sehingga
penjelasan di Bab III dan implementasi tidak lagi tersebar di arsip.

Peta algoritma → dokumen sumber
-------------------------------
| # | Algoritma / fungsi                         | Sumber di repo                                        |
|---|--------------------------------------------|-------------------------------------------------------|
| A1| Segmentasi + resampling 2 s → 1 s          | `01/15` §12, `01/19` §4.4A, P2                        |
| A2| EWMA penghalus metrik                      | `01/05` §2(1), Roberts (1959)                         |
| A3| Normalisasi N-a/N-b/N-c/N-d                | `01/04` §2, `01/05` §2(2)                             |
| A4| Bobot statis-ahli / sama / Entropy / CRITIC| `01/04` §3, `01/05` §2(3)                             |
| A4b| Bobot MEREC                               | `01/04` §3.2, `01/06` baris 20                        |
| A4c| Bobot hibrida γ                           | `01/04` §3.4, `01/05` §2(3)                           |
| A4d| **TW-SAW (baru)** bobot stabil-temporal   | berkas ini §A4d + `00_README_Algoritma.md`            |
| A5| Skor SAW Q_i(t) 0–100                      | `01/05` §2, `01/13` §2.2                              |
| A6| Gerbang histeresis (none/simetris/asimetris)| `01/05` §2(4), `01/13` §3, `01/08` §4a (perlakuan B/D/F)|
| A7| State machine tri-link 8 state             | `01/15` §8                                            |
| A8| Target rasio + headroom                    | arsip `06_Tahap_04/02` §5.1–5.2                       |
| A9| Bucket mapping N=20, b_min/b_max           | `01/15` §9, arsip `02` §5.5                           |
| A10| Alokasi sadar-stok (κ)                    | arsip `03_Tahap_02/02` §1.9, `01/18` K-E              |
| A11| Metrik: flap, recovery, ELS, TTR, RST/SIWG | arsip `03_Tahap_02/02` §1, `01/08` §6                 |
| A12| Pelabelan episode                          | `01/19` §4.2, `11_Kolektor_Baseline/analyze_baseline.py`|
| A13| Periodisitas: ACF, FFT, korelasi, Jaccard  | `11_Kolektor_Baseline/analyze_periodicity.py`         |
| A14| Ablasi normalisasi × pembobotan            | `01/08` §5, `01/18` K-A/K-D, P1                       |

Berkas ini **hanya memakai pustaka standar Python** (tanpa numpy/scipy) agar
dapat dijalankan pada `.venv` repositori apa adanya.

Cara pakai
----------
    python algoritma_terpadu.py selftest        # uji golden (harus lulus)
    python algoritma_terpadu.py demo            # data sintetis + tabel hasil
    python algoritma_terpadu.py ablation        # bandingkan semua pembobot
    python algoritma_terpadu.py replay --seconds 1800
                                                # replay dataset baseline asli
    python algoritma_terpadu.py replay --ablation --seconds 900

Konvensi label: [FAKTA] diambil dari kode/dokumen · [USULAN] desain baru.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict, deque
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable, Sequence

# =============================================================================
# 0. KONSTANTA & KONFIGURASI
# =============================================================================

LINK_A = "ether1-ISP-A"   # Starlink LEO-1
LINK_B = "ether2-ISP-B"   # Starlink LEO-2
LINK_C = "ether3-ISP-C"   # FO IndiHome
LINKS = (LINK_A, LINK_B, LINK_C)

CRITERIA = ("delay", "jitter", "loss", "thr")

CRIT_META = {
    "delay":  {"label": "Delay (RTT)",        "unit": "ms",   "dir": "cost",    "ref": (0.0, 150.0)},
    "jitter": {"label": "Jitter",             "unit": "ms",   "dir": "cost",    "ref": (0.0, 30.0)},
    "loss":   {"label": "Packet loss",        "unit": "%",    "dir": "cost",    "ref": (0.0, 5.0)},
    "thr":    {"label": "Throughput/headroom","unit": "Mbps", "dir": "benefit", "ref": (0.0, 100.0)},
}

# Bobot ahli naskah lama (`01/05` §1): w_D=0.30, w_J=0.25, w_PL=0.25, w_T=0.20
EXPERT_W = {"delay": 0.30, "jitter": 0.25, "loss": 0.25, "thr": 0.20}

# Bobot alternatif dari arsip formalisasi (`06_Tahap_04/02` §3.3)
ARCHIVE_W = {"delay": 0.30, "jitter": 0.15, "loss": 0.20, "thr": 0.35}

# Label state per link
STABLE = "B"        # Baik / STABLE
DEGRADED = "T"      # Terdegradasi / DEGRADED


# =============================================================================
# A0. UTILITAS UMUM
# =============================================================================

def mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def stdev(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = sum(values) / len(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def percentile(values: Sequence[float], p: float) -> float | None:
    """Persentil dengan interpolasi linear (sama seperti analyze_baseline.py)."""
    if not values:
        return None
    data = sorted(values)
    if len(data) == 1:
        return data[0]
    rank = (len(data) - 1) * p
    lo, hi = math.floor(rank), math.ceil(rank)
    if lo == hi:
        return data[lo]
    return data[lo] + (data[hi] - data[lo]) * (rank - lo)


def pearson(x: Sequence[float], y: Sequence[float]) -> float | None:
    n = min(len(x), len(y))
    if n < 3:
        return None
    xs, ys = list(x[:n]), list(y[:n])
    mx, my = mean(xs), mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    dy = math.sqrt(sum((b - my) ** 2 for b in ys))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def _rank(values: Sequence[float]) -> list[float]:
    """Peringkat dengan penanganan seri (rata-rata peringkat)."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x: Sequence[float], y: Sequence[float]) -> float | None:
    """Korelasi peringkat Spearman tanpa scipy (untuk metrik akurasi Q)."""
    if len(x) < 3 or len(y) < 3:
        return None
    return pearson(_rank(x), _rank(y))


def auc_score(labels: Sequence[int], scores: Sequence[float]) -> float | None:
    """
    AUC untuk deteksi episode (label 1 = degradasi).
    `scores` = skor "semakin tinggi semakin buruk" (mis. 100 - Q).
    """
    pos = [s for l, s in zip(labels, scores) if l == 1]
    neg = [s for l, s in zip(labels, scores) if l == 0]
    if not pos or not neg:
        return None
    ranks = _rank(scores)
    rank_pos = sum(r for r, l in zip(ranks, labels) if l == 1)
    n1, n0 = len(pos), len(neg)
    return (rank_pos - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def _normalize_dict(w: dict[str, float], floor: float = 1e-12) -> dict[str, float]:
    total = sum(max(v, 0.0) for v in w.values())
    if total <= floor:
        n = len(w) or 1
        return {k: 1.0 / n for k in w}
    return {k: max(v, 0.0) / total for k, v in w.items()}


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _round_or_none(value: float | None, digits: int = 4) -> float | None:
    return None if value is None else round(value, digits)


# =============================================================================
# A1. SEGMENTASI & RESAMPLING 2 s → 1 s  [P2, C-4]
# =============================================================================

def parse_ts(value: str) -> float | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def split_segments(rows: Sequence[dict], gap_s: float = 300.0) -> list[list[dict]]:
    """
    Pecah deret menjadi segmen kontinu.
    Aturan `01/19` §4.4A: JANGAN menginterpolasi lintas celah — korelasi yang
    dihitung pada grid penuh lintas hari kosong adalah artefak.
    """
    if not rows:
        return []
    rows = sorted(rows, key=lambda r: r["t"])
    segs, cur = [], [rows[0]]
    for r in rows[1:]:
        if r["t"] - cur[-1]["t"] > gap_s:
            segs.append(cur)
            cur = [r]
        else:
            cur.append(r)
    segs.append(cur)
    return segs


def resample_1s(rows: Sequence[dict], policy: str = "interp") -> tuple[list[float], list[dict]]:
    """
    Resampling ke grid 1 detik DALAM satu segmen.

    policy:
      - "interp"    : interpolasi linear nilai valid (default, dipakai analisis)
      - "aggregate" : rata-rata sampel yang jatuh pada detik yang sama
      - "ffill"     : tahan nilai terakhir (step function, untuk counter)
    """
    if not rows:
        return [], []
    t0 = math.floor(rows[0]["t"])
    t1 = math.ceil(rows[-1]["t"])
    grid = [float(t) for t in range(int(t0), int(t1) + 1)]
    out: list[dict] = []

    if policy == "aggregate":
        buckets: dict[int, list[dict]] = defaultdict(list)
        for r in rows:
            buckets[int(math.floor(r["t"]))].append(r)
        last = None
        for g in grid:
            here = buckets.get(int(g), [])
            if here:
                agg = {}
                for key in here[0]:
                    if key == "t":
                        continue
                    vals = [h[key] for h in here if isinstance(h.get(key), (int, float))]
                    agg[key] = mean(vals) if vals else None
                last = agg
            out.append(dict(last or {}))
        return grid, out

    if policy == "ffill":
        j = 0
        last = dict(rows[0])
        for g in grid:
            while j + 1 < len(rows) and rows[j + 1]["t"] <= g:
                j += 1
                last = dict(rows[j])
            out.append(dict(last))
        return grid, out

    # interpolasi linear per kunci numerik
    keys = [k for k, v in rows[0].items() if k != "t" and isinstance(v, (int, float))]
    prepared = {}
    for k in keys:
        pts = [(r["t"], r[k]) for r in rows if isinstance(r.get(k), (int, float))]
        prepared[k] = pts
    for g in grid:
        rec = {}
        for k, pts in prepared.items():
            if not pts:
                rec[k] = None
                continue
            if g <= pts[0][0]:
                rec[k] = pts[0][1]
            elif g >= pts[-1][0]:
                rec[k] = pts[-1][1]
            else:
                lo, hi = 0, len(pts) - 1
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if pts[mid][0] <= g:
                        lo = mid
                    else:
                        hi = mid
                (ta, va), (tb, vb) = pts[lo], pts[hi]
                rec[k] = va if tb == ta else va + (vb - va) * (g - ta) / (tb - ta)
        out.append(rec)
    return grid, out


def load_jsonl_probes(
    paths: Sequence[Path],
    interfaces: Sequence[str] = LINKS,
    duration_s: float | None = None,
) -> tuple[dict[tuple[str, str], list[dict]], list[dict], float | None]:
    """
    Baca JSONL kolektor. Mengembalikan:
      probes[(interface, target)] = [{t, rtt, loss, success}]
      interface_rows[interface]   = [{t, rx, tx, running}]
      t_start
    """
    probes: dict[tuple[str, str], list[dict]] = defaultdict(list)
    iface_rows: dict[str, list[dict]] = defaultdict(list)
    t_start = None

    for path in paths:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if '"kind": "probe"' not in line and '"kind": "interface"' not in line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = parse_ts(rec.get("ts_utc", ""))
                if t is None:
                    continue
                if t_start is None:
                    t_start = t
                if duration_s is not None and t - t_start > duration_s:
                    continue
                kind, data = rec.get("kind"), rec.get("data")
                if kind == "probe" and isinstance(data, dict):
                    iface = data.get("interface")
                    if iface not in interfaces:
                        continue
                    probes[(iface, data.get("target"))].append({
                        "t": t,
                        "rtt": data.get("rtt_ms"),
                        "loss": float(data.get("packet_loss") or 0.0),
                        "success": bool(data.get("success")),
                    })
                elif kind == "interface" and isinstance(data, list):
                    for item in data:
                        name = item.get("name")
                        if name not in interfaces:
                            continue
                        try:
                            rx = int(str(item.get("rx-byte", "0")))
                            tx = int(str(item.get("tx-byte", "0")))
                        except ValueError:
                            continue
                        iface_rows[name].append({"t": t, "rx": rx, "tx": tx})
    return probes, [dict(iface=i, rows=r) for i, r in iface_rows.items()], t_start


def build_replay_dataset(
    paths: Sequence[Path],
    duration_s: float | None = 1800.0,
    capacity_mbps: dict[str, float] | None = None,
) -> list[dict]:
    """
    Ubah JSONL mentah menjadi dataset siap-pipeline:
      [{t, links: {link: {delay, jitter, loss, thr, util}}}, ...]

    Catatan metodologis:
      - Probe 2 s → grid 1 s (P2). Jitter = |ΔRTT| per detik.
      - Throughput dari delta counter interface (RX, Mbps) → step 1 s.
      - Bila sebuah link tidak punya delta counter pada suatu detik, baris
        dilewati (tidak diisi 0 palsu, tidak diinterpolasi lintas celah).
      - **Kapasitas efektif** = p95 throughput pada segmen (bukan angka iklan),
        sesuai `01/16` §2 ("kapasitas efektif dari baseline"). Dapat
        ditimpa lewat argumen `capacity_mbps` (mis. dari kontrak ISP).
    """
    probes, iface_rows, t_start = load_jsonl_probes(paths, duration_s=duration_s)
    if t_start is None:
        return []

    # --- probe per link: gabungkan beberapa target (median RTT, maks loss)
    per_link: dict[str, dict[float, dict]] = defaultdict(dict)
    for (iface, _target), rows in probes.items():
        for seg in split_segments(rows):
            grid, res = resample_1s(seg, "interp")
            for g, r in zip(grid, res):
                rtt = r.get("rtt")
                rec = per_link[iface].setdefault(g, {"rtt": [], "loss": []})
                if rtt is not None:
                    rec["rtt"].append(rtt)
                rec["loss"].append(r.get("loss") or 0.0)

    # --- throughput per link dari counter
    thr_by_link: dict[str, dict[float, float]] = defaultdict(dict)
    for item in iface_rows:
        iface, rows = item["iface"], item["rows"]
        if len(rows) < 2:
            continue
        grid, res = resample_1s(rows, "ffill")
        prev = None
        for g, r in zip(grid, res):
            if prev is not None and r.get("t") is not None:
                dt = r["t"] - prev["t"]
                if 0 < dt <= 60:
                    mbps = (r["rx"] - prev["rx"]) * 8 / dt / 1e6
                    if mbps >= 0:
                        thr_by_link[iface][g] = mbps
            prev = r
        # isi detik tanpa delta dengan nilai terakhir
        last = None
        for g in sorted(grid):
            if g in thr_by_link[iface]:
                last = thr_by_link[iface][g]
            elif last is not None:
                thr_by_link[iface][g] = last

    # --- kapasitas efektif: p95 throughput per link pada jendela ini,
    # kecuali ditimpa eksplisit oleh pemanggil (mis. kapasitas kontrak).
    if capacity_mbps:
        cap = {link: float(capacity_mbps.get(link, 0.0)) or 1.0 for link in LINKS}
    else:
        cap = {}
        for link in LINKS:
            vals = list(thr_by_link.get(link, {}).values())
            p95 = percentile(vals, 0.95) if vals else None
            cap[link] = max(p95 or 1.0, 1.0)
    cap_note = {k: round(v, 2) for k, v in cap.items()}

    # --- rakitan
    # Hanya detik ketika KETIGA link punya delta counter yang diketahui.
    # Tanpa syarat ini, detik-detik awal (sebelum delta pertama) akan berisi
    # throughput 0 palsu — artefak yang justru dilarang (lihat `01/19` §4.4A).
    common = None
    for iface in cap:
        known = set(thr_by_link.get(iface, {}))
        common = known if common is None else (common & known)
    dataset: list[dict] = []
    if not common:
        return dataset

    prev_rtt: dict[str, float] = {}
    for g in sorted(common):
        links = {}
        for iface in cap:
            rec = per_link[iface].get(g)
            if not rec or not rec["rtt"]:
                continue
            rtt = statistics.median(rec["rtt"])
            jitter = abs(rtt - prev_rtt[iface]) if iface in prev_rtt else 0.0
            prev_rtt[iface] = rtt
            loss = max(rec["loss"]) if rec["loss"] else 0.0
            thr = thr_by_link[iface][g]
            links[iface] = {
                "delay": rtt,
                "jitter": jitter,
                "loss": loss,
                "thr": thr,
                "util": clip(thr / cap[iface], 0.0, 1.0),
            }
        if len(links) == len(cap):
            dataset.append({"t": g - t_start if t_start else g, "links": links,
                            "capacity": dict(cap)})
    return dataset


# =============================================================================
# A2. EWMA  [Roberts 1959; `01/05` §2(1)]
# =============================================================================

def ewma_value(prev: float | None, x: float, alpha: float) -> float:
    """E_t = α·x_t + (1−α)·E_{t−1}. Jendela efektif ≈ 2/α − 1 sampel."""
    if prev is None:
        return float(x)
    return alpha * float(x) + (1.0 - alpha) * prev


def ewma_series(series: Iterable[float], alpha: float) -> list[float]:
    out, prev = [], None
    for x in series:
        prev = ewma_value(prev, x, alpha)
        out.append(prev)
    return out


# =============================================================================
# A3. NORMALISASI N-a / N-b / N-c / N-d  [`01/04` §2]
# =============================================================================

def _norm_na(x: float, meta: dict, cross: Sequence[float]) -> float:
    """N-a (naskah lama): cost min/x, benefit x/max. Rentang (0,1]."""
    if meta["dir"] == "cost":
        mn = min([c for c in cross if c is not None] or [x])
        return clip(mn / x, 0.0, 1.0) if x > 0 else 1.0
    mx = max([c for c in cross if c is not None] or [x])
    return clip(x / mx, 0.0, 1.0) if mx > 0 else 0.0


def _norm_nb(x: float, meta: dict, cross: Sequence[float]) -> float:
    """N-b: min–max. Batas bergeser tiap siklus → komparabilitas rendah."""
    vals = [c for c in cross if c is not None] or [x]
    mn, mx = min(vals), max(vals)
    if mx - mn <= 1e-12:
        return 1.0
    if meta["dir"] == "cost":
        return clip((mx - x) / (mx - mn), 0.0, 1.0)
    return clip((x - mn) / (mx - mn), 0.0, 1.0)


def _norm_nc(x: float, meta: dict, cross: Sequence[float]) -> float:
    """N-c (default): clip ke batas acuan tetap TIPHON/Y.1541."""
    lo, hi = meta["ref"]
    if hi - lo <= 1e-12:
        return 1.0
    if meta["dir"] == "cost":
        return clip((hi - x) / (hi - lo), 0.0, 1.0)
    return clip((x - lo) / (hi - lo), 0.0, 1.0)


def _norm_nd(x: float, meta: dict, cross: Sequence[float]) -> float:
    """N-d: normalisasi vektor (x / ||x||). Tidak dipakai (pembanding)."""
    vals = [c for c in cross if c is not None] or [x]
    if meta["dir"] == "cost":
        inv = [(1.0 / c) if c > 0 else 0.0 for c in vals]
        norm = math.sqrt(sum(v * v for v in inv)) or 1.0
        return clip(((1.0 / x) if x > 0 else 0.0) / norm, 0.0, 1.0)
    norm = math.sqrt(sum(c * c for c in vals)) or 1.0
    return clip(x / norm, 0.0, 1.0)


NORMALIZERS: dict[str, Callable[[float, dict, Sequence[float]], float]] = {
    "n-a": _norm_na,
    "n-b": _norm_nb,
    "n-c": _norm_nc,
    "n-d": _norm_nd,
}
DEFAULT_NORMALIZER = "n-c"


def normalize_row(
    smoothed: dict[str, dict[str, float]],
    links: Sequence[str] = LINKS,
    method: str = DEFAULT_NORMALIZER,
) -> dict[str, dict[str, float]]:
    """Normalisasi per kriteria dengan 'cross' = nilai ketiga link."""
    fn = NORMALIZERS[method]
    out: dict[str, dict[str, float]] = {link: {} for link in links}
    for crit in CRITERIA:
        cross = [smoothed[link][crit] for link in links if link in smoothed]
        meta = CRIT_META[crit]
        for link in links:
            if link in smoothed:
                out[link][crit] = fn(smoothed[link][crit], meta, cross)
    return out


# =============================================================================
# A4. PEMBOBOTAN
# =============================================================================

def weights_expert(_window=None, _prev=None, ctx=None) -> dict[str, float]:
    """A4a. Bobot statis-ahli (naskah lama)."""
    return dict(ctx["expert"])


def weights_equal(_window=None, _prev=None, _ctx=None) -> dict[str, float]:
    """A4b. Bobot sama-rata 1/4 (baseline naif)."""
    return {c: 1.0 / len(CRITERIA) for c in CRITERIA}


def _window_matrix(window: Sequence[dict[str, dict[str, float]]]) -> list[list[float]]:
    """Ratakan jendela → matriks alternatif × kriteria (pooled)."""
    rows = []
    for snap in window:
        for _link, vals in snap.items():
            rows.append([vals[c] for c in CRITERIA])
    return rows


def weights_entropy(window, _prev=None, _ctx=None) -> dict[str, float]:
    """
    A4c. Entropy [`01/04` §3.2].
    p_ij = r_ij / Σ_i r_ij ; e_j = −(1/ln m) Σ p ln p ; w_j = (1−e_j)/Σ(1−e_k)
    """
    matrix = _window_matrix(window)
    m = len(matrix)
    if m < 2:
        return {c: 1.0 / len(CRITERIA) for c in CRITERIA}
    w = {}
    for j, crit in enumerate(CRITERIA):
        col = [matrix[i][j] for i in range(m)]
        total = sum(col)
        if total <= 1e-12:
            w[crit] = 0.0
            continue
        e = 0.0
        for v in col:
            p = v / total
            if p > 1e-12:
                e -= p * math.log(p)
        e /= math.log(m)
        w[crit] = max(0.0, 1.0 - e)
    return _normalize_dict(w)


def weights_critic(window, _prev=None, _ctx=None) -> dict[str, float]:
    """
    A4d. CRITIC: C_j = σ_j · Σ_k (1 − ρ_jk) ; w_j = C_j / Σ C_k.
    σ dan ρ dihitung pada matriks pooled (jendela × link).
    """
    matrix = _window_matrix(window)
    if len(matrix) < 3:
        return {c: 1.0 / len(CRITERIA) for c in CRITERIA}
    cols = {crit: [row[j] for row in matrix] for j, crit in enumerate(CRITERIA)}
    sigma = {c: stdev(cols[c]) for c in CRITERIA}
    cval = {}
    for c in CRITERIA:
        conflict = 0.0
        for k in CRITERIA:
            if k == c:
                continue
            r = pearson(cols[c], cols[k]) or 0.0
            conflict += (1.0 - r)
        cval[c] = sigma[c] * conflict
    return _normalize_dict(cval)


def weights_merec(window, _prev=None, _ctx=None) -> dict[str, float]:
    """
    A4e. MEREC (Removal Effects of Criteria).
    S_i   = ln(1 + (1/m) Σ_j |ln r_ij|)
    S'_ij = ln(1 + (1/m) Σ_{k≠j} |ln r_ik|)
    E_j   = Σ_i |S'_ij − S_i| ; w_j = E_j / Σ E_k
    """
    matrix = _window_matrix(window)
    if len(matrix) < 2:
        return {c: 1.0 / len(CRITERIA) for c in CRITERIA}
    m = len(CRITERIA)
    safe = [[min(max(v, 1e-6), 1.0) for v in row] for row in matrix]
    logs = [[abs(math.log(v)) for v in row] for row in safe]
    s_i = [math.log(1.0 + sum(row) / m) for row in logs]
    effects = {}
    for j, crit in enumerate(CRITERIA):
        e = 0.0
        for i, row in enumerate(logs):
            without = (sum(row) - row[j]) / m
            e += abs(math.log(1.0 + without) - s_i[i])
        effects[crit] = e
    return _normalize_dict(effects)


def weights_hybrid(window, _prev=None, ctx=None) -> dict[str, float]:
    """
    A4f. Hibrida γ: w_j(t) = γ·w_j^ahli + (1−γ)·w_j^obj(t)  [`01/04` §3.4].
    CATATAN: bobot objektif dihitung ulang tiap siklus pada jendela geser —
    inilah sumber *chattering* yang dikritik pada B-1/G-W1.
    """
    p = ctx["params"]
    obj_fn = ctx["obj_fn"]
    obj = obj_fn(window)
    mixed = {c: p.gamma * ctx["expert"][c] + (1.0 - p.gamma) * obj[c] for c in CRITERIA}
    return _normalize_dict(mixed)


def weights_temporal(window, _prev=None, ctx=None) -> dict[str, float]:
    """
    A4g. **TW-SAW — Temporal-Stability Weighting (ALGORITMA BARU [USULAN]).**

    Masalah yang diserang (G-N2 + G-W1 + B-1):
      Hibrida γ masih memperbarui w_obj setiap siklus dari jendela yang bising.
      Kriteria yang derau-nya paling besar justru bisa memperoleh bobot besar
      (Entropy/CRITIC menghargai dispersi), sehingga Q berkedip.

    Empat komponen:
      1. Bobot objektif dasar  w^obj  (Entropy/CRITIC/MEREC) pada jendela N.
      2. **Reliabilitas belah-dua** (split-half reliability):
             d_j = |w_j^A − w_j^B| / (w_j^A + w_j^B)
             ρ_j = 1 / (1 + λ·d_j)
         w_j^A dan w_j^B dihitung pada dua paruh jendela. Kriteria yang
         bobotnya tidak konsisten antar-paruh diberi penalti → mengurangi
         chattering TANPA mematikan kriteria yang informatif.
      3. **Anchor ahli + guard rail**:
             m_j = γ w_j^ahli + (1−γ) · (w_j^obj ρ_j) / Σ_k (w_k^obj ρ_k)
             m_j di-clip ke [g_lo·w_j^ahli, g_hi·w_j^ahli] lalu dinormalisasi
         → mencegah kolaps ke 0 (kriteria konstan) atau dominasi satu kriteria.
      4. **Penghalusan + gerbang perubahan minimum**:
             w(t) = (1−β) w(t−1) + β m(t)
             bila max_j |w_j(t) − w_j(t−1)| < δ  →  pertahankan w(t−1)
         Gerbang δ inilah yang membuat bobot "histeresis", analog gerbang
         histeresis pada Q (A6) tetapi bekerja pada level bobot.

    Klaim yang aman: *bobot diperbarui dari data, tetapi laju perubahannya
    dibatasi oleh reliabilitas antar-paruh dan gerbang perubahan minimum.*
    Bukan pembelajaran otomatis (self-tuning).
    """
    p = ctx["params"]
    expert = ctx["expert"]
    obj_fn = ctx["obj_fn"]
    n = len(window)
    if n < 4:
        base = obj_fn(window)
    else:
        h = n // 2
        w_all = obj_fn(window)
        w_a = obj_fn(window[:h])
        w_b = obj_fn(window[h:])
        num = {}
        for c in CRITERIA:
            d = abs(w_a[c] - w_b[c]) / max(w_a[c] + w_b[c], 1e-9)
            reliability = 1.0 / (1.0 + p.lambda_stab * d)
            num[c] = w_all[c] * reliability
        base = _normalize_dict(num)

    mixed = {c: p.gamma * expert[c] + (1.0 - p.gamma) * base[c] for c in CRITERIA}
    guarded = {
        c: clip(mixed[c], p.guard_lo * expert[c], p.guard_hi * expert[c])
        for c in CRITERIA
    }
    target = _normalize_dict(guarded)

    prev = ctx.get("prev_w")
    if prev is None:
        return target
    smoothed = {c: (1.0 - p.beta_w) * prev[c] + p.beta_w * target[c] for c in CRITERIA}
    smoothed = _normalize_dict(smoothed)
    if max(abs(smoothed[c] - prev[c]) for c in CRITERIA) < p.delta_w:
        return dict(prev)
    return smoothed


OBJ_METHODS = ("entropy", "critic", "merec")


    "statis": weights_expert,
    "sama": weights_equal,
    "entropy": weights_entropy,
    "critic": weights_critic,
    "merec": weights_merec,
    "hibrida": weights_hybrid,
    "tw-saw": weights_temporal,   # BARU
}


# =============================================================================
# A5. SKOR SAW  [`01/05` §2]
# =============================================================================

def saw_score(norm: dict[str, float], weights: dict[str, float]) -> float:
    """Q_i(t) = 100 · Σ_j w_j · r_ij. Rentang 0–100."""
    return 100.0 * sum(weights[c] * norm.get(c, 0.0) for c in CRITERIA)


# =============================================================================
# A6. GERBANG HISTERESIS  [`01/05` §2(4), `01/13` §3]
# =============================================================================

@dataclass
class GateParams:
    mode: str = "asymmetric"       # none | symmetric | asymmetric
    theta_deg: float = 60.0        # θ_degradasi (skala 0–100)
    theta_rec: float = 80.0        # θ_pemulihan (> θ_deg → asimetri)
    k_down: int = 20               # dwell masuk degradasi (sampel)
    k_up: int = 60                 # dwell kembali baik (asimetris) / 20 (simetris)
    min_share_delta: float = 0.10  # deadband perubahan alokasi (10 poin persen)
    hold_s: float = 300.0          # perubahan harus bertahan ≥ 5 menit


class AllocationGate:
    """
    Gerbang perubahan aturan (arsip `06_Tahap_04/02` §4.3 — evaluasi ulang
    paksa): perubahan rasio hanya diterapkan bila (1) selisih pangsa target
    vs aktif > `min_share_delta` DAN (2) kondisi bertahan ≥ `hold_s`.

    Tanpa gerbang ini, target rasio berbasis Q yang bising akan menghasilkan
    perubahan bucket hampir tiap detik (rule churn), yang justru menjadi
    sumber flapping yang ingin ditekan.
    """

    def __init__(self, p: GateParams):
        self.p = p
        self.active: dict[str, float] | None = None
        self.pending: dict[str, float] | None = None
        self.pending_since: float | None = None

    def update(
        self,
        target: dict[str, float],
        state_code: str,
        t: float,
        bypass: bool = False,
    ) -> tuple[dict[str, float], bool]:
        """Kembalikan (alokasi aktif, apakah berubah)."""
        if self.active is None:
            self.active = dict(target)
            return dict(self.active), True

        # transisi status B↔T adalah peristiwa → langsung terapkan
        if bypass:
            changed = max(abs(target[k] - self.active[k]) for k in target) > 1e-9
            self.active = dict(target)
            self.pending, self.pending_since = None, None
            return dict(self.active), changed

        delta = max(abs(target[k] - self.active[k]) for k in target)
        if delta < self.p.min_share_delta:
            self.pending, self.pending_since = None, None
            return dict(self.active), False

        if self.pending is None or self.pending_since is None:
            self.pending, self.pending_since = dict(target), t
            return dict(self.active), False

        if t - self.pending_since >= self.p.hold_s:
            self.active = dict(target)
            self.pending, self.pending_since = None, None
            return dict(self.active), True
        return dict(self.active), False


class HysteresisGate:
    """
    Gerbang histeresis dua ambang + dwell, DIHITUNG PADA Q_i(t) (bukan metrik
    mentah) — menutup temuan M14. Satu instance per link.

    mode:
      - "none"      : keputusan instan (perlakuan B) → pembanding
      - "symmetric" : θ sama, k_up = k_down (perlakuan D)
      - "asymmetric": θ_rec > θ_deg, k_up > k_down (perlakuan F, usulan)
    """

    def __init__(self, p: GateParams):
        self.p = p
        self.state = STABLE
        self.down_count = 0
        self.up_count = 0
        self.episode_start: float | None = None
        self.recovery_times: list[float] = []
        self.transitions: list[dict] = []

    def _thresholds(self) -> tuple[float, float, int, int]:
        if self.p.mode == "symmetric":
            return self.p.theta_deg, self.p.theta_deg, self.p.k_down, self.p.k_down
        return self.p.theta_deg, self.p.theta_rec, self.p.k_down, self.p.k_up

    def update(self, q: float, t: float) -> str:
        if self.p.mode == "none":
            new = DEGRADED if q < self.p.theta_deg else STABLE
            if new != self.state:
                self._transition(t, new, q)
            return self.state

        theta_deg, theta_rec, k_down, k_up = self._thresholds()

        if self.state == STABLE:
            self.up_count = 0
            if q < theta_deg:
                self.down_count += 1
                if self.down_count >= k_down:
                    self.episode_start = t - (k_down - 1)
                    self._transition(t, DEGRADED, q)
                    self.down_count = 0
            else:
                self.down_count = 0
        else:
            self.down_count = 0
            if q > theta_rec:
                self.up_count += 1
                if self.up_count >= k_up:
                    if self.episode_start is not None:
                        self.recovery_times.append(t - self.episode_start)
                    self._transition(t, STABLE, q)
                    self.up_count = 0
            else:
                self.up_count = 0
        return self.state

    def _transition(self, t: float, new: str, q: float) -> None:
        self.transitions.append({"t": t, "from": self.state, "to": new, "q": q})
        self.state = new


# =============================================================================
# A7. STATE MACHINE TRI-LINK (8 STATE)  [`01/15` §8]
# =============================================================================

STATE_ACTIONS = {
    "S0": "semua sehat → rasio mengikuti target Q",
    "S1": "LEO-1 turun → alihkan dari ISP-A",
    "S2": "LEO-2 turun → alihkan dari ISP-B",
    "S3": "FO turun → alihkan dari ISP-C",
    "S4": "kedua LEO turun → prioritaskan FO",
    "S5": "LEO-1 + FO turun → prioritaskan LEO-2",
    "S6": "LEO-2 + FO turun → prioritaskan LEO-1",
    "S7": "semua turun → fail-static (tahan konfigurasi terakhir)",
}


def state_machine_3link(states: dict[str, str]) -> tuple[str, str]:
    """
    Peta status per link (B/T) ke kode S0–S7 + aksi.
    Urutan bit: A, B, C; B=0 (baik), T=1 (terdegradasi).
    """
    bits = "".join("1" if states.get(link) == DEGRADED else "0" for link in LINKS)
    code = f"S{int(bits, 2)}"
    return code, STATE_ACTIONS[code]


# =============================================================================
# A8. TARGET RASIO & HEADROOM  [arsip `06_Tahap_04/02` §5.1–5.2]
# =============================================================================

def headroom(utilization: float, eps: float = 1e-3) -> float:
    """H_i = max(ε, 1 − u_i). Bila utilisasi tak tersedia, H=1 (degraded mode)."""
    if utilization is None:
        return 1.0
    return max(eps, 1.0 - clip(utilization, 0.0, 1.0))


def target_ratio(q: dict[str, float], util: dict[str, float] | None = None,
                 use_headroom: bool = True) -> dict[str, float]:
    """T_i = Q_i·H_i / Σ_k Q_k·H_k (fallback ke Q_i saja bila H tidak dipakai)."""
    num = {}
    for link in LINKS:
        h = headroom(util.get(link)) if (use_headroom and util) else 1.0
        num[link] = max(q.get(link, 0.0), 0.0) * h
    if sum(num.values()) <= 1e-12:
        return {link: 1.0 / len(LINKS) for link in LINKS}
    return _normalize_dict(num)


# =============================================================================
# A10. ALOKASI SADAR-STOK (κ)  [arsip `03_Tahap_02/02` §1.9; `01/18` K-E]
# =============================================================================

def stock_flow_ratio(
    target: dict[str, float],
    stock: dict[str, float] | None,
    kappa: float,
    w_min: float = 0.15,
    w_max: float = 0.85,
) -> dict[str, float]:
    """
    W_i = clip(T_i + κ(T_i − S_i/ΣS), W_min, W_max), lalu renormalisasi
    dengan batas tetap (water-filling sederhana).

    κ=0 → alokasi kualitas saja (kondisi F). κ>0 → stok lama yang menumpuk
    di link buruk dikompensasi pada alokasi koneksi baru (kondisi H).
    """
    if not stock or sum(stock.values()) <= 0:
        return _clip_and_renormalize(dict(target), w_min, w_max)
    share = {link: stock.get(link, 0.0) / sum(stock.values()) for link in LINKS}
    raw = {
        link: target[link] + kappa * (target[link] - share[link])
        for link in LINKS
    }
    return _clip_and_renormalize(raw, w_min, w_max)


def _clip_and_renormalize(values: dict[str, float], lo: float, hi: float) -> dict[str, float]:
    """Clip tiap nilai ke [lo,hi] lalu distribusikan sisa agar Σ=1."""
    links = list(values)
    n = len(links)
    if lo * n > 1.0 or hi * n < 1.0:
        return {k: 1.0 / n for k in links}

    out = {k: clip(values[k], lo, hi) for k in links}
    for _ in range(10):
        diff = 1.0 - sum(out.values())
        if abs(diff) < 1e-9:
            break
        if diff > 0:
            free = [k for k in links if out[k] < hi - 1e-12]
            if not free:
                break
            share = diff / len(free)
            for k in free:
                out[k] = min(hi, out[k] + share)
        else:
            free = [k for k in links if out[k] > lo + 1e-12]
            if not free:
                break
            share = -diff / len(free)
            for k in free:
                out[k] = max(lo, out[k] - share)
    return _normalize_dict(out)


def apply_degradation_override(
    w: dict[str, float],
    states: dict[str, str],
    w_min: float = 0.15,
    w_max: float = 0.85,
) -> dict[str, float]:
    """
    Bila ada link TERDEGRADASI, batasi pangsa link tersebut ke W_min dan
    bagikan sisanya proporsional pada link sehat (generalisasi tabel
    arsip §5.4 untuk tiga link). Bila semua terdegradasi → fail-static.
    """
    degraded = [link for link in LINKS if states.get(link) == DEGRADED]
    if not degraded:
        return dict(w)
    if len(degraded) == len(LINKS):
        return dict(w)  # fail-static: tahan keputusan terakhir
    healthy = [link for link in LINKS if link not in degraded]
    for link in degraded:
        w[link] = min(w[link], w_min)
    remainder = 1.0 - sum(w[link] for link in degraded)
    base = sum(max(w[link], 1e-9) for link in healthy)
    for link in healthy:
        w[link] = remainder * max(w[link], 1e-9) / base
    return _clip_and_renormalize(w, w_min, w_max)


# =============================================================================
# A9. BUCKET MAPPING PCC  [`01/15` §9; arsip `02` §5.5]
# =============================================================================

def bucket_map(
    w: dict[str, float],
    n_bucket: int = 20,
    b_min: int = 2,
    b_max: int = 14,
) -> dict[str, int]:
    """
    Kontinu → bucket integer. Jaminan: Σ b_i = N dan b_min ≤ b_i ≤ b_max
    selama L·b_min ≤ N ≤ L·b_max; jika tidak layak → fallback merata.
    Sisa pembulatan dialokasikan dengan *largest remainder*.
    """
    links = sorted(w)
    L = len(links)
    if L == 0:
        return {}
    if n_bucket < b_min * L or n_bucket > b_max * L:
        base = n_bucket // L
        out = {link: base for link in links}
        for link in links[: n_bucket - base * L]:
            out[link] += 1
        return out

    raw = {link: n_bucket * max(w[link], 0.0) for link in links}
    frac = {link: raw[link] - math.floor(raw[link]) for link in links}
    b = {link: int(clip(math.floor(raw[link]), b_min, b_max)) for link in links}

    diff = n_bucket - sum(b.values())
    guard = 0
    while diff > 0 and guard < 1000:
        candidates = [k for k in links if b[k] < b_max]
        if not candidates:
            break
        pick = max(candidates, key=lambda k: (frac[k], raw[k]))
        b[pick] += 1
        frac[pick] -= 1.0
        diff -= 1
        guard += 1
    while diff < 0 and guard < 2000:
        candidates = [k for k in links if b[k] > b_min]
        if not candidates:
            break
        pick = min(candidates, key=lambda k: (frac[k], raw[k]))
        b[pick] -= 1
        frac[pick] += 1.0
        diff += 1
        guard += 1

    if sum(b.values()) != n_bucket:
        base = n_bucket // L
        b = {link: base for link in links}
        for link in links[: n_bucket - base * L]:
            b[link] += 1
    return b


# =============================================================================
# A11. METRIK EVALUASI
# =============================================================================

def effective_load_skew(load_share: dict[str, float], target: dict[str, float]) -> float:
    """ELS = ½ Σ_i |L_i − T_i|. 0 = alokasi persis sesuai target."""
    return 0.5 * sum(abs(load_share.get(link, 0.0) - target.get(link, 0.0)) for link in LINKS)


def siwg(goodput_mbps: float, rst_flow_rate: float, lam: float = 1.0) -> float:
    """SIWG = G_eff · (1 − λ·RST_flow) — alat pembanding internal, bukan standar."""
    return goodput_mbps * (1.0 - lam * clip(rst_flow_rate, 0.0, 1.0))


def flap_count(changes: Sequence[dict], window_s: float = 300.0) -> int:
    """
    Definisi operasional flap (arsip §1.3, M12): perubahan aturan efektif
    (jumlah bucket satu link berubah) yang diikuti perubahan ARAH sebaliknya
    dalam jendela W. Satu pembalikan arah = satu flap.

    `changes` = [{"t": float, "buckets": {link: int}, "prev_buckets": {...}}, ...]
    """
    flaps = 0
    last_delta: dict[str, tuple[float, int]] = {}
    for change in changes:
        t, buckets = change["t"], change["buckets"]
        prev = change.get("prev_buckets", {})
        reversed_any = False
        for link, b in buckets.items():
            if link not in prev:
                continue
            delta = b - prev[link]
            if delta == 0:
                continue
            earlier = last_delta.get(link)
            if earlier and t - earlier[0] <= window_s and delta * earlier[1] < 0:
                reversed_any = True
            last_delta[link] = (t, delta)
        if reversed_any:
            flaps += 1
    return flaps


def chattering_rate(q_series: Sequence[float], threshold: float = 5.0, duration_s: float | None = None) -> float:
    """Proporsi langkah waktu dengan |ΔQ| > threshold (mis. 5 poin)."""
    if len(q_series) < 2:
        return 0.0
    jumps = sum(1 for a, b in zip(q_series, q_series[1:]) if abs(b - a) > threshold)
    rate = jumps / (len(q_series) - 1)
    return rate


def top1_switch_rate(q_by_time: Sequence[dict[str, float]]) -> float:
    """Proporsi langkah waktu di mana link ber-Q tertinggi berganti."""
    if len(q_by_time) < 2:
        return 0.0
    tops = [max(q, key=q.get) for q in q_by_time]
    switches = sum(1 for a, b in zip(tops, tops[1:]) if a != b)
    return switches / len(tops[1:])


def weight_volatility(w_by_time: Sequence[dict[str, float]]) -> float:
    """Rata-rata L1 |Δw| antar siklus (0 = bobot tidak pernah berubah)."""
    if len(w_by_time) < 2:
        return 0.0
    vals = []
    for a, b in zip(w_by_time, w_by_time[1:]):
        vals.append(0.5 * sum(abs(a[c] - b[c]) for c in CRITERIA))
    return mean(vals) or 0.0


def rank_reversal_rate(
    norm_by_time: Sequence[dict[str, dict[str, float]]],
    w_by_time: Sequence[dict[str, float]],
    perturb: float = 0.20,
    max_samples: int = 500,
) -> float:
    """
    Rank reversal (metode Vafaei): ganggu tiap bobot ±perturb (20%), hitung
    Q ulang, lalu hitung proporsi pasangan link yang peringkatnya terbalik.
    """
    if not norm_by_time:
        return 0.0
    step = max(1, len(norm_by_time) // max_samples)
    pairs = [(LINKS[i], LINKS[j]) for i in range(len(LINKS)) for j in range(i + 1, len(LINKS))]
    flips = trials = 0
    for idx in range(0, len(norm_by_time), step):
        norm, w = norm_by_time[idx], w_by_time[idx]
        base_q = {link: sum(w[c] * norm[link].get(c, 0.0) for c in CRITERIA) for link in LINKS}
        for crit in CRITERIA:
            for sign in (+1.0, -1.0):
                w2 = dict(w)
                w2[crit] = max(1e-9, w2[crit] * (1.0 + sign * perturb))
                w2 = _normalize_dict(w2)
                q2 = {link: sum(w2[c] * norm[link].get(c, 0.0) for c in CRITERIA) for link in LINKS}
                for a, b in pairs:
                    d0 = base_q[a] - base_q[b]
                    d1 = q2[a] - q2[b]
                    if d0 != 0 and d1 != 0 and (d0 > 0) != (d1 > 0):
                        flips += 1
                    trials += 1
    return flips / trials if trials else 0.0


def label_episodes(rtt: float, loss: float, success: bool = True,
                   rtt_threshold: float = 100.0, loss_threshold: float = 1.0) -> int:
    """A12. Label episode degenerasi sederhana (sama dengan analyze_baseline)."""
    return int((not success) or loss > loss_threshold or rtt > rtt_threshold)


def episode_boundaries(bad: Sequence[int]) -> list[tuple[int, int]]:
    """Indeks awal–akhir setiap episode 'buruk' (inklusif)."""
    out, start = [], None
    for i, v in enumerate(bad):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(bad) - 1))
    return out


def time_to_rebalance(els_series: Sequence[float], times: Sequence[float],
                      eps: float = 0.05, hold_s: float = 5.0) -> list[float]:
    """
    TTR umum: dari setiap awal episode ELS > eps sampai ELS ≤ eps dan bertahan
    `hold_s` detik. Mengembalikan daftar TTR per episode.
    """
    out, start, hold_start = [], None, None
    for els, t in zip(els_series, times):
        if start is None:
            if els > eps:
                start = t
        else:
            if els <= eps:
                if hold_start is None:
                    hold_start = t
                elif t - hold_start >= hold_s:
                    out.append(hold_start - start)
                    start, hold_start = None, None
            else:
                hold_start = None
    if start is not None:
        out.append(times[-1] - start)
    return out


def time_to_rebalance_events(
    els_series: Sequence[float],
    times: Sequence[float],
    events: Sequence[float],
    eps: float = 0.05,
    hold_s: float = 5.0,
    max_wait_s: float = 1800.0,
) -> list[float]:
    """
    TTR per peristiwa degradasi (transisi B→T dari gerbang histeresis).
    Lebih tepat daripada TTR dari setiap persilangan ELS: ELS bisa > eps sejak
    awal karena stok belum seimbang, bukan karena degradasi baru.
    """
    out = []
    for t0 in events:
        after = [(t, e) for t, e in zip(times, els_series) if t >= t0]
        hold_start = None
        done = False
        for t, e in after:
            if t - t0 > max_wait_s:
                break
            if e <= eps:
                if hold_start is None:
                    hold_start = t
                elif t - hold_start >= hold_s:
                    out.append(hold_start - t0)
                    done = True
                    break
            else:
                hold_start = None
        if not done and after and after[-1][0] - t0 <= max_wait_s:
            out.append(after[-1][0] - t0)
    return out


# =============================================================================
# A13. PERIODISITAS: ACF, FFT, KORELASI, JACCARD
# =============================================================================

def moving_average(values: Sequence[float], window: int = 61) -> list[float]:
    if not values:
        return []
    half = window // 2
    out = []
    for i in range(len(values)):
        lo, hi = max(0, i - half), min(len(values), i + half + 1)
        out.append(sum(values[lo:hi]) / (hi - lo))
    return out


def acf(values: Sequence[float], lag: int) -> float | None:
    """Autokorelasi pada lag tertentu (asumsi rata-rata dihilangkan)."""
    x = list(values)
    n = len(x)
    if n <= lag + 2:
        return None
    m = sum(x) / n
    denom = sum((v - m) ** 2 for v in x)
    if denom <= 0:
        return None
    num = sum((x[i] - m) * (x[i + lag] - m) for i in range(n - lag))
    return num / denom


def dominant_period(values: Sequence[float], min_period: float = 5.0,
                    max_period: float = 30.0, step: float = 0.5) -> tuple[float | None, float | None]:
    """
    Periode dominan via DFT (Goertzel) pada rentang 5–30 s.
    Mengembalikan (periode, rasio puncak terhadap median amplitudo).
    """
    x = list(values)
    n = len(x)
    if n < 120:
        return None, None
    m = sum(x) / n
    x = [v - m for v in x]
    best_p, best_amp, amps = None, -1.0, []
    p = min_period
    while p <= max_period:
        w = 2.0 * math.pi / p
        re = sum(v * math.cos(w * i) for i, v in enumerate(x))
        im = sum(v * math.sin(w * i) for i, v in enumerate(x))
        amp = math.hypot(re, im) / n
        amps.append(amp)
        if amp > best_amp:
            best_amp, best_p = amp, p
        p += step
    med = statistics.median(amps) if amps else 0.0
    ratio = best_amp / med if med > 1e-12 else None
    return best_p, ratio


def jaccard(a: Sequence[int], b: Sequence[int]) -> float | None:
    union = sum(1 for x, y in zip(a, b) if x or y)
    if union == 0:
        return None
    return sum(1 for x, y in zip(a, b) if x and y) / union


def episode_match(a_starts: Sequence[int], b_starts: Sequence[int], tolerance: int = 2) -> float | None:
    """Proporsi episode A yang punya pasangan episode B dalam ±tolerance detik."""
    if not a_starts or not b_starts:
        return None
    hits = sum(1 for x in a_starts if min(abs(x - y) for y in b_starts) <= tolerance)
    return hits / len(a_starts)


def independence_report(
    series_a: Sequence[float],
    series_b: Sequence[float],
    bad_a: Sequence[int] | None = None,
    bad_b: Sequence[int] | None = None,
    lag: int = 15,
) -> dict:
    """
    Ringkasan uji independensi antar-link: korelasi residual (setelah tren
    dihilangkan), ACF lag 15, Jaccard episode buruk, dan episode match.
    """
    n = min(len(series_a), len(series_b))
    if n < 60:
        return {"n": n, "residual_r": None, "raw_r": None}
    a = list(series_a[-n:])
    b = list(series_b[-n:])
    base_a = moving_average(a)
    base_b = moving_average(b)
    res_a = [x - y for x, y in zip(a, base_a)]
    res_b = [x - y for x, y in zip(b, base_b)]
    sa = [i for i, v in enumerate(bad_a) if v and i == 0 or (v and not bad_a[i - 1])] if bad_a else []
    sb = [i for i, v in enumerate(bad_b) if v and i == 0 or (v and not bad_b[i - 1])] if bad_b else []
    return {
        "n": n,
        "raw_r": pearson(a, b),
        "residual_r": pearson(res_a, res_b),
        "acf15_a": acf(res_a, lag),
        "acf15_b": acf(res_b, lag),
        "bad_jaccard": jaccard(bad_a or [], bad_b or []) if bad_a and bad_b else None,
        "episode_match": episode_match(sa, sb) if sa and sb else None,
    }


# =============================================================================
# PARAMETER
# =============================================================================

@dataclass
class Params:
    # waktu
    Ts: float = 1.0
    alpha: float = 0.20                 # EWMA
    # bobot
    window: int = 40                    # jendela update bobot N (sampel)
    gamma: float = 0.5                  # anchor ahli pada hibrida / TW-SAW
    obj_method: str = "entropy"         # entropy | critic | merec
    # TW-SAW [USULAN]
    beta_w: float = 0.30                # laju penghalusan bobot
    delta_w: float = 0.01               # gerbang perubahan minimum (L∞)
    lambda_stab: float = 2.0            # penalti reliabilitas belah-dua
    guard_lo: float = 0.50              # batas bawah relatif terhadap w_ahli
    guard_hi: float = 1.50              # batas atas relatif terhadap w_ahli
    # gerbang
    gate: GateParams = field(default_factory=GateParams)
    # alokasi
    use_headroom: bool = True
    kappa: float = 0.5                  # gain koreksi stok
    w_min: float = 0.15
    w_max: float = 0.85
    n_bucket: int = 20
    b_min: int = 2
    b_max: int = 14
    # evaluasi
    flap_window_s: float = 300.0
    chatter_threshold: float = 5.0
    siwg_lambda: float = 1.0
    capacity: dict[str, float] = field(
        default_factory=lambda: {LINK_A: 100.0, LINK_B: 90.0, LINK_C: 90.0}
    )
    expert_w: dict[str, float] = field(default_factory=lambda: dict(EXPERT_W))


# =============================================================================
# PIPELINE END-TO-END:  metrik → EWMA → normalisasi → bobot → Q → gerbang →
#                       state machine → target → stok → bucket
# =============================================================================

@dataclass
class RunResult:
    rows: list[dict] = field(default_factory=list)
    q_by_time: list[dict[str, float]] = field(default_factory=list)
    w_by_time: list[dict[str, float]] = field(default_factory=list)
    norm_by_time: list[dict[str, dict[str, float]]] = field(default_factory=list)
    summary: dict = field(default_factory=dict)


def run_pipeline(
    dataset: Sequence[dict],
    params: Params | None = None,
    normalizer: str = DEFAULT_NORMALIZER,
    weighter: str = "tw-saw",
    gate_mode: str | None = None,
) -> RunResult:
    """
    Jalankan satu konfigurasi (normalisasi × pembobotan × gerbang) penuh.

    `dataset` = [{"t": float, "links": {link: {delay,jitter,loss,thr,util}},
                  "stock": {link: float} (opsional),
                  "gt": {link: float} (opsional, ground truth 0–1)}]
    """
    p = params or Params()
    if gate_mode:
        p = replace(p, gate=replace(p.gate, mode=gate_mode))

    ctx_base = {
        "params": p,
        "expert": p.expert_w,
        "obj_fn": WEIGHTERS[p.obj_method] if p.obj_method in WEIGHTERS else weights_entropy,
    }
    weighter_fn = WEIGHTERS[weighter]

    smooth: dict[str, dict[str, float]] = {link: {} for link in LINKS}
    gates = {link: HysteresisGate(p.gate) for link in LINKS}
    alloc_gate = AllocationGate(p.gate)
    window: deque[dict[str, dict[str, float]]] = deque(maxlen=max(4, p.window))
    prev_w: dict[str, float] | None = None

    stock = {link: 1000.0 for link in LINKS}
    bucket_prev: dict[str, int] | None = None
    prev_states: dict[str, str] = {}
    cap_seen = None
    changes: list[dict] = []
    rows: list[dict] = []
    q_by_time, w_by_time, norm_by_time = [], [], []
    els_series, times = [], []
    gt_flat, q_flat, labels, bad_scores = [], [], [], []
    q_series_per_link: dict[str, list[float]] = {link: [] for link in LINKS}
    rst_proxy = 0.0   # hanya terukur di staging; di sini 0 (offline, no capture)

    for snap in dataset:
        t = snap["t"]
        links_data = snap.get("links", {})
        if not all(link in links_data for link in LINKS):
            continue

        # --- A2: EWMA per metrik per link
        for link in LINKS:
            for crit in CRITERIA:
                x = links_data[link].get(crit)
                if x is None:
                    continue
                smooth[link][crit] = ewma_value(smooth[link].get(crit), x, p.alpha)
        if any(c not in smooth[link] for link in LINKS for c in CRITERIA):
            continue

        # --- A3: normalisasi
        norm = normalize_row(smooth, LINKS, normalizer)

        # --- A4: bobot (jendela geser)
        window.append(norm)
        if len(window) < 2:
            weights = dict(p.expert_w)
        else:
            ctx = dict(ctx_base, prev_w=prev_w)
            weights = weighter_fn(list(window), prev_w, ctx)
        weights = _normalize_dict(weights)
        prev_w = weights

        # --- A5: skor SAW
        q = {link: saw_score(norm[link], weights) for link in LINKS}

        # --- A6: gerbang histeresis per link
        states = {link: gates[link].update(q[link], t) for link in LINKS}

        # --- A7: state machine tri-link
        code, action = state_machine_3link(states)

        # --- A8–A10: target rasio → koreksi stok → override degradasi
        util = {link: links_data[link].get("util") for link in LINKS}
        target = target_ratio(q, util, p.use_headroom)
        if "stock" in snap:
            stock = {link: snap["stock"].get(link, stock[link]) for link in LINKS}
        w_raw = stock_flow_ratio(target, stock, p.kappa, p.w_min, p.w_max)
        w_raw = apply_degradation_override(w_raw, states, p.w_min, p.w_max)

        # --- gerbang perubahan aturan (deadband + hold).
        # Perubahan status (transisi B↔T) adalah peristiwa → diterapkan segera;
        # perubahan halus akibat derau Q harus melewati deadband + hold.
        transitioned = bool(prev_states) and any(
            states[link] != prev_states[link] for link in LINKS
        )
        w, alloc_changed = alloc_gate.update(w_raw, code, t, bypass=transitioned)
        prev_states = dict(states)

        # --- A9: bucket
        buckets = bucket_map(w, p.n_bucket, p.b_min, p.b_max)
        if bucket_prev is not None and buckets != bucket_prev:
            changes.append({"t": t, "buckets": buckets, "prev_buckets": dict(bucket_prev)})
        bucket_prev = buckets

        # --- stok simulasi (bila dataset tidak menyediakannya)
        if "stock" not in snap:
            new_rate = 120.0
            churn = 0.005
            for link in LINKS:
                stock[link] = stock[link] * (1.0 - churn) + new_rate * w[link]

        # --- ELS
        load_share = _normalize_dict({link: stock[link] for link in LINKS})
        els = effective_load_skew(load_share, target)

        row = {
            "t": t,
            "q": q,
            "w": weights,
            "state": dict(states),
            "state_code": code,
            "target": target,
            "alloc": w,
            "buckets": buckets,
            "els": els,
        }
        if "gt" in snap:
            row["gt"] = snap["gt"]
            gt_flat.extend(snap["gt"][link] for link in LINKS)
            q_flat.extend(q[link] for link in LINKS)
        if "capacity" in snap:
            cap_seen = snap["capacity"]
        # AUC per link: label buruk dari metrik mentah link itu vs Q link itu
        for link in LINKS:
            labels.append(label_episodes(
                links_data[link]["delay"], links_data[link]["loss"]
            ))
            bad_scores.append(100.0 - q[link])

        rows.append(row)
        q_by_time.append(q)
        w_by_time.append(weights)
        norm_by_time.append(norm)
        els_series.append(els)
        times.append(t)
        for link in LINKS:
            q_series_per_link[link].append(q[link])

    # --- ringkasan metrik
    duration_s = (times[-1] - times[0] + p.Ts) if len(times) > 1 else 0.0
    hours = duration_s / 3600.0 if duration_s else 0.0
    flaps = flap_count(changes, p.flap_window_s)
    degrade_events = [
        tr["t"] for tr in (g.transitions for g in gates.values()) for tr in tr
        if tr["to"] == DEGRADED
    ]
    ttr = time_to_rebalance_events(els_series, times, sorted(degrade_events)) if times else []
    recovery = [x for g in gates.values() for x in g.recovery_times]
    episodes_detected = sum(
        sum(1 for tr in g.transitions if tr["to"] == DEGRADED) for g in gates.values()
    )

    chatters = [
        chattering_rate(q_series_per_link[link], p.chatter_threshold) for link in LINKS
    ]
    summary = {
        "normalizer": normalizer,
        "weighter": weighter,
        "obj_method": p.obj_method,
        "gate_mode": p.gate.mode,
        "n_samples": len(times),
        "duration_h": round(hours, 4),
        "capacity_eff_mbps": cap_seen or None,
        "q_mean": {link: round(mean(q_series_per_link[link]) or 0.0, 2) for link in LINKS},
        "q_std": {link: round(stdev(q_series_per_link[link]), 2) for link in LINKS},
        "chattering_rate": round(mean(chatters) or 0.0, 4),
        "top1_switch_rate": round(top1_switch_rate(q_by_time), 4),
        "weight_volatility": round(weight_volatility(w_by_time), 4),
        "rank_reversal_rate": round(rank_reversal_rate(norm_by_time, w_by_time), 4),
        "rule_changes": len(changes),
        "flaps": flaps,
        "flaps_per_hour": round(flaps / hours, 2) if hours else None,
        "recovery_median_s": round(percentile(recovery, 0.50), 2) if recovery else None,
        "episodes_detected": episodes_detected,
        "els_mean": round(mean(els_series) or 0.0, 4),
        "ttr_median_s": round(percentile(ttr, 0.50), 2) if ttr else None,
        "auc": _round_or_none(auc_score(labels, bad_scores), 4),
        "spearman_gt": _round_or_none(spearman(q_flat, gt_flat), 4),
        # RST & goodput tidak dapat diukur offline (butuh capture/sintesis lalu
        # lintas). Dibiarkan None secara eksplisit agar tidak dilaporkan
        # sebagai hasil (prinsip "tidak ada imputasi untuk outcome primer").
        "rst_flow_rate": None,
        "siwg": None,
        "weights_final": {c: round(prev_w[c], 4) for c in CRITERIA} if prev_w else None,
    }
    return RunResult(rows=rows, q_by_time=q_by_time, w_by_time=w_by_time,
                     norm_by_time=norm_by_time, summary=summary)


# =============================================================================
# A14. ABLASI: normalisasi × pembobotan  [P1, K-A, K-D]
# =============================================================================

def ablation(
    dataset: Sequence[dict],
    norm_methods: Sequence[str] = ("n-a", "n-b", "n-c"),
    weighters: Sequence[str] = ("statis", "sama", "entropy", "critic", "merec", "hibrida", "tw-saw"),
    params: Params | None = None,
    gate_mode: str | None = None,
) -> list[dict]:
    """Jalankan grid penuh dan kembalikan satu baris ringkasan per konfigurasi."""
    rows = []
    for norm in norm_methods:
        for wt in weighters:
            res = run_pipeline(dataset, params=params, normalizer=norm,
                               weighter=wt, gate_mode=gate_mode)
            rows.append(res.summary)
    return rows


# =============================================================================
# GENERATOR DATA SINTETIS (kondisi N/T/S/R/K)  [`01/08` §4b]
# =============================================================================

def synthetic_dataset(
    seconds: int = 1800,
    condition: str = "N",
    seed: int = 7,
    total_conn: int = 16000,
    new_conn_per_s: float = 120.0,
) -> list[dict]:
    """
    Bangkitkan dataset 3 link dengan nilai LATEN (gt) dan nilai TERUKUR
    (delay/jitter/loss/thr) yang bising.

    condition:
      N = normal; T = transien LEO 15 s (pola 4 s tiap 15 s);
      S = degradasi FO bertahap; R = rain fade (dua LEO); K = T + S.
    """
    rng = random.Random(seed)
    base = {
        LINK_A: {"delay": 48.0, "jitter": 6.0, "loss": 0.30, "thr": 70.0, "cap": 100.0},
        LINK_B: {"delay": 50.0, "jitter": 6.5, "loss": 0.35, "thr": 65.0, "cap": 90.0},
        LINK_C: {"delay": 46.0, "jitter": 0.35, "loss": 0.05, "thr": 60.0, "cap": 90.0},
    }
    # bobot "kebenaran" sengaja BEDA dari w_ahli agar tidak bias ke statis
    w_true = {"delay": 0.25, "jitter": 0.15, "loss": 0.30, "thr": 0.30}

    stock = {link: total_conn / 3 for link in LINKS}
    out = []
    for i in range(seconds):
        latent = {link: dict(base[link]) for link in LINKS}

        # --- pola degradasi pada nilai laten
        if condition in ("T", "K"):
            if i % 15 < 4:
                for link in (LINK_A, LINK_B):
                    latent[link]["delay"] += 55.0
                    latent[link]["jitter"] += 14.0
                    latent[link]["loss"] += 2.5
                    latent[link]["thr"] *= 0.45
        if condition in ("S", "K") and 300 <= i < 1200:
            ramp = min(1.0, (i - 300) / 600.0)
            latent[LINK_C]["delay"] += 110.0 * ramp
            latent[LINK_C]["jitter"] += 1.5 * ramp
            latent[LINK_C]["loss"] += 2.0 * ramp
            latent[LINK_C]["thr"] *= (1.0 - 0.70 * ramp)
        if condition == "R" and 200 <= i < 900:
            for link in (LINK_A, LINK_B):
                latent[link]["thr"] *= 0.65
                latent[link]["loss"] += 1.2

        # --- ground truth utility dari nilai laten (N-c)
        gt = {}
        for link in LINKS:
            r = {}
            for crit in CRITERIA:
                meta = CRIT_META[crit]
                lo, hi = meta["ref"]
                v = latent[link][crit]
                r[crit] = clip((hi - v) / (hi - lo), 0.0, 1.0) if meta["dir"] == "cost" \
                    else clip((v - lo) / (hi - lo), 0.0, 1.0)
            gt[link] = sum(w_true[c] * r[c] for c in CRITERIA)

        # --- nilai terukur = laten + derau (derau LEO lebih besar)
        links = {}
        for link in LINKS:
            sigma = 3.0 if link != LINK_C else 0.5
            delay = max(1.0, latent[link]["delay"] + rng.gauss(0, sigma))
            jitter = max(0.01, latent[link]["jitter"] * (1 + rng.gauss(0, 0.15)))
            loss = max(0.0, latent[link]["loss"] + rng.gauss(0, 0.06 if link != LINK_C else 0.01))
            thr = max(0.0, latent[link]["thr"] + rng.gauss(0, 4.0))
            links[link] = {
                "delay": round(delay, 3),
                "jitter": round(jitter, 3),
                "loss": round(loss, 3),
                "thr": round(thr, 3),
                "util": clip(thr / base[link]["cap"], 0.0, 1.0),
            }
        out.append({"t": float(i), "links": links, "gt": gt,
                    "stock": dict(stock)})

        # --- dinamika stok sederhana (agar ELS/TTR bermakna)
        alloc = _normalize_dict({link: max(gt[link], 0.05) for link in LINKS})
        for link in LINKS:
            stock[link] = stock[link] * 0.995 + new_conn_per_s * alloc[link]
    return out


# =============================================================================
# SELFTEST: golden test dari dokumen repo
# =============================================================================

def selftest() -> list[str]:
    """
    Uji golden yang HARUS lulus (angka diambil dari dokumen repo):
      1. `01/05` §1: N-a, w=0.30/0.25/0.25/0.20 → FO 91.3 ; LEO 53.3
      2. arsip `06_Tahap_04/02` §6: N-c, w=0.35/0.30/0.15/0.20 → FO 0.935 ; LEO 0.665
      3. Σ bucket = N dan b_min ≤ b_i ≤ b_max
      4. Σ w = 1 untuk semua pembobot
      5. State machine: 8 kombinasi → S0…S7
      6. Histeresis: transien pendek tidak memicu degradasi
    """
    logs = []

    def check(name: str, got, want, tol=1e-3):
        ok = abs(got - want) <= tol
        logs.append(f"{'PASS' if ok else 'FAIL'}  {name}: got={got:.4f} want={want:.4f}")
        return ok

    # 1. Golden N-a (naskah lama)
    fo = {"delay": 25.0, "jitter": 3.0, "loss": 0.5, "thr": 45.0}
    leo = {"delay": 45.0, "jitter": 12.0, "loss": 1.2, "thr": 80.0}
    norm = normalize_row({LINK_C: fo, LINK_A: leo}, [LINK_C, LINK_A], "n-a")
    q_fo = saw_score(norm[LINK_C], EXPERT_W)
    q_leo = saw_score(norm[LINK_A], EXPERT_W)
    check("golden N-a FO", q_fo, 91.25, 0.05)
    check("golden N-a LEO", q_leo, 53.33, 0.05)
    logs.append(f"      Q_FO={q_fo:.2f} (dokumen 91,3) ; Q_LEO={q_leo:.2f} (dokumen 53,3)")

    # 2. Golden N-c (arsip formalisasi §6)
    fo2 = {"thr": 90.0, "delay": 10.0, "jitter": 2.0, "loss": 0.0}
    leo2 = {"thr": 50.0, "delay": 40.0, "jitter": 8.0, "loss": 1.0}
    norm2 = normalize_row({LINK_C: fo2, LINK_A: leo2}, [LINK_C, LINK_A], "n-c")
    check("golden N-c FO", saw_score(norm2[LINK_C], ARCHIVE_W), 93.5, 0.05)
    check("golden N-c LEO", saw_score(norm2[LINK_A], ARCHIVE_W), 66.5, 0.05)

    # 3. Bucket mapping
    b = bucket_map({LINK_A: 0.70, LINK_B: 0.20, LINK_C: 0.10}, 20, 2, 14)
    logs.append(f"{'PASS' if sum(b.values()) == 20 else 'FAIL'}  bucket Σ=N: {b} (Σ={sum(b.values())})")
    logs.append(f"{'PASS' if all(2 <= v <= 14 for v in b.values()) else 'FAIL'}  bucket batas 2..14")

    # 4. Normalisasi bobot (deterministik: seed tetap)
    rnd = random.Random(1234)
    window = [{link: {c: rnd.uniform(0.1, 0.9) for c in CRITERIA} for link in LINKS}
              for _ in range(30)]
    for name, fn in WEIGHTERS.items():
        ctx = {"params": Params(), "expert": EXPERT_W, "obj_fn": weights_entropy, "prev_w": None}
        w = _normalize_dict(fn(window, None, ctx))
        s = sum(w.values())
        logs.append(f"{'PASS' if abs(s - 1) < 1e-6 else 'FAIL'}  bobot {name}: Σ={s:.6f} {({k: round(v,3) for k,v in w.items()})}")

    # 5. State machine lengkap
    seen = []
    for i in range(8):
        st = {link: (DEGRADED if (i >> (2 - k)) & 1 else STABLE) for k, link in enumerate(LINKS)}
        code, _ = state_machine_3link(st)
        seen.append(code)
    logs.append(f"{'PASS' if seen == [f'S{i}' for i in range(8)] else 'FAIL'}  state machine: {seen}")

    # 6. Histeresis menahan transien 4 detik
    gate = HysteresisGate(GateParams(mode="asymmetric"))
    for i in range(100):
        q = 40.0 if 40 <= i < 44 else 90.0
        gate.update(q, float(i))
    trans = [x for x in gate.transitions if x["to"] == DEGRADED]
    logs.append(f"{'PASS' if not trans else 'FAIL'}  histeresis menahan transien 4 s (transisi={len(trans)})")

    # 7. Gerbang asimetris bereaksi pada degradasi sustained
    gate2 = HysteresisGate(GateParams(mode="asymmetric"))
    for i in range(200):
        gate2.update(40.0 if i >= 20 else 90.0, float(i))
    ok = any(x["to"] == DEGRADED for x in gate2.transitions)
    logs.append(f"{'PASS' if ok else 'FAIL'}  histeresis mendeteksi degradasi sustained")

    return logs


def rng_uniform(a: float, b: float) -> float:
    """Helper kecil (tidak dipakai di selftest utama; disisakan untuk eksperimen)."""
    return random.Random(hash((a, b, random.random())) & 0xFFFF).uniform(a, b)


# =============================================================================
# CLI
# =============================================================================

def _print_table(rows: Sequence[dict], columns: Sequence[str]) -> str:
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in columns}
    head = " | ".join(c.ljust(widths[c]) for c in columns)
    sep = "-+-".join("-" * widths[c] for c in columns)
    body = [" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in columns) for r in rows]
    return "\n".join([head, sep] + body)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Algoritma terpadu ALQI–SAW + TW-SAW")
    ap.add_argument("mode", choices=["selftest", "demo", "ablation", "replay"],
                    nargs="?", default="selftest")
    ap.add_argument("--seconds", type=float, default=1800.0)
    ap.add_argument("--condition", default="N", choices=list("NTSRK"))
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--glob", default="baseline_rb1100ahx4_2026111*.jsonl")
    ap.add_argument("--normalizer", default=DEFAULT_NORMALIZER, choices=list(NORMALIZERS))
    ap.add_argument("--weighter", default="tw-saw", choices=list(WEIGHTERS))
    ap.add_argument("--gate", default="asymmetric", choices=["none", "symmetric", "asymmetric"])
    ap.add_argument("--obj", default="entropy", choices=list(OBJ_METHODS),
                    help="pembobot objektif dasar untuk hibrida/tw-saw")
    ap.add_argument("--ablation", action="store_true", help="untuk mode replay")
    ap.add_argument("--json", action="store_true", help="cetak ringkasan JSON")
    args = ap.parse_args(argv)

    if args.mode == "selftest":
        logs = selftest()
        print("\n".join(logs))
        return 0 if all(l.startswith("PASS") or l.startswith("      ") for l in logs) else 1

    if args.mode == "demo":
        data = synthetic_dataset(int(args.seconds), args.condition, args.seed)
        res = run_pipeline(data, params=Params(obj_method=args.obj),
                           normalizer=args.normalizer, weighter=args.weighter,
                           gate_mode=args.gate)
        if args.json:
            print(json.dumps(res.summary, indent=2, ensure_ascii=False))
        else:
            print(f"# Demo sintetis — kondisi {args.condition}, {len(data)} detik")
            print(json.dumps(res.summary, indent=2, ensure_ascii=False))
        return 0

    if args.mode == "ablation":
        grid = []
        for cond in ("N", "T", "S", "R", "K"):
            data = synthetic_dataset(int(args.seconds), cond, args.seed)
            base_params = Params(obj_method=args.obj)
            for row in ablation(data, params=base_params, gate_mode=args.gate):
                row["condition"] = cond
                grid.append(row)
        cols = ["condition", "normalizer", "weighter", "q_mean", "q_std", "chattering_rate",
                "top1_switch_rate", "weight_volatility", "rank_reversal_rate",
                "flaps_per_hour", "els_mean", "auc", "spearman_gt"]
        compact = []
        for r in grid:
            compact.append({
                "condition": r["condition"], "normalizer": r["normalizer"],
                "weighter": r["weighter"],
                "q_mean": round(mean(list(r["q_mean"].values())) or 0, 2),
                "q_std": round(mean(list(r["q_std"].values())) or 0, 2),
                "chattering_rate": r["chattering_rate"],
                "top1_switch_rate": r["top1_switch_rate"],
                "weight_volatility": r["weight_volatility"],
                "rank_reversal_rate": r["rank_reversal_rate"],
                "flaps_per_hour": r["flaps_per_hour"],
                "els_mean": r["els_mean"], "auc": r["auc"],
                "spearman_gt": r["spearman_gt"],
            })
        print(_print_table(compact, cols))
        return 0

    # --- replay
    base = Path(args.data_dir) if args.data_dir else (
        Path(__file__).resolve().parents[1]
        / "01_Arsip_SPA-HSM_Tahap_01-12" / "11_Kolektor_Baseline" / "data"
    )
    paths = sorted(base.glob(args.glob))
    if not paths:
        print(f"[ERROR] Tidak ada berkas JSONL di {base}")
        return 2
    data = build_replay_dataset(paths, duration_s=args.seconds)
    if not data:
        print("[ERROR] Dataset replay kosong (cek format JSONL)")
        return 2
    if args.ablation:
        rows = ablation(data, params=Params(obj_method=args.obj), gate_mode=args.gate)
        compact = [{
            "normalizer": r["normalizer"], "weighter": r["weighter"],
            "q_std_mean": round(mean(list(r["q_std"].values())) or 0, 2),
            "chattering_rate": r["chattering_rate"],
            "top1_switch_rate": r["top1_switch_rate"],
            "weight_volatility": r["weight_volatility"],
            "rank_reversal_rate": r["rank_reversal_rate"],
            "flaps_per_hour": r["flaps_per_hour"],
            "els_mean": r["els_mean"], "auc": r["auc"],
        } for r in rows]
        print(_print_table(compact, list(compact[0])))
    else:
        res = run_pipeline(data, params=Params(obj_method=args.obj),
                           normalizer=args.normalizer, weighter=args.weighter,
                           gate_mode=args.gate)
        print(json.dumps(res.summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
