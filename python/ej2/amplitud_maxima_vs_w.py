import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import load_data, read_config, save_plot


def get_stationary_amplitude(sim_dir, stationary_time):
    config = read_config(sim_dir)
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
        t, positions = load_data(data_file)

        if t is None or positions is None:
            return None, None

        # Calculamos la máxima amplitud absoluta para cada instante de tiempo
        max_amplitudes = np.max(np.abs(positions), axis=1)

        # Guardamos las amplitudes máximas junto con el tiempo
        np.savetxt(max_amplitudes_file, np.column_stack((t, max_amplitudes)))

    # Descartamos los tiempos que no son estacionarios
    stationary_indices = np.where(t >= stationary_time)[0]
    if len(stationary_indices) == 0:
        print(f"Error: No stationary data found in {sim_dir}")
        return None, None

    t = t[stationary_indices]
    max_amplitudes = max_amplitudes[stationary_indices]

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

    # Encontrar el punto máximo
    max_idx = np.argmax(amplitudes)
    max_omega = omegas[max_idx]
    max_amplitude = amplitudes[max_idx]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(omegas, amplitudes, "bo-", linewidth=2, markersize=8, label="Amplitud vs ω")

    # Marcar el punto máximo en rojo
    ax.plot(max_omega, max_amplitude, "ro", markersize=10, label=f"Máximo (ω={max_omega:.2f})")

    ax.set_xlabel("ω [rad/s]")
    ax.set_ylabel("Amplitud máxima absoluta |y| [m]")
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend()

    plot_path = os.path.join(sim_dirs[0], "amplitud_maxima_vs_w.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()
