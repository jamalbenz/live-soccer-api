from flask import Flask, jsonify
import json
import os
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"success": True, "message": "API working"})

@app.route("/matches")
def matches():
    if not os.path.exists("matches.json"):
        return jsonify({"success": False, "matches": [], "message": "No cached matches yet"})

    with open("matches.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

@app.route("/refresh")
def refresh():
    try:
        subprocess.run(
            [sys.executable, "flashscore_scraper.py"],
            timeout=180,
            check=False
        )

        if not os.path.exists("matches.json"):
            return jsonify({"success": False, "matches": [], "message": "Refresh failed"})

        with open("matches.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        return jsonify({"success": True, "message": "Matches refreshed", "data": data})

    except Exception as e:
        return jsonify({"success": False, "matches": [], "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)