import json
import os
import sys

import numpy as np


def read_config(simulation_dir):
    config_path = os.path.join(simulation_dir, "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.json not found in {simulation_dir}")

    with open(config_path, "r") as f:
        return json.load(f)


def validate_simulation_dir():
    if len(sys.argv) != 2:
        print("Usage: python script.py <simulation_directory>")
        sys.exit(1)

    sim_dir = sys.argv[1]
    if not os.path.exists(sim_dir):
        print(f"Directory '{sim_dir}' does not exist")
        sys.exit(1)

    return sim_dir


def save_plot(fig, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    print(f"Plot saved to {filepath}")


def load_data(filename):
    try:
        data = np.loadtxt(filename)
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            print("Error: Data file contains NaN or Inf values")
            return None, None

        return data[:, 0], data[:, 1:]  # tiempo y todas las posiciones

    except Exception as e:
        print(f"Error loading data file {filename}: {e}")
        return None, None


def mce(num, ana):
    return np.mean((num - ana) ** 2)
