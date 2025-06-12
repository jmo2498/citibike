from google.cloud import secretmanager
import json

def get_db_config():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/vertextraining-448821/secrets/sql_creds/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    return json.loads(response.payload.data.decode("utf-8"))