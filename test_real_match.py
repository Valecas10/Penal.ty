import requests

from detector import is_shootout
from firebase_sender import send_penalty_notification


LEAGUE_ID = "arg.copa"
EVENT_ID = "401912728"


def get_summary():

    url = (
        "https://site.api.espn.com/apis/site/v2/sports/"
        f"soccer/{LEAGUE_ID}/summary?event={EVENT_ID}"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    return response.json()


print("\n⚽ PENAL.TY — TEST PARTIDO REAL")
print("=" * 45)

summary = get_summary()

competition = summary["header"]["competitions"][0]

teams = competition["competitors"]

team1 = teams[0]["team"]["displayName"]
team2 = teams[1]["team"]["displayName"]

print(f"\n⚽ {team1} vs {team2}")

status = competition["status"]["type"]

print(f"Estado: {status.get('detail')}")

if is_shootout(summary):

    print("\n🔥 ¡PENALES DETECTADOS!")

    title = "⚽ PENAL.TY"
    body = f"🔥 ¡{team1} vs {team2} FUE A PENALES!"

    send_penalty_notification(title, body)

else:

    print("\n❌ No se detectó una tanda.")