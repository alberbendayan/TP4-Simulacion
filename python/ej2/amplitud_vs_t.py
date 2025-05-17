import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from utils.utils import read_config, validate_simulation_dir

def load_data(filename):
    try:
        data = np.loadtxt(filename)
        if data.shape[1] == 3:  # Only last particle data
            print("Warning: Data file only contains last particle position. Cannot analyze full system.")
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

    # Calculate maximum amplitude for each time step
    max_amplitudes = np.max(np.abs(positions), axis=1)

    # Create figure and axis
    plt.figure(figsize=(12, 6))
    
    # Plot the maximum amplitude over time
    plt.plot(t, max_amplitudes, 'b-', linewidth=2)
    
    # Set up the plot
    plt.xlabel('Time [s]')
    plt.ylabel('Maximum Amplitude [m]')
    plt.title(f'Maximum Amplitude Over Time\nk = {config["parameters"]["k"]}, ω = {config["parameters"]["omega"]}')
    plt.grid(True)

    # Create graphics directory in results
    graphics_dir = os.path.join(os.path.dirname(os.path.dirname(sim_dir)), "graphics")
    os.makedirs(graphics_dir, exist_ok=True)

    # Save the plot
    timestamp = os.path.basename(sim_dir)
    plt.savefig(os.path.join(graphics_dir, f'max_amplitude_{timestamp}.png'), dpi=300, bbox_inches='tight')
    print(f"Plot saved to {graphics_dir}/max_amplitude_{timestamp}.png")

    plt.show()

if __name__ == "__main__":
    main() 