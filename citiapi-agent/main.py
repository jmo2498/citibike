from flask import Flask, request, jsonify
import requests as r
import json
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# === CONFIG ===
APP_URL = "https://adk-default-service-name-779352444610.us-central1.run.app"
APP_NAME = "citi"
USER_ID = "user_123"
SESSION_ID = "session_abc"

# === Get Identity Token at Startup ===
print("🔐 Getting ID token...")
TOKEN = subprocess.check_output(["gcloud", "auth", "print-identity-token"]).decode().strip()
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# === Create Session at Startup ===
print("📦 Creating session...")
session_url = f"{APP_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
session_payload = {
    "state": {
        "preferred_language": "English",
        "visit_count": 5
    }
}
r.post(session_url, headers=HEADERS, json=session_payload)

# === API Endpoint ===
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    prompt = data["message"]
    payload = {
        "app_name": APP_NAME,
        "user_id": USER_ID,
        "session_id": SESSION_ID,
        "new_message": {
            "role": "user",
            "parts": [{"text": prompt}]
        },
        "streaming": False
    }

    response = r.post(f"{APP_URL}/run_sse", headers=HEADERS, json=payload, stream=True)

    result = {"response": "", "function_call": None}

    for line in response.iter_lines():
        if line and line.startswith(b"data: "):
            data = json.loads(line[6:])
            parts = data.get("content", {}).get("parts", [])

            for part in parts:
                if "text" in part:
                    result["response"] += part["text"]
                elif "functionCall" in part:
                    result["function_call"] = part["functionCall"]
                elif "functionResponse" in part:
                    result["response"] += part["functionResponse"].get("response", {}).get("result", "")

    if result["response"]:
        return jsonify({"response": result["response"]})
    elif result["function_call"]:
        return jsonify(result)
    else:
        return jsonify({"error": "No valid response from agent"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
