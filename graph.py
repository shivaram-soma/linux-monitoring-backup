#!/usr/bin/env python3
"""Visualize CPU/memory trends from health_log.csv with matplotlib."""

import csv
from datetime import datetime

import matplotlib
matplotlib.use("Agg")  # no display needed — works on headless servers
import matplotlib.pyplot as plt

ts, cpu, mem = [], [], []
with open("health_log.csv") as f:
    for row in csv.DictReader(f):
        ts.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
        cpu.append(float(row["cpu_percent"]))
        mem.append(float(row["mem_percent"]))

plt.figure(figsize=(12, 5))
plt.plot(ts, cpu, label="CPU %", linewidth=1.5)
plt.plot(ts, mem, label="Memory %", linewidth=1.5)
plt.axhline(y=80, linestyle="--", alpha=0.5, color="red", label="Threshold 80%")
plt.xlabel("Time"); plt.ylabel("Usage %"); plt.title("CPU & Memory Trends")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig("trends.png", dpi=120)
print("Saved trends.png")
