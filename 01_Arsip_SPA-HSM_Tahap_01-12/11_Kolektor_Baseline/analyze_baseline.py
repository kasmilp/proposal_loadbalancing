#!/usr/bin/env python3
"""
Analisis baseline dari collector.py.

Input : file JSONL hasil collector.
Output: report.md + summary.json

Tidak memerlukan pandas/numpy.
"""

import argparse
import glob
import json
import math
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def parse_ts(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def percentile(values, p):
    if not values:
        return None
    data = sorted(values)
    if len(data) == 1:
        return data[0]
    rank = (len(data) - 1) * p
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return data[lo]
    return data[lo] + (data[hi] - data[lo]) * (rank - lo)


def mean(values):
    return sum(values) / len(values) if values else None


def pearson(x, y):
    n = min(len(x), len(y))
    if n < 3:
        return None
    x = x[:n]
    y = y[:n]
    mx = mean(x)
    my = mean(y)
    if mx is None or my is None:
        return None
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a - mx) ** 2 for a in x))
    dy = math.sqrt(sum((b - my) ** 2 for b in y))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def autocorr(values, lag):
    if len(values) <= lag + 2:
        return None
    return pearson(values[:-lag], values[lag:])


def resample_1s(times, values):
    """Interpolasi linear ke grid 1 detik."""
    if len(times) < 2:
        return [], []
    pairs = sorted(zip(times, values))
    t0 = math.floor(pairs[0][0])
    t1 = math.ceil(pairs[-1][0])
    grid = list(range(t0, t1 + 1))
    out = []
    j = 0
    for t in grid:
        while j + 1 < len(pairs) and pairs[j + 1][0] < t:
            j += 1
        if t <= pairs[0][0]:
            out.append(pairs[0][1])
            continue
        if t >= pairs[-1][0]:
            out.append(pairs[-1][1])
            continue
        a, b = pairs[j], pairs[j + 1]
        if b[0] == a[0]:
            out.append(a[1])
        else:
            ratio = (t - a[0]) / (b[0] - a[0])
            out.append(a[1] + (b[1] - a[1]) * ratio)
    return grid, out


