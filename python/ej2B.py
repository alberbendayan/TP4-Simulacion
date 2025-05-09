import os
import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from utils import read_config, validate_simulation_dir

def cargar_datos(nombre_archivo):
    data = np.loadtxt(nombre_archivo)
    tiempo = data[:, 0]
    posicion = data[:, 1]
    return tiempo, posicion

def extraer_omega(nombre_archivo):
    match = re.search(r"omega_(\d+\.\d+)_k_(\d+\.\d+)", nombre_archivo)
    return float(match.group(1)) if match else None

# Get simulation directory from command line
sim_dir = validate_simulation_dir()

# Read configuration
config = read_config(sim_dir)

# Verify this is a coupled oscillator simulation
if config['oscillatorType'] != 'coupled':
    print("Error: This script is for coupled oscillator simulations")
    sys.exit(1)

archivos = [os.path.join(sim_dir, f) for f in os.listdir(sim_dir) if f.endswith(".txt")]
archivos.sort(key=lambda x: extraer_omega(x) or 0)

plt.figure(figsize=(10, 6))

for archivo in archivos:
    t, x = cargar_datos(archivo)
    omega = extraer_omega(archivo)
    if omega is not None:
        plt.plot(t, x, label=f"ω = {omega:.2f}")

plt.xlabel("Tiempo [s]")
plt.ylabel("Posición de partícula 999 [m]")
plt.title(f"Osciladores acoplados: posición vs tiempo (k = {config['parameters']['k']})")
plt.legend()
plt.grid(True)

# Create graphics directory in results
graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
os.makedirs(graphics_dir, exist_ok=True)

# Save plot with timestamp from simulation directory
timestamp = os.path.basename(sim_dir)
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, f"osc_acoplado_vs_tiempo_{timestamp}.png"), dpi=300)
plt.show()