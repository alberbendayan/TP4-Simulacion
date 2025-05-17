import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import read_config, save_plot


def load_data(filename, stationary_time, dt):
    try:
        # Calculamos la cantidad de lineas que se tiene que saltear
        lines_to_skip = int(stationary_time / dt) + 1

        data = np.loadtxt(filename, skiprows=lines_to_skip)
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            print("Error: Data file contains NaN or Inf values")
            return None, None

        return data[:, 0], data[:, 1:]  # tiempo y todas las posiciones

    except Exception as e:
        print(f"Error loading data file {filename}: {e}")
        return None, None


def get_stationary_amplitude(sim_dir, stationary_time):
    config = read_config(sim_dir)
    dt = config["simulation"]["dt"]
    omega = config["parameters"]["omega"]

    # La simulación tiene que ser de osciladores acoplados
    if config["oscillatorType"] != "coupled":
        print(f"Error: Simulation in {sim_dir} is not a coupled oscillator simulation")
        return None, None

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
        t, positions = load_data(data_file, stationary_time, dt)

        if t is None or positions is None:
            return None, None

        # Calculamos la máxima amplitud absoluta para cada instante de tiempo
        max_amplitudes = np.max(np.abs(positions), axis=1)

        # Guardamos las amplitudes máximas junto con el tiempo
        np.savetxt(max_amplitudes_file, np.column_stack((t, max_amplitudes)))

    return np.max(max_amplitudes), omega


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_stationary_amplitudes.py <stationary_time> <sim_dir1> [sim_dir2 sim_dir3 ...]")
        sys.exit(1)

    try:
        stationary_time = float(sys.argv[1])

    except ValueError:
        print("Error: Stationary time must be a number")
        sys.exit(1)

    sim_dirs = sys.argv[2:]

    amplitudes = []
    omegas = []

    for sim_dir in sim_dirs:
        amp, omega = get_stationary_amplitude(sim_dir, stationary_time)
        if amp is not None and omega is not None:
            amplitudes.append(amp)
            omegas.append(omega)
            print(f"Amplitude: {amp}, Omega: {omega}")

    if not amplitudes:
        print("Error: No valid data found in any simulation directory")
        sys.exit(1)

    # Ordenamos los datos por omega
    sorted_indices = np.argsort(omegas)
    omegas = np.array(omegas)[sorted_indices]
    amplitudes = np.array(amplitudes)[sorted_indices]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(omegas, amplitudes, "bo-", linewidth=2, markersize=8)

    ax.set_xlabel("ω [rad/s]")
    ax.set_ylabel("Amplitud máxima absoluta |y| [m]")
    ax.grid(True, linestyle="--", alpha=0.7)

    plot_path = os.path.join(sim_dirs[0], "amplitud_maxima_vs_w.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()
