# Firebase Admin SDK setup (same pattern as your other project)
import os
from django.conf import settings

# Path to service account JSON (dentist/firebase_key.json in project root)
firebase_key_path = getattr(
    settings,
    "FCM_SERVICE_ACCOUNT_FILE",
    os.path.join(settings.BASE_DIR, "dentist", "firebase_key.json"),
)

_firebase_initialized = False


def initialize_firebase():
    """Initialize Firebase Admin SDK once. Safe to call multiple times."""
    global _firebase_initialized
    if _firebase_initialized:
        return True
    if not os.path.isfile(firebase_key_path):
        return False
    try:
        import firebase_admin
        from firebase_admin import credentials
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        return True
    except Exception:
        return False
