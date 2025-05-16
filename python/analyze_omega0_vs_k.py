import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

def load_data(filename):
    data = np.loadtxt(filename)
    times = data[:, 0]
    last_particle = data[:, -1]
    return times, last_particle

def calculate_amplitude(y):
    peaks_pos, _ = find_peaks(y)
    peaks_neg, _ = find_peaks(-y)
    
    if len(peaks_pos) == 0 or len(peaks_neg) == 0:
        return 0
    
    avg_max = np.mean(y[peaks_pos])
    avg_min = np.mean(y[peaks_neg])
    return (avg_max - avg_min) / 2

def power_law(k, a):
    return a * np.sqrt(k)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_omega0_vs_k.py <results_directory>")
        sys.exit(1)

    results_dir = sys.argv[1]
    k_values = []
    resonance_omegas = []

    # Agrupar archivos por k
    k_groups = {}
    for filename in os.listdir(results_dir):
        if filename.startswith("coupled_omega_"):
            parts = filename.split("_")
            omega = float(parts[2])
            k = float(parts[4].replace(".txt", ""))
            
            if k not in k_groups:
                k_groups[k] = []
            k_groups[k].append((omega, filename))

    # Para cada k, encontrar la frecuencia de resonancia
    for k, files in k_groups.items():
        omegas = []
        amplitudes = []
        
        for omega, filename in files:
            filepath = os.path.join(results_dir, filename)
            times, positions = load_data(filepath)
            amplitude = calculate_amplitude(positions)
            omegas.append(omega)
            amplitudes.append(amplitude)

        # Encontrar omega de resonancia (máxima amplitud)
        max_idx = np.argmax(amplitudes)
        k_values.append(k)
        resonance_omegas.append(omegas[max_idx])

    # Ordenar por k
    k_values = np.array(k_values)
    resonance_omegas = np.array(resonance_omegas)
    sort_idx = np.argsort(k_values)
    k_values = k_values[sort_idx]
    resonance_omegas = resonance_omegas[sort_idx]

    # Ajustar ley de potencias
    popt, pcov = curve_fit(power_law, k_values, resonance_omegas)
    a_fit = popt[0]

    # Graficar resultados
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, resonance_omegas, 'o', label='Datos experimentales')
    
    # Graficar ajuste
    k_fit = np.linspace(min(k_values), max(k_values), 100)
    plt.plot(k_fit, power_law(k_fit, a_fit), '-', 
             label=f'Ajuste: ω₀ = {a_fit:.3f}√k')
    
    plt.xlabel('Constante elástica k (N/m)')
    plt.ylabel('Frecuencia de resonancia ω₀ (rad/s)')
    plt.title('Relación entre frecuencia de resonancia y constante elástica')
    plt.grid(True)
    plt.legend()

    # Usar escala logarítmica
    plt.xscale('log')
    plt.yscale('log')

    # Guardar gráfico
    graphics_dir = os.path.join(os.path.dirname(results_dir), "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plt.savefig(os.path.join(graphics_dir, "omega0_vs_k.png"), dpi=300)
    plt.show()

    print(f"Coeficiente de ajuste a = {a_fit:.3f}")
    print(f"La relación encontrada es: ω₀ = {a_fit:.3f}√k")

if __name__ == "__main__":
    main() 