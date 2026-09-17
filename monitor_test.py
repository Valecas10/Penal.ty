import json
import subprocess
import sys

match = {
    "id": "401892190",
    "league": "Copa Argentina",
    "league_id": "arg.copa",
    "name": "Boca Juniors at Vélez Sarsfield",
    "date": "2025-11-27T00:00:00Z"
}

subprocess.run([
    sys.executable,
    "monitor.py",
    json.dumps(match)
])