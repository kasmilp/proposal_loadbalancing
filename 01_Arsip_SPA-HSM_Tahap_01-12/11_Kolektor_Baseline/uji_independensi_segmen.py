#!/usr/bin/env python3
"""
Uji independensi A–B per SEGMEN KONTINU (data asli, tanpa interpolasi lintas celah).

Latar: file baseline 13–18 Nov tidak kontinu (data asli hanya 12, 17, 18 Nov UTC).
Skrip sebelumnya memakai grid 1 detik penuh → tercemar interpolasi pada hari kosong.
Skrip ini:
1. load semua probe asli
2. pecah ke segmen kontinu (gap > 300 s = batas segmen baru)
3. resample per segmen (1 s, hanya dalam segmen)
4. hitung per segmen: korelasi residual & mentah A–B, Jaccard, episode match
5. keluarkan laporan per segmen + agregat

[konvensi hasil: FAKTA untuk dokumen 19/02]
"""

import glob
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

THRESHOLD_RTT = 100.0
THRESHOLD_LOSS = 1.0
SEGMENT_GAP_S = 300.0


def parse_ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def load_probes(paths):
    series = defaultdict(list)
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("kind") != "probe":
                    continue
                d = r.get("data", {})
                key = (d.get("interface"), d.get("target"))
                if not all(key):
                    continue
                try:
                    t = parse_ts(r["ts_utc"])
                except Exception:
                    continue
                series[key].append({
                    "t": t,
                    "rtt": d.get("rtt_ms"),
                    "success": bool(d.get("success")),
                    "loss": float(d.get("packet_loss") or 0),
                })
    return series


def split_segments(rows):
    rows = sorted(rows, key=lambda x: x["t"])
    segs = []
    cur = [rows[0]]
    for r in rows[1:]:
        if r["t"] - cur[-1]["t"] > SEGMENT_GAP_S:
            segs.append(cur)
            cur = [r]
        else:
            cur.append(r)
    segs.append(cur)
    return segs


def resample(rows):
    if len(rows) < 3:
        return None, None, None
    t = np.array([r["t"] for r in rows], dtype=float)
    t0 = math.floor(t[0])
    t1 = math.ceil(t[-1])
    grid = np.arange(t0, t1 + 1, 1.0)
    rtt = np.interp(grid, t, np.array([
        r["rtt"] if (r["success"] and r["rtt"] is not None) else np.nan for r in rows
    ], dtype=float))
    if np.isnan(rtt).any():
        good = ~np.isnan(rtt)
        if good.sum() < 2:
            return None, None, None
        rtt = np.interp(grid, grid[good], rtt[good])
    loss = np.interp(grid, t, np.array([r["loss"] for r in rows], dtype=float))
    success = np.interp(grid, t, np.array([1.0 if r["success"] else 0.0 for r in rows], dtype=float))
    return grid, rtt, {"loss": loss, "success": success}


def moving_average(x, window=61):
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


def bad_indicator(rtt, loss, success):
    return (~success.astype(bool)) | (loss > THRESHOLD_LOSS) | (rtt > THRESHOLD_RTT)


def episode_starts(bad):
    starts = []
    prev = False
    for i, value in enumerate(bad):
        if value and not prev:
            starts.append(i)
        prev = value
    return starts


def jaccard(a, b):
    a = np.asarray(a, dtype=bool)
    b = np.asarray(b, dtype=bool)
    union = np.logical_or(a, b).sum()
    if union == 0:
        return None
    return np.logical_and(a, b).sum() / union


def match_starts(a, b, tolerance=2):
    if not a or not b:
        return None
    b = np.array(b)
    matched = 0
    for x in a:
        if np.min(np.abs(b - x)) <= tolerance:
            matched += 1
    return matched / len(a)


def pair_stats(grid_a, rtt_a, bad_a, raw_a, grid_b, rtt_b, bad_b, raw_b):
    start = max(grid_a[0], grid_b[0])
    end = min(grid_a[-1], grid_b[-1])
    if end <= start:
        return None
    grid = np.arange(start, end + 1)
    x = np.interp(grid, grid_a, rtt_a)
    y = np.interp(grid, grid_b, rtt_b)
    r_res = float(np.corrcoef(x, y)[0, 1])
    if math.isnan(r_res):
        r_res = None
    xr = np.interp(grid, grid_a, raw_a)
    yr = np.interp(grid, grid_b, raw_b)
    r_raw = float(np.corrcoef(xr, yr)[0, 1])
    if math.isnan(r_raw):
        r_raw = None
    b1 = np.interp(grid, grid_a, bad_a) > 0.5
    b2 = np.interp(grid, grid_b, bad_b) > 0.5
    return {
        "residual_r": r_res,
        "raw_r": r_raw,
        "bad_jaccard": jaccard(b1, b2),
        "episode_match": match_starts(episode_starts(b1), episode_starts(b2)),
        "n": len(grid),
    }


