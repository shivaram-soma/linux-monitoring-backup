#!/usr/bin/env python3
"""
Linux System Monitor — samples CPU, memory, and disk every 60s (matches resume),
logs to CSV, warns when thresholds are crossed.

Run continuously:   python3 monitor.py --loop
Single sample:      python3 monitor.py        (for cron-based scheduling instead)
"""

import argparse
import csv
import os
import time
from datetime import datetime

import psutil

CPU_THRESHOLD = 80
MEM_THRESHOLD = 80
DISK_THRESHOLD = 85
SAMPLE_INTERVAL = 60  # seconds — matches resume: "samples every 60s"
LOG_FILE = "health_log.csv"
ALERT_FILE = "alerts.log"


def collect():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "mem_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }


def log_csv(m):
    new_file = not os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=m.keys())
        if new_file:
            w.writeheader()
        w.writerow(m)


def check_thresholds(m):
    warnings = []
    if m["cpu_percent"] > CPU_THRESHOLD:
        warnings.append(f"HIGH CPU {m['cpu_percent']}% (>{CPU_THRESHOLD}%)")
    if m["mem_percent"] > MEM_THRESHOLD:
        warnings.append(f"HIGH MEMORY {m['mem_percent']}% (>{MEM_THRESHOLD}%)")
    if m["disk_percent"] > DISK_THRESHOLD:
        warnings.append(f"HIGH DISK {m['disk_percent']}% (>{DISK_THRESHOLD}%)")
    for w in warnings:
        line = f"[{m['timestamp']}] WARNING: {w}"
        print(line)
        with open(ALERT_FILE, "a") as f:
            f.write(line + "\n")


def sample_once():
    m = collect()
    log_csv(m)
    check_thresholds(m)
    print(
        f"[{m['timestamp']}] "
        f"CPU {m['cpu_percent']}% | "
        f"MEM {m['mem_percent']}% | "
        f"DISK {m['disk_percent']}% "
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true", help="sample every 60s forever")
    args = parser.parse_args()

    if args.loop:
        print(f"Monitoring every {SAMPLE_INTERVAL}s — Ctrl+C to stop")
        while True:
            sample_once()
            time.sleep(SAMPLE_INTERVAL - 1)  # -1 compensates for cpu_percent's 1s interval
    else:
        sample_once()
