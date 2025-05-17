import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import read_config, validate_simulation_dir


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

# Create graphics directory in results
graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
os.makedirs(graphics_dir, exist_ok=True)

# Save plot with timestamp from simulation directory
timestamp = os.path.basename(sim_dir)
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, f"comparacion_metodos_{timestamp}.png"), dpi=300)
plt.show()