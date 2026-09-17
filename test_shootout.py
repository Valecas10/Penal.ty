import requests
import json

LEAGUE_ID = "arg.copa"
EVENT_ID = "401892190"

url = (
    "https://site.api.espn.com/apis/site/v2/sports/"
    f"soccer/{LEAGUE_ID}/summary?event={EVENT_ID}"
)

response = requests.get(url, timeout=15)
response.raise_for_status()

summary = response.json()

print("\n=== SHOOTOUT ===\n")

print(json.dumps(
    summary.get("shootout", []),
    indent=4,
    ensure_ascii=False
))