def fmt(value, digits=3):
    if value is None:
        return "—"
    try:
        if math.isnan(value):
            return "—"
    except TypeError:
        pass
    return f"{value:.{digits}f}"


def main():
    paths = sorted(glob.glob("data/baseline_rb1100ahx4_2026111*.jsonl"))
    series = load_probes(paths)

    # Pecah per interface-target menjadi segmen kontinu
    seg_store = defaultdict(list)  # (iface, target, seg_idx) -> prepared
    seg_meta = {}
    seg_counter = defaultdict(int)

    for key, rows in series.items():
        segs = split_segments(rows)
        for si, seg in enumerate(segs):
            grid, rtt, extra = resample(seg)
            if grid is None or len(grid) < 120:
                continue
            margin = 60
            core = slice(margin, len(rtt) - margin)
            base = moving_average(rtt, 61)
            residual = rtt - base
            bad = bad_indicator(rtt[core], extra["loss"][core], extra["success"][core]).astype(float)
            g = grid[core]
            seg_store[(key[0], key[1], seg_counter[key])].append((g, residual[core], bad, rtt[core]))
            seg_meta[(key[0], key[1], seg_counter[key])] = (
                datetime.fromtimestamp(g[0], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.fromtimestamp(g[-1], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                int(len(g)),
            )
            seg_counter[key] += 1

    # Cari segmen yang A dan B sama-sama punya data (per target)
    targets = sorted({k[1] for k in seg_store})
    lines = []
    lines.append("# Uji Independensi A–B per Segmen Kontinu (Data Asli)")
    lines.append("")
    lines.append(f"**Sumber:** {', '.join(paths)}")
    lines.append("")
    lines.append(f"Segmen = deret probe kontinu (gap antar-probe ≤ {int(SEGMENT_GAP_S)} s). "
                 "Resample 1 s **hanya dalam segmen** — tidak ada interpolasi lintas celah.")
    lines.append("")

    all_pairs = []
    for target in targets:
        keys = sorted([k for k in seg_store if k[1] == target])
        # kelompokkan per segmen index
        by_seg = defaultdict(list)
        for k in keys:
            by_seg[k[2]].append(k)
        for seg_idx, ks in sorted(by_seg.items()):
            if len(ks) < 2:
                continue
            kA = next((k for k in ks if k[0] == "ether1-ISP-A"), None)
            kB = next((k for k in ks if k[0] == "ether2-ISP-B"), None)
            if kA is None or kB is None:
                continue
            gA, rA, bA, rawA = seg_store[kA][0]
            gB, rB, bB, rawB = seg_store[kB][0]
            st = pair_stats(gA, rA, bA, rawA, gB, rB, bB, rawB)
            if st is None:
                continue
            t0A, t1A, nA = seg_meta[kA]
            t0B, t1B, nB = seg_meta[kB]
            start = max(t0A, t0B)
            end = min(t1A, t1B)
            all_pairs.append({**st, "target": target, "start": start, "end": end})
            lines.append(f"### Segmen: {start} → {end} (UTC) — target {target}")
            lines.append("")
            lines.append(f"| A | B | r residual | r mentah | Jaccard bad | Episode match | n |")
            lines.append(f"|---|---|---:|---:|---:|---:|---:|")
            lines.append(f"| {kA[0]} | {kB[0]} | {fmt(st['residual_r'])} | {fmt(st['raw_r'])} | "
                         f"{fmt(st['bad_jaccard'])} | {fmt(st['episode_match'])} | {st['n']} |")
            lines.append("")

    Path("data/uji_independensi_AB_segmen.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Segmen diperiksa: {len(all_pairs)}")
    for p in all_pairs:
        print(f"{p['start']} → {p['end']} [{p['target']}]: residual={fmt(p['residual_r'])} "
              f"raw={fmt(p['raw_r'])} jaccard={fmt(p['bad_jaccard'])} match={fmt(p['episode_match'])} n={p['n']}")


if __name__ == "__main__":
    main()
