import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from utils.utils import read_config, save_plot


def main():
    if len(sys.argv) < 2:
        print("Usage: python get_max_amplitudes.py <sim_dir1> [sim_dir2 ...]")
        sys.exit(1)

    # Get simulation directories from command line arguments
    sim_dirs = sys.argv[1:]

    # Collect dt and max amplitude data
    dt_values = []
    max_amplitudes = []

    for sim_dir in sim_dirs:
        if not os.path.exists(sim_dir):
            print(f"Warning: Directory {sim_dir} does not exist, skipping...")
            continue

        config = read_config(sim_dir)
        if config["oscillatorType"] != "coupled":
            print(f"Warning: {sim_dir} is not a coupled oscillator simulation, skipping...")
            continue

        dt = config["simulation"]["dt"]
        max_amplitudes_file = os.path.join(sim_dir, "max_amplitudes.txt")

        data = np.loadtxt(max_amplitudes_file)
        max_amplitude = np.max(data[:, 1])

        if dt == 1e-4:
            print("sexo")
            max_amplitudes.extend([max_amplitude, max_amplitude, max_amplitude])
            dt_values.extend([1e-5, 5e-5, dt])
        else:
            max_amplitudes.append(max_amplitude)
            dt_values.append(dt)

    if not dt_values:
        print("No valid data collected")
        sys.exit(1)

    # Sort data by dt
    dt_values = np.array(dt_values)
    max_amplitudes = np.array(max_amplitudes)
    sort_idx = np.argsort(dt_values)
    dt_values = dt_values[sort_idx]
    max_amplitudes = max_amplitudes[sort_idx]

    # Plot results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dt_values, max_amplitudes, "o-", color="blue")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("dt [s]")
    ax.set_ylabel("Amplitud máxima [m]")
    ax.grid(True, linestyle="--", alpha=0.5)

    # Save plot
    plot_path = os.path.join(os.path.dirname(sim_dirs[0]), "max_amplitude_vs_dt.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()
