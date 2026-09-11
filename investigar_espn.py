import requests
import json

LEAGUE = "arg.copa"
DATE = "20260902"

url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{LEAGUE}/scoreboard"

print("Consultando ESPN...")
print("URL:", url)
print("Fecha:", DATE)
print()

response = requests.get(
    url,
    params={
        "dates": DATE
    },
    timeout=15
)

print("Status HTTP:", response.status_code)

response.raise_for_status()

data = response.json()

# Guardamos la respuesta completa
with open("scoreboard_boca_velez.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

events = data.get("events", [])

print()
print("Eventos encontrados:", len(events))
print("=" * 60)

for event in events:

    print()
    print("PARTIDO:", event.get("name"))
    print("ID:", event.get("id"))

    status = event.get("status", {})
    status_type = status.get("type", {})

    print("Estado:", status_type.get("detail"))
    print("Estado corto:", status_type.get("shortDetail"))
    print("Completado:", status_type.get("completed"))

    competitions = event.get("competitions", [])

    for competition in competitions:

        print()
        print("COMPETIDORES:")

        for competitor in competition.get("competitors", []):

            team = competitor.get("team", {})

            print(
                f"- {team.get('displayName')} "
                f"| Score: {competitor.get('score')} "
                f"| Winner: {competitor.get('winner')}"
            )

    print("-" * 60)

print()
print("JSON guardado en: scoreboard_boca_velez.json")