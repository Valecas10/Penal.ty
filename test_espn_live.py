import requests
import json

LEAGUE_ID = "uefa.champions"

url = (
    f"https://site.api.espn.com/apis/site/v2/sports/"
    f"soccer/{LEAGUE_ID}/scoreboard"
)

data = requests.get(url).json()

print("\n⚽ PARTIDOS CHAMPIONS")
print("=" * 60)

for event in data.get("events", []):

    print(f"\nNombre: {event.get('name')}")
    print(f"ID: {event.get('id')}")
    print(f"Fecha: {event.get('date')}")

    status = event["status"]["type"]

    print(f"Estado: {status.get('shortDetail')}")