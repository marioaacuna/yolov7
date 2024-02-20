
# Alternatively, you can run the following command in the terminal:
# python detect.py --weights D:\YOLOv7_training\pain_and_anxiety\weights\best.pt --conf 0.5 --img-size 704 --source D:/_test_YOLOv7/eval_vids/CNO_injection_685.mp4 --device 0 --save-txt --save-conf --name pain_and_anx

import subprocess
import os
from workflow.Utilities.get_conda_env import get_conda_env_path

# Define variables for the command parameters
weights = os.path.join('C:/Users/acuna/Repositories/yolov7/runs/train/yolov7-e6-custom/weights/best.pt')
conf = 0.5     # This is the confidence threshold - constant do not modify
img_size = 704 # This is the size of the images that the model was trained on so it's a constant
source_path = 'D:/_test_YOLOv7/eval_vids/' # This is the path to the video file
video_name = 'CNO_injection_685.mp4' # This is the name of the video file
source = os.path.join(source_path,video_name) # This is the path to the video file
working_directory = 'C:/Users/acuna/Repositories/yolov7/' # This is where 'detect.py' is located
env_name = 'env_yolo7' # Conda environment name
classes_file_path = './data/labels/classes.txt' # This is the path to the classes file

# Read the classes from the file and strip any whitespace
with open(classes_file_path, 'r') as file:
    classes = [line.strip() for line in file.readlines()]

class_indices = ','.join(map(str, classes))  # This converts integers to strings and then joins them
# Define the path to the Python interpreter in the env_Yolo7 Conda environment

env_path = get_conda_env_path(env_name)
if env_path:
    env_python_path = os.path.join(env_path, 'python')
    #print(f'Python path for {env_name}: {env_python_path}')
else:
    print(f'Conda environment {env_name} not found.')
    KeyError( f'Conda environment {env_name} not found.')


# Project folder
project_folder = os.path.join(source_path, 'runs/detect')
if not os.path.exists(project_folder):
    os.makedirs(project_folder)

# Construct the command with variables
args = [
    env_python_path, 'detect.py',
    '--weights', weights,
    '--conf', str(conf),
    '--img-size', str(img_size),
    '--source', source,
#    '--classes', classes,
    '--project', project_folder,
    '--device', '0',
    '--save-txt',
    '--save-conf'
]

# Let user know we will run it know
print('Running detection...')
# Execute the subprocess with the constructed arguments
process = subprocess.Popen(args, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Wait for the command to complete and capture the output
stdout, stderr = process.communicate()

# Print the outputs
print(stdout)
print(stderr)

print('Detection completed!')


# python detect.py --weights C:/Users/acuna/Repositories/yolov7/runs/train/yolov7-e6-custom/weights/best.pt --conf 0.25 --img-size 704 --source D:/_test_YOLOv7/eval_vids/CNO_injection_685.mp4 --nosave False --save-txt True --save-conf True