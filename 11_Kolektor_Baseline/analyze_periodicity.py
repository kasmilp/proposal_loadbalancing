#!/usr/bin/env python3
"""
Analisis lanjutan: periodisitas 15 detik, korelasi, dan Episode.
Membutuhkan numpy.

Fokus pada satu file JSONL hasil collector.
"""

import argparse
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np


def parse_ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def load_probes(path):
    series = defaultdict(list)
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
            series[key].append({
                "t": parse_ts(r["ts_utc"]),
                "rtt": d.get("rtt_ms"),
                "success": bool(d.get("success")),
                "loss": float(d.get("packet_loss") or 0),
            })
    return series


def resample(rows):
    rows = sorted([r for r in rows if r["t"] is not None], key=lambda x: x["t"])
    if len(rows) < 3:
        return None, None, None
    t = np.array([r["t"] for r in rows], dtype=float)
    t0 = math.floor(t[0])
    t1 = math.ceil(t[-1])
    grid = np.arange(t0, t1 + 1, 1.0)
    rtt = np.interp(grid, t, np.array([
        r["rtt"] if (r["success"] and r["rtt"] is not None) else np.nan for r in rows
    ], dtype=float))
    # Isi NaN dengan interpolasi linear
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


def acf(x, max_lag=60):
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    denom = np.dot(x, x)
    if denom <= 0:
        return np.zeros(max_lag + 1)
    return np.array([np.dot(x[:-lag], x[lag:]) / denom if lag else 1.0 for lag in range(max_lag + 1)])


def dominant_period(x, min_period=5.0, max_period=30.0):
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    n = len(x)
    if n < 120:
        return None, None
    freqs = np.fft.rfftfreq(n, d=1.0)
    amp = np.abs(np.fft.rfft(x))
    mask = (freqs >= 1.0 / max_period) & (freqs <= 1.0 / min_period)
    if not mask.any():
        return None, None
    idx = np.where(mask)[0]
    best = idx[np.argmax(amp[idx])]
    period = 1.0 / freqs[best]
    ratio = amp[best] / (np.median(amp[idx]) + 1e-12)
    return period, ratio


def bad_indicator(rtt, loss, success, threshold):
    return (~success.astype(bool)) | (loss > 1.0) | (rtt > threshold)


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


