#!/usr/bin/env python3
"""
Analisis khusus file baseline_rb1100ahx4_20261117_181759.jsonl.

Output:
- jenis record & jumlah
- rentang waktu per jenis
- ringkasan probe per (interface, target): n, sukses, loss, RTT median/p95/min/max, jitter
- kualitas: gap antar-probe, jumlah timeout, duplikasi timestamp
- interval sampling per jenis record
"""

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np


def parse_ts(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def main(path, out):
    counts = defaultdict(int)
    first_ts = {}
    last_ts = {}
    probes = defaultdict(list)

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = r.get("kind", "?")
            counts[kind] += 1
            ts = parse_ts(r.get("ts_utc", ""))
            if ts is None:
                continue
            if kind not in first_ts or ts < first_ts[kind]:
                first_ts[kind] = ts
            if kind not in last_ts or ts > last_ts[kind]:
                last_ts[kind] = ts
            if kind == "probe":
                d = r.get("data", {})
                key = (d.get("interface"), d.get("target"))
                probes[key].append({
                    "t": ts,
                    "rtt": d.get("rtt_ms"),
                    "success": bool(d.get("success")),
                    "loss": float(d.get("packet_loss") or 0),
                })

    lines = []
    lines.append("# Analisis File baseline_rb1100ahx4_20261117_181759.jsonl")
    lines.append("")
    lines.append(f"**Sumber:** `{path}`")
    lines.append("")

    lines.append("## 1. Jenis record")
    lines.append("")
    lines.append("| Jenis | Jumlah | Rentang waktu (UTC) |")
    lines.append("|---|---|---|")
    for k, v in sorted(counts.items()):
        t0 = datetime.utcfromtimestamp(first_ts[k]).strftime("%Y-%m-%d %H:%M:%S") if k in first_ts else "-"
        t1 = datetime.utcfromtimestamp(last_ts[k]).strftime("%Y-%m-%d %H:%M:%S") if k in last_ts else "-"
        lines.append(f"| {k} | {v} | {t0} → {t1} |")
    lines.append("")

    lines.append("## 2. Ringkasan probe per WAN")
    lines.append("")
    probes = {k: sorted(v, key=lambda x: x["t"]) for k, v in probes.items()}
    for (iface, target), rows in sorted(probes.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        n = len(rows)
        ok = sum(1 for r in rows if r["success"])
        loss_pct = 100.0 * (1 - ok / n) if n else None
        rtts = [r["rtt"] for r in rows if r["success"] and r["rtt"] is not None]
        if rtts:
            med = float(np.median(rtts))
            p95 = float(np.percentile(rtts, 95))
            mn = min(rtts)
            mx = max(rtts)
            diffs = [abs(rtts[i] - rtts[i - 1]) for i in range(1, len(rtts))]
            jitter = float(np.mean(diffs)) if diffs else None
        else:
            med = p95 = mn = mx = jitter = None

        gaps = np.diff([r["t"] for r in rows])
        gap_median = float(np.median(gaps)) if len(gaps) else None
        gap_max = float(np.max(gaps)) if len(gaps) else None
        span = rows[-1]["t"] - rows[0]["t"] if n > 1 else 0

        lines.append(f"### {iface} → {target}")
        lines.append("")
        lines.append(f"- n = {n}, sukses = {ok}, loss = {loss_pct:.3f}%")
        lines.append(f"- RTT median = {med:.2f} ms, p95 = {p95:.2f} ms, min = {mn:.2f} ms, max = {mx:.2f} ms, jitter = {jitter:.2f} ms")
        lines.append(f"- Gap antar-probe: median = {gap_median:.2f} s, maks = {gap_max:.2f} s; rentang durasi = {span/3600:.2f} jam")
        lines.append("")

    all_ts = []
    for rows in probes.values():
        all_ts.extend(r["t"] for r in rows)
    dup = len(all_ts) - len(set(all_ts))
    big_gaps = 0
    for rows in probes.values():
        g = np.diff([r["t"] for r in rows])
        big_gaps += int((g > 60).sum())

    lines.append("## 3. Kualitas data")
    lines.append("")
    lines.append(f"- Total probe = {len(all_ts)}; timestamp duplikat = {dup}")
    lines.append(f"- Gap antar-probe > 60 s (jumlah kejadian) = {big_gaps}")
    lines.append("")

    Path(out).write_text("\n".join(lines), encoding="utf-8")
    print(f"Laporan: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    out = args.out or str(Path(args.file).with_suffix(".analisis.md"))
    main(args.file, out)

