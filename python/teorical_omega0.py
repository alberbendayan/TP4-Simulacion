import numpy as np

# Parámetros del sistema
N = 1000
m = 0.00021
k = 102.3

# Cálculo de omega_0
omega_0 = 2 * np.sqrt(k / m) * np.sin(np.pi / (2 * (N + 1)))

print(f"Omega_0 (frecuencia natural del modo fundamental): {omega_0:.4f} rad/s")
