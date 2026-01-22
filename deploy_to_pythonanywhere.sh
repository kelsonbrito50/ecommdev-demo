#!/bin/bash
# Deploy security updates to PythonAnywhere
# Run this script manually: ./deploy_to_pythonanywhere.sh

set -e

SERVER="MrDev02@ssh.pythonanywhere.com"
REMOTE_DIR="/home/MrDev02/ecommdev"
LOCAL_DIR="/home/mrdev02/Documents/ECOMM_DEV"

echo "=========================================="
echo "Deploying Security Updates to PythonAnywhere"
echo "=========================================="

# Step 1: Create remote directories if they don't exist
echo ""
echo "[1/5] Creating remote directories..."
ssh $SERVER "mkdir -p $REMOTE_DIR/core/templatetags"

# Step 2: Upload files using rsync
echo ""
echo "[2/5] Uploading files..."

# Upload settings and main files
rsync -avz --progress \
  $LOCAL_DIR/ecommdev/settings.py \
  $SERVER:$REMOTE_DIR/ecommdev/

rsync -avz --progress \
  $LOCAL_DIR/faturas/views.py \
  $SERVER:$REMOTE_DIR/faturas/

rsync -avz --progress \
  $LOCAL_DIR/requirements.txt \
  $SERVER:$REMOTE_DIR/

# Upload new security files
rsync -avz --progress \
  $LOCAL_DIR/core/validators.py \
  $LOCAL_DIR/core/models.py \
  $SERVER:$REMOTE_DIR/core/

rsync -avz --progress \
  $LOCAL_DIR/core/templatetags/ \
  $SERVER:$REMOTE_DIR/core/templatetags/

# Upload model files with validators
rsync -avz --progress \
  $LOCAL_DIR/clientes/models.py \
  $SERVER:$REMOTE_DIR/clientes/

rsync -avz --progress \
  $LOCAL_DIR/projetos/models.py \
  $SERVER:$REMOTE_DIR/projetos/

rsync -avz --progress \
  $LOCAL_DIR/blog/models.py \
  $SERVER:$REMOTE_DIR/blog/

rsync -avz --progress \
  $LOCAL_DIR/portfolio/models.py \
  $SERVER:$REMOTE_DIR/portfolio/

rsync -avz --progress \
  $LOCAL_DIR/servicos/models.py \
  $SERVER:$REMOTE_DIR/servicos/

# Upload templates with XSS fixes
rsync -avz --progress \
  $LOCAL_DIR/templates/blog/detalhe.html \
  $SERVER:$REMOTE_DIR/templates/blog/

rsync -avz --progress \
  $LOCAL_DIR/templates/servicos/detalhe.html \
  $SERVER:$REMOTE_DIR/templates/servicos/

rsync -avz --progress \
  $LOCAL_DIR/templates/portfolio/detalhe.html \
  $SERVER:$REMOTE_DIR/templates/portfolio/

# Step 3: Install dependencies
echo ""
echo "[3/5] Installing dependencies..."
ssh $SERVER "cd $REMOTE_DIR && pip install --user -r requirements.txt"

# Step 4: Run migrations
echo ""
echo "[4/5] Running migrations..."
ssh $SERVER "cd $REMOTE_DIR && python manage.py migrate"

# Step 5: Check deployment
echo ""
echo "[5/5] Running security checks..."
ssh $SERVER "cd $REMOTE_DIR && python manage.py check"

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
echo ""
echo "IMPORTANT: Now reload your web app at:"
echo "https://www.pythonanywhere.com/user/MrDev02/webapps/"
echo ""
echo "Also update your .env file with:"
echo "  MERCADOPAGO_WEBHOOK_SECRET=your-secret-here"
echo "  DEBUG=False"
