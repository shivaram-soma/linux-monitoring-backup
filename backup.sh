#!/bin/bash
# Backup automation — timestamped .tar.gz archives, rotates older backups
# into an archive/ folder (matches resume), logs pass/fail status.

set -euo pipefail

SOURCE_DIR="${1:-$HOME/Documents}"
BACKUP_DIR="${2:-$HOME/backups}"
ARCHIVE_DIR="$BACKUP_DIR/archive"
KEEP_RECENT=5          # newest N stay in BACKUP_DIR; older move to archive/
LOG_FILE="$BACKUP_DIR/backup.log"

ts() { date "+%Y-%m-%d %H:%M:%S"; }
log() { echo "$(ts) $1" | tee -a "$LOG_FILE"; }

mkdir -p "$BACKUP_DIR" "$ARCHIVE_DIR"

if [ ! -d "$SOURCE_DIR" ]; then
    log "FAIL: source $SOURCE_DIR does not exist"
    exit 1
fi

NAME="backup_$(basename "$SOURCE_DIR")_$(date +%Y%m%d_%H%M%S).tar.gz"

if tar -czf "$BACKUP_DIR/$NAME" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"; then
    log "PASS: created $NAME ($(du -h "$BACKUP_DIR/$NAME" | cut -f1))"
else
    log "FAIL: tar exited non-zero for $SOURCE_DIR"
    exit 1
fi

# Rotation: move backups beyond the newest KEEP_RECENT into archive/
COUNT=$(ls -1 "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null | wc -l)
if [ "$COUNT" -gt "$KEEP_RECENT" ]; then
    ls -1t "$BACKUP_DIR"/backup_*.tar.gz | tail -n +$((KEEP_RECENT + 1)) | while read -r OLD; do
        mv "$OLD" "$ARCHIVE_DIR/"
        log "ROTATED: $(basename "$OLD") -> archive/"
    done
fi

log "DONE: $(ls -1 "$BACKUP_DIR"/backup_*.tar.gz | wc -l) recent, $(ls -1 "$ARCHIVE_DIR" 2>/dev/null | wc -l) archived"
