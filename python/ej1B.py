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
    print("Uso: un run ej1B.py <valor>")
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


nombres_metodos = list(archivos.keys())
ecms = []

for nombre, archivo in archivos.items():
    _, num, ana = cargar_datos(archivo)
    ecm = error_cuadratico_medio(num, ana)
    ecms.append(ecm)



plt.figure(figsize=(8, 5))
for i, ecm in enumerate(ecms):
    plt.text(i, ecm, f"{ecm:.2e}", ha='center', va='bottom', fontsize=9)
plt.bar(nombres_metodos, ecms, color=[colores[n] for n in nombres_metodos])
plt.ylabel("Error cuadrático medio (ECM)")
plt.grid(axis='y')
plt.xticks(rotation=20)
plt.yscale("log")

os.makedirs("../results/graphics", exist_ok=True)
plt.tight_layout()
plt.savefig(f"../results/graphics/ecm_metodos_{valor}.png", dpi=300)
plt.show()