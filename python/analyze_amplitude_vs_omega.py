import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from scipy.signal import find_peaks

def load_data(filename):
    data = np.loadtxt(filename)
    times = data[:, 0]
    # La última partícula es la columna N
    last_particle = data[:, -1]
    return times, last_particle

def calculate_amplitude(y):
    # Encontrar picos positivos y negativos
    peaks_pos, _ = find_peaks(y)
    peaks_neg, _ = find_peaks(-y)
    
    if len(peaks_pos) == 0 or len(peaks_neg) == 0:
        return 0
    
    # Calcular amplitud como promedio de máximos y mínimos
    avg_max = np.mean(y[peaks_pos])
    avg_min = np.mean(y[peaks_neg])
    return (avg_max - avg_min) / 2

def process_directory(directory):
    print(f"\nProcesando directorio: {directory}")
    omegas = []
    amplitudes = []
    k_value = None

    # Buscar archivos de simulación
    for filename in os.listdir(directory):
        if filename.startswith("coupled_omega_"):
            print(f"Procesando archivo: {filename}")
            try:
                # Extraer omega y k del nombre del archivo
                parts = filename.split("_")
                omega = float(parts[2])
                k = float(parts[4].replace(".txt", ""))
                
                # Si es el primer archivo, guardar el valor de k
                if k_value is None:
                    k_value = k
                # Si no es el primer archivo, verificar que k sea el mismo
                elif k != k_value:
                    print(f"Advertencia: Valor de k diferente encontrado ({k} != {k_value})")
                    continue
                
                filepath = os.path.join(directory, filename)
                print(f"Omega = {omega}, k = {k}")
                
                # Cargar datos y calcular amplitud
                times, positions = load_data(filepath)
                amplitude = calculate_amplitude(positions)
                print(f"Amplitud calculada: {amplitude}")
                
                omegas.append(omega)
                amplitudes.append(amplitude)
            except Exception as e:
                print(f"Error procesando {filename}: {str(e)}")
    
    return omegas, amplitudes, k_value

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_amplitude_vs_omega.py <results_directory1> [results_directory2 ...]")
        sys.exit(1)

    all_omegas = []
    all_amplitudes = []
    k_value = None

    # Procesar cada directorio
    for directory in sys.argv[1:]:
        omegas, amplitudes, k = process_directory(directory)
        
        # Verificar que el valor de k sea consistente entre directorios
        if k_value is None:
            k_value = k
        elif k != k_value:
            print(f"Advertencia: Directorio {directory} tiene un k diferente ({k} != {k_value})")
            continue
            
        all_omegas.extend(omegas)
        all_amplitudes.extend(amplitudes)

    if not all_omegas:
        print("No se encontraron archivos válidos para procesar")
        sys.exit(1)

    print(f"\nValores de omega encontrados: {all_omegas}")
    print(f"Amplitudes correspondientes: {all_amplitudes}")

    # Ordenar por omega
    sorted_indices = np.argsort(all_omegas)
    all_omegas = np.array(all_omegas)[sorted_indices]
    all_amplitudes = np.array(all_amplitudes)[sorted_indices]

    # Crear gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(all_omegas, all_amplitudes, 'o-')
    plt.xlabel('Frecuencia ω (rad/s)')
    plt.ylabel('Amplitud (m)')
    plt.title(f'Amplitud de oscilación vs Frecuencia (k = {k_value})')
    plt.grid(True)

    # Encontrar frecuencia de resonancia
    resonance_idx = np.argmax(all_amplitudes)
    resonance_omega = all_omegas[resonance_idx]
    plt.axvline(x=resonance_omega, color='r', linestyle='--', 
                label=f'ω₀ = {resonance_omega:.2f} rad/s')
    plt.legend()

    # Guardar gráfico
    # Usar el directorio del primer argumento como base para guardar los gráficos
    base_dir = os.path.dirname(os.path.dirname(sys.argv[1]))
    graphics_dir = os.path.join(base_dir, "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plt.savefig(os.path.join(graphics_dir, "amplitude_vs_omega.png"), dpi=300)
    plt.show()

    print(f"\nFrecuencia de resonancia encontrada: {resonance_omega:.2f} rad/s")

if __name__ == "__main__":
    main() 