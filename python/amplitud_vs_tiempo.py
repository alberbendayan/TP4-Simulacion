import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from utils import read_config, validate_simulation_dir

def plot_amplitude_vs_time(filename):
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

    # Calcular la envolvente usando ventana móvil
    window_size = int(len(t) / 100)  # Ajustar según necesidad
    if window_size % 2 == 0:
        window_size += 1
    
    max_envelope = []
    min_envelope = []
    times_envelope = []
    
    for i in range(0, len(t) - window_size, window_size):
        window = y[i:i+window_size]
        max_envelope.append(np.max(np.abs(window)))
        min_envelope.append(np.min(np.abs(window)))
        times_envelope.append(t[i + window_size//2])

    # Crear el gráfico
    plt.figure(figsize=(12, 8))
    
    # Graficar la señal original
    plt.plot(t, y, 'b-', alpha=0.3, label='Señal original')
    
    # Graficar la envolvente
    plt.plot(times_envelope, max_envelope, 'r-', linewidth=2, label='Amplitud máxima')
    
    # Configurar el gráfico
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud [m]')
    omega = float(os.path.basename(filename).split('_')[2])
    plt.title(f'Evolución de la amplitud (ω = {omega} rad/s)')
    plt.grid(True)
    plt.legend()
    
    # Guardar el gráfico
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(filename)))
    graphics_dir = os.path.join(base_dir, "graphics")
    os.makedirs(graphics_dir, exist_ok=True)
    plt.savefig(os.path.join(graphics_dir, f"amplitud_vs_tiempo_omega_{omega:.2f}.png"), dpi=300)
    
    # Mostrar información relevante
    print(f"Tiempo total de simulación: {max(t):.1f} s")
    print(f"Amplitud máxima final: {max_envelope[-1]:.6e} m")
    print(f"Amplitud máxima global: {max(max_envelope):.6e} m")
    
    return plt

def main():
    if len(sys.argv) < 2:
        print("Uso: python amplitud_vs_tiempo.py <directorio_simulacion1> [directorio_simulacion2 ...]")
        sys.exit(1)

    for sim_dir in sys.argv[1:]:
        if not os.path.exists(sim_dir):
            print(f"Error: El directorio '{sim_dir}' no existe")
            continue
            
        # Procesar cada archivo en el directorio
        for filename in os.listdir(sim_dir):
            if filename.startswith("coupled_omega_") and filename.endswith(".txt"):
                full_path = os.path.join(sim_dir, filename)
                plt = plot_amplitude_vs_time(full_path)
                plt.show()
                plt.close()

if __name__ == "__main__":
    main() 