import subprocess
import json
import os

def get_conda_env_path(env_name):
    # Run 'conda info --json' and parse the output to JSON
    output = subprocess.run(['conda', 'info', '--json'], capture_output=True, text=True)
    conda_info = json.loads(output.stdout)

    # Get the 'envs' dict which contains paths to all conda environments
    envs_paths = conda_info.get('envs_dirs', [])
    # Iterate through the environments to find the one we're interested in
    for envs_dir in envs_paths:
        env_path = f'{envs_dir}\\{env_name}'
        return env_path if os.path.exists(env_path) else None

    # If the environment is not found, return None or raise an error
    return None

def main():
    # Example usage
    env_name = 'env_yolo7'
    env_path = get_conda_env_path(env_name)
    if env_path:
        env_python_path = os.path.join(env_path, 'python')
        print(f'Python path for {env_name}: {env_python_path}')
    else:
        print(f'Conda environment {env_name} not found.')

if __name__ == '__main__':
    main()
