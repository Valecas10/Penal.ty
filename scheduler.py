import requests
import json
from datetime import datetime

LEAGUES = {
    "Copa Argentina": "arg.copa",
    "Libertadores": "conmebol.libertadores",
    "Sudamericana": "conmebol.sudamericana",
}


def get_matches(league_id):
    url = (
        "https://site.api.espn.com/apis/site/v2/sports/"
        f"soccer/{league_id}/scoreboard"
    )

    response = requests.get(
        url,
        params={"limit": 100},
        timeout=15
    )

    response.raise_for_status()
    return response.json().get("events", [])


def can_go_to_penalties(league_name, competition):

    # Copa Argentina: partido único
    if league_name == "Copa Argentina":
        return True

    notes = competition.get("notes", [])

    for note in notes:
        text = note.get("text", "").lower()

        if "1st leg" in text:
            return False

        if "2nd leg" in text:
            return True

    return False


print("\n⚽ PENAL.TY — SCHEDULER")
print("=" * 50)

matches_to_monitor = []

for league_name, league_id in LEAGUES.items():

    try:
        events = get_matches(league_id)

        for event in events:

            competition = event.get("competitions", [{}])[0]

            if not can_go_to_penalties(league_name, competition):
                continue

            matches_to_monitor.append({
                "id": event["id"],
                "league": league_name,
                "league_id": league_id,
                "name": event["name"],
                "date": event["date"]
            })

    except Exception as e:
        print(f"❌ Error en {league_name}: {e}")


# Guardar partidos
with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(
        matches_to_monitor,
        f,
        indent=4,
        ensure_ascii=False
    )


if not matches_to_monitor:

    print("\nNo hay partidos próximos que puedan ir a penales.")

else:

    print("\n🔥 PARTIDOS GUARDADOS PARA MONITOREAR:\n")

    for match in matches_to_monitor:

        date = datetime.fromisoformat(
            match["date"].replace("Z", "+00:00")
        )

        print(f"🏆 {match['league']}")
        print(f"⚽ {match['name']}")
        print(f"📅 {date}")
        print(f"🆔 {match['id']}")
        print("-" * 50)


print("\n✅ Archivo matches.json actualizado.")