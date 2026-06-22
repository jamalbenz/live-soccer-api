from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"success": True, "message": "API working"})

@app.route("/matches")
def matches():
    if not os.path.exists("matches.json"):
        return jsonify({"success": False, "matches": [], "message": "matches.json not found"})

    with open("matches.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)

if __name__ == "__main__":
    app.run()