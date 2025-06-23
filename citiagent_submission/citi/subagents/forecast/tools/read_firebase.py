import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from ...monitor.tools.get_cred import get_firestore_cred
import logging

def read_firebase_variables(station_name: str) -> dict:
    try:
        if not firebase_admin._apps:
            cred_data = get_firestore_cred()
            cred = credentials.Certificate(cred_data)
            firebase_admin.initialize_app(cred)
            logging.info("✅ Firebase initialized successfully")
        else:
            logging.info("ℹ️ Firebase already initialized")

        db = firestore.client()

        stations_doc = db.collection('stations_reports').document('latest').get()
        weather_doc = db.collection('weather_reports').document('latest').get()

        if not stations_doc.exists or not weather_doc.exists:
            return {"error": "Missing data in Firebase."}

        stations_data = stations_doc.to_dict()["data"]["report"]["stations"]
        station = next((s for s in stations_data if s["name"] == station_name), None)
        if not station:
            return {"error": f"Station '{station_name}' not found."}

        lat = station["lat"]
        lon = station["lon"]

        weather_data = weather_doc.to_dict()["data"]["report"]["weather"]
        temperature_c = weather_data.get("temperature_c")
        temperature_f = (
            round((temperature_c * 9 / 5) + 32, 1)
            if isinstance(temperature_c, (int, float))
            else None
        )

        return {
            "name": station_name,
            "lat": lat,
            "lon": lon,
            "temperature": temperature_f or 0.0,
            "condition": weather_data.get("condition", "Unknown"),
            "wind": weather_data.get("wind_speed_mps", 0.0),
            "humidity": weather_data.get("humidity_percent", 0),
            "bikes": station.get("num_bikes_available", 0),
            "docks": station.get("num_docks_available", 0),
            "flag": station.get("availability_flag", "normal"),
        }

    except Exception as e:
        logging.error("❌ Failed to read Firebase variables", exc_info=True)
        return {"error": str(e)}