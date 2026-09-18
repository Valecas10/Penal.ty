import time

from firebase_sender import send_penalty_notification


TOPIC = "copa_argentina"
MATCH_ID = "test_live_123"

TEAM1 = "Boca Juniors"
TEAM2 = "Vélez Sarsfield"


states = [
    {
        "Boca Juniors": ["O"],
        "Vélez Sarsfield": []
    },
    {
        "Boca Juniors": ["O"],
        "Vélez Sarsfield": ["X"]
    },
    {
        "Boca Juniors": ["O", "O"],
        "Vélez Sarsfield": ["X"]
    },
    {
        "Boca Juniors": ["O", "O"],
        "Vélez Sarsfield": ["X", "O"]
    },
    {
        "Boca Juniors": ["O", "O", "X"],
        "Vélez Sarsfield": ["X", "O"]
    },
    {
        "Boca Juniors": ["O", "O", "X"],
        "Vélez Sarsfield": ["X", "O", "O"]
    },
    {
        "Boca Juniors": ["O", "O", "X", "O"],
        "Vélez Sarsfield": ["X", "O", "O"]
    },
    {
        "Boca Juniors": ["O", "O", "X", "O"],
        "Vélez Sarsfield": ["X", "O", "O", "O"]
    },
    {
        "Boca Juniors": ["O", "O", "X", "O", "O"],
        "Vélez Sarsfield": ["X", "O", "O", "O", "X"]
    }
]


def format_state(state):

    boca = " ".join(state["Boca Juniors"])
    velez = " ".join(state["Vélez Sarsfield"])

    return f"Boca Juniors: {boca} | Vélez Sarsfield: {velez}"


print("\n⚽ TEST DE TANDA EN VIVO")
print("=" * 50)


# -------------------------------------------------
# ALERTA INICIAL
# -------------------------------------------------

print("\n🚨 INICIANDO TANDA")

send_penalty_notification(
    title="PENAL.TY",
    body=f"{TEAM1} vs {TEAM2} VAN A PENALES",
    topic=TOPIC,
    notification_type="alert",
    match_id=MATCH_ID
)

print("🔔 Alerta inicial enviada.")

time.sleep(5)


# -------------------------------------------------
# SIMULAR TIROS
# -------------------------------------------------

for index, state in enumerate(states):

    body = format_state(state)

    print(f"\n🥅 TIRO {index + 1}")
    print(body)

    send_penalty_notification(
        title=f"{TEAM1} vs {TEAM2}",
        body=body,
        topic=TOPIC,
        notification_type="update",
        match_id=MATCH_ID
    )

    print("🔄 Actualización enviada.")

    # Delay entre cada penal
    time.sleep(5)


print("\n🏁 TANDA FINALIZADA")