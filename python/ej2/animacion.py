import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from utils.utils import load_data, read_config, validate_simulation_dir


def main():
    sim_dir = validate_simulation_dir()
    config = read_config(sim_dir)

    # La simulación tiene que ser de osciladores acoplados
    if config["oscillatorType"] != "coupled":
        print("Error: This script is for coupled oscillator simulations")
        sys.exit(1)

    sim_file = "output.txt"
    data_file = os.path.join(sim_dir, sim_file)
    t, positions = load_data(data_file)

    if t is None or positions is None:
        print("Error: Could not load valid data from the file")
        sys.exit(1)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Posiciones en el eje x de 0 a n-1
    n = positions.shape[1]
    x_positions = np.arange(n)

    (line,) = ax.plot([], [], "c-", lw=2)  # Ondita
    (points,) = ax.plot([], [], "ro", markersize=4, alpha=0.2)  # Partículas

    ax.set_xlim(-1, n)
    y_min = np.min(positions)
    y_max = np.max(positions)

    if np.isnan(y_min) or np.isnan(y_max) or np.isinf(y_min) or np.isinf(y_max):
        print("Error: Invalid position values in data")
        sys.exit(1)

    margin = (y_max - y_min) * 0.1
    if margin < 1e-10:
        margin = 0.1

    ax.set_ylim(y_min - margin, y_max + margin)
    ax.set_xlabel("Partícula")
    ax.set_ylabel("Posición [m]")
    ax.grid(True, linestyle="--", alpha=0.7)

    def init():
        line.set_data([], [])
        points.set_data([], [])
        return line, points

    def animate(frame):
        y_values = positions[frame]
        line.set_data(x_positions, y_values)
        points.set_data(x_positions, y_values)
        return line, points

    # Calculamos la duración total de la simulación
    total_time = config["simulation"]["tMax"]
    dt = config["simulation"]["dt"]
    total_frames = int(total_time / dt)
    frames = min(total_frames, 1000)  # Máximo 1000 frames
    frame_indices = np.linspace(0, len(t) - 1, frames, dtype=int)

    anim = FuncAnimation(fig, animate, init_func=init, frames=frame_indices, interval=20)
    animation_path = os.path.join(sim_dir, "animation.mp4")
    anim.save(animation_path, writer="ffmpeg", fps=50, dpi=100)
    print(f"Animation saved to {animation_path}")


if __name__ == "__main__":
    main()
