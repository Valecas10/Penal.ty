import requests
import json

LEAGUES = {
    "Liga Argentina": "arg.1",
    "Copa Argentina": "arg.copa",
    "Libertadores": "conmebol.libertadores",
    "Sudamericana": "conmebol.sudamericana",
}


def get_scoreboard(league_id):
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
    return response.json()


for league_name, league_id in LEAGUES.items():

    print("\n" + "=" * 70)
    print(f"🏆 {league_name}")
    print("=" * 70)

    try:
        data = get_scoreboard(league_id)

        # Guardamos el JSON completo para analizarlo después
        filename = f"fixtures_{league_id.replace('.', '_')}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        events = data.get("events", [])

        print(f"\nPartidos encontrados: {len(events)}\n")

        for event in events:

            competition = event.get("competitions", [{}])[0]
            status = event.get("status", {}).get("type", {})

            print("PARTIDO:", event.get("name"))
            print("ID:", event.get("id"))
            print("FECHA:", event.get("date"))

            print("\nSTATUS:")
            print("  name:", status.get("name"))
            print("  detail:", status.get("detail"))
            print("  state:", status.get("state"))

            print("\nCAMPOS DEL EVENTO:")
            print(list(event.keys()))

            print("\nCAMPOS DE COMPETITION:")
            print(list(competition.keys()))

            # Mostrar notes, si existen
            notes = competition.get("notes", [])

            if notes:
                print("\nNOTES:")
                for note in notes:
                    print(" ", note)

            print("-" * 70)

    except Exception as e:
        print(f"❌ Error: {e}")

print("\n✅ Investigación terminada.")