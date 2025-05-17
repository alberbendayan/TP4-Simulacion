import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import read_config, save_plot, validate_simulation_dir


def load_data(filename):
    try:
        data = np.loadtxt(filename)
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            print("Error: Data file contains NaN or Inf values")
            return None, None

        return data[:, 0], data[:, 1:]  # tiempo y todas las posiciones

    except Exception as e:
        print(f"Error loading data file {filename}: {e}")
        return None, None


def main():
    sim_dir = validate_simulation_dir()
    config = read_config(sim_dir)

    # La simulación tiene que ser de osciladores acoplados
    if config["oscillatorType"] != "coupled":
        print("Error: This script is for coupled oscillator simulations")
        sys.exit(1)

    # Chequeamos si ya se había creado el archivo de máximas amplitudes
    max_amplitudes_file = os.path.join(sim_dir, "max_amplitudes.txt")
    if os.path.exists(max_amplitudes_file):
        data = np.loadtxt(max_amplitudes_file)
        t = data[:, 0]
        max_amplitudes = data[:, 1]

    # Sino buscamos por archivo de simulación y lo calculamos
    else:
        sim_file = "output.txt"
        data_file = os.path.join(sim_dir, sim_file)
        t, positions = load_data(data_file)

        if t is None or positions is None:
            print("Error: Could not load valid data from the file")
            sys.exit(1)

        # Calculamos la máxima amplitud absoluta para cada instante de tiempo
        max_amplitudes = np.max(np.abs(positions), axis=1)

        # Guardamos las amplitudes máximas junto con el tiempo
        np.savetxt(max_amplitudes_file, np.column_stack((t, max_amplitudes)))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(t, max_amplitudes, "b-", linewidth=2)

    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Amplitud máxima absoluta |y| [m]")
    ax.grid(True, linestyle="--", alpha=0.7)

    plot_path = os.path.join(sim_dir, "amplitud_maxima_vs_t.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()
