"""
GitHub Webhook for automatic deployment
"""
import subprocess
import hmac
import hashlib
import logging
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def github_webhook(request):
    """Handle GitHub webhook for auto-deployment"""

    secret = getattr(settings, 'GITHUB_WEBHOOK_SECRET', None)

    # SECURITY: Require secret in production
    if not secret:
        if not settings.DEBUG:
            logger.error("GitHub webhook called but GITHUB_WEBHOOK_SECRET not configured")
            return HttpResponseForbidden('Webhook not configured')
        logger.warning("GITHUB_WEBHOOK_SECRET not set - skipping verification (DEBUG mode)")
    else:
        # Verify webhook signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not signature:
            logger.warning(f"Missing signature from IP: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden('Missing signature')

        expected = 'sha256=' + hmac.new(
            secret.encode(),
            request.body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            logger.warning(f"Invalid signature from IP: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden('Invalid signature')

    # Run deploy script
    try:
        result = subprocess.run(
            ['/home/MrDev02/deploy.sh'],
            capture_output=True,
            text=True,
            timeout=120
        )
        logger.info(f"Deploy completed successfully")
        return HttpResponse(f'Deployed!\n{result.stdout}', status=200)
    except Exception as e:
        logger.error(f"Deploy failed: {str(e)}")
        return HttpResponse(f'Deploy failed: {str(e)}', status=500)
