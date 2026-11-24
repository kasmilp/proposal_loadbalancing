#!/usr/bin/env python3
"""Cakupan data asli (probe) per hari UTC untuk semua file baseline.

Menampilkan timestamp pertama/terakhir & jumlah probe asli per tanggal,
tanpa interpolasi. Untuk memvalidasi klaim "baseline 5 hari"."
"""

import glob
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def parse_ts(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def main():
    files = sorted(glob.glob("data/baseline_rb1100ahx4_2026111*.jsonl"))
    per_day = defaultdict(lambda: {"n": 0, "first": None, "last": None})
    for path in files:
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
                ts = parse_ts(r.get("ts_utc", ""))
                if ts is None:
                    continue
                day = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
                d = per_day[day]
                d["n"] += 1
                if d["first"] is None or ts < d["first"]:
                    d["first"] = ts
                if d["last"] is None or ts > d["last"]:
                    d["last"] = ts
    print("Hari (UTC) | n probe asli | pertama | terakhir | durasi jam")
    for day in sorted(per_day):
        d = per_day[day]
        dur = (d["last"] - d["first"]) / 3600 if d["first"] and d["last"] else 0
        f = datetime.fromtimestamp(d["first"], tz=timezone.utc).strftime("%H:%M:%S")
        l = datetime.fromtimestamp(d["last"], tz=timezone.utc).strftime("%H:%M:%S")
        print(f"{day} | {d['n']} | {f} | {l} | {dur:.2f}")


if __name__ == "__main__":
    main()