def load_records(paths):
    records = []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def analyze(paths, rtt_threshold, loss_threshold, interfaces_filter):
    records = load_records(paths)
    if not records:
        raise SystemExit("Tidak ada record")

    meta = next((r["data"] for r in records if r.get("kind") == "meta"), {})
    times = [parse_ts(r.get("ts_utc")) for r in records if r.get("ts_utc")]
    times = [t for t in times if t is not None]

    probes = defaultdict(list)
    interface_series = defaultdict(list)
    latest = {}
    counts = defaultdict(int)

    for rec in records:
        kind = rec.get("kind")
        data = rec.get("data")
        ts = parse_ts(rec.get("ts_utc"))
        if ts is None:
            continue
        if kind == "probe" and isinstance(data, dict):
            key = (data.get("interface"), data.get("target"))
            probes[key].append((ts, data))
        elif kind == "interface" and isinstance(data, list):
            for item in data:
                name = item.get("name")
                try:
                    rx = int(str(item.get("rx-byte", "0")))
                    tx = int(str(item.get("tx-byte", "0")))
                except ValueError:
                    continue
                interface_series[name].append((ts, rx, tx))
        elif kind in ("route", "mangle", "address", "service", "group", "netwatch", "resource", "identity"):
            if isinstance(data, list):
                counts[kind] = max(counts[kind], len(data))
                latest[kind] = data

    # Probe summary
    probe_summary = []
    series_by_interface = defaultdict(list)
    for (iface, target), rows in sorted(probes.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        rtts = [r.get("rtt_ms") for _, r in rows if r.get("success") and r.get("rtt_ms") is not None]
        successes = [1 if r.get("success") else 0 for _, r in rows]
        n = len(rows)
        loss = 100.0 * (1 - sum(successes) / n) if n else None
        summary = {
            "interface": iface,
            "target": target,
            "samples": n,
            "success": sum(successes),
            "loss_pct": round(loss, 3) if loss is not None else None,
            "rtt_median_ms": round(percentile(rtts, 0.50), 2) if rtts else None,
            "rtt_p95_ms": round(percentile(rtts, 0.95), 2) if rtts else None,
            "rtt_min_ms": round(min(rtts), 2) if rtts else None,
            "rtt_max_ms": round(max(rtts), 2) if rtts else None,
        }
        # Jitter: rata-rata selisih absolut RTT berurutan
        if len(rtts) > 1:
            diffs = [abs(rtts[i] - rtts[i - 1]) for i in range(1, len(rtts))]
            summary["jitter_ms"] = round(mean(diffs), 2)
        else:
            summary["jitter_ms"] = None

        # Periodisitas pada grid 1 detik
        if len(rtts) >= 20:
            t_valid = [t for t, r in rows if r.get("success") and r.get("rtt_ms") is not None]
            grid, resampled = resample_1s(t_valid, rtts)
            if len(resampled) >= 60:
                ac = {lag: autocorr(resampled, lag) for lag in range(1, 61)}
                valid = {k: v for k, v in ac.items() if v is not None}
                top = sorted(valid.items(), key=lambda kv: kv[1], reverse=True)[:3]
                summary["periodicity"] = [
                    {"lag_s": lag, "autocorr": round(val, 3)} for lag, val in top
                ]
                summary["autocorr_15s"] = round(ac.get(15), 3) if ac.get(15) is not None else None
                series_by_interface[iface].append((grid, resampled, target))
        probe_summary.append(summary)

    # Korelasi antar-interface pada target yang sama
    correlations = []
    by_target = defaultdict(dict)
    for iface, grid, target in [(i, g, t) for i, lst in series_by_interface.items() for g, _, t in lst]:
        by_target[target][iface] = grid
    # Sederhanakan: korelasi memakai RTT median series per interface/target
    raw_series = defaultdict(list)
    for (iface, target), rows in probes.items():
        if not iface or not target:
            continue
        t_valid = [t for t, r in rows if r.get("success") and r.get("rtt_ms") is not None]
        v_valid = [r.get("rtt_ms") for _, r in rows if r.get("success") and r.get("rtt_ms") is not None]
        if len(t_valid) >= 20:
            grid, resampled = resample_1s(t_valid, v_valid)
            raw_series[(iface, target)] = (grid, resampled)
    for target in sorted({k[1] for k in raw_series}):
        ifaces = sorted({k[0] for k in raw_series if k[1] == target})
        for i in range(len(ifaces)):
            for j in range(i + 1, len(ifaces)):
                g1, v1 = raw_series[(ifaces[i], target)]
                g2, v2 = raw_series[(ifaces[j], target)]
                start = max(g1[0], g2[0])
                end = min(g1[-1], g2[-1])
                if end <= start:
                    continue
                x = [v1[t - g1[0]] for t in range(start, end + 1)]
                y = [v2[t - g2[0]] for t in range(start, end + 1)]
                r = pearson(x, y)
                if r is not None:
                    correlations.append({
                        "target": target,
                        "interface_a": ifaces[i],
                        "interface_b": ifaces[j],
                        "pearson_r": round(r, 3),
                        "n": len(x),
                    })

    # Episode degradasi sederhana
    episodes = []
    for (iface, target), rows in probes.items():
        degraded = []
        for ts, r in rows:
            loss = 0.0
            try:
                loss = float(r.get("packet_loss") or 0)
            except ValueError:
                pass
            rtt = r.get("rtt_ms")
            is_bad = (not r.get("success")) or loss > loss_threshold or (rtt is not None and rtt > rtt_threshold)
            degraded.append((ts, is_bad))
        count = 0
        total = 0
        durations = []
        start = None
        prev = None
        for ts, bad in degraded:
            if bad and start is None:
                start = ts
            if not bad and start is not None:
                count += 1
                durations.append(ts - start)
                total += ts - start
                start = None
            prev = ts
        if start is not None:
            count += 1
            durations.append(prev - start)
            total += prev - start
        episodes.append({
            "interface": iface,
            "target": target,
            "episodes": count,
            "total_duration_s": round(total, 1),
            "median_duration_s": round(percentile(durations, 0.50), 1) if durations else None,
        })

    # Throughput interface dari delta counter
    throughput = []
    for name, rows in interface_series.items():
        if interfaces_filter and name not in interfaces_filter:
            continue
        rows = sorted(rows)
        rx_rates = []
        tx_rates = []
        for (t1, rx1, tx1), (t2, rx2, tx2) in zip(rows, rows[1:]):
            dt = t2 - t1
            if dt <= 0 or dt > 60:
                continue
            rx_rates.append((rx2 - rx1) * 8 / dt / 1e6)
            tx_rates.append((tx2 - tx1) * 8 / dt / 1e6)
        if rx_rates:
            throughput.append({
                "interface": name,
                "samples": len(rx_rates),
                "rx_mean_mbps": round(mean(rx_rates), 3),
                "rx_p95_mbps": round(percentile(rx_rates, 0.95), 3),
                "tx_mean_mbps": round(mean(tx_rates), 3),
                "tx_p95_mbps": round(percentile(tx_rates, 0.95), 3),
            })

    # Layanan terbuka
    open_services = []
    for item in latest.get("service", []):
        if item.get("disabled") in (True, "true"):
            continue
        if item.get("address") in (None, ""):
            open_services.append(item.get("name"))

    return {
        "meta": meta,
        "time_range": {
            "start": datetime.fromtimestamp(min(times)).isoformat() if times else None,
            "end": datetime.fromtimestamp(max(times)).isoformat() if times else None,
        },
        "records": len(records),
        "counts": dict(counts),
        "probe_summary": probe_summary,
        "correlations": correlations,
        "episodes": episodes,
        "throughput": throughput,
        "open_services": sorted(set(open_services)),
        "files": [str(p) for p in paths],
    }


def write_report(result, out_path, rtt_threshold, loss_threshold):
    lines = []
    lines.append("# Laporan Baseline Read-Only\n")
    lines.append(f"**Rentang:** {result['time_range']['start']} → {result['time_range']['end']}\n")
    lines.append(f"**Jumlah record:** {result['records']}\n")
    meta = result.get("meta", {})
    lines.append(f"**Router:** {meta.get('router')} | **Site:** {meta.get('site')} | **Read-only:** {meta.get('read_only')}\n")
    lines.append("")
    lines.append("## 1. Probe per WAN\n")
    lines.append("| Interface | Target | Sampel | Sukses | Loss % | RTT median | RTT p95 | Jitter | Autokorelasi 15 s |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in result["probe_summary"]:
        lines.append(
            f"| {row['interface']} | {row['target']} | {row['samples']} | {row['success']} | "
            f"{row['loss_pct']} | {row['rtt_median_ms']} | {row['rtt_p95_ms']} | "
            f"{row.get('jitter_ms')} | {row.get('autocorr_15s')} |"
        )
    lines.append("")
    lines.append("## 2. Periodisitas\n")
    for row in result["probe_summary"]:
        per = row.get("periodicity")
        if per:
            lines.append(f"- **{row['interface']}** → {row['target']}: " + ", ".join(
                f"lag {p['lag_s']} s (r={p['autocorr']})" for p in per
            ))
    if not any(row.get("periodicity") for row in result["probe_summary"]):
        lines.append("Tidak cukup data untuk analisis periodisitas (minimal ±60 sampel valid).")
    lines.append("")
    lines.append("## 3. Korelasi Antar-Interface\n")
    if result["correlations"]:
        lines.append("| Target | Interface A | Interface B | Pearson r | n |")
        lines.append("|---|---|---|---:|---:|")
        for c in result["correlations"]:
            lines.append(f"| {c['target']} | {c['interface_a']} | {c['interface_b']} | {c['pearson_r']} | {c['n']} |")
    else:
        lines.append("Belum ada pasangan data yang cukup.")
    lines.append("")
    lines.append("## 4. Episode Degradasi\n")
    lines.append(f"Ambang: RTT > {rtt_threshold} ms atau loss > {loss_threshold}%.\n")
    lines.append("| Interface | Target | Episode | Total durasi (s) | Median durasi (s) |")
    lines.append("|---|---|---:|---:|---:|")
    for e in result["episodes"]:
        lines.append(
            f"| {e['interface']} | {e['target']} | {e['episodes']} | "
            f"{e['total_duration_s']} | {e['median_duration_s']} |"
        )
    lines.append("")
    lines.append("## 5. Throughput Interface\n")
    if result["throughput"]:
        lines.append("| Interface | Sampel | RX mean (Mbps) | RX p95 | TX mean | TX p95 |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for t in result["throughput"]:
            lines.append(
                f"| {t['interface']} | {t['samples']} | {t['rx_mean_mbps']} | "
                f"{t['rx_p95_mbps']} | {t['tx_mean_mbps']} | {t['tx_p95_mbps']} |"
            )
    else:
        lines.append("Belum ada data counter interface.")
    lines.append("")
    lines.append("## 6. Snapshot Konfigurasi\n")
    lines.append(f"- Route: {result['counts'].get('route')}")
    lines.append(f"- Mangle: {result['counts'].get('mangle')}")
    lines.append(f"- Address: {result['counts'].get('address')}")
    lines.append(f"- Service terbuka tanpa address: {', '.join(result['open_services']) or '—'}")
    lines.append("")
    lines.append("## 7. Keterbatasan\n")
    lines.append("- Episode dihitung dari sampel probe, bukan dari Q_i(t) penuh.")
    lines.append("- Periodisitas bergantung pada interval probe dan kualitas timestamp.")
    lines.append("- Korelasi Pearson mengasumsikan hubungan linier.")
    lines.append("- Tidak ada klaim kausal dari data observasional ini.")
    lines.append("")

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Analisis baseline collector")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--glob", default="*.jsonl")
    parser.add_argument("--rtt-threshold", type=float, default=100.0)
    parser.add_argument("--loss-threshold", type=float, default=1.0)
    parser.add_argument("--interfaces", default=None, help="Filter interface, pisahkan koma")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    data_dir = Path(args.data_dir or base / "data")
    paths = sorted(Path(p) for p in glob.glob(str(data_dir / args.glob)))
    if not paths:
        raise SystemExit(f"Tidak ada file di {data_dir}")

    interfaces = [x.strip() for x in args.interfaces.split(",")] if args.interfaces else None
    result = analyze(paths, args.rtt_threshold, args.loss_threshold, interfaces)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_md = Path(args.out or base / f"report_{stamp}.md")
    out_json = out_md.with_suffix(".json")
    write_report(result, out_md, args.rtt_threshold, args.loss_threshold)
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Laporan: {out_md}")
    print(f"Ringkasan: {out_json}")


if __name__ == "__main__":
    main()
