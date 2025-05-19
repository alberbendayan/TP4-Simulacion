import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from utils.utils import read_config, save_plot


def extract_w0_k(sim_dir):
    config = read_config(sim_dir)
    w0 = config["parameters"]["omega"]
    k = config["parameters"]["k"]
    return w0, k


def main():
    # if len(sys.argv) < 2:
    #     print("Usage: python w0_vs_k.py <sim_dir1> [sim_dir2 sim_dir3 ...]")
    #     sys.exit(1)

    # sim_dirs = sys.argv[1:]
    # w0s = []
    # ks = []

    # for sim_dir in sim_dirs:
    #     w0, k = extract_w0_k(sim_dir)
    #     w0s.append(w0)
    #     ks.append(k)

    # w0s = np.array(w0s)
    # ks = np.array(ks)

    ks = np.array([102.3, 500, 1000, 5000, 8000, 10000])
    w0s = np.array([1.94, 4.78, 6.8, 15.3, 19.35, 21.6])

    # Fit: w0 = C * sqrt(k)
    def fit_func(k, c):
        return c * np.sqrt(k)

    popt, _ = curve_fit(fit_func, ks, w0s)
    c_fit = popt[0]

    # Calculamos el error de ajuste (suma de los cuadrados de los residuos)
    residuals = w0s - fit_func(ks, c_fit)
    adjustment_error = np.sum(residuals**2)
    print(f"Error de ajuste (E) = {adjustment_error:.4f}")

    fig, ax = plt.subplots(figsize=(10, 6))
    k_fit = np.linspace(0, ks.max() * 1.05, 200)
    ax.plot(k_fit, fit_func(k_fit, c_fit), "r--", label=f"Ajuste: ω₀ = {c_fit:.3f}·√k")
    ax.plot(ks, w0s, "o", label="ω₀ simulada")
    ax.set_xlabel("k [kg/s²]")
    ax.set_ylabel("ω₀ [rad/s]")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.7)

    plot_path = os.path.join("plots", "w_vs_k.png")
    save_plot(fig, plot_path)
    plt.show()

    # Rango de valores de c alrededor del ajuste
    c_values = np.linspace(c_fit * 0.5, c_fit * 1.5, 500)
    errors = [np.sum((w0s - fit_func(ks, c)) ** 2) for c in c_values]
    errors = np.array(errors)

    # Encontramos el mínimo (debería ser en c_fit)
    min_idx = np.argmin(errors)
    c_star = c_values[min_idx]
    E_star = errors[min_idx]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(c_values, errors, "b-", label="E(C)")
    ax.axvline(c_star, color="r", linestyle="--")
    ax.plot(c_star, E_star, "ro", label=f"Mínimo: c* = {c_star:.3f}")
    ax.set_xlabel("C")
    ax.set_ylabel("E(C)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.7)
    plot_path = os.path.join("plots", "w_vs_k_error.png")
    save_plot(fig, plot_path)
    plt.show()

    print(f"El valor óptimo es c* = {c_star:.4f} (curve_fit: {c_fit:.4f}) con error E(c*) = {E_star:.4f}")


if __name__ == "__main__":
    main()
