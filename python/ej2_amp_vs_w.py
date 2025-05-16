import numpy as np
import os
import re
import sys
import matplotlib.pyplot as plt
from utils import read_config, validate_simulation_dir
from scipy.signal import find_peaks
from pathlib import Path
import json

def get_amplitude(filename, transient=12):
    print(f"\nAnalizando archivo: {filename}")
    
    # Cargar datos
    data = np.loadtxt(filename)
    t = data[:, 0]  # Primera columna siempre es tiempo
    
    # Si hay más de 3 columnas, estamos en modo saveAll=true
    # y queremos la última partícula (última columna)
    if data.shape[1] > 3:
        y = data[:, -1]  # Última columna (posición de la última partícula)
        print("Modo saveAll=true, usando última columna")
    else:
        y = data[:, 1]  # Segunda columna (posición)
        print("Modo saveAll=false, usando segunda columna")
    
    # Graficar la señal completa y marcar el transiente
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Gráfico superior: señal completa
    ax1.plot(t, y, 'b-', label='Señal completa', alpha=0.7)
    ax1.axvline(x=transient, color='r', linestyle='--', label=f'Transiente ({transient} s)')
    ax1.set_xlabel('Tiempo [s]')
    ax1.set_ylabel('Posición [m]')
    ax1.set_title(f'Señal completa\n{os.path.basename(filename)}')
    ax1.grid(True)
    ax1.legend()
    
    # Descartar transiente
    steady_mask = t > transient
    t_steady = t[steady_mask]
    y_steady = y[steady_mask]
    
    # Gráfico inferior: estado estacionario en detalle
    ax2.plot(t_steady, y_steady, 'g-', label='Estado estacionario', linewidth=1.5)
    ax2.set_xlabel('Tiempo [s]')
    ax2.set_ylabel('Posición [m]')
    ax2.set_title('Estado estacionario (detalle)')
    ax2.grid(True)
    
    # Marcar máximos y mínimos
    peaks_pos, _ = find_peaks(y_steady)
    peaks_neg, _ = find_peaks(-y_steady)
    if len(peaks_pos) > 0:
        ax2.plot(t_steady[peaks_pos], y_steady[peaks_pos], 'ro', label='Máximos')
    if len(peaks_neg) > 0:
        ax2.plot(t_steady[peaks_neg], y_steady[peaks_neg], 'ko', label='Mínimos')
    ax2.legend()
    
    plt.tight_layout()
    
    # Guardar el gráfico
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(filename)))
    graphics_dir = os.path.join(base_dir, "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plt.savefig(os.path.join(graphics_dir, f"analisis_detallado_{os.path.basename(filename)}.png"), dpi=300)
    plt.close()
    
    print(f"Tiempo total de simulación: {max(t):.1f} s")
    print(f"Número total de puntos: {len(y)}")
    print(f"Puntos después del transiente: {len(y_steady)}")
    
    if len(y_steady) < 2:
        print("ADVERTENCIA: No hay suficientes puntos después del transiente!")
        return 0
    
    # Calcular amplitud usando máximos y mínimos
    max_val = np.max(y_steady)
    min_val = np.min(y_steady)
    amp = (max_val - min_val) / 2
    
    print(f"Valor máximo: {max_val}")
    print(f"Valor mínimo: {min_val}")
    print(f"Amplitud calculada: {amp}")
    
    # Calcular período aproximado si hay suficientes picos
    if len(peaks_pos) >= 2:
        periodos = np.diff(t_steady[peaks_pos])
        periodo_promedio = np.mean(periodos)
        print(f"Período promedio: {periodo_promedio:.3f} s")
        print(f"Frecuencia medida: {2*np.pi/periodo_promedio:.3f} rad/s")
    
    return amp

def process_directory(sim_dir):
    # Read configuration
    config = read_config(sim_dir)

    # Verify this is a coupled oscillator simulation
    if config['oscillatorType'] != 'coupled':
        print(f"Error: Directory {sim_dir} is not a coupled oscillator simulation")
        return None, None, None

    # Get all files matching the pattern
    file_pattern = re.compile(r'coupled_omega_([\d.]+)_k_([\d.]+)\.txt')
    files = [f for f in os.listdir(sim_dir) if file_pattern.match(f)]
    files.sort()

    omegas = []
    amplitudes = []

    print(f"\nProcesando directorio: {sim_dir}")
    for f in files:
        # Extract omega from filename
        match = file_pattern.match(f)
        omega = float(match.group(1))
        amp = get_amplitude(os.path.join(sim_dir, f))
        omegas.append(omega)
        amplitudes.append(amp)
        print(f"ω = {omega:.3f}, Amplitud = {amp:.6f}")

    return np.array(omegas), np.array(amplitudes), config

def extract_omega_from_filename(filename):
    match = re.search(r'omega_(\d+\.\d+)', filename)
    return float(match.group(1)) if match else None

def load_simulation_data(file_path):
    data = np.loadtxt(file_path)
    time = data[:, 0]
    # Todas las posiciones excepto el tiempo
    positions = data[:, 1:]
    return time, positions

def calculate_amplitude(time, positions, t_transient=15.0):
    # Encontrar índices después del transitorio
    steady_state_idx = np.where(time > t_transient)[0]
    
    # Obtener posiciones en estado estacionario
    steady_state_pos = positions[steady_state_idx]
    
    # Calcular amplitud para cada partícula
    amplitudes = (np.max(steady_state_pos, axis=0) - np.min(steady_state_pos, axis=0)) / 2
    
    # Retornar la amplitud de la última partícula
    return amplitudes[-1]

def analyze_resonance(base_dir):
    # Encontrar todos los archivos de simulación
    simulation_files = list(Path(base_dir).glob('coupled_omega_*.txt'))
    
    omegas = []
    amplitudes = []
    
    for file_path in simulation_files:
        omega = extract_omega_from_filename(str(file_path))
        if omega is not None:
            time, positions = load_simulation_data(file_path)
            amplitude = calculate_amplitude(time, positions)
            
            omegas.append(omega)
            amplitudes.append(amplitude)
    
    # Ordenar por omega
    sorted_indices = np.argsort(omegas)
    omegas = np.array(omegas)[sorted_indices]
    amplitudes = np.array(amplitudes)[sorted_indices]
    
    # Encontrar la frecuencia de resonancia
    resonance_idx = np.argmax(amplitudes)
    omega_0 = omegas[resonance_idx]
    max_amplitude = amplitudes[resonance_idx]
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(omegas, amplitudes, 'b-', label='Amplitud')
    plt.plot(omega_0, max_amplitude, 'ro', label=f'Resonancia (ω₀ = {omega_0:.2f})')
    
    plt.xlabel('Frecuencia ω (rad/s)')
    plt.ylabel('Amplitud (m)')
    plt.title('Amplitud vs Frecuencia')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Guardar datos
    results = {
        'omega_0': float(omega_0),
        'max_amplitude': float(max_amplitude),
        'data': {
            'omegas': omegas.tolist(),
            'amplitudes': amplitudes.tolist()
        }
    }
    
    # Guardar gráfico
    plt.savefig(Path(base_dir) / 'amplitude_vs_omega.png')
    
    # Guardar resultados en JSON
    with open(Path(base_dir) / 'resonance_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Frecuencia de resonancia (ω₀): {omega_0:.2f} rad/s")
    print(f"Amplitud máxima: {max_amplitude:.6f} m")
    
    return omega_0, max_amplitude

def main():
    if len(sys.argv) < 2:
        print("Uso: python ej2_amp_vs_w.py <directorio1> <directorio2> ...")
        sys.exit(1)

    # Procesar todos los directorios dados como argumentos
    all_omegas = []
    all_amplitudes = []

    for sim_dir in sys.argv[1:]:
        if not os.path.exists(sim_dir):
            print(f"Error: El directorio {sim_dir} no existe")
            continue

        # Procesar cada archivo en el directorio
        for file in os.listdir(sim_dir):
            if file.startswith("coupled_omega_") and file.endswith(".txt"):
                file_path = os.path.join(sim_dir, file)
                omega = extract_omega_from_filename(file)
                if omega is not None:
                    time, positions = load_simulation_data(file_path)
                    amplitude = calculate_amplitude(time, positions, t_transient=5.0)
                    all_omegas.append(omega)
                    all_amplitudes.append(amplitude)
                    print(f"Procesado ω = {omega:.3f}, amplitud = {amplitude:.6f}")

    if not all_omegas:
        print("No se encontraron datos para procesar")
        return

    # Convertir a arrays y ordenar por omega
    all_omegas = np.array(all_omegas)
    all_amplitudes = np.array(all_amplitudes)
    sort_idx = np.argsort(all_omegas)
    all_omegas = all_omegas[sort_idx]
    all_amplitudes = all_amplitudes[sort_idx]

    # Encontrar la frecuencia de resonancia
    resonance_idx = np.argmax(all_amplitudes)
    omega_0 = all_omegas[resonance_idx]
    max_amplitude = all_amplitudes[resonance_idx]

    # Crear gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(all_omegas, all_amplitudes, 'b.-', label='Amplitud')
    plt.plot(omega_0, max_amplitude, 'ro', label=f'Resonancia (ω₀ = {omega_0:.2f})')

    plt.xlabel('Frecuencia ω (rad/s)')
    plt.ylabel('Amplitud (m)')
    plt.title('Amplitud vs Frecuencia')
    plt.grid(True)
    plt.legend()

    # Guardar resultados
    results_dir = os.path.join(os.path.dirname(sys.argv[1]), "results")
    os.makedirs(results_dir, exist_ok=True)

    # Guardar gráfico
    plt.savefig(os.path.join(results_dir, 'amplitude_vs_omega.png'))
    plt.close()

    # Guardar datos en CSV
    results_data = np.column_stack((all_omegas, all_amplitudes))
    np.savetxt(os.path.join(results_dir, 'amplitude_vs_omega.csv'), 
               results_data, 
               header='omega,amplitude', 
               delimiter=',',
               comments='')

    print(f"\nResultados:")
    print(f"Frecuencia de resonancia (ω₀): {omega_0:.2f} rad/s")
    print(f"Amplitud máxima: {max_amplitude:.6f} m")
    print(f"\nResultados guardados en: {results_dir}")

if __name__ == "__main__":
    main()