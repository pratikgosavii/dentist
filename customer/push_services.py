"""
Push notification service (FCM).
Uses Firebase Admin SDK (firebase_key.json) when available, else FCM legacy API (FCM_SERVER_KEY).
"""
import logging
import os
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


def _send_via_firebase_admin(user, tokens, title, body, data_payload):
    """Send via Firebase Admin SDK messaging. Returns True if at least one sent."""
    try:
        from dentist.firebase_config import initialize_firebase
        if not initialize_firebase():
            return False
        import firebase_admin
        from firebase_admin import messaging
        firebase_admin.get_app()
    except Exception as e:
        logger.warning("Firebase Admin not available: %s", e)
        return False

    sent = False
    for device_token in tokens:
        try:
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data=data_payload or {},
                token=device_token,
            )
            messaging.send(message)
            sent = True
        except Exception as e:
            logger.warning("FCM send failed for token: %s", e)
    return sent


def _send_legacy(user, tokens, title, body, data_payload):
    """Send via FCM legacy API (FCM_SERVER_KEY). Returns True if at least one sent."""
    fcm_key = getattr(settings, "FCM_SERVER_KEY", None) or getattr(settings, "FCM_LEGACY_SERVER_KEY", None)
    if not fcm_key:
        return False
    headers = {"Authorization": f"key={fcm_key}", "Content-Type": "application/json"}
    sent = False
    for token in tokens:
        payload = {"to": token, "notification": {"title": title, "body": body}, "data": data_payload}
        try:
            response = requests.post("https://fcm.googleapis.com/fcm/send", json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                sent = True
            else:
                logger.warning("FCM legacy returned %s: %s", response.status_code, response.text[:200])
        except Exception as e:
            logger.exception("Push (legacy) failed: %s", e)
    return sent


def send_push_notification(user, title, body, data=None):
    """
    Send push notification to user's device(s).
    Prefers Firebase Admin SDK (firebase_key.json); falls back to FCM_SERVER_KEY (legacy).
    """
    tokens = _get_tokens_for_user(user)
    if not tokens:
        logger.info("[PUSH] Skipped: user_id=%s has no device tokens in user_token", user.id if user else None)
        print(f"[PUSH] Skipped: user_id={user.id if user else None} has no device tokens")
        return False

    firebase_key_path = getattr(settings, "FCM_SERVICE_ACCOUNT_FILE", None) or os.path.join(settings.BASE_DIR, "dentist", "firebase_key.json")
    use_firebase_admin = firebase_key_path and os.path.isfile(firebase_key_path)
    use_legacy = getattr(settings, "FCM_SERVER_KEY", None) or getattr(settings, "FCM_LEGACY_SERVER_KEY", None)

    if not use_firebase_admin and not use_legacy:
        logger.info("[PUSH] Skipped: no firebase_key.json and no FCM_SERVER_KEY")
        print("[PUSH] Skipped: no firebase_key.json and no FCM_SERVER_KEY")
        return False

    logger.info("[PUSH] Sending to user_id=%s title=%s tokens_count=%s", user.id, title, len(tokens))
    print(f"[PUSH] Sending to user_id={user.id} | title={title} | body={body} | tokens={len(tokens)}")

    data_payload = {k: str(v) for k, v in (data or {}).items()}

    sent = False
    if use_firebase_admin:
        sent = _send_via_firebase_admin(user, tokens, title, body, data_payload)
    if not sent and use_legacy:
        sent = _send_legacy(user, tokens, title, body, data_payload)

    if sent:
        logger.info("Push sent to user %s", user.id)
        print(f"[PUSH] Sent OK to user_id={user.id}")
    return sent
