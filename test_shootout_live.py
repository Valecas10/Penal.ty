import time

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

previous_state = None

for state in states:

    if state != previous_state:

        print("\n🥅 NUEVO ESTADO")

        for team, shots in state.items():
            print(f"{team}: {' '.join(shots)}")

        previous_state = state

    time.sleep(2)

print("\n🏁 TANDA FINALIZADA")