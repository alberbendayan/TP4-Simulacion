import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import load_data, mce, read_config, save_plot

from .common import ARCHIVOS


def get_mce(sim_dir, errores_por_metodo):
    config = read_config(sim_dir)
    dt = config["simulation"]["dt"]

    # La simulación tiene que ser de oscilador armónico simple
    if config["oscillatorType"] != "single":
        print(f"Error: Directory '{sim_dir}' is not a single oscillator simulation")
        return None, None

    for nombre, archivo in ARCHIVOS.items():
        path_archivo = os.path.join(sim_dir, archivo)
        t, data = load_data(path_archivo)

        if t is None or data is None:
            return None, None

        # Calcular el error cuadrático medio
        errores_por_metodo[nombre].append(mce(data[:, 0], data[:, 2]))

    return dt


def main():
    if len(sys.argv) < 2:
        print("Usage: python ej1C.py <simulation_directory1> [simulation_directory2 ...]")
        sys.exit(1)

    sim_dirs = sys.argv[1:]

    errores_por_metodo = {nombre: [] for nombre in ARCHIVOS.keys()}
    dts = []

    for sim_dir in sim_dirs:
        dt = get_mce(sim_dir, errores_por_metodo)
        if dt is not None:
            dts.append(dt)

    if not dts:
        print("Error: No valid simulation directories found")
        sys.exit(1)

    # Ordenamos los datos por dt
    sorted_indices = np.argsort(dts)
    dts = np.array(dts)[sorted_indices]
    for nombre in ARCHIVOS.keys():
        data = errores_por_metodo[nombre]
        errores_por_metodo[nombre] = np.array(data)[sorted_indices]

    fig, ax = plt.subplots(figsize=(12, 6))
    for nombre, errores in errores_por_metodo.items():
        ax.plot(dts, errores, marker="o", label=nombre)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Paso de integración dt [s]")
    ax.set_ylabel("Error cuadrático medio (ECM)")
    ax.legend(loc="lower right")
    ax.grid(True, which="both", linestyle="--", linewidth=0.7)

    plot_path = os.path.join(sim_dirs[0], "ecm_vs_dt.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()
