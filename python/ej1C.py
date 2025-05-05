import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt


def cargar_datos(path_archivo):
    data = np.loadtxt(path_archivo)
    tiempo = data[:, 0]
    numerica = data[:, 1]
    analitica = data[:, 3]
    return numerica, analitica


def error_cuadratico_medio(num, ana):
    return np.mean((num - ana) ** 2)


def extraer_dt_de_nombre(nombre_dir):
    # Intenta extraer dt de nombres tipo "dt_0.01", "dt0.001", etc.
    for parte in nombre_dir.replace('-', '_').split('_'):
        try:
            return float(parte)
        except ValueError:
            continue
    raise ValueError(f"No se pudo extraer dt del nombre del directorio: {nombre_dir}")


def main():
    parser = argparse.ArgumentParser(description="Estudia cómo disminuye el ECM al disminuir dt.")
    parser.add_argument("directorios", nargs='+', help="Lista de carpetas con archivos output_*.txt")
    args = parser.parse_args()

    metodos = {
        "Gear predictor Corrector": "output_gear.txt",
        "Euler-Predictor-Corrector Modified": "output_beeman.txt",
        "Verlet": "output_verlet.txt",
    }

    errores_por_metodo = {nombre: [] for nombre in metodos}
    dts = []

    for directorio in args.directorios:
        try:
            dt = extraer_dt_de_nombre(os.path.basename(directorio))
            dts.append(dt)

            for nombre_metodo, archivo in metodos.items():
                path_archivo = os.path.join(directorio, archivo)
                numerica, analitica = cargar_datos(path_archivo)
                ecm = error_cuadratico_medio(numerica, analitica)
                errores_por_metodo[nombre_metodo].append(ecm)

        except Exception as e:
            print(f"Error en '{directorio}': {e}", file=sys.stderr)

    # Ordenar por dt creciente
    dts, errores_ordenados = zip(*sorted(zip(dts, zip(*[errores_por_metodo[m] for m in metodos]))))
    dts = np.array(dts)
    errores_por_metodo = {
        metodo: np.array(errores) for metodo, errores in zip(metodos, zip(*errores_ordenados))
    }

    # Plot
    plt.figure(figsize=(10, 6))
    for nombre, errores in errores_por_metodo.items():
        plt.plot(dts, errores, marker='o', label=nombre)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Paso de integración dt (log)")
    plt.ylabel("Error cuadrático medio (log)")
    plt.title("Disminución del error con respecto al paso dt")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("error_vs_dt.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
