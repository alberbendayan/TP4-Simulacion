import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from utils.utils import read_config, validate_simulation_dir

def load_data(filename):
    try:
        data = np.loadtxt(filename)
        if data.shape[1] == 3:  # Only last particle data
            print("Warning: Data file only contains last particle position. Cannot animate full system.")
            return None, None

        # Check for NaN or Inf values
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            print("Error: Data file contains NaN or Inf values")
            return None, None

        return data[:, 0], data[:, 1:]  # time and all positions
    except Exception as e:
        print(f"Error loading data file {filename}: {e}")
        return None, None

def main():
    # Get simulation directory from command line
    sim_dir = validate_simulation_dir()

    # Read configuration
    config = read_config(sim_dir)

    # Verify this is a coupled oscillator simulation
    if config['oscillatorType'] != 'coupled':
        print("Error: This script is for coupled oscillator simulations")
        sys.exit(1)

    # Find the data file with the correct pattern
    txt_files = [f for f in os.listdir(sim_dir) if f.endswith('.txt') and f.startswith('coupled_omega_')]
    if not txt_files:
        print("No coupled oscillator data files found in the directory")
        sys.exit(1)

    data_file = os.path.join(sim_dir, txt_files[0])
    t, positions = load_data(data_file)

    if t is None or positions is None:
        print("Error: Could not load valid data from the file")
        sys.exit(1)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create x-axis positions for particles (0 to N-1)
    N = positions.shape[1]  # number of particles
    x_positions = np.arange(N)

    # Initialize the plots
    line, = ax.plot([], [], 'b-', lw=2, alpha=0.5)  # Wave-like behavior
    points, = ax.plot([], [], 'ro', markersize=4)   # Individual particles

    # Set up the plot with safe limits
    ax.set_xlim(-1, N)
    y_min = np.min(positions)
    y_max = np.max(positions)

    # Ensure we have valid limits
    if np.isnan(y_min) or np.isnan(y_max) or np.isinf(y_min) or np.isinf(y_max):
        print("Error: Invalid position values in data")
        sys.exit(1)

    margin = (y_max - y_min) * 0.1
    # Ensure margin is not zero or too small
    if margin < 1e-10:
        margin = 0.1
    ax.set_ylim(y_min - margin, y_max + margin)
    ax.set_xlabel('Particle Index')
    ax.set_ylabel('Position [m]')
    ax.set_title(f'Coupled Oscillator System Animation\nk = {config["parameters"]["k"]}, ω = {config["parameters"]["omega"]}')
    ax.grid(True)

    def init():
        line.set_data([], [])
        points.set_data([], [])
        return line, points

    def animate(frame):
        # Get positions for all particles at this frame
        y_values = positions[frame]
        # Update both the wave line and the points
        line.set_data(x_positions, y_values)
        points.set_data(x_positions, y_values)
        return line, points

    # Create animation with appropriate number of frames
    total_time = config['simulation']['tMax']
    dt = config['simulation']['dt']
    total_frames = int(total_time / dt)
    frames = min(total_frames, 1000)  # Limit to 1000 frames max
    frame_indices = np.linspace(0, len(t)-1, frames, dtype=int)

    anim = FuncAnimation(fig, animate, init_func=init, frames=frame_indices, interval=20)

    # Create graphics directory in results
    graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
    os.makedirs(graphics_dir, exist_ok=True)

    # Save animation
    timestamp = os.path.basename(sim_dir)
    try:
        anim.save(os.path.join(graphics_dir, f'coupled_oscillator_animation_{timestamp}.mp4'),
                 writer='ffmpeg', fps=50, dpi=100)
        print(f"Animation saved to {graphics_dir}/coupled_oscillator_animation_{timestamp}.mp4")
    except Exception as e:
        print(f"Warning: Could not save animation: {e}")
        print("Showing animation instead...")

if __name__ == "__main__":
    main()
