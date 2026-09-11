import requests
import json

EVENT_ID = "401892190"

url = (
    "https://site.api.espn.com/apis/site/v2/sports/"
    f"soccer/arg.copa/summary?event={EVENT_ID}"
)

print("Consultando resumen detallado de ESPN...")
print("Evento:", EVENT_ID)
print()

response = requests.get(url, timeout=15)

print("Status HTTP:", response.status_code)

response.raise_for_status()

data = response.json()

# Guardamos absolutamente todo
filename = "summary_boca_velez.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print()
print(f"JSON completo guardado en: {filename}")

print()
print("=" * 70)
print("CLAVES PRINCIPALES DEL JSON")
print("=" * 70)

for key in data.keys():
    value = data[key]

    if isinstance(value, list):
        print(f"{key}: LISTA ({len(value)} elementos)")

    elif isinstance(value, dict):
        print(f"{key}: OBJETO")

    else:
        print(f"{key}: {value}")


# ---------------------------------------------------------
# BUSCADOR RECURSIVO
# ---------------------------------------------------------

KEYWORDS = [
    "pen",
    "shoot",
    "goal",
    "period"
]


def buscar(obj, path="root"):

    if isinstance(obj, dict):

        for key, value in obj.items():

            new_path = f"{path}.{key}"

            # Buscamos palabras en nombres de campos
            if any(word.lower() in key.lower() for word in KEYWORDS):

                print()
                print("🔎 CAMPO ENCONTRADO")
                print("PATH:", new_path)

                if isinstance(value, (str, int, float, bool)):
                    print("VALOR:", value)

                else:
                    print("TIPO:", type(value).__name__)

            buscar(value, new_path)

    elif isinstance(obj, list):

        for i, item in enumerate(obj):

            buscar(item, f"{path}[{i}]")

    elif isinstance(obj, str):

        if any(word.lower() in obj.lower() for word in KEYWORDS):

            print()
            print("🔎 TEXTO ENCONTRADO")
            print("PATH:", path)
            print("VALOR:", obj)


print()
print("=" * 70)
print("BUSCANDO INFORMACIÓN SOBRE PENALES")
print("=" * 70)

buscar(data)

print()
print("=" * 70)
print("INVESTIGACIÓN TERMINADA")
print("=" * 70)