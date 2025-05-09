import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from utils import read_config, validate_simulation_dir


def cargar_datos(nombre_archivo):
    data = np.loadtxt(nombre_archivo)
    tiempo = data[:, 0]
    numerica = data[:, 1]
    analitica = data[:, 3]
    return tiempo, numerica, analitica


def error_cuadratico_medio(num, ana):
    return np.mean((num - ana) ** 2)


# Get simulation directory from command line
sim_dir = validate_simulation_dir()

# Read configuration
config = read_config(sim_dir)

# Verify this is a single oscillator simulation
if config['oscillatorType'] != 'single':
    print("Error: This script is for single oscillator simulations")
    sys.exit(1)

# Archivos de salida de los métodos
archivos = {
    "Gear predictor Corrector": os.path.join(sim_dir, "output_gear.txt"),
    "Euler-Predictor-Corrector Modified": os.path.join(sim_dir, "output_beeman.txt"),
    "Verlet": os.path.join(sim_dir, "output_verlet.txt"),
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

# Create graphics directory in results
graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
os.makedirs(graphics_dir, exist_ok=True)

# Save plot with timestamp from simulation directory
timestamp = os.path.basename(sim_dir)
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, f"ecm_metodos_{timestamp}.png"), dpi=300)
plt.show()