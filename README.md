# Linux System Monitor & Backup Automation

![Python](https://img.shields.io/badge/python-3.8+-blue?logo=python)
![CI](https://github.com/shivaram-soma/linux-monitoring-backup/actions/workflows/ci.yml/badge.svg)
![Shell](https://img.shields.io/badge/shell-bash-green?logo=gnubash)

A Linux DevOps toolkit for system observability and data protection:
- **monitor.py** — samples CPU, memory, and disk every 60 seconds, logs to CSV, and alerts on threshold breaches
- **graph.py** — generates a matplotlib trend chart from the CSV log (headless, works on servers)
- **backup.sh** — timestamped tar.gz archives with rotation: keeps N recent copies locally, moves older ones to `archive/`

## Demo

```
[2025-06-13 10:00:00] CPU 12.5% | MEM 43.2% | DISK 61.0%
[2025-06-13 10:01:00] CPU 88.4% | MEM 43.3% | DISK 61.0%
[2025-06-13 10:01:00] WARNING: HIGH CPU 88.4% (>80%)
```

Alert log (`alerts.log`):
```
[2025-06-13 10:01:00] WARNING: HIGH CPU 88.4% (>80%)
```

## Quick Start

```bash
git clone https://github.com/shivaram-soma/linux-monitoring-backup.git
cd linux-monitoring-backup
pip install -r requirements.txt

# Single sample
python3 monitor.py

# Continuous monitoring (every 60s)
python3 monitor.py --loop

# Generate trend chart from log data
python3 graph.py
# → saves trends.png

# Backup ~/Documents
bash backup.sh ~/Documents ~/backups
```

## Scheduling with Cron

```bash
# Sample every minute
* * * * * /usr/bin/python3 /path/to/monitor.py >> /var/log/monitor.log 2>&1

# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh /home/shiva/Documents /home/shiva/backups >> /var/log/backup.log 2>&1
```

## Run as a systemd Service (continuous monitoring)

```bash
sudo cp linux-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now linux-monitor
sudo systemctl status linux-monitor
journalctl -u linux-monitor -f
```

See [linux-monitor.service](./linux-monitor.service) in this repo.

## Thresholds (configurable at top of monitor.py)

| Metric | Alert Threshold |
|--------|----------------|
| CPU | > 80% |
| Memory | > 80% |
| Disk | > 85% |

## Project Structure

```
linux-monitoring-backup/
├── monitor.py              # System metrics collector (psutil)
├── graph.py                # CSV → matplotlib trend chart
├── backup.sh               # Timestamped backups with rotation
├── requirements.txt        # psutil, matplotlib
├── linux-monitor.service   # systemd unit file
├── .env.example
├── .gitignore
├── Dockerfile              # For containerized monitoring
├── docker-compose.yml      # Run monitor as a container
├── DEPLOYMENT.md
└── .github/
    └── workflows/
        └── ci.yml          # Test + lint on push
```

## Docker (Containerized Monitoring)

```bash
docker compose up -d
docker logs -f linux-monitor
```

The container mounts `/proc` and `/sys` from the host so `psutil` reads real host metrics.

## Output Files

| File | Description |
|------|-------------|
| `health_log.csv` | Timestamped metric samples |
| `alerts.log` | Threshold breach warnings |
| `trends.png` | CPU & memory trend chart |
| `backups/backup_*.tar.gz` | Recent backup archives |
| `backups/archive/` | Rotated older backups |
