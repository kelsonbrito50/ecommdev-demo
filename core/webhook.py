"""
GitHub Webhook for automatic deployment
"""
import hashlib
import hmac
import logging
import os
import subprocess

from decouple import config
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def github_webhook(request):
    """Handle GitHub webhook for auto-deployment with HMAC signature verification."""

    # 1. Read secret from environment via decouple
    secret = config('GITHUB_WEBHOOK_SECRET', default=None)

    if not secret:
        logger.error("GITHUB_WEBHOOK_SECRET not configured — webhook disabled")
        return HttpResponseForbidden('Webhook not configured')

    # 2. Verify X-Hub-Signature-256 header
    signature_header = request.headers.get('X-Hub-Signature-256', '')
    if not signature_header:
        logger.warning(
            "Missing X-Hub-Signature-256 header from IP: %s",
            request.META.get('REMOTE_ADDR'),
        )
        return HttpResponseForbidden('Missing signature')

    # 3. Compute expected HMAC-SHA256 signature
    expected_signature = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        request.body,
        hashlib.sha256,
    ).hexdigest()

    # 4. Constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(signature_header, expected_signature):
        logger.warning(
            "Invalid webhook signature from IP: %s",
            request.META.get('REMOTE_ADDR'),
        )
        return HttpResponseForbidden('Invalid signature')

    # 5. Signature verified — proceed with deployment
    deploy_script = config('DEPLOY_SCRIPT_PATH', default='./deploy.sh')
    try:
        result = subprocess.run(
            [deploy_script],
            capture_output=True,
            text=True,
            timeout=120,
        )
        logger.info("Deploy completed. stdout: %s", result.stdout)
        if result.returncode != 0:
            logger.error("Deploy script error. stderr: %s", result.stderr)
            return HttpResponse('Deploy error', status=500)
        return HttpResponse('OK', status=200)
    except subprocess.TimeoutExpired:
        logger.error("Deploy script timed out after 120s")
        return HttpResponse('Deploy timed out', status=500)
    except Exception as exc:
        logger.error("Deploy failed: %s", str(exc))
        return HttpResponse('Error', status=500)
