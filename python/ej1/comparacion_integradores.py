import os
import sys

import matplotlib.pyplot as plt

from utils.utils import load_data, read_config, save_plot, validate_simulation_dir

from .common import ARCHIVOS, COLORES


def main():
    sim_dir = validate_simulation_dir()
    config = read_config(sim_dir)

    # La simulación tiene que ser oscilador armónico simple
    if config["oscillatorType"] != "single":
        print("Error: This script is for single oscillator simulations")
        sys.exit(1)

    fig, ax = plt.subplots(figsize=(12, 6))

    for nombre, archivo in ARCHIVOS.items():
        t, data = load_data(os.path.join(sim_dir, archivo))
        ax.plot(t, data[:, 0], label=nombre, color=COLORES[nombre])

    ax.plot(t, data[:, 2], label="Analítica", color="blue", linewidth=4, zorder=0, alpha=0.5)

    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Posición [m]")
    ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.7)

    plot_path = os.path.join(sim_dir, "comparacion_metodos.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()
