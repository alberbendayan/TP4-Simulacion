import json
import os
import sys

def read_config(simulation_dir):
    """
    Read and parse the config.json file from a simulation directory.
    
    Args:
        simulation_dir (str): Path to the simulation directory containing config.json
        
    Returns:
        dict: Configuration data from the JSON file
        
    Raises:
        FileNotFoundError: If config.json doesn't exist
        json.JSONDecodeError: If config.json is invalid
    """
    config_path = os.path.join(simulation_dir, "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.json not found in {simulation_dir}")
        
    with open(config_path, 'r') as f:
        return json.load(f)

def validate_simulation_dir():
    """
    Validate that a simulation directory was provided as a command line argument.
    
    Returns:
        str: Path to the simulation directory
        
    Raises:
        SystemExit: If no directory is provided or it doesn't exist
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <simulation_directory>")
        sys.exit(1)
        
    sim_dir = sys.argv[1]
    if not os.path.exists(sim_dir):
        print(f"Directory '{sim_dir}' does not exist")
        sys.exit(1)
        
    return sim_dir 