import numpy as np
import os
import re
import sys
import matplotlib.pyplot as plt
from utils import read_config, validate_simulation_dir

def get_amplitude(filename, transient=100):
    data = np.loadtxt(filename)
    t, y = data[:,0], data[:,1]
    # Discard transient
    y_steady = y[t > transient]
    # Amplitude as half the peak-to-peak in steady state
    amp = (np.max(y_steady) - np.min(y_steady)) / 2
    return amp

# Get simulation directory from command line
sim_dir = validate_simulation_dir()

# Read configuration
config = read_config(sim_dir)

# Verify this is a coupled oscillator simulation
if config['oscillatorType'] != 'coupled':
    print("Error: This script is for coupled oscillator simulations")
    sys.exit(1)

# Get all files matching the pattern
file_pattern = re.compile(r'coupled_omega_([\d.]+)_k_([\d.]+)\.txt')
files = [f for f in os.listdir(sim_dir) if file_pattern.match(f)]
files.sort()

omegas = []
amplitudes = []

for f in files:
    # Extract omega from filename
    match = file_pattern.match(f)
    omega = float(match.group(1))
    amp = get_amplitude(os.path.join(sim_dir, f))
    omegas.append(omega)
    amplitudes.append(amp)

omegas = np.array(omegas)
amplitudes = np.array(amplitudes)

plt.figure()
plt.plot(omegas, amplitudes, 'o-')
plt.xlabel(r'$\omega$')
plt.ylabel('Amplitud (m)')
plt.title(f'Amplitud vs. Frecuencia (k = {config["parameters"]["k"]})')
plt.grid()

# Create graphics directory in results
graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
os.makedirs(graphics_dir, exist_ok=True)

# Save plot with timestamp from simulation directory
timestamp = os.path.basename(sim_dir)
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, f"amplitud_vs_frecuencia_{timestamp}.png"), dpi=300)
plt.show()

# Resonance frequency
resonance_omega = omegas[np.argmax(amplitudes)]
print(f"Resonance frequency ω₀ ≈ {resonance_omega:.4f}")