import os
import matplotlib.pyplot as plt
import numpy as np
import re

# 📁 Directorio donde están los resultados
RESULTS_DIR = '../results/ej2_500/'

file_pattern = re.compile(r'coupled_omega_([\d.]+)\.txt')

frequencies = []
amplitudes = []

# 🔍 Recorremos todos los archivos del directorio
for filename in os.listdir(RESULTS_DIR):
    match = file_pattern.match(filename)
    if match:
        omega = float(match.group(1))
        print(f'Processing {filename}... and omega = {omega}')
        frequencies.append(omega)
        
        filepath = os.path.join(RESULTS_DIR, filename)
        y_values = []

        with open(filepath) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    y = float(parts[1])
                    y_values.append(abs(y))
        
        max_amp = max(y_values)
        amplitudes.append(max_amp)

# 📊 Ordenamos por frecuencia (por si leyo desordenado)
freqs, amps = zip(*sorted(zip(frequencies, amplitudes)))

# 🎨 Graficamos
plt.figure(figsize=(10, 6))
plt.plot(freqs, amps, marker='o', linestyle='-', color='b')
plt.xlabel('Frecuencia de forzamiento ω')
plt.ylabel('Amplitud máxima de y₅₀₀')
plt.title('Curva de resonancia')
plt.grid(True)
plt.tight_layout()
plt.show()