def analyze(path, threshold=100.0):
    series = load_probes(path)
    results = []
    residuals = {}
    bads = {}

    for key, rows in sorted(series.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        iface, target = key
        grid, rtt, extra = resample(rows)
        if grid is None or len(grid) < 120:
            continue
        base = moving_average(rtt, 61)
        residual = rtt - base
        # Buang tepi yang bias moving average
        margin = 60
        core = slice(margin, len(rtt) - margin)
        r = residual[core]
        ac = acf(r, 60)
        period, ratio = dominant_period(r)
        loss = extra["loss"][core]
        success = extra["success"][core]
        bad = bad_indicator(rtt[core], loss, success, threshold)
        ac_bad = acf(bad.astype(float), 30)
        starts = episode_starts(bad)
        gaps = np.diff(starts) if len(starts) > 1 else np.array([])
        gaps_mod = np.mod(gaps, 15) if len(gaps) else np.array([])
        near15 = np.mean((gaps_mod <= 1) | (gaps_mod >= 14)) if len(gaps_mod) else None

        results.append({
            "interface": iface,
            "target": target,
            "n_1s": int(len(r)),
            "rtt_median": float(np.median(rtt[core])),
            "rtt_p95": float(np.percentile(rtt[core], 95)),
            "acf15_raw": float(ac[15]),
            "acf15_residual": float(acf(r, 60)[15]),
            "period_s": float(period) if period else None,
            "period_ratio": float(ratio) if ratio else None,
            "bad_acf15": float(ac_bad[15]),
            "bad_acf_peak_lag": int(np.argmax(ac_bad[1:]) + 1),
            "bad_acf_peak": float(np.max(ac_bad[1:])),
            "episodes": len(starts),
            "gap_near15_frac": float(near15) if near15 is not None else None,
        })
        residuals[(iface, target)] = (grid[core], r)
        bads[(iface, target)] = (grid[core], bad.astype(float))

    # Korelasi antar-interface untuk target yang sama
    corr = []
    targets = sorted({k[1] for k in residuals})
    for target in targets:
        keys = sorted([k for k in residuals if k[1] == target])
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                g1, r1 = residuals[keys[i]]
                g2, r2 = residuals[keys[j]]
                start = max(g1[0], g2[0])
                end = min(g1[-1], g2[-1])
                if end <= start:
                    continue
                grid = np.arange(start, end + 1)
                x = np.interp(grid, g1, r1)
                y = np.interp(grid, g2, r2)
                r = float(np.corrcoef(x, y)[0, 1])
                if math.isnan(r):
                    r = None
                g1b, b1v = bads[keys[i]]
                g2b, b2v = bads[keys[j]]
                b1 = np.interp(grid, g1b, b1v) > 0.5
                b2 = np.interp(grid, g2b, b2v) > 0.5
                corr.append({
                    "target": target,
                    "a": keys[i][0],
                    "b": keys[j][0],
                    "residual_r": r,
                    "bad_jaccard": jaccard(b1, b2),
                    "episode_match": match_starts(episode_starts(b1), episode_starts(b2)),
                    "n": len(grid),
                })

    return results, corr


def write_report(results, corr, out, path):
    def fmt(value, digits=3):
        if value is None:
            return "—"
        try:
            if math.isnan(value):
                return "—"
        except TypeError:
            pass
        return f"{value:.{digits}f}"

    lines = ["# Analisis Periodisitas dan Korelasi Baseline", ""]
    lines.append(f"**File:** `{path}`")
    lines.append("")
    lines.append("## 1. Periodisitas per Seri")
    lines.append("")
    lines.append("| Interface | Target | n (1 s) | Median RTT | p95 | ACF15 residual | Periode dominan | Rasio puncak | Bad ACF15 | Episode | Gap ≈15 s |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in results:
        gap = f"{r['gap_near15_frac']:.2f}" if r['gap_near15_frac'] is not None else "—"
        period = f"{r['period_s']:.2f}" if r['period_s'] is not None else "—"
        ratio = f"{r['period_ratio']:.1f}" if r['period_ratio'] is not None else "—"
        lines.append(
            f"| {r['interface']} | {r['target']} | {r['n_1s']} | {r['rtt_median']:.1f} | {r['rtt_p95']:.1f} | "
            f"{r['acf15_residual']:.3f} | {period} | {ratio} | "
            f"{r['bad_acf15']:.3f} | {r['episodes']} | {gap} |"
        )
    lines.append("")
    lines.append("## 2. Korelasi Antar-Interface")
    lines.append("")
    lines.append("| Target | A | B | r residual | Jaccard bad | Episode match | n |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for c in corr:
        lines.append(
            f"| {c['target']} | {c['a']} | {c['b']} | {fmt(c['residual_r'])} | "
            f"{fmt(c['bad_jaccard'])} | {fmt(c['episode_match'])} | {c['n']} |"
        )
    lines.append("")
    lines.append("## 3. Interpretasi Cepat")
    lines.append("")
    lines.append("- **ACF15 residual** mengukur korelasi setelah tren 60 detik dihilangkan.")
    lines.append("- **Periode dominan** diambil dari FFT pada rentang 5–30 detik.")
    lines.append("- **Bad ACF15** mengukur apakah episode buruk berulang tiap 15 detik.")
    lines.append("- **Jaccard** mengukur tumpang tindih episode buruk antar-WAN.")
    lines.append("- **Episode match** mengukur proporsi episode A yang punya pasangan episode B dalam ±2 detik.")
    Path(out).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--out", default=None)
    parser.add_argument("--threshold", type=float, default=100.0)
    args = parser.parse_args()

    results, corr = analyze(args.file, args.threshold)
    out = args.out or str(Path(args.file).with_suffix(".periodicity.md"))
    write_report(results, corr, out, args.file)
    print(f"Laporan: {out}")


if __name__ == "__main__":
    main()
