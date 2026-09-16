import requests
import json
import time
import sys

from detector import is_shootout
from firebase_sender import send_penalty_notification


def get_match_summary(match):

    url = (
        "https://site.api.espn.com/apis/site/v2/sports/"
        f"soccer/{match['league_id']}/summary?event={match['id']}"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    return response.json()


def get_status(summary):

    try:
        return summary["header"]["competitions"][0]["status"]["type"]
    except (KeyError, IndexError):
        return {}


def get_teams(summary):

    competition = summary["header"]["competitions"][0]
    teams = competition["competitors"]

    return (
        teams[0]["team"]["displayName"],
        teams[1]["team"]["displayName"]
    )


def is_cancelled_or_suspended(status):

    name = status.get("name", "").lower()
    detail = status.get("detail", "").lower()

    invalid_statuses = [
        "postponed",
        "cancelled",
        "canceled",
        "suspended"
    ]

    return any(
        word in name or word in detail
        for word in invalid_statuses
    )


def get_interval(status):

    short_detail = status.get("shortDetail", "")
    detail = status.get("detail", "")
    name = status.get("name", "")

    # ⚽ Si estamos en tiempo añadido
    # Ej: 90'+1'
    if "90'" in short_detail:
        return 60

    # ⏱️ Tiempo extra / alargue
    if (
        "extra" in detail.lower()
        or "extra" in name.lower()
        or "extra" in status.get("description", "").lower()
    ):
        return 60

    # 🔢 Minutos normales: 83', 72', etc.
    try:
        minute_text = short_detail.replace("'", "").strip()

        if minute_text.isdigit():
            minute = int(minute_text)

            if minute >= 80:
                return 60

    except Exception:
        pass

    # 🕐 Todo lo anterior al minuto 80
    return 600


def main():

    # Recibir partido desde launcher.py
    if len(sys.argv) < 2:
        print("❌ No se recibió ningún partido.")
        return

    match = json.loads(sys.argv[1])

    print("\n⚽ PENAL.TY — MONITOR")
    print("=" * 50)
    print(f"🏆 {match['league']}")
    print(f"⚽ {match['name']}")
    print("=" * 50)

    notification_sent = False

    while True:

        try:

            summary = get_match_summary(match)

            status = get_status(summary)

            team1, team2 = get_teams(summary)

            print(f"\n⚽ {team1} vs {team2}")
            print(
                f"⏱️ {status.get('shortDetail', status.get('detail'))}"
            )

            # ❌ Suspendido / cancelado / reprogramado
            if is_cancelled_or_suspended(status):

                print("❌ Partido suspendido/cancelado/reprogramado.")
                break

            # 🔥 PENALTIES
            if is_shootout(summary):

                if not notification_sent:

                    print("\n🔥 ¡PENALES DETECTADOS!")

                    topic_map = {
                        "Liga Argentina": "liga_argentina",
                        "Copa Argentina": "copa_argentina",
                        "Libertadores": "libertadores",
                        "Sudamericana": "sudamericana",
                    }

                    topic = topic_map.get(match["league"])

                    if topic:
                        send_penalty_notification(
                            "⚽ PENAL.TY",
                            f"🔥 ¡{team1} vs {team2} VA A PENALES!",
                            topic
                        )

                        notification_sent = True

                    else:
                        print(f"❌ No existe topic para: {match['league']}")

            # 🏁 Partido terminado
            if status.get("completed") is True:

                print("\n🏁 Partido finalizado.")
                break

            # ⏳ Próxima consulta
            interval = get_interval(status)

            print(
                f"⏳ Próxima consulta en "
                f"{interval // 60} minuto(s)..."
            )

            time.sleep(interval)

        except Exception as e:

            print(f"❌ Error: {e}")
            print("⏳ Reintentando en 1 minuto...")

            time.sleep(60)


if __name__ == "__main__":
    main()