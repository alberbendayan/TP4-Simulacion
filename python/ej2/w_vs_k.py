import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from utils.utils import read_config


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
    w0s = np.array([1.94, 4.78, 6.8, 15.3, 19.36, 21.6])

    # Fit: w0 = C * sqrt(k)
    def fit_func(k, c):
        return c * np.sqrt(k)

    popt, _ = curve_fit(fit_func, ks, w0s)
    c_fit = popt[0]

    # Plot
    plt.figure(figsize=(10, 6))
    k_fit = np.linspace(0, ks.max() * 1.05, 200)
    plt.plot(k_fit, fit_func(k_fit, c_fit), "r--", label=f"Fit: ω₀ = {c_fit:.2f}·√k")
    plt.plot(ks, w0s, "o", label="ω₀ simulada")
    plt.xlabel("k (kg/s²)")
    plt.ylabel("ω₀ (rad/s)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.show()


if __name__ == "__main__":
    main()
