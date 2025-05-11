import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from utils import read_config, validate_simulation_dir

def load_data(filename):
    data = np.loadtxt(filename)
    if data.shape[1] == 3:  # Only last particle data
        print("Warning: Data file only contains last particle position. Cannot animate full system.")
        return None, None
    return data[:, 0], data[:, 1:]  # time and all positions

def main():
    # Get simulation directory from command line
    sim_dir = validate_simulation_dir()

    # Read configuration
    config = read_config(sim_dir)

    # Verify this is a coupled oscillator simulation
    if config['oscillatorType'] != 'coupled':
        print("Error: This script is for coupled oscillator simulations")
        sys.exit(1)

    # Get the first .txt file in the directory
    txt_files = [f for f in os.listdir(sim_dir) if f.endswith('.txt')]
    if not txt_files:
        print("No data files found in the directory")
        sys.exit(1)
    
    data_file = os.path.join(sim_dir, txt_files[0])
    t, positions = load_data(data_file)
    
    if t is None:
        print("Please run the simulation with the saveAll parameter set to true:")
        print("java Main 2 <omega> <k> true")
        sys.exit(1)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create x-axis positions for particles (0 to N-1)
    N = positions.shape[1]  # number of particles
    x_positions = np.arange(N)
    
    # Initialize the line plot
    line, = ax.plot([], [], 'b-', lw=2)
    points, = ax.plot([], [], 'ro', markersize=4)
    
    # Set up the plot
    ax.set_xlim(-1, N)
    y_min = np.min(positions)
    y_max = np.max(positions)
    ax.set_ylim(y_min * 1.1, y_max * 1.1)
    ax.set_xlabel('Particle Index')
    ax.set_ylabel('Position [m]')
    ax.set_title(f'Coupled Oscillator System Animation (k = {config["parameters"]["k"]})')
    ax.grid(True)

    def init():
        # line.set_data([], [])
        points.set_data([], [])
        return line, points

    def animate(frame):
        # Get positions for all particles at this frame
        y_values = positions[frame]
        # line.set_data(x_positions, y_values)
        points.set_data(x_positions, y_values)
        return line, points

    # Create animation with fewer frames to make it smoother
    frames = min(len(t), 10000)  # Increase number of frames for smoother animation
    frame_indices = np.linspace(0, len(t)-1, frames, dtype=int)
    
    # Create animation with slower interval (100ms between frames)
    anim = FuncAnimation(fig, animate, init_func=init, frames=frame_indices,
                        interval=10, blit=True)

    # Create graphics directory in results
    graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
    os.makedirs(graphics_dir, exist_ok=True)

    # Save animation with lower fps for slower playback
    timestamp = os.path.basename(sim_dir)
    try:
        anim.save(os.path.join(graphics_dir, f'coupled_oscillator_animation_{timestamp}.mp4'),
                 writer='ffmpeg', fps=60)  # Lower fps for slower playback
    except Exception as e:
        print(f"Warning: Could not save animation: {e}")
        print("Showing animation instead...")

    plt.show()

if __name__ == "__main__":
    main() 