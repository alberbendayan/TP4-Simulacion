import glob

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def power_law(x, a):
    return a * x**0.5


def get_amplitude(filename, transient=100):
    data = np.loadtxt(filename)
    t, y = data[:, 0], data[:, 1]
    # Discard transient
    y_steady = y[t > transient]
    # Amplitude as half the peak-to-peak in steady state
    amp = (np.max(y_steady) - np.min(y_steady)) / 2
    return amp


k_values = [1e2, 5e2, 1e3, 5e3, 1e4]  # Example k values
resonance_omegas = []
resonance_omegas = []

for k in k_values:
    files = sorted(glob.glob(f"../results/ej2_k{k:.0e}/coupled_omega_*.txt"))
    omegas = []
    amplitudes = []
    for f in files:
        omega = float(f.split("_")[-1].replace(".txt", ""))
        amp = get_amplitude(f)
        omegas.append(omega)
        amplitudes.append(amp)
    omegas = np.array(omegas)
    amplitudes = np.array(amplitudes)
    resonance_omega = omegas[np.argmax(amplitudes)]
    resonance_omegas.append(resonance_omega)
    print(f"k={k:.0e}, ω₀={resonance_omega:.4f}")

k_values = np.array(k_values)
resonance_omegas = np.array(resonance_omegas)

popt, _ = curve_fit(power_law, k_values, resonance_omegas)
a_fit = popt[0]

plt.figure()
plt.plot(k_values, resonance_omegas, "o", label="Datos")
plt.plot(
    k_values,
    power_law(k_values, a_fit),
    "-",
    label=rf"Ajuste: $a \cdot k^{{1/2}},\ a={a_fit:.3f}$",
)
plt.xlabel("k (N/m)")
plt.ylabel(r"Frecuencia de resonancia $\omega_0$")
plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.grid()
plt.title("Ajuste de ley de potencias")
plt.show()
