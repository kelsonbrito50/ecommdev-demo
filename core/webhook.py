"""
GitHub Webhook for automatic deployment
"""
import subprocess
import hmac
import hashlib
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings


@csrf_exempt
@require_POST
def github_webhook(request):
    """Handle GitHub webhook for auto-deployment"""

    # Verify webhook secret (optional but recommended)
    secret = getattr(settings, 'GITHUB_WEBHOOK_SECRET', None)

    if secret:
        signature = request.headers.get('X-Hub-Signature-256', '')
        if signature:
            expected = 'sha256=' + hmac.new(
                secret.encode(),
                request.body,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected):
                return HttpResponseForbidden('Invalid signature')

    # Run deploy script
    try:
        result = subprocess.run(
            ['/home/MrDev02/deploy.sh'],
            capture_output=True,
            text=True,
            timeout=120
        )
        return HttpResponse(f'Deployed!\n{result.stdout}', status=200)
    except Exception as e:
        return HttpResponse(f'Deploy failed: {str(e)}', status=500)
