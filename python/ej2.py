import os
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
from utils import read_config, validate_simulation_dir

# Get simulation directory from command line
sim_dir = validate_simulation_dir()

# Read configuration
config = read_config(sim_dir)

# Verify this is a coupled oscillator simulation
if config['oscillatorType'] != 'coupled':
    print("Error: This script is for coupled oscillator simulations")
    sys.exit(1)

file_pattern = re.compile(r'coupled_omega_([\d.]+)_k_([\d.]+)\.txt')

frequencies = []
amplitudes = []

# Process all files in the directory
for filename in os.listdir(sim_dir):
    match = file_pattern.match(filename)
    if match:
        omega = float(match.group(1))
        k = float(match.group(2))
        print(f'Processing {filename}... omega = {omega}, k = {k}')
        frequencies.append(omega)
        
        filepath = os.path.join(sim_dir, filename)
        y_values = []

        with open(filepath) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    y = float(parts[1])
                    y_values.append(abs(y))
        
        max_amp = max(y_values)
        amplitudes.append(max_amp)

# Sort by frequency
freqs, amps = zip(*sorted(zip(frequencies, amplitudes)))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(freqs, amps, marker='o', linestyle='-', color='b')
plt.xlabel('Frecuencia de forzamiento ω')
plt.ylabel('Amplitud máxima de y₅₀₀')
plt.title(f'Curva de resonancia (k = {config["parameters"]["k"]})')
plt.grid(True)

# Create graphics directory in results
graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
os.makedirs(graphics_dir, exist_ok=True)

# Save plot with timestamp from simulation directory
timestamp = os.path.basename(sim_dir)
plt.tight_layout()
plt.savefig(os.path.join(graphics_dir, f"resonance_curve_{timestamp}.png"), dpi=300)
plt.show()
