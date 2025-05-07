import os
import re
import sys

import matplotlib.pyplot as plt
import numpy as np


def cargar_datos(nombre_archivo):
    data = np.loadtxt(nombre_archivo)
    tiempo = data[:, 0]
    posicion = data[:, 1]
    return tiempo, posicion

def extraer_omega(nombre_archivo):
    match = re.search(r"omega_(\d+\.\d+)", nombre_archivo)
    return float(match.group(1)) if match else None

if len(sys.argv) != 2:
    print("Uso: python graficar_osc_acoplado.py <directorio>")
    sys.exit(1)

base_path = sys.argv[1]

if not os.path.exists(base_path):
    print(f"El directorio '{base_path}' no existe.")
    sys.exit(1)

archivos = [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".txt")]
archivos.sort(key=lambda x: extraer_omega(x) or 0)

plt.figure(figsize=(10, 6))

for archivo in archivos:
    t, x = cargar_datos(archivo)
    omega = extraer_omega(archivo)
    if omega is not None:
        plt.plot(t, x, label=f"ω = {omega:.2f}")

plt.xlabel("Tiempo [s]")
plt.ylabel("Posición de partícula 999 [m]")
plt.title("Osciladores acoplados: posición vs tiempo")
plt.legend()
plt.grid(True)
plt.tight_layout()
os.makedirs("../results/graphics", exist_ok=True)
plt.savefig("../results/graphics/osc_acoplado_vs_tiempo.png", dpi=300)
plt.show()