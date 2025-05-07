import numpy as np
import glob
import matplotlib.pyplot as plt

def get_amplitude(filename, transient=100):
    data = np.loadtxt(filename)
    t, y = data[:,0], data[:,1]
    # Discard transient
    y_steady = y[t > transient]
    # Amplitude as half the peak-to-peak in steady state
    amp = (np.max(y_steady) - np.min(y_steady)) / 2
    return amp

# Adjust the path to your results directory
files = sorted(glob.glob("../results/ej2/coupled_omega_*.txt"))
omegas = []
amplitudes = []

for f in files:
    # Extract omega from filename
    omega = float(f.split("_")[-1].replace(".txt", ""))
    amp = get_amplitude(f)
    omegas.append(omega)
    amplitudes.append(amp)

omegas = np.array(omegas)
amplitudes = np.array(amplitudes)

plt.figure()
plt.plot(omegas, amplitudes, 'o-')
plt.xlabel(r'$\omega$')
plt.ylabel('Amplitud (m)')
plt.title('Amplitud vs. Frecuencia')
plt.grid()
plt.show()

# Resonance frequency
resonance_omega = omegas[np.argmax(amplitudes)]
print(f"Resonance frequency ω₀ ≈ {resonance_omega:.4f}")