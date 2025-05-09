import os
import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from utils import read_config

def get_amplitude(filename, transient=100):
    data = np.loadtxt(filename)
    t, y = data[:,0], data[:,1]
    # Discard transient
    y_steady = y[t > transient]
    # Amplitude as half the peak-to-peak in steady state
    amp = (np.max(y_steady) - np.min(y_steady)) / 2
    return amp

def main():
    if len(sys.argv) < 2:
        print("Usage: python ej2_k_values.py <simulation_directory1> [simulation_directory2 ...]")
        sys.exit(1)

    k_values = []
    resonance_omegas = []

    for sim_dir in sys.argv[1:]:
        if not os.path.exists(sim_dir):
            print(f"Directory '{sim_dir}' does not exist")
            continue

        try:
            # Read configuration
            config = read_config(sim_dir)
            
            # Verify this is a coupled oscillator simulation
            if config['oscillatorType'] != 'coupled':
                print(f"Error: Directory '{sim_dir}' is not a coupled oscillator simulation")
                continue

            k = config['parameters']['k']
            k_values.append(k)

            # Get all files matching the pattern
            file_pattern = re.compile(r'coupled_omega_([\d.]+)_k_([\d.]+)\.txt')
            files = [f for f in os.listdir(sim_dir) if file_pattern.match(f)]
            files.sort()

            omegas = []
            amplitudes = []

            for f in files:
                match = file_pattern.match(f)
                omega = float(match.group(1))
                amp = get_amplitude(os.path.join(sim_dir, f))
                omegas.append(omega)
                amplitudes.append(amp)

            omegas = np.array(omegas)
            amplitudes = np.array(amplitudes)
            resonance_omega = omegas[np.argmax(amplitudes)]
            resonance_omegas.append(resonance_omega)
            print(f"k={k:.0e}, ω₀={resonance_omega:.4f}")

        except Exception as e:
            print(f"Error processing '{sim_dir}': {e}", file=sys.stderr)

    if not k_values:
        print("No valid simulation directories found")
        sys.exit(1)

    # Sort by k value
    k_values, resonance_omegas = zip(*sorted(zip(k_values, resonance_omegas)))
    k_values = np.array(k_values)
    resonance_omegas = np.array(resonance_omegas)

    plt.figure()
    plt.plot(k_values, resonance_omegas, "o-")
    plt.xlabel("k (N/m)")
    plt.ylabel(r"Frecuencia de resonancia $\omega_0$")
    plt.title("Frecuencia de resonancia vs. k")
    plt.xscale("log")
    plt.grid()

    # Create graphics directory in results
    graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
    os.makedirs(graphics_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(os.path.join(graphics_dir, "resonance_freq_vs_k.png"), dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
