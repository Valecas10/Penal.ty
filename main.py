import subprocess
import sys

print("\n⚽ PENAL.TY — SISTEMA PRINCIPAL")
print("=" * 50)

print("\n📅 Buscando partidos del día...")

result = subprocess.run([
    sys.executable,
    "scheduler.py"
])

# ❌ Si scheduler falló, detener todo
if result.returncode != 0:
    print("\n❌ ERROR: El scheduler falló.")
    print("🛑 El launcher NO será iniciado.")
    sys.exit(1)


print("\n🚀 Iniciando launcher...")

result = subprocess.run([
    sys.executable,
    "launcher.py"
])

if result.returncode != 0:
    print("\n❌ ERROR: El launcher terminó con un error.")
    sys.exit(1)