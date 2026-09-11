import time


# Estados simulados del partido
STATES = [
    {
        "status": "PRE",
        "shootout": []
    },
    {
        "status": "1st Half",
        "shootout": []
    },
    {
        "status": "Halftime",
        "shootout": []
    },
    {
        "status": "2nd Half",
        "shootout": []
    },
    {
        "status": "Extra Time",
        "shootout": []
    },

    # 🔥 ACÁ EMPIEZA LA TANDA
    {
        "status": "PENALTIES",
        "shootout": [
            {
                "team": "River Plate",
                "shots": [
                    {
                        "player": "Jugador 1",
                        "shotNumber": 1,
                        "didScore": True
                    }
                ]
            },
            {
                "team": "Boca Juniors",
                "shots": [
                    {
                        "player": "Jugador 1",
                        "shotNumber": 1,
                        "didScore": True
                    }
                ]
            }
        ]
    },

    {
        "status": "PENALTIES",
        "shootout": [
            {
                "team": "River Plate",
                "shots": [
                    {
                        "player": "Jugador 1",
                        "shotNumber": 1,
                        "didScore": True
                    },
                    {
                        "player": "Jugador 2",
                        "shotNumber": 2,
                        "didScore": True
                    }
                ]
            },
            {
                "team": "Boca Juniors",
                "shots": [
                    {
                        "player": "Jugador 1",
                        "shotNumber": 1,
                        "didScore": True
                    },
                    {
                        "player": "Jugador 2",
                        "shotNumber": 2,
                        "didScore": False
                    }
                ]
            }
        ]
    },

    {
        "status": "FT-Pens",
        "shootout": [
            {
                "team": "River Plate",
                "shots": [
                    {"didScore": True},
                    {"didScore": True},
                    {"didScore": True},
                    {"didScore": True},
                    {"didScore": True}
                ]
            },
            {
                "team": "Boca Juniors",
                "shots": [
                    {"didScore": True},
                    {"didScore": False},
                    {"didScore": True},
                    {"didScore": False},
                    {"didScore": True}
                ]
            }
        ]
    }
]


def is_shootout(state):
    return bool(state.get("shootout"))


def main():

    print("\n⚽ PENAL.TY — TEST MODE")
    print("=" * 45)

    notification_sent = False

    for state in STATES:

        print(f"\n⏱️ Estado: {state['status']}")

        if is_shootout(state):

            # Solo notificamos una vez
            if not notification_sent:

                print("\n🔥" * 3)
                print("🚨 ¡PENALES DETECTADOS!")
                print("🔔 NOTIFICACIÓN ENVIADA")
                print("🔥" * 3)

                notification_sent = True

            else:
                print("⚽ Tanda continúa...")

        else:
            print("⏳ No hay tanda.")

        time.sleep(2)

    print("\n🏁 TEST TERMINADO")


if __name__ == "__main__":
    main()