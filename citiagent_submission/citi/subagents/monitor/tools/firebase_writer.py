import firebase_admin
from firebase_admin import credentials, firestore
from google.api_core.retry import Retry
import os
from datetime import datetime
import traceback
import json
from .get_cred import get_firestore_cred


# One-time Firebase initialization
try:
    # Get credentials as a dictionary
    cred_dict = get_firestore_cred()
    cred = credentials.Certificate(cred_dict)
    
    # Initialize Firebase with credentials only once
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized successfully")
        
except Exception as e:
    print(f"❌ Failed to initialize Firebase: {e}")
    print("Traceback:")
    traceback.print_exc()
    raise

# Optionally support the Firestore emulator
if os.getenv("FIRESTORE_EMULATOR_HOST"):
    print("🔌 Using Firestore emulator at", os.environ["FIRESTORE_EMULATOR_HOST"])

db = firestore.client()

# Configure a reasonable retry policy
FIRESTORE_RETRY = Retry(
    initial=1.0,
    maximum=10.0,
    multiplier=2.0,
    deadline=30.0
)
def write_monitor_report(header: str, data: dict) -> dict:
    """
    Stores `data` under the Firestore collection `<header>_reports`, document `latest`.
    Overwrites the previous report each time.
    """
    valid = ("stations", "weather")
    if header not in valid:
        raise ValueError(f"Invalid header {header!r}. Must be one of {valid}.")

    coll = f"{header}_reports"
    doc_id = "latest"  # fixed doc ID to always overwrite

    try:
        print(f"📤 Writing to Firestore collection `{coll}`, doc `{doc_id}`:")
        print(json.dumps(data, indent=2))

        doc_ref = db.collection(coll).document(doc_id)

        payload = {
            "type": header,
            "data": data,
            "created_at": firestore.SERVER_TIMESTAMP
        }

        doc_ref.set(payload, merge=False, retry=FIRESTORE_RETRY)

        print(f"✅ [SUCCESS] Overwrote `{coll}` doc={doc_id}")
        return {
            "status": "success",
            "collection": coll,
            "doc_id": doc_id,
        }

    except Exception as e:
        print(f"❌ [ERROR] Failed writing to `{coll}`:")
        traceback.print_exc()
        return {
            "status": "error",
            "collection": coll,
            "error_message": str(e)
        }