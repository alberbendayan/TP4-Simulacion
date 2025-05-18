import os
import sys

import matplotlib.pyplot as plt

from utils.utils import load_data, mce, read_config, save_plot, validate_simulation_dir

from .common import ARCHIVOS, COLORES


def main():
    sim_dir = validate_simulation_dir()
    config = read_config(sim_dir)

    # La simulación tiene que ser oscilador armónico simple
    if config["oscillatorType"] != "single":
        print("Error: This script is for single oscillator simulations")
        sys.exit(1)

    nombres_metodos = list(ARCHIVOS.keys())
    ecms = []

    for nombre, archivo in ARCHIVOS.items():
        _, data = load_data(os.path.join(sim_dir, archivo))
        ecm = mce(data[0], data[1])
        ecms.append(ecm)

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, ecm in enumerate(ecms):
        ax.text(nombres_metodos[i], ecm, f"{ecm:.2e}", ha="center", va="bottom")

    ax.bar(nombres_metodos, ecms, color=[COLORES[n] for n in nombres_metodos])
    ax.set_ylabel("Error cuadrático medio (ECM)")
    ax.set_yscale("log")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plot_path = os.path.join(sim_dir, "ecm_metodos.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()
