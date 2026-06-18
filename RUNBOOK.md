# Incident Response Runbook

## High CPU Alert

### Symptoms
- CPU usage exceeds 80%
- Monitoring script generates alert

### Investigation
```bash
top
ps aux --sort=-%cpu | head
```

### Action
- Identify high CPU process
- Record PID
- Restart service if required

---

## High Disk Usage Alert

### Investigation
```bash
df -h
du -sh /*
```

### Action
- Identify large directories
- Remove unnecessary files
- Verify available disk space

---

## Backup Failure

### Investigation
```bash
cat /var/log/backup.log
```

### Action
- Check backup logs
- Verify destination path
- Ensure sufficient disk space

---

## Escalation

Document findings in:

- alerts.log
- backup.log

Include:
- Timestamp
- Hostname
- Alert Type
- Resolution Steps
