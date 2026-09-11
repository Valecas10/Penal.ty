import json
import time
import subprocess
import sys
from datetime import datetime, timezone


def get_match_time(match):
    return datetime.fromisoformat(
        match["date"].replace("Z", "+00:00")
    )


def start_monitor(match):

    print("\n🚀 INICIANDO MONITOR")
    print(f"⚽ {match['name']}")
    print(f"🏆 {match['league']}")

    subprocess.Popen([
        sys.executable,
        "monitor.py",
        json.dumps(match)
    ])


def main():

    print("\n⚽ PENAL.TY — LAUNCHER")
    print("=" * 50)

    with open("matches_test.json", "r", encoding="utf-8") as file:
        matches = json.load(file)

    launched_matches = set()

    while True:

        now = datetime.now(timezone.utc)

        for match in matches:

            event_id = match["id"]

            # Ya lanzamos un monitor para este partido
            if event_id in launched_matches:
                continue

            match_time = get_match_time(match)

            # Llegó la hora del partido
            if now >= match_time:

                start_monitor(match)

                launched_matches.add(event_id)

        # Si todos los monitores fueron lanzados
        if len(launched_matches) == len(matches):

            print("\n✅ Todos los monitores fueron iniciados.")
            break

        # Revisar cada 10 segundos
        time.sleep(10)


if __name__ == "__main__":
    main()