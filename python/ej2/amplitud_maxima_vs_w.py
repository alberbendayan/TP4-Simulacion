import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import read_config


def load_data(filename, stationary_time, dt):
    try:
        # Calculate the number of lines to skip
        lines_to_skip = int(stationary_time / dt) + 1

        # Load data skipping the initial lines
        data = np.loadtxt(filename, skiprows=lines_to_skip)

        if data.shape[1] == 3:  # Only last particle data
            print("Warning: Data file only contains last particle position. Cannot analyze full system.")
            return None, None

        # Check for NaN or Inf values
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            print("Error: Data file contains NaN or Inf values")
            return None, None

        return data[:, 0], data[:, 1:]  # time and all positions

    except Exception as e:
        print(f"Error loading data file {filename}: {e}")
        return None, None


def get_stationary_amplitude(sim_dir, stationary_time):
    # Read configuration
    config = read_config(sim_dir)
    dt = config["simulation"]["dt"]

    # Find the data file
    txt_files = [
        f
        for f in os.listdir(sim_dir)
        if f.endswith(".txt") and f.startswith("coupled_omega_")
    ]
    if not txt_files:
        print(f"No coupled oscillator data files found in {sim_dir}")
        return None, None

    data_file = os.path.join(sim_dir, txt_files[0])
    t, positions = load_data(data_file, stationary_time, dt)

    if t is None or positions is None:
        return None, None

    # Calculate max amplitudes for stationary state
    max_amplitudes = np.max(np.abs(positions), axis=1)

    # Return the maximum of maximums in stationary state and the omega value
    return np.max(max_amplitudes), config["parameters"]["omega"]


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python compare_stationary_amplitudes.py <stationary_time> <sim_dir1> [sim_dir2 sim_dir3 ...]"
        )
        sys.exit(1)

    try:
        stationary_time = float(sys.argv[1])

    except ValueError:
        print("Error: Stationary time must be a number")
        sys.exit(1)

    sim_dirs = sys.argv[2:]

    # Collect data from all simulations
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

    # Sort by omega for better visualization
    sorted_indices = np.argsort(omegas)
    omegas = np.array(omegas)[sorted_indices]
    amplitudes = np.array(amplitudes)[sorted_indices]

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(omegas, amplitudes, "bo-", linewidth=2, markersize=8)

    # Set up the plot
    plt.xlabel("ω [rad/s]")
    plt.ylabel("Maximum Amplitude in Stationary State [m]")
    plt.title(
        f"Stationary State Maximum Amplitude vs ω\n(Stationary time ≥ {stationary_time}s)"
    )
    plt.grid(True)

    # Create graphics directory
    graphics_dir = os.path.join(
        os.path.dirname(os.path.dirname(sim_dirs[0])), "graphics"
    )
    os.makedirs(graphics_dir, exist_ok=True)

    # Save the plot
    plt.savefig(
        os.path.join(graphics_dir, "amplitud_maxima_vs_w.png"),
        dpi=300,
        bbox_inches="tight",
    )
    print(f"Plot saved to {graphics_dir}/amplitud_maxima_vs_w.png")
    plt.show()


if __name__ == "__main__":
    main()
