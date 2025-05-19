import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from utils.utils import load_data, read_config, save_plot


def get_max_amplitudes(sim_dir):
    """Get maximum amplitudes and parameters for a simulation directory."""
    config = read_config(sim_dir)

    # La simulación tiene que ser de osciladores acoplados
    if config["oscillatorType"] != "coupled":
        print(f"Error: Directory '{sim_dir}' is not a coupled oscillator simulation")
        return None, None, None, None

    # Extraer parámetros
    k = config["parameters"]["k"]
    omega = config["parameters"]["omega"]

    # Chequeamos si ya se había creado el archivo de máximas amplitudes
    max_amplitudes_file = os.path.join(sim_dir, "max_amplitudes.txt")
    if os.path.exists(max_amplitudes_file):
        data = np.loadtxt(max_amplitudes_file)
        t = data[:, 0]
        max_amplitudes = data[:, 1]

    # Sino buscamos por archivo de simulación y lo calculamos
    else:
        sim_file = "output.txt"
        data_file = os.path.join(sim_dir, sim_file)
        t, positions = load_data(data_file)

        if t is None or positions is None:
            print(f"Error: Could not load valid data from {sim_dir}")
            return None, None, None, None

        # Calculamos la máxima amplitud absoluta para cada instante de tiempo
        max_amplitudes = np.max(np.abs(positions), axis=1)

        # Guardamos las amplitudes máximas junto con el tiempo
        np.savetxt(max_amplitudes_file, np.column_stack((t, max_amplitudes)))

    return t, max_amplitudes, k, omega


def main():
    if len(sys.argv) < 2:
        print("Usage: python amplitud_maxima_vs_t_multiple.py <sim_dir1> [sim_dir2 sim_dir3 ...]")
        sys.exit(1)

    sim_dirs = sys.argv[1:]

    # Recolectar datos de todas las simulaciones
    data = []
    for sim_dir in sim_dirs:
        result = get_max_amplitudes(sim_dir)
        if result[0] is not None:  # Si los datos son válidos
            data.append(result)

    if not data:
        print("Error: No valid data found in any simulation directory")
        sys.exit(1)

    # Ordenar por k para que la leyenda quede ordenada
    data.sort(key=lambda x: x[2], reverse=True)  # Ordenar por k (índice 2)

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    for i, (t, max_amplitudes, k, omega) in enumerate(data):
        label = f"k = {k:.1f}, ω = {omega:.2f}"
        ax.plot(t, max_amplitudes, linewidth=2, label=label, alpha=0.8)

    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Amplitud máxima absoluta |y| [m]")
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(title="Parámetros", bbox_to_anchor=(1.05, 1), loc="upper left")

    # Ajustar el layout para que quepa la leyenda
    plt.tight_layout()

    # Guardar en el directorio del primer argumento
    plot_path = os.path.join(sim_dirs[0], "amplitud_maxima_vs_t_multiple.png")
    save_plot(fig, plot_path)
    plt.show()


if __name__ == "__main__":
    main()

