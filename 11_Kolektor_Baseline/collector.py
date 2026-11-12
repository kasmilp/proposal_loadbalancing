#!/usr/bin/env python3
"""
Kolektor baseline read-only untuk RouterOS.

Prinsip:
- Hanya memanggil endpoint /print dan /ping (test).
- Tidak ada add/set/remove/disable/enable.
- Kredensial dibaca dari environment atau .env lokal.
- Output JSONL, satu baris per observasi.
"""

import argparse
import json
import logging
import os
import re
import signal
import ssl
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import librouteros
except ImportError:
    sys.exit("librouteros belum terpasang. Jalankan: pip install librouteros")

READ_PATHS = {
    "/system/resource/print": "resource",
    "/system/identity/print": "identity",
    "/interface/print": "interface",
    "/interface/ethernet/print": "ethernet",
    "/ip/address/print": "address",
    "/ip/route/print": "route",
    "/ip/firewall/mangle/print": "mangle",
    "/ip/firewall/nat/print": "nat",
    "/ip/service/print": "service",
    "/user/group/print": "group",
    "/tool/netwatch/print": "netwatch",
}

RUNNING = True


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_env(path: Path):
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def env(name, default=None):
    return os.environ.get(name, default)


def parse_duration(value):
    if value is None or str(value).strip() in ("", "0"):
        return 0
    text = str(value).strip().lower()
    match = re.fullmatch(r"(\d+(?:\.\d+)?)([smhd])", text)
    if not match:
        raise ValueError(f"Durasi tidak valid: {value}")
    number, unit = match.groups()
    factor = {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
    return float(number) * factor


def parse_ros_duration(text):
    """Ubah '45ms793us' atau '1s23ms' menjadi milidetik."""
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    text = str(text).strip()
    if not text:
        return None
    units = {
        "w": 604800000.0,
        "d": 86400000.0,
        "h": 3600000.0,
        "ms": 1.0,
        "us": 0.001,
        "ns": 0.000001,
        "m": 60000.0,
        "s": 1000.0,
    }
    found = re.findall(r"(\d+(?:\.\d+)?)(ms|us|ns|w|d|h|m|s)", text)
    if not found:
        return None
    total = 0.0
    for number, unit in found:
        total += float(number) * units[unit]
    return round(total, 3)


def make_ssl_wrapper(host):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1
    except Exception:
        pass
    ctx.set_ciphers("ALL:@SECLEVEL=0")
    if hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"):
        ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT

    def wrap(sock):
        return ctx.wrap_socket(sock, server_hostname=host)

    return wrap


class Collector:
    def __init__(self, args):
        self.host = env("ROS_HOST")
        self.port = int(env("ROS_PORT", "8729"))
        self.user = env("ROS_USER")
        self.password = env("ROS_PASS")
        if not all([self.host, self.user, self.password]):
            raise SystemExit("ROS_HOST, ROS_USER, dan ROS_PASS harus diisi")

        self.site = env("SITE_LABEL", "site")
        self.router = env("ROUTER_LABEL", "router")
        self.tag = args.tag
        self.probe = not args.no_probe
        self.connections = args.connections
        self.probe_targets = [x.strip() for x in env("PROBE_TARGETS", "1.1.1.1").split(",") if x.strip()]
        self.probe_interfaces = [
            x.strip() for x in env(
                "PROBE_INTERFACES",
                "ether1-ISP-A,ether2-ISP-B,ether3-ISP-C"
            ).split(",") if x.strip()
        ]

        self.intervals = {
            "resource": int(env("INTERVAL_RESOURCE", "10")),
            "identity": 3600,
            "interface": int(env("INTERVAL_INTERFACE", "10")),
            "ethernet": 300,
            "address": 60,
            "route": int(env("INTERVAL_ROUTE", "60")),
            "mangle": int(env("INTERVAL_MANGLE", "60")),
            "nat": 300,
            "service": int(env("INTERVAL_SERVICE", "3600")),
            "group": int(env("INTERVAL_SERVICE", "3600")),
            "netwatch": 60,
        }
        self.probe_interval = float(env("INTERVAL_PROBE", "2"))

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = Path(__file__).resolve().parent
        self.out_dir = Path(args.out_dir or env("OUT_DIR", str(base / "data")))
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir = base / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.out_path = self.out_dir / f"{self.tag}_{self.router}_{stamp}.jsonl"
        self.log_path = self.log_dir / f"collector_{stamp}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            handlers=[
                logging.FileHandler(self.log_path, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.log = logging.getLogger("collector")
        self.api = None
        self.fh = None

    def connect(self):
        self.log.info("Menghubungkan ke %s:%s", self.host, self.port)
        self.api = librouteros.connect(
            host=self.host,
            username=self.user,
            password=self.password,
            port=self.port,
            timeout=10,
            ssl_wrapper=make_ssl_wrapper(self.host),
        )
        self.log.info("Terhubung (read-only)")

    def ensure_api(self):
        if self.api is None:
            self.connect()
        return self.api

    def close(self):
        if self.api is not None:
            try:
                self.api.close()
            except Exception:
                pass
            self.api = None

    def emit(self, kind, data):
        record = {
            "ts_utc": now_utc(),
            "site": self.site,
            "router": self.router,
            "kind": kind,
            "data": data,
        }
        self.fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        self.fh.flush()

    def read(self, path):
        if path not in READ_PATHS:
            raise ValueError(f"Path tidak diizinkan: {path}")
        try:
            return list(self.ensure_api()(path))
        except Exception as exc:
            self.emit("error", {"path": path, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
            self.log.warning("Gagal membaca %s: %s", path, exc)
            self.close()
            return None

    def snapshot(self, kind=None):
        for path, name in READ_PATHS.items():
            if kind and name != kind:
                continue
            rows = self.read(path)
            if rows is not None:
                self.emit(name, rows)

    def router_ping(self, interface, target):
        try:
            rows = list(self.ensure_api()(
                "/ping",
                address=target,
                count="1",
                interface=interface,
            ))
        except Exception as exc:
            self.emit("error", {"interface": interface, "target": target, "error": f"{type(exc).__name__}: {str(exc)[:160]}"})
            self.close()
            return {
                "interface": interface,
                "target": target,
                "success": False,
                "error": f"{type(exc).__name__}: {str(exc)[:160]}",
            }
        if not rows:
            return {"interface": interface, "target": target, "success": False, "error": "no response row"}
        row = rows[-1]
        sent = int(str(row.get("sent", "0")))
        received = int(str(row.get("received", "0")))
        rtt = parse_ros_duration(row.get("time") or row.get("avg-rtt") or row.get("max-rtt"))
        return {
            "interface": interface,
            "target": target,
            "success": received > 0,
            "rtt_ms": rtt,
            "packet_loss": row.get("packet-loss"),
            "sent": sent,
            "received": received,
            "raw": {k: row.get(k) for k in ("time", "min-rtt", "avg-rtt", "max-rtt")},
        }

    def probe_once(self):
        if not self.probe:
            return
        for interface in self.probe_interfaces:
            for target in self.probe_targets:
                self.emit("probe", self.router_ping(interface, target))

    def write_meta(self, duration):
        self.emit("meta", {
            "version": 1,
            "host": self.host,
            "port": self.port,
            "site": self.site,
            "router": self.router,
            "tag": self.tag,
            "probe": self.probe,
            "probe_targets": self.probe_targets,
            "probe_interfaces": self.probe_interfaces,
            "intervals": self.intervals,
            "probe_interval": self.probe_interval,
            "duration_s": duration,
            "connection_table": self.connections,
            "read_only": True,
        })

    def read_connections(self):
        try:
            rows = list(self.ensure_api()("/ip/firewall/connection/print"))
            self.emit("connection", rows)
        except Exception as exc:
            self.emit("error", {
                "path": "/ip/firewall/connection/print",
                "error": f"{type(exc).__name__}: {str(exc)[:200]}",
            })
            self.close()

    def run_once(self):
        self.write_meta(0)
        self.snapshot()
        if self.connections:
            self.read_connections()
        self.probe_once()
        self.log.info("Snapshot selesai: %s", self.out_path)

    def run_loop(self, duration):
        self.write_meta(duration)
        next_run = {name: 0.0 for name in self.intervals}
        next_run["probe"] = 0.0
        start = time.monotonic()

        while RUNNING:
            now = time.monotonic()
            if duration and now - start >= duration:
                self.log.info("Durasi tercapai, berhenti")
                break

            for name, interval in self.intervals.items():
                if now >= next_run[name]:
                    self.snapshot(name)
                    next_run[name] = now + interval

            if self.probe and now >= next_run["probe"]:
                self.probe_once()
                next_run["probe"] = now + self.probe_interval

            time.sleep(0.5)

    def close_all(self):
        self.close()
        if self.fh:
            self.fh.close()
            self.fh = None


def handle_signal(signum, frame):
    global RUNNING
    RUNNING = False


def main():
    parser = argparse.ArgumentParser(description="Kolektor baseline read-only RouterOS")
    parser.add_argument("--once", action="store_true", help="Ambil satu snapshot lalu keluar")
    parser.add_argument("--no-probe", action="store_true", help="Jangan jalankan ping")
    parser.add_argument("--connections", action="store_true", help="Baca tabel koneksi (bisa timeout)")
    parser.add_argument("--duration", default=None, help="Durasi, mis. 7d, 24h, 3600s")
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--tag", default="baseline")
    args = parser.parse_args()

    load_env(Path(__file__).with_name(".env"))
    collector = Collector(args)
    collector.fh = collector.out_path.open("a", encoding="utf-8")

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        collector.connect()
        if args.once:
            collector.run_once()
        else:
            duration = parse_duration(args.duration if args.duration is not None else env("DURATION", "0"))
            collector.run_loop(duration)
    finally:
        collector.close_all()
        print(f"Data: {collector.out_path}")
        print(f"Log : {collector.log_path}")


if __name__ == "__main__":
    main()
