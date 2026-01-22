#!/bin/bash
cd /home/mrdev02/Documents/ECOMM_DEV
rsync -avz --progress \
  --exclude='venv/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='db.sqlite3' \
  --exclude='media/' \
  --exclude='staticfiles/' \
  --exclude='logs/' \
  --exclude='.env' \
  --exclude='*.zip' \
  --exclude='*.sh' \
  ./ MrDev02@ssh.pythonanywhere.com:/home/MrDev02/ecommdev/
