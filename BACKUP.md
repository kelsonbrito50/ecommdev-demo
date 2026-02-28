# Database Backup & Restore — ECOMMDEV

This document describes the procedures for backing up and restoring the ECOMMDEV PostgreSQL database.

---

## Table of Contents

- [Backup Strategy](#backup-strategy)
- [Manual Backup](#manual-backup)
- [Automated Backup](#automated-backup)
- [Restore Procedure](#restore-procedure)
- [Docker-based Backup](#docker-based-backup)
- [Verification](#verification)
- [Off-site Storage](#off-site-storage)

---

## Backup Strategy

| Type | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Full dump (SQL) | Daily | 30 days | `/backups/daily/` |
| Weekly snapshot | Weekly | 12 weeks | `/backups/weekly/` |
| Pre-deploy backup | On every deploy | 10 versions | `/backups/deploys/` |
| Media files | Weekly | 4 weeks | `/backups/media/` |

---

## Manual Backup

### PostgreSQL Full Dump

```bash
# Standard pg_dump (plain SQL format — human-readable)
pg_dump \
  -h $DB_HOST \
  -p $DB_PORT \
  -U $DB_USER \
  -d $DB_NAME \
  --no-password \
  --format=plain \
  --verbose \
  --file=ecommdev_$(date +%Y%m%d_%H%M%S).sql

# Custom format (smaller, parallel restore support)
pg_dump \
  -h $DB_HOST \
  -U $DB_USER \
  -d $DB_NAME \
  --format=custom \
  --file=ecommdev_$(date +%Y%m%d_%H%M%S).dump
```

### Media Files

```bash
# Compress and archive media directory
tar -czf media_$(date +%Y%m%d_%H%M%S).tar.gz /app/media/
```

### Django Data Export (JSON fixtures)

```bash
# Export all data
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude auth.permission \
  --exclude contenttypes \
  --indent 2 \
  > fixtures/backup_$(date +%Y%m%d).json

# Export specific app
python manage.py dumpdata core --indent 2 > fixtures/core_backup.json
```

---

## Automated Backup

Add the following cron jobs to the server:

```bash
# Edit crontab
crontab -e
```

```cron
# Daily database backup at 2:00 AM
0 2 * * * /opt/ecommdev/scripts/backup_db.sh >> /var/log/ecommdev_backup.log 2>&1

# Weekly media backup on Sundays at 3:00 AM
0 3 * * 0 /opt/ecommdev/scripts/backup_media.sh >> /var/log/ecommdev_backup.log 2>&1
```

### Backup Script (`scripts/backup_db.sh`)

```bash
#!/bin/bash
set -euo pipefail

source /opt/ecommdev/.env

BACKUP_DIR="/backups/daily"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/ecommdev_$DATE.dump"

mkdir -p "$BACKUP_DIR"

PGPASSWORD="$DB_PASSWORD" pg_dump \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  --format=custom \
  --file="$BACKUP_FILE"

echo "[$(date)] Backup created: $BACKUP_FILE ($(du -sh $BACKUP_FILE | cut -f1))"

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "*.dump" -mtime +30 -delete
echo "[$(date)] Old backups cleaned."
```

---

## Restore Procedure

> ⚠️ **Warning:** Restoring overwrites all current data. Always verify you have a working backup before proceeding.

### Step 1: Confirm Backup Integrity

```bash
# List available backups
ls -lh /backups/daily/

# Verify the dump file is valid
pg_restore --list ecommdev_20260101_020000.dump | head -20
```

### Step 2: Stop Application (prevent writes during restore)

```bash
# With Docker
docker compose stop web celery celery-beat

# Or without Docker
sudo systemctl stop gunicorn
```

### Step 3: Drop and Recreate the Database

```bash
# Connect as postgres superuser
psql -h $DB_HOST -U postgres

-- Drop existing database
DROP DATABASE ecommdev;

-- Recreate
CREATE DATABASE ecommdev OWNER ecommdev_user;

\q
```

### Step 4: Restore the Dump

```bash
# Restore from custom format dump
PGPASSWORD=$DB_PASSWORD pg_restore \
  -h $DB_HOST \
  -p $DB_PORT \
  -U $DB_USER \
  -d $DB_NAME \
  --no-owner \
  --role=$DB_USER \
  --verbose \
  ecommdev_20260101_020000.dump

# Restore from plain SQL dump
PGPASSWORD=$DB_PASSWORD psql \
  -h $DB_HOST \
  -U $DB_USER \
  -d $DB_NAME \
  < ecommdev_20260101_020000.sql
```

### Step 5: Run Django Migrations (if needed)

```bash
python manage.py migrate --run-syncdb
```

### Step 6: Restore Media Files (if applicable)

```bash
tar -xzf media_20260101_030000.tar.gz -C /
```

### Step 7: Restart Application

```bash
# With Docker
docker compose up -d

# Without Docker
sudo systemctl start gunicorn
```

### Step 8: Verify Restore

```bash
# Check app health
curl http://localhost:8000/api/v1/health/

# Check Django can connect to DB
python manage.py dbshell -c "\dt" | head
```

---

## Docker-based Backup

When running with Docker Compose:

```bash
# Backup directly from the db container
docker compose exec db pg_dump \
  -U $DB_USER \
  -d $DB_NAME \
  --format=custom \
  > ecommdev_$(date +%Y%m%d).dump

# Restore into the db container
cat ecommdev_20260101.dump | docker compose exec -T db pg_restore \
  -U $DB_USER \
  -d $DB_NAME \
  --no-owner \
  --clean

# Backup media volume
docker run --rm \
  -v ecommdev_media_volume:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/media_$(date +%Y%m%d).tar.gz /data
```

---

## Verification

After any backup, verify it can be restored:

```bash
# Create a test database
psql -U postgres -c "CREATE DATABASE ecommdev_verify;"

# Restore the backup into it
pg_restore \
  -U postgres \
  -d ecommdev_verify \
  --no-owner \
  ecommdev_YYYYMMDD.dump

# Check row counts match
psql -U postgres -d ecommdev_verify \
  -c "SELECT schemaname, tablename, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 10;"

# Drop test database
psql -U postgres -c "DROP DATABASE ecommdev_verify;"
```

---

## Off-site Storage

Copy backups to S3 or another remote location:

```bash
# Upload to S3
aws s3 cp ecommdev_$(date +%Y%m%d).dump \
  s3://ecommdev-backups/db/$(date +%Y/%m)/

# Sync entire backup directory
aws s3 sync /backups/daily/ s3://ecommdev-backups/db/ \
  --exclude "*" \
  --include "*.dump"
```

> Configure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your environment for S3 access.

---

## Point-in-Time Recovery (Advanced)

For production, enable WAL archiving in PostgreSQL for point-in-time recovery (PITR):

```sql
-- postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backups/wal/%f'
```

Consult the [PostgreSQL PITR documentation](https://www.postgresql.org/docs/current/continuous-archiving.html) for full setup.
