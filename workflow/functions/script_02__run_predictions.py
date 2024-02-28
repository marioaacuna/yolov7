# script_02__run_predictions.py
import torch
import subprocess
import os
from Utilities.get_conda_env import get_conda_env_path  # Ensure this module is accessible

def run_detection(video_name, project_folder, 
                  source_path='D:/_test_YOLOv7/eval_vids/', 
                  weights='C:/Users/acuna/Repositories/yolov7/runs/train/yolov7-e6-custom/weights/best.pt', 
                  conf=0.5, 
                  img_size=704, 
                  env_name='env_yolo7', 
                  device='0'):
    """Run detection on a video file using YOLOv7."""
    # Construct the source path to the video file
    source = os.path.join(source_path, video_name)
    # working directory must one folder upstream to the current directory of this script
    working_directory = os.getcwd() # location of detect.py
    
    # working_directory = 'C:/Users/acuna/Repositories/yolov7/'  # Location of detect.py
    
    # Attempt to get the Conda environment's Python path
    env_path = get_conda_env_path(env_name)
    if not env_path:
        raise EnvironmentError(f"Conda environment '{env_name}' not found.")
    
    env_python_path = os.path.join(env_path, 'python')
    
    # Project folder for output
    #project_folder = os.path.join(source_path, 'runs/detect')
    #os.makedirs(project_folder, exist_ok=True)  # Ensure the directory exists
    # check if cuda is installed if not, then device = 'cpu'

    if not torch.cuda.is_available():
        device = 'cpu'

    # Construct the command with variables
    args = [
        env_python_path, 'detect.py',
        '--weights', weights,
        '--conf', str(conf),
        '--img-size', str(img_size),
        '--source', source,
        '--project', project_folder,
        '--device', device,
        '--name', video_name,
        '--save-txt',
        '--save-conf',
        '--nosave' # Do not save the output video
    ]

    print('Running detection, be patient...')
    # Execute the subprocess with the constructed arguments
    process = subprocess.Popen(args, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Wait for the command to complete and capture the output
    stdout, stderr = process.communicate()

    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    print('Detection completed!')

if __name__ == '__main__':
    # Example usage
    run_detection('CNO_injection_685.mp4')
