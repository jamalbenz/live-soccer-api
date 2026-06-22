import requests
import json
from datetime import datetime, timezone

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

URL = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{TODAY}"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

IMPORTANT_LEAGUES = [
    "World Championship", "World Cup", "Champions League", "Europa League",
    "Premier League", "LaLiga", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
    "Allsvenskan", "Superettan", "Saudi Pro League", "Eredivisie", "Primeira Liga"
]

def team_logo(team_id):
    return f"https://api.sofascore.app/api/v1/team/{team_id}/image"

def league_logo(tournament_id):
    return f"https://api.sofascore.app/api/v1/unique-tournament/{tournament_id}/image"

def status_info(event):
    status = event.get("status", {})
    code = status.get("code")
    desc = status.get("description", "")
    short = status.get("type", "")

    is_live = short == "inprogress"
    if short == "finished":
        minute = "Finished"
    elif is_live:
        minute = str(event.get("time", {}).get("currentPeriodStartTimestamp", "LIVE"))
    else:
        minute = datetime.fromtimestamp(event.get("startTimestamp", 0)).strftime("%H:%M")

    return desc or short, minute, is_live

response = requests.get(URL, headers=HEADERS, timeout=30)
data = response.json()

matches = []

for event in data.get("events", []):
    tournament = event.get("tournament", {})
    unique = tournament.get("uniqueTournament", {})
    league = unique.get("name") or tournament.get("name") or "Football"

    if not any(x.lower() in league.lower() for x in IMPORTANT_LEAGUES):
        continue

    home = event.get("homeTeam", {})
    away = event.get("awayTeam", {})
    home_score = event.get("homeScore", {}).get("current", "")
    away_score = event.get("awayScore", {}).get("current", "")

    status, minute, is_live = status_info(event)

    matches.append({
        "id": str(event.get("id")),
        "league": league,
        "league_logo": league_logo(unique.get("id", "")),
        "country": tournament.get("category", {}).get("name", ""),
        "home": home.get("name", ""),
        "home_logo": team_logo(home.get("id", "")),
        "away": away.get("name", ""),
        "away_logo": team_logo(away.get("id", "")),
        "home_score": home_score,
        "away_score": away_score,
        "status": status,
        "minute": minute,
        "match_time": datetime.fromtimestamp(event.get("startTimestamp", 0)).strftime("%H:%M"),
        "is_live": is_live
    })

result = {
    "success": True,
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "count": len(matches),
    "matches": matches[:40]
}

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))