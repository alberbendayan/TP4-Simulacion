import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from utils.utils import read_config


def cargar_datos(path_archivo):
    data = np.loadtxt(path_archivo)
    tiempo = data[:, 0]
    numerica = data[:, 1]
    analitica = data[:, 3]
    return numerica, analitica


def error_cuadratico_medio(num, ana):
    return np.mean((num - ana) ** 2)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ej1C.py <simulation_directory1> [simulation_directory2 ...]")
        sys.exit(1)

    metodos = {
        "Gear predictor Corrector": "output_gear.txt",
        "Euler-Predictor-Corrector Modified": "output_beeman.txt",
        "Verlet": "output_verlet.txt",
    }

    errores_por_metodo = {nombre: [] for nombre in metodos}
    dts = []

    for sim_dir in sys.argv[1:]:
        if not os.path.exists(sim_dir):
            print(f"Directory '{sim_dir}' does not exist")
            continue

        try:
            # Read configuration
            config = read_config(sim_dir)
            
            # Verify this is a single oscillator simulation
            if config['oscillatorType'] != 'single':
                print(f"Error: Directory '{sim_dir}' is not a single oscillator simulation")
                continue

            dt = config['simulation']['dt']
            dts.append(dt)

            for nombre_metodo, archivo in metodos.items():
                path_archivo = os.path.join(sim_dir, archivo)
                numerica, analitica = cargar_datos(path_archivo)
                ecm = error_cuadratico_medio(numerica, analitica)
                errores_por_metodo[nombre_metodo].append(ecm)

        except Exception as e:
            print(f"Error processing '{sim_dir}': {e}", file=sys.stderr)

    if not dts:
        print("No valid simulation directories found")
        sys.exit(1)

    # Sort by dt creciente
    dts, errores_ordenados = zip(*sorted(zip(dts, zip(*[errores_por_metodo[m] for m in metodos]))))
    dts = np.array(dts)
    errores_por_metodo = {
        metodo: np.array(errores) for metodo, errores in zip(metodos, zip(*errores_ordenados))
    }

    # Plot
    plt.figure(figsize=(10, 6))
    for nombre, errores in errores_por_metodo.items():
        plt.plot(dts, errores, marker='o', label=nombre)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Paso de integración dt (log)")
    plt.ylabel("Error cuadrático medio (log)")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Create graphics directory in results
    graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
    os.makedirs(graphics_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(os.path.join(graphics_dir, "error_vs_dt.png"), dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
