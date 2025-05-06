import matplotlib.pyplot as plt
import numpy as np
import sys
import os


def cargar_datos(nombre_archivo):
    data = np.loadtxt(nombre_archivo)
    tiempo = data[:, 0]
    numerica = data[:, 1]
    analitica = data[:, 3]
    return tiempo, numerica, analitica


def error_cuadratico_medio(num, ana):
    return np.mean((num - ana) ** 2)

if len(sys.argv) != 2:
    print("Uso: un run ej1A.py <valor>")
    sys.exit(1)

valor = sys.argv[1]
base_path = f"../results/{valor}"
if not os.path.exists(base_path):
    print(f"El directorio '{base_path}' no existe.")
    sys.exit(1)

# Archivos de salida de los métodos
archivos = {
    "Gear predictor Corrector": f"{base_path}/output_gear.txt",
    "Euler-Predictor-Corrector Modified": f"{base_path}/output_beeman.txt",
    "Verlet": f"{base_path}/output_verlet.txt",
}

# Colores
colores = {
    "Analítica": "blue",
    "Euler-Predictor-Corrector Modified": "magenta",
    "Verlet": "cyan",
    "Gear predictor Corrector": "black",
}

plt.figure(figsize=(10, 6))

# Subplot 1: todo el rango
for nombre, archivo in archivos.items():
    t, num, ana = cargar_datos(archivo)
    plt.plot(t, num, label=nombre, color=colores[nombre])

plt.plot(t, ana, label="Analítica", color="blue")

plt.xlabel("Tiempo [s]")
plt.ylabel("Posición [m]")
plt.legend()
plt.grid(True)
os.makedirs("../results/graphics", exist_ok=True)
plt.tight_layout()
plt.savefig(f"../results/graphics/comparacion_metodos_{valor}.png", dpi=300)
plt.show()