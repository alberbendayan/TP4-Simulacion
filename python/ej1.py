import matplotlib.pyplot as plt
import numpy as np


def cargar_datos(nombre_archivo):
    data = np.loadtxt(nombre_archivo)
    tiempo = data[:, 0]
    numerica = data[:, 1]
    analitica = data[:, 3]
    return tiempo, numerica, analitica


def error_cuadratico_medio(num, ana):
    return np.mean((num - ana) ** 2)


# Archivos de salida de los métodos
archivos = {
    "Gear predictor Corrector": "../output_gear.txt",
    "Euler-Predictor-Corrector Modified": "../output_beeman.txt",
    "Verlet": "../output_verlet.txt",
}

# Colores
colores = {
    "Analítica": "blue",
    "Euler-Predictor-Corrector Modified": "magenta",
    "Verlet": "cyan",
    "Gear predictor Corrector": "black",
}

plt.figure(figsize=(10, 6))

# Subplot 1: todo el rango
for nombre, archivo in archivos.items():
    t, num, ana = cargar_datos(archivo)
    plt.plot(t, num, label=nombre, color=colores[nombre])

plt.plot(t, ana, label="Analítica", color="blue")

plt.xlabel("Tiempo [s]")
plt.ylabel("Posición [m]")
plt.title("Comparación general")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("comparacion_metodos.png", dpi=300)
plt.show()

# Imprimir errores
print("\nErrores cuadráticos medios (ECM):")
for nombre, archivo in archivos.items():
    _, num, ana = cargar_datos(archivo)
    ecm = error_cuadratico_medio(num, ana)
    print(f"{nombre}: {ecm:.6e}")
