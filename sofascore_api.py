import requests
import json
from datetime import datetime

def get_sofascore_matches():
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://www.sofascore.com/api/v1/sport/football/events/live"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers, timeout=20)
    data = r.json()

    matches = []

    for event in data.get("events", []):
        tournament = event.get("tournament", {}).get("name", "Football")
        home = event.get("homeTeam", {})
        away = event.get("awayTeam", {})
        home_score = event.get("homeScore", {}).get("current", "")
        away_score = event.get("awayScore", {}).get("current", "")
        status = event.get("status", {})

        home_id = home.get("id", "")
        away_id = away.get("id", "")

        matches.append({
            "league": tournament,
            "home": home.get("name", "Home"),
            "away": away.get("name", "Away"),
            "home_logo": f"https://api.sofascore.app/api/v1/team/{home_id}/image" if home_id else "",
            "away_logo": f"https://api.sofascore.app/api/v1/team/{away_id}/image" if away_id else "",
            "home_score": home_score,
            "away_score": away_score,
            "status": status.get("type", "LIVE"),
            "minute": status.get("description", "LIVE"),
            "is_live": True
        })

    if not matches:
        matches = [
            {
                "league": "Premium Football",
                "home": "Real Madrid",
                "away": "Barcelona",
                "home_logo": "",
                "away_logo": "",
                "home_score": "",
                "away_score": "",
                "status": "NS",
                "minute": "Today",
                "is_live": False
            }
        ]

    return {
        "success": True,
        "date": today,
        "count": len(matches),
        "matches": matches
    }

print(json.dumps(get_sofascore_matches(), ensure_ascii=False, indent=2))