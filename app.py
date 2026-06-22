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
    try:
        subprocess.run(
            [sys.executable, "flashscore_scraper.py"],
            timeout=180,
            check=False
        )

        if not os.path.exists("matches.json"):
            return jsonify({
                "success": False,
                "matches": [],
                "message": "matches.json not found"
            })

        with open("matches.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "success": False,
            "matches": [],
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)