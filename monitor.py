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
    description = status.get("description", "")

    if "pens" in short_detail.lower():
        return 60

    if "90'" in short_detail:
        return 60

    if (
        "extra" in detail.lower()
        or "extra" in name.lower()
        or "extra" in description.lower()
    ):
        return 60

    try:
        minute_text = short_detail.replace("'", "").strip()

        if minute_text.isdigit():
            minute = int(minute_text)

            if minute >= 80:
                return 60

    except Exception:
        pass

    return 600


def get_shootout_state(summary):
    shootout = summary.get("shootout") or []

    state = []

    for team in shootout:
        shots = []

        for shot in team.get("shots", []):
            shots.append({
                "shotNumber": shot.get("shotNumber"),
                "didScore": shot.get("didScore")
            })

        state.append({
            "team": team.get("team"),
            "shots": shots
        })

    return state


def format_shootout(state):
    lines = []

    for team in state:
        team_name = team["team"]

        symbols = []

        for shot in team["shots"]:
            if shot["didScore"]:
                symbols.append("O")
            else:
                symbols.append("X")

        lines.append(
            f"{team_name}: {' '.join(symbols)}"
        )

    return "\n".join(lines)


def format_shootout_notification(state):
    parts = []

    for team in state:
        team_name = team["team"]

        symbols = []

        for shot in team["shots"]:
            if shot["didScore"]:
                symbols.append("O")
            else:
                symbols.append("X")

        parts.append(
            f"{team_name}: {' '.join(symbols)}"
        )

    return " | ".join(parts)


def main():

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
    previous_shootout_state = []

    topic_map = {
        "Liga Argentina": "liga_argentina",
        "Copa Argentina": "copa_argentina",
        "Libertadores": "libertadores",
        "Sudamericana": "sudamericana",
    }

    topic = topic_map.get(match["league"])

    while True:

        try:

            summary = get_match_summary(match)

            status = get_status(summary)

            team1, team2 = get_teams(summary)

            print(
                f"\n⚽ {team1} vs {team2}"
            )

            print(
                f"⏱️ {status.get('shortDetail', status.get('detail'))}"
            )

            if is_cancelled_or_suspended(status):

                print(
                    "❌ Partido suspendido/cancelado/reprogramado."
                )

                break

            if is_shootout(summary):

                current_shootout_state = get_shootout_state(summary)

                # -----------------------------------------
                # PRIMERA DETECCIÓN
                # -----------------------------------------

                if not notification_sent:

                    print("\n🔥 ¡PENALES DETECTADOS!")

                    if topic:

                        send_penalty_notification(
                            title="PENAL.TY",
                            body=f"{team1} vs {team2} VAN A PENALES",
                            topic=topic,
                            notification_type="alert",
                            match_id=match["id"]
                        )

                        notification_sent = True

                    else:

                        print(
                            f"❌ No existe topic para: {match['league']}"
                        )

                # -----------------------------------------
                # ACTUALIZACIONES DE LA TANDA
                # -----------------------------------------

                if current_shootout_state != previous_shootout_state:

                    if current_shootout_state:

                        print("\n🥅 ESTADO DE LA TANDA:")
                        print(
                            format_shootout(
                                current_shootout_state
                            )
                        )

                        if (
                            notification_sent
                            and current_shootout_state
                            != previous_shootout_state
                        ):

                            notification_body = (
                                format_shootout_notification(
                                    current_shootout_state
                                )
                            )

                            if topic:

                                send_penalty_notification(
                                    title=f"{team1} vs {team2}",
                                    body=notification_body,
                                    topic=topic,
                                    notification_type="update",
                                    match_id=match["id"]
                                )

                        previous_shootout_state = (
                            current_shootout_state
                        )

            # -----------------------------------------
            # PARTIDO TERMINADO
            # -----------------------------------------

            if status.get("completed") is True:

                print("\n🏁 Partido finalizado.")

                break

            # -----------------------------------------
            # PRÓXIMA CONSULTA
            # -----------------------------------------

            interval = get_interval(status)

            print(
                f"⏳ Próxima consulta en "
                f"{interval // 60} minuto(s)..."
            )

            time.sleep(interval)

        except Exception as e:

            print(f"❌ Error: {e}")

            print(
                "⏳ Reintentando en 1 minuto..."
            )

            time.sleep(60)


if __name__ == "__main__":
    main()
