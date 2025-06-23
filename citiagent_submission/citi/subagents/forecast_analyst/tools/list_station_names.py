import logging
from firebase_admin import firestore, credentials
import firebase_admin
from ...monitor.tools.get_cred import get_firestore_cred

logger = logging.getLogger(__name__)

def list_station_names() -> list[str]:
    try:
        if not firebase_admin._apps:
            cred_data = get_firestore_cred()
            cred = credentials.Certificate(cred_data)
            firebase_admin.initialize_app(cred)
            logger.info("✅ Firebase initialized successfully")
        else:
            logger.debug("ℹ️ Firebase already initialized")

        db = firestore.client()
        doc = db.collection("stations_reports").document("latest").get()
        if not doc.exists:
            raise ValueError("⚠️ No 'latest' document in 'stations_reports'.")

        stations_data = doc.to_dict()["data"]["report"]["stations"]
        return [station["name"] for station in stations_data]

    except Exception as e:
        logger.error("❌ Error in list_station_names", exc_info=True)
        return []