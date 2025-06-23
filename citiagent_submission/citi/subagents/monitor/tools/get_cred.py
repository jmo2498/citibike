import json
import logging
from google.cloud import secretmanager

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_db_config():
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = "projects/vertextraining-448821/secrets/sql_creds/versions/latest"
        logging.info(f"🔐 Accessing secret: {secret_name}")
        response = client.access_secret_version(request={"name": secret_name})
        secret_data = response.payload.data.decode("utf-8")
        logging.info("✅ Successfully accessed DB secret")
        return json.loads(secret_data)
    except Exception as e:
        logging.error("❌ Failed to retrieve database credentials:", exc_info=True)
        raise

def get_firestore_cred():
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = "projects/vertextraining-448821/secrets/firestore_cred/versions/latest"
        logging.info(f"🔐 Accessing secret: {secret_name}")
        response = client.access_secret_version(request={"name": secret_name})
        secret_data = response.payload.data.decode("utf-8")
        logging.info("✅ Successfully accessed Firestore secret")
        return json.loads(secret_data)
    except Exception as e:
        logging.error("❌ Failed to retrieve Firestore credentials:", exc_info=True)
        raise