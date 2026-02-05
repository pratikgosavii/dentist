"""
Push notification service (FCM or compatible).
Sends push notifications using tokens from user_token table (UserToken model).
"""
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_tokens_for_user(user):
    """Get all device tokens for user from user_token table."""
    if not user or not user.pk:
        return []
    try:
        from users.models import UserToken
        return list(UserToken.objects.filter(user=user).values_list("token", flat=True))
    except Exception as e:
        logger.warning("Could not get UserToken for user %s: %s", user.pk, e)
        return []


def send_push_notification(user, title, body, data=None):
    """
    Send push notification to user's device(s).
    Tokens are read from user_token table (UserToken model).
    Uses FCM legacy HTTP API if FCM_SERVER_KEY is set.

    Args:
        user: User model instance
        title: Notification title
        body: Notification body text
        data: Optional dict of key-value data payload

    Returns:
        bool: True if at least one push was sent, False if skipped (no tokens or no key)
    """
    tokens = _get_tokens_for_user(user)
    if not tokens:
        logger.info("[PUSH] Skipped: user_id=%s has no device tokens in user_token", user.id if user else None)
        print(f"[PUSH] Skipped: user_id={user.id if user else None} has no device tokens")
        return False

    fcm_key = getattr(settings, "FCM_SERVER_KEY", None) or getattr(settings, "FCM_LEGACY_SERVER_KEY", None)
    if not fcm_key:
        logger.info("[PUSH] Skipped: FCM_SERVER_KEY not configured")
        print("[PUSH] Skipped: FCM_SERVER_KEY not configured")
        return False

    logger.info("[PUSH] Sending to user_id=%s title=%s tokens_count=%s", user.id, title, len(tokens))
    print(f"[PUSH] Sending to user_id={user.id} | title={title} | body={body} | tokens={len(tokens)}")

    headers = {
        "Authorization": f"key={fcm_key}",
        "Content-Type": "application/json",
    }

    # FCM data payload: all values must be strings (for tap-to-open appointment)
    data_payload = {k: str(v) for k, v in (data or {}).items()}

    sent = False
    for token in tokens:
        payload = {
            "to": token,
            "notification": {"title": title, "body": body},
            "data": data_payload,
        }
        try:
            print(f"[PUSH] FCM request for user_id={user.id} token_preview={token[:20]}...")
            response = requests.post(
                "https://fcm.googleapis.com/fcm/send",
                json=payload,
                headers=headers,
                timeout=10,
            )
            if response.status_code == 200:
                logger.info("Push sent to user %s (token)", user.id)
                print(f"[PUSH] Sent OK to user_id={user.id}")
                sent = True
            else:
                logger.warning("FCM returned %s: %s", response.status_code, response.text)
                print(f"[PUSH] FCM error status={response.status_code} body={response.text[:200]}")
        except Exception as e:
            logger.exception("Push notification failed: %s", e)
            print(f"[PUSH] Exception: {e}")

    return sent